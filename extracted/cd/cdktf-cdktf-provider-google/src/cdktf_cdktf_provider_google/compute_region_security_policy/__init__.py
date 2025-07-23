r'''
# `google_compute_region_security_policy`

Refer to the Terraform Registry for docs: [`google_compute_region_security_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy).
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


class ComputeRegionSecurityPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy google_compute_region_security_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        ddos_protection_config: typing.Optional[typing.Union["ComputeRegionSecurityPolicyDdosProtectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionSecurityPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy google_compute_region_security_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#name ComputeRegionSecurityPolicy#name}
        :param ddos_protection_config: ddos_protection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ddos_protection_config ComputeRegionSecurityPolicy#ddos_protection_config}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#description ComputeRegionSecurityPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#id ComputeRegionSecurityPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#project ComputeRegionSecurityPolicy#project}.
        :param region: The Region in which the created Region Security Policy should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#region ComputeRegionSecurityPolicy#region}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#rules ComputeRegionSecurityPolicy#rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#timeouts ComputeRegionSecurityPolicy#timeouts}
        :param type: The type indicates the intended use of the security policy. - CLOUD_ARMOR: Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers. - CLOUD_ARMOR_EDGE: Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache. - CLOUD_ARMOR_NETWORK: Cloud Armor network policies can be configured to filter packets targeting network load balancing resources such as backend services, target pools, target instances, and instances with external IPs. They filter requests before the request is served from the application. This field can be set only at resource creation time. Possible values: ["CLOUD_ARMOR", "CLOUD_ARMOR_EDGE", "CLOUD_ARMOR_NETWORK"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#type ComputeRegionSecurityPolicy#type}
        :param user_defined_fields: user_defined_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#user_defined_fields ComputeRegionSecurityPolicy#user_defined_fields}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7f81edc6e4b37b62fba52cf6cfbe3eacd60bd2fd3e63b4410a0d6d72f6de63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRegionSecurityPolicyConfig(
            name=name,
            ddos_protection_config=ddos_protection_config,
            description=description,
            id=id,
            project=project,
            region=region,
            rules=rules,
            timeouts=timeouts,
            type=type,
            user_defined_fields=user_defined_fields,
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
        '''Generates CDKTF code for importing a ComputeRegionSecurityPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRegionSecurityPolicy to import.
        :param import_from_id: The id of the existing ComputeRegionSecurityPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRegionSecurityPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0718af724d77f1a7a31d3f1355989c79a682ef3f67cbbf0f1e85cc1f03a271a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDdosProtectionConfig")
    def put_ddos_protection_config(self, *, ddos_protection: builtins.str) -> None:
        '''
        :param ddos_protection: Google Cloud Armor offers the following options to help protect systems against DDoS attacks: - STANDARD: basic always-on protection for network load balancers, protocol forwarding, or VMs with public IP addresses. - ADVANCED: additional protections for Managed Protection Plus subscribers who use network load balancers, protocol forwarding, or VMs with public IP addresses. - ADVANCED_PREVIEW: flag to enable the security policy in preview mode. Possible values: ["ADVANCED", "ADVANCED_PREVIEW", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ddos_protection ComputeRegionSecurityPolicy#ddos_protection}
        '''
        value = ComputeRegionSecurityPolicyDdosProtectionConfig(
            ddos_protection=ddos_protection
        )

        return typing.cast(None, jsii.invoke(self, "putDdosProtectionConfig", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a249e65fd5e75e23187dfc65e7dd6a4fb69b9cfed16e9a7c8dcaeeb69f14a7c0)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#create ComputeRegionSecurityPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#delete ComputeRegionSecurityPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#update ComputeRegionSecurityPolicy#update}.
        '''
        value = ComputeRegionSecurityPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUserDefinedFields")
    def put_user_defined_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b8bd3a9e394cf41045a813dec5441db1190e84825156edeed511bd00f08613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUserDefinedFields", [value]))

    @jsii.member(jsii_name="resetDdosProtectionConfig")
    def reset_ddos_protection_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDdosProtectionConfig", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUserDefinedFields")
    def reset_user_defined_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefinedFields", []))

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
    @jsii.member(jsii_name="ddosProtectionConfig")
    def ddos_protection_config(
        self,
    ) -> "ComputeRegionSecurityPolicyDdosProtectionConfigOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyDdosProtectionConfigOutputReference", jsii.get(self, "ddosProtectionConfig"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "ComputeRegionSecurityPolicyRulesList":
        return typing.cast("ComputeRegionSecurityPolicyRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="selfLinkWithPolicyId")
    def self_link_with_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLinkWithPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRegionSecurityPolicyTimeoutsOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFields")
    def user_defined_fields(self) -> "ComputeRegionSecurityPolicyUserDefinedFieldsList":
        return typing.cast("ComputeRegionSecurityPolicyUserDefinedFieldsList", jsii.get(self, "userDefinedFields"))

    @builtins.property
    @jsii.member(jsii_name="ddosProtectionConfigInput")
    def ddos_protection_config_input(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyDdosProtectionConfig"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyDdosProtectionConfig"], jsii.get(self, "ddosProtectionConfigInput"))

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
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionSecurityPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRegionSecurityPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFieldsInput")
    def user_defined_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyUserDefinedFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyUserDefinedFields"]]], jsii.get(self, "userDefinedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d609edbe46167304d21117df0e8687587f2cad9e1714c280b98aebab6120f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4316574cf65f690e9c4b9ad72cabc01c0aad7eca81d4b1abdde54ba486aa4677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fb4689415e6b5bd303298bffa3002f28dca4a65feec08a6f3ebf1603244711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ed9d4b1bf67ed903956c8ef8db3b6c6d9b208fd12c924e7a41cb59db23226f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223f097badcfb2259616c5d0cff78971c076e673f8f4c152ab99bc603520fe6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f041ddb2fe9360f37de0614f77afb6c1197d3c1c842e54248aaf77f0c73e0aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyConfig",
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
        "ddos_protection_config": "ddosProtectionConfig",
        "description": "description",
        "id": "id",
        "project": "project",
        "region": "region",
        "rules": "rules",
        "timeouts": "timeouts",
        "type": "type",
        "user_defined_fields": "userDefinedFields",
    },
)
class ComputeRegionSecurityPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ddos_protection_config: typing.Optional[typing.Union["ComputeRegionSecurityPolicyDdosProtectionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["ComputeRegionSecurityPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#name ComputeRegionSecurityPolicy#name}
        :param ddos_protection_config: ddos_protection_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ddos_protection_config ComputeRegionSecurityPolicy#ddos_protection_config}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#description ComputeRegionSecurityPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#id ComputeRegionSecurityPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#project ComputeRegionSecurityPolicy#project}.
        :param region: The Region in which the created Region Security Policy should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#region ComputeRegionSecurityPolicy#region}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#rules ComputeRegionSecurityPolicy#rules}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#timeouts ComputeRegionSecurityPolicy#timeouts}
        :param type: The type indicates the intended use of the security policy. - CLOUD_ARMOR: Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers. - CLOUD_ARMOR_EDGE: Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache. - CLOUD_ARMOR_NETWORK: Cloud Armor network policies can be configured to filter packets targeting network load balancing resources such as backend services, target pools, target instances, and instances with external IPs. They filter requests before the request is served from the application. This field can be set only at resource creation time. Possible values: ["CLOUD_ARMOR", "CLOUD_ARMOR_EDGE", "CLOUD_ARMOR_NETWORK"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#type ComputeRegionSecurityPolicy#type}
        :param user_defined_fields: user_defined_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#user_defined_fields ComputeRegionSecurityPolicy#user_defined_fields}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(ddos_protection_config, dict):
            ddos_protection_config = ComputeRegionSecurityPolicyDdosProtectionConfig(**ddos_protection_config)
        if isinstance(timeouts, dict):
            timeouts = ComputeRegionSecurityPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4d20bb990c37dcd315406420eaf0e28bf8909f686e9e809da1a188c6bb2729)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ddos_protection_config", value=ddos_protection_config, expected_type=type_hints["ddos_protection_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user_defined_fields", value=user_defined_fields, expected_type=type_hints["user_defined_fields"])
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
        if ddos_protection_config is not None:
            self._values["ddos_protection_config"] = ddos_protection_config
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if rules is not None:
            self._values["rules"] = rules
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type
        if user_defined_fields is not None:
            self._values["user_defined_fields"] = user_defined_fields

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
        '''Name of the resource.

        Provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035.
        Specifically, the name must be 1-63 characters long and match the regular expression `a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_? which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#name ComputeRegionSecurityPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ddos_protection_config(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyDdosProtectionConfig"]:
        '''ddos_protection_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ddos_protection_config ComputeRegionSecurityPolicy#ddos_protection_config}
        '''
        result = self._values.get("ddos_protection_config")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyDdosProtectionConfig"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#description ComputeRegionSecurityPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#id ComputeRegionSecurityPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#project ComputeRegionSecurityPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The Region in which the created Region Security Policy should reside.

        If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#region ComputeRegionSecurityPolicy#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#rules ComputeRegionSecurityPolicy#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRules"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRegionSecurityPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#timeouts ComputeRegionSecurityPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type indicates the intended use of the security policy.

        - CLOUD_ARMOR: Cloud Armor backend security policies can be configured to filter incoming HTTP requests targeting backend services. They filter requests before they hit the origin servers.
        - CLOUD_ARMOR_EDGE: Cloud Armor edge security policies can be configured to filter incoming HTTP requests targeting backend services (including Cloud CDN-enabled) as well as backend buckets (Cloud Storage). They filter requests before the request is served from Google's cache.
        - CLOUD_ARMOR_NETWORK: Cloud Armor network policies can be configured to filter packets targeting network load balancing resources such as backend services, target pools, target instances, and instances with external IPs. They filter requests before the request is served from the application.
          This field can be set only at resource creation time. Possible values: ["CLOUD_ARMOR", "CLOUD_ARMOR_EDGE", "CLOUD_ARMOR_NETWORK"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#type ComputeRegionSecurityPolicy#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_defined_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyUserDefinedFields"]]]:
        '''user_defined_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#user_defined_fields ComputeRegionSecurityPolicy#user_defined_fields}
        '''
        result = self._values.get("user_defined_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyUserDefinedFields"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyDdosProtectionConfig",
    jsii_struct_bases=[],
    name_mapping={"ddos_protection": "ddosProtection"},
)
class ComputeRegionSecurityPolicyDdosProtectionConfig:
    def __init__(self, *, ddos_protection: builtins.str) -> None:
        '''
        :param ddos_protection: Google Cloud Armor offers the following options to help protect systems against DDoS attacks: - STANDARD: basic always-on protection for network load balancers, protocol forwarding, or VMs with public IP addresses. - ADVANCED: additional protections for Managed Protection Plus subscribers who use network load balancers, protocol forwarding, or VMs with public IP addresses. - ADVANCED_PREVIEW: flag to enable the security policy in preview mode. Possible values: ["ADVANCED", "ADVANCED_PREVIEW", "STANDARD"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ddos_protection ComputeRegionSecurityPolicy#ddos_protection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f653bca987192e8be63b9bc18aa1a6c187fc08fa4e89ba23e05ce228c9ecd8c)
            check_type(argname="argument ddos_protection", value=ddos_protection, expected_type=type_hints["ddos_protection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ddos_protection": ddos_protection,
        }

    @builtins.property
    def ddos_protection(self) -> builtins.str:
        '''Google Cloud Armor offers the following options to help protect systems against DDoS attacks: - STANDARD: basic always-on protection for network load balancers, protocol forwarding, or VMs with public IP addresses.

        - ADVANCED: additional protections for Managed Protection Plus subscribers who use network load balancers, protocol forwarding, or VMs with public IP addresses.
        - ADVANCED_PREVIEW: flag to enable the security policy in preview mode. Possible values: ["ADVANCED", "ADVANCED_PREVIEW", "STANDARD"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ddos_protection ComputeRegionSecurityPolicy#ddos_protection}
        '''
        result = self._values.get("ddos_protection")
        assert result is not None, "Required property 'ddos_protection' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyDdosProtectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyDdosProtectionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyDdosProtectionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87a2efa3c13b3c9ae848685975dbf54052b6b68e33f2062c6e4c2e9c93e4527f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ddosProtectionInput")
    def ddos_protection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ddosProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="ddosProtection")
    def ddos_protection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ddosProtection"))

    @ddos_protection.setter
    def ddos_protection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7cd01a816bbf8d98f5c14b28223a625953a561bb8ad344dbe35870dedf1ce4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ddosProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyDdosProtectionConfig]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyDdosProtectionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyDdosProtectionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab6992c517bd7c4fa52b722581f7da6a6a950c844f673a8e747b479a1eedee0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRules",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "priority": "priority",
        "description": "description",
        "match": "match",
        "network_match": "networkMatch",
        "preconfigured_waf_config": "preconfiguredWafConfig",
        "preview": "preview",
        "rate_limit_options": "rateLimitOptions",
    },
)
class ComputeRegionSecurityPolicyRules:
    def __init__(
        self,
        *,
        action: builtins.str,
        priority: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        match: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        network_match: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesNetworkMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        preconfigured_waf_config: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rate_limit_options: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesRateLimitOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: The Action to perform when the rule is matched. The following are the valid actions:. - allow: allow access to target. - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502. - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set. - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR. - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#action ComputeRegionSecurityPolicy#action}
        :param priority: An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#priority ComputeRegionSecurityPolicy#priority}
        :param description: An optional description of this resource. Provide this property when you create the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#description ComputeRegionSecurityPolicy#description}
        :param match: match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#match ComputeRegionSecurityPolicy#match}
        :param network_match: network_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#network_match ComputeRegionSecurityPolicy#network_match}
        :param preconfigured_waf_config: preconfigured_waf_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#preconfigured_waf_config ComputeRegionSecurityPolicy#preconfigured_waf_config}
        :param preview: If set to true, the specified action is not enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#preview ComputeRegionSecurityPolicy#preview}
        :param rate_limit_options: rate_limit_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#rate_limit_options ComputeRegionSecurityPolicy#rate_limit_options}
        '''
        if isinstance(match, dict):
            match = ComputeRegionSecurityPolicyRulesMatch(**match)
        if isinstance(network_match, dict):
            network_match = ComputeRegionSecurityPolicyRulesNetworkMatch(**network_match)
        if isinstance(preconfigured_waf_config, dict):
            preconfigured_waf_config = ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig(**preconfigured_waf_config)
        if isinstance(rate_limit_options, dict):
            rate_limit_options = ComputeRegionSecurityPolicyRulesRateLimitOptions(**rate_limit_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cefa813c968e44384908a8333bcb74172b63db28344fd73523435df7d2d0214)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument network_match", value=network_match, expected_type=type_hints["network_match"])
            check_type(argname="argument preconfigured_waf_config", value=preconfigured_waf_config, expected_type=type_hints["preconfigured_waf_config"])
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
            check_type(argname="argument rate_limit_options", value=rate_limit_options, expected_type=type_hints["rate_limit_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "priority": priority,
        }
        if description is not None:
            self._values["description"] = description
        if match is not None:
            self._values["match"] = match
        if network_match is not None:
            self._values["network_match"] = network_match
        if preconfigured_waf_config is not None:
            self._values["preconfigured_waf_config"] = preconfigured_waf_config
        if preview is not None:
            self._values["preview"] = preview
        if rate_limit_options is not None:
            self._values["rate_limit_options"] = rate_limit_options

    @builtins.property
    def action(self) -> builtins.str:
        '''The Action to perform when the rule is matched. The following are the valid actions:.

        - allow: allow access to target.
        - deny(STATUS): deny access to target, returns the HTTP response code specified. Valid values for STATUS are 403, 404, and 502.
        - rate_based_ban: limit client traffic to the configured threshold and ban the client if the traffic exceeds the threshold. Configure parameters for this action in RateLimitOptions. Requires rateLimitOptions to be set.
        - redirect: redirect to a different target. This can either be an internal reCAPTCHA redirect, or an external URL-based redirect via a 302 response. Parameters for this action can be configured via redirectOptions. This action is only supported in Global Security Policies of type CLOUD_ARMOR.
        - throttle: limit client traffic to the configured threshold. Configure parameters for this action in rateLimitOptions. Requires rateLimitOptions to be set for this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#action ComputeRegionSecurityPolicy#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''An integer indicating the priority of a rule in the list.

        The priority must be a positive value between 0 and 2147483647.
        Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest priority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#priority ComputeRegionSecurityPolicy#priority}
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource. Provide this property when you create the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#description ComputeRegionSecurityPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match(self) -> typing.Optional["ComputeRegionSecurityPolicyRulesMatch"]:
        '''match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#match ComputeRegionSecurityPolicy#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesMatch"], result)

    @builtins.property
    def network_match(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulesNetworkMatch"]:
        '''network_match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#network_match ComputeRegionSecurityPolicy#network_match}
        '''
        result = self._values.get("network_match")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesNetworkMatch"], result)

    @builtins.property
    def preconfigured_waf_config(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig"]:
        '''preconfigured_waf_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#preconfigured_waf_config ComputeRegionSecurityPolicy#preconfigured_waf_config}
        '''
        result = self._values.get("preconfigured_waf_config")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig"], result)

    @builtins.property
    def preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the specified action is not enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#preview ComputeRegionSecurityPolicy#preview}
        '''
        result = self._values.get("preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rate_limit_options(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptions"]:
        '''rate_limit_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#rate_limit_options ComputeRegionSecurityPolicy#rate_limit_options}
        '''
        result = self._values.get("rate_limit_options")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a873a88162d10458fe4fef4dff48c024e9518d57a2f5687de5f2cec36f886e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3eb34087422edda0ca0e9cdece8074ba7d00eb0db88eb691d94f03db8f9c26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f93308b70db4b327f95d35639313bc7bb4d04e9635b9361fa462032aa3e7d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9432aac519228371db2286ad97720a583a986f3e73989d1833bceca8347864f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16f1a6c9e725cdda479484c57e6aa62ebdb9c8acb438f5bfb13933086949ce10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5374edefbf8f7936fbf41b881c7524bcf55260673e868d9ff88f75c3f97bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesMatch",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "expr": "expr",
        "versioned_expr": "versionedExpr",
    },
)
class ComputeRegionSecurityPolicyRulesMatch:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesMatchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesMatchExpr", typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#config ComputeRegionSecurityPolicy#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#expr ComputeRegionSecurityPolicy#expr}
        :param versioned_expr: Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#versioned_expr ComputeRegionSecurityPolicy#versioned_expr}
        '''
        if isinstance(config, dict):
            config = ComputeRegionSecurityPolicyRulesMatchConfig(**config)
        if isinstance(expr, dict):
            expr = ComputeRegionSecurityPolicyRulesMatchExpr(**expr)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5eb8d17f901130f23ad88c4ad55439b8bdd1995a19d590686955226f87d3f7b)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument expr", value=expr, expected_type=type_hints["expr"])
            check_type(argname="argument versioned_expr", value=versioned_expr, expected_type=type_hints["versioned_expr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if expr is not None:
            self._values["expr"] = expr
        if versioned_expr is not None:
            self._values["versioned_expr"] = versioned_expr

    @builtins.property
    def config(self) -> typing.Optional["ComputeRegionSecurityPolicyRulesMatchConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#config ComputeRegionSecurityPolicy#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesMatchConfig"], result)

    @builtins.property
    def expr(self) -> typing.Optional["ComputeRegionSecurityPolicyRulesMatchExpr"]:
        '''expr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#expr ComputeRegionSecurityPolicy#expr}
        '''
        result = self._values.get("expr")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesMatchExpr"], result)

    @builtins.property
    def versioned_expr(self) -> typing.Optional[builtins.str]:
        '''Preconfigured versioned expression.

        If this field is specified, config must also be specified.
        Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#versioned_expr ComputeRegionSecurityPolicy#versioned_expr}
        '''
        result = self._values.get("versioned_expr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesMatchConfig",
    jsii_struct_bases=[],
    name_mapping={"src_ip_ranges": "srcIpRanges"},
)
class ComputeRegionSecurityPolicyRulesMatchConfig:
    def __init__(
        self,
        *,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param src_ip_ranges: CIDR IP address range. Maximum number of srcIpRanges allowed is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ip_ranges ComputeRegionSecurityPolicy#src_ip_ranges}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0002711b34841f41c67d4184e3112940413cfe6759d974ec206fc14361e2d367)
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if src_ip_ranges is not None:
            self._values["src_ip_ranges"] = src_ip_ranges

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''CIDR IP address range. Maximum number of srcIpRanges allowed is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ip_ranges ComputeRegionSecurityPolicy#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesMatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesMatchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesMatchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__966d79c220cc2bccbe3a72e45af4cabd6b1bd088669474fc39dc2962ea1ed0a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSrcIpRanges")
    def reset_src_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcIpRanges", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2037997dc661317d1c9b3a61f5044c519f4b2a93fe50f4fdc4bcb443b713e33f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesMatchConfig]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesMatchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulesMatchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2570b33fa52cbe6fcf3ed36844870495c03bd00d50e77970f6cc4bee238f554c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesMatchExpr",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class ComputeRegionSecurityPolicyRulesMatchExpr:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#expression ComputeRegionSecurityPolicy#expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463f52431c1632354a966a3b26af9397e16600d85abcd22bdd628cd682a33222)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Textual representation of an expression in Common Expression Language syntax.

        The application context of the containing message determines which well-known feature set of CEL is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#expression ComputeRegionSecurityPolicy#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesMatchExpr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesMatchExprOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesMatchExprOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a9c602327cbf510cd4d11e31e26f2c32955bab5c60d578266926e94c5052341)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd3fb913311727bca3f0cae7471f25c399b302e939e0c1f8cfd5663a497ff344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesMatchExpr]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesMatchExpr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulesMatchExpr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__289783a9c7c308fab4656e5cca711f25f212733775b8ef66d07fde7b7d2c0d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fc270d18fab8844e0cf0b1f21b85a4e5577f2432f426ac8559748cc9136b75b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param src_ip_ranges: CIDR IP address range. Maximum number of srcIpRanges allowed is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ip_ranges ComputeRegionSecurityPolicy#src_ip_ranges}
        '''
        value = ComputeRegionSecurityPolicyRulesMatchConfig(
            src_ip_ranges=src_ip_ranges
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="putExpr")
    def put_expr(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Textual representation of an expression in Common Expression Language syntax. The application context of the containing message determines which well-known feature set of CEL is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#expression ComputeRegionSecurityPolicy#expression}
        '''
        value = ComputeRegionSecurityPolicyRulesMatchExpr(expression=expression)

        return typing.cast(None, jsii.invoke(self, "putExpr", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetExpr")
    def reset_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpr", []))

    @jsii.member(jsii_name="resetVersionedExpr")
    def reset_versioned_expr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionedExpr", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> ComputeRegionSecurityPolicyRulesMatchConfigOutputReference:
        return typing.cast(ComputeRegionSecurityPolicyRulesMatchConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="expr")
    def expr(self) -> ComputeRegionSecurityPolicyRulesMatchExprOutputReference:
        return typing.cast(ComputeRegionSecurityPolicyRulesMatchExprOutputReference, jsii.get(self, "expr"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesMatchConfig]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesMatchConfig], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="exprInput")
    def expr_input(self) -> typing.Optional[ComputeRegionSecurityPolicyRulesMatchExpr]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesMatchExpr], jsii.get(self, "exprInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7e04ccda5e92f5b5a41a2052b8f16a6b3a01b77d60b2784336a197669578ab52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionedExpr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRegionSecurityPolicyRulesMatch]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulesMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4569d99fb3223dcbd803c23c6363f79d835120f245d032e7d1d03b60e7f65a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesNetworkMatch",
    jsii_struct_bases=[],
    name_mapping={
        "dest_ip_ranges": "destIpRanges",
        "dest_ports": "destPorts",
        "ip_protocols": "ipProtocols",
        "src_asns": "srcAsns",
        "src_ip_ranges": "srcIpRanges",
        "src_ports": "srcPorts",
        "src_region_codes": "srcRegionCodes",
        "user_defined_fields": "userDefinedFields",
    },
)
class ComputeRegionSecurityPolicyRulesNetworkMatch:
    def __init__(
        self,
        *,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_asns: typing.Optional[typing.Sequence[jsii.Number]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dest_ip_ranges: Destination IPv4/IPv6 addresses or CIDR prefixes, in standard text format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#dest_ip_ranges ComputeRegionSecurityPolicy#dest_ip_ranges}
        :param dest_ports: Destination port numbers for TCP/UDP/SCTP. Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#dest_ports ComputeRegionSecurityPolicy#dest_ports}
        :param ip_protocols: IPv4 protocol / IPv6 next header (after extension headers). Each element can be an 8-bit unsigned decimal number (e.g. "6"), range (e.g. "253-254"), or one of the following protocol names: "tcp", "udp", "icmp", "esp", "ah", "ipip", or "sctp". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ip_protocols ComputeRegionSecurityPolicy#ip_protocols}
        :param src_asns: BGP Autonomous System Number associated with the source IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_asns ComputeRegionSecurityPolicy#src_asns}
        :param src_ip_ranges: Source IPv4/IPv6 addresses or CIDR prefixes, in standard text format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ip_ranges ComputeRegionSecurityPolicy#src_ip_ranges}
        :param src_ports: Source port numbers for TCP/UDP/SCTP. Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ports ComputeRegionSecurityPolicy#src_ports}
        :param src_region_codes: Two-letter ISO 3166-1 alpha-2 country code associated with the source IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_region_codes ComputeRegionSecurityPolicy#src_region_codes}
        :param user_defined_fields: user_defined_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#user_defined_fields ComputeRegionSecurityPolicy#user_defined_fields}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6425e3247d3a064408daaf18c053fafeb50b15379311728214cc788420f968b3)
            check_type(argname="argument dest_ip_ranges", value=dest_ip_ranges, expected_type=type_hints["dest_ip_ranges"])
            check_type(argname="argument dest_ports", value=dest_ports, expected_type=type_hints["dest_ports"])
            check_type(argname="argument ip_protocols", value=ip_protocols, expected_type=type_hints["ip_protocols"])
            check_type(argname="argument src_asns", value=src_asns, expected_type=type_hints["src_asns"])
            check_type(argname="argument src_ip_ranges", value=src_ip_ranges, expected_type=type_hints["src_ip_ranges"])
            check_type(argname="argument src_ports", value=src_ports, expected_type=type_hints["src_ports"])
            check_type(argname="argument src_region_codes", value=src_region_codes, expected_type=type_hints["src_region_codes"])
            check_type(argname="argument user_defined_fields", value=user_defined_fields, expected_type=type_hints["user_defined_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dest_ip_ranges is not None:
            self._values["dest_ip_ranges"] = dest_ip_ranges
        if dest_ports is not None:
            self._values["dest_ports"] = dest_ports
        if ip_protocols is not None:
            self._values["ip_protocols"] = ip_protocols
        if src_asns is not None:
            self._values["src_asns"] = src_asns
        if src_ip_ranges is not None:
            self._values["src_ip_ranges"] = src_ip_ranges
        if src_ports is not None:
            self._values["src_ports"] = src_ports
        if src_region_codes is not None:
            self._values["src_region_codes"] = src_region_codes
        if user_defined_fields is not None:
            self._values["user_defined_fields"] = user_defined_fields

    @builtins.property
    def dest_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Destination IPv4/IPv6 addresses or CIDR prefixes, in standard text format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#dest_ip_ranges ComputeRegionSecurityPolicy#dest_ip_ranges}
        '''
        result = self._values.get("dest_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dest_ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Destination port numbers for TCP/UDP/SCTP.

        Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#dest_ports ComputeRegionSecurityPolicy#dest_ports}
        '''
        result = self._values.get("dest_ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IPv4 protocol / IPv6 next header (after extension headers).

        Each element can be an 8-bit unsigned decimal number (e.g. "6"), range (e.g. "253-254"), or one of the following protocol names: "tcp", "udp", "icmp", "esp", "ah", "ipip", or "sctp".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ip_protocols ComputeRegionSecurityPolicy#ip_protocols}
        '''
        result = self._values.get("ip_protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_asns(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''BGP Autonomous System Number associated with the source IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_asns ComputeRegionSecurityPolicy#src_asns}
        '''
        result = self._values.get("src_asns")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def src_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Source IPv4/IPv6 addresses or CIDR prefixes, in standard text format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ip_ranges ComputeRegionSecurityPolicy#src_ip_ranges}
        '''
        result = self._values.get("src_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Source port numbers for TCP/UDP/SCTP.

        Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ports ComputeRegionSecurityPolicy#src_ports}
        '''
        result = self._values.get("src_ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def src_region_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Two-letter ISO 3166-1 alpha-2 country code associated with the source IP address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_region_codes ComputeRegionSecurityPolicy#src_region_codes}
        '''
        result = self._values.get("src_region_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_defined_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields"]]]:
        '''user_defined_fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#user_defined_fields ComputeRegionSecurityPolicy#user_defined_fields}
        '''
        result = self._values.get("user_defined_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesNetworkMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesNetworkMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesNetworkMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ffd5cc5484019ca940dfe6bdd308eb3e51b849f6a54e3aa4d6027f81c54967)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUserDefinedFields")
    def put_user_defined_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395b428988231f3446e50582fb2fdd944647d8f8c4ed5035ed68b183bf647996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUserDefinedFields", [value]))

    @jsii.member(jsii_name="resetDestIpRanges")
    def reset_dest_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestIpRanges", []))

    @jsii.member(jsii_name="resetDestPorts")
    def reset_dest_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestPorts", []))

    @jsii.member(jsii_name="resetIpProtocols")
    def reset_ip_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpProtocols", []))

    @jsii.member(jsii_name="resetSrcAsns")
    def reset_src_asns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcAsns", []))

    @jsii.member(jsii_name="resetSrcIpRanges")
    def reset_src_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcIpRanges", []))

    @jsii.member(jsii_name="resetSrcPorts")
    def reset_src_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcPorts", []))

    @jsii.member(jsii_name="resetSrcRegionCodes")
    def reset_src_region_codes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrcRegionCodes", []))

    @jsii.member(jsii_name="resetUserDefinedFields")
    def reset_user_defined_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefinedFields", []))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFields")
    def user_defined_fields(
        self,
    ) -> "ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsList":
        return typing.cast("ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsList", jsii.get(self, "userDefinedFields"))

    @builtins.property
    @jsii.member(jsii_name="destIpRangesInput")
    def dest_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="destPortsInput")
    def dest_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipProtocolsInput")
    def ip_protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipProtocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcAsnsInput")
    def src_asns_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "srcAsnsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcIpRangesInput")
    def src_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="srcPortsInput")
    def src_ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodesInput")
    def src_region_codes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "srcRegionCodesInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedFieldsInput")
    def user_defined_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields"]]], jsii.get(self, "userDefinedFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="destIpRanges")
    def dest_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destIpRanges"))

    @dest_ip_ranges.setter
    def dest_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a6bce1a545021fe32a187f1ff01df05ca8b7244cdbf5d47895c9f320b9cae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destPorts")
    def dest_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destPorts"))

    @dest_ports.setter
    def dest_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d321561b722ca6b8b022195a964687453ded0761d3824577e97d5cf17db7107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipProtocols")
    def ip_protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipProtocols"))

    @ip_protocols.setter
    def ip_protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0d07dcf550ec9b5d2303690f3cbe005506d2facb991b27637e2e08846bcdc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipProtocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcAsns")
    def src_asns(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "srcAsns"))

    @src_asns.setter
    def src_asns(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5610ca5263332a2e2653acc988ed9bba222abe97ed6c2c7d0bd583b25616dc8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcAsns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcIpRanges")
    def src_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcIpRanges"))

    @src_ip_ranges.setter
    def src_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65ab30966b20412f3e66f403ec5cb9eb7bf4bc2f192dfc3cf200201fc6216b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcPorts")
    def src_ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcPorts"))

    @src_ports.setter
    def src_ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466b490f2b1938dffe1ee54092aad4d18d5f6f85d62434b815fdba1495cfeb2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="srcRegionCodes")
    def src_region_codes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "srcRegionCodes"))

    @src_region_codes.setter
    def src_region_codes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3d450bdcd2ccd84dcac887e482d1f0baf85159edb16ee56d83d2b3a1cb018b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "srcRegionCodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesNetworkMatch]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesNetworkMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulesNetworkMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9182ac57633390174c0bf595e5118621f73a9c88d976f7088c4a6004ba7a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Name of the user-defined field, as given in the definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#name ComputeRegionSecurityPolicy#name}
        :param values: Matching values of the field. Each element can be a 32-bit unsigned decimal or hexadecimal (starting with "0x") number (e.g. "64") or range (e.g. "0x400-0x7ff"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#values ComputeRegionSecurityPolicy#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0b25fe0a3d85060aeb6c2eb9756b0eefb0b8a0cff063d3da5148635d13c5ad)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the user-defined field, as given in the definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#name ComputeRegionSecurityPolicy#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Matching values of the field.

        Each element can be a 32-bit unsigned decimal or hexadecimal (starting with "0x") number (e.g. "64") or range (e.g. "0x400-0x7ff").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#values ComputeRegionSecurityPolicy#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02d84b5a33be52ea607ebe08a3d834acb77a837a3e11dca0bdf50b33ce4ef013)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24260af5f6fcc155735ac514fa95293b0b88d2ffd93ff4c03853ab262e976983)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31da08a23d6c082ef27cfb504d72609892fc5945c495c9089717fe2fe8bd317)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9d8a199481895e7c78c780edd439dffd6eeabe204d21e2ab3b39e7b1ef3e5b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68f515c652493af9c52cc530ea1097261c815f54ddf62a0726326ace10eaa006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0cc99d96cfbb824bc20fd56a44721ba135fa931a80673ce04a177bd935b6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6682f3104e30d033f0f1b3ad7a60d147ccd6c0d48dcb5eccf357d539db197fce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436e531e72e5c5a9b20f43a5308c00691dca16f5c34f3e9206bbed0bb64790ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199083b30283568e3f6ade96480a9ab4bdf7a307dc111680e437f393548baa4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f534077fd39fede33d182186f794276d363a346d73353971ba5b3c55453bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27cd60e991a568c70ae683f0a1b87dfa687e97e6e51cffeed5c6d26070e24cf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        *,
        config: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesMatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        expr: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesMatchExpr, typing.Dict[builtins.str, typing.Any]]] = None,
        versioned_expr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#config ComputeRegionSecurityPolicy#config}
        :param expr: expr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#expr ComputeRegionSecurityPolicy#expr}
        :param versioned_expr: Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding srcIpRange field in config. Possible values: ["SRC_IPS_V1"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#versioned_expr ComputeRegionSecurityPolicy#versioned_expr}
        '''
        value = ComputeRegionSecurityPolicyRulesMatch(
            config=config, expr=expr, versioned_expr=versioned_expr
        )

        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="putNetworkMatch")
    def put_network_match(
        self,
        *,
        dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        dest_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_asns: typing.Optional[typing.Sequence[jsii.Number]] = None,
        src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
        src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param dest_ip_ranges: Destination IPv4/IPv6 addresses or CIDR prefixes, in standard text format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#dest_ip_ranges ComputeRegionSecurityPolicy#dest_ip_ranges}
        :param dest_ports: Destination port numbers for TCP/UDP/SCTP. Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#dest_ports ComputeRegionSecurityPolicy#dest_ports}
        :param ip_protocols: IPv4 protocol / IPv6 next header (after extension headers). Each element can be an 8-bit unsigned decimal number (e.g. "6"), range (e.g. "253-254"), or one of the following protocol names: "tcp", "udp", "icmp", "esp", "ah", "ipip", or "sctp". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ip_protocols ComputeRegionSecurityPolicy#ip_protocols}
        :param src_asns: BGP Autonomous System Number associated with the source IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_asns ComputeRegionSecurityPolicy#src_asns}
        :param src_ip_ranges: Source IPv4/IPv6 addresses or CIDR prefixes, in standard text format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ip_ranges ComputeRegionSecurityPolicy#src_ip_ranges}
        :param src_ports: Source port numbers for TCP/UDP/SCTP. Each element can be a 16-bit unsigned decimal number (e.g. "80") or range (e.g. "0-1023"). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_ports ComputeRegionSecurityPolicy#src_ports}
        :param src_region_codes: Two-letter ISO 3166-1 alpha-2 country code associated with the source IP address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#src_region_codes ComputeRegionSecurityPolicy#src_region_codes}
        :param user_defined_fields: user_defined_fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#user_defined_fields ComputeRegionSecurityPolicy#user_defined_fields}
        '''
        value = ComputeRegionSecurityPolicyRulesNetworkMatch(
            dest_ip_ranges=dest_ip_ranges,
            dest_ports=dest_ports,
            ip_protocols=ip_protocols,
            src_asns=src_asns,
            src_ip_ranges=src_ip_ranges,
            src_ports=src_ports,
            src_region_codes=src_region_codes,
            user_defined_fields=user_defined_fields,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkMatch", [value]))

    @jsii.member(jsii_name="putPreconfiguredWafConfig")
    def put_preconfigured_waf_config(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#exclusion ComputeRegionSecurityPolicy#exclusion}
        '''
        value = ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig(
            exclusion=exclusion
        )

        return typing.cast(None, jsii.invoke(self, "putPreconfiguredWafConfig", [value]))

    @jsii.member(jsii_name="putRateLimitOptions")
    def put_rate_limit_options(
        self,
        *,
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        conform_action: typing.Optional[builtins.str] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_action: typing.Optional[builtins.str] = None,
        rate_limit_threshold: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ban_duration_sec ComputeRegionSecurityPolicy#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ban_threshold ComputeRegionSecurityPolicy#ban_threshold}
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#conform_action ComputeRegionSecurityPolicy#conform_action}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key ComputeRegionSecurityPolicy#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_configs ComputeRegionSecurityPolicy#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_name ComputeRegionSecurityPolicy#enforce_on_key_name}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to deny with a specified HTTP response code. Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#exceed_action ComputeRegionSecurityPolicy#exceed_action}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#rate_limit_threshold ComputeRegionSecurityPolicy#rate_limit_threshold}
        '''
        value = ComputeRegionSecurityPolicyRulesRateLimitOptions(
            ban_duration_sec=ban_duration_sec,
            ban_threshold=ban_threshold,
            conform_action=conform_action,
            enforce_on_key=enforce_on_key,
            enforce_on_key_configs=enforce_on_key_configs,
            enforce_on_key_name=enforce_on_key_name,
            exceed_action=exceed_action,
            rate_limit_threshold=rate_limit_threshold,
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimitOptions", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetNetworkMatch")
    def reset_network_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkMatch", []))

    @jsii.member(jsii_name="resetPreconfiguredWafConfig")
    def reset_preconfigured_waf_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreconfiguredWafConfig", []))

    @jsii.member(jsii_name="resetPreview")
    def reset_preview(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreview", []))

    @jsii.member(jsii_name="resetRateLimitOptions")
    def reset_rate_limit_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimitOptions", []))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> ComputeRegionSecurityPolicyRulesMatchOutputReference:
        return typing.cast(ComputeRegionSecurityPolicyRulesMatchOutputReference, jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="networkMatch")
    def network_match(
        self,
    ) -> ComputeRegionSecurityPolicyRulesNetworkMatchOutputReference:
        return typing.cast(ComputeRegionSecurityPolicyRulesNetworkMatchOutputReference, jsii.get(self, "networkMatch"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfig")
    def preconfigured_waf_config(
        self,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigOutputReference", jsii.get(self, "preconfiguredWafConfig"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitOptions")
    def rate_limit_options(
        self,
    ) -> "ComputeRegionSecurityPolicyRulesRateLimitOptionsOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRulesRateLimitOptionsOutputReference", jsii.get(self, "rateLimitOptions"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(self) -> typing.Optional[ComputeRegionSecurityPolicyRulesMatch]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesMatch], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="networkMatchInput")
    def network_match_input(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesNetworkMatch]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesNetworkMatch], jsii.get(self, "networkMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="preconfiguredWafConfigInput")
    def preconfigured_waf_config_input(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig"], jsii.get(self, "preconfiguredWafConfigInput"))

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
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptions"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptions"], jsii.get(self, "rateLimitOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9038f8185830b8939df63cb2cf31e9c066697da92d95cb340996103d3a7496c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15de9c5d44a2f781114e4ce2ad3d7328ea915743744b804d9cdeb7cfd7eeaf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5564163349d33804e5cfe018c8214abb305d0da361bb165a3d6734ef77bb7429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preview", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48a183385eab0c06d8914a380f9653eb4d8f743d5ec681b167c2c69f8feada4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcca5639dc9d404045e7b98359a85fe82baabff2349f908eabe4f59001e0a276)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig",
    jsii_struct_bases=[],
    name_mapping={"exclusion": "exclusion"},
)
class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig:
    def __init__(
        self,
        *,
        exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param exclusion: exclusion block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#exclusion ComputeRegionSecurityPolicy#exclusion}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c4ba74c99bd9777d28f383a7c820acfb284e0f2bb092ee41c45e4aaee31b1f)
            check_type(argname="argument exclusion", value=exclusion, expected_type=type_hints["exclusion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusion is not None:
            self._values["exclusion"] = exclusion

    @builtins.property
    def exclusion(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion"]]]:
        '''exclusion block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#exclusion ComputeRegionSecurityPolicy#exclusion}
        '''
        result = self._values.get("exclusion")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion",
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
class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion:
    def __init__(
        self,
        *,
        target_rule_set: builtins.str,
        request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam", typing.Dict[builtins.str, typing.Any]]]]] = None,
        request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param target_rule_set: Target WAF rule set to apply the preconfigured WAF exclusion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#target_rule_set ComputeRegionSecurityPolicy#target_rule_set}
        :param request_cookie: request_cookie block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#request_cookie ComputeRegionSecurityPolicy#request_cookie}
        :param request_header: request_header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#request_header ComputeRegionSecurityPolicy#request_header}
        :param request_query_param: request_query_param block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#request_query_param ComputeRegionSecurityPolicy#request_query_param}
        :param request_uri: request_uri block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#request_uri ComputeRegionSecurityPolicy#request_uri}
        :param target_rule_ids: A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion. If omitted, it refers to all the rule IDs under the WAF rule set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#target_rule_ids ComputeRegionSecurityPolicy#target_rule_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5abfbe58f769d17d3c9cbfd713110adf36fecb1b9980d3b01b642df47a55d35)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#target_rule_set ComputeRegionSecurityPolicy#target_rule_set}
        '''
        result = self._values.get("target_rule_set")
        assert result is not None, "Required property 'target_rule_set' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_cookie(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie"]]]:
        '''request_cookie block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#request_cookie ComputeRegionSecurityPolicy#request_cookie}
        '''
        result = self._values.get("request_cookie")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie"]]], result)

    @builtins.property
    def request_header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader"]]]:
        '''request_header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#request_header ComputeRegionSecurityPolicy#request_header}
        '''
        result = self._values.get("request_header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader"]]], result)

    @builtins.property
    def request_query_param(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam"]]]:
        '''request_query_param block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#request_query_param ComputeRegionSecurityPolicy#request_query_param}
        '''
        result = self._values.get("request_query_param")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam"]]], result)

    @builtins.property
    def request_uri(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri"]]]:
        '''request_uri block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#request_uri ComputeRegionSecurityPolicy#request_uri}
        '''
        result = self._values.get("request_uri")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri"]]], result)

    @builtins.property
    def target_rule_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of target rule IDs under the WAF rule set to apply the preconfigured WAF exclusion.

        If omitted, it refers to all the rule IDs under the WAF rule set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#target_rule_ids ComputeRegionSecurityPolicy#target_rule_ids}
        '''
        result = self._values.get("target_rule_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5ac7b1716fdd333618434850d35f33aedf0300b2399e612436ab6357d633a8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dfd37f42a6072a45f4d12ce274a74adba70d7b3b8659af07d4a7f39b11319c0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62603d9fa708a51fbaf426d4528ca8b4c6ca45d26263d3abbfac63f7c239e2fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__003a50f2f223fe47825da2e30687a0b193f8590d79139c3285a2357a673d7e32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66e90086f9cc607760c04d4daaf441a6e1fd110e2f87b1160c607a9893cc739e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345b14b3c2791f1e527b760f606e22d30e99928c42ad69c6a082c2c5def6c9cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a07a6ef02bdb2de5185895b48dc1f8f943948129aa57852762c11c4cba52f09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRequestCookie")
    def put_request_cookie(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146c8152ef37801fb030c53b49d009588a0d409f201b51b6018fc4a15f5c800f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestCookie", [value]))

    @jsii.member(jsii_name="putRequestHeader")
    def put_request_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ad8fddedb8cf9103b64d4ebb4e3abc42965601acc8856d93f69737f44440cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestHeader", [value]))

    @jsii.member(jsii_name="putRequestQueryParam")
    def put_request_query_param(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd627c7c73343099bf0f7199b7d6b015b77a642b6bda8d61c285c09eda833c9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRequestQueryParam", [value]))

    @jsii.member(jsii_name="putRequestUri")
    def put_request_uri(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a707780ec7f1fe5494c2964b959c066554572dc21b57cf4d1e6b2864f3ec916f)
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
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieList":
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieList", jsii.get(self, "requestCookie"))

    @builtins.property
    @jsii.member(jsii_name="requestHeader")
    def request_header(
        self,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderList":
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderList", jsii.get(self, "requestHeader"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParam")
    def request_query_param(
        self,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamList":
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamList", jsii.get(self, "requestQueryParam"))

    @builtins.property
    @jsii.member(jsii_name="requestUri")
    def request_uri(
        self,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriList":
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriList", jsii.get(self, "requestUri"))

    @builtins.property
    @jsii.member(jsii_name="requestCookieInput")
    def request_cookie_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie"]]], jsii.get(self, "requestCookieInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderInput")
    def request_header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader"]]], jsii.get(self, "requestHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="requestQueryParamInput")
    def request_query_param_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam"]]], jsii.get(self, "requestQueryParamInput"))

    @builtins.property
    @jsii.member(jsii_name="requestUriInput")
    def request_uri_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri"]]], jsii.get(self, "requestUriInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__11d9cbc10fa2e4e10dc244c45e5fa5f38ee50c8820d5a5660a1388c22d651b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetRuleSet")
    def target_rule_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRuleSet"))

    @target_rule_set.setter
    def target_rule_set(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7356957aa3cd135aeda0f9e5961131c4dde8460e73ab89cd30fd816909642ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRuleSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a192ffeeae44313a989b4eae2350178b6d97aa699949bc7fcc5247b5f47198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#operator ComputeRegionSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#value ComputeRegionSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586e116284bc84a244405be34f4ec6a5dc6918dcbc925742f36e020297093fe5)
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

        Available options:
        EQUALS: The operator matches if the field value equals the specified value.
        STARTS_WITH: The operator matches if the field value starts with the specified value.
        ENDS_WITH: The operator matches if the field value ends with the specified value.
        CONTAINS: The operator matches if the field value contains the specified value.
        EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#operator ComputeRegionSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#value ComputeRegionSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23a7a8c9570a1a331a7b57cd9fccf5ff9e7e7e50689c7101e055705c81b63d13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ab91f339fcc11722ccdfcbeaacfe17974e39db6d579b4883de46b9c63d3811)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430f739bf74a67d2118c44da4b08091dd367e6fd51de02cb42a68c52e6ff5a87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6d4adb8b988fb6bea48000bb15111f5419bed5fad9f348b75c9ed1e93de0fb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c0db6b2d7a30c4a91be5c4713b05c1ac89afff04182a538bcdce43b37a2cb80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a229b741b8c83817e100c07afec28c5fbf81c9b1d52f197ca1c8128c2508a97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35eab3e5805557bdaaf619847f3bbb72abba0c9c02141dea5f70616a5f89abaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f008ccefe0aae500e0aeb0cff66bdd589245b952d2ca973e27bcb3fa772cbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046d5722f0fb1f676bb90ccacfe01f4301b95644da62831b622efa91e8a9d3fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd793b1a70828e9ab8aa2863da6069a425b1f887a30f875d05621dcb7905df6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#operator ComputeRegionSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#value ComputeRegionSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f87d43c581f1e9b6ffdb4de90389151430beff8ec4307ca8de134e92f67d0d)
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

        Available options:
        EQUALS: The operator matches if the field value equals the specified value.
        STARTS_WITH: The operator matches if the field value starts with the specified value.
        ENDS_WITH: The operator matches if the field value ends with the specified value.
        CONTAINS: The operator matches if the field value contains the specified value.
        EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#operator ComputeRegionSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#value ComputeRegionSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__835b1a453fe56dbc945152caff52d868960474f6bc97a83d2667dfc29efbe3f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b7b35c90b57756f1bb02c69e952d8c0199c329cfa2f97fcef76668f9db04e9c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec9d3a2c679c471bcb14396287da86a7db9f9e4e0fb2601f57cf59e6d8292cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4104c70c6c6aa10ae0544dacd543993a25689178843dc5a4b060e3a6ea447e87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2999451649117072cb40069a8442d6754df4a6a2850b1fc4f2ca42eb025d79d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e015c5cdebb54f5d774da35a4165515a6394dce0aba29e5cded283adacd31ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a43a17757b985c8f0be027fd2f6d352ebfb6408d405562b752c6de306b920618)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f02fc442b138a8b2cfa3f28b8fd1c7f8215b071a02320976cb29a4ac851a01c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928e1ab01d9186dd8b3ac85a5bd4994c4c67570ce552d8b9ff95acc028e623ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3db31177fbebc2332b31349de7a64caf4d3f4a160ffdb9ae652db3fdc4f1d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#operator ComputeRegionSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#value ComputeRegionSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3577ce5af3fbcb4bef21065668b151380645697e64612fc9e2c5a2a21da98a)
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

        Available options:
        EQUALS: The operator matches if the field value equals the specified value.
        STARTS_WITH: The operator matches if the field value starts with the specified value.
        ENDS_WITH: The operator matches if the field value ends with the specified value.
        CONTAINS: The operator matches if the field value contains the specified value.
        EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#operator ComputeRegionSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#value ComputeRegionSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a51cce2df031deecc0369dfe7e8304a1986084d099951524efdedcfee3beeb15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa50a06423f675b00c308b945f24d52626d72301617eb91a44bea5e01d764e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c125f0fcc5d515fee752c43ba1a0251e2131fbc1b6b90ac5de89ef3b659051ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bae0b9f9e6474be689504d440231e1822960244d74fedbd2824a2be174d00f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__177121df2ca4b69cba78a424e7a891a06e6eadef78718949ea6a7a48d0a8bc56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5127be06835d8dbad722f70b9f738b9e7a95c5ab4f06c50f06ffdba01f44ac61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__402c732773dbd646b173432f5e18eddcb6eab7347deb6996fea7a476faae6149)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4765cd37d38711bf47a051338155a434f7ac10bba6dbd837d8461dd6bfaba6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ef2fb3b9b9ebdf67b316946abc7517905aa82bff1251cab87574d21331d296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0655c2cac7af39fafd63fef177db77fa4621f64d0fce74bd5b3a1ed331bf9363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "value": "value"},
)
class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri:
    def __init__(
        self,
        *,
        operator: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param operator: You can specify an exact match or a partial match by using a field operator and a field value. Available options: EQUALS: The operator matches if the field value equals the specified value. STARTS_WITH: The operator matches if the field value starts with the specified value. ENDS_WITH: The operator matches if the field value ends with the specified value. CONTAINS: The operator matches if the field value contains the specified value. EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#operator ComputeRegionSecurityPolicy#operator}
        :param value: A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation. The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#value ComputeRegionSecurityPolicy#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241543090feffd50c2a541866523ca8de43d9526f4bc4313b5c079c2baa5cdd4)
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

        Available options:
        EQUALS: The operator matches if the field value equals the specified value.
        STARTS_WITH: The operator matches if the field value starts with the specified value.
        ENDS_WITH: The operator matches if the field value ends with the specified value.
        CONTAINS: The operator matches if the field value contains the specified value.
        EQUALS_ANY: The operator matches if the field value is any value. Possible values: ["CONTAINS", "ENDS_WITH", "EQUALS", "EQUALS_ANY", "STARTS_WITH"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#operator ComputeRegionSecurityPolicy#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''A request field matching the specified value will be excluded from inspection during preconfigured WAF evaluation.

        The field value must be given if the field operator is not EQUALS_ANY, and cannot be given if the field operator is EQUALS_ANY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#value ComputeRegionSecurityPolicy#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d38b8c47606e45b49f516bb1aba41a78555faa32554b33027523f90e115a677)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0b6ed3c088bd05424c1b0ad61a9d28d8c1b089ca31af2bc5155db0dbb65020a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea1ed772121be127fa8c6c82a314191b7214d036ab8f8ca7be52267d416be65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1864cc5a77770c117113f84521bdfa9740c36a49b1a47150f3d3d5275e4df8ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02f3ed0575d142d219e2eadaa1088f6101d25d21f4ed8f03a21362c685d500b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687fbefdb899aa54ea578f2ceacce22712f77bd2627287c0d835abbc38d462ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec1ab10f401bbb183e3aa5a59ab2459e1c2afbd1d74d20ae7a837417eda7ad2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e22f63812eb9e32b82a79c0813bc39144f164ce485b38c17026b73a7a8f0655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20848e7535ee9b64a04bee963388203c76e74aa3fbddac1de7a4efba37d3a263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15392ca460bc6c1a2109e2333720eb41b4d348853fca685a7c1e264c20e6c44b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc7e3f41ec22aa58c609e0110b5f96cca421598f216733fa48316557681eb70b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusion")
    def put_exclusion(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e4d2b06a15eb5bda4fd8f3585cfd80248bc53b9b7e8df8148b92a5be46f5d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusion", [value]))

    @jsii.member(jsii_name="resetExclusion")
    def reset_exclusion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusion", []))

    @builtins.property
    @jsii.member(jsii_name="exclusion")
    def exclusion(
        self,
    ) -> ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionList:
        return typing.cast(ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionList, jsii.get(self, "exclusion"))

    @builtins.property
    @jsii.member(jsii_name="exclusionInput")
    def exclusion_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]]], jsii.get(self, "exclusionInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8bbe33ae39b57b802a7f1bb2a2423432ab3dbcf11275a12aa4bc5b52f85bfd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ban_duration_sec": "banDurationSec",
        "ban_threshold": "banThreshold",
        "conform_action": "conformAction",
        "enforce_on_key": "enforceOnKey",
        "enforce_on_key_configs": "enforceOnKeyConfigs",
        "enforce_on_key_name": "enforceOnKeyName",
        "exceed_action": "exceedAction",
        "rate_limit_threshold": "rateLimitThreshold",
    },
)
class ComputeRegionSecurityPolicyRulesRateLimitOptions:
    def __init__(
        self,
        *,
        ban_duration_sec: typing.Optional[jsii.Number] = None,
        ban_threshold: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
        conform_action: typing.Optional[builtins.str] = None,
        enforce_on_key: typing.Optional[builtins.str] = None,
        enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        exceed_action: typing.Optional[builtins.str] = None,
        rate_limit_threshold: typing.Optional[typing.Union["ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ban_duration_sec: Can only be specified if the action for the rule is "rate_based_ban". If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ban_duration_sec ComputeRegionSecurityPolicy#ban_duration_sec}
        :param ban_threshold: ban_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ban_threshold ComputeRegionSecurityPolicy#ban_threshold}
        :param conform_action: Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#conform_action ComputeRegionSecurityPolicy#conform_action}
        :param enforce_on_key: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key ComputeRegionSecurityPolicy#enforce_on_key}
        :param enforce_on_key_configs: enforce_on_key_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_configs ComputeRegionSecurityPolicy#enforce_on_key_configs}
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_name ComputeRegionSecurityPolicy#enforce_on_key_name}
        :param exceed_action: Action to take for requests that are above the configured rate limit threshold, to deny with a specified HTTP response code. Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#exceed_action ComputeRegionSecurityPolicy#exceed_action}
        :param rate_limit_threshold: rate_limit_threshold block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#rate_limit_threshold ComputeRegionSecurityPolicy#rate_limit_threshold}
        '''
        if isinstance(ban_threshold, dict):
            ban_threshold = ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold(**ban_threshold)
        if isinstance(rate_limit_threshold, dict):
            rate_limit_threshold = ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold(**rate_limit_threshold)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac360ee9672fe20eefb07afbaadbd1ae0c67bf20f636fe65cc37bcf10a19969)
            check_type(argname="argument ban_duration_sec", value=ban_duration_sec, expected_type=type_hints["ban_duration_sec"])
            check_type(argname="argument ban_threshold", value=ban_threshold, expected_type=type_hints["ban_threshold"])
            check_type(argname="argument conform_action", value=conform_action, expected_type=type_hints["conform_action"])
            check_type(argname="argument enforce_on_key", value=enforce_on_key, expected_type=type_hints["enforce_on_key"])
            check_type(argname="argument enforce_on_key_configs", value=enforce_on_key_configs, expected_type=type_hints["enforce_on_key_configs"])
            check_type(argname="argument enforce_on_key_name", value=enforce_on_key_name, expected_type=type_hints["enforce_on_key_name"])
            check_type(argname="argument exceed_action", value=exceed_action, expected_type=type_hints["exceed_action"])
            check_type(argname="argument rate_limit_threshold", value=rate_limit_threshold, expected_type=type_hints["rate_limit_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ban_duration_sec is not None:
            self._values["ban_duration_sec"] = ban_duration_sec
        if ban_threshold is not None:
            self._values["ban_threshold"] = ban_threshold
        if conform_action is not None:
            self._values["conform_action"] = conform_action
        if enforce_on_key is not None:
            self._values["enforce_on_key"] = enforce_on_key
        if enforce_on_key_configs is not None:
            self._values["enforce_on_key_configs"] = enforce_on_key_configs
        if enforce_on_key_name is not None:
            self._values["enforce_on_key_name"] = enforce_on_key_name
        if exceed_action is not None:
            self._values["exceed_action"] = exceed_action
        if rate_limit_threshold is not None:
            self._values["rate_limit_threshold"] = rate_limit_threshold

    @builtins.property
    def ban_duration_sec(self) -> typing.Optional[jsii.Number]:
        '''Can only be specified if the action for the rule is "rate_based_ban".

        If specified, determines the time (in seconds) the traffic will continue to be banned by the rate limit after the rate falls below the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ban_duration_sec ComputeRegionSecurityPolicy#ban_duration_sec}
        '''
        result = self._values.get("ban_duration_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ban_threshold(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold"]:
        '''ban_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#ban_threshold ComputeRegionSecurityPolicy#ban_threshold}
        '''
        result = self._values.get("ban_threshold")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold"], result)

    @builtins.property
    def conform_action(self) -> typing.Optional[builtins.str]:
        '''Action to take for requests that are under the configured rate limit threshold. Valid option is "allow" only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#conform_action ComputeRegionSecurityPolicy#conform_action}
        '''
        result = self._values.get("conform_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key(self) -> typing.Optional[builtins.str]:
        '''Determines the key to enforce the rateLimitThreshold on.

        Possible values are:

        - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKey" is not configured.
        - IP: The source IP address of the request is the key. Each IP has this limit enforced separately.
        - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL.
        - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP.
        - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL.
        - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes.
        - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session.
        - REGION_CODE: The country/region from which the request originates.
        - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL.
        - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL.
        - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key ComputeRegionSecurityPolicy#enforce_on_key}
        '''
        result = self._values.get("enforce_on_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs"]]]:
        '''enforce_on_key_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_configs ComputeRegionSecurityPolicy#enforce_on_key_configs}
        '''
        result = self._values.get("enforce_on_key_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs"]]], result)

    @builtins.property
    def enforce_on_key_name(self) -> typing.Optional[builtins.str]:
        '''Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value.

        HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_name ComputeRegionSecurityPolicy#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exceed_action(self) -> typing.Optional[builtins.str]:
        '''Action to take for requests that are above the configured rate limit threshold, to deny with a specified HTTP response code.

        Valid options are deny(STATUS), where valid values for STATUS are 403, 404, 429, and 502.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#exceed_action ComputeRegionSecurityPolicy#exceed_action}
        '''
        result = self._values.get("exceed_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limit_threshold(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold"]:
        '''rate_limit_threshold block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#rate_limit_threshold ComputeRegionSecurityPolicy#rate_limit_threshold}
        '''
        result = self._values.get("rate_limit_threshold")
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesRateLimitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#count ComputeRegionSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#interval_sec ComputeRegionSecurityPolicy#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca286cb8f965f239979801294f640b230f973f8790b186b8248b7b8adf78837)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval_sec", value=interval_sec, expected_type=type_hints["interval_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval_sec is not None:
            self._values["interval_sec"] = interval_sec

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Number of HTTP(S) requests for calculating the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#count ComputeRegionSecurityPolicy#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_sec(self) -> typing.Optional[jsii.Number]:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#interval_sec ComputeRegionSecurityPolicy#interval_sec}
        '''
        result = self._values.get("interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e015c07d00828f705abe35ce649ad0c2ca770e1a423d1799075fb7508fa7f705)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetIntervalSec")
    def reset_interval_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSec", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a21f09cd9dc6ab08dbc5d28cc804e3c108c2acb2b170cc23da6f64be851c5d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390507953484de658b0a3e535e6a5f0dc95ec319a57bb093a36ddd5efbf26412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5cad28c967d6c17ad321cfdeed5b146b85760573d2fc9c9cda1cc93adfad30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "enforce_on_key_name": "enforceOnKeyName",
        "enforce_on_key_type": "enforceOnKeyType",
    },
)
class ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs:
    def __init__(
        self,
        *,
        enforce_on_key_name: typing.Optional[builtins.str] = None,
        enforce_on_key_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enforce_on_key_name: Rate limit key name applicable only for the following key types: HTTP_HEADER -- Name of the HTTP header whose value is taken as the key value. HTTP_COOKIE -- Name of the HTTP cookie whose value is taken as the key value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_name ComputeRegionSecurityPolicy#enforce_on_key_name}
        :param enforce_on_key_type: Determines the key to enforce the rateLimitThreshold on. Possible values are: - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKeyConfigs" is not configured. - IP: The source IP address of the request is the key. Each IP has this limit enforced separately. - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL. - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP. - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL. - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes. - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session. - REGION_CODE: The country/region from which the request originates. - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL. - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_type ComputeRegionSecurityPolicy#enforce_on_key_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ae5914f6a3c772559eea42f9f56182691d5e727120fbacc9fc93564a1d8a72)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_name ComputeRegionSecurityPolicy#enforce_on_key_name}
        '''
        result = self._values.get("enforce_on_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_on_key_type(self) -> typing.Optional[builtins.str]:
        '''Determines the key to enforce the rateLimitThreshold on.

        Possible values are:

        - ALL: A single rate limit threshold is applied to all the requests matching this rule. This is the default value if "enforceOnKeyConfigs" is not configured.
        - IP: The source IP address of the request is the key. Each IP has this limit enforced separately.
        - HTTP_HEADER: The value of the HTTP header whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the header value. If no such header is present in the request, the key type defaults to ALL.
        - XFF_IP: The first IP address (i.e. the originating client IP address) specified in the list of IPs under X-Forwarded-For HTTP header. If no such header is present or the value is not a valid IP, the key defaults to the source IP address of the request i.e. key type IP.
        - HTTP_COOKIE: The value of the HTTP cookie whose name is configured under "enforceOnKeyName". The key value is truncated to the first 128 bytes of the cookie value. If no such cookie is present in the request, the key type defaults to ALL.
        - HTTP_PATH: The URL path of the HTTP request. The key value is truncated to the first 128 bytes.
        - SNI: Server name indication in the TLS session of the HTTPS request. The key value is truncated to the first 128 bytes. The key type defaults to ALL on a HTTP session.
        - REGION_CODE: The country/region from which the request originates.
        - TLS_JA3_FINGERPRINT: JA3 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL.
        - TLS_JA4_FINGERPRINT: JA4 TLS/SSL fingerprint if the client connects using HTTPS, HTTP/2 or HTTP/3. If not available, the key type defaults to ALL.
        - USER_IP: The IP address of the originating client, which is resolved based on "userIpRequestHeaders" configured with the security policy. If there is no "userIpRequestHeaders" configuration or an IP address cannot be resolved from it, the key type defaults to IP. Possible values: ["ALL", "IP", "HTTP_HEADER", "XFF_IP", "HTTP_COOKIE", "HTTP_PATH", "SNI", "REGION_CODE", "TLS_JA3_FINGERPRINT", "TLS_JA4_FINGERPRINT", "USER_IP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#enforce_on_key_type ComputeRegionSecurityPolicy#enforce_on_key_type}
        '''
        result = self._values.get("enforce_on_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa22f0bb278af9558fd209e8214e0cbdb15d40885956b0433aff57ed61dcc9b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000640fe73dd3f7f21c50edf042292ae9eebdb79212aa3413b17997a1a050cb8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f352c773cd7177a19a6091cb0b1a6bf7794de2e41e51a81339c18a6b16f7e548)
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
            type_hints = typing.get_type_hints(_typecheckingstub__780852e3141052a2a33a4789037081713f79e3d3a0b8dde8d4c591b651c79eb8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8908a8ac625dfaed9244afd038d66a8ed6c947074dceb86548d6fb7f90ed67cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69962c04b51be45f68cf82d890d6cf3c13dfd3b710a03e09fb1016f7aa67c10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95551714447d7a993165a208f0b1b9a05c40af42efd2e0576a9e55eb1eb436cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b39c6706579b53f64f9963fbae7ed1db90e3d4d06adc011ed78c67a513c251f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyType")
    def enforce_on_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyType"))

    @enforce_on_key_type.setter
    def enforce_on_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3c5aa25685e843863b8a0b3cff9c8adc3106569cc281534a32a333cf13535b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ceef096c8f3a694292fc7d4c9050845c9cee05c8efc7a99932404b5502e8627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyRulesRateLimitOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d9a3411ad0f319ae582ad65010b847d26c32b3d5a2bed51295ed1d0ebdb292b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBanThreshold")
    def put_ban_threshold(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#count ComputeRegionSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#interval_sec ComputeRegionSecurityPolicy#interval_sec}
        '''
        value = ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putBanThreshold", [value]))

    @jsii.member(jsii_name="putEnforceOnKeyConfigs")
    def put_enforce_on_key_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf06e700c34e6eb1663e887274243e67318398dcea1fd3421ce4c48458ddddad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnforceOnKeyConfigs", [value]))

    @jsii.member(jsii_name="putRateLimitThreshold")
    def put_rate_limit_threshold(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#count ComputeRegionSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#interval_sec ComputeRegionSecurityPolicy#interval_sec}
        '''
        value = ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold(
            count=count, interval_sec=interval_sec
        )

        return typing.cast(None, jsii.invoke(self, "putRateLimitThreshold", [value]))

    @jsii.member(jsii_name="resetBanDurationSec")
    def reset_ban_duration_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBanDurationSec", []))

    @jsii.member(jsii_name="resetBanThreshold")
    def reset_ban_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBanThreshold", []))

    @jsii.member(jsii_name="resetConformAction")
    def reset_conform_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConformAction", []))

    @jsii.member(jsii_name="resetEnforceOnKey")
    def reset_enforce_on_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKey", []))

    @jsii.member(jsii_name="resetEnforceOnKeyConfigs")
    def reset_enforce_on_key_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyConfigs", []))

    @jsii.member(jsii_name="resetEnforceOnKeyName")
    def reset_enforce_on_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceOnKeyName", []))

    @jsii.member(jsii_name="resetExceedAction")
    def reset_exceed_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExceedAction", []))

    @jsii.member(jsii_name="resetRateLimitThreshold")
    def reset_rate_limit_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimitThreshold", []))

    @builtins.property
    @jsii.member(jsii_name="banThreshold")
    def ban_threshold(
        self,
    ) -> ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThresholdOutputReference:
        return typing.cast(ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThresholdOutputReference, jsii.get(self, "banThreshold"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigs")
    def enforce_on_key_configs(
        self,
    ) -> ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsList:
        return typing.cast(ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsList, jsii.get(self, "enforceOnKeyConfigs"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitThreshold")
    def rate_limit_threshold(
        self,
    ) -> "ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThresholdOutputReference":
        return typing.cast("ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThresholdOutputReference", jsii.get(self, "rateLimitThreshold"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSecInput")
    def ban_duration_sec_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "banDurationSecInput"))

    @builtins.property
    @jsii.member(jsii_name="banThresholdInput")
    def ban_threshold_input(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold], jsii.get(self, "banThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="conformActionInput")
    def conform_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conformActionInput"))

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyConfigsInput")
    def enforce_on_key_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]]], jsii.get(self, "enforceOnKeyConfigsInput"))

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
    @jsii.member(jsii_name="rateLimitThresholdInput")
    def rate_limit_threshold_input(
        self,
    ) -> typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold"]:
        return typing.cast(typing.Optional["ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold"], jsii.get(self, "rateLimitThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="banDurationSec")
    def ban_duration_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "banDurationSec"))

    @ban_duration_sec.setter
    def ban_duration_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b96f5b1d7ac4d888c7d9c0373858e309a099abdbd24b6f24d5bde09735e775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "banDurationSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="conformAction")
    def conform_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conformAction"))

    @conform_action.setter
    def conform_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1af8a0f1880d79e45ed27356539de759bb201cb6e73ce65b1d8f3f99b68b340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conformAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKey")
    def enforce_on_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKey"))

    @enforce_on_key.setter
    def enforce_on_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__628fff6ec2378f38cb1eee8115d07e81354a08179f40c4d60206d9cf63befb97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enforceOnKeyName")
    def enforce_on_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceOnKeyName"))

    @enforce_on_key_name.setter
    def enforce_on_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10ccfdef40fca2a26b9ce5468952f4719749c645a0be0e37d4a6eb5b9a432f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enforceOnKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exceedAction")
    def exceed_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exceedAction"))

    @exceed_action.setter
    def exceed_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0252bb6399f499d3bc18c59df1ba9ab44af76a2cebf3cccc9c98d7471b3ecc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exceedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptions]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2b7efeebee0347a79f8a3430513c03761d90feb41b561a5c1be14e18307db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold",
    jsii_struct_bases=[],
    name_mapping={"count": "count", "interval_sec": "intervalSec"},
)
class ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        interval_sec: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: Number of HTTP(S) requests for calculating the threshold. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#count ComputeRegionSecurityPolicy#count}
        :param interval_sec: Interval over which the threshold is computed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#interval_sec ComputeRegionSecurityPolicy#interval_sec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da43e14cc256865a032a122180e34720ceaa78e80c7722668dc8953541f39749)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument interval_sec", value=interval_sec, expected_type=type_hints["interval_sec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if interval_sec is not None:
            self._values["interval_sec"] = interval_sec

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''Number of HTTP(S) requests for calculating the threshold.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#count ComputeRegionSecurityPolicy#count}
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_sec(self) -> typing.Optional[jsii.Number]:
        '''Interval over which the threshold is computed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#interval_sec ComputeRegionSecurityPolicy#interval_sec}
        '''
        result = self._values.get("interval_sec")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThresholdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThresholdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a7d281375cacf3ed1682aabe619e7991bddcb113460f4d219a9fbbc2e0d7bbf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCount")
    def reset_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCount", []))

    @jsii.member(jsii_name="resetIntervalSec")
    def reset_interval_sec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntervalSec", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__abae33e27ad48bdaa8afe8f403916ee822f00cccb5d73a60dcecbc4ad05039da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intervalSec")
    def interval_sec(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "intervalSec"))

    @interval_sec.setter
    def interval_sec(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2885743361feda5808f74340ca345a771ff66632e099dfeb1df5bc51d93f0d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intervalSec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold]:
        return typing.cast(typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608f86d4e9fdf2bbbb04e019a6d08158a33ff07bc68df6ebd484386a03ef8a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRegionSecurityPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#create ComputeRegionSecurityPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#delete ComputeRegionSecurityPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#update ComputeRegionSecurityPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463ce504ad58545609e4650abc735eddfc7658d02ce825ac10a23997e58ab92a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#create ComputeRegionSecurityPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#delete ComputeRegionSecurityPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#update ComputeRegionSecurityPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86e7ba37b34bea1b98bf7ea61d0031552421876b447dbda9f057b8ed9e9ad4a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84ee95626d7ac7cf113bc16afecd95f4ad0fdc52e24357078bd181d5fe55d378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7636efaec162f5d336bb9903ff4b069249c0fc528933d66d8f64e66a138d1dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f91b459b5e335ac1636823767d3322611f8d3fb14ef14150c125e2795b8eb3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c52fb396792d99ffa196ade4885a78679c3bcaa65cfda6c33c6861a21843bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyUserDefinedFields",
    jsii_struct_bases=[],
    name_mapping={
        "base": "base",
        "mask": "mask",
        "name": "name",
        "offset": "offset",
        "size": "size",
    },
)
class ComputeRegionSecurityPolicyUserDefinedFields:
    def __init__(
        self,
        *,
        base: builtins.str,
        mask: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        offset: typing.Optional[jsii.Number] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param base: The base relative to which 'offset' is measured. Possible values are: - IPV4: Points to the beginning of the IPv4 header. - IPV6: Points to the beginning of the IPv6 header. - TCP: Points to the beginning of the TCP header, skipping over any IPv4 options or IPv6 extension headers. Not present for non-first fragments. - UDP: Points to the beginning of the UDP header, skipping over any IPv4 options or IPv6 extension headers. Not present for non-first fragments. Possible values: ["IPV4", "IPV6", "TCP", "UDP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#base ComputeRegionSecurityPolicy#base}
        :param mask: If specified, apply this mask (bitwise AND) to the field to ignore bits before matching. Encoded as a hexadecimal number (starting with "0x"). The last byte of the field (in network byte order) corresponds to the least significant byte of the mask. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#mask ComputeRegionSecurityPolicy#mask}
        :param name: The name of this field. Must be unique within the policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#name ComputeRegionSecurityPolicy#name}
        :param offset: Offset of the first byte of the field (in network byte order) relative to 'base'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#offset ComputeRegionSecurityPolicy#offset}
        :param size: Size of the field in bytes. Valid values: 1-4. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#size ComputeRegionSecurityPolicy#size}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f72ef4350f915cea8152371e598af9682d15acd5733f2553507f618f715c16)
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
            check_type(argname="argument mask", value=mask, expected_type=type_hints["mask"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base": base,
        }
        if mask is not None:
            self._values["mask"] = mask
        if name is not None:
            self._values["name"] = name
        if offset is not None:
            self._values["offset"] = offset
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def base(self) -> builtins.str:
        '''The base relative to which 'offset' is measured.

        Possible values are:

        - IPV4: Points to the beginning of the IPv4 header.
        - IPV6: Points to the beginning of the IPv6 header.
        - TCP: Points to the beginning of the TCP header, skipping over any IPv4 options or IPv6 extension headers. Not present for non-first fragments.
        - UDP: Points to the beginning of the UDP header, skipping over any IPv4 options or IPv6 extension headers. Not present for non-first fragments. Possible values: ["IPV4", "IPV6", "TCP", "UDP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#base ComputeRegionSecurityPolicy#base}
        '''
        result = self._values.get("base")
        assert result is not None, "Required property 'base' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mask(self) -> typing.Optional[builtins.str]:
        '''If specified, apply this mask (bitwise AND) to the field to ignore bits before matching.

        Encoded as a hexadecimal number (starting with "0x").
        The last byte of the field (in network byte order) corresponds to the least significant byte of the mask.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#mask ComputeRegionSecurityPolicy#mask}
        '''
        result = self._values.get("mask")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this field. Must be unique within the policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#name ComputeRegionSecurityPolicy#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def offset(self) -> typing.Optional[jsii.Number]:
        '''Offset of the first byte of the field (in network byte order) relative to 'base'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#offset ComputeRegionSecurityPolicy#offset}
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''Size of the field in bytes. Valid values: 1-4.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_region_security_policy#size ComputeRegionSecurityPolicy#size}
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRegionSecurityPolicyUserDefinedFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRegionSecurityPolicyUserDefinedFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyUserDefinedFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0493159749a2505bb278d35e4bdbdc19a3298b925e9b772da5e43ffda608f9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRegionSecurityPolicyUserDefinedFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf8ec9d91e0e19df740068b0411b97cbbc46f523c676f4701ca10ce96e7a485)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRegionSecurityPolicyUserDefinedFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c490223e10d1e9944ae2f327d74c903de3f93bade206e7255b18fd460d6245fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bb6a1df0a1b38a55bc86accce9cd6fdb3d826de02d3b145e4f072a2e1c83677)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3755637a663d35bd4667b99720e23b6c38f23d163ab91aab98b37fc2d88368ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyUserDefinedFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyUserDefinedFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyUserDefinedFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271e8c9f661957fd53b9820b9452ecdf86f99dbfa58882fd4fa8a55518dbbff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRegionSecurityPolicyUserDefinedFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRegionSecurityPolicy.ComputeRegionSecurityPolicyUserDefinedFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a013c1282046f331cf1d8c6216191ec0864a9b8b6ca205f12f99cd333a492b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMask")
    def reset_mask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMask", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOffset")
    def reset_offset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOffset", []))

    @jsii.member(jsii_name="resetSize")
    def reset_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSize", []))

    @builtins.property
    @jsii.member(jsii_name="baseInput")
    def base_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseInput"))

    @builtins.property
    @jsii.member(jsii_name="maskInput")
    def mask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maskInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="offsetInput")
    def offset_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "offsetInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="base")
    def base(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "base"))

    @base.setter
    def base(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b41cc0913f37d2f2a37247af99bd9a9d51e75142dd4d6ebdd846acaa7f5232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "base", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mask")
    def mask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mask"))

    @mask.setter
    def mask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285c4678ea6b96f4ec8fa26f6ed4a80f5dc18c9624b8bcf8b242b84853b9aa01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mask", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f993fd5d90e55ba60714a18dcbfc81e7ee927e9db5e181af7ea1084a9f91c994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offset")
    def offset(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "offset"))

    @offset.setter
    def offset(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b224b13414ad5d1fdddb98ba9f32513be2e44d46971945f6af8a718dd07cc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offset", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7991709d411c79ba48fe1ccedd8c4cce10512a51b48b7da74589579240e59685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyUserDefinedFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyUserDefinedFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyUserDefinedFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2097f8f20652988b48f525b3ba44a917711b9fcfe960401a37fb6790b55fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRegionSecurityPolicy",
    "ComputeRegionSecurityPolicyConfig",
    "ComputeRegionSecurityPolicyDdosProtectionConfig",
    "ComputeRegionSecurityPolicyDdosProtectionConfigOutputReference",
    "ComputeRegionSecurityPolicyRules",
    "ComputeRegionSecurityPolicyRulesList",
    "ComputeRegionSecurityPolicyRulesMatch",
    "ComputeRegionSecurityPolicyRulesMatchConfig",
    "ComputeRegionSecurityPolicyRulesMatchConfigOutputReference",
    "ComputeRegionSecurityPolicyRulesMatchExpr",
    "ComputeRegionSecurityPolicyRulesMatchExprOutputReference",
    "ComputeRegionSecurityPolicyRulesMatchOutputReference",
    "ComputeRegionSecurityPolicyRulesNetworkMatch",
    "ComputeRegionSecurityPolicyRulesNetworkMatchOutputReference",
    "ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields",
    "ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsList",
    "ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFieldsOutputReference",
    "ComputeRegionSecurityPolicyRulesOutputReference",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionList",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionOutputReference",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieList",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookieOutputReference",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderList",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeaderOutputReference",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamList",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParamOutputReference",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriList",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUriOutputReference",
    "ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigOutputReference",
    "ComputeRegionSecurityPolicyRulesRateLimitOptions",
    "ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold",
    "ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThresholdOutputReference",
    "ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs",
    "ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsList",
    "ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigsOutputReference",
    "ComputeRegionSecurityPolicyRulesRateLimitOptionsOutputReference",
    "ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold",
    "ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThresholdOutputReference",
    "ComputeRegionSecurityPolicyTimeouts",
    "ComputeRegionSecurityPolicyTimeoutsOutputReference",
    "ComputeRegionSecurityPolicyUserDefinedFields",
    "ComputeRegionSecurityPolicyUserDefinedFieldsList",
    "ComputeRegionSecurityPolicyUserDefinedFieldsOutputReference",
]

publication.publish()

def _typecheckingstub__ae7f81edc6e4b37b62fba52cf6cfbe3eacd60bd2fd3e63b4410a0d6d72f6de63(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    ddos_protection_config: typing.Optional[typing.Union[ComputeRegionSecurityPolicyDdosProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionSecurityPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__0718af724d77f1a7a31d3f1355989c79a682ef3f67cbbf0f1e85cc1f03a271a0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a249e65fd5e75e23187dfc65e7dd6a4fb69b9cfed16e9a7c8dcaeeb69f14a7c0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b8bd3a9e394cf41045a813dec5441db1190e84825156edeed511bd00f08613(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d609edbe46167304d21117df0e8687587f2cad9e1714c280b98aebab6120f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4316574cf65f690e9c4b9ad72cabc01c0aad7eca81d4b1abdde54ba486aa4677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fb4689415e6b5bd303298bffa3002f28dca4a65feec08a6f3ebf1603244711(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ed9d4b1bf67ed903956c8ef8db3b6c6d9b208fd12c924e7a41cb59db23226f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223f097badcfb2259616c5d0cff78971c076e673f8f4c152ab99bc603520fe6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f041ddb2fe9360f37de0614f77afb6c1197d3c1c842e54248aaf77f0c73e0aba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4d20bb990c37dcd315406420eaf0e28bf8909f686e9e809da1a188c6bb2729(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    ddos_protection_config: typing.Optional[typing.Union[ComputeRegionSecurityPolicyDdosProtectionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[ComputeRegionSecurityPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
    user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f653bca987192e8be63b9bc18aa1a6c187fc08fa4e89ba23e05ce228c9ecd8c(
    *,
    ddos_protection: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a2efa3c13b3c9ae848685975dbf54052b6b68e33f2062c6e4c2e9c93e4527f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7cd01a816bbf8d98f5c14b28223a625953a561bb8ad344dbe35870dedf1ce4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab6992c517bd7c4fa52b722581f7da6a6a950c844f673a8e747b479a1eedee0(
    value: typing.Optional[ComputeRegionSecurityPolicyDdosProtectionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cefa813c968e44384908a8333bcb74172b63db28344fd73523435df7d2d0214(
    *,
    action: builtins.str,
    priority: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    match: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    network_match: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesNetworkMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    preconfigured_waf_config: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    preview: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rate_limit_options: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesRateLimitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a873a88162d10458fe4fef4dff48c024e9518d57a2f5687de5f2cec36f886e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3eb34087422edda0ca0e9cdece8074ba7d00eb0db88eb691d94f03db8f9c26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f93308b70db4b327f95d35639313bc7bb4d04e9635b9361fa462032aa3e7d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9432aac519228371db2286ad97720a583a986f3e73989d1833bceca8347864f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f1a6c9e725cdda479484c57e6aa62ebdb9c8acb438f5bfb13933086949ce10(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5374edefbf8f7936fbf41b881c7524bcf55260673e868d9ff88f75c3f97bc7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5eb8d17f901130f23ad88c4ad55439b8bdd1995a19d590686955226f87d3f7b(
    *,
    config: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesMatchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    expr: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesMatchExpr, typing.Dict[builtins.str, typing.Any]]] = None,
    versioned_expr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0002711b34841f41c67d4184e3112940413cfe6759d974ec206fc14361e2d367(
    *,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966d79c220cc2bccbe3a72e45af4cabd6b1bd088669474fc39dc2962ea1ed0a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2037997dc661317d1c9b3a61f5044c519f4b2a93fe50f4fdc4bcb443b713e33f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2570b33fa52cbe6fcf3ed36844870495c03bd00d50e77970f6cc4bee238f554c(
    value: typing.Optional[ComputeRegionSecurityPolicyRulesMatchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463f52431c1632354a966a3b26af9397e16600d85abcd22bdd628cd682a33222(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9c602327cbf510cd4d11e31e26f2c32955bab5c60d578266926e94c5052341(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3fb913311727bca3f0cae7471f25c399b302e939e0c1f8cfd5663a497ff344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289783a9c7c308fab4656e5cca711f25f212733775b8ef66d07fde7b7d2c0d07(
    value: typing.Optional[ComputeRegionSecurityPolicyRulesMatchExpr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc270d18fab8844e0cf0b1f21b85a4e5577f2432f426ac8559748cc9136b75b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e04ccda5e92f5b5a41a2052b8f16a6b3a01b77d60b2784336a197669578ab52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4569d99fb3223dcbd803c23c6363f79d835120f245d032e7d1d03b60e7f65a46(
    value: typing.Optional[ComputeRegionSecurityPolicyRulesMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6425e3247d3a064408daaf18c053fafeb50b15379311728214cc788420f968b3(
    *,
    dest_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    dest_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_asns: typing.Optional[typing.Sequence[jsii.Number]] = None,
    src_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    src_region_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_defined_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ffd5cc5484019ca940dfe6bdd308eb3e51b849f6a54e3aa4d6027f81c54967(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395b428988231f3446e50582fb2fdd944647d8f8c4ed5035ed68b183bf647996(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a6bce1a545021fe32a187f1ff01df05ca8b7244cdbf5d47895c9f320b9cae3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d321561b722ca6b8b022195a964687453ded0761d3824577e97d5cf17db7107(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0d07dcf550ec9b5d2303690f3cbe005506d2facb991b27637e2e08846bcdc9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5610ca5263332a2e2653acc988ed9bba222abe97ed6c2c7d0bd583b25616dc8b(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ab30966b20412f3e66f403ec5cb9eb7bf4bc2f192dfc3cf200201fc6216b53(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466b490f2b1938dffe1ee54092aad4d18d5f6f85d62434b815fdba1495cfeb2b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3d450bdcd2ccd84dcac887e482d1f0baf85159edb16ee56d83d2b3a1cb018b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9182ac57633390174c0bf595e5118621f73a9c88d976f7088c4a6004ba7a47(
    value: typing.Optional[ComputeRegionSecurityPolicyRulesNetworkMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0b25fe0a3d85060aeb6c2eb9756b0eefb0b8a0cff063d3da5148635d13c5ad(
    *,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d84b5a33be52ea607ebe08a3d834acb77a837a3e11dca0bdf50b33ce4ef013(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24260af5f6fcc155735ac514fa95293b0b88d2ffd93ff4c03853ab262e976983(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31da08a23d6c082ef27cfb504d72609892fc5945c495c9089717fe2fe8bd317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9d8a199481895e7c78c780edd439dffd6eeabe204d21e2ab3b39e7b1ef3e5b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f515c652493af9c52cc530ea1097261c815f54ddf62a0726326ace10eaa006(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0cc99d96cfbb824bc20fd56a44721ba135fa931a80673ce04a177bd935b6a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6682f3104e30d033f0f1b3ad7a60d147ccd6c0d48dcb5eccf357d539db197fce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436e531e72e5c5a9b20f43a5308c00691dca16f5c34f3e9206bbed0bb64790ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199083b30283568e3f6ade96480a9ab4bdf7a307dc111680e437f393548baa4d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f534077fd39fede33d182186f794276d363a346d73353971ba5b3c55453bfe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesNetworkMatchUserDefinedFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cd60e991a568c70ae683f0a1b87dfa687e97e6e51cffeed5c6d26070e24cf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9038f8185830b8939df63cb2cf31e9c066697da92d95cb340996103d3a7496c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15de9c5d44a2f781114e4ce2ad3d7328ea915743744b804d9cdeb7cfd7eeaf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5564163349d33804e5cfe018c8214abb305d0da361bb165a3d6734ef77bb7429(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48a183385eab0c06d8914a380f9653eb4d8f743d5ec681b167c2c69f8feada4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcca5639dc9d404045e7b98359a85fe82baabff2349f908eabe4f59001e0a276(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c4ba74c99bd9777d28f383a7c820acfb284e0f2bb092ee41c45e4aaee31b1f(
    *,
    exclusion: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5abfbe58f769d17d3c9cbfd713110adf36fecb1b9980d3b01b642df47a55d35(
    *,
    target_rule_set: builtins.str,
    request_cookie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_query_param: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam, typing.Dict[builtins.str, typing.Any]]]]] = None,
    request_uri: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_rule_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ac7b1716fdd333618434850d35f33aedf0300b2399e612436ab6357d633a8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfd37f42a6072a45f4d12ce274a74adba70d7b3b8659af07d4a7f39b11319c0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62603d9fa708a51fbaf426d4528ca8b4c6ca45d26263d3abbfac63f7c239e2fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003a50f2f223fe47825da2e30687a0b193f8590d79139c3285a2357a673d7e32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e90086f9cc607760c04d4daaf441a6e1fd110e2f87b1160c607a9893cc739e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345b14b3c2791f1e527b760f606e22d30e99928c42ad69c6a082c2c5def6c9cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a07a6ef02bdb2de5185895b48dc1f8f943948129aa57852762c11c4cba52f09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146c8152ef37801fb030c53b49d009588a0d409f201b51b6018fc4a15f5c800f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ad8fddedb8cf9103b64d4ebb4e3abc42965601acc8856d93f69737f44440cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd627c7c73343099bf0f7199b7d6b015b77a642b6bda8d61c285c09eda833c9b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a707780ec7f1fe5494c2964b959c066554572dc21b57cf4d1e6b2864f3ec916f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d9cbc10fa2e4e10dc244c45e5fa5f38ee50c8820d5a5660a1388c22d651b21(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7356957aa3cd135aeda0f9e5961131c4dde8460e73ab89cd30fd816909642ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a192ffeeae44313a989b4eae2350178b6d97aa699949bc7fcc5247b5f47198(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586e116284bc84a244405be34f4ec6a5dc6918dcbc925742f36e020297093fe5(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a7a8c9570a1a331a7b57cd9fccf5ff9e7e7e50689c7101e055705c81b63d13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ab91f339fcc11722ccdfcbeaacfe17974e39db6d579b4883de46b9c63d3811(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430f739bf74a67d2118c44da4b08091dd367e6fd51de02cb42a68c52e6ff5a87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d4adb8b988fb6bea48000bb15111f5419bed5fad9f348b75c9ed1e93de0fb5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0db6b2d7a30c4a91be5c4713b05c1ac89afff04182a538bcdce43b37a2cb80(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a229b741b8c83817e100c07afec28c5fbf81c9b1d52f197ca1c8128c2508a97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35eab3e5805557bdaaf619847f3bbb72abba0c9c02141dea5f70616a5f89abaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f008ccefe0aae500e0aeb0cff66bdd589245b952d2ca973e27bcb3fa772cbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046d5722f0fb1f676bb90ccacfe01f4301b95644da62831b622efa91e8a9d3fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd793b1a70828e9ab8aa2863da6069a425b1f887a30f875d05621dcb7905df6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestCookie]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f87d43c581f1e9b6ffdb4de90389151430beff8ec4307ca8de134e92f67d0d(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835b1a453fe56dbc945152caff52d868960474f6bc97a83d2667dfc29efbe3f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7b35c90b57756f1bb02c69e952d8c0199c329cfa2f97fcef76668f9db04e9c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec9d3a2c679c471bcb14396287da86a7db9f9e4e0fb2601f57cf59e6d8292cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4104c70c6c6aa10ae0544dacd543993a25689178843dc5a4b060e3a6ea447e87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2999451649117072cb40069a8442d6754df4a6a2850b1fc4f2ca42eb025d79d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e015c5cdebb54f5d774da35a4165515a6394dce0aba29e5cded283adacd31ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43a17757b985c8f0be027fd2f6d352ebfb6408d405562b752c6de306b920618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02fc442b138a8b2cfa3f28b8fd1c7f8215b071a02320976cb29a4ac851a01c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928e1ab01d9186dd8b3ac85a5bd4994c4c67570ce552d8b9ff95acc028e623ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3db31177fbebc2332b31349de7a64caf4d3f4a160ffdb9ae652db3fdc4f1d5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3577ce5af3fbcb4bef21065668b151380645697e64612fc9e2c5a2a21da98a(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51cce2df031deecc0369dfe7e8304a1986084d099951524efdedcfee3beeb15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa50a06423f675b00c308b945f24d52626d72301617eb91a44bea5e01d764e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c125f0fcc5d515fee752c43ba1a0251e2131fbc1b6b90ac5de89ef3b659051ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bae0b9f9e6474be689504d440231e1822960244d74fedbd2824a2be174d00f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177121df2ca4b69cba78a424e7a891a06e6eadef78718949ea6a7a48d0a8bc56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5127be06835d8dbad722f70b9f738b9e7a95c5ab4f06c50f06ffdba01f44ac61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402c732773dbd646b173432f5e18eddcb6eab7347deb6996fea7a476faae6149(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4765cd37d38711bf47a051338155a434f7ac10bba6dbd837d8461dd6bfaba6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ef2fb3b9b9ebdf67b316946abc7517905aa82bff1251cab87574d21331d296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0655c2cac7af39fafd63fef177db77fa4621f64d0fce74bd5b3a1ed331bf9363(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestQueryParam]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241543090feffd50c2a541866523ca8de43d9526f4bc4313b5c079c2baa5cdd4(
    *,
    operator: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d38b8c47606e45b49f516bb1aba41a78555faa32554b33027523f90e115a677(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0b6ed3c088bd05424c1b0ad61a9d28d8c1b089ca31af2bc5155db0dbb65020a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea1ed772121be127fa8c6c82a314191b7214d036ab8f8ca7be52267d416be65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1864cc5a77770c117113f84521bdfa9740c36a49b1a47150f3d3d5275e4df8ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f3ed0575d142d219e2eadaa1088f6101d25d21f4ed8f03a21362c685d500b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687fbefdb899aa54ea578f2ceacce22712f77bd2627287c0d835abbc38d462ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec1ab10f401bbb183e3aa5a59ab2459e1c2afbd1d74d20ae7a837417eda7ad2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e22f63812eb9e32b82a79c0813bc39144f164ce485b38c17026b73a7a8f0655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20848e7535ee9b64a04bee963388203c76e74aa3fbddac1de7a4efba37d3a263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15392ca460bc6c1a2109e2333720eb41b4d348853fca685a7c1e264c20e6c44b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusionRequestUri]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7e3f41ec22aa58c609e0110b5f96cca421598f216733fa48316557681eb70b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e4d2b06a15eb5bda4fd8f3585cfd80248bc53b9b7e8df8148b92a5be46f5d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfigExclusion, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bbe33ae39b57b802a7f1bb2a2423432ab3dbcf11275a12aa4bc5b52f85bfd2(
    value: typing.Optional[ComputeRegionSecurityPolicyRulesPreconfiguredWafConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bac360ee9672fe20eefb07afbaadbd1ae0c67bf20f636fe65cc37bcf10a19969(
    *,
    ban_duration_sec: typing.Optional[jsii.Number] = None,
    ban_threshold: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
    conform_action: typing.Optional[builtins.str] = None,
    enforce_on_key: typing.Optional[builtins.str] = None,
    enforce_on_key_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    exceed_action: typing.Optional[builtins.str] = None,
    rate_limit_threshold: typing.Optional[typing.Union[ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca286cb8f965f239979801294f640b230f973f8790b186b8248b7b8adf78837(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e015c07d00828f705abe35ce649ad0c2ca770e1a423d1799075fb7508fa7f705(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21f09cd9dc6ab08dbc5d28cc804e3c108c2acb2b170cc23da6f64be851c5d44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390507953484de658b0a3e535e6a5f0dc95ec319a57bb093a36ddd5efbf26412(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5cad28c967d6c17ad321cfdeed5b146b85760573d2fc9c9cda1cc93adfad30(
    value: typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsBanThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ae5914f6a3c772559eea42f9f56182691d5e727120fbacc9fc93564a1d8a72(
    *,
    enforce_on_key_name: typing.Optional[builtins.str] = None,
    enforce_on_key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa22f0bb278af9558fd209e8214e0cbdb15d40885956b0433aff57ed61dcc9b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000640fe73dd3f7f21c50edf042292ae9eebdb79212aa3413b17997a1a050cb8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f352c773cd7177a19a6091cb0b1a6bf7794de2e41e51a81339c18a6b16f7e548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780852e3141052a2a33a4789037081713f79e3d3a0b8dde8d4c591b651c79eb8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8908a8ac625dfaed9244afd038d66a8ed6c947074dceb86548d6fb7f90ed67cb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69962c04b51be45f68cf82d890d6cf3c13dfd3b710a03e09fb1016f7aa67c10d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95551714447d7a993165a208f0b1b9a05c40af42efd2e0576a9e55eb1eb436cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b39c6706579b53f64f9963fbae7ed1db90e3d4d06adc011ed78c67a513c251f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3c5aa25685e843863b8a0b3cff9c8adc3106569cc281534a32a333cf13535b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ceef096c8f3a694292fc7d4c9050845c9cee05c8efc7a99932404b5502e8627(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9a3411ad0f319ae582ad65010b847d26c32b3d5a2bed51295ed1d0ebdb292b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf06e700c34e6eb1663e887274243e67318398dcea1fd3421ce4c48458ddddad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRegionSecurityPolicyRulesRateLimitOptionsEnforceOnKeyConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b96f5b1d7ac4d888c7d9c0373858e309a099abdbd24b6f24d5bde09735e775(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1af8a0f1880d79e45ed27356539de759bb201cb6e73ce65b1d8f3f99b68b340(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__628fff6ec2378f38cb1eee8115d07e81354a08179f40c4d60206d9cf63befb97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10ccfdef40fca2a26b9ce5468952f4719749c645a0be0e37d4a6eb5b9a432f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0252bb6399f499d3bc18c59df1ba9ab44af76a2cebf3cccc9c98d7471b3ecc47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2b7efeebee0347a79f8a3430513c03761d90feb41b561a5c1be14e18307db3(
    value: typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da43e14cc256865a032a122180e34720ceaa78e80c7722668dc8953541f39749(
    *,
    count: typing.Optional[jsii.Number] = None,
    interval_sec: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7d281375cacf3ed1682aabe619e7991bddcb113460f4d219a9fbbc2e0d7bbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abae33e27ad48bdaa8afe8f403916ee822f00cccb5d73a60dcecbc4ad05039da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2885743361feda5808f74340ca345a771ff66632e099dfeb1df5bc51d93f0d5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608f86d4e9fdf2bbbb04e019a6d08158a33ff07bc68df6ebd484386a03ef8a33(
    value: typing.Optional[ComputeRegionSecurityPolicyRulesRateLimitOptionsRateLimitThreshold],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463ce504ad58545609e4650abc735eddfc7658d02ce825ac10a23997e58ab92a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e7ba37b34bea1b98bf7ea61d0031552421876b447dbda9f057b8ed9e9ad4a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ee95626d7ac7cf113bc16afecd95f4ad0fdc52e24357078bd181d5fe55d378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7636efaec162f5d336bb9903ff4b069249c0fc528933d66d8f64e66a138d1dd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f91b459b5e335ac1636823767d3322611f8d3fb14ef14150c125e2795b8eb3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c52fb396792d99ffa196ade4885a78679c3bcaa65cfda6c33c6861a21843bf8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f72ef4350f915cea8152371e598af9682d15acd5733f2553507f618f715c16(
    *,
    base: builtins.str,
    mask: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    offset: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0493159749a2505bb278d35e4bdbdc19a3298b925e9b772da5e43ffda608f9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf8ec9d91e0e19df740068b0411b97cbbc46f523c676f4701ca10ce96e7a485(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c490223e10d1e9944ae2f327d74c903de3f93bade206e7255b18fd460d6245fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb6a1df0a1b38a55bc86accce9cd6fdb3d826de02d3b145e4f072a2e1c83677(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3755637a663d35bd4667b99720e23b6c38f23d163ab91aab98b37fc2d88368ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271e8c9f661957fd53b9820b9452ecdf86f99dbfa58882fd4fa8a55518dbbff9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRegionSecurityPolicyUserDefinedFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a013c1282046f331cf1d8c6216191ec0864a9b8b6ca205f12f99cd333a492b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b41cc0913f37d2f2a37247af99bd9a9d51e75142dd4d6ebdd846acaa7f5232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285c4678ea6b96f4ec8fa26f6ed4a80f5dc18c9624b8bcf8b242b84853b9aa01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f993fd5d90e55ba60714a18dcbfc81e7ee927e9db5e181af7ea1084a9f91c994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b224b13414ad5d1fdddb98ba9f32513be2e44d46971945f6af8a718dd07cc86(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7991709d411c79ba48fe1ccedd8c4cce10512a51b48b7da74589579240e59685(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2097f8f20652988b48f525b3ba44a917711b9fcfe960401a37fb6790b55fe6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRegionSecurityPolicyUserDefinedFields]],
) -> None:
    """Type checking stubs"""
    pass
