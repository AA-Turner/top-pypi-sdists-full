r'''
# `google_network_security_authz_policy`

Refer to the Terraform Registry for docs: [`google_network_security_authz_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy).
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


class NetworkSecurityAuthzPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy google_network_security_authz_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        location: builtins.str,
        name: builtins.str,
        target: typing.Union["NetworkSecurityAuthzPolicyTarget", typing.Dict[builtins.str, typing.Any]],
        custom_provider: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyCustomProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        http_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy google_network_security_authz_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: When the action is CUSTOM, customProvider must be specified. When the action is ALLOW, only requests matching the policy will be allowed. When the action is DENY, only requests matching the policy will be denied. When a request arrives, the policies are evaluated in the following order: 1. If there is a CUSTOM policy that matches the request, the CUSTOM policy is evaluated using the custom authorization providers and the request is denied if the provider rejects the request. 2. If there are any DENY policies that match the request, the request is denied. 3. If there are no ALLOW policies for the resource or if any of the ALLOW policies match the request, the request is allowed. 4. Else the request is denied by default if none of the configured AuthzPolicies with ALLOW action match the request. Possible values: ["ALLOW", "DENY", "CUSTOM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#action NetworkSecurityAuthzPolicy#action}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#location NetworkSecurityAuthzPolicy#location}
        :param name: Identifier. Name of the AuthzPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#name NetworkSecurityAuthzPolicy#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#target NetworkSecurityAuthzPolicy#target}
        :param custom_provider: custom_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#custom_provider NetworkSecurityAuthzPolicy#custom_provider}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#description NetworkSecurityAuthzPolicy#description}
        :param http_rules: http_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#http_rules NetworkSecurityAuthzPolicy#http_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#id NetworkSecurityAuthzPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the AuthzExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#labels NetworkSecurityAuthzPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#project NetworkSecurityAuthzPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#timeouts NetworkSecurityAuthzPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5b682aefe4d148fc59c51c68d15a27401334ef7498b49b1b4704527f3fd6ab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkSecurityAuthzPolicyConfig(
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
        '''Generates CDKTF code for importing a NetworkSecurityAuthzPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkSecurityAuthzPolicy to import.
        :param import_from_id: The id of the existing NetworkSecurityAuthzPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkSecurityAuthzPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524e719387501ff5db891f23a732441444950951b4061e9ee8ec88746d7937f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomProvider")
    def put_custom_provider(
        self,
        *,
        authz_extension: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyCustomProviderAuthzExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_iap: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyCustomProviderCloudIap", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authz_extension: authz_extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#authz_extension NetworkSecurityAuthzPolicy#authz_extension}
        :param cloud_iap: cloud_iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#cloud_iap NetworkSecurityAuthzPolicy#cloud_iap}
        '''
        value = NetworkSecurityAuthzPolicyCustomProvider(
            authz_extension=authz_extension, cloud_iap=cloud_iap
        )

        return typing.cast(None, jsii.invoke(self, "putCustomProvider", [value]))

    @jsii.member(jsii_name="putHttpRules")
    def put_http_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0460c4bc9a2a12955b86ef412b039bb37e6523bd6b3e9725876ab9418da6e9ac)
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
        :param load_balancing_scheme: All gateways and forwarding rules referenced by this policy and extensions must share the same load balancing scheme. For more information, refer to `Backend services overview <https://cloud.google.com/load-balancing/docs/backend-service>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#load_balancing_scheme NetworkSecurityAuthzPolicy#load_balancing_scheme}
        :param resources: A list of references to the Forwarding Rules on which this policy will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        value = NetworkSecurityAuthzPolicyTarget(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#create NetworkSecurityAuthzPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#delete NetworkSecurityAuthzPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#update NetworkSecurityAuthzPolicy#update}.
        '''
        value = NetworkSecurityAuthzPolicyTimeouts(
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
    ) -> "NetworkSecurityAuthzPolicyCustomProviderOutputReference":
        return typing.cast("NetworkSecurityAuthzPolicyCustomProviderOutputReference", jsii.get(self, "customProvider"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="httpRules")
    def http_rules(self) -> "NetworkSecurityAuthzPolicyHttpRulesList":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesList", jsii.get(self, "httpRules"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "NetworkSecurityAuthzPolicyTargetOutputReference":
        return typing.cast("NetworkSecurityAuthzPolicyTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkSecurityAuthzPolicyTimeoutsOutputReference":
        return typing.cast("NetworkSecurityAuthzPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["NetworkSecurityAuthzPolicyCustomProvider"]:
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyCustomProvider"], jsii.get(self, "customProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpRulesInput")
    def http_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRules"]]], jsii.get(self, "httpRulesInput"))

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
    def target_input(self) -> typing.Optional["NetworkSecurityAuthzPolicyTarget"]:
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkSecurityAuthzPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkSecurityAuthzPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882e4ec1c352ff1cf7c22ceb78335ec6bee83d180c52bb42b0e749bbc7aa5de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d96f0b9182a2e5a2e45f6cc7277314d955ea6db98870e74d399a3a0a5242374)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6349695530f6146c3aca61b0a2a5b47208e4b019d1ed1abb9aadafaf8adbe2de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449f17a18bd5ad21d72f173f9730879e6e72934294590aa8175f6572c8c3335e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9900cb0c82fa36d88f08171acd2de61140f822dd478f5c5a20ff663f26ab66c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf511e649a1ec4ecf8f77abea6999b9a70e36c22e352bb2aa231da6b01ccc43a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2f99e2342b2b516257b455e04422d6eca1b4b8b84ca22873c568312111bfcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyConfig",
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
class NetworkSecurityAuthzPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        target: typing.Union["NetworkSecurityAuthzPolicyTarget", typing.Dict[builtins.str, typing.Any]],
        custom_provider: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyCustomProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        http_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: When the action is CUSTOM, customProvider must be specified. When the action is ALLOW, only requests matching the policy will be allowed. When the action is DENY, only requests matching the policy will be denied. When a request arrives, the policies are evaluated in the following order: 1. If there is a CUSTOM policy that matches the request, the CUSTOM policy is evaluated using the custom authorization providers and the request is denied if the provider rejects the request. 2. If there are any DENY policies that match the request, the request is denied. 3. If there are no ALLOW policies for the resource or if any of the ALLOW policies match the request, the request is allowed. 4. Else the request is denied by default if none of the configured AuthzPolicies with ALLOW action match the request. Possible values: ["ALLOW", "DENY", "CUSTOM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#action NetworkSecurityAuthzPolicy#action}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#location NetworkSecurityAuthzPolicy#location}
        :param name: Identifier. Name of the AuthzPolicy resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#name NetworkSecurityAuthzPolicy#name}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#target NetworkSecurityAuthzPolicy#target}
        :param custom_provider: custom_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#custom_provider NetworkSecurityAuthzPolicy#custom_provider}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#description NetworkSecurityAuthzPolicy#description}
        :param http_rules: http_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#http_rules NetworkSecurityAuthzPolicy#http_rules}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#id NetworkSecurityAuthzPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of labels associated with the AuthzExtension resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#labels NetworkSecurityAuthzPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#project NetworkSecurityAuthzPolicy#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#timeouts NetworkSecurityAuthzPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(target, dict):
            target = NetworkSecurityAuthzPolicyTarget(**target)
        if isinstance(custom_provider, dict):
            custom_provider = NetworkSecurityAuthzPolicyCustomProvider(**custom_provider)
        if isinstance(timeouts, dict):
            timeouts = NetworkSecurityAuthzPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1f0d9144aad0177f70fb5f9ecd68b6863394c4542c0ce1cef0362be0ec7d963)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#action NetworkSecurityAuthzPolicy#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#location NetworkSecurityAuthzPolicy#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Identifier. Name of the AuthzPolicy resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#name NetworkSecurityAuthzPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> "NetworkSecurityAuthzPolicyTarget":
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#target NetworkSecurityAuthzPolicy#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("NetworkSecurityAuthzPolicyTarget", result)

    @builtins.property
    def custom_provider(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyCustomProvider"]:
        '''custom_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#custom_provider NetworkSecurityAuthzPolicy#custom_provider}
        '''
        result = self._values.get("custom_provider")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyCustomProvider"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#description NetworkSecurityAuthzPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRules"]]]:
        '''http_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#http_rules NetworkSecurityAuthzPolicy#http_rules}
        '''
        result = self._values.get("http_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRules"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#id NetworkSecurityAuthzPolicy#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#labels NetworkSecurityAuthzPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#project NetworkSecurityAuthzPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkSecurityAuthzPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#timeouts NetworkSecurityAuthzPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyCustomProvider",
    jsii_struct_bases=[],
    name_mapping={"authz_extension": "authzExtension", "cloud_iap": "cloudIap"},
)
class NetworkSecurityAuthzPolicyCustomProvider:
    def __init__(
        self,
        *,
        authz_extension: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyCustomProviderAuthzExtension", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_iap: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyCustomProviderCloudIap", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authz_extension: authz_extension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#authz_extension NetworkSecurityAuthzPolicy#authz_extension}
        :param cloud_iap: cloud_iap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#cloud_iap NetworkSecurityAuthzPolicy#cloud_iap}
        '''
        if isinstance(authz_extension, dict):
            authz_extension = NetworkSecurityAuthzPolicyCustomProviderAuthzExtension(**authz_extension)
        if isinstance(cloud_iap, dict):
            cloud_iap = NetworkSecurityAuthzPolicyCustomProviderCloudIap(**cloud_iap)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c04903da53856c5904a2b1bbe61a80c251e1bd0204eb31c80189a66326929f)
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
    ) -> typing.Optional["NetworkSecurityAuthzPolicyCustomProviderAuthzExtension"]:
        '''authz_extension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#authz_extension NetworkSecurityAuthzPolicy#authz_extension}
        '''
        result = self._values.get("authz_extension")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyCustomProviderAuthzExtension"], result)

    @builtins.property
    def cloud_iap(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyCustomProviderCloudIap"]:
        '''cloud_iap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#cloud_iap NetworkSecurityAuthzPolicy#cloud_iap}
        '''
        result = self._values.get("cloud_iap")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyCustomProviderCloudIap"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyCustomProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyCustomProviderAuthzExtension",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources"},
)
class NetworkSecurityAuthzPolicyCustomProviderAuthzExtension:
    def __init__(self, *, resources: typing.Sequence[builtins.str]) -> None:
        '''
        :param resources: A list of references to authorization extensions that will be invoked for requests matching this policy. Limited to 1 custom provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7402158dc10a8e9258482876989913285ac33f7416bf18fd3c5be996f2c1a4e5)
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resources": resources,
        }

    @builtins.property
    def resources(self) -> typing.List[builtins.str]:
        '''A list of references to authorization extensions that will be invoked for requests matching this policy.

        Limited to 1 custom provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyCustomProviderAuthzExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30c44d2ebeb48091acd29cfbd18c9d0285cbcf216143b82f13fa88510cc9734f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9b7251979a99da2a5c3f3bf6511d6237022c768052e473075978c2bf7396176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyCustomProviderAuthzExtension]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyCustomProviderAuthzExtension], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyCustomProviderAuthzExtension],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f949a9cb1af4a85b98d12d957432ffe8410518daa6d3ca26dc13cca17e043e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyCustomProviderCloudIap",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class NetworkSecurityAuthzPolicyCustomProviderCloudIap:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Enable Cloud IAP at the AuthzPolicy level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#enabled NetworkSecurityAuthzPolicy#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a3456d47b995ef7cf0237c3f34789674d58893cd4cfe9dcc69f019aabdb225)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Enable Cloud IAP at the AuthzPolicy level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#enabled NetworkSecurityAuthzPolicy#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyCustomProviderCloudIap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13fec207955061629dd3e0b840a2f0dc65feea49445d22fff4bc787e83797fde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c11757c0ff2a7d38920d076fb9b8b516100bc74afddbc5d88d9e9e6ea13cfd7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyCustomProviderCloudIap]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyCustomProviderCloudIap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyCustomProviderCloudIap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b3d4e0be96473137ce3691cbd573121d45ce192efb4ded831e1fe4947c529c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyCustomProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyCustomProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__876db6207232bfd6dc6b2627777ddef29dbf279de5731ea3a08763a9fef440d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthzExtension")
    def put_authz_extension(self, *, resources: typing.Sequence[builtins.str]) -> None:
        '''
        :param resources: A list of references to authorization extensions that will be invoked for requests matching this policy. Limited to 1 custom provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        value = NetworkSecurityAuthzPolicyCustomProviderAuthzExtension(
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
        :param enabled: Enable Cloud IAP at the AuthzPolicy level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#enabled NetworkSecurityAuthzPolicy#enabled}
        '''
        value = NetworkSecurityAuthzPolicyCustomProviderCloudIap(enabled=enabled)

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
    ) -> NetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference:
        return typing.cast(NetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference, jsii.get(self, "authzExtension"))

    @builtins.property
    @jsii.member(jsii_name="cloudIap")
    def cloud_iap(
        self,
    ) -> NetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference:
        return typing.cast(NetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference, jsii.get(self, "cloudIap"))

    @builtins.property
    @jsii.member(jsii_name="authzExtensionInput")
    def authz_extension_input(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyCustomProviderAuthzExtension]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyCustomProviderAuthzExtension], jsii.get(self, "authzExtensionInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudIapInput")
    def cloud_iap_input(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyCustomProviderCloudIap]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyCustomProviderCloudIap], jsii.get(self, "cloudIapInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyCustomProvider]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyCustomProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyCustomProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0655fb2749cb529db667a1a80502e2c64db858f9468c20d55acc7c6d59b9f28a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRules",
    jsii_struct_bases=[],
    name_mapping={"from_": "from", "to": "to", "when": "when"},
)
class NetworkSecurityAuthzPolicyHttpRules:
    def __init__(
        self,
        *,
        from_: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFrom", typing.Dict[builtins.str, typing.Any]]] = None,
        to: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesTo", typing.Dict[builtins.str, typing.Any]]] = None,
        when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_: from block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#from NetworkSecurityAuthzPolicy#from}
        :param to: to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#to NetworkSecurityAuthzPolicy#to}
        :param when: CEL expression that describes the conditions to be satisfied for the action. The result of the CEL expression is ANDed with the from and to. Refer to the CEL language reference for a list of available attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#when NetworkSecurityAuthzPolicy#when}
        '''
        if isinstance(from_, dict):
            from_ = NetworkSecurityAuthzPolicyHttpRulesFrom(**from_)
        if isinstance(to, dict):
            to = NetworkSecurityAuthzPolicyHttpRulesTo(**to)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4899d07a04516b9bae5b90d7dfc900801a1dc6ad8fdb664e61fe1c392f23b4)
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
    def from_(self) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFrom"]:
        '''from block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#from NetworkSecurityAuthzPolicy#from}
        '''
        result = self._values.get("from_")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFrom"], result)

    @builtins.property
    def to(self) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesTo"]:
        '''to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#to NetworkSecurityAuthzPolicy#to}
        '''
        result = self._values.get("to")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesTo"], result)

    @builtins.property
    def when(self) -> typing.Optional[builtins.str]:
        '''CEL expression that describes the conditions to be satisfied for the action.

        The result of the CEL expression is ANDed with the from and to. Refer to the CEL language reference for a list of available attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#when NetworkSecurityAuthzPolicy#when}
        '''
        result = self._values.get("when")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFrom",
    jsii_struct_bases=[],
    name_mapping={"not_sources": "notSources", "sources": "sources"},
)
class NetworkSecurityAuthzPolicyHttpRulesFrom:
    def __init__(
        self,
        *,
        not_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromNotSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromSources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param not_sources: not_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#not_sources NetworkSecurityAuthzPolicy#not_sources}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#sources NetworkSecurityAuthzPolicy#sources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb93ed401a52343dfcd3e8632fcfe5c380b3b2c49b2c0122d81e8136e6aba3d5)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSources"]]]:
        '''not_sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#not_sources NetworkSecurityAuthzPolicy#not_sources}
        '''
        result = self._values.get("not_sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSources"]]], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSources"]]]:
        '''sources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#sources NetworkSecurityAuthzPolicy#sources}
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSources",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals", "resources": "resources"},
)
class NetworkSecurityAuthzPolicyHttpRulesFromNotSources:
    def __init__(
        self,
        *,
        principals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param principals: principals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#principals NetworkSecurityAuthzPolicy#principals}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8071a14b4870e8b03826de281dfc08236065de6b052387c574e64013f4218041)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals"]]]:
        '''principals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#principals NetworkSecurityAuthzPolicy#principals}
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals"]]], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources"]]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromNotSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__266fefa873b8a6e28d505e41f25ced04ccaf4cc7c001f5fb099c2f18b5d1185f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cebeb061bb0e76dbd471b8aceef401f3dfc31811ab25afeefe586b5e58331eba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aaab2e7c87b631f47206aea22e05c99956448e0697c06e560966bc48a14c4fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec64604a53d1e45c9552b2f88c8efefc3b46d3221e969e433d3811c43fe643b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ce5c1e25a9ffb056b5ba9e8759c3fdd83a845ea9cf36d7e933aa734ce89ad0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d41f9af96484fd9b542df51bc8952fcdab6bd5966d7b83d25e2a623adc522c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a6d62201a308d5001ba32843cd52ff8f1529c6b7f9b83d5276bbbc5c716043f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPrincipals")
    def put_principals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbcafbf091f8bc16ee9702617434c7476cfc04f32c415615c734fa06c77d3a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrincipals", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a82576d8d31b7a5de76c7c2b21bcd9979930e758cca2fe455d61cfc05b692c)
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
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList", jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="principalsInput")
    def principals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals"]]], jsii.get(self, "principalsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2028504086df7381fe244fd3252c09d08decdedfc6ce6d2e06721b08ae6149a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a3d0f0eaed2e161d23d8d6a9de0cc0ae7f33199f8ef2b8b5508e1cb3d5dffa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b39b8f8922b5820d4a288588c6aac1685d89e782baae59bbbdd396ddf609575)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b2be2ad811068877412f52508455716af920ed441e14ebd25a7ee2749f9b65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5a91f1e2e262d1861d2aad0d7be873929d0cb48893d70cb5f157671d1f90b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3caf1cf8d8f2a4349f444bb664e0cdafc724ac0fc5c3db091a726c07e934f9e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7418b4fde4e63f89e94b5719b9af0a64e9d2c59082aa5fe3922403405a44b488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea0bb2abe91bb7ed1477c1ee6c99b16e659fbd5773862cab7911742580d08f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaf32d2c94a853e65fa29b74c0d87b720caaefe2308d82bfffbe9e738d59a01b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3584dd77a8e0432099f8ced77674508edab64b3dc964c880454aa7baee29389e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29c9ec471cde6638abc46e275c3bee922736a89b3ce2b9c34c2a77866b736e8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__227f15759e8db669aee820acd48ae47d7364d189893273fa9a2683db28f1b2d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20da40a0e2e06040d673ac4e7559da781d62f2927d3767010fea495e7c842d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea199583baa79f191f649e6aa8e988a9c0b54e28f3053aff4c6c7652c4129118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9169d7d46a6b80cba8aab9cef7dacd627aa174cf0184fefb517570d75ee841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources",
    jsii_struct_bases=[],
    name_mapping={
        "iam_service_account": "iamServiceAccount",
        "tag_value_id_set": "tagValueIdSet",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources:
    def __init__(
        self,
        *,
        iam_service_account: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_value_id_set: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iam_service_account: iam_service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#iam_service_account NetworkSecurityAuthzPolicy#iam_service_account}
        :param tag_value_id_set: tag_value_id_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#tag_value_id_set NetworkSecurityAuthzPolicy#tag_value_id_set}
        '''
        if isinstance(iam_service_account, dict):
            iam_service_account = NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount(**iam_service_account)
        if isinstance(tag_value_id_set, dict):
            tag_value_id_set = NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet(**tag_value_id_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd2e2937095ffd9433279b4492fa76c9c89e23f96a993ea293294d05167aed9)
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
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount"]:
        '''iam_service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#iam_service_account NetworkSecurityAuthzPolicy#iam_service_account}
        '''
        result = self._values.get("iam_service_account")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount"], result)

    @builtins.property
    def tag_value_id_set(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet"]:
        '''tag_value_id_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#tag_value_id_set NetworkSecurityAuthzPolicy#tag_value_id_set}
        '''
        result = self._values.get("tag_value_id_set")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7969b937adf36be994fb80545ae6fb4494071bfdf7c3e59ab69c88081b9ac5b4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c35cce7777b8fe4e18e2a7b0d35def99173d6b0edcfe269eb952470bacd003d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8143ae674dfc2a9be36517e39a2b21772153f499487b15a9ec6ed79793d15f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0459e7005f055dd74a11d6da447ae151574909cddacb4d7d577a5ec0e3cefab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d29f2010fd8f633e7f094fe735613e2b77400148410e1ad36ec5c4baa16841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7111f7a904907db961547709cc377a1f52e4d6f4975d57a7fd1dcf20bb44d7f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7310fa0a64c9ad4d0cf8d2bb9d016ee3e1d5ebfcd41dbd66dac006736881790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642d3e34c2583b8981fa38da84cb057424bbe9f70c354a80b4282390fd3b6988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3960d999e1cfa60dfe69bd8f36a54159d9f21a27fd8484d23674e3533bc8ad58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741e9619018a4a26394cc5870238dbc2232a0573b7e05d7ae2f38cab7b809cc5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00af9602228989f97b6c3329716bb7b17e38325528c2d25d9e419c6c3e65347)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bd9be09623268c89a9bf500abfcd193a4a9066d62794f01fb8d3c6c5fdedb10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__181cfaf86de44140ab4b0dfb28d4be601d376394fdfc22bc336bd559dc25bec7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5092f50ea67851b6f829ccae378d7e1cee08d612ed012d8f951bdfee9971658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45a5c543fde938b3c32579399f5f00221302d1c50b845fada3c3e3859aed169d)
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount(
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
        :param ids: A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request. The match follows AND semantics which means all the ids must match. Limited to 5 matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ids NetworkSecurityAuthzPolicy#ids}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet(
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
    ) -> NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference, jsii.get(self, "iamServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="tagValueIdSet")
    def tag_value_id_set(
        self,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference", jsii.get(self, "tagValueIdSet"))

    @builtins.property
    @jsii.member(jsii_name="iamServiceAccountInput")
    def iam_service_account_input(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount], jsii.get(self, "iamServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueIdSetInput")
    def tag_value_id_set_input(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet"]:
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet"], jsii.get(self, "tagValueIdSetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bdca4f84c1f8766cf51483e34280dd4f92ef9bd0e8cdecb878e2f50bc47867d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet",
    jsii_struct_bases=[],
    name_mapping={"ids": "ids"},
)
class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet:
    def __init__(
        self,
        *,
        ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ids: A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request. The match follows AND semantics which means all the ids must match. Limited to 5 matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ids NetworkSecurityAuthzPolicy#ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eede2a0c13905a01d402780cc37a64780f57e212067db22e98962c716241046)
            check_type(argname="argument ids", value=ids, expected_type=type_hints["ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ids is not None:
            self._values["ids"] = ids

    @builtins.property
    def ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request.

        The match follows AND semantics which means all the ids must match.
        Limited to 5 matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ids NetworkSecurityAuthzPolicy#ids}
        '''
        result = self._values.get("ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6741eda7d00c1ab3aacf103cad2ed8140e36d327a59e69eccff643374bea7c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__382eea6b9f67cc59d6ae2a95217ac71d31bea1bfd523193f0f17c5b4e8777a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14afc194324e4e6ad9d7ec0ba87e0764ae0b34ad0067070f8471238be8b3833b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f60294e19dd6a44d72b5c1605ec7300a4d5c817e3e3ce495cca3721863101f0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotSources")
    def put_not_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSources, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8266ec049fe93a75914d30e56b5224e538b582d9d19355871b471e51831b30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotSources", [value]))

    @jsii.member(jsii_name="putSources")
    def put_sources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromSources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ee4d15e3cca7ec97e9dbe8e2fa541e71c8cf3e1a9e55de8429984f9f6457cd)
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
    def not_sources(self) -> NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList, jsii.get(self, "notSources"))

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> "NetworkSecurityAuthzPolicyHttpRulesFromSourcesList":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromSourcesList", jsii.get(self, "sources"))

    @builtins.property
    @jsii.member(jsii_name="notSourcesInput")
    def not_sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSources]]], jsii.get(self, "notSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourcesInput")
    def sources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSources"]]], jsii.get(self, "sourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFrom]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFrom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFrom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b33db9ad2a9437a6cce9bdf071a1d9954cf77371ccd5664b4715a5544759792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSources",
    jsii_struct_bases=[],
    name_mapping={"principals": "principals", "resources": "resources"},
)
class NetworkSecurityAuthzPolicyHttpRulesFromSources:
    def __init__(
        self,
        *,
        principals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param principals: principals block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#principals NetworkSecurityAuthzPolicy#principals}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202ad195ef6ed01a7e191d41a985c65dda904d59c572ed4785827c5ee6a8e291)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals"]]]:
        '''principals block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#principals NetworkSecurityAuthzPolicy#principals}
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals"]]], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources"]]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesFromSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe3d00cbae446d2a0525560bff5d637f0904b3d03f492cbcf530192adc134c41)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd848eee9dfebad6312a7ee924b493744d47d99be77413e263c2163381f5a50)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9630f19d640ffc33eb025c954ab218449dc71a0947961d447765c862e74092d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e185633221dab2feef015b337d85d5ff4ec07c6bd5f14e789b6a7b677ee8506)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aabd6b44ca47edd50792034e9c5e2f304219d2271f5c31e3d4fa66bf0096fd18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c085afb184dab90bcc382843f9a1310cc6e95bd1d4746eef95610daa26ba1cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec6241d55a1316301a86426a2f88f4bf7c6c23302b5dee742686a611b257c57b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPrincipals")
    def put_principals(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1727963e9de87a0c01f93037b79cd8a1fd28f1e617f9f69dc36c56e343b3df7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrincipals", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b409a64245e09dd4c66951684ba257cc14fc9bde51b800b33cb84430f729aa2)
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
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList", jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="principalsInput")
    def principals_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals"]]], jsii.get(self, "principalsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0de0ebaec27c0658836792dec5e6a8549dfbb5f5aec7a200552a51ebcc7a6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a780786761e8ceaf7f21fcb9e7162eadca6970c7e4e9b379fed536796f1fdfa7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__726d170e106ca8c410f77627449bebc5136251274721d9fe96fc471d08210d9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95abec1acd1d41647391a94f9e68cd9fcc0a02e8c99fb6e99fa944577b898e68)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6000652c64fa8a95da2b7e37975623c82c39cd6da1fcf864c863b64a8f6e509)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fb6d04fbb09c948a6649b8708497abc40aca246b5f65646769d9f9e59a19b22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__470ea010777af4c6e668f0f2bc6d9726fd1970d017d31b9dbf9930ca5f3b5c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb23bdc9006f55f0dcea7a28510fb4dcde7d54e377b335a8bd8a557cbbdef9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45613272cc99a0681d75020c052eebf3aa50feec21bf6cf44e478d80c0e33010)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d7061e7cc2c165bbc7e88a6338002631bce303cad23988dcd60548788aaf093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24dc9f68eb103e7784e72ab666a1d7c76e936389ceaeebc85f364bcd03f64c1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a04e27a40922fb05617e35d4b790c323fbe3a24438420ac86183ca0f27f7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57bfc78be589c22ff2d81bf90b22244d8b686318a716d017fff8bdc8421d8f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6e97a96c2ba62f998370199504d412c420baa07b04eef3c6d7458623f43ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a3056f91b6df5d4ed5be16f7770ce58fbb3049dd15e13c9bd66bc4acd42073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources",
    jsii_struct_bases=[],
    name_mapping={
        "iam_service_account": "iamServiceAccount",
        "tag_value_id_set": "tagValueIdSet",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources:
    def __init__(
        self,
        *,
        iam_service_account: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_value_id_set: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iam_service_account: iam_service_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#iam_service_account NetworkSecurityAuthzPolicy#iam_service_account}
        :param tag_value_id_set: tag_value_id_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#tag_value_id_set NetworkSecurityAuthzPolicy#tag_value_id_set}
        '''
        if isinstance(iam_service_account, dict):
            iam_service_account = NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount(**iam_service_account)
        if isinstance(tag_value_id_set, dict):
            tag_value_id_set = NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet(**tag_value_id_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66881cc7537b81465fcc56a4d08d801beeb03c15f1afa04e8c70912b8d1c38a9)
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
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount"]:
        '''iam_service_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#iam_service_account NetworkSecurityAuthzPolicy#iam_service_account}
        '''
        result = self._values.get("iam_service_account")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount"], result)

    @builtins.property
    def tag_value_id_set(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet"]:
        '''tag_value_id_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#tag_value_id_set NetworkSecurityAuthzPolicy#tag_value_id_set}
        '''
        result = self._values.get("tag_value_id_set")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180a0d51fadca1f7abe2bb927ee2bbfe81c3d2a1abb55dd82867265bf93bfa17)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c8e4514f779844b03f847bc32129a8a3e455f74cf003263b4153584d263f29e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1ce92936f1914d1161d17984bc9b7f4810af8b8be5a104285ae838008d1e45b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac1a26d0848499c70958cf1bfdd649e50ce8064e83c43517c92004b755e77b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5c83b72f95a78db2431cbe0b82e1cbe3b7063bde3b23374ebd5ca78b2bf92a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a91be37b107b8cf86ec0273f941f5e3511df6ca37de48b9887b05cf092bc543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc3879a8fd51f6a3ba2d3f9b0f5eb0092b2f0937675fd3b84f6a9af404addc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19f35e1af33ad174a48366a5beca436c5d8c6bb888f1a9d8e5445b5402fba5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31d83ff053430042a147bc423a0d88e278f0166815a7921efc9cab2e1231515f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65857d900e1964147e65a4c29c42b51434ba438d4fc3c007a966ad0c541e6cc2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4fcb17cdcedc904858075cf7ccbc4a6ec1b6593cb76bff4f17d4a9de8507cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efa0b027951d329f491dbabb5939409635b423230a5d9bfcd75daa9fde5cd324)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e8b4b4b0aa7013e39bb7215b40e6f6e6b17ad1c24cd47214e5b747704798067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcef953ae9bb92fc1bc9a00e35fbd4e3d61c67f5fa5fec732f2f653f3e09c5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ea1ea4c2f5d606e8b449e462b042770f97b9e39d3e8302d439c1de415edcbaa)
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount(
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
        :param ids: A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request. The match follows AND semantics which means all the ids must match. Limited to 5 matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ids NetworkSecurityAuthzPolicy#ids}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet(
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
    ) -> NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference, jsii.get(self, "iamServiceAccount"))

    @builtins.property
    @jsii.member(jsii_name="tagValueIdSet")
    def tag_value_id_set(
        self,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference", jsii.get(self, "tagValueIdSet"))

    @builtins.property
    @jsii.member(jsii_name="iamServiceAccountInput")
    def iam_service_account_input(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount], jsii.get(self, "iamServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueIdSetInput")
    def tag_value_id_set_input(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet"]:
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet"], jsii.get(self, "tagValueIdSetInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce94d9c5b0418bedf688b700aa6b90d0d7a9fb0a9a016de10b718e70997bd89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet",
    jsii_struct_bases=[],
    name_mapping={"ids": "ids"},
)
class NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet:
    def __init__(
        self,
        *,
        ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ids: A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request. The match follows AND semantics which means all the ids must match. Limited to 5 matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ids NetworkSecurityAuthzPolicy#ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e721368ea7ab364a176631e742b938d58d2288608c751f2833d5aaa58f692ca7)
            check_type(argname="argument ids", value=ids, expected_type=type_hints["ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ids is not None:
            self._values["ids"] = ids

    @builtins.property
    def ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of resource tag value permanent IDs to match against the resource manager tags value associated with the source VM of a request.

        The match follows AND semantics which means all the ids must match.
        Limited to 5 matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ids NetworkSecurityAuthzPolicy#ids}
        '''
        result = self._values.get("ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cc9f4350be4bf9e7cab8e3e9c8acdb901924d309ed654544b4e559d3680251b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ffb3327a9eaeab812b300a7eeaeeba05320663b119ebf568fc0106608cac049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9740f6afb333486a2ec00ea8cddb8c9dc2eb731e9299caa68007bd4d94175fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0ce2ee4e591ed54563a178179adb5a539925130da3da110b555768ee84a4ad1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8de59bdbb994d69e618af54c96120c301bf5b3b62eb41cadf166855c9943dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f464ece72f3a979a4f50a74d9ceec5d69544efbfcdbec91390abefb86d3a55b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b06007bb57d7ed10fedcc818a348e3962a1f94b4920a81374a254ed04e0d4245)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a50983ce2e4cd836cb650eacd75c5be8b06d6bd3577c9de2a49738eb7f196b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a58546cb8ff88abaf08d10c727f912045677d28d955327e539f84f37c48f7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97be5e72d79e641544fa8d0dc11a98c9a4cec3dbbcfeda91a5fc7c0f4a3a2f86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFrom")
    def put_from(
        self,
        *,
        not_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
        sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param not_sources: not_sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#not_sources NetworkSecurityAuthzPolicy#not_sources}
        :param sources: sources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#sources NetworkSecurityAuthzPolicy#sources}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesFrom(
            not_sources=not_sources, sources=sources
        )

        return typing.cast(None, jsii.invoke(self, "putFrom", [value]))

    @jsii.member(jsii_name="putTo")
    def put_to(
        self,
        *,
        not_operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToNotOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param not_operations: not_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#not_operations NetworkSecurityAuthzPolicy#not_operations}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#operations NetworkSecurityAuthzPolicy#operations}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesTo(
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
    def from_(self) -> NetworkSecurityAuthzPolicyHttpRulesFromOutputReference:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesFromOutputReference, jsii.get(self, "from"))

    @builtins.property
    @jsii.member(jsii_name="to")
    def to(self) -> "NetworkSecurityAuthzPolicyHttpRulesToOutputReference":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToOutputReference", jsii.get(self, "to"))

    @builtins.property
    @jsii.member(jsii_name="fromInput")
    def from_input(self) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFrom]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFrom], jsii.get(self, "fromInput"))

    @builtins.property
    @jsii.member(jsii_name="toInput")
    def to_input(self) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesTo"]:
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesTo"], jsii.get(self, "toInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7ce528304448b69ff346f53ee635ffa94806802b747736ac2cffaf647df6b14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "when", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a55279d7f39d70f03eeb7449af09de13875d07f5794f123d9c78b9dd2e5b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesTo",
    jsii_struct_bases=[],
    name_mapping={"not_operations": "notOperations", "operations": "operations"},
)
class NetworkSecurityAuthzPolicyHttpRulesTo:
    def __init__(
        self,
        *,
        not_operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToNotOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToOperations", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param not_operations: not_operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#not_operations NetworkSecurityAuthzPolicy#not_operations}
        :param operations: operations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#operations NetworkSecurityAuthzPolicy#operations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fabfdd6312e5ee01cc9c9b9895e4ae8dc280327d3f1a8700fcb5e481e468861)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperations"]]]:
        '''not_operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#not_operations NetworkSecurityAuthzPolicy#not_operations}
        '''
        result = self._values.get("not_operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperations"]]], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperations"]]]:
        '''operations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#operations NetworkSecurityAuthzPolicy#operations}
        '''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperations"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperations",
    jsii_struct_bases=[],
    name_mapping={
        "header_set": "headerSet",
        "hosts": "hosts",
        "methods": "methods",
        "paths": "paths",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesToNotOperations:
    def __init__(
        self,
        *,
        header_set: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet", typing.Dict[builtins.str, typing.Any]]] = None,
        hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param header_set: header_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#header_set NetworkSecurityAuthzPolicy#header_set}
        :param hosts: hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#hosts NetworkSecurityAuthzPolicy#hosts}
        :param methods: A list of HTTP methods to match against. Each entry must be a valid HTTP method name (GET, PUT, POST, HEAD, PATCH, DELETE, OPTIONS). It only allows exact match and is always case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#methods NetworkSecurityAuthzPolicy#methods}
        :param paths: paths block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#paths NetworkSecurityAuthzPolicy#paths}
        '''
        if isinstance(header_set, dict):
            header_set = NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet(**header_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68bd6ad31e87746ebbda2ae205a5829ba3c84e6db7e83670d906e652fdc4913)
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
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet"]:
        '''header_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#header_set NetworkSecurityAuthzPolicy#header_set}
        '''
        result = self._values.get("header_set")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet"], result)

    @builtins.property
    def hosts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts"]]]:
        '''hosts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#hosts NetworkSecurityAuthzPolicy#hosts}
        '''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts"]]], result)

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of HTTP methods to match against.

        Each entry must be a valid HTTP method name (GET, PUT, POST, HEAD, PATCH, DELETE, OPTIONS). It only allows exact match and is always case sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#methods NetworkSecurityAuthzPolicy#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths"]]]:
        '''paths block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#paths NetworkSecurityAuthzPolicy#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToNotOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers"},
)
class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#headers NetworkSecurityAuthzPolicy#headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed882854635e84c42cf02d8dc9d009e0d7b26f1c85cb1bd0b703db551f29e8f)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#headers NetworkSecurityAuthzPolicy#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Specifies the name of the header in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#name NetworkSecurityAuthzPolicy#name}
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#value NetworkSecurityAuthzPolicy#value}
        '''
        if isinstance(value, dict):
            value = NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9f7a93f8fe4855c1ae7ad75a772341aa6e786f40af276cbc7af9265985b841)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#name NetworkSecurityAuthzPolicy#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#value NetworkSecurityAuthzPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__317c8602bcef2b1dac1c3335a287bd7e3b992719bff106d46593da9833e21142)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3f54826846bef204e36e6bb00c75f75561b67b378b2e90216250b2ebed8516)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c44048e32a2949bb963efe5c91b64e1e49c4076c28a5e07f8ae1f870fd83c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b0b3fda1be32b9d88ffe14bb619f37915d2abe2942bb6d2e7fa169925e0bf15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad8cb3dfd0f0a85a2883de72a433a0bdbd99d3c27e70a0628a86cb48b4bb7d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e858c867fd937ba2240032f124a2d2dcdd168060bfb5d2c558d1102dc391b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fe5f25e89f3eb3573d8adebf22fc5cac6f3af6d8022966fcf4fb7b90b0b2602)
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue(
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
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue"]:
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db34ab3a5144bbd6fe52e7150c27d22020946d6692855b79c285cbab6e898ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e48682de5c59baba4dec7510eea60720c793dfda797f46fb27b03b3122d4f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58b4d2ed02448a4eecf870fc4efcd9287e94b96d87536450c9bcd80671b18ed)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a3de8072a4d2f8d0b8573716a1b44b10513337b5cc4e928d340606b1435d38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__618c313af05b9c862e2c813ead7aecec92b112df2ee8625deaf0dfa7beb92555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84370ceee9154e07c498c6987b5eecbd534e248d9beb9fe0348b3bb297066f5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ad5cfa06c5acffb5e13f3aeb55169b61d8676ecd9025cfcd252e90a087324a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c10b2daf155f3955e59d5e516ae57192bc27c918a20ba98a863e86d2ddff56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c68e427de757e54f26b05f5b8a838fea0d143692f018ab589a85a6f9f7ecb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e2f2ffdf3bc209ef0d2eee01b6e33ce6db8302ba0c59867d4537ab4333bb2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b6b212126715af27e5a828a343e31654779f47386481d1af4d7d784056cf7dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39ec376dc0d1dcd9640fab0e69a614147e0ca2498853b2871c4d3e395e13e165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(
        self,
    ) -> NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2331005435a3f1b9e08dea509a92d0c2205c8e5097801df0310ea8eddbae4fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d276d66bdc04152040c9d6fe00f3e935deeecd411a27ce30a760aa1d92f2871d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b39bd0e6342db0a038f2e088634fdc001a0e44e6d0c32c8c99a93208e6376aec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f076d38495eecd4f94a9e6850859c507543af4e716a102b2e56cd79b11df0d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce05c77db589456798d31c1a20ae0ebd8e6db66571bf1bfa0fc12129c4717b8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d65a24a2a73650aaa671abff5c36dfa14a4ff0ab20922825116cff72be7031b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1904742a8113a54a8fd5ba50e99f0e417f528bc4122a508021f65dce48a8c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee815007b3a4cc6d1e77eec7661c79d3bb6b2b177c16073b0e4062ef4681a465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38f804bd7f620d20ca507398df3b394845631174f2395b662d79e29a2ed5b5be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc1e47a85581fc759ba9d102e07f90a27f1f9df29da46f1704b549f8df975584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc28e1bd60c78bb97ff502a5ada3e3ba28f410e0c50368746226b5a0df4a35ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21312e0256c897724dc8db5d842a20ddb9ce7363e7c1498a579da16f67a52195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c6abcea36666549f732f6a96236ad4230fa1dcbe7cff23fd9026bd6eecc1bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f528345759a582fe384b88cf870c8ffacadbbc07166731222573df2e2a3e7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2405fe2b97477168f0bbb463b089e9d0ab0facfcfa8ad9f8d140d2606a96064b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2890ace34af1b04965d2575e0e2da9e628b0427bec95182c44a46f7cb6b18e9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c633e7346801ccf210aa0ede03590206172dd41860574d14cd6f21720b470f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9300b33c263a8c33b698153b0f8e2eabe4ac0072e4838915ae50a7451fffa4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46e28e0b9f7da719fd5673f1dcbbad85a9112f98cf63d2e645eff25a401cc7e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ddd17b46f0be90bc0e2799ab349fec73c0c269f1316f56ca627ec2c8ccdf19e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4277d9151cf9e50921f7e1e89b9e93b8dba0ccbe0d2be63b706ec8625a5728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c899ffbc36b7ee62d3a0a87291eabc87fac17b943972b4e5c510fc88f7b353a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderSet")
    def put_header_set(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#headers NetworkSecurityAuthzPolicy#headers}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet(
            headers=headers
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderSet", [value]))

    @jsii.member(jsii_name="putHosts")
    def put_hosts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67750932c067fff48a537c07d3b044a03b768d949ddb50c974ea7733fe7389fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHosts", [value]))

    @jsii.member(jsii_name="putPaths")
    def put_paths(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac381bc17c17d0cd88207341fbcc24c6710e045cc4b9ffaf1992b8e7cdd34cf0)
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
    ) -> NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference, jsii.get(self, "headerSet"))

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList, jsii.get(self, "hosts"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList", jsii.get(self, "paths"))

    @builtins.property
    @jsii.member(jsii_name="headerSetInput")
    def header_set_input(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet], jsii.get(self, "headerSetInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths"]]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf72249835aa8973c53be78c21ff643a053c88d1d096b9bf945932659a3a006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698ae37c100932075e6ab474af8338de431730f8e47a6c2f4569a77333428036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7713aab54afb2a1f0c85daf0baed4bbf3f205ce2324bfd9da6223c13da41ab)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b792d277c764d892cf31e730c8bafd089b804128bcc07c611da8fe214a7cb38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5928104eb6378c6b5764adc23ee2d674bf62afb84036f8ad3bdf103ac1f88aaa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424e53303346e7e19fb18f07cc49a9933d8e40f217aaee37a2d1f1a5568e1964)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e5ac252d691a8eb5c443b7e3ef7991b8bf788c35585121d9d0cf177859784b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb35086f94fc4773434961ce782e35dca21014ef016c790667d2f4829b8b8b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f09038eb7f985855f77dbedb79852c5c73e0c9e9747a02526e24d1a99bde9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a336a32838ab3339b2d7453f54f2ab66af305bf4c4c06bf1f041665ad80563a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c611ef8aea05808049467fbe58f13f0dd2363300752c6fb3ca29b9985781559a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ad7ff2950787c12e45c0357f66c857133d2c94d41428c22c5e6c0853ad5fa7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b19c06736209dd623265e5855aa59357599dce97adea3c47d42f88f6d45fb3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4807a5977463e5cbb49241036ae23231b55aef90c74ca65c9ebbc928dcef0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45252e168df4c2fdf8b52c16332bb194bf5e3e1ea7e72f7000739cff6e97dcb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d0b70b0a2ad0207a0c25e0729bb69d1178dbd0ad66802a24b99c04ef2683e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperations",
    jsii_struct_bases=[],
    name_mapping={
        "header_set": "headerSet",
        "hosts": "hosts",
        "methods": "methods",
        "paths": "paths",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesToOperations:
    def __init__(
        self,
        *,
        header_set: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet", typing.Dict[builtins.str, typing.Any]]] = None,
        hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param header_set: header_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#header_set NetworkSecurityAuthzPolicy#header_set}
        :param hosts: hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#hosts NetworkSecurityAuthzPolicy#hosts}
        :param methods: A list of HTTP methods to match against. Each entry must be a valid HTTP method name (GET, PUT, POST, HEAD, PATCH, DELETE, OPTIONS). It only allows exact match and is always case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#methods NetworkSecurityAuthzPolicy#methods}
        :param paths: paths block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#paths NetworkSecurityAuthzPolicy#paths}
        '''
        if isinstance(header_set, dict):
            header_set = NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet(**header_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6821189130034d89205e386cb15965fdd932b7586955de39dc9506d97655cb)
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
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet"]:
        '''header_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#header_set NetworkSecurityAuthzPolicy#header_set}
        '''
        result = self._values.get("header_set")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet"], result)

    @builtins.property
    def hosts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts"]]]:
        '''hosts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#hosts NetworkSecurityAuthzPolicy#hosts}
        '''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts"]]], result)

    @builtins.property
    def methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of HTTP methods to match against.

        Each entry must be a valid HTTP method name (GET, PUT, POST, HEAD, PATCH, DELETE, OPTIONS). It only allows exact match and is always case sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#methods NetworkSecurityAuthzPolicy#methods}
        '''
        result = self._values.get("methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths"]]]:
        '''paths block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#paths NetworkSecurityAuthzPolicy#paths}
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToOperations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers"},
)
class NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#headers NetworkSecurityAuthzPolicy#headers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12ebbf6994306b11e92c9beefbf729208d3a72607fde890af13733cc036b179)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#headers NetworkSecurityAuthzPolicy#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Specifies the name of the header in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#name NetworkSecurityAuthzPolicy#name}
        :param value: value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#value NetworkSecurityAuthzPolicy#value}
        '''
        if isinstance(value, dict):
            value = NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7994d43a505cc2f384e673b066c5f4844ce568861ee10363fc91c906eb9fdb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#name NetworkSecurityAuthzPolicy#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue"]:
        '''value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#value NetworkSecurityAuthzPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fea86fb3dd66e21f4be178b004c12ad110bb89b17561f74f14ba21560f08a85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010e6898bc9bc4c95423a0dbb920d9139ff4949aa4d71d2e9b46c7fd7ab0aa55)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb7ea1863960987ab10314e6ce855b6687888b0019e49119408890a445192f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb506213042c816f762f1fff8380b638c33ec73f5559ebdb68442fc744af70ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__013d424beca4b1820df6ba21eba10d71c70da9df08ceedf0713222eedfc6a4da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b856f208f3ca208e26eec54880c2d19f03a27a3a330c8f9cfbf27fde6ae185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a63e7b9ff94afb2e7ff0a1dd64d36ab93767a7326f03ed0377b6280f90ce79c)
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue(
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
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue"]:
        return typing.cast(typing.Optional["NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45634889379cf0cbe4d6e51993b82072d3c9dec7e37be84538d0079c48278289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36778cdcfecc85413a9cdc42d9d66661967f9214bcef265ad8e4039de100760c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f897056c7bea96911aac350a27541cd73ad29b339a258b8891273aefbc071d74)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25bafad8ea3eea874a0f70f8fddcabf7fa3cd20009edb8daa2733b176711d628)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b2eef2f6d1d5b57488a9632ec01e37889cd5af58fbb3b74118aa725d7b745e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d3a02578c99560c16881044673ee132dedf39360680c807c54b06baea2a018)
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
            type_hints = typing.get_type_hints(_typecheckingstub__346b3a2d468bc53473d53f8a180b55f9a9861c6098565a89cf86b0f3a8b1c768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447794117a203d52fca2e289ad1b1ce840132def5021f6ffa6771ec2e57fd164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e5addc75c1f9242e99496cd9ade55e536cbb984314c37b1add2778928b9e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6754f8eba5743a19b3766c0d35e07e3a2d187382b8fdf65e8411746fc84b1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1681ea006a9fa8a91fbc07c3fb37908e861a97341e69d15e95d45a449557ce53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095e8c14fbcba7a72da4231c71d1aa3439d9979b77af8eef5fa0705d2a434739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(
        self,
    ) -> NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c83673eae2a1012a1776c1e92781f02e30332e1d4619659b23fedc825f2aed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c74885b77a253a507146dafff7336a15e658b896d0111035591adf4af8f098)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07ed520ad01065f275913a9663187be269856fd5bfb261193462f4bf2b5f92b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a07f4061a5a83731bb196cccb892450ea86b41d1edab90171c58fe4d3ea12bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35c108baad652192358efc54be360b0638f446f2704a9ac95287f9b3a906207)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a04f17f61c653bd2a2059f0dddb97ec3bc223eedef02bbaccbf02622c17ca12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2e2be08a97368fe7078331f571b1c978e1d8756fa5414d46cf70bc04a93b5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32414d23796a69fd1eb307f41955a08945e9111b7fd57292218ae33d086049f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a597bd6f893303498501849f59f8690aaca876f6f83fd9ee9ea6ab9782502c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f7dd1b73ad1466a64fa2b5eb6820fae90975127418291dd797ba5d90e45761e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be87f4c1280e9664faba7850ebff671275f79a5892122b87910b1cc96f44d48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7875c609143301dd21f85f79cae7d285247ef55926f5ec5e60e1f6882c706021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31235f2093cc9be7cdd24dc0af3917697bb77fa160995c393b6d5e64a77212d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41090e7249fc29013203536d7493f983dae035cad00edca5f464e36e48ed0c9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03d7d9ef4c1507458d50fbd48f08ed845d339fc6feeeddbf025201ec214d159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToOperationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8466e1c282a58d9918c4f95959bb588a47604dd246099c8dabb82011d348325)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87539e0443d888b27cc8cd5bdaf366b99159f42954b9e3cb1a0fa523e76b0534)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86317cc03fd8c44cd38d048ad55be80072f7353df8156b219ce09faec1f64c91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__314d8a10391c47132fb23c85fe6fd81468b7870c74ebafc54674923d74142a70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64e4e6c6d7f4504f2dd6f1fad38ad2879e98748d8f3fb4dec18ac09dacb311f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a3414eb882c262a69c3186aae5adfa1866a064d58c43ca6bb996d2e4af4fc04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f19940c18f84e9211bdea26af104850c55aea074706afe8464e33afc29dda11f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaderSet")
    def put_header_set(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#headers NetworkSecurityAuthzPolicy#headers}
        '''
        value = NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet(
            headers=headers
        )

        return typing.cast(None, jsii.invoke(self, "putHeaderSet", [value]))

    @jsii.member(jsii_name="putHosts")
    def put_hosts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721e1f7323673f41b5ad71b8205462936629252dc3373534a5d452730bc4988b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHosts", [value]))

    @jsii.member(jsii_name="putPaths")
    def put_paths(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8316d9066aa5d479963553e5cbd945fa39d63c318b6c4560259e3b700cc2368f)
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
    ) -> NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference, jsii.get(self, "headerSet"))

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList, jsii.get(self, "hosts"))

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> "NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList":
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList", jsii.get(self, "paths"))

    @builtins.property
    @jsii.member(jsii_name="headerSetInput")
    def header_set_input(
        self,
    ) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet], jsii.get(self, "headerSetInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="methodsInput")
    def methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "methodsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths"]]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="methods")
    def methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "methods"))

    @methods.setter
    def methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f87aa08876eb78e399923b21d885b9c229808c3fee58f7d2b18ba8100dba291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "methods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f71f927cc941bebf02161e830c886a7ddd179448542535cb6cb40d633d3611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths",
    jsii_struct_bases=[],
    name_mapping={
        "contains": "contains",
        "exact": "exact",
        "ignore_case": "ignoreCase",
        "prefix": "prefix",
        "suffix": "suffix",
    },
)
class NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths:
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
        :param contains: The input string must have the substring specified here. Note: empty contains match is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc.def Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        :param exact: The input string must match exactly the string specified here. Examples: * abc only matches the value abc. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        :param ignore_case: If true, indicates the exact/prefix/suffix/contains matching should be case insensitive. For example, the matcher data will match both input string Data and data if set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        :param prefix: The input string must have the prefix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value abc.xyz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        :param suffix: The input string must have the suffix specified here. Note: empty prefix is not allowed, please use regex instead. Examples: - abc matches the value xyz.abc Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1958bc9a641b3e06eafbefd2aa26e9a9f679ea1e3cb77630530f02168cc52a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#contains NetworkSecurityAuthzPolicy#contains}
        '''
        result = self._values.get("contains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exact(self) -> typing.Optional[builtins.str]:
        '''The input string must match exactly the string specified here. Examples: * abc only matches the value abc.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#exact NetworkSecurityAuthzPolicy#exact}
        '''
        result = self._values.get("exact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, indicates the exact/prefix/suffix/contains matching should be case insensitive.

        For example, the matcher data will match both input string Data and data if set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#ignore_case NetworkSecurityAuthzPolicy#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the prefix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value abc.xyz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#prefix NetworkSecurityAuthzPolicy#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''The input string must have the suffix specified here.

        Note: empty prefix is not allowed, please use regex instead.
        Examples:

        - abc matches the value xyz.abc

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#suffix NetworkSecurityAuthzPolicy#suffix}
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af7e38d54253ab3dccf46e6bf359b0f66c4e0fbd0a42b11dfe657caa511842b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcab51b6c9bef4cd0b1fcf751d34df4ae878a1fdc577483149c865cf2e62971)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e5602b45c0795bd2d72933a0aa5edf54b9a42e15dcb1e5e001a6ff1c6965b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__326d143a4d95559349035693715aa643edba08ce7e3358916970bf346a956585)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40e366f4b0f9a4e23982f0f67f01c1a7fb31f2205c3915fbb356768d49e5dae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e8fec0f7a6323315c9b9971a0713bf2be7b4fdf9ec955ce7f4d0fffc7ac4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08035f6b81fbe416596d1d69b01fe5628217aa2d328a1319a63b83b5873bf15f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4efde1fd28f5f45fdb1b1af710bcd5cd1b07107896a61aa6a7e2ab4944bc59cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exact")
    def exact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exact"))

    @exact.setter
    def exact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c34dd656c6ebc02fed1c73a2abda0e72714a835843af69b933b1762f9f9bfd7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0ea101871ba7843d3cd306a1008fb1f7cfd3dceb49a58e690ff01fbbe868d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f62a5f583fcb6b3edad305e091e7a91ba96306acc62d23d1a80361c291688cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffix")
    def suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffix"))

    @suffix.setter
    def suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6705b1c708a0d510631819960ac00d7e660d94cade300f8e6432a70ac9b0fe1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad1bb39906249cd411bb151e96dbab25489527258cda62baf3ec710fd6ff79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkSecurityAuthzPolicyHttpRulesToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyHttpRulesToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9cb2d79d0bd35a05c9753860184e270bd3972a74f4028422fd29a23666a7460)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNotOperations")
    def put_not_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a554aae22fe02bf3ee14c61a4abb7a61abede56cd20386bf3347714321c1bc0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNotOperations", [value]))

    @jsii.member(jsii_name="putOperations")
    def put_operations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c042091c8a81cdc1caaaf8f58d4720db245d62d9ed3234dc2905a60b48864607)
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
    def not_operations(self) -> NetworkSecurityAuthzPolicyHttpRulesToNotOperationsList:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesToNotOperationsList, jsii.get(self, "notOperations"))

    @builtins.property
    @jsii.member(jsii_name="operations")
    def operations(self) -> NetworkSecurityAuthzPolicyHttpRulesToOperationsList:
        return typing.cast(NetworkSecurityAuthzPolicyHttpRulesToOperationsList, jsii.get(self, "operations"))

    @builtins.property
    @jsii.member(jsii_name="notOperationsInput")
    def not_operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperations]]], jsii.get(self, "notOperationsInput"))

    @builtins.property
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperations]]], jsii.get(self, "operationsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkSecurityAuthzPolicyHttpRulesTo]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyHttpRulesTo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesTo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceed0edbd8e784d23f3d78b0cbbe72ed093cdb11bb19034686a024fda166940f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyTarget",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancing_scheme": "loadBalancingScheme",
        "resources": "resources",
    },
)
class NetworkSecurityAuthzPolicyTarget:
    def __init__(
        self,
        *,
        load_balancing_scheme: builtins.str,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param load_balancing_scheme: All gateways and forwarding rules referenced by this policy and extensions must share the same load balancing scheme. For more information, refer to `Backend services overview <https://cloud.google.com/load-balancing/docs/backend-service>`_. Possible values: ["INTERNAL_MANAGED", "EXTERNAL_MANAGED", "INTERNAL_SELF_MANAGED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#load_balancing_scheme NetworkSecurityAuthzPolicy#load_balancing_scheme}
        :param resources: A list of references to the Forwarding Rules on which this policy will be applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37da43a58c6a13dc766c0f76ad69a830655fcfa0969db3d17f505927ffc926d4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#load_balancing_scheme NetworkSecurityAuthzPolicy#load_balancing_scheme}
        '''
        result = self._values.get("load_balancing_scheme")
        assert result is not None, "Required property 'load_balancing_scheme' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of references to the Forwarding Rules on which this policy will be applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#resources NetworkSecurityAuthzPolicy#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7735fff7ab565fbadf8a1e65329c86ceba4cd63254d6fc4063b2f3554117eb39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0375157c1d067151f6c0408f4690c05d2a03176d6b403194a5db122f971103da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingScheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f8870a466d749443339eb2ac760cfdca39c8230bd2b6f7a7ac6f25711cb81a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkSecurityAuthzPolicyTarget]:
        return typing.cast(typing.Optional[NetworkSecurityAuthzPolicyTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkSecurityAuthzPolicyTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6910a4ce6a86b17f6e1391547f6ee58780cfb76192a7acca9ef706a3a2fabc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkSecurityAuthzPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#create NetworkSecurityAuthzPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#delete NetworkSecurityAuthzPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#update NetworkSecurityAuthzPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7600bbb9655f177ed60d3b4dafac2e5f301305be27b8793eb8298e8138e1d2c3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#create NetworkSecurityAuthzPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#delete NetworkSecurityAuthzPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_security_authz_policy#update NetworkSecurityAuthzPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkSecurityAuthzPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkSecurityAuthzPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkSecurityAuthzPolicy.NetworkSecurityAuthzPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eeb1bd563ca2b976e213be549ebd3bdd5104d715bec451adf7d89f5e2c62ab5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7498ba69122c1f3dd7fbe4d7308e33c065925b21265a0d8c432f19faf4e413ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01675652a63f3354415abda4b427577ac6c6b48e9fed16fc5ba5bd9902961ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c54d1cbc0b58c42392629b6ae25d73da998fd7420b52d9222acbed88f88da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12ff24086888809d18a4ff4f77e9ae1cfbe7caacb79863e6a19b9ff83b28229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkSecurityAuthzPolicy",
    "NetworkSecurityAuthzPolicyConfig",
    "NetworkSecurityAuthzPolicyCustomProvider",
    "NetworkSecurityAuthzPolicyCustomProviderAuthzExtension",
    "NetworkSecurityAuthzPolicyCustomProviderAuthzExtensionOutputReference",
    "NetworkSecurityAuthzPolicyCustomProviderCloudIap",
    "NetworkSecurityAuthzPolicyCustomProviderCloudIapOutputReference",
    "NetworkSecurityAuthzPolicyCustomProviderOutputReference",
    "NetworkSecurityAuthzPolicyHttpRules",
    "NetworkSecurityAuthzPolicyHttpRulesFrom",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSources",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesList",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsList",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipalsOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccountOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesList",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet",
    "NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSetOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromSources",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesList",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsList",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipalsOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccountOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesList",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet",
    "NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSetOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesList",
    "NetworkSecurityAuthzPolicyHttpRulesOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesTo",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperations",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersList",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValueOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsList",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHostsOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsList",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsList",
    "NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPathsOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToOperations",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersList",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValueOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsList",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsHostsOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsList",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsList",
    "NetworkSecurityAuthzPolicyHttpRulesToOperationsPathsOutputReference",
    "NetworkSecurityAuthzPolicyHttpRulesToOutputReference",
    "NetworkSecurityAuthzPolicyTarget",
    "NetworkSecurityAuthzPolicyTargetOutputReference",
    "NetworkSecurityAuthzPolicyTimeouts",
    "NetworkSecurityAuthzPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cd5b682aefe4d148fc59c51c68d15a27401334ef7498b49b1b4704527f3fd6ab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    location: builtins.str,
    name: builtins.str,
    target: typing.Union[NetworkSecurityAuthzPolicyTarget, typing.Dict[builtins.str, typing.Any]],
    custom_provider: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyCustomProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    http_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__524e719387501ff5db891f23a732441444950951b4061e9ee8ec88746d7937f2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0460c4bc9a2a12955b86ef412b039bb37e6523bd6b3e9725876ab9418da6e9ac(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882e4ec1c352ff1cf7c22ceb78335ec6bee83d180c52bb42b0e749bbc7aa5de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d96f0b9182a2e5a2e45f6cc7277314d955ea6db98870e74d399a3a0a5242374(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6349695530f6146c3aca61b0a2a5b47208e4b019d1ed1abb9aadafaf8adbe2de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449f17a18bd5ad21d72f173f9730879e6e72934294590aa8175f6572c8c3335e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9900cb0c82fa36d88f08171acd2de61140f822dd478f5c5a20ff663f26ab66c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf511e649a1ec4ecf8f77abea6999b9a70e36c22e352bb2aa231da6b01ccc43a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2f99e2342b2b516257b455e04422d6eca1b4b8b84ca22873c568312111bfcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f0d9144aad0177f70fb5f9ecd68b6863394c4542c0ce1cef0362be0ec7d963(
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
    target: typing.Union[NetworkSecurityAuthzPolicyTarget, typing.Dict[builtins.str, typing.Any]],
    custom_provider: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyCustomProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    http_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c04903da53856c5904a2b1bbe61a80c251e1bd0204eb31c80189a66326929f(
    *,
    authz_extension: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyCustomProviderAuthzExtension, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_iap: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyCustomProviderCloudIap, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7402158dc10a8e9258482876989913285ac33f7416bf18fd3c5be996f2c1a4e5(
    *,
    resources: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c44d2ebeb48091acd29cfbd18c9d0285cbcf216143b82f13fa88510cc9734f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b7251979a99da2a5c3f3bf6511d6237022c768052e473075978c2bf7396176(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f949a9cb1af4a85b98d12d957432ffe8410518daa6d3ca26dc13cca17e043e3c(
    value: typing.Optional[NetworkSecurityAuthzPolicyCustomProviderAuthzExtension],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a3456d47b995ef7cf0237c3f34789674d58893cd4cfe9dcc69f019aabdb225(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fec207955061629dd3e0b840a2f0dc65feea49445d22fff4bc787e83797fde(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11757c0ff2a7d38920d076fb9b8b516100bc74afddbc5d88d9e9e6ea13cfd7f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b3d4e0be96473137ce3691cbd573121d45ce192efb4ded831e1fe4947c529c(
    value: typing.Optional[NetworkSecurityAuthzPolicyCustomProviderCloudIap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876db6207232bfd6dc6b2627777ddef29dbf279de5731ea3a08763a9fef440d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0655fb2749cb529db667a1a80502e2c64db858f9468c20d55acc7c6d59b9f28a(
    value: typing.Optional[NetworkSecurityAuthzPolicyCustomProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4899d07a04516b9bae5b90d7dfc900801a1dc6ad8fdb664e61fe1c392f23b4(
    *,
    from_: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFrom, typing.Dict[builtins.str, typing.Any]]] = None,
    to: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesTo, typing.Dict[builtins.str, typing.Any]]] = None,
    when: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb93ed401a52343dfcd3e8632fcfe5c380b3b2c49b2c0122d81e8136e6aba3d5(
    *,
    not_sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8071a14b4870e8b03826de281dfc08236065de6b052387c574e64013f4218041(
    *,
    principals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266fefa873b8a6e28d505e41f25ced04ccaf4cc7c001f5fb099c2f18b5d1185f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebeb061bb0e76dbd471b8aceef401f3dfc31811ab25afeefe586b5e58331eba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aaab2e7c87b631f47206aea22e05c99956448e0697c06e560966bc48a14c4fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec64604a53d1e45c9552b2f88c8efefc3b46d3221e969e433d3811c43fe643b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce5c1e25a9ffb056b5ba9e8759c3fdd83a845ea9cf36d7e933aa734ce89ad0d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d41f9af96484fd9b542df51bc8952fcdab6bd5966d7b83d25e2a623adc522c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6d62201a308d5001ba32843cd52ff8f1529c6b7f9b83d5276bbbc5c716043f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbcafbf091f8bc16ee9702617434c7476cfc04f32c415615c734fa06c77d3a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a82576d8d31b7a5de76c7c2b21bcd9979930e758cca2fe455d61cfc05b692c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2028504086df7381fe244fd3252c09d08decdedfc6ce6d2e06721b08ae6149a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a3d0f0eaed2e161d23d8d6a9de0cc0ae7f33199f8ef2b8b5508e1cb3d5dffa(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b39b8f8922b5820d4a288588c6aac1685d89e782baae59bbbdd396ddf609575(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b2be2ad811068877412f52508455716af920ed441e14ebd25a7ee2749f9b65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5a91f1e2e262d1861d2aad0d7be873929d0cb48893d70cb5f157671d1f90b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caf1cf8d8f2a4349f444bb664e0cdafc724ac0fc5c3db091a726c07e934f9e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7418b4fde4e63f89e94b5719b9af0a64e9d2c59082aa5fe3922403405a44b488(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea0bb2abe91bb7ed1477c1ee6c99b16e659fbd5773862cab7911742580d08f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf32d2c94a853e65fa29b74c0d87b720caaefe2308d82bfffbe9e738d59a01b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3584dd77a8e0432099f8ced77674508edab64b3dc964c880454aa7baee29389e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29c9ec471cde6638abc46e275c3bee922736a89b3ce2b9c34c2a77866b736e8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227f15759e8db669aee820acd48ae47d7364d189893273fa9a2683db28f1b2d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20da40a0e2e06040d673ac4e7559da781d62f2927d3767010fea495e7c842d1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea199583baa79f191f649e6aa8e988a9c0b54e28f3053aff4c6c7652c4129118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9169d7d46a6b80cba8aab9cef7dacd627aa174cf0184fefb517570d75ee841(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesPrincipals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd2e2937095ffd9433279b4492fa76c9c89e23f96a993ea293294d05167aed9(
    *,
    iam_service_account: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_value_id_set: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7969b937adf36be994fb80545ae6fb4494071bfdf7c3e59ab69c88081b9ac5b4(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c35cce7777b8fe4e18e2a7b0d35def99173d6b0edcfe269eb952470bacd003d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8143ae674dfc2a9be36517e39a2b21772153f499487b15a9ec6ed79793d15f94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0459e7005f055dd74a11d6da447ae151574909cddacb4d7d577a5ec0e3cefab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d29f2010fd8f633e7f094fe735613e2b77400148410e1ad36ec5c4baa16841(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7111f7a904907db961547709cc377a1f52e4d6f4975d57a7fd1dcf20bb44d7f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7310fa0a64c9ad4d0cf8d2bb9d016ee3e1d5ebfcd41dbd66dac006736881790(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642d3e34c2583b8981fa38da84cb057424bbe9f70c354a80b4282390fd3b6988(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesIamServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3960d999e1cfa60dfe69bd8f36a54159d9f21a27fd8484d23674e3533bc8ad58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741e9619018a4a26394cc5870238dbc2232a0573b7e05d7ae2f38cab7b809cc5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00af9602228989f97b6c3329716bb7b17e38325528c2d25d9e419c6c3e65347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd9be09623268c89a9bf500abfcd193a4a9066d62794f01fb8d3c6c5fdedb10(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__181cfaf86de44140ab4b0dfb28d4be601d376394fdfc22bc336bd559dc25bec7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5092f50ea67851b6f829ccae378d7e1cee08d612ed012d8f951bdfee9971658(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a5c543fde938b3c32579399f5f00221302d1c50b845fada3c3e3859aed169d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bdca4f84c1f8766cf51483e34280dd4f92ef9bd0e8cdecb878e2f50bc47867d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eede2a0c13905a01d402780cc37a64780f57e212067db22e98962c716241046(
    *,
    ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6741eda7d00c1ab3aacf103cad2ed8140e36d327a59e69eccff643374bea7c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382eea6b9f67cc59d6ae2a95217ac71d31bea1bfd523193f0f17c5b4e8777a62(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14afc194324e4e6ad9d7ec0ba87e0764ae0b34ad0067070f8471238be8b3833b(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromNotSourcesResourcesTagValueIdSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60294e19dd6a44d72b5c1605ec7300a4d5c817e3e3ce495cca3721863101f0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8266ec049fe93a75914d30e56b5224e538b582d9d19355871b471e51831b30(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromNotSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ee4d15e3cca7ec97e9dbe8e2fa541e71c8cf3e1a9e55de8429984f9f6457cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b33db9ad2a9437a6cce9bdf071a1d9954cf77371ccd5664b4715a5544759792(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFrom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202ad195ef6ed01a7e191d41a985c65dda904d59c572ed4785827c5ee6a8e291(
    *,
    principals: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3d00cbae446d2a0525560bff5d637f0904b3d03f492cbcf530192adc134c41(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd848eee9dfebad6312a7ee924b493744d47d99be77413e263c2163381f5a50(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9630f19d640ffc33eb025c954ab218449dc71a0947961d447765c862e74092d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e185633221dab2feef015b337d85d5ff4ec07c6bd5f14e789b6a7b677ee8506(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabd6b44ca47edd50792034e9c5e2f304219d2271f5c31e3d4fa66bf0096fd18(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c085afb184dab90bcc382843f9a1310cc6e95bd1d4746eef95610daa26ba1cd8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec6241d55a1316301a86426a2f88f4bf7c6c23302b5dee742686a611b257c57b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1727963e9de87a0c01f93037b79cd8a1fd28f1e617f9f69dc36c56e343b3df7c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b409a64245e09dd4c66951684ba257cc14fc9bde51b800b33cb84430f729aa2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0de0ebaec27c0658836792dec5e6a8549dfbb5f5aec7a200552a51ebcc7a6f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a780786761e8ceaf7f21fcb9e7162eadca6970c7e4e9b379fed536796f1fdfa7(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726d170e106ca8c410f77627449bebc5136251274721d9fe96fc471d08210d9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95abec1acd1d41647391a94f9e68cd9fcc0a02e8c99fb6e99fa944577b898e68(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6000652c64fa8a95da2b7e37975623c82c39cd6da1fcf864c863b64a8f6e509(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb6d04fbb09c948a6649b8708497abc40aca246b5f65646769d9f9e59a19b22(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470ea010777af4c6e668f0f2bc6d9726fd1970d017d31b9dbf9930ca5f3b5c00(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb23bdc9006f55f0dcea7a28510fb4dcde7d54e377b335a8bd8a557cbbdef9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45613272cc99a0681d75020c052eebf3aa50feec21bf6cf44e478d80c0e33010(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7061e7cc2c165bbc7e88a6338002631bce303cad23988dcd60548788aaf093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24dc9f68eb103e7784e72ab666a1d7c76e936389ceaeebc85f364bcd03f64c1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a04e27a40922fb05617e35d4b790c323fbe3a24438420ac86183ca0f27f7de(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bfc78be589c22ff2d81bf90b22244d8b686318a716d017fff8bdc8421d8f04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6e97a96c2ba62f998370199504d412c420baa07b04eef3c6d7458623f43ad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a3056f91b6df5d4ed5be16f7770ce58fbb3049dd15e13c9bd66bc4acd42073(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSourcesPrincipals]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66881cc7537b81465fcc56a4d08d801beeb03c15f1afa04e8c70912b8d1c38a9(
    *,
    iam_service_account: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_value_id_set: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180a0d51fadca1f7abe2bb927ee2bbfe81c3d2a1abb55dd82867265bf93bfa17(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8e4514f779844b03f847bc32129a8a3e455f74cf003263b4153584d263f29e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ce92936f1914d1161d17984bc9b7f4810af8b8be5a104285ae838008d1e45b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac1a26d0848499c70958cf1bfdd649e50ce8064e83c43517c92004b755e77b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c83b72f95a78db2431cbe0b82e1cbe3b7063bde3b23374ebd5ca78b2bf92a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a91be37b107b8cf86ec0273f941f5e3511df6ca37de48b9887b05cf092bc543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc3879a8fd51f6a3ba2d3f9b0f5eb0092b2f0937675fd3b84f6a9af404addc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19f35e1af33ad174a48366a5beca436c5d8c6bb888f1a9d8e5445b5402fba5c(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesIamServiceAccount],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d83ff053430042a147bc423a0d88e278f0166815a7921efc9cab2e1231515f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65857d900e1964147e65a4c29c42b51434ba438d4fc3c007a966ad0c541e6cc2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4fcb17cdcedc904858075cf7ccbc4a6ec1b6593cb76bff4f17d4a9de8507cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa0b027951d329f491dbabb5939409635b423230a5d9bfcd75daa9fde5cd324(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8b4b4b0aa7013e39bb7215b40e6f6e6b17ad1c24cd47214e5b747704798067(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcef953ae9bb92fc1bc9a00e35fbd4e3d61c67f5fa5fec732f2f653f3e09c5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea1ea4c2f5d606e8b449e462b042770f97b9e39d3e8302d439c1de415edcbaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce94d9c5b0418bedf688b700aa6b90d0d7a9fb0a9a016de10b718e70997bd89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesFromSourcesResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e721368ea7ab364a176631e742b938d58d2288608c751f2833d5aaa58f692ca7(
    *,
    ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc9f4350be4bf9e7cab8e3e9c8acdb901924d309ed654544b4e559d3680251b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffb3327a9eaeab812b300a7eeaeeba05320663b119ebf568fc0106608cac049(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9740f6afb333486a2ec00ea8cddb8c9dc2eb731e9299caa68007bd4d94175fa2(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesFromSourcesResourcesTagValueIdSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ce2ee4e591ed54563a178179adb5a539925130da3da110b555768ee84a4ad1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8de59bdbb994d69e618af54c96120c301bf5b3b62eb41cadf166855c9943dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f464ece72f3a979a4f50a74d9ceec5d69544efbfcdbec91390abefb86d3a55b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06007bb57d7ed10fedcc818a348e3962a1f94b4920a81374a254ed04e0d4245(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a50983ce2e4cd836cb650eacd75c5be8b06d6bd3577c9de2a49738eb7f196b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a58546cb8ff88abaf08d10c727f912045677d28d955327e539f84f37c48f7bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97be5e72d79e641544fa8d0dc11a98c9a4cec3dbbcfeda91a5fc7c0f4a3a2f86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce528304448b69ff346f53ee635ffa94806802b747736ac2cffaf647df6b14c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a55279d7f39d70f03eeb7449af09de13875d07f5794f123d9c78b9dd2e5b2b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fabfdd6312e5ee01cc9c9b9895e4ae8dc280327d3f1a8700fcb5e481e468861(
    *,
    not_operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    operations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperations, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68bd6ad31e87746ebbda2ae205a5829ba3c84e6db7e83670d906e652fdc4913(
    *,
    header_set: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet, typing.Dict[builtins.str, typing.Any]]] = None,
    hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed882854635e84c42cf02d8dc9d009e0d7b26f1c85cb1bd0b703db551f29e8f(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9f7a93f8fe4855c1ae7ad75a772341aa6e786f40af276cbc7af9265985b841(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317c8602bcef2b1dac1c3335a287bd7e3b992719bff106d46593da9833e21142(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3f54826846bef204e36e6bb00c75f75561b67b378b2e90216250b2ebed8516(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c44048e32a2949bb963efe5c91b64e1e49c4076c28a5e07f8ae1f870fd83c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0b3fda1be32b9d88ffe14bb619f37915d2abe2942bb6d2e7fa169925e0bf15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8cb3dfd0f0a85a2883de72a433a0bdbd99d3c27e70a0628a86cb48b4bb7d4b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e858c867fd937ba2240032f124a2d2dcdd168060bfb5d2c558d1102dc391b9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe5f25e89f3eb3573d8adebf22fc5cac6f3af6d8022966fcf4fb7b90b0b2602(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db34ab3a5144bbd6fe52e7150c27d22020946d6692855b79c285cbab6e898ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e48682de5c59baba4dec7510eea60720c793dfda797f46fb27b03b3122d4f64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58b4d2ed02448a4eecf870fc4efcd9287e94b96d87536450c9bcd80671b18ed(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a3de8072a4d2f8d0b8573716a1b44b10513337b5cc4e928d340606b1435d38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618c313af05b9c862e2c813ead7aecec92b112df2ee8625deaf0dfa7beb92555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84370ceee9154e07c498c6987b5eecbd534e248d9beb9fe0348b3bb297066f5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad5cfa06c5acffb5e13f3aeb55169b61d8676ecd9025cfcd252e90a087324a0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c10b2daf155f3955e59d5e516ae57192bc27c918a20ba98a863e86d2ddff56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c68e427de757e54f26b05f5b8a838fea0d143692f018ab589a85a6f9f7ecb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e2f2ffdf3bc209ef0d2eee01b6e33ce6db8302ba0c59867d4537ab4333bb2d(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeadersValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6b212126715af27e5a828a343e31654779f47386481d1af4d7d784056cf7dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ec376dc0d1dcd9640fab0e69a614147e0ca2498853b2871c4d3e395e13e165(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2331005435a3f1b9e08dea509a92d0c2205c8e5097801df0310ea8eddbae4fd2(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHeaderSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d276d66bdc04152040c9d6fe00f3e935deeecd411a27ce30a760aa1d92f2871d(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39bd0e6342db0a038f2e088634fdc001a0e44e6d0c32c8c99a93208e6376aec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f076d38495eecd4f94a9e6850859c507543af4e716a102b2e56cd79b11df0d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce05c77db589456798d31c1a20ae0ebd8e6db66571bf1bfa0fc12129c4717b8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65a24a2a73650aaa671abff5c36dfa14a4ff0ab20922825116cff72be7031b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1904742a8113a54a8fd5ba50e99f0e417f528bc4122a508021f65dce48a8c90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee815007b3a4cc6d1e77eec7661c79d3bb6b2b177c16073b0e4062ef4681a465(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f804bd7f620d20ca507398df3b394845631174f2395b662d79e29a2ed5b5be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1e47a85581fc759ba9d102e07f90a27f1f9df29da46f1704b549f8df975584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc28e1bd60c78bb97ff502a5ada3e3ba28f410e0c50368746226b5a0df4a35ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21312e0256c897724dc8db5d842a20ddb9ce7363e7c1498a579da16f67a52195(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c6abcea36666549f732f6a96236ad4230fa1dcbe7cff23fd9026bd6eecc1bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f528345759a582fe384b88cf870c8ffacadbbc07166731222573df2e2a3e7f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2405fe2b97477168f0bbb463b089e9d0ab0facfcfa8ad9f8d140d2606a96064b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2890ace34af1b04965d2575e0e2da9e628b0427bec95182c44a46f7cb6b18e9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c633e7346801ccf210aa0ede03590206172dd41860574d14cd6f21720b470f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9300b33c263a8c33b698153b0f8e2eabe4ac0072e4838915ae50a7451fffa4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e28e0b9f7da719fd5673f1dcbbad85a9112f98cf63d2e645eff25a401cc7e4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddd17b46f0be90bc0e2799ab349fec73c0c269f1316f56ca627ec2c8ccdf19e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4277d9151cf9e50921f7e1e89b9e93b8dba0ccbe0d2be63b706ec8625a5728(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c899ffbc36b7ee62d3a0a87291eabc87fac17b943972b4e5c510fc88f7b353a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67750932c067fff48a537c07d3b044a03b768d949ddb50c974ea7733fe7389fe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsHosts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac381bc17c17d0cd88207341fbcc24c6710e045cc4b9ffaf1992b8e7cdd34cf0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf72249835aa8973c53be78c21ff643a053c88d1d096b9bf945932659a3a006(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698ae37c100932075e6ab474af8338de431730f8e47a6c2f4569a77333428036(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7713aab54afb2a1f0c85daf0baed4bbf3f205ce2324bfd9da6223c13da41ab(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b792d277c764d892cf31e730c8bafd089b804128bcc07c611da8fe214a7cb38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5928104eb6378c6b5764adc23ee2d674bf62afb84036f8ad3bdf103ac1f88aaa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424e53303346e7e19fb18f07cc49a9933d8e40f217aaee37a2d1f1a5568e1964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5ac252d691a8eb5c443b7e3ef7991b8bf788c35585121d9d0cf177859784b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb35086f94fc4773434961ce782e35dca21014ef016c790667d2f4829b8b8b1d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f09038eb7f985855f77dbedb79852c5c73e0c9e9747a02526e24d1a99bde9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a336a32838ab3339b2d7453f54f2ab66af305bf4c4c06bf1f041665ad80563a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c611ef8aea05808049467fbe58f13f0dd2363300752c6fb3ca29b9985781559a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ad7ff2950787c12e45c0357f66c857133d2c94d41428c22c5e6c0853ad5fa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19c06736209dd623265e5855aa59357599dce97adea3c47d42f88f6d45fb3f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4807a5977463e5cbb49241036ae23231b55aef90c74ca65c9ebbc928dcef0f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45252e168df4c2fdf8b52c16332bb194bf5e3e1ea7e72f7000739cff6e97dcb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d0b70b0a2ad0207a0c25e0729bb69d1178dbd0ad66802a24b99c04ef2683e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToNotOperationsPaths]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6821189130034d89205e386cb15965fdd932b7586955de39dc9506d97655cb(
    *,
    header_set: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet, typing.Dict[builtins.str, typing.Any]]] = None,
    hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    paths: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12ebbf6994306b11e92c9beefbf729208d3a72607fde890af13733cc036b179(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7994d43a505cc2f384e673b066c5f4844ce568861ee10363fc91c906eb9fdb(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fea86fb3dd66e21f4be178b004c12ad110bb89b17561f74f14ba21560f08a85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010e6898bc9bc4c95423a0dbb920d9139ff4949aa4d71d2e9b46c7fd7ab0aa55(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb7ea1863960987ab10314e6ce855b6687888b0019e49119408890a445192f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb506213042c816f762f1fff8380b638c33ec73f5559ebdb68442fc744af70ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013d424beca4b1820df6ba21eba10d71c70da9df08ceedf0713222eedfc6a4da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b856f208f3ca208e26eec54880c2d19f03a27a3a330c8f9cfbf27fde6ae185(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a63e7b9ff94afb2e7ff0a1dd64d36ab93767a7326f03ed0377b6280f90ce79c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45634889379cf0cbe4d6e51993b82072d3c9dec7e37be84538d0079c48278289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36778cdcfecc85413a9cdc42d9d66661967f9214bcef265ad8e4039de100760c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f897056c7bea96911aac350a27541cd73ad29b339a258b8891273aefbc071d74(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25bafad8ea3eea874a0f70f8fddcabf7fa3cd20009edb8daa2733b176711d628(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b2eef2f6d1d5b57488a9632ec01e37889cd5af58fbb3b74118aa725d7b745e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d3a02578c99560c16881044673ee132dedf39360680c807c54b06baea2a018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346b3a2d468bc53473d53f8a180b55f9a9861c6098565a89cf86b0f3a8b1c768(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447794117a203d52fca2e289ad1b1ce840132def5021f6ffa6771ec2e57fd164(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e5addc75c1f9242e99496cd9ade55e536cbb984314c37b1add2778928b9e2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6754f8eba5743a19b3766c0d35e07e3a2d187382b8fdf65e8411746fc84b1dc(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeadersValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1681ea006a9fa8a91fbc07c3fb37908e861a97341e69d15e95d45a449557ce53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095e8c14fbcba7a72da4231c71d1aa3439d9979b77af8eef5fa0705d2a434739(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSetHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c83673eae2a1012a1776c1e92781f02e30332e1d4619659b23fedc825f2aed0(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesToOperationsHeaderSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c74885b77a253a507146dafff7336a15e658b896d0111035591adf4af8f098(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ed520ad01065f275913a9663187be269856fd5bfb261193462f4bf2b5f92b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a07f4061a5a83731bb196cccb892450ea86b41d1edab90171c58fe4d3ea12bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35c108baad652192358efc54be360b0638f446f2704a9ac95287f9b3a906207(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a04f17f61c653bd2a2059f0dddb97ec3bc223eedef02bbaccbf02622c17ca12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e2be08a97368fe7078331f571b1c978e1d8756fa5414d46cf70bc04a93b5a9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32414d23796a69fd1eb307f41955a08945e9111b7fd57292218ae33d086049f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a597bd6f893303498501849f59f8690aaca876f6f83fd9ee9ea6ab9782502c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7dd1b73ad1466a64fa2b5eb6820fae90975127418291dd797ba5d90e45761e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be87f4c1280e9664faba7850ebff671275f79a5892122b87910b1cc96f44d48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7875c609143301dd21f85f79cae7d285247ef55926f5ec5e60e1f6882c706021(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31235f2093cc9be7cdd24dc0af3917697bb77fa160995c393b6d5e64a77212d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41090e7249fc29013203536d7493f983dae035cad00edca5f464e36e48ed0c9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03d7d9ef4c1507458d50fbd48f08ed845d339fc6feeeddbf025201ec214d159(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8466e1c282a58d9918c4f95959bb588a47604dd246099c8dabb82011d348325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87539e0443d888b27cc8cd5bdaf366b99159f42954b9e3cb1a0fa523e76b0534(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86317cc03fd8c44cd38d048ad55be80072f7353df8156b219ce09faec1f64c91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314d8a10391c47132fb23c85fe6fd81468b7870c74ebafc54674923d74142a70(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e4e6c6d7f4504f2dd6f1fad38ad2879e98748d8f3fb4dec18ac09dacb311f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a3414eb882c262a69c3186aae5adfa1866a064d58c43ca6bb996d2e4af4fc04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19940c18f84e9211bdea26af104850c55aea074706afe8464e33afc29dda11f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721e1f7323673f41b5ad71b8205462936629252dc3373534a5d452730bc4988b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsHosts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8316d9066aa5d479963553e5cbd945fa39d63c318b6c4560259e3b700cc2368f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f87aa08876eb78e399923b21d885b9c229808c3fee58f7d2b18ba8100dba291(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f71f927cc941bebf02161e830c886a7ddd179448542535cb6cb40d633d3611(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1958bc9a641b3e06eafbefd2aa26e9a9f679ea1e3cb77630530f02168cc52a(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7e38d54253ab3dccf46e6bf359b0f66c4e0fbd0a42b11dfe657caa511842b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcab51b6c9bef4cd0b1fcf751d34df4ae878a1fdc577483149c865cf2e62971(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e5602b45c0795bd2d72933a0aa5edf54b9a42e15dcb1e5e001a6ff1c6965b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326d143a4d95559349035693715aa643edba08ce7e3358916970bf346a956585(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e366f4b0f9a4e23982f0f67f01c1a7fb31f2205c3915fbb356768d49e5dae8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e8fec0f7a6323315c9b9971a0713bf2be7b4fdf9ec955ce7f4d0fffc7ac4be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08035f6b81fbe416596d1d69b01fe5628217aa2d328a1319a63b83b5873bf15f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4efde1fd28f5f45fdb1b1af710bcd5cd1b07107896a61aa6a7e2ab4944bc59cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c34dd656c6ebc02fed1c73a2abda0e72714a835843af69b933b1762f9f9bfd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ea101871ba7843d3cd306a1008fb1f7cfd3dceb49a58e690ff01fbbe868d84(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f62a5f583fcb6b3edad305e091e7a91ba96306acc62d23d1a80361c291688cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6705b1c708a0d510631819960ac00d7e660d94cade300f8e6432a70ac9b0fe1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad1bb39906249cd411bb151e96dbab25489527258cda62baf3ec710fd6ff79a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyHttpRulesToOperationsPaths]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cb2d79d0bd35a05c9753860184e270bd3972a74f4028422fd29a23666a7460(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a554aae22fe02bf3ee14c61a4abb7a61abede56cd20386bf3347714321c1bc0e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToNotOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c042091c8a81cdc1caaaf8f58d4720db245d62d9ed3234dc2905a60b48864607(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkSecurityAuthzPolicyHttpRulesToOperations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceed0edbd8e784d23f3d78b0cbbe72ed093cdb11bb19034686a024fda166940f(
    value: typing.Optional[NetworkSecurityAuthzPolicyHttpRulesTo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37da43a58c6a13dc766c0f76ad69a830655fcfa0969db3d17f505927ffc926d4(
    *,
    load_balancing_scheme: builtins.str,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7735fff7ab565fbadf8a1e65329c86ceba4cd63254d6fc4063b2f3554117eb39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0375157c1d067151f6c0408f4690c05d2a03176d6b403194a5db122f971103da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f8870a466d749443339eb2ac760cfdca39c8230bd2b6f7a7ac6f25711cb81a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6910a4ce6a86b17f6e1391547f6ee58780cfb76192a7acca9ef706a3a2fabc2(
    value: typing.Optional[NetworkSecurityAuthzPolicyTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7600bbb9655f177ed60d3b4dafac2e5f301305be27b8793eb8298e8138e1d2c3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eeb1bd563ca2b976e213be549ebd3bdd5104d715bec451adf7d89f5e2c62ab5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7498ba69122c1f3dd7fbe4d7308e33c065925b21265a0d8c432f19faf4e413ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01675652a63f3354415abda4b427577ac6c6b48e9fed16fc5ba5bd9902961ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c54d1cbc0b58c42392629b6ae25d73da998fd7420b52d9222acbed88f88da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12ff24086888809d18a4ff4f77e9ae1cfbe7caacb79863e6a19b9ff83b28229(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkSecurityAuthzPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
