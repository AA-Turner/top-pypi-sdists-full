r'''
# `google_apigee_keystores_aliases_self_signed_cert`

Refer to the Terraform Registry for docs: [`google_apigee_keystores_aliases_self_signed_cert`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert).
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


class ApigeeKeystoresAliasesSelfSignedCert(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCert",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert google_apigee_keystores_aliases_self_signed_cert}.'''

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
        subject: typing.Union["ApigeeKeystoresAliasesSelfSignedCertSubject", typing.Dict[builtins.str, typing.Any]],
        cert_validity_in_days: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        key_size: typing.Optional[builtins.str] = None,
        subject_alternative_dns_names: typing.Optional[typing.Union["ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApigeeKeystoresAliasesSelfSignedCertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert google_apigee_keystores_aliases_self_signed_cert} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias for the key/certificate pair. Values must match the regular expression [\\w\\s-.]{1,255}. This must be provided for all formats except selfsignedcert; self-signed certs may specify the alias in either this parameter or the JSON body. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#alias ApigeeKeystoresAliasesSelfSignedCert#alias}
        :param environment: The Apigee environment name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#environment ApigeeKeystoresAliasesSelfSignedCert#environment}
        :param keystore: The Apigee keystore name associated in an Apigee environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#keystore ApigeeKeystoresAliasesSelfSignedCert#keystore}
        :param org_id: The Apigee Organization name associated with the Apigee environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org_id ApigeeKeystoresAliasesSelfSignedCert#org_id}
        :param sig_alg: Signature algorithm to generate private key. Valid values are SHA512withRSA, SHA384withRSA, and SHA256withRSA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#sig_alg ApigeeKeystoresAliasesSelfSignedCert#sig_alg}
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject ApigeeKeystoresAliasesSelfSignedCert#subject}
        :param cert_validity_in_days: Validity duration of certificate, in days. Accepts positive non-zero value. Defaults to 365. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#cert_validity_in_days ApigeeKeystoresAliasesSelfSignedCert#cert_validity_in_days}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#id ApigeeKeystoresAliasesSelfSignedCert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_size: Key size. Default and maximum value is 2048 bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#key_size ApigeeKeystoresAliasesSelfSignedCert#key_size}
        :param subject_alternative_dns_names: subject_alternative_dns_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject_alternative_dns_names ApigeeKeystoresAliasesSelfSignedCert#subject_alternative_dns_names}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#timeouts ApigeeKeystoresAliasesSelfSignedCert#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bf09125f4a5bd5e2a3eb58d7b14a3b1ca0f805b7e43c5e53c52cef66db014c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigeeKeystoresAliasesSelfSignedCertConfig(
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
        '''Generates CDKTF code for importing a ApigeeKeystoresAliasesSelfSignedCert resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigeeKeystoresAliasesSelfSignedCert to import.
        :param import_from_id: The id of the existing ApigeeKeystoresAliasesSelfSignedCert that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigeeKeystoresAliasesSelfSignedCert to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a06ac16b0a5b584297dc55a74f29fc881169b8a51ac0dabf52ad510ec1d4b4)
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
        :param common_name: Common name of the organization. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#common_name ApigeeKeystoresAliasesSelfSignedCert#common_name}
        :param country_code: Two-letter country code. Example, IN for India, US for United States of America. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#country_code ApigeeKeystoresAliasesSelfSignedCert#country_code}
        :param email: Email address. Max 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#email ApigeeKeystoresAliasesSelfSignedCert#email}
        :param locality: City or town name. Maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#locality ApigeeKeystoresAliasesSelfSignedCert#locality}
        :param org: Organization name. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org ApigeeKeystoresAliasesSelfSignedCert#org}
        :param org_unit: Organization team name. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org_unit ApigeeKeystoresAliasesSelfSignedCert#org_unit}
        :param state: State or district name. Maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#state ApigeeKeystoresAliasesSelfSignedCert#state}
        '''
        value = ApigeeKeystoresAliasesSelfSignedCertSubject(
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
        :param subject_alternative_name: Subject Alternative Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject_alternative_name ApigeeKeystoresAliasesSelfSignedCert#subject_alternative_name}
        '''
        value = ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#create ApigeeKeystoresAliasesSelfSignedCert#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#delete ApigeeKeystoresAliasesSelfSignedCert#delete}.
        '''
        value = ApigeeKeystoresAliasesSelfSignedCertTimeouts(
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
    def certs_info(self) -> "ApigeeKeystoresAliasesSelfSignedCertCertsInfoList":
        return typing.cast("ApigeeKeystoresAliasesSelfSignedCertCertsInfoList", jsii.get(self, "certsInfo"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> "ApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference":
        return typing.cast("ApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference", jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeDnsNames")
    def subject_alternative_dns_names(
        self,
    ) -> "ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference":
        return typing.cast("ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference", jsii.get(self, "subjectAlternativeDnsNames"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference":
        return typing.cast("ApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames"]:
        return typing.cast(typing.Optional["ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames"], jsii.get(self, "subjectAlternativeDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(
        self,
    ) -> typing.Optional["ApigeeKeystoresAliasesSelfSignedCertSubject"]:
        return typing.cast(typing.Optional["ApigeeKeystoresAliasesSelfSignedCertSubject"], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeKeystoresAliasesSelfSignedCertTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeKeystoresAliasesSelfSignedCertTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba8349c4b44954f08aa8bd821236ed5337909a6d6fe4228bbca757c8b734ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certValidityInDays")
    def cert_validity_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "certValidityInDays"))

    @cert_validity_in_days.setter
    def cert_validity_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd846d81a2cc7be73c766d4884de9c174dd49eeb19204d25112f66ec7554e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certValidityInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56bb07133d9a11f128708ebdaf900afc64c660e1c36db78d494e2e4ab1af3e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21e5007d411380b03a2de492e8e7f6db39bedb2a15c65d4afbf9045baf9f008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keySize")
    def key_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keySize"))

    @key_size.setter
    def key_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c406bdbd2ea7ca14d67d055c76635e3c542b790c39873a11c51a8eff371319fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keySize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keystore")
    def keystore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystore"))

    @keystore.setter
    def keystore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428d0df4462a59edc3916d6d1e76a4818296f898c4bd35c2639fef015c985766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a99ff5780878c3196954b3995ef0e0a0dbdc68b6323b2b7df54a28695be0e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sigAlg")
    def sig_alg(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sigAlg"))

    @sig_alg.setter
    def sig_alg(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4c6b28b8dc29d200e3ccd3fed4688e93fc688b7275000ad1d65b018444820d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sigAlg", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertCertsInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApigeeKeystoresAliasesSelfSignedCertCertsInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesSelfSignedCertCertsInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f186d56c318e3fa4f8ed76b85b85f166f33f2b74a68dc59d2363c6cea20c001)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25aca3943b0b51fd823841a96d2843f5bd0a6301d488b256ed93fd7890390b5d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0014a6d41b7ef88d081fa9e0b404bf63d313417f547de228db37def3c2a3d50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a86957e7e9f2f18501b3a3872d96dcda43e1458d0a277d704e1dd80617bd4999)
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
            type_hints = typing.get_type_hints(_typecheckingstub__234bdcb9ae2500ffc4af21de74027a5d914fcb02d18a7b28508c84ca04068dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1a98e0893a2421e443ede228f97d33dc31bcb22666ec8cc70365678cbedb925)
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
    ) -> typing.Optional[ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo]:
        return typing.cast(typing.Optional[ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c85385862dfa629da7fca7017ca019664bf0f126e0ac418c5cb40250c45971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeKeystoresAliasesSelfSignedCertCertsInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertCertsInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5b8740e64584c6a849fc677e6ffc88cfdc0d66c7e2fcf904b8e0103ea9427c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8f8d7f916aa2f61d35a51b9ff49e69f1ff06f5ad64e926a11b425ad6fba56d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e190de5df7cd6aa63a6734cbc7afbb22aa8972cce09a2268b3aa5d7d2b37de41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__149ebc77ecaa2233955b34295773e76b6399f5dca0ccc663f0b6e23ef2e05020)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1af4e1576456b085f57733471e15507c26d4874889bfd578c1dcd52e1050edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b54fe25262ff19f90b9157bebc62a812c5a444f67b7223da0c2ce31f3dfdae3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="certInfo")
    def cert_info(self) -> ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList:
        return typing.cast(ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList, jsii.get(self, "certInfo"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeKeystoresAliasesSelfSignedCertCertsInfo]:
        return typing.cast(typing.Optional[ApigeeKeystoresAliasesSelfSignedCertCertsInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeKeystoresAliasesSelfSignedCertCertsInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3044355d0c565c033d5b81716ebe6f3023271560cdbfab465d2ca181d43f1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertConfig",
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
class ApigeeKeystoresAliasesSelfSignedCertConfig(
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
        subject: typing.Union["ApigeeKeystoresAliasesSelfSignedCertSubject", typing.Dict[builtins.str, typing.Any]],
        cert_validity_in_days: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        key_size: typing.Optional[builtins.str] = None,
        subject_alternative_dns_names: typing.Optional[typing.Union["ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApigeeKeystoresAliasesSelfSignedCertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param alias: Alias for the key/certificate pair. Values must match the regular expression [\\w\\s-.]{1,255}. This must be provided for all formats except selfsignedcert; self-signed certs may specify the alias in either this parameter or the JSON body. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#alias ApigeeKeystoresAliasesSelfSignedCert#alias}
        :param environment: The Apigee environment name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#environment ApigeeKeystoresAliasesSelfSignedCert#environment}
        :param keystore: The Apigee keystore name associated in an Apigee environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#keystore ApigeeKeystoresAliasesSelfSignedCert#keystore}
        :param org_id: The Apigee Organization name associated with the Apigee environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org_id ApigeeKeystoresAliasesSelfSignedCert#org_id}
        :param sig_alg: Signature algorithm to generate private key. Valid values are SHA512withRSA, SHA384withRSA, and SHA256withRSA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#sig_alg ApigeeKeystoresAliasesSelfSignedCert#sig_alg}
        :param subject: subject block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject ApigeeKeystoresAliasesSelfSignedCert#subject}
        :param cert_validity_in_days: Validity duration of certificate, in days. Accepts positive non-zero value. Defaults to 365. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#cert_validity_in_days ApigeeKeystoresAliasesSelfSignedCert#cert_validity_in_days}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#id ApigeeKeystoresAliasesSelfSignedCert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_size: Key size. Default and maximum value is 2048 bits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#key_size ApigeeKeystoresAliasesSelfSignedCert#key_size}
        :param subject_alternative_dns_names: subject_alternative_dns_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject_alternative_dns_names ApigeeKeystoresAliasesSelfSignedCert#subject_alternative_dns_names}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#timeouts ApigeeKeystoresAliasesSelfSignedCert#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(subject, dict):
            subject = ApigeeKeystoresAliasesSelfSignedCertSubject(**subject)
        if isinstance(subject_alternative_dns_names, dict):
            subject_alternative_dns_names = ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames(**subject_alternative_dns_names)
        if isinstance(timeouts, dict):
            timeouts = ApigeeKeystoresAliasesSelfSignedCertTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506dadcb17c04ed412171f26c8ee73269ad6d28d78481d82b3826813f81af11f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#alias ApigeeKeystoresAliasesSelfSignedCert#alias}
        '''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(self) -> builtins.str:
        '''The Apigee environment name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#environment ApigeeKeystoresAliasesSelfSignedCert#environment}
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keystore(self) -> builtins.str:
        '''The Apigee keystore name associated in an Apigee environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#keystore ApigeeKeystoresAliasesSelfSignedCert#keystore}
        '''
        result = self._values.get("keystore")
        assert result is not None, "Required property 'keystore' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''The Apigee Organization name associated with the Apigee environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org_id ApigeeKeystoresAliasesSelfSignedCert#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sig_alg(self) -> builtins.str:
        '''Signature algorithm to generate private key. Valid values are SHA512withRSA, SHA384withRSA, and SHA256withRSA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#sig_alg ApigeeKeystoresAliasesSelfSignedCert#sig_alg}
        '''
        result = self._values.get("sig_alg")
        assert result is not None, "Required property 'sig_alg' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject(self) -> "ApigeeKeystoresAliasesSelfSignedCertSubject":
        '''subject block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject ApigeeKeystoresAliasesSelfSignedCert#subject}
        '''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast("ApigeeKeystoresAliasesSelfSignedCertSubject", result)

    @builtins.property
    def cert_validity_in_days(self) -> typing.Optional[jsii.Number]:
        '''Validity duration of certificate, in days. Accepts positive non-zero value. Defaults to 365.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#cert_validity_in_days ApigeeKeystoresAliasesSelfSignedCert#cert_validity_in_days}
        '''
        result = self._values.get("cert_validity_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#id ApigeeKeystoresAliasesSelfSignedCert#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_size(self) -> typing.Optional[builtins.str]:
        '''Key size. Default and maximum value is 2048 bits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#key_size ApigeeKeystoresAliasesSelfSignedCert#key_size}
        '''
        result = self._values.get("key_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alternative_dns_names(
        self,
    ) -> typing.Optional["ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames"]:
        '''subject_alternative_dns_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject_alternative_dns_names ApigeeKeystoresAliasesSelfSignedCert#subject_alternative_dns_names}
        '''
        result = self._values.get("subject_alternative_dns_names")
        return typing.cast(typing.Optional["ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["ApigeeKeystoresAliasesSelfSignedCertTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#timeouts ApigeeKeystoresAliasesSelfSignedCert#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigeeKeystoresAliasesSelfSignedCertTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesSelfSignedCertConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertSubject",
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
class ApigeeKeystoresAliasesSelfSignedCertSubject:
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
        :param common_name: Common name of the organization. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#common_name ApigeeKeystoresAliasesSelfSignedCert#common_name}
        :param country_code: Two-letter country code. Example, IN for India, US for United States of America. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#country_code ApigeeKeystoresAliasesSelfSignedCert#country_code}
        :param email: Email address. Max 255 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#email ApigeeKeystoresAliasesSelfSignedCert#email}
        :param locality: City or town name. Maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#locality ApigeeKeystoresAliasesSelfSignedCert#locality}
        :param org: Organization name. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org ApigeeKeystoresAliasesSelfSignedCert#org}
        :param org_unit: Organization team name. Maximum length is 64 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org_unit ApigeeKeystoresAliasesSelfSignedCert#org_unit}
        :param state: State or district name. Maximum length is 128 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#state ApigeeKeystoresAliasesSelfSignedCert#state}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce7e0015bf6128153eb31108c1bb7caa46fd7039ffc0843fb5229eebf3d575f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#common_name ApigeeKeystoresAliasesSelfSignedCert#common_name}
        '''
        result = self._values.get("common_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''Two-letter country code. Example, IN for India, US for United States of America.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#country_code ApigeeKeystoresAliasesSelfSignedCert#country_code}
        '''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email address. Max 255 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#email ApigeeKeystoresAliasesSelfSignedCert#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locality(self) -> typing.Optional[builtins.str]:
        '''City or town name. Maximum length is 128 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#locality ApigeeKeystoresAliasesSelfSignedCert#locality}
        '''
        result = self._values.get("locality")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org(self) -> typing.Optional[builtins.str]:
        '''Organization name. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org ApigeeKeystoresAliasesSelfSignedCert#org}
        '''
        result = self._values.get("org")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def org_unit(self) -> typing.Optional[builtins.str]:
        '''Organization team name. Maximum length is 64 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#org_unit ApigeeKeystoresAliasesSelfSignedCert#org_unit}
        '''
        result = self._values.get("org_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''State or district name. Maximum length is 128 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#state ApigeeKeystoresAliasesSelfSignedCert#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesSelfSignedCertSubject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames",
    jsii_struct_bases=[],
    name_mapping={"subject_alternative_name": "subjectAlternativeName"},
)
class ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames:
    def __init__(
        self,
        *,
        subject_alternative_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subject_alternative_name: Subject Alternative Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject_alternative_name ApigeeKeystoresAliasesSelfSignedCert#subject_alternative_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971813d7aa65aad103a4bded609c21e0473d4241de731b2163efaf69f61653f9)
            check_type(argname="argument subject_alternative_name", value=subject_alternative_name, expected_type=type_hints["subject_alternative_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if subject_alternative_name is not None:
            self._values["subject_alternative_name"] = subject_alternative_name

    @builtins.property
    def subject_alternative_name(self) -> typing.Optional[builtins.str]:
        '''Subject Alternative Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#subject_alternative_name ApigeeKeystoresAliasesSelfSignedCert#subject_alternative_name}
        '''
        result = self._values.get("subject_alternative_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17378173a5293336266f87df098042c1db8709a40c108bc3695946acd16af00a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cef17c7b01a9c8d4c3d919639802ec5e22d6a6f47716191299c4eae60be1b54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectAlternativeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames]:
        return typing.cast(typing.Optional[ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6902cff3b98be86d6e38a3bda52d7a8c657eb7a755ed6f2fb0b3307c61ebed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6eda31d68948d5ad8b8761fa88755a76b486bcab7a270371a937bc59a00437f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2473817a363b0b5010759bc2c8a4fe0bd335fd94b9a1b516da34f0bfaa973a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commonName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a8b766c8fae3b22007ef7ebc17230e6a1ed32e74ed43b3719d1ae21b1711d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bd2710bfc852d7c59db2f0dfab4707f5d05dfb07213c0a5434aa4e6385ae46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="locality")
    def locality(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locality"))

    @locality.setter
    def locality(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811202eae6664a78630d9043792e20e35da2d72272d3e3e1cacdd36c2408786c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locality", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="org")
    def org(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "org"))

    @org.setter
    def org(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe01e6f862c8bf6b9d28fffc7fad10d714b131a85f4a77ec8a2012ee0a32c37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "org", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgUnit")
    def org_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgUnit"))

    @org_unit.setter
    def org_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29463784b4af89558e0984e50bb23aaf4044723214b37a5c91955f2d9d200013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c12128cb04d3c6de56545446fff1946e0566fe5b7d571699c17d8fccf8d053db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeKeystoresAliasesSelfSignedCertSubject]:
        return typing.cast(typing.Optional[ApigeeKeystoresAliasesSelfSignedCertSubject], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeKeystoresAliasesSelfSignedCertSubject],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce491d21f48eeaf343d28b1e27f197b3f53ce4c330580d2c3fe25faa1bc7a683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class ApigeeKeystoresAliasesSelfSignedCertTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#create ApigeeKeystoresAliasesSelfSignedCert#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#delete ApigeeKeystoresAliasesSelfSignedCert#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9d4e7fa36c1be405f6265f3032747566456a65a12a8526a8e255dc39374076)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#create ApigeeKeystoresAliasesSelfSignedCert#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_self_signed_cert#delete ApigeeKeystoresAliasesSelfSignedCert#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesSelfSignedCertTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesSelfSignedCert.ApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d1fd4868553391d54fad94057ce284fd731f9cf0af9bc8f5525910115e9ef68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ad102f4b83deb6d62f9aa30f93a8cdc94aa9b0a3b97f4a30da0b70f81f18c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e1fe24fa3a1fc8e5ee83b2e8825dadefdf205e9de32f19f73cc55f6b78ea4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesSelfSignedCertTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesSelfSignedCertTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesSelfSignedCertTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56df50ac4b3d5485615a790a9a1fa81f5898e07bc214633634c9b14037da4847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigeeKeystoresAliasesSelfSignedCert",
    "ApigeeKeystoresAliasesSelfSignedCertCertsInfo",
    "ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo",
    "ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoList",
    "ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfoOutputReference",
    "ApigeeKeystoresAliasesSelfSignedCertCertsInfoList",
    "ApigeeKeystoresAliasesSelfSignedCertCertsInfoOutputReference",
    "ApigeeKeystoresAliasesSelfSignedCertConfig",
    "ApigeeKeystoresAliasesSelfSignedCertSubject",
    "ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames",
    "ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNamesOutputReference",
    "ApigeeKeystoresAliasesSelfSignedCertSubjectOutputReference",
    "ApigeeKeystoresAliasesSelfSignedCertTimeouts",
    "ApigeeKeystoresAliasesSelfSignedCertTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b1bf09125f4a5bd5e2a3eb58d7b14a3b1ca0f805b7e43c5e53c52cef66db014c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    alias: builtins.str,
    environment: builtins.str,
    keystore: builtins.str,
    org_id: builtins.str,
    sig_alg: builtins.str,
    subject: typing.Union[ApigeeKeystoresAliasesSelfSignedCertSubject, typing.Dict[builtins.str, typing.Any]],
    cert_validity_in_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    key_size: typing.Optional[builtins.str] = None,
    subject_alternative_dns_names: typing.Optional[typing.Union[ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApigeeKeystoresAliasesSelfSignedCertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f8a06ac16b0a5b584297dc55a74f29fc881169b8a51ac0dabf52ad510ec1d4b4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba8349c4b44954f08aa8bd821236ed5337909a6d6fe4228bbca757c8b734ed4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd846d81a2cc7be73c766d4884de9c174dd49eeb19204d25112f66ec7554e11(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56bb07133d9a11f128708ebdaf900afc64c660e1c36db78d494e2e4ab1af3e93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21e5007d411380b03a2de492e8e7f6db39bedb2a15c65d4afbf9045baf9f008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c406bdbd2ea7ca14d67d055c76635e3c542b790c39873a11c51a8eff371319fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428d0df4462a59edc3916d6d1e76a4818296f898c4bd35c2639fef015c985766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a99ff5780878c3196954b3995ef0e0a0dbdc68b6323b2b7df54a28695be0e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4c6b28b8dc29d200e3ccd3fed4688e93fc688b7275000ad1d65b018444820d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f186d56c318e3fa4f8ed76b85b85f166f33f2b74a68dc59d2363c6cea20c001(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25aca3943b0b51fd823841a96d2843f5bd0a6301d488b256ed93fd7890390b5d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0014a6d41b7ef88d081fa9e0b404bf63d313417f547de228db37def3c2a3d50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86957e7e9f2f18501b3a3872d96dcda43e1458d0a277d704e1dd80617bd4999(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234bdcb9ae2500ffc4af21de74027a5d914fcb02d18a7b28508c84ca04068dae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a98e0893a2421e443ede228f97d33dc31bcb22666ec8cc70365678cbedb925(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c85385862dfa629da7fca7017ca019664bf0f126e0ac418c5cb40250c45971(
    value: typing.Optional[ApigeeKeystoresAliasesSelfSignedCertCertsInfoCertInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5b8740e64584c6a849fc677e6ffc88cfdc0d66c7e2fcf904b8e0103ea9427c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8f8d7f916aa2f61d35a51b9ff49e69f1ff06f5ad64e926a11b425ad6fba56d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e190de5df7cd6aa63a6734cbc7afbb22aa8972cce09a2268b3aa5d7d2b37de41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149ebc77ecaa2233955b34295773e76b6399f5dca0ccc663f0b6e23ef2e05020(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1af4e1576456b085f57733471e15507c26d4874889bfd578c1dcd52e1050edf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54fe25262ff19f90b9157bebc62a812c5a444f67b7223da0c2ce31f3dfdae3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3044355d0c565c033d5b81716ebe6f3023271560cdbfab465d2ca181d43f1f4(
    value: typing.Optional[ApigeeKeystoresAliasesSelfSignedCertCertsInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506dadcb17c04ed412171f26c8ee73269ad6d28d78481d82b3826813f81af11f(
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
    subject: typing.Union[ApigeeKeystoresAliasesSelfSignedCertSubject, typing.Dict[builtins.str, typing.Any]],
    cert_validity_in_days: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    key_size: typing.Optional[builtins.str] = None,
    subject_alternative_dns_names: typing.Optional[typing.Union[ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApigeeKeystoresAliasesSelfSignedCertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce7e0015bf6128153eb31108c1bb7caa46fd7039ffc0843fb5229eebf3d575f(
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

def _typecheckingstub__971813d7aa65aad103a4bded609c21e0473d4241de731b2163efaf69f61653f9(
    *,
    subject_alternative_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17378173a5293336266f87df098042c1db8709a40c108bc3695946acd16af00a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef17c7b01a9c8d4c3d919639802ec5e22d6a6f47716191299c4eae60be1b54a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6902cff3b98be86d6e38a3bda52d7a8c657eb7a755ed6f2fb0b3307c61ebed2(
    value: typing.Optional[ApigeeKeystoresAliasesSelfSignedCertSubjectAlternativeDnsNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6eda31d68948d5ad8b8761fa88755a76b486bcab7a270371a937bc59a00437f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2473817a363b0b5010759bc2c8a4fe0bd335fd94b9a1b516da34f0bfaa973a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a8b766c8fae3b22007ef7ebc17230e6a1ed32e74ed43b3719d1ae21b1711d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bd2710bfc852d7c59db2f0dfab4707f5d05dfb07213c0a5434aa4e6385ae46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811202eae6664a78630d9043792e20e35da2d72272d3e3e1cacdd36c2408786c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe01e6f862c8bf6b9d28fffc7fad10d714b131a85f4a77ec8a2012ee0a32c37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29463784b4af89558e0984e50bb23aaf4044723214b37a5c91955f2d9d200013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12128cb04d3c6de56545446fff1946e0566fe5b7d571699c17d8fccf8d053db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce491d21f48eeaf343d28b1e27f197b3f53ce4c330580d2c3fe25faa1bc7a683(
    value: typing.Optional[ApigeeKeystoresAliasesSelfSignedCertSubject],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9d4e7fa36c1be405f6265f3032747566456a65a12a8526a8e255dc39374076(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1fd4868553391d54fad94057ce284fd731f9cf0af9bc8f5525910115e9ef68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad102f4b83deb6d62f9aa30f93a8cdc94aa9b0a3b97f4a30da0b70f81f18c8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e1fe24fa3a1fc8e5ee83b2e8825dadefdf205e9de32f19f73cc55f6b78ea4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56df50ac4b3d5485615a790a9a1fa81f5898e07bc214633634c9b14037da4847(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesSelfSignedCertTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
