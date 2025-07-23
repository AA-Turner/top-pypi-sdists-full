r'''
# `google_privateca_certificate_template`

Refer to the Terraform Registry for docs: [`google_privateca_certificate_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template).
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


class PrivatecaCertificateTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template google_privateca_certificate_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity_constraints: typing.Optional[typing.Union["PrivatecaCertificateTemplateIdentityConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maximum_lifetime: typing.Optional[builtins.str] = None,
        passthrough_extensions: typing.Optional[typing.Union["PrivatecaCertificateTemplatePassthroughExtensions", typing.Dict[builtins.str, typing.Any]]] = None,
        predefined_values: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValues", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["PrivatecaCertificateTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template google_privateca_certificate_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#location PrivatecaCertificateTemplate#location}
        :param name: The resource name for this CertificateTemplate in the format 'projects/* /locations/* /certificateTemplates/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#name PrivatecaCertificateTemplate#name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param description: Optional. A human-readable description of scenarios this template is intended for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#description PrivatecaCertificateTemplate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#id PrivatecaCertificateTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_constraints: identity_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#identity_constraints PrivatecaCertificateTemplate#identity_constraints}
        :param labels: Optional. Labels with user-defined metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#labels PrivatecaCertificateTemplate#labels}
        :param maximum_lifetime: Optional. The maximum lifetime allowed for all issued certificates that use this template. If the issuing CaPool's IssuancePolicy specifies a maximum lifetime the minimum of the two durations will be the maximum lifetime for issued. Note that if the issuing CertificateAuthority expires before a Certificate's requested maximum_lifetime, the effective lifetime will be explicitly truncated to match it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#maximum_lifetime PrivatecaCertificateTemplate#maximum_lifetime}
        :param passthrough_extensions: passthrough_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#passthrough_extensions PrivatecaCertificateTemplate#passthrough_extensions}
        :param predefined_values: predefined_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#predefined_values PrivatecaCertificateTemplate#predefined_values}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#project PrivatecaCertificateTemplate#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#timeouts PrivatecaCertificateTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caafb7ad7113e498f1d8707e68f61ccc79b80631e245b780ffba7f630d7960dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PrivatecaCertificateTemplateConfig(
            location=location,
            name=name,
            description=description,
            id=id,
            identity_constraints=identity_constraints,
            labels=labels,
            maximum_lifetime=maximum_lifetime,
            passthrough_extensions=passthrough_extensions,
            predefined_values=predefined_values,
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
        '''Generates CDKTF code for importing a PrivatecaCertificateTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PrivatecaCertificateTemplate to import.
        :param import_from_id: The id of the existing PrivatecaCertificateTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PrivatecaCertificateTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c3418c7bbb197a7fcbd0bfe8fb4b869b2fe1bc943ed69301cd199f11cf357c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentityConstraints")
    def put_identity_constraints(
        self,
        *,
        allow_subject_alt_names_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        allow_subject_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cel_expression: typing.Optional[typing.Union["PrivatecaCertificateTemplateIdentityConstraintsCelExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_subject_alt_names_passthrough: Required. If this is true, the SubjectAltNames extension may be copied from a certificate request into the signed certificate. Otherwise, the requested SubjectAltNames will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#allow_subject_alt_names_passthrough PrivatecaCertificateTemplate#allow_subject_alt_names_passthrough}
        :param allow_subject_passthrough: Required. If this is true, the Subject field may be copied from a certificate request into the signed certificate. Otherwise, the requested Subject will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#allow_subject_passthrough PrivatecaCertificateTemplate#allow_subject_passthrough}
        :param cel_expression: cel_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#cel_expression PrivatecaCertificateTemplate#cel_expression}
        '''
        value = PrivatecaCertificateTemplateIdentityConstraints(
            allow_subject_alt_names_passthrough=allow_subject_alt_names_passthrough,
            allow_subject_passthrough=allow_subject_passthrough,
            cel_expression=cel_expression,
        )

        return typing.cast(None, jsii.invoke(self, "putIdentityConstraints", [value]))

    @jsii.member(jsii_name="putPassthroughExtensions")
    def put_passthrough_extensions(
        self,
        *,
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        known_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#additional_extensions PrivatecaCertificateTemplate#additional_extensions}
        :param known_extensions: Optional. A set of named X.509 extensions. Will be combined with additional_extensions to determine the full set of X.509 extensions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#known_extensions PrivatecaCertificateTemplate#known_extensions}
        '''
        value = PrivatecaCertificateTemplatePassthroughExtensions(
            additional_extensions=additional_extensions,
            known_extensions=known_extensions,
        )

        return typing.cast(None, jsii.invoke(self, "putPassthroughExtensions", [value]))

    @jsii.member(jsii_name="putPredefinedValues")
    def put_predefined_values(
        self,
        *,
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ca_options: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValuesCaOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        key_usage: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValuesKeyUsage", typing.Dict[builtins.str, typing.Any]]] = None,
        name_constraints: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValuesNameConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePredefinedValuesPolicyIds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#additional_extensions PrivatecaCertificateTemplate#additional_extensions}
        :param aia_ocsp_servers: Optional. Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#aia_ocsp_servers PrivatecaCertificateTemplate#aia_ocsp_servers}
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#ca_options PrivatecaCertificateTemplate#ca_options}
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_usage PrivatecaCertificateTemplate#key_usage}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#name_constraints PrivatecaCertificateTemplate#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#policy_ids PrivatecaCertificateTemplate#policy_ids}
        '''
        value = PrivatecaCertificateTemplatePredefinedValues(
            additional_extensions=additional_extensions,
            aia_ocsp_servers=aia_ocsp_servers,
            ca_options=ca_options,
            key_usage=key_usage,
            name_constraints=name_constraints,
            policy_ids=policy_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putPredefinedValues", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#create PrivatecaCertificateTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#delete PrivatecaCertificateTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#update PrivatecaCertificateTemplate#update}.
        '''
        value = PrivatecaCertificateTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentityConstraints")
    def reset_identity_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityConstraints", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaximumLifetime")
    def reset_maximum_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumLifetime", []))

    @jsii.member(jsii_name="resetPassthroughExtensions")
    def reset_passthrough_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassthroughExtensions", []))

    @jsii.member(jsii_name="resetPredefinedValues")
    def reset_predefined_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredefinedValues", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="identityConstraints")
    def identity_constraints(
        self,
    ) -> "PrivatecaCertificateTemplateIdentityConstraintsOutputReference":
        return typing.cast("PrivatecaCertificateTemplateIdentityConstraintsOutputReference", jsii.get(self, "identityConstraints"))

    @builtins.property
    @jsii.member(jsii_name="passthroughExtensions")
    def passthrough_extensions(
        self,
    ) -> "PrivatecaCertificateTemplatePassthroughExtensionsOutputReference":
        return typing.cast("PrivatecaCertificateTemplatePassthroughExtensionsOutputReference", jsii.get(self, "passthroughExtensions"))

    @builtins.property
    @jsii.member(jsii_name="predefinedValues")
    def predefined_values(
        self,
    ) -> "PrivatecaCertificateTemplatePredefinedValuesOutputReference":
        return typing.cast("PrivatecaCertificateTemplatePredefinedValuesOutputReference", jsii.get(self, "predefinedValues"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PrivatecaCertificateTemplateTimeoutsOutputReference":
        return typing.cast("PrivatecaCertificateTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="identityConstraintsInput")
    def identity_constraints_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplateIdentityConstraints"]:
        return typing.cast(typing.Optional["PrivatecaCertificateTemplateIdentityConstraints"], jsii.get(self, "identityConstraintsInput"))

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
    @jsii.member(jsii_name="maximumLifetimeInput")
    def maximum_lifetime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maximumLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passthroughExtensionsInput")
    def passthrough_extensions_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePassthroughExtensions"]:
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePassthroughExtensions"], jsii.get(self, "passthroughExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="predefinedValuesInput")
    def predefined_values_input(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePredefinedValues"]:
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePredefinedValues"], jsii.get(self, "predefinedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivatecaCertificateTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PrivatecaCertificateTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88773560b1d9d364f49a52c6c91015b86af4c936d811074dc0a75a130ac3000b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eabfe4ed6a67b2b0aec1fca3f109bd824ab56737decda7b56808ade1d14d11af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f154086853685004ae59d46d054a9f4edab205c8d9ca86b48e93c1ed4226329b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e907f979f9433cdad222495168762d2be75994b482716da11046111b84ecf554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumLifetime")
    def maximum_lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maximumLifetime"))

    @maximum_lifetime.setter
    def maximum_lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08cba57826a7d05fc53245ebe0100c3ef248a010ebc89270cd574c342b154beb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumLifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc2120af37c679785bd3abf69784e6fad74759e4dbf40d55b49b26a6cfdf812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7193e3f9a46bd0490ec6b305c0a30bceb884556a698af1405f042c048cd520ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "description": "description",
        "id": "id",
        "identity_constraints": "identityConstraints",
        "labels": "labels",
        "maximum_lifetime": "maximumLifetime",
        "passthrough_extensions": "passthroughExtensions",
        "predefined_values": "predefinedValues",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class PrivatecaCertificateTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        identity_constraints: typing.Optional[typing.Union["PrivatecaCertificateTemplateIdentityConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        maximum_lifetime: typing.Optional[builtins.str] = None,
        passthrough_extensions: typing.Optional[typing.Union["PrivatecaCertificateTemplatePassthroughExtensions", typing.Dict[builtins.str, typing.Any]]] = None,
        predefined_values: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValues", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["PrivatecaCertificateTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#location PrivatecaCertificateTemplate#location}
        :param name: The resource name for this CertificateTemplate in the format 'projects/* /locations/* /certificateTemplates/*'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#name PrivatecaCertificateTemplate#name} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param description: Optional. A human-readable description of scenarios this template is intended for. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#description PrivatecaCertificateTemplate#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#id PrivatecaCertificateTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity_constraints: identity_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#identity_constraints PrivatecaCertificateTemplate#identity_constraints}
        :param labels: Optional. Labels with user-defined metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#labels PrivatecaCertificateTemplate#labels}
        :param maximum_lifetime: Optional. The maximum lifetime allowed for all issued certificates that use this template. If the issuing CaPool's IssuancePolicy specifies a maximum lifetime the minimum of the two durations will be the maximum lifetime for issued. Note that if the issuing CertificateAuthority expires before a Certificate's requested maximum_lifetime, the effective lifetime will be explicitly truncated to match it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#maximum_lifetime PrivatecaCertificateTemplate#maximum_lifetime}
        :param passthrough_extensions: passthrough_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#passthrough_extensions PrivatecaCertificateTemplate#passthrough_extensions}
        :param predefined_values: predefined_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#predefined_values PrivatecaCertificateTemplate#predefined_values}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#project PrivatecaCertificateTemplate#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#timeouts PrivatecaCertificateTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity_constraints, dict):
            identity_constraints = PrivatecaCertificateTemplateIdentityConstraints(**identity_constraints)
        if isinstance(passthrough_extensions, dict):
            passthrough_extensions = PrivatecaCertificateTemplatePassthroughExtensions(**passthrough_extensions)
        if isinstance(predefined_values, dict):
            predefined_values = PrivatecaCertificateTemplatePredefinedValues(**predefined_values)
        if isinstance(timeouts, dict):
            timeouts = PrivatecaCertificateTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0b7e773f715961fff8e9d7c8b6f34d2c9a6019b059b0d2bf5211b57e43a4de)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity_constraints", value=identity_constraints, expected_type=type_hints["identity_constraints"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument maximum_lifetime", value=maximum_lifetime, expected_type=type_hints["maximum_lifetime"])
            check_type(argname="argument passthrough_extensions", value=passthrough_extensions, expected_type=type_hints["passthrough_extensions"])
            check_type(argname="argument predefined_values", value=predefined_values, expected_type=type_hints["predefined_values"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if identity_constraints is not None:
            self._values["identity_constraints"] = identity_constraints
        if labels is not None:
            self._values["labels"] = labels
        if maximum_lifetime is not None:
            self._values["maximum_lifetime"] = maximum_lifetime
        if passthrough_extensions is not None:
            self._values["passthrough_extensions"] = passthrough_extensions
        if predefined_values is not None:
            self._values["predefined_values"] = predefined_values
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
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#location PrivatecaCertificateTemplate#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name for this CertificateTemplate in the format 'projects/* /locations/* /certificateTemplates/*'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#name PrivatecaCertificateTemplate#name}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. A human-readable description of scenarios this template is intended for.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#description PrivatecaCertificateTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#id PrivatecaCertificateTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_constraints(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplateIdentityConstraints"]:
        '''identity_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#identity_constraints PrivatecaCertificateTemplate#identity_constraints}
        '''
        result = self._values.get("identity_constraints")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplateIdentityConstraints"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels with user-defined metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#labels PrivatecaCertificateTemplate#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def maximum_lifetime(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The maximum lifetime allowed for all issued certificates that use this template. If the issuing CaPool's IssuancePolicy specifies a maximum lifetime the minimum of the two durations will be the maximum lifetime for issued. Note that if the issuing CertificateAuthority expires before a Certificate's requested maximum_lifetime, the effective lifetime will be explicitly truncated to match it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#maximum_lifetime PrivatecaCertificateTemplate#maximum_lifetime}
        '''
        result = self._values.get("maximum_lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def passthrough_extensions(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePassthroughExtensions"]:
        '''passthrough_extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#passthrough_extensions PrivatecaCertificateTemplate#passthrough_extensions}
        '''
        result = self._values.get("passthrough_extensions")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePassthroughExtensions"], result)

    @builtins.property
    def predefined_values(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePredefinedValues"]:
        '''predefined_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#predefined_values PrivatecaCertificateTemplate#predefined_values}
        '''
        result = self._values.get("predefined_values")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePredefinedValues"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#project PrivatecaCertificateTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PrivatecaCertificateTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#timeouts PrivatecaCertificateTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplateIdentityConstraints",
    jsii_struct_bases=[],
    name_mapping={
        "allow_subject_alt_names_passthrough": "allowSubjectAltNamesPassthrough",
        "allow_subject_passthrough": "allowSubjectPassthrough",
        "cel_expression": "celExpression",
    },
)
class PrivatecaCertificateTemplateIdentityConstraints:
    def __init__(
        self,
        *,
        allow_subject_alt_names_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        allow_subject_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        cel_expression: typing.Optional[typing.Union["PrivatecaCertificateTemplateIdentityConstraintsCelExpression", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_subject_alt_names_passthrough: Required. If this is true, the SubjectAltNames extension may be copied from a certificate request into the signed certificate. Otherwise, the requested SubjectAltNames will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#allow_subject_alt_names_passthrough PrivatecaCertificateTemplate#allow_subject_alt_names_passthrough}
        :param allow_subject_passthrough: Required. If this is true, the Subject field may be copied from a certificate request into the signed certificate. Otherwise, the requested Subject will be discarded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#allow_subject_passthrough PrivatecaCertificateTemplate#allow_subject_passthrough}
        :param cel_expression: cel_expression block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#cel_expression PrivatecaCertificateTemplate#cel_expression}
        '''
        if isinstance(cel_expression, dict):
            cel_expression = PrivatecaCertificateTemplateIdentityConstraintsCelExpression(**cel_expression)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ea12e09f162782b3b919a19a054446ed3e5c89aaaa80bd279ec37198a2c0bf)
            check_type(argname="argument allow_subject_alt_names_passthrough", value=allow_subject_alt_names_passthrough, expected_type=type_hints["allow_subject_alt_names_passthrough"])
            check_type(argname="argument allow_subject_passthrough", value=allow_subject_passthrough, expected_type=type_hints["allow_subject_passthrough"])
            check_type(argname="argument cel_expression", value=cel_expression, expected_type=type_hints["cel_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_subject_alt_names_passthrough": allow_subject_alt_names_passthrough,
            "allow_subject_passthrough": allow_subject_passthrough,
        }
        if cel_expression is not None:
            self._values["cel_expression"] = cel_expression

    @builtins.property
    def allow_subject_alt_names_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Required.

        If this is true, the SubjectAltNames extension may be copied from a certificate request into the signed certificate. Otherwise, the requested SubjectAltNames will be discarded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#allow_subject_alt_names_passthrough PrivatecaCertificateTemplate#allow_subject_alt_names_passthrough}
        '''
        result = self._values.get("allow_subject_alt_names_passthrough")
        assert result is not None, "Required property 'allow_subject_alt_names_passthrough' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def allow_subject_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Required.

        If this is true, the Subject field may be copied from a certificate request into the signed certificate. Otherwise, the requested Subject will be discarded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#allow_subject_passthrough PrivatecaCertificateTemplate#allow_subject_passthrough}
        '''
        result = self._values.get("allow_subject_passthrough")
        assert result is not None, "Required property 'allow_subject_passthrough' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def cel_expression(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplateIdentityConstraintsCelExpression"]:
        '''cel_expression block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#cel_expression PrivatecaCertificateTemplate#cel_expression}
        '''
        result = self._values.get("cel_expression")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplateIdentityConstraintsCelExpression"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplateIdentityConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplateIdentityConstraintsCelExpression",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "expression": "expression",
        "location": "location",
        "title": "title",
    },
)
class PrivatecaCertificateTemplateIdentityConstraintsCelExpression:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#description PrivatecaCertificateTemplate#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#expression PrivatecaCertificateTemplate#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#location PrivatecaCertificateTemplate#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#title PrivatecaCertificateTemplate#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f65171773132ed02c0c623332f9a650adb3b967ccf6cf2ab6e6cbc1fee467c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#description PrivatecaCertificateTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''Textual representation of an expression in Common Expression Language syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#expression PrivatecaCertificateTemplate#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Optional.

        String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#location PrivatecaCertificateTemplate#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#title PrivatecaCertificateTemplate#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplateIdentityConstraintsCelExpression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplateIdentityConstraintsCelExpressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplateIdentityConstraintsCelExpressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16ee5e55ea5d93a9d9a20c970000beb2dc7905715b0d678570864790e889f2b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe93dd64b0b8e99b9ae31982fe87aa4dc4f9d7153f94e896be470124ebf58abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108b3953813051187aa44a7ffd974f3b1c34b19199e1da4b3903e1ef1f3a2769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359c230ff116bc141037fe8392d1bc62cab371b77d7647004961be18d264bfff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d78e5c1a28022a8fcc36e9943c9be44e6168dd182431d8297e85a6529d576e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplateIdentityConstraintsCelExpression]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplateIdentityConstraintsCelExpression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplateIdentityConstraintsCelExpression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92efb22990912b9f044c335f11a499193d2f9cc7eba7d85564a903b4652f774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateTemplateIdentityConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplateIdentityConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fd53bbaf40f28f38b0a1543d706d2e6b28896473a1edf1e610c1f3b164b3ede)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCelExpression")
    def put_cel_expression(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#description PrivatecaCertificateTemplate#description}
        :param expression: Textual representation of an expression in Common Expression Language syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#expression PrivatecaCertificateTemplate#expression}
        :param location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#location PrivatecaCertificateTemplate#location}
        :param title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#title PrivatecaCertificateTemplate#title}
        '''
        value = PrivatecaCertificateTemplateIdentityConstraintsCelExpression(
            description=description,
            expression=expression,
            location=location,
            title=title,
        )

        return typing.cast(None, jsii.invoke(self, "putCelExpression", [value]))

    @jsii.member(jsii_name="resetCelExpression")
    def reset_cel_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCelExpression", []))

    @builtins.property
    @jsii.member(jsii_name="celExpression")
    def cel_expression(
        self,
    ) -> PrivatecaCertificateTemplateIdentityConstraintsCelExpressionOutputReference:
        return typing.cast(PrivatecaCertificateTemplateIdentityConstraintsCelExpressionOutputReference, jsii.get(self, "celExpression"))

    @builtins.property
    @jsii.member(jsii_name="allowSubjectAltNamesPassthroughInput")
    def allow_subject_alt_names_passthrough_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSubjectAltNamesPassthroughInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSubjectPassthroughInput")
    def allow_subject_passthrough_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSubjectPassthroughInput"))

    @builtins.property
    @jsii.member(jsii_name="celExpressionInput")
    def cel_expression_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplateIdentityConstraintsCelExpression]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplateIdentityConstraintsCelExpression], jsii.get(self, "celExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSubjectAltNamesPassthrough")
    def allow_subject_alt_names_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSubjectAltNamesPassthrough"))

    @allow_subject_alt_names_passthrough.setter
    def allow_subject_alt_names_passthrough(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8552ee992ce7ade47f86d4c86d645f6233bb48f355f6b7ba4b761639d8b6693d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSubjectAltNamesPassthrough", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowSubjectPassthrough")
    def allow_subject_passthrough(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSubjectPassthrough"))

    @allow_subject_passthrough.setter
    def allow_subject_passthrough(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9536bd91a47029a6ddbe13411f3746f7a6dc2ad4ff4cdd6bd35fa4e1c48199a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSubjectPassthrough", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplateIdentityConstraints]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplateIdentityConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplateIdentityConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a333a03dbc40b2e4029eccdfb08afd99ae4a68a93f785c0ad2b0a045bb9075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePassthroughExtensions",
    jsii_struct_bases=[],
    name_mapping={
        "additional_extensions": "additionalExtensions",
        "known_extensions": "knownExtensions",
    },
)
class PrivatecaCertificateTemplatePassthroughExtensions:
    def __init__(
        self,
        *,
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        known_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#additional_extensions PrivatecaCertificateTemplate#additional_extensions}
        :param known_extensions: Optional. A set of named X.509 extensions. Will be combined with additional_extensions to determine the full set of X.509 extensions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#known_extensions PrivatecaCertificateTemplate#known_extensions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2040856d9d45b08696cfd04168a44d78bc65194a5d57d34a2078e973f0885b7d)
            check_type(argname="argument additional_extensions", value=additional_extensions, expected_type=type_hints["additional_extensions"])
            check_type(argname="argument known_extensions", value=known_extensions, expected_type=type_hints["known_extensions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_extensions is not None:
            self._values["additional_extensions"] = additional_extensions
        if known_extensions is not None:
            self._values["known_extensions"] = known_extensions

    @builtins.property
    def additional_extensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions"]]]:
        '''additional_extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#additional_extensions PrivatecaCertificateTemplate#additional_extensions}
        '''
        result = self._values.get("additional_extensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions"]]], result)

    @builtins.property
    def known_extensions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        A set of named X.509 extensions. Will be combined with additional_extensions to determine the full set of X.509 extensions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#known_extensions PrivatecaCertificateTemplate#known_extensions}
        '''
        result = self._values.get("known_extensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePassthroughExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: Required. The parts of an OID path. The most significant parts of the path come first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c23cd0f3692f4832a9b0fa488d74dadb284338092d211f65a2228c0050408cb)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''Required. The parts of an OID path. The most significant parts of the path come first.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31856794374e45316c9874abe5ea975d852bdc35c76b3725c5a6cab94eb15a3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1b5a635417a30c99842341d93c8c5bcb597b3b448171d996deb8ba808362ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b37a99e5d9ad0efdebadb41c884481548172575975780178c38cf3b5ae8350)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66acd6ebe8a8f71b34fbaaca8366fe7ff2b3d55377642a05423c27edf1355086)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5624bc3f8a82bb53c82294869dd9a529cabdb75721c2c9999f62ef1b5348359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2dff7b1ec9138f7362fd9250b47112d777d04d218afd9fca6acabc89b8cf73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5815557eeb13e5c4b357c88f9e6e12890614d50d987c953bd60deb40453e158)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60042b5cf4f1332d5fae88c645c2a73077b77eb860702e623ae2e066e6621039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538e936876d56d2fcdd7084c455f056c1a38c703495fb6ddc99decea6186d37a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateTemplatePassthroughExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePassthroughExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94369883c0c526202a1fdb2e6faa5f00664ea60d94e3d068713124f346a2a877)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalExtensions")
    def put_additional_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39a3498507e62b14408aead556ece6d6233d61fb1c19a49030188603a0e25ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalExtensions", [value]))

    @jsii.member(jsii_name="resetAdditionalExtensions")
    def reset_additional_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalExtensions", []))

    @jsii.member(jsii_name="resetKnownExtensions")
    def reset_known_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKnownExtensions", []))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensions")
    def additional_extensions(
        self,
    ) -> PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsList:
        return typing.cast(PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsList, jsii.get(self, "additionalExtensions"))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensionsInput")
    def additional_extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]]], jsii.get(self, "additionalExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="knownExtensionsInput")
    def known_extensions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "knownExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="knownExtensions")
    def known_extensions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "knownExtensions"))

    @known_extensions.setter
    def known_extensions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b49b21bb5a6ddb341742a821b0fc034c81f6e420f1234f819f4d1194b241d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knownExtensions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePassthroughExtensions]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePassthroughExtensions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplatePassthroughExtensions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1568f7d8c1db7d06dc100faa7e3ca59c2c5df641b59f257bfcb4981bdea0984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValues",
    jsii_struct_bases=[],
    name_mapping={
        "additional_extensions": "additionalExtensions",
        "aia_ocsp_servers": "aiaOcspServers",
        "ca_options": "caOptions",
        "key_usage": "keyUsage",
        "name_constraints": "nameConstraints",
        "policy_ids": "policyIds",
    },
)
class PrivatecaCertificateTemplatePredefinedValues:
    def __init__(
        self,
        *,
        additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        ca_options: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValuesCaOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        key_usage: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValuesKeyUsage", typing.Dict[builtins.str, typing.Any]]] = None,
        name_constraints: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValuesNameConstraints", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePredefinedValuesPolicyIds", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param additional_extensions: additional_extensions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#additional_extensions PrivatecaCertificateTemplate#additional_extensions}
        :param aia_ocsp_servers: Optional. Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#aia_ocsp_servers PrivatecaCertificateTemplate#aia_ocsp_servers}
        :param ca_options: ca_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#ca_options PrivatecaCertificateTemplate#ca_options}
        :param key_usage: key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_usage PrivatecaCertificateTemplate#key_usage}
        :param name_constraints: name_constraints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#name_constraints PrivatecaCertificateTemplate#name_constraints}
        :param policy_ids: policy_ids block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#policy_ids PrivatecaCertificateTemplate#policy_ids}
        '''
        if isinstance(ca_options, dict):
            ca_options = PrivatecaCertificateTemplatePredefinedValuesCaOptions(**ca_options)
        if isinstance(key_usage, dict):
            key_usage = PrivatecaCertificateTemplatePredefinedValuesKeyUsage(**key_usage)
        if isinstance(name_constraints, dict):
            name_constraints = PrivatecaCertificateTemplatePredefinedValuesNameConstraints(**name_constraints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8175658194cbfc94e4abca87ea6414ec7d8f3700f2b798cdc8f6b7ff6f0a4fe3)
            check_type(argname="argument additional_extensions", value=additional_extensions, expected_type=type_hints["additional_extensions"])
            check_type(argname="argument aia_ocsp_servers", value=aia_ocsp_servers, expected_type=type_hints["aia_ocsp_servers"])
            check_type(argname="argument ca_options", value=ca_options, expected_type=type_hints["ca_options"])
            check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            check_type(argname="argument name_constraints", value=name_constraints, expected_type=type_hints["name_constraints"])
            check_type(argname="argument policy_ids", value=policy_ids, expected_type=type_hints["policy_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_extensions is not None:
            self._values["additional_extensions"] = additional_extensions
        if aia_ocsp_servers is not None:
            self._values["aia_ocsp_servers"] = aia_ocsp_servers
        if ca_options is not None:
            self._values["ca_options"] = ca_options
        if key_usage is not None:
            self._values["key_usage"] = key_usage
        if name_constraints is not None:
            self._values["name_constraints"] = name_constraints
        if policy_ids is not None:
            self._values["policy_ids"] = policy_ids

    @builtins.property
    def additional_extensions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions"]]]:
        '''additional_extensions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#additional_extensions PrivatecaCertificateTemplate#additional_extensions}
        '''
        result = self._values.get("additional_extensions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions"]]], result)

    @builtins.property
    def aia_ocsp_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        Describes Online Certificate Status Protocol (OCSP) endpoint addresses that appear in the "Authority Information Access" extension in the certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#aia_ocsp_servers PrivatecaCertificateTemplate#aia_ocsp_servers}
        '''
        result = self._values.get("aia_ocsp_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ca_options(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePredefinedValuesCaOptions"]:
        '''ca_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#ca_options PrivatecaCertificateTemplate#ca_options}
        '''
        result = self._values.get("ca_options")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePredefinedValuesCaOptions"], result)

    @builtins.property
    def key_usage(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePredefinedValuesKeyUsage"]:
        '''key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_usage PrivatecaCertificateTemplate#key_usage}
        '''
        result = self._values.get("key_usage")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePredefinedValuesKeyUsage"], result)

    @builtins.property
    def name_constraints(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePredefinedValuesNameConstraints"]:
        '''name_constraints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#name_constraints PrivatecaCertificateTemplate#name_constraints}
        '''
        result = self._values.get("name_constraints")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePredefinedValuesNameConstraints"], result)

    @builtins.property
    def policy_ids(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesPolicyIds"]]]:
        '''policy_ids block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#policy_ids PrivatecaCertificateTemplate#policy_ids}
        '''
        result = self._values.get("policy_ids")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesPolicyIds"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions",
    jsii_struct_bases=[],
    name_mapping={"object_id": "objectId", "value": "value", "critical": "critical"},
)
class PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions:
    def __init__(
        self,
        *,
        object_id: typing.Union["PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId", typing.Dict[builtins.str, typing.Any]],
        value: builtins.str,
        critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param object_id: object_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id PrivatecaCertificateTemplate#object_id}
        :param value: Required. The value of this X.509 extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#value PrivatecaCertificateTemplate#value}
        :param critical: Optional. Indicates whether or not this extension is critical (i.e., if the client does not know how to handle this extension, the client should consider this to be an error). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#critical PrivatecaCertificateTemplate#critical}
        '''
        if isinstance(object_id, dict):
            object_id = PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId(**object_id)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6929a9c4c5d17afb71986fc7bfe577b2ba1a080f425ae1aece852d899e3e75d)
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id": object_id,
            "value": value,
        }
        if critical is not None:
            self._values["critical"] = critical

    @builtins.property
    def object_id(
        self,
    ) -> "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId":
        '''object_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id PrivatecaCertificateTemplate#object_id}
        '''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast("PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId", result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Required. The value of this X.509 extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#value PrivatecaCertificateTemplate#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def critical(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Indicates whether or not this extension is critical (i.e., if the client does not know how to handle this extension, the client should consider this to be an error).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#critical PrivatecaCertificateTemplate#critical}
        '''
        result = self._values.get("critical")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e463bf9dc9f6efbdbb487008c7f2cd3618dc75122fb3c423b7dfd243bfdb738f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37588689665cf6de2bb8cddb6ef49d03e6d80f20bb6373079744a3a51c49a981)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbc1708fbdc542c9bd5b42caacd2e453372d0979f7570923e573fcfb6dc429d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed1339cd5b23041f89ec738306c4d7ea7cb526e7fcb41adc202206863d43154b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d665325bee7c063db91163bb34c8ab96ee86f57ca564c5c127e1e03dd027b5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a217e1a1d8e5c42a01cf898b2975381d77f158f5623f9712b848ac7da6c75927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: Required. The parts of an OID path. The most significant parts of the path come first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbefc0da6768bda6b24809bea66a8e103ac23efa0de20aef2aa7e928c91fc359)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''Required. The parts of an OID path. The most significant parts of the path come first.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aec1a55af179b29bb54f80c0a54318d2d49ffeb152061edd82c47941695f2fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8c0c25484e692bb622f311c820b232760c1f9da1183d4b1fe4acdd51bb3712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c5d35db8464ce286c5738f10653188bdecfe3e67e4cabec4cd3e4f094085b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16663201d03180576c2237df30d5a6c8b99f18d4ce7cc97033d9128e1b37c91b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putObjectId")
    def put_object_id(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: Required. The parts of an OID path. The most significant parts of the path come first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        value = PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId(
            object_id_path=object_id_path
        )

        return typing.cast(None, jsii.invoke(self, "putObjectId", [value]))

    @jsii.member(jsii_name="resetCritical")
    def reset_critical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCritical", []))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(
        self,
    ) -> PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectIdOutputReference:
        return typing.cast(PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectIdOutputReference, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "critical"))

    @critical.setter
    def critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cd1a8ad4f6591b5532cf05f177fc4f650f7baa480bfa34357e1b41498999cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfd20dd5020b52b180e7797635ae9cbfabc668bc7665f6a2ca6aa62e86e350f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c841023c388ae4790b44f7806a8215b252688d7122b873c571589a4895ad31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesCaOptions",
    jsii_struct_bases=[],
    name_mapping={
        "is_ca": "isCa",
        "max_issuer_path_length": "maxIssuerPathLength",
        "null_ca": "nullCa",
        "zero_max_issuer_path_length": "zeroMaxIssuerPathLength",
    },
)
class PrivatecaCertificateTemplatePredefinedValuesCaOptions:
    def __init__(
        self,
        *,
        is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        null_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: Optional. Refers to the "CA" X.509 extension, which is a boolean value. When this value is true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#is_ca PrivatecaCertificateTemplate#is_ca}
        :param max_issuer_path_length: Optional. Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#max_issuer_path_length PrivatecaCertificateTemplate#max_issuer_path_length}
        :param null_ca: Optional. When true, the "CA" in Basic Constraints extension will be set to null and omitted from the CA certificate. If both 'is_ca' and 'null_ca' are unset, the "CA" in Basic Constraints extension will be set to false. Note that the behavior when 'is_ca = false' for this resource is different from the behavior in the Certificate Authority, Certificate and CaPool resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#null_ca PrivatecaCertificateTemplate#null_ca}
        :param zero_max_issuer_path_length: Optional. When true, the "path length constraint" in Basic Constraints extension will be set to 0. if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#zero_max_issuer_path_length PrivatecaCertificateTemplate#zero_max_issuer_path_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91663ea25b0e236cdfcf45d1563be0b5213f4cc5676510dd5e863e13720d8b71)
            check_type(argname="argument is_ca", value=is_ca, expected_type=type_hints["is_ca"])
            check_type(argname="argument max_issuer_path_length", value=max_issuer_path_length, expected_type=type_hints["max_issuer_path_length"])
            check_type(argname="argument null_ca", value=null_ca, expected_type=type_hints["null_ca"])
            check_type(argname="argument zero_max_issuer_path_length", value=zero_max_issuer_path_length, expected_type=type_hints["zero_max_issuer_path_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if is_ca is not None:
            self._values["is_ca"] = is_ca
        if max_issuer_path_length is not None:
            self._values["max_issuer_path_length"] = max_issuer_path_length
        if null_ca is not None:
            self._values["null_ca"] = null_ca
        if zero_max_issuer_path_length is not None:
            self._values["zero_max_issuer_path_length"] = zero_max_issuer_path_length

    @builtins.property
    def is_ca(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        Refers to the "CA" X.509 extension, which is a boolean value. When this value is true, the "CA" in Basic Constraints extension will be set to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#is_ca PrivatecaCertificateTemplate#is_ca}
        '''
        result = self._values.get("is_ca")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_issuer_path_length(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of
        subordinate CA certificates that are allowed. If this value is less than 0, the request will fail.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#max_issuer_path_length PrivatecaCertificateTemplate#max_issuer_path_length}
        '''
        result = self._values.get("max_issuer_path_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def null_ca(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        When true, the "CA" in Basic Constraints extension will be set to null and omitted from the CA certificate.
        If both 'is_ca' and 'null_ca' are unset, the "CA" in Basic Constraints extension will be set to false.
        Note that the behavior when 'is_ca = false' for this resource is different from the behavior in the Certificate Authority, Certificate and CaPool resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#null_ca PrivatecaCertificateTemplate#null_ca}
        '''
        result = self._values.get("null_ca")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zero_max_issuer_path_length(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Optional.

        When true, the "path length constraint" in Basic Constraints extension will be set to 0.
        if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset,
        the max path length will be omitted from the CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#zero_max_issuer_path_length PrivatecaCertificateTemplate#zero_max_issuer_path_length}
        '''
        result = self._values.get("zero_max_issuer_path_length")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesCaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePredefinedValuesCaOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesCaOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c691d68ab55c331446a515c9e100ca5b147ae101edea353ab17f7d4e1ac5f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsCa")
    def reset_is_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCa", []))

    @jsii.member(jsii_name="resetMaxIssuerPathLength")
    def reset_max_issuer_path_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIssuerPathLength", []))

    @jsii.member(jsii_name="resetNullCa")
    def reset_null_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullCa", []))

    @jsii.member(jsii_name="resetZeroMaxIssuerPathLength")
    def reset_zero_max_issuer_path_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZeroMaxIssuerPathLength", []))

    @builtins.property
    @jsii.member(jsii_name="isCaInput")
    def is_ca_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCaInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLengthInput")
    def max_issuer_path_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIssuerPathLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="nullCaInput")
    def null_ca_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nullCaInput"))

    @builtins.property
    @jsii.member(jsii_name="zeroMaxIssuerPathLengthInput")
    def zero_max_issuer_path_length_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zeroMaxIssuerPathLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="isCa")
    def is_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCa"))

    @is_ca.setter
    def is_ca(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4072c9c73689011d3fbdfcc5b928fa20ffca08955ef7fa1a531338e8ca610050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxIssuerPathLength")
    def max_issuer_path_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIssuerPathLength"))

    @max_issuer_path_length.setter
    def max_issuer_path_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6770a603fb1e7a811ebc74ec3394e180ffa7c3d5babda701edc539617a0a6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIssuerPathLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullCa")
    def null_ca(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nullCa"))

    @null_ca.setter
    def null_ca(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2592a7b66e168a4c8e55d319f9f16d2a0a5c3bcfec6422da375a4a1737a67ec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullCa", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zeroMaxIssuerPathLength")
    def zero_max_issuer_path_length(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zeroMaxIssuerPathLength"))

    @zero_max_issuer_path_length.setter
    def zero_max_issuer_path_length(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92657c797cab029f17318f5911052584f6495239ac87e158099f7cda6afdccad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zeroMaxIssuerPathLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesCaOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesCaOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f6ceca2ade4e8afd32e881e53ac68f3e3dd1b7db4cf4af7b222e8367211ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "base_key_usage": "baseKeyUsage",
        "extended_key_usage": "extendedKeyUsage",
        "unknown_extended_key_usages": "unknownExtendedKeyUsages",
    },
)
class PrivatecaCertificateTemplatePredefinedValuesKeyUsage:
    def __init__(
        self,
        *,
        base_key_usage: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage", typing.Dict[builtins.str, typing.Any]]] = None,
        extended_key_usage: typing.Optional[typing.Union["PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage", typing.Dict[builtins.str, typing.Any]]] = None,
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#base_key_usage PrivatecaCertificateTemplate#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#extended_key_usage PrivatecaCertificateTemplate#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#unknown_extended_key_usages PrivatecaCertificateTemplate#unknown_extended_key_usages}
        '''
        if isinstance(base_key_usage, dict):
            base_key_usage = PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage(**base_key_usage)
        if isinstance(extended_key_usage, dict):
            extended_key_usage = PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage(**extended_key_usage)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ab4e8a951110e7164f30562925046ad990a515425366dde391a6a81ebe4981)
            check_type(argname="argument base_key_usage", value=base_key_usage, expected_type=type_hints["base_key_usage"])
            check_type(argname="argument extended_key_usage", value=extended_key_usage, expected_type=type_hints["extended_key_usage"])
            check_type(argname="argument unknown_extended_key_usages", value=unknown_extended_key_usages, expected_type=type_hints["unknown_extended_key_usages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_key_usage is not None:
            self._values["base_key_usage"] = base_key_usage
        if extended_key_usage is not None:
            self._values["extended_key_usage"] = extended_key_usage
        if unknown_extended_key_usages is not None:
            self._values["unknown_extended_key_usages"] = unknown_extended_key_usages

    @builtins.property
    def base_key_usage(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage"]:
        '''base_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#base_key_usage PrivatecaCertificateTemplate#base_key_usage}
        '''
        result = self._values.get("base_key_usage")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage"], result)

    @builtins.property
    def extended_key_usage(
        self,
    ) -> typing.Optional["PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage"]:
        '''extended_key_usage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#extended_key_usage PrivatecaCertificateTemplate#extended_key_usage}
        '''
        result = self._values.get("extended_key_usage")
        return typing.cast(typing.Optional["PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage"], result)

    @builtins.property
    def unknown_extended_key_usages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages"]]]:
        '''unknown_extended_key_usages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#unknown_extended_key_usages PrivatecaCertificateTemplate#unknown_extended_key_usages}
        '''
        result = self._values.get("unknown_extended_key_usages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "cert_sign": "certSign",
        "content_commitment": "contentCommitment",
        "crl_sign": "crlSign",
        "data_encipherment": "dataEncipherment",
        "decipher_only": "decipherOnly",
        "digital_signature": "digitalSignature",
        "encipher_only": "encipherOnly",
        "key_agreement": "keyAgreement",
        "key_encipherment": "keyEncipherment",
    },
)
class PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage:
    def __init__(
        self,
        *,
        cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#cert_sign PrivatecaCertificateTemplate#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#content_commitment PrivatecaCertificateTemplate#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#crl_sign PrivatecaCertificateTemplate#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#data_encipherment PrivatecaCertificateTemplate#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#decipher_only PrivatecaCertificateTemplate#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#digital_signature PrivatecaCertificateTemplate#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#encipher_only PrivatecaCertificateTemplate#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_agreement PrivatecaCertificateTemplate#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_encipherment PrivatecaCertificateTemplate#key_encipherment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2182d3369fdc879f949cdf7431415d619d787c17f4e9264a4f6b1966e53f1ef)
            check_type(argname="argument cert_sign", value=cert_sign, expected_type=type_hints["cert_sign"])
            check_type(argname="argument content_commitment", value=content_commitment, expected_type=type_hints["content_commitment"])
            check_type(argname="argument crl_sign", value=crl_sign, expected_type=type_hints["crl_sign"])
            check_type(argname="argument data_encipherment", value=data_encipherment, expected_type=type_hints["data_encipherment"])
            check_type(argname="argument decipher_only", value=decipher_only, expected_type=type_hints["decipher_only"])
            check_type(argname="argument digital_signature", value=digital_signature, expected_type=type_hints["digital_signature"])
            check_type(argname="argument encipher_only", value=encipher_only, expected_type=type_hints["encipher_only"])
            check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
            check_type(argname="argument key_encipherment", value=key_encipherment, expected_type=type_hints["key_encipherment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cert_sign is not None:
            self._values["cert_sign"] = cert_sign
        if content_commitment is not None:
            self._values["content_commitment"] = content_commitment
        if crl_sign is not None:
            self._values["crl_sign"] = crl_sign
        if data_encipherment is not None:
            self._values["data_encipherment"] = data_encipherment
        if decipher_only is not None:
            self._values["decipher_only"] = decipher_only
        if digital_signature is not None:
            self._values["digital_signature"] = digital_signature
        if encipher_only is not None:
            self._values["encipher_only"] = encipher_only
        if key_agreement is not None:
            self._values["key_agreement"] = key_agreement
        if key_encipherment is not None:
            self._values["key_encipherment"] = key_encipherment

    @builtins.property
    def cert_sign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to sign certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#cert_sign PrivatecaCertificateTemplate#cert_sign}
        '''
        result = self._values.get("cert_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def content_commitment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#content_commitment PrivatecaCertificateTemplate#content_commitment}
        '''
        result = self._values.get("content_commitment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crl_sign(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used sign certificate revocation lists.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#crl_sign PrivatecaCertificateTemplate#crl_sign}
        '''
        result = self._values.get("crl_sign")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#data_encipherment PrivatecaCertificateTemplate#data_encipherment}
        '''
        result = self._values.get("data_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def decipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to decipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#decipher_only PrivatecaCertificateTemplate#decipher_only}
        '''
        result = self._values.get("decipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def digital_signature(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used for digital signatures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#digital_signature PrivatecaCertificateTemplate#digital_signature}
        '''
        result = self._values.get("digital_signature")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encipher_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#encipher_only PrivatecaCertificateTemplate#encipher_only}
        '''
        result = self._values.get("encipher_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_agreement(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used in a key agreement protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_agreement PrivatecaCertificateTemplate#key_agreement}
        '''
        result = self._values.get("key_agreement")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key_encipherment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The key may be used to encipher other keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_encipherment PrivatecaCertificateTemplate#key_encipherment}
        '''
        result = self._values.get("key_encipherment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1e9686589f50a1518d044f16529633ee1aa9eef5eeb601b5d6653118c22b984)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCertSign")
    def reset_cert_sign(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertSign", []))

    @jsii.member(jsii_name="resetContentCommitment")
    def reset_content_commitment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentCommitment", []))

    @jsii.member(jsii_name="resetCrlSign")
    def reset_crl_sign(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrlSign", []))

    @jsii.member(jsii_name="resetDataEncipherment")
    def reset_data_encipherment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataEncipherment", []))

    @jsii.member(jsii_name="resetDecipherOnly")
    def reset_decipher_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecipherOnly", []))

    @jsii.member(jsii_name="resetDigitalSignature")
    def reset_digital_signature(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigitalSignature", []))

    @jsii.member(jsii_name="resetEncipherOnly")
    def reset_encipher_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncipherOnly", []))

    @jsii.member(jsii_name="resetKeyAgreement")
    def reset_key_agreement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyAgreement", []))

    @jsii.member(jsii_name="resetKeyEncipherment")
    def reset_key_encipherment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyEncipherment", []))

    @builtins.property
    @jsii.member(jsii_name="certSignInput")
    def cert_sign_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "certSignInput"))

    @builtins.property
    @jsii.member(jsii_name="contentCommitmentInput")
    def content_commitment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "contentCommitmentInput"))

    @builtins.property
    @jsii.member(jsii_name="crlSignInput")
    def crl_sign_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crlSignInput"))

    @builtins.property
    @jsii.member(jsii_name="dataEnciphermentInput")
    def data_encipherment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dataEnciphermentInput"))

    @builtins.property
    @jsii.member(jsii_name="decipherOnlyInput")
    def decipher_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "decipherOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="digitalSignatureInput")
    def digital_signature_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "digitalSignatureInput"))

    @builtins.property
    @jsii.member(jsii_name="encipherOnlyInput")
    def encipher_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encipherOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAgreementInput")
    def key_agreement_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keyAgreementInput"))

    @builtins.property
    @jsii.member(jsii_name="keyEnciphermentInput")
    def key_encipherment_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keyEnciphermentInput"))

    @builtins.property
    @jsii.member(jsii_name="certSign")
    def cert_sign(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "certSign"))

    @cert_sign.setter
    def cert_sign(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067589cba431c9b0d784b767b176043e2eeedd260bd8cf748dcfcd582a041b7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certSign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentCommitment")
    def content_commitment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "contentCommitment"))

    @content_commitment.setter
    def content_commitment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe1e7dc3a37cb3e174491399a02964228c83d2bb6735a7a36fbb6e204772760e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentCommitment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crlSign")
    def crl_sign(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crlSign"))

    @crl_sign.setter
    def crl_sign(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4524375e03c0f99ce694f0e188db9623bb2fb302421c4371ba28e1484cc82960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crlSign", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataEncipherment")
    def data_encipherment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dataEncipherment"))

    @data_encipherment.setter
    def data_encipherment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1b5fb726c172d86a3af08821dc3519d1d5d81ac6b0e8a55e53c57d899e4e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataEncipherment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="decipherOnly")
    def decipher_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "decipherOnly"))

    @decipher_only.setter
    def decipher_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9876c0a1fc1816d81495967fef556397fa63fcad65eb524e7346b27f9bb591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decipherOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="digitalSignature")
    def digital_signature(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "digitalSignature"))

    @digital_signature.setter
    def digital_signature(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388b7c82f17ee7c9cf13056389d7c628cebcb4656c70bdfba48961f96159e4b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "digitalSignature", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encipherOnly")
    def encipher_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encipherOnly"))

    @encipher_only.setter
    def encipher_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71da8f3df1fcc1c33ce7eeddf36c49cc41bbc1757cba290e32102a97d854797b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encipherOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyAgreement")
    def key_agreement(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keyAgreement"))

    @key_agreement.setter
    def key_agreement(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3347d759489f85f8aa939c18af0b528ee85d90e2db8d5ae828cabd0b2fd8b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAgreement", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyEncipherment")
    def key_encipherment(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keyEncipherment"))

    @key_encipherment.setter
    def key_encipherment(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc8c63c30ce1b6f48fd768b25651ec095417f0c7f6d5f40c13be5617d329bb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyEncipherment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ede101ffbbfbe0d623cc33a1c4b665387d77ba065bbf21c79c5c4f2340ebf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage",
    jsii_struct_bases=[],
    name_mapping={
        "client_auth": "clientAuth",
        "code_signing": "codeSigning",
        "email_protection": "emailProtection",
        "ocsp_signing": "ocspSigning",
        "server_auth": "serverAuth",
        "time_stamping": "timeStamping",
    },
)
class PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage:
    def __init__(
        self,
        *,
        client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#client_auth PrivatecaCertificateTemplate#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#code_signing PrivatecaCertificateTemplate#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#email_protection PrivatecaCertificateTemplate#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#ocsp_signing PrivatecaCertificateTemplate#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#server_auth PrivatecaCertificateTemplate#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#time_stamping PrivatecaCertificateTemplate#time_stamping}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff67ecf1ff863391aea5a417804b8a91d79341fe040f9430f735dcf8a21feecf)
            check_type(argname="argument client_auth", value=client_auth, expected_type=type_hints["client_auth"])
            check_type(argname="argument code_signing", value=code_signing, expected_type=type_hints["code_signing"])
            check_type(argname="argument email_protection", value=email_protection, expected_type=type_hints["email_protection"])
            check_type(argname="argument ocsp_signing", value=ocsp_signing, expected_type=type_hints["ocsp_signing"])
            check_type(argname="argument server_auth", value=server_auth, expected_type=type_hints["server_auth"])
            check_type(argname="argument time_stamping", value=time_stamping, expected_type=type_hints["time_stamping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_auth is not None:
            self._values["client_auth"] = client_auth
        if code_signing is not None:
            self._values["code_signing"] = code_signing
        if email_protection is not None:
            self._values["email_protection"] = email_protection
        if ocsp_signing is not None:
            self._values["ocsp_signing"] = ocsp_signing
        if server_auth is not None:
            self._values["server_auth"] = server_auth
        if time_stamping is not None:
            self._values["time_stamping"] = time_stamping

    @builtins.property
    def client_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#client_auth PrivatecaCertificateTemplate#client_auth}
        '''
        result = self._values.get("client_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def code_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#code_signing PrivatecaCertificateTemplate#code_signing}
        '''
        result = self._values.get("code_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def email_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#email_protection PrivatecaCertificateTemplate#email_protection}
        '''
        result = self._values.get("email_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ocsp_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#ocsp_signing PrivatecaCertificateTemplate#ocsp_signing}
        '''
        result = self._values.get("ocsp_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def server_auth(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#server_auth PrivatecaCertificateTemplate#server_auth}
        '''
        result = self._values.get("server_auth")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def time_stamping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#time_stamping PrivatecaCertificateTemplate#time_stamping}
        '''
        result = self._values.get("time_stamping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98984527a9bd368b5cd595860e3ce5a5789f1a3db8dfc95b1516cb88e8acf4cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientAuth")
    def reset_client_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientAuth", []))

    @jsii.member(jsii_name="resetCodeSigning")
    def reset_code_signing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeSigning", []))

    @jsii.member(jsii_name="resetEmailProtection")
    def reset_email_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailProtection", []))

    @jsii.member(jsii_name="resetOcspSigning")
    def reset_ocsp_signing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOcspSigning", []))

    @jsii.member(jsii_name="resetServerAuth")
    def reset_server_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerAuth", []))

    @jsii.member(jsii_name="resetTimeStamping")
    def reset_time_stamping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeStamping", []))

    @builtins.property
    @jsii.member(jsii_name="clientAuthInput")
    def client_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="codeSigningInput")
    def code_signing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "codeSigningInput"))

    @builtins.property
    @jsii.member(jsii_name="emailProtectionInput")
    def email_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "emailProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="ocspSigningInput")
    def ocsp_signing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ocspSigningInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAuthInput")
    def server_auth_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serverAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="timeStampingInput")
    def time_stamping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeStampingInput"))

    @builtins.property
    @jsii.member(jsii_name="clientAuth")
    def client_auth(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientAuth"))

    @client_auth.setter
    def client_auth(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e746dfa5dee48a391a75d838acf4b679d596bfb0fefca3c784822d9c2d080e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeSigning")
    def code_signing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "codeSigning"))

    @code_signing.setter
    def code_signing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdfec3db966eb6b8b5e8414a59b4ba70a860b38c898af3c1997dc8d707bba592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeSigning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailProtection")
    def email_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "emailProtection"))

    @email_protection.setter
    def email_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816519bbc73db6148efa815f8874cde3bd4a5034dc41fa8e6b049d9221c91ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ocspSigning")
    def ocsp_signing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ocspSigning"))

    @ocsp_signing.setter
    def ocsp_signing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdadc70da9e345ceb6c045059ec95ae6c5edf79329c3a7b96f2bd10d35e5c0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ocspSigning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverAuth")
    def server_auth(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serverAuth"))

    @server_auth.setter
    def server_auth(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906d6c1a728b1bff2e2bbda36e6d7e0b77d6483c150cf0aa165d25e45a1ca501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeStamping")
    def time_stamping(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "timeStamping"))

    @time_stamping.setter
    def time_stamping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a117da6d9d1b7dd22f6ce2f66b7e31fb7a8af5231312de5ae0604cbd3ee9b987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeStamping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2b4af5d240b9d15e250fdf6b9ceb30c95a6459673408b864e7db3fc5a0587d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateTemplatePredefinedValuesKeyUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4944f1341b67b29fc0249bb8b8c9b7f2cd1ec1b70ffb7327f2c021806bc9a45b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBaseKeyUsage")
    def put_base_key_usage(
        self,
        *,
        cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cert_sign: The key may be used to sign certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#cert_sign PrivatecaCertificateTemplate#cert_sign}
        :param content_commitment: The key may be used for cryptographic commitments. Note that this may also be referred to as "non-repudiation". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#content_commitment PrivatecaCertificateTemplate#content_commitment}
        :param crl_sign: The key may be used sign certificate revocation lists. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#crl_sign PrivatecaCertificateTemplate#crl_sign}
        :param data_encipherment: The key may be used to encipher data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#data_encipherment PrivatecaCertificateTemplate#data_encipherment}
        :param decipher_only: The key may be used to decipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#decipher_only PrivatecaCertificateTemplate#decipher_only}
        :param digital_signature: The key may be used for digital signatures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#digital_signature PrivatecaCertificateTemplate#digital_signature}
        :param encipher_only: The key may be used to encipher only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#encipher_only PrivatecaCertificateTemplate#encipher_only}
        :param key_agreement: The key may be used in a key agreement protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_agreement PrivatecaCertificateTemplate#key_agreement}
        :param key_encipherment: The key may be used to encipher other keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#key_encipherment PrivatecaCertificateTemplate#key_encipherment}
        '''
        value = PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage(
            cert_sign=cert_sign,
            content_commitment=content_commitment,
            crl_sign=crl_sign,
            data_encipherment=data_encipherment,
            decipher_only=decipher_only,
            digital_signature=digital_signature,
            encipher_only=encipher_only,
            key_agreement=key_agreement,
            key_encipherment=key_encipherment,
        )

        return typing.cast(None, jsii.invoke(self, "putBaseKeyUsage", [value]))

    @jsii.member(jsii_name="putExtendedKeyUsage")
    def put_extended_key_usage(
        self,
        *,
        client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_auth: Corresponds to OID 1.3.6.1.5.5.7.3.2. Officially described as "TLS WWW client authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#client_auth PrivatecaCertificateTemplate#client_auth}
        :param code_signing: Corresponds to OID 1.3.6.1.5.5.7.3.3. Officially described as "Signing of downloadable executable code client authentication". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#code_signing PrivatecaCertificateTemplate#code_signing}
        :param email_protection: Corresponds to OID 1.3.6.1.5.5.7.3.4. Officially described as "Email protection". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#email_protection PrivatecaCertificateTemplate#email_protection}
        :param ocsp_signing: Corresponds to OID 1.3.6.1.5.5.7.3.9. Officially described as "Signing OCSP responses". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#ocsp_signing PrivatecaCertificateTemplate#ocsp_signing}
        :param server_auth: Corresponds to OID 1.3.6.1.5.5.7.3.1. Officially described as "TLS WWW server authentication", though regularly used for non-WWW TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#server_auth PrivatecaCertificateTemplate#server_auth}
        :param time_stamping: Corresponds to OID 1.3.6.1.5.5.7.3.8. Officially described as "Binding the hash of an object to a time". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#time_stamping PrivatecaCertificateTemplate#time_stamping}
        '''
        value = PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage(
            client_auth=client_auth,
            code_signing=code_signing,
            email_protection=email_protection,
            ocsp_signing=ocsp_signing,
            server_auth=server_auth,
            time_stamping=time_stamping,
        )

        return typing.cast(None, jsii.invoke(self, "putExtendedKeyUsage", [value]))

    @jsii.member(jsii_name="putUnknownExtendedKeyUsages")
    def put_unknown_extended_key_usages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5ceed319a9cb6cf8d4ec63380575cc1821c3e7d40315a650c7a4ab1902afc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUnknownExtendedKeyUsages", [value]))

    @jsii.member(jsii_name="resetBaseKeyUsage")
    def reset_base_key_usage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseKeyUsage", []))

    @jsii.member(jsii_name="resetExtendedKeyUsage")
    def reset_extended_key_usage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtendedKeyUsage", []))

    @jsii.member(jsii_name="resetUnknownExtendedKeyUsages")
    def reset_unknown_extended_key_usages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnknownExtendedKeyUsages", []))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsage")
    def base_key_usage(
        self,
    ) -> PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsageOutputReference, jsii.get(self, "baseKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsage")
    def extended_key_usage(
        self,
    ) -> PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsageOutputReference, jsii.get(self, "extendedKeyUsage"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsages")
    def unknown_extended_key_usages(
        self,
    ) -> "PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesList":
        return typing.cast("PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesList", jsii.get(self, "unknownExtendedKeyUsages"))

    @builtins.property
    @jsii.member(jsii_name="baseKeyUsageInput")
    def base_key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage], jsii.get(self, "baseKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="extendedKeyUsageInput")
    def extended_key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage], jsii.get(self, "extendedKeyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="unknownExtendedKeyUsagesInput")
    def unknown_extended_key_usages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages"]]], jsii.get(self, "unknownExtendedKeyUsagesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99001647f3ba85c2706d581d9c979f205a8dc735b2f2f365fe785c95d46da88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: Required. The parts of an OID path. The most significant parts of the path come first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae675e8ce519d67ec30253043015637407a2c5c045eb6db98088473f0f22268)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''Required. The parts of an OID path. The most significant parts of the path come first.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81150b6d5693c4ca6b05ee6616cc69e1e24326903d04d9700de45b6aeab21278)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbaeaae9d1153fa3c677d713f31cd1d7c19e85f30d82def26c09ca25637ae67)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be82928dff365277d11453bcbd6418a8431965d386353ba2d28a83a3dc8831fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f01ed51c0832eb289f1e614ac29c80848c5bb1b0fd41bf6e7747e81ebb9b70ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6f38d7292f055640348ee02434f44053c3cdc539c7d1b78367d688cd3093099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd2dc33fb093d2377da62e28c0d53bd0b6673a71517cbf737ec20419d4f0cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6ec22b4809f910b4eaaf7df7c8c120546828301646716d05919103d756450b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca404958814495d7330c51c021d0ef7aca522693fc72631b27f0e8a090cad70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2dcac53347b6f0a6d482aea8ab38408a3ee3076bdfeeaf8d3db0769e1b7a8d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesNameConstraints",
    jsii_struct_bases=[],
    name_mapping={
        "critical": "critical",
        "excluded_dns_names": "excludedDnsNames",
        "excluded_email_addresses": "excludedEmailAddresses",
        "excluded_ip_ranges": "excludedIpRanges",
        "excluded_uris": "excludedUris",
        "permitted_dns_names": "permittedDnsNames",
        "permitted_email_addresses": "permittedEmailAddresses",
        "permitted_ip_ranges": "permittedIpRanges",
        "permitted_uris": "permittedUris",
    },
)
class PrivatecaCertificateTemplatePredefinedValuesNameConstraints:
    def __init__(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#critical PrivatecaCertificateTemplate#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_dns_names PrivatecaCertificateTemplate#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_email_addresses PrivatecaCertificateTemplate#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_ip_ranges PrivatecaCertificateTemplate#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_uris PrivatecaCertificateTemplate#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_dns_names PrivatecaCertificateTemplate#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_email_addresses PrivatecaCertificateTemplate#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_ip_ranges PrivatecaCertificateTemplate#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_uris PrivatecaCertificateTemplate#permitted_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1b39fdd4eb5f55a2c54488ff1f7096102b46e6736954e14771935691cdc4e8)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument excluded_dns_names", value=excluded_dns_names, expected_type=type_hints["excluded_dns_names"])
            check_type(argname="argument excluded_email_addresses", value=excluded_email_addresses, expected_type=type_hints["excluded_email_addresses"])
            check_type(argname="argument excluded_ip_ranges", value=excluded_ip_ranges, expected_type=type_hints["excluded_ip_ranges"])
            check_type(argname="argument excluded_uris", value=excluded_uris, expected_type=type_hints["excluded_uris"])
            check_type(argname="argument permitted_dns_names", value=permitted_dns_names, expected_type=type_hints["permitted_dns_names"])
            check_type(argname="argument permitted_email_addresses", value=permitted_email_addresses, expected_type=type_hints["permitted_email_addresses"])
            check_type(argname="argument permitted_ip_ranges", value=permitted_ip_ranges, expected_type=type_hints["permitted_ip_ranges"])
            check_type(argname="argument permitted_uris", value=permitted_uris, expected_type=type_hints["permitted_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "critical": critical,
        }
        if excluded_dns_names is not None:
            self._values["excluded_dns_names"] = excluded_dns_names
        if excluded_email_addresses is not None:
            self._values["excluded_email_addresses"] = excluded_email_addresses
        if excluded_ip_ranges is not None:
            self._values["excluded_ip_ranges"] = excluded_ip_ranges
        if excluded_uris is not None:
            self._values["excluded_uris"] = excluded_uris
        if permitted_dns_names is not None:
            self._values["permitted_dns_names"] = permitted_dns_names
        if permitted_email_addresses is not None:
            self._values["permitted_email_addresses"] = permitted_email_addresses
        if permitted_ip_ranges is not None:
            self._values["permitted_ip_ranges"] = permitted_ip_ranges
        if permitted_uris is not None:
            self._values["permitted_uris"] = permitted_uris

    @builtins.property
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether or not the name constraints are marked critical.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#critical PrivatecaCertificateTemplate#critical}
        '''
        result = self._values.get("critical")
        assert result is not None, "Required property 'critical' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def excluded_dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains excluded DNS names.

        Any DNS name that can be
        constructed by simply adding zero or more labels to
        the left-hand side of the name satisfies the name constraint.
        For example, 'example.com', 'www.example.com', 'www.sub.example.com'
        would satisfy 'example.com' while 'example1.com' does not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_dns_names PrivatecaCertificateTemplate#excluded_dns_names}
        '''
        result = self._values.get("excluded_dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded email addresses.

        The value can be a particular
        email address, a hostname to indicate all email addresses on that host or
        a domain with a leading period (e.g. '.example.com') to indicate
        all email addresses in that domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_email_addresses PrivatecaCertificateTemplate#excluded_email_addresses}
        '''
        result = self._values.get("excluded_email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded IP ranges.

        For IPv4 addresses, the ranges
        are expressed using CIDR notation as specified in RFC 4632.
        For IPv6 addresses, the ranges are expressed in similar encoding as IPv4
        addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_ip_ranges PrivatecaCertificateTemplate#excluded_ip_ranges}
        '''
        result = self._values.get("excluded_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the excluded URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_uris PrivatecaCertificateTemplate#excluded_uris}
        '''
        result = self._values.get("excluded_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_dns_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains permitted DNS names.

        Any DNS name that can be
        constructed by simply adding zero or more labels to
        the left-hand side of the name satisfies the name constraint.
        For example, 'example.com', 'www.example.com', 'www.sub.example.com'
        would satisfy 'example.com' while 'example1.com' does not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_dns_names PrivatecaCertificateTemplate#permitted_dns_names}
        '''
        result = self._values.get("permitted_dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted email addresses.

        The value can be a particular
        email address, a hostname to indicate all email addresses on that host or
        a domain with a leading period (e.g. '.example.com') to indicate
        all email addresses in that domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_email_addresses PrivatecaCertificateTemplate#permitted_email_addresses}
        '''
        result = self._values.get("permitted_email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted IP ranges.

        For IPv4 addresses, the ranges
        are expressed using CIDR notation as specified in RFC 4632.
        For IPv6 addresses, the ranges are expressed in similar encoding as IPv4
        addresses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_ip_ranges PrivatecaCertificateTemplate#permitted_ip_ranges}
        '''
        result = self._values.get("permitted_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permitted_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Contains the permitted URIs that apply to the host part of the name.

        The value can be a hostname or a domain with a
        leading period (like '.example.com')

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_uris PrivatecaCertificateTemplate#permitted_uris}
        '''
        result = self._values.get("permitted_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesNameConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePredefinedValuesNameConstraintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesNameConstraintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eb4c8d6f2d460696345895e0ee2752b8bbdd641e5d0a7578aa7b4eddc43af14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludedDnsNames")
    def reset_excluded_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedDnsNames", []))

    @jsii.member(jsii_name="resetExcludedEmailAddresses")
    def reset_excluded_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedEmailAddresses", []))

    @jsii.member(jsii_name="resetExcludedIpRanges")
    def reset_excluded_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedIpRanges", []))

    @jsii.member(jsii_name="resetExcludedUris")
    def reset_excluded_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedUris", []))

    @jsii.member(jsii_name="resetPermittedDnsNames")
    def reset_permitted_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedDnsNames", []))

    @jsii.member(jsii_name="resetPermittedEmailAddresses")
    def reset_permitted_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedEmailAddresses", []))

    @jsii.member(jsii_name="resetPermittedIpRanges")
    def reset_permitted_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedIpRanges", []))

    @jsii.member(jsii_name="resetPermittedUris")
    def reset_permitted_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermittedUris", []))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNamesInput")
    def excluded_dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddressesInput")
    def excluded_email_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedEmailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedIpRangesInput")
    def excluded_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedUrisInput")
    def excluded_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNamesInput")
    def permitted_dns_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddressesInput")
    def permitted_email_addresses_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedEmailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedIpRangesInput")
    def permitted_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="permittedUrisInput")
    def permitted_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permittedUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "critical"))

    @critical.setter
    def critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31eb79abdf922f2ccc3f330348b2ebadb9508b7790e8da1f0f7d3410224303d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedDnsNames")
    def excluded_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedDnsNames"))

    @excluded_dns_names.setter
    def excluded_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8f24515fb1f1a5e437b913651a0cd58cd9f17438c8acaba4a54d8c65129ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedEmailAddresses")
    def excluded_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedEmailAddresses"))

    @excluded_email_addresses.setter
    def excluded_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42eaac1b07266b42ec4c453ea30383d6f35be1cd3fa17d18b12aeb05703a0cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedIpRanges")
    def excluded_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedIpRanges"))

    @excluded_ip_ranges.setter
    def excluded_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a62f3ece5701dca0b98712f73c61ec86a204669153540e61014ff29aa88e4cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedUris")
    def excluded_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedUris"))

    @excluded_uris.setter
    def excluded_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ed30fc01c14a0d99b03eab530697bb4c6aceb7637a5cfddc6f401bc014b4dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedDnsNames")
    def permitted_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedDnsNames"))

    @permitted_dns_names.setter
    def permitted_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d560a4ea0ccf9ddfc138147e7f35e6495b1e63a7012d96a91d411083da0545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedEmailAddresses")
    def permitted_email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedEmailAddresses"))

    @permitted_email_addresses.setter
    def permitted_email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323e53cb12a8a1d23d26b558fbfd7ee246fe28615ae24bbdeeb267a380e56544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedEmailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedIpRanges")
    def permitted_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedIpRanges"))

    @permitted_ip_ranges.setter
    def permitted_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda875466dcb98f3f2fd7ed6b5c10def091bfd3c1de5bad607e0b801ac4847c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedIpRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permittedUris")
    def permitted_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "permittedUris"))

    @permitted_uris.setter
    def permitted_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__074bdbc0fa403b7069c5d20e2ea843d1d1967080fe2f2f382ec004e941cdb45c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permittedUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesNameConstraints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesNameConstraints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8259e1914ac90eebeb4ee55ca4359756b410706039b4dbe625408710c57f1cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateTemplatePredefinedValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1aeb74bff67788482ab08e61908b495a5ca37a208b1fd3fd46dc53cfe8aad563)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdditionalExtensions")
    def put_additional_extensions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40620c8b8841bb3efab245a8557c5ca595692154e5afa49f7db4e7483f1379c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalExtensions", [value]))

    @jsii.member(jsii_name="putCaOptions")
    def put_ca_options(
        self,
        *,
        is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_issuer_path_length: typing.Optional[jsii.Number] = None,
        null_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param is_ca: Optional. Refers to the "CA" X.509 extension, which is a boolean value. When this value is true, the "CA" in Basic Constraints extension will be set to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#is_ca PrivatecaCertificateTemplate#is_ca}
        :param max_issuer_path_length: Optional. Refers to the "path length constraint" in Basic Constraints extension. For a CA certificate, this value describes the depth of subordinate CA certificates that are allowed. If this value is less than 0, the request will fail. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#max_issuer_path_length PrivatecaCertificateTemplate#max_issuer_path_length}
        :param null_ca: Optional. When true, the "CA" in Basic Constraints extension will be set to null and omitted from the CA certificate. If both 'is_ca' and 'null_ca' are unset, the "CA" in Basic Constraints extension will be set to false. Note that the behavior when 'is_ca = false' for this resource is different from the behavior in the Certificate Authority, Certificate and CaPool resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#null_ca PrivatecaCertificateTemplate#null_ca}
        :param zero_max_issuer_path_length: Optional. When true, the "path length constraint" in Basic Constraints extension will be set to 0. if both 'max_issuer_path_length' and 'zero_max_issuer_path_length' are unset, the max path length will be omitted from the CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#zero_max_issuer_path_length PrivatecaCertificateTemplate#zero_max_issuer_path_length}
        '''
        value = PrivatecaCertificateTemplatePredefinedValuesCaOptions(
            is_ca=is_ca,
            max_issuer_path_length=max_issuer_path_length,
            null_ca=null_ca,
            zero_max_issuer_path_length=zero_max_issuer_path_length,
        )

        return typing.cast(None, jsii.invoke(self, "putCaOptions", [value]))

    @jsii.member(jsii_name="putKeyUsage")
    def put_key_usage(
        self,
        *,
        base_key_usage: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]]] = None,
        extended_key_usage: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]]] = None,
        unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param base_key_usage: base_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#base_key_usage PrivatecaCertificateTemplate#base_key_usage}
        :param extended_key_usage: extended_key_usage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#extended_key_usage PrivatecaCertificateTemplate#extended_key_usage}
        :param unknown_extended_key_usages: unknown_extended_key_usages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#unknown_extended_key_usages PrivatecaCertificateTemplate#unknown_extended_key_usages}
        '''
        value = PrivatecaCertificateTemplatePredefinedValuesKeyUsage(
            base_key_usage=base_key_usage,
            extended_key_usage=extended_key_usage,
            unknown_extended_key_usages=unknown_extended_key_usages,
        )

        return typing.cast(None, jsii.invoke(self, "putKeyUsage", [value]))

    @jsii.member(jsii_name="putNameConstraints")
    def put_name_constraints(
        self,
        *,
        critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param critical: Indicates whether or not the name constraints are marked critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#critical PrivatecaCertificateTemplate#critical}
        :param excluded_dns_names: Contains excluded DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_dns_names PrivatecaCertificateTemplate#excluded_dns_names}
        :param excluded_email_addresses: Contains the excluded email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_email_addresses PrivatecaCertificateTemplate#excluded_email_addresses}
        :param excluded_ip_ranges: Contains the excluded IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_ip_ranges PrivatecaCertificateTemplate#excluded_ip_ranges}
        :param excluded_uris: Contains the excluded URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#excluded_uris PrivatecaCertificateTemplate#excluded_uris}
        :param permitted_dns_names: Contains permitted DNS names. Any DNS name that can be constructed by simply adding zero or more labels to the left-hand side of the name satisfies the name constraint. For example, 'example.com', 'www.example.com', 'www.sub.example.com' would satisfy 'example.com' while 'example1.com' does not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_dns_names PrivatecaCertificateTemplate#permitted_dns_names}
        :param permitted_email_addresses: Contains the permitted email addresses. The value can be a particular email address, a hostname to indicate all email addresses on that host or a domain with a leading period (e.g. '.example.com') to indicate all email addresses in that domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_email_addresses PrivatecaCertificateTemplate#permitted_email_addresses}
        :param permitted_ip_ranges: Contains the permitted IP ranges. For IPv4 addresses, the ranges are expressed using CIDR notation as specified in RFC 4632. For IPv6 addresses, the ranges are expressed in similar encoding as IPv4 addresses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_ip_ranges PrivatecaCertificateTemplate#permitted_ip_ranges}
        :param permitted_uris: Contains the permitted URIs that apply to the host part of the name. The value can be a hostname or a domain with a leading period (like '.example.com') Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#permitted_uris PrivatecaCertificateTemplate#permitted_uris}
        '''
        value = PrivatecaCertificateTemplatePredefinedValuesNameConstraints(
            critical=critical,
            excluded_dns_names=excluded_dns_names,
            excluded_email_addresses=excluded_email_addresses,
            excluded_ip_ranges=excluded_ip_ranges,
            excluded_uris=excluded_uris,
            permitted_dns_names=permitted_dns_names,
            permitted_email_addresses=permitted_email_addresses,
            permitted_ip_ranges=permitted_ip_ranges,
            permitted_uris=permitted_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putNameConstraints", [value]))

    @jsii.member(jsii_name="putPolicyIds")
    def put_policy_ids(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PrivatecaCertificateTemplatePredefinedValuesPolicyIds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7dfebc609c6cf08c068a315927e540b4e7bf7381059e6e1a625e3350be534cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyIds", [value]))

    @jsii.member(jsii_name="resetAdditionalExtensions")
    def reset_additional_extensions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalExtensions", []))

    @jsii.member(jsii_name="resetAiaOcspServers")
    def reset_aia_ocsp_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAiaOcspServers", []))

    @jsii.member(jsii_name="resetCaOptions")
    def reset_ca_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaOptions", []))

    @jsii.member(jsii_name="resetKeyUsage")
    def reset_key_usage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyUsage", []))

    @jsii.member(jsii_name="resetNameConstraints")
    def reset_name_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameConstraints", []))

    @jsii.member(jsii_name="resetPolicyIds")
    def reset_policy_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyIds", []))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensions")
    def additional_extensions(
        self,
    ) -> PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsList:
        return typing.cast(PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsList, jsii.get(self, "additionalExtensions"))

    @builtins.property
    @jsii.member(jsii_name="caOptions")
    def ca_options(
        self,
    ) -> PrivatecaCertificateTemplatePredefinedValuesCaOptionsOutputReference:
        return typing.cast(PrivatecaCertificateTemplatePredefinedValuesCaOptionsOutputReference, jsii.get(self, "caOptions"))

    @builtins.property
    @jsii.member(jsii_name="keyUsage")
    def key_usage(
        self,
    ) -> PrivatecaCertificateTemplatePredefinedValuesKeyUsageOutputReference:
        return typing.cast(PrivatecaCertificateTemplatePredefinedValuesKeyUsageOutputReference, jsii.get(self, "keyUsage"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraints")
    def name_constraints(
        self,
    ) -> PrivatecaCertificateTemplatePredefinedValuesNameConstraintsOutputReference:
        return typing.cast(PrivatecaCertificateTemplatePredefinedValuesNameConstraintsOutputReference, jsii.get(self, "nameConstraints"))

    @builtins.property
    @jsii.member(jsii_name="policyIds")
    def policy_ids(self) -> "PrivatecaCertificateTemplatePredefinedValuesPolicyIdsList":
        return typing.cast("PrivatecaCertificateTemplatePredefinedValuesPolicyIdsList", jsii.get(self, "policyIds"))

    @builtins.property
    @jsii.member(jsii_name="additionalExtensionsInput")
    def additional_extensions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]]], jsii.get(self, "additionalExtensionsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServersInput")
    def aia_ocsp_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aiaOcspServersInput"))

    @builtins.property
    @jsii.member(jsii_name="caOptionsInput")
    def ca_options_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesCaOptions]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesCaOptions], jsii.get(self, "caOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyUsageInput")
    def key_usage_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsage]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsage], jsii.get(self, "keyUsageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameConstraintsInput")
    def name_constraints_input(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValuesNameConstraints]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValuesNameConstraints], jsii.get(self, "nameConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdsInput")
    def policy_ids_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesPolicyIds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PrivatecaCertificateTemplatePredefinedValuesPolicyIds"]]], jsii.get(self, "policyIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="aiaOcspServers")
    def aia_ocsp_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aiaOcspServers"))

    @aia_ocsp_servers.setter
    def aia_ocsp_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049c0e12b8c28ddc42e4527fd6c70a51ab9cfd9fb6eb18645f9f1e8946dd133b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aiaOcspServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PrivatecaCertificateTemplatePredefinedValues]:
        return typing.cast(typing.Optional[PrivatecaCertificateTemplatePredefinedValues], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PrivatecaCertificateTemplatePredefinedValues],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80a7292088e6063431c0b895cc0d75d789bf498cc6f7fbac267c4e3e6e49d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesPolicyIds",
    jsii_struct_bases=[],
    name_mapping={"object_id_path": "objectIdPath"},
)
class PrivatecaCertificateTemplatePredefinedValuesPolicyIds:
    def __init__(self, *, object_id_path: typing.Sequence[jsii.Number]) -> None:
        '''
        :param object_id_path: Required. The parts of an OID path. The most significant parts of the path come first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44b31789aa06843d58ec190d8bfd9b05e3e6bbcabaac56c353455a7d820e9de)
            check_type(argname="argument object_id_path", value=object_id_path, expected_type=type_hints["object_id_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id_path": object_id_path,
        }

    @builtins.property
    def object_id_path(self) -> typing.List[jsii.Number]:
        '''Required. The parts of an OID path. The most significant parts of the path come first.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#object_id_path PrivatecaCertificateTemplate#object_id_path}
        '''
        result = self._values.get("object_id_path")
        assert result is not None, "Required property 'object_id_path' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplatePredefinedValuesPolicyIds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplatePredefinedValuesPolicyIdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesPolicyIdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d1c46969ef029017de98400e8796af7100e2e8a9b6816e6ee3f3cb6affe4734)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PrivatecaCertificateTemplatePredefinedValuesPolicyIdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad4a4cc866bbb08f9290d76873bfd73bb299c0f4ca715e134d8dc856d1fe2cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PrivatecaCertificateTemplatePredefinedValuesPolicyIdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978148413942dccaaae50d355053da16426bedcdcf50cb3e61e7f79b3f136d69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aefd565cff7f4c7bf6ab6d97ff33dc37b68b463307585c61af2dd47f5a82ca74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91d7c61224c36110c8fe6a1af1b36ede8acc558b4d33d7e3e97b4a7aeb0cddb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesPolicyIds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesPolicyIds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesPolicyIds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6a4ea32abca279ee49c18b71b328b375c3256bfdb763be7317f658aaf0578c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PrivatecaCertificateTemplatePredefinedValuesPolicyIdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplatePredefinedValuesPolicyIdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9efe709ff4309c6d19a660cac9e235025ed942f3e2efbb1ceb5f0c5b2981dccb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectIdPathInput")
    def object_id_path_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "objectIdPathInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdPath")
    def object_id_path(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "objectIdPath"))

    @object_id_path.setter
    def object_id_path(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e7f246a19524d5b8164e3f469e38949d35768e1f0a2164761241f532235273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectIdPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesPolicyIds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesPolicyIds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesPolicyIds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6fc94628cd080ba6e43364f837d30659a262930c03e2939745c3b0e90084e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class PrivatecaCertificateTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#create PrivatecaCertificateTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#delete PrivatecaCertificateTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#update PrivatecaCertificateTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83223bb77845b8f72ec69e77d510fb397dbdb37ec1067b393fc741da727cf308)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#create PrivatecaCertificateTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#delete PrivatecaCertificateTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/privateca_certificate_template#update PrivatecaCertificateTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivatecaCertificateTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrivatecaCertificateTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.privatecaCertificateTemplate.PrivatecaCertificateTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b3d824b17dd4edb0eef2314209b88da5fbdb1f1d87760eb59e76c277050f4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df6c26b2ae999c78087fb2631bb6b86f49fd0699fdf0bd8e401423d2383e7f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c1e047005692c6d54464d5caf7c9cf08c28ded8906b58b4aab4750f792000f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8006026c751efe8b2ee7446167811abb1172c708791a147978d529b5f52c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cb8249baea8907401dec5ba428b8208845bfeffe11bccfe6771f9fd78bf03f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PrivatecaCertificateTemplate",
    "PrivatecaCertificateTemplateConfig",
    "PrivatecaCertificateTemplateIdentityConstraints",
    "PrivatecaCertificateTemplateIdentityConstraintsCelExpression",
    "PrivatecaCertificateTemplateIdentityConstraintsCelExpressionOutputReference",
    "PrivatecaCertificateTemplateIdentityConstraintsOutputReference",
    "PrivatecaCertificateTemplatePassthroughExtensions",
    "PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions",
    "PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsList",
    "PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensionsOutputReference",
    "PrivatecaCertificateTemplatePassthroughExtensionsOutputReference",
    "PrivatecaCertificateTemplatePredefinedValues",
    "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions",
    "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsList",
    "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId",
    "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectIdOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesCaOptions",
    "PrivatecaCertificateTemplatePredefinedValuesCaOptionsOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsage",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsageOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsageOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsageOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesList",
    "PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsagesOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesNameConstraints",
    "PrivatecaCertificateTemplatePredefinedValuesNameConstraintsOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesOutputReference",
    "PrivatecaCertificateTemplatePredefinedValuesPolicyIds",
    "PrivatecaCertificateTemplatePredefinedValuesPolicyIdsList",
    "PrivatecaCertificateTemplatePredefinedValuesPolicyIdsOutputReference",
    "PrivatecaCertificateTemplateTimeouts",
    "PrivatecaCertificateTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__caafb7ad7113e498f1d8707e68f61ccc79b80631e245b780ffba7f630d7960dc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity_constraints: typing.Optional[typing.Union[PrivatecaCertificateTemplateIdentityConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maximum_lifetime: typing.Optional[builtins.str] = None,
    passthrough_extensions: typing.Optional[typing.Union[PrivatecaCertificateTemplatePassthroughExtensions, typing.Dict[builtins.str, typing.Any]]] = None,
    predefined_values: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValues, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[PrivatecaCertificateTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f1c3418c7bbb197a7fcbd0bfe8fb4b869b2fe1bc943ed69301cd199f11cf357c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88773560b1d9d364f49a52c6c91015b86af4c936d811074dc0a75a130ac3000b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabfe4ed6a67b2b0aec1fca3f109bd824ab56737decda7b56808ade1d14d11af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f154086853685004ae59d46d054a9f4edab205c8d9ca86b48e93c1ed4226329b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e907f979f9433cdad222495168762d2be75994b482716da11046111b84ecf554(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08cba57826a7d05fc53245ebe0100c3ef248a010ebc89270cd574c342b154beb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc2120af37c679785bd3abf69784e6fad74759e4dbf40d55b49b26a6cfdf812(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7193e3f9a46bd0490ec6b305c0a30bceb884556a698af1405f042c048cd520ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0b7e773f715961fff8e9d7c8b6f34d2c9a6019b059b0d2bf5211b57e43a4de(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    identity_constraints: typing.Optional[typing.Union[PrivatecaCertificateTemplateIdentityConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    maximum_lifetime: typing.Optional[builtins.str] = None,
    passthrough_extensions: typing.Optional[typing.Union[PrivatecaCertificateTemplatePassthroughExtensions, typing.Dict[builtins.str, typing.Any]]] = None,
    predefined_values: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValues, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[PrivatecaCertificateTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ea12e09f162782b3b919a19a054446ed3e5c89aaaa80bd279ec37198a2c0bf(
    *,
    allow_subject_alt_names_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    allow_subject_passthrough: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    cel_expression: typing.Optional[typing.Union[PrivatecaCertificateTemplateIdentityConstraintsCelExpression, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f65171773132ed02c0c623332f9a650adb3b967ccf6cf2ab6e6cbc1fee467c(
    *,
    description: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ee5e55ea5d93a9d9a20c970000beb2dc7905715b0d678570864790e889f2b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe93dd64b0b8e99b9ae31982fe87aa4dc4f9d7153f94e896be470124ebf58abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108b3953813051187aa44a7ffd974f3b1c34b19199e1da4b3903e1ef1f3a2769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359c230ff116bc141037fe8392d1bc62cab371b77d7647004961be18d264bfff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d78e5c1a28022a8fcc36e9943c9be44e6168dd182431d8297e85a6529d576e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92efb22990912b9f044c335f11a499193d2f9cc7eba7d85564a903b4652f774(
    value: typing.Optional[PrivatecaCertificateTemplateIdentityConstraintsCelExpression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd53bbaf40f28f38b0a1543d706d2e6b28896473a1edf1e610c1f3b164b3ede(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8552ee992ce7ade47f86d4c86d645f6233bb48f355f6b7ba4b761639d8b6693d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9536bd91a47029a6ddbe13411f3746f7a6dc2ad4ff4cdd6bd35fa4e1c48199a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a333a03dbc40b2e4029eccdfb08afd99ae4a68a93f785c0ad2b0a045bb9075(
    value: typing.Optional[PrivatecaCertificateTemplateIdentityConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2040856d9d45b08696cfd04168a44d78bc65194a5d57d34a2078e973f0885b7d(
    *,
    additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    known_extensions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c23cd0f3692f4832a9b0fa488d74dadb284338092d211f65a2228c0050408cb(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31856794374e45316c9874abe5ea975d852bdc35c76b3725c5a6cab94eb15a3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1b5a635417a30c99842341d93c8c5bcb597b3b448171d996deb8ba808362ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b37a99e5d9ad0efdebadb41c884481548172575975780178c38cf3b5ae8350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66acd6ebe8a8f71b34fbaaca8366fe7ff2b3d55377642a05423c27edf1355086(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5624bc3f8a82bb53c82294869dd9a529cabdb75721c2c9999f62ef1b5348359(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2dff7b1ec9138f7362fd9250b47112d777d04d218afd9fca6acabc89b8cf73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5815557eeb13e5c4b357c88f9e6e12890614d50d987c953bd60deb40453e158(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60042b5cf4f1332d5fae88c645c2a73077b77eb860702e623ae2e066e6621039(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538e936876d56d2fcdd7084c455f056c1a38c703495fb6ddc99decea6186d37a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94369883c0c526202a1fdb2e6faa5f00664ea60d94e3d068713124f346a2a877(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39a3498507e62b14408aead556ece6d6233d61fb1c19a49030188603a0e25ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePassthroughExtensionsAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b49b21bb5a6ddb341742a821b0fc034c81f6e420f1234f819f4d1194b241d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1568f7d8c1db7d06dc100faa7e3ca59c2c5df641b59f257bfcb4981bdea0984(
    value: typing.Optional[PrivatecaCertificateTemplatePassthroughExtensions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8175658194cbfc94e4abca87ea6414ec7d8f3700f2b798cdc8f6b7ff6f0a4fe3(
    *,
    additional_extensions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aia_ocsp_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ca_options: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValuesCaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    key_usage: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValuesKeyUsage, typing.Dict[builtins.str, typing.Any]]] = None,
    name_constraints: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValuesNameConstraints, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_ids: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePredefinedValuesPolicyIds, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6929a9c4c5d17afb71986fc7bfe577b2ba1a080f425ae1aece852d899e3e75d(
    *,
    object_id: typing.Union[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId, typing.Dict[builtins.str, typing.Any]],
    value: builtins.str,
    critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e463bf9dc9f6efbdbb487008c7f2cd3618dc75122fb3c423b7dfd243bfdb738f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37588689665cf6de2bb8cddb6ef49d03e6d80f20bb6373079744a3a51c49a981(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbc1708fbdc542c9bd5b42caacd2e453372d0979f7570923e573fcfb6dc429d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1339cd5b23041f89ec738306c4d7ea7cb526e7fcb41adc202206863d43154b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d665325bee7c063db91163bb34c8ab96ee86f57ca564c5c127e1e03dd027b5ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a217e1a1d8e5c42a01cf898b2975381d77f158f5623f9712b848ac7da6c75927(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbefc0da6768bda6b24809bea66a8e103ac23efa0de20aef2aa7e928c91fc359(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aec1a55af179b29bb54f80c0a54318d2d49ffeb152061edd82c47941695f2fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8c0c25484e692bb622f311c820b232760c1f9da1183d4b1fe4acdd51bb3712(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5d35db8464ce286c5738f10653188bdecfe3e67e4cabec4cd3e4f094085b64(
    value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensionsObjectId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16663201d03180576c2237df30d5a6c8b99f18d4ce7cc97033d9128e1b37c91b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cd1a8ad4f6591b5532cf05f177fc4f650f7baa480bfa34357e1b41498999cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfd20dd5020b52b180e7797635ae9cbfabc668bc7665f6a2ca6aa62e86e350f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c841023c388ae4790b44f7806a8215b252688d7122b873c571589a4895ad31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91663ea25b0e236cdfcf45d1563be0b5213f4cc5676510dd5e863e13720d8b71(
    *,
    is_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_issuer_path_length: typing.Optional[jsii.Number] = None,
    null_ca: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zero_max_issuer_path_length: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c691d68ab55c331446a515c9e100ca5b147ae101edea353ab17f7d4e1ac5f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4072c9c73689011d3fbdfcc5b928fa20ffca08955ef7fa1a531338e8ca610050(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6770a603fb1e7a811ebc74ec3394e180ffa7c3d5babda701edc539617a0a6c2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2592a7b66e168a4c8e55d319f9f16d2a0a5c3bcfec6422da375a4a1737a67ec9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92657c797cab029f17318f5911052584f6495239ac87e158099f7cda6afdccad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f6ceca2ade4e8afd32e881e53ac68f3e3dd1b7db4cf4af7b222e8367211ab7(
    value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesCaOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ab4e8a951110e7164f30562925046ad990a515425366dde391a6a81ebe4981(
    *,
    base_key_usage: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage, typing.Dict[builtins.str, typing.Any]]] = None,
    extended_key_usage: typing.Optional[typing.Union[PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage, typing.Dict[builtins.str, typing.Any]]] = None,
    unknown_extended_key_usages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2182d3369fdc879f949cdf7431415d619d787c17f4e9264a4f6b1966e53f1ef(
    *,
    cert_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    content_commitment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crl_sign: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    data_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    decipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    digital_signature: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encipher_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key_encipherment: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e9686589f50a1518d044f16529633ee1aa9eef5eeb601b5d6653118c22b984(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067589cba431c9b0d784b767b176043e2eeedd260bd8cf748dcfcd582a041b7e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe1e7dc3a37cb3e174491399a02964228c83d2bb6735a7a36fbb6e204772760e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4524375e03c0f99ce694f0e188db9623bb2fb302421c4371ba28e1484cc82960(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1b5fb726c172d86a3af08821dc3519d1d5d81ac6b0e8a55e53c57d899e4e36(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9876c0a1fc1816d81495967fef556397fa63fcad65eb524e7346b27f9bb591(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388b7c82f17ee7c9cf13056389d7c628cebcb4656c70bdfba48961f96159e4b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71da8f3df1fcc1c33ce7eeddf36c49cc41bbc1757cba290e32102a97d854797b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3347d759489f85f8aa939c18af0b528ee85d90e2db8d5ae828cabd0b2fd8b39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc8c63c30ce1b6f48fd768b25651ec095417f0c7f6d5f40c13be5617d329bb2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ede101ffbbfbe0d623cc33a1c4b665387d77ba065bbf21c79c5c4f2340ebf2(
    value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageBaseKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff67ecf1ff863391aea5a417804b8a91d79341fe040f9430f735dcf8a21feecf(
    *,
    client_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    code_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    email_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ocsp_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    server_auth: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    time_stamping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98984527a9bd368b5cd595860e3ce5a5789f1a3db8dfc95b1516cb88e8acf4cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e746dfa5dee48a391a75d838acf4b679d596bfb0fefca3c784822d9c2d080e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfec3db966eb6b8b5e8414a59b4ba70a860b38c898af3c1997dc8d707bba592(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816519bbc73db6148efa815f8874cde3bd4a5034dc41fa8e6b049d9221c91ce7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdadc70da9e345ceb6c045059ec95ae6c5edf79329c3a7b96f2bd10d35e5c0a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906d6c1a728b1bff2e2bbda36e6d7e0b77d6483c150cf0aa165d25e45a1ca501(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a117da6d9d1b7dd22f6ce2f66b7e31fb7a8af5231312de5ae0604cbd3ee9b987(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2b4af5d240b9d15e250fdf6b9ceb30c95a6459673408b864e7db3fc5a0587d(
    value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsageExtendedKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4944f1341b67b29fc0249bb8b8c9b7f2cd1ec1b70ffb7327f2c021806bc9a45b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5ceed319a9cb6cf8d4ec63380575cc1821c3e7d40315a650c7a4ab1902afc7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99001647f3ba85c2706d581d9c979f205a8dc735b2f2f365fe785c95d46da88(
    value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesKeyUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae675e8ce519d67ec30253043015637407a2c5c045eb6db98088473f0f22268(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81150b6d5693c4ca6b05ee6616cc69e1e24326903d04d9700de45b6aeab21278(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbaeaae9d1153fa3c677d713f31cd1d7c19e85f30d82def26c09ca25637ae67(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be82928dff365277d11453bcbd6418a8431965d386353ba2d28a83a3dc8831fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01ed51c0832eb289f1e614ac29c80848c5bb1b0fd41bf6e7747e81ebb9b70ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f38d7292f055640348ee02434f44053c3cdc539c7d1b78367d688cd3093099(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd2dc33fb093d2377da62e28c0d53bd0b6673a71517cbf737ec20419d4f0cd5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ec22b4809f910b4eaaf7df7c8c120546828301646716d05919103d756450b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca404958814495d7330c51c021d0ef7aca522693fc72631b27f0e8a090cad70(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2dcac53347b6f0a6d482aea8ab38408a3ee3076bdfeeaf8d3db0769e1b7a8d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesKeyUsageUnknownExtendedKeyUsages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1b39fdd4eb5f55a2c54488ff1f7096102b46e6736954e14771935691cdc4e8(
    *,
    critical: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    excluded_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    permitted_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb4c8d6f2d460696345895e0ee2752b8bbdd641e5d0a7578aa7b4eddc43af14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31eb79abdf922f2ccc3f330348b2ebadb9508b7790e8da1f0f7d3410224303d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8f24515fb1f1a5e437b913651a0cd58cd9f17438c8acaba4a54d8c65129ddd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42eaac1b07266b42ec4c453ea30383d6f35be1cd3fa17d18b12aeb05703a0cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62f3ece5701dca0b98712f73c61ec86a204669153540e61014ff29aa88e4cc9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ed30fc01c14a0d99b03eab530697bb4c6aceb7637a5cfddc6f401bc014b4dba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d560a4ea0ccf9ddfc138147e7f35e6495b1e63a7012d96a91d411083da0545(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323e53cb12a8a1d23d26b558fbfd7ee246fe28615ae24bbdeeb267a380e56544(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda875466dcb98f3f2fd7ed6b5c10def091bfd3c1de5bad607e0b801ac4847c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__074bdbc0fa403b7069c5d20e2ea843d1d1967080fe2f2f382ec004e941cdb45c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8259e1914ac90eebeb4ee55ca4359756b410706039b4dbe625408710c57f1cd3(
    value: typing.Optional[PrivatecaCertificateTemplatePredefinedValuesNameConstraints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aeb74bff67788482ab08e61908b495a5ca37a208b1fd3fd46dc53cfe8aad563(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40620c8b8841bb3efab245a8557c5ca595692154e5afa49f7db4e7483f1379c8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePredefinedValuesAdditionalExtensions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dfebc609c6cf08c068a315927e540b4e7bf7381059e6e1a625e3350be534cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PrivatecaCertificateTemplatePredefinedValuesPolicyIds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049c0e12b8c28ddc42e4527fd6c70a51ab9cfd9fb6eb18645f9f1e8946dd133b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80a7292088e6063431c0b895cc0d75d789bf498cc6f7fbac267c4e3e6e49d59(
    value: typing.Optional[PrivatecaCertificateTemplatePredefinedValues],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44b31789aa06843d58ec190d8bfd9b05e3e6bbcabaac56c353455a7d820e9de(
    *,
    object_id_path: typing.Sequence[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1c46969ef029017de98400e8796af7100e2e8a9b6816e6ee3f3cb6affe4734(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad4a4cc866bbb08f9290d76873bfd73bb299c0f4ca715e134d8dc856d1fe2cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978148413942dccaaae50d355053da16426bedcdcf50cb3e61e7f79b3f136d69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefd565cff7f4c7bf6ab6d97ff33dc37b68b463307585c61af2dd47f5a82ca74(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d7c61224c36110c8fe6a1af1b36ede8acc558b4d33d7e3e97b4a7aeb0cddb0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a4ea32abca279ee49c18b71b328b375c3256bfdb763be7317f658aaf0578c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PrivatecaCertificateTemplatePredefinedValuesPolicyIds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efe709ff4309c6d19a660cac9e235025ed942f3e2efbb1ceb5f0c5b2981dccb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e7f246a19524d5b8164e3f469e38949d35768e1f0a2164761241f532235273(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6fc94628cd080ba6e43364f837d30659a262930c03e2939745c3b0e90084e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplatePredefinedValuesPolicyIds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83223bb77845b8f72ec69e77d510fb397dbdb37ec1067b393fc741da727cf308(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b3d824b17dd4edb0eef2314209b88da5fbdb1f1d87760eb59e76c277050f4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6c26b2ae999c78087fb2631bb6b86f49fd0699fdf0bd8e401423d2383e7f1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c1e047005692c6d54464d5caf7c9cf08c28ded8906b58b4aab4750f792000f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8006026c751efe8b2ee7446167811abb1172c708791a147978d529b5f52c0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cb8249baea8907401dec5ba428b8208845bfeffe11bccfe6771f9fd78bf03f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PrivatecaCertificateTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
