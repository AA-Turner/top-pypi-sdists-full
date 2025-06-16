r'''
# `google_apigee_keystores_aliases_self_signed_cert`

Refer to the Terraform Registry for docs: [`google_apigee_keystores_aliases_self_signed_cert`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert).
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


class GoogleApigeeKeystoresAliasesSelfSignedCert(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCert",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert google_apigee_keystores_aliases_self_signed_cert}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        alias: builtins.str,
        environment: builtins.str,
        keystore: builtins.str,
        org_id: builtins.str,
        sig_alg: builtins.str,
        subject: typing.Union["GoogleApigeeKeystoresAliasesSelfSignedCertSubject", typing.Dict[builtins.str, typing.Any]],
        cert_validity_in_days: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        key_size: typing.Optional[builtins.str] = None,
        subject_alternative_dns_names: typing.Optional[typing.Union["GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert google_apigee_keystores_aliases_self_signed_cert} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias for the key/certificate pair. Values must match the regular expression [\\w\\s-.]{1,255}. This must be provided for all formats except selfsignedcert; self-signed certs may specify the alias in either this parameter or the JSON body. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#alias GoogleApigeeKeystoresAliasesSelfSignedCert#alias}
        :param environment: The Apigee environment name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#environment GoogleApigeeKeystoresAliasesSelfSignedCert#environment}
        :param keystore: The Apigee keystore name associated in an Apigee environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#keystore GoogleApigeeKeystoresAliasesSelfSignedCert#keystore}
        :param org_id: The Apigee Organization name associated with the Apigee environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org_id GoogleApigeeKeystoresAliasesSelfSignedCert#org_id}
        :param sig_alg: Signature algorithm to generate private key. Valid values are SHA512withRSA, SHA384withRSA, and SHA256withRSA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#sig_alg GoogleApigeeKeystoresAliasesSelfSignedCert#sig_alg}
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject GoogleApigeeKeystoresAliasesSelfSignedCert#subject}
        :param cert_validity_in_days: Validity duration of certificate, in days. Accepts positive non-zero value. Defaults to 365. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#cert_validity_in_days GoogleApigeeKeystoresAliasesSelfSignedCert#cert_validity_in_days}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#id GoogleApigeeKeystoresAliasesSelfSignedCert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_size: Key size. Default and maximum value is 2048 bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#key_size GoogleApigeeKeystoresAliasesSelfSignedCert#key_size}
        :param subject_alternative_dns_names: subject_alternative_dns_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject_alternative_dns_names GoogleApigeeKeystoresAliasesSelfSignedCert#subject_alternative_dns_names}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#timeouts GoogleApigeeKeystoresAliasesSelfSignedCert#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55959bf8a8c7dfd5c3a2204ebe98df24486e3587abed4bc4134eddcee6fd0024)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApigeeKeystoresAliasesSelfSignedCertConfig(
            alias=alias,
            environment=environment,
            keystore=keystore,
            org_id=org_id,
            sig_alg=sig_alg,
            subject=subject,
            cert_validity_in_days=cert_validity_in_days,
            id=id,
            key_size=key_size,
            subject_alternative_dns_names=subject_alternative_dns_names,
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
        '''Generates CDKTF code for importing a GoogleApigeeKeystoresAliasesSelfSignedCert resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApigeeKeystoresAliasesSelfSignedCert to import.
        :param import_from_id: The id of the existing GoogleApigeeKeystoresAliasesSelfSignedCert that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApigeeKeystoresAliasesSelfSignedCert to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43602ad339bdae388980cb0f9b5de6f2b1b177d5a5c9cb6539f667df24e5529d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSubject")
    def put_subject(
        self,
        *,
        common_name: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        org_unit: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: Common name of the organization. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#common_name GoogleApigeeKeystoresAliasesSelfSignedCert#common_name}
        :param country_code: Two-letter country code. Example, IN for India, US for United States of America. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#country_code GoogleApigeeKeystoresAliasesSelfSignedCert#country_code}
        :param email: Email address. Max 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#email GoogleApigeeKeystoresAliasesSelfSignedCert#email}
        :param locality: City or town name. Maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#locality GoogleApigeeKeystoresAliasesSelfSignedCert#locality}
        :param org: Organization name. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org GoogleApigeeKeystoresAliasesSelfSignedCert#org}
        :param org_unit: Organization team name. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org_unit GoogleApigeeKeystoresAliasesSelfSignedCert#org_unit}
        :param state: State or district name. Maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#state GoogleApigeeKeystoresAliasesSelfSignedCert#state}
        '''
        value = GoogleApigeeKeystoresAliasesSelfSignedCertSubject(
            common_name=common_name,
            country_code=country_code,
            email=email,
            locality=locality,
            org=org,
            org_unit=org_unit,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putSubject", [value]))

    @jsii.member(jsii_name="putSubjectAlternativeDnsNames")
    def put_subject_alternative_dns_names(
        self,
        *,
        subject_alternative_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subject_alternative_name: Subject Alternative Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject_alternative_name GoogleApigeeKeystoresAliasesSelfSignedCert#subject_alternative_name}
        '''
        value = GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames(
            subject_alternative_name=subject_alternative_name
        )

        return typing.cast(None, jsii.invoke(self, "putSubjectAlternativeDnsNames", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#create GoogleApigeeKeystoresAliasesSelfSignedCert#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#delete GoogleApigeeKeystoresAliasesSelfSignedCert#delete}.
        '''
        value = GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts(
            create=create, delete=delete
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCertValidityInDays")
    def reset_cert_validity_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertValidityInDays", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeySize")
    def reset_key_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeySize", []))

    @jsii.member(jsii_name="resetSubjectAlternativeDnsNames")
    def reset_subject_alternative_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAlternativeDnsNames", []))

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
    @jsii.member(jsii_name="certsInfo")
    def certs_info(self) -> "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoList":
        return typing.cast("GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoList", jsii.get(self, "certsInfo"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(
        self,
    ) -> "GoogleApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference":
        return typing.cast("GoogleApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference", jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeDnsNames")
    def subject_alternative_dns_names(
        self,
    ) -> "GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference":
        return typing.cast("GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference", jsii.get(self, "subjectAlternativeDnsNames"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference":
        return typing.cast("GoogleApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="certValidityInDaysInput")
    def cert_validity_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "certValidityInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keySizeInput")
    def key_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keySizeInput"))

    @builtins.property
    @jsii.member(jsii_name="keystoreInput")
    def keystore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keystoreInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sigAlgInput")
    def sig_alg_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sigAlgInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeDnsNamesInput")
    def subject_alternative_dns_names_input(
        self,
    ) -> typing.Optional["GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames"]:
        return typing.cast(typing.Optional["GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames"], jsii.get(self, "subjectAlternativeDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(
        self,
    ) -> typing.Optional["GoogleApigeeKeystoresAliasesSelfSignedCertSubject"]:
        return typing.cast(typing.Optional["GoogleApigeeKeystoresAliasesSelfSignedCertSubject"], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d8288c268788aef42c7d3a47a4ff899c6f16c60ec5656e068f46a8de577aae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certValidityInDays")
    def cert_validity_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "certValidityInDays"))

    @cert_validity_in_days.setter
    def cert_validity_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f7f98862768863ae68e63b8a722eb35262a59ec9bbdc2e7fb9881089de19ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certValidityInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c608c99f2c31c7510a52625ca1e12336d43491d9f44ccbb44637aa3f060adfb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2262a5c07894574ad000bb38a9f19eecfdfc9a061a4d2771259549ff3b4f8c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keySize")
    def key_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keySize"))

    @key_size.setter
    def key_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd445b4b9c70821fb3afb4d77ee90e4e38971342e79f0b11ac50644d57a63cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keySize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keystore")
    def keystore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystore"))

    @keystore.setter
    def keystore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9c027e843c74863e1f9d06f2b0d26de8d459e876f429b2e0780d3b0e9070db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4df9a46208b46cf5c04ed0255c3ee94a801a5993cb6d303fd44af4d50cae0eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sigAlg")
    def sig_alg(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sigAlg"))

    @sig_alg.setter
    def sig_alg(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac4464fb0eeb1673d0422c375349413e224dbad85f7ac723c6389f1ab441328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sigAlg", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd185c56af516160dfd3c31a22889646543784beda1a0c31201ea41d5fe8ae0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6caa2710e1e4d29612b1c18c6b963da1ddce9e5a1a8cbfe0277727f608e275fe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd086cff290c9412fb968c40dfebb24639e79b50eec959d47bd9db1ddf5d07dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__062f3f4cd4e3fc893e704856b3c5198e3c1d33aec8e34b68c7d1ea32b04466b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__404d7277dbdb2f82714e514acf5d938613116f71e35de11ce82f840aad4a2e55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64f3dfd1bad52013c2eb2917aaf1f6633b2ec9087b11a0dc75e0c6bd1e22c4fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="basicConstraints")
    def basic_constraints(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basicConstraints"))

    @builtins.property
    @jsii.member(jsii_name="expiryDate")
    def expiry_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiryDate"))

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @builtins.property
    @jsii.member(jsii_name="isValid")
    def is_valid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isValid"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @builtins.property
    @jsii.member(jsii_name="sigAlgName")
    def sig_alg_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sigAlgName"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subjectAlternativeNames"))

    @builtins.property
    @jsii.member(jsii_name="validFrom")
    def valid_from(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validFrom"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo]:
        return typing.cast(typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2b04e59c80edccbb1be9f788d2b37bfc08a5d8406cdfe5ab99afe179982003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9461d9d95534c90fb64546914cd31c76200d76c652ded9f534c40876e0ff35e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75666744659664a3497d3d846460ed07b8e6ac837fb42b85a46c9ceed03e77c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7712ae823aaa3bc27cd1114a8067c339cc834e3d7cebc3eb76c40f845e1c8b25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e090cc0cb9c628db3e764d292977e1099909924a6a59d9058cd6aa27c169b758)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ec6a2ca0e791f0f1ab371e132c091c4132715b7874de0deab0cc34f716864d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45e74adc58925027da120afec7ca2cead442184883e2129848d9afd7fdfd9c52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certInfo")
    def cert_info(
        self,
    ) -> GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList:
        return typing.cast(GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList, jsii.get(self, "certInfo"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfo]:
        return typing.cast(typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cc0332521b216e6618b92e75c112e2f0e8c482d8d548346514eb274c115537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "alias": "alias",
        "environment": "environment",
        "keystore": "keystore",
        "org_id": "orgId",
        "sig_alg": "sigAlg",
        "subject": "subject",
        "cert_validity_in_days": "certValidityInDays",
        "id": "id",
        "key_size": "keySize",
        "subject_alternative_dns_names": "subjectAlternativeDnsNames",
        "timeouts": "timeouts",
    },
)
class GoogleApigeeKeystoresAliasesSelfSignedCertConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        alias: builtins.str,
        environment: builtins.str,
        keystore: builtins.str,
        org_id: builtins.str,
        sig_alg: builtins.str,
        subject: typing.Union["GoogleApigeeKeystoresAliasesSelfSignedCertSubject", typing.Dict[builtins.str, typing.Any]],
        cert_validity_in_days: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        key_size: typing.Optional[builtins.str] = None,
        subject_alternative_dns_names: typing.Optional[typing.Union["GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param alias: Alias for the key/certificate pair. Values must match the regular expression [\\w\\s-.]{1,255}. This must be provided for all formats except selfsignedcert; self-signed certs may specify the alias in either this parameter or the JSON body. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#alias GoogleApigeeKeystoresAliasesSelfSignedCert#alias}
        :param environment: The Apigee environment name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#environment GoogleApigeeKeystoresAliasesSelfSignedCert#environment}
        :param keystore: The Apigee keystore name associated in an Apigee environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#keystore GoogleApigeeKeystoresAliasesSelfSignedCert#keystore}
        :param org_id: The Apigee Organization name associated with the Apigee environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org_id GoogleApigeeKeystoresAliasesSelfSignedCert#org_id}
        :param sig_alg: Signature algorithm to generate private key. Valid values are SHA512withRSA, SHA384withRSA, and SHA256withRSA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#sig_alg GoogleApigeeKeystoresAliasesSelfSignedCert#sig_alg}
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject GoogleApigeeKeystoresAliasesSelfSignedCert#subject}
        :param cert_validity_in_days: Validity duration of certificate, in days. Accepts positive non-zero value. Defaults to 365. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#cert_validity_in_days GoogleApigeeKeystoresAliasesSelfSignedCert#cert_validity_in_days}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#id GoogleApigeeKeystoresAliasesSelfSignedCert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_size: Key size. Default and maximum value is 2048 bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#key_size GoogleApigeeKeystoresAliasesSelfSignedCert#key_size}
        :param subject_alternative_dns_names: subject_alternative_dns_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject_alternative_dns_names GoogleApigeeKeystoresAliasesSelfSignedCert#subject_alternative_dns_names}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#timeouts GoogleApigeeKeystoresAliasesSelfSignedCert#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(subject, dict):
            subject = GoogleApigeeKeystoresAliasesSelfSignedCertSubject(**subject)
        if isinstance(subject_alternative_dns_names, dict):
            subject_alternative_dns_names = GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames(**subject_alternative_dns_names)
        if isinstance(timeouts, dict):
            timeouts = GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54237a1e32c64c6141d420895f0f18f70726dc57e5482c3f7ea91b52b5a95f7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument keystore", value=keystore, expected_type=type_hints["keystore"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument sig_alg", value=sig_alg, expected_type=type_hints["sig_alg"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument cert_validity_in_days", value=cert_validity_in_days, expected_type=type_hints["cert_validity_in_days"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_size", value=key_size, expected_type=type_hints["key_size"])
            check_type(argname="argument subject_alternative_dns_names", value=subject_alternative_dns_names, expected_type=type_hints["subject_alternative_dns_names"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias": alias,
            "environment": environment,
            "keystore": keystore,
            "org_id": org_id,
            "sig_alg": sig_alg,
            "subject": subject,
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
        if cert_validity_in_days is not None:
            self._values["cert_validity_in_days"] = cert_validity_in_days
        if id is not None:
            self._values["id"] = id
        if key_size is not None:
            self._values["key_size"] = key_size
        if subject_alternative_dns_names is not None:
            self._values["subject_alternative_dns_names"] = subject_alternative_dns_names
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
    def alias(self) -> builtins.str:
        '''Alias for the key/certificate pair.

        Values must match the regular expression [\\w\\s-.]{1,255}.
        This must be provided for all formats except selfsignedcert; self-signed certs may specify the alias in either
        this parameter or the JSON body.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#alias GoogleApigeeKeystoresAliasesSelfSignedCert#alias}
        '''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(self) -> builtins.str:
        '''The Apigee environment name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#environment GoogleApigeeKeystoresAliasesSelfSignedCert#environment}
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keystore(self) -> builtins.str:
        '''The Apigee keystore name associated in an Apigee environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#keystore GoogleApigeeKeystoresAliasesSelfSignedCert#keystore}
        '''
        result = self._values.get("keystore")
        assert result is not None, "Required property 'keystore' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The Apigee Organization name associated with the Apigee environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org_id GoogleApigeeKeystoresAliasesSelfSignedCert#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sig_alg(self) -> builtins.str:
        '''Signature algorithm to generate private key. Valid values are SHA512withRSA, SHA384withRSA, and SHA256withRSA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#sig_alg GoogleApigeeKeystoresAliasesSelfSignedCert#sig_alg}
        '''
        result = self._values.get("sig_alg")
        assert result is not None, "Required property 'sig_alg' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> "GoogleApigeeKeystoresAliasesSelfSignedCertSubject":
        '''subject block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject GoogleApigeeKeystoresAliasesSelfSignedCert#subject}
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast("GoogleApigeeKeystoresAliasesSelfSignedCertSubject", result)

    @builtins.property
    def cert_validity_in_days(self) -> typing.Optional[jsii.Number]:
        '''Validity duration of certificate, in days. Accepts positive non-zero value. Defaults to 365.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#cert_validity_in_days GoogleApigeeKeystoresAliasesSelfSignedCert#cert_validity_in_days}
        '''
        result = self._values.get("cert_validity_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#id GoogleApigeeKeystoresAliasesSelfSignedCert#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_size(self) -> typing.Optional[builtins.str]:
        '''Key size. Default and maximum value is 2048 bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#key_size GoogleApigeeKeystoresAliasesSelfSignedCert#key_size}
        '''
        result = self._values.get("key_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alternative_dns_names(
        self,
    ) -> typing.Optional["GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames"]:
        '''subject_alternative_dns_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject_alternative_dns_names GoogleApigeeKeystoresAliasesSelfSignedCert#subject_alternative_dns_names}
        '''
        result = self._values.get("subject_alternative_dns_names")
        return typing.cast(typing.Optional["GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#timeouts GoogleApigeeKeystoresAliasesSelfSignedCert#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesSelfSignedCertConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertSubject",
    jsii_struct_bases=[],
    name_mapping={
        "common_name": "commonName",
        "country_code": "countryCode",
        "email": "email",
        "locality": "locality",
        "org": "org",
        "org_unit": "orgUnit",
        "state": "state",
    },
)
class GoogleApigeeKeystoresAliasesSelfSignedCertSubject:
    def __init__(
        self,
        *,
        common_name: typing.Optional[builtins.str] = None,
        country_code: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        locality: typing.Optional[builtins.str] = None,
        org: typing.Optional[builtins.str] = None,
        org_unit: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param common_name: Common name of the organization. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#common_name GoogleApigeeKeystoresAliasesSelfSignedCert#common_name}
        :param country_code: Two-letter country code. Example, IN for India, US for United States of America. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#country_code GoogleApigeeKeystoresAliasesSelfSignedCert#country_code}
        :param email: Email address. Max 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#email GoogleApigeeKeystoresAliasesSelfSignedCert#email}
        :param locality: City or town name. Maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#locality GoogleApigeeKeystoresAliasesSelfSignedCert#locality}
        :param org: Organization name. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org GoogleApigeeKeystoresAliasesSelfSignedCert#org}
        :param org_unit: Organization team name. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org_unit GoogleApigeeKeystoresAliasesSelfSignedCert#org_unit}
        :param state: State or district name. Maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#state GoogleApigeeKeystoresAliasesSelfSignedCert#state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fab836dd2baaed5082bc1785a12134e5002d02b7e0d379969e75162ecc8e08)
            check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
            check_type(argname="argument org", value=org, expected_type=type_hints["org"])
            check_type(argname="argument org_unit", value=org_unit, expected_type=type_hints["org_unit"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if common_name is not None:
            self._values["common_name"] = common_name
        if country_code is not None:
            self._values["country_code"] = country_code
        if email is not None:
            self._values["email"] = email
        if locality is not None:
            self._values["locality"] = locality
        if org is not None:
            self._values["org"] = org
        if org_unit is not None:
            self._values["org_unit"] = org_unit
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def common_name(self) -> typing.Optional[builtins.str]:
        '''Common name of the organization. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#common_name GoogleApigeeKeystoresAliasesSelfSignedCert#common_name}
        '''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''Two-letter country code. Example, IN for India, US for United States of America.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#country_code GoogleApigeeKeystoresAliasesSelfSignedCert#country_code}
        '''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email address. Max 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#email GoogleApigeeKeystoresAliasesSelfSignedCert#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''City or town name. Maximum length is 128 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#locality GoogleApigeeKeystoresAliasesSelfSignedCert#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''Organization name. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org GoogleApigeeKeystoresAliasesSelfSignedCert#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org_unit(self) -> typing.Optional[builtins.str]:
        '''Organization team name. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#org_unit GoogleApigeeKeystoresAliasesSelfSignedCert#org_unit}
        '''
        result = self._values.get("org_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''State or district name. Maximum length is 128 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#state GoogleApigeeKeystoresAliasesSelfSignedCert#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesSelfSignedCertSubject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames",
    jsii_struct_bases=[],
    name_mapping={"subject_alternative_name": "subjectAlternativeName"},
)
class GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames:
    def __init__(
        self,
        *,
        subject_alternative_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subject_alternative_name: Subject Alternative Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject_alternative_name GoogleApigeeKeystoresAliasesSelfSignedCert#subject_alternative_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492652ec26327d9db4cb300e53c2cef358a98f31402b76eafe7fd85277525093)
            check_type(argname="argument subject_alternative_name", value=subject_alternative_name, expected_type=type_hints["subject_alternative_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if subject_alternative_name is not None:
            self._values["subject_alternative_name"] = subject_alternative_name

    @builtins.property
    def subject_alternative_name(self) -> typing.Optional[builtins.str]:
        '''Subject Alternative Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#subject_alternative_name GoogleApigeeKeystoresAliasesSelfSignedCert#subject_alternative_name}
        '''
        result = self._values.get("subject_alternative_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b34a191efd437324bcebd0036ab87d40e47943084227f402c81ec42350923b40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSubjectAlternativeName")
    def reset_subject_alternative_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAlternativeName", []))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNameInput")
    def subject_alternative_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectAlternativeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeName")
    def subject_alternative_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subjectAlternativeName"))

    @subject_alternative_name.setter
    def subject_alternative_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7f21b08ea85d6d287c952981ad8916384cf1218f083f374c7929ea3f555d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectAlternativeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames]:
        return typing.cast(typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492bb71c9de0b143ff0a4985fb20a8a8ba582bf7ed552883ba52790a2d405c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e287a8fb8eb63e1815e39780b2c6d25ee57957ccc53caa71368c849851cdafe5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCommonName")
    def reset_common_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommonName", []))

    @jsii.member(jsii_name="resetCountryCode")
    def reset_country_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCountryCode", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetLocality")
    def reset_locality(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocality", []))

    @jsii.member(jsii_name="resetOrg")
    def reset_org(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrg", []))

    @jsii.member(jsii_name="resetOrgUnit")
    def reset_org_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgUnit", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="commonNameInput")
    def common_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commonNameInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="localityInput")
    def locality_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localityInput"))

    @builtins.property
    @jsii.member(jsii_name="orgInput")
    def org_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgInput"))

    @builtins.property
    @jsii.member(jsii_name="orgUnitInput")
    def org_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="commonName")
    def common_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "commonName"))

    @common_name.setter
    def common_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f68f7cdd30b162674ed7e7150d7a0f42d9db24e7836ff77b8502cd2550e844c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de55f392ad99358aa68789055ba0b5c5beb37d526092a15abea5079247ed5db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db521b5bb883394db92ae3e7fb9a831382b90c63f9ac5df37b1de5796cb9fe4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490e18a0d9df1065a4dbcccecebc8d9dd26619d7169631fc5aef4c48344dcad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c499c60a578fc325ca91a3a9077ce1c94e0f31f18ae2ea88ae6b8c4a3d87640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgUnit")
    def org_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgUnit"))

    @org_unit.setter
    def org_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2b341e75154913a3e5c487718ae2d42b706d755d67e7ab8e7ed8d0fdaa6c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fef59f9782472fec0721b4e6e8f582537589c09a8bddfaaf30e3d7dec4ada507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertSubject]:
        return typing.cast(typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertSubject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertSubject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d66d848fe94e559d73647242ab533c0a26588feced01a7d766069026536007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#create GoogleApigeeKeystoresAliasesSelfSignedCert#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#delete GoogleApigeeKeystoresAliasesSelfSignedCert#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d47bad486347ca57adeae5029cb4f0dca33bf0127f4a678224cc613c40bca2)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#create GoogleApigeeKeystoresAliasesSelfSignedCert#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_self_signed_cert#delete GoogleApigeeKeystoresAliasesSelfSignedCert#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesSelfSignedCert.GoogleApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8214402a9f9914d2c64fc65c6e152604b95bad09a842b32565fd1156d5ed7fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9fc4aec0ee0e2603eb0a75614c48ac6003a75c107cf2e8bc637f4d28f1019f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4198b12b62c4682e6753e6f328c160d689b0506db8bae7e9a7f90a3b96e5d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9ab34bf9e1f992b6a99737df49ecb2bbad1b641e98a400f434ccc029f10ef41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApigeeKeystoresAliasesSelfSignedCert",
    "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfo",
    "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo",
    "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList",
    "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference",
    "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoList",
    "GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference",
    "GoogleApigeeKeystoresAliasesSelfSignedCertConfig",
    "GoogleApigeeKeystoresAliasesSelfSignedCertSubject",
    "GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames",
    "GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference",
    "GoogleApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference",
    "GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts",
    "GoogleApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__55959bf8a8c7dfd5c3a2204ebe98df24486e3587abed4bc4134eddcee6fd0024(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    alias: builtins.str,
    environment: builtins.str,
    keystore: builtins.str,
    org_id: builtins.str,
    sig_alg: builtins.str,
    subject: typing.Union[GoogleApigeeKeystoresAliasesSelfSignedCertSubject, typing.Dict[builtins.str, typing.Any]],
    cert_validity_in_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    key_size: typing.Optional[builtins.str] = None,
    subject_alternative_dns_names: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__43602ad339bdae388980cb0f9b5de6f2b1b177d5a5c9cb6539f667df24e5529d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d8288c268788aef42c7d3a47a4ff899c6f16c60ec5656e068f46a8de577aae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7f98862768863ae68e63b8a722eb35262a59ec9bbdc2e7fb9881089de19ab7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c608c99f2c31c7510a52625ca1e12336d43491d9f44ccbb44637aa3f060adfb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2262a5c07894574ad000bb38a9f19eecfdfc9a061a4d2771259549ff3b4f8c73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd445b4b9c70821fb3afb4d77ee90e4e38971342e79f0b11ac50644d57a63cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c027e843c74863e1f9d06f2b0d26de8d459e876f429b2e0780d3b0e9070db2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4df9a46208b46cf5c04ed0255c3ee94a801a5993cb6d303fd44af4d50cae0eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac4464fb0eeb1673d0422c375349413e224dbad85f7ac723c6389f1ab441328(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd185c56af516160dfd3c31a22889646543784beda1a0c31201ea41d5fe8ae0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6caa2710e1e4d29612b1c18c6b963da1ddce9e5a1a8cbfe0277727f608e275fe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd086cff290c9412fb968c40dfebb24639e79b50eec959d47bd9db1ddf5d07dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062f3f4cd4e3fc893e704856b3c5198e3c1d33aec8e34b68c7d1ea32b04466b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404d7277dbdb2f82714e514acf5d938613116f71e35de11ce82f840aad4a2e55(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64f3dfd1bad52013c2eb2917aaf1f6633b2ec9087b11a0dc75e0c6bd1e22c4fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2b04e59c80edccbb1be9f788d2b37bfc08a5d8406cdfe5ab99afe179982003(
    value: typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9461d9d95534c90fb64546914cd31c76200d76c652ded9f534c40876e0ff35e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75666744659664a3497d3d846460ed07b8e6ac837fb42b85a46c9ceed03e77c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7712ae823aaa3bc27cd1114a8067c339cc834e3d7cebc3eb76c40f845e1c8b25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e090cc0cb9c628db3e764d292977e1099909924a6a59d9058cd6aa27c169b758(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec6a2ca0e791f0f1ab371e132c091c4132715b7874de0deab0cc34f716864d6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45e74adc58925027da120afec7ca2cead442184883e2129848d9afd7fdfd9c52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cc0332521b216e6618b92e75c112e2f0e8c482d8d548346514eb274c115537(
    value: typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertCertsInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54237a1e32c64c6141d420895f0f18f70726dc57e5482c3f7ea91b52b5a95f7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alias: builtins.str,
    environment: builtins.str,
    keystore: builtins.str,
    org_id: builtins.str,
    sig_alg: builtins.str,
    subject: typing.Union[GoogleApigeeKeystoresAliasesSelfSignedCertSubject, typing.Dict[builtins.str, typing.Any]],
    cert_validity_in_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    key_size: typing.Optional[builtins.str] = None,
    subject_alternative_dns_names: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fab836dd2baaed5082bc1785a12134e5002d02b7e0d379969e75162ecc8e08(
    *,
    common_name: typing.Optional[builtins.str] = None,
    country_code: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    org: typing.Optional[builtins.str] = None,
    org_unit: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492652ec26327d9db4cb300e53c2cef358a98f31402b76eafe7fd85277525093(
    *,
    subject_alternative_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34a191efd437324bcebd0036ab87d40e47943084227f402c81ec42350923b40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7f21b08ea85d6d287c952981ad8916384cf1218f083f374c7929ea3f555d64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492bb71c9de0b143ff0a4985fb20a8a8ba582bf7ed552883ba52790a2d405c4b(
    value: typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e287a8fb8eb63e1815e39780b2c6d25ee57957ccc53caa71368c849851cdafe5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f68f7cdd30b162674ed7e7150d7a0f42d9db24e7836ff77b8502cd2550e844c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de55f392ad99358aa68789055ba0b5c5beb37d526092a15abea5079247ed5db6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db521b5bb883394db92ae3e7fb9a831382b90c63f9ac5df37b1de5796cb9fe4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490e18a0d9df1065a4dbcccecebc8d9dd26619d7169631fc5aef4c48344dcad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c499c60a578fc325ca91a3a9077ce1c94e0f31f18ae2ea88ae6b8c4a3d87640(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2b341e75154913a3e5c487718ae2d42b706d755d67e7ab8e7ed8d0fdaa6c10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fef59f9782472fec0721b4e6e8f582537589c09a8bddfaaf30e3d7dec4ada507(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d66d848fe94e559d73647242ab533c0a26588feced01a7d766069026536007(
    value: typing.Optional[GoogleApigeeKeystoresAliasesSelfSignedCertSubject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d47bad486347ca57adeae5029cb4f0dca33bf0127f4a678224cc613c40bca2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8214402a9f9914d2c64fc65c6e152604b95bad09a842b32565fd1156d5ed7fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9fc4aec0ee0e2603eb0a75614c48ac6003a75c107cf2e8bc637f4d28f1019f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4198b12b62c4682e6753e6f328c160d689b0506db8bae7e9a7f90a3b96e5d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ab34bf9e1f992b6a99737df49ecb2bbad1b641e98a400f434ccc029f10ef41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesSelfSignedCertTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
