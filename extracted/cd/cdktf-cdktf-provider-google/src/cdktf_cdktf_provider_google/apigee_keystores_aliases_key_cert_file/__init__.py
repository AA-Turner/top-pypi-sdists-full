r'''
# `google_apigee_keystores_aliases_key_cert_file`

Refer to the Terraform Registry for docs: [`google_apigee_keystores_aliases_key_cert_file`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file).
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


class ApigeeKeystoresAliasesKeyCertFile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file google_apigee_keystores_aliases_key_cert_file}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        alias: builtins.str,
        cert: builtins.str,
        environment: builtins.str,
        keystore: builtins.str,
        org_id: builtins.str,
        certs_info: typing.Optional[typing.Union["ApigeeKeystoresAliasesKeyCertFileCertsInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeKeystoresAliasesKeyCertFileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file google_apigee_keystores_aliases_key_cert_file} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#alias ApigeeKeystoresAliasesKeyCertFile#alias}
        :param cert: Cert content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#cert ApigeeKeystoresAliasesKeyCertFile#cert}
        :param environment: Environment associated with the alias. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#environment ApigeeKeystoresAliasesKeyCertFile#environment}
        :param keystore: Keystore Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#keystore ApigeeKeystoresAliasesKeyCertFile#keystore}
        :param org_id: Organization ID associated with the alias. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#org_id ApigeeKeystoresAliasesKeyCertFile#org_id}
        :param certs_info: certs_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#certs_info ApigeeKeystoresAliasesKeyCertFile#certs_info}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#id ApigeeKeystoresAliasesKeyCertFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key: Private Key content, omit if uploading to truststore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#key ApigeeKeystoresAliasesKeyCertFile#key}
        :param password: Password for the Private Key if it's encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#password ApigeeKeystoresAliasesKeyCertFile#password}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#timeouts ApigeeKeystoresAliasesKeyCertFile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3340e8d44501faa51d2bf6b2af9ebc82826118275fd6e49caa0266f9e6557b68)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApigeeKeystoresAliasesKeyCertFileConfig(
            alias=alias,
            cert=cert,
            environment=environment,
            keystore=keystore,
            org_id=org_id,
            certs_info=certs_info,
            id=id,
            key=key,
            password=password,
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
        '''Generates CDKTF code for importing a ApigeeKeystoresAliasesKeyCertFile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApigeeKeystoresAliasesKeyCertFile to import.
        :param import_from_id: The id of the existing ApigeeKeystoresAliasesKeyCertFile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApigeeKeystoresAliasesKeyCertFile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb655abdc775dcd32114fdf8b5fb16ced6c4b055a0e3d8a649b143ba61d3a2b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCertsInfo")
    def put_certs_info(
        self,
        *,
        cert_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cert_info: cert_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#cert_info ApigeeKeystoresAliasesKeyCertFile#cert_info}
        '''
        value = ApigeeKeystoresAliasesKeyCertFileCertsInfo(cert_info=cert_info)

        return typing.cast(None, jsii.invoke(self, "putCertsInfo", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#create ApigeeKeystoresAliasesKeyCertFile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#delete ApigeeKeystoresAliasesKeyCertFile#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#read ApigeeKeystoresAliasesKeyCertFile#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#update ApigeeKeystoresAliasesKeyCertFile#update}.
        '''
        value = ApigeeKeystoresAliasesKeyCertFileTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCertsInfo")
    def reset_certs_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertsInfo", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

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
    def certs_info(self) -> "ApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference":
        return typing.cast("ApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference", jsii.get(self, "certsInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference":
        return typing.cast("ApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="certsInfoInput")
    def certs_info_input(
        self,
    ) -> typing.Optional["ApigeeKeystoresAliasesKeyCertFileCertsInfo"]:
        return typing.cast(typing.Optional["ApigeeKeystoresAliasesKeyCertFileCertsInfo"], jsii.get(self, "certsInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="keystoreInput")
    def keystore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keystoreInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeKeystoresAliasesKeyCertFileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApigeeKeystoresAliasesKeyCertFileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5502411992055d6c3f10540269a30eebfa8123f35a4cbc8e34002f62aa85cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cert"))

    @cert.setter
    def cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5154e9474746f5804d78a1665681bb5acc3a51badfbb59be3d6b8178394233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d02eb0467cebe0cf9ed77b8f43f69fe7b08b4a6d99c54d4d4d95088579eb8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9105125d85cea74e6f29b5731534d6fcbc3cfa0c4bdb207cc197c0d2d03a0e44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdcb46654a835b9a47cf5a2957e7feee56c9c45c7ced7072cb809053833dcda6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keystore")
    def keystore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystore"))

    @keystore.setter
    def keystore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cf634edbdc2c70a9aa751f6c7761dfd422475389c1d3790b8d5af416cb215e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2648fbd1881b11550a778ec396f07d5ad82d8ffbdc28caca2b37b3e204fe81bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc6260d3beef936bed5b5bed8ef3005481205cf03b9764777dee56e55e67c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFileCertsInfo",
    jsii_struct_bases=[],
    name_mapping={"cert_info": "certInfo"},
)
class ApigeeKeystoresAliasesKeyCertFileCertsInfo:
    def __init__(
        self,
        *,
        cert_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cert_info: cert_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#cert_info ApigeeKeystoresAliasesKeyCertFile#cert_info}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345c60a0c60a56c9f803060f691230ed09af7526fda8e532de4f8e49fa894784)
            check_type(argname="argument cert_info", value=cert_info, expected_type=type_hints["cert_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cert_info is not None:
            self._values["cert_info"] = cert_info

    @builtins.property
    def cert_info(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo"]]]:
        '''cert_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#cert_info ApigeeKeystoresAliasesKeyCertFile#cert_info}
        '''
        result = self._values.get("cert_info")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesKeyCertFileCertsInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo",
    jsii_struct_bases=[],
    name_mapping={
        "basic_constraints": "basicConstraints",
        "expiry_date": "expiryDate",
        "issuer": "issuer",
        "is_valid": "isValid",
        "public_key": "publicKey",
        "serial_number": "serialNumber",
        "sig_alg_name": "sigAlgName",
        "subject": "subject",
        "subject_alternative_names": "subjectAlternativeNames",
        "valid_from": "validFrom",
        "version": "version",
    },
)
class ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo:
    def __init__(
        self,
        *,
        basic_constraints: typing.Optional[builtins.str] = None,
        expiry_date: typing.Optional[builtins.str] = None,
        issuer: typing.Optional[builtins.str] = None,
        is_valid: typing.Optional[builtins.str] = None,
        public_key: typing.Optional[builtins.str] = None,
        serial_number: typing.Optional[builtins.str] = None,
        sig_alg_name: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        valid_from: typing.Optional[builtins.str] = None,
        version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param basic_constraints: X.509 basic constraints extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#basic_constraints ApigeeKeystoresAliasesKeyCertFile#basic_constraints}
        :param expiry_date: X.509 notAfter validity period in milliseconds since epoch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#expiry_date ApigeeKeystoresAliasesKeyCertFile#expiry_date}
        :param issuer: X.509 issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#issuer ApigeeKeystoresAliasesKeyCertFile#issuer}
        :param is_valid: Flag that specifies whether the certificate is valid. Flag is set to Yes if the certificate is valid, No if expired, or Not yet if not yet valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#is_valid ApigeeKeystoresAliasesKeyCertFile#is_valid}
        :param public_key: Public key component of the X.509 subject public key info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#public_key ApigeeKeystoresAliasesKeyCertFile#public_key}
        :param serial_number: X.509 serial number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#serial_number ApigeeKeystoresAliasesKeyCertFile#serial_number}
        :param sig_alg_name: X.509 signatureAlgorithm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#sig_alg_name ApigeeKeystoresAliasesKeyCertFile#sig_alg_name}
        :param subject: X.509 subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#subject ApigeeKeystoresAliasesKeyCertFile#subject}
        :param subject_alternative_names: X.509 subject alternative names (SANs) extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#subject_alternative_names ApigeeKeystoresAliasesKeyCertFile#subject_alternative_names}
        :param valid_from: X.509 notBefore validity period in milliseconds since epoch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#valid_from ApigeeKeystoresAliasesKeyCertFile#valid_from}
        :param version: X.509 version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#version ApigeeKeystoresAliasesKeyCertFile#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b524324c1d572fc2bf7eec87e72aafe8ed2ecf87397a8717ddc7e65dd21a00a7)
            check_type(argname="argument basic_constraints", value=basic_constraints, expected_type=type_hints["basic_constraints"])
            check_type(argname="argument expiry_date", value=expiry_date, expected_type=type_hints["expiry_date"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument is_valid", value=is_valid, expected_type=type_hints["is_valid"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
            check_type(argname="argument sig_alg_name", value=sig_alg_name, expected_type=type_hints["sig_alg_name"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument valid_from", value=valid_from, expected_type=type_hints["valid_from"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_constraints is not None:
            self._values["basic_constraints"] = basic_constraints
        if expiry_date is not None:
            self._values["expiry_date"] = expiry_date
        if issuer is not None:
            self._values["issuer"] = issuer
        if is_valid is not None:
            self._values["is_valid"] = is_valid
        if public_key is not None:
            self._values["public_key"] = public_key
        if serial_number is not None:
            self._values["serial_number"] = serial_number
        if sig_alg_name is not None:
            self._values["sig_alg_name"] = sig_alg_name
        if subject is not None:
            self._values["subject"] = subject
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names
        if valid_from is not None:
            self._values["valid_from"] = valid_from
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def basic_constraints(self) -> typing.Optional[builtins.str]:
        '''X.509 basic constraints extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#basic_constraints ApigeeKeystoresAliasesKeyCertFile#basic_constraints}
        '''
        result = self._values.get("basic_constraints")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiry_date(self) -> typing.Optional[builtins.str]:
        '''X.509 notAfter validity period in milliseconds since epoch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#expiry_date ApigeeKeystoresAliasesKeyCertFile#expiry_date}
        '''
        result = self._values.get("expiry_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''X.509 issuer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#issuer ApigeeKeystoresAliasesKeyCertFile#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_valid(self) -> typing.Optional[builtins.str]:
        '''Flag that specifies whether the certificate is valid.

        Flag is set to Yes if the certificate is valid, No if expired, or Not yet if not yet valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#is_valid ApigeeKeystoresAliasesKeyCertFile#is_valid}
        '''
        result = self._values.get("is_valid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key(self) -> typing.Optional[builtins.str]:
        '''Public key component of the X.509 subject public key info.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#public_key ApigeeKeystoresAliasesKeyCertFile#public_key}
        '''
        result = self._values.get("public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_number(self) -> typing.Optional[builtins.str]:
        '''X.509 serial number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#serial_number ApigeeKeystoresAliasesKeyCertFile#serial_number}
        '''
        result = self._values.get("serial_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sig_alg_name(self) -> typing.Optional[builtins.str]:
        '''X.509 signatureAlgorithm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#sig_alg_name ApigeeKeystoresAliasesKeyCertFile#sig_alg_name}
        '''
        result = self._values.get("sig_alg_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''X.509 subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#subject ApigeeKeystoresAliasesKeyCertFile#subject}
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''X.509 subject alternative names (SANs) extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#subject_alternative_names ApigeeKeystoresAliasesKeyCertFile#subject_alternative_names}
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def valid_from(self) -> typing.Optional[builtins.str]:
        '''X.509 notBefore validity period in milliseconds since epoch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#valid_from ApigeeKeystoresAliasesKeyCertFile#valid_from}
        '''
        result = self._values.get("valid_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''X.509 version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#version ApigeeKeystoresAliasesKeyCertFile#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__17ba3535b96df5dd7a2b72e5bb26bdeffbd125d36b5c8eb231901b39bf9345a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f19047f6e2300ea30d91274e476a8babc6ae4a2eb09a812e370c41477c7e040)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63616813a7485b6e5c251d76f331986a228824f506982d0d1208c90ffb9c7df1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57d42425ac30337dfd63343ac9c1569bc676474bf265f6659e0caed338080555)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa66755e2c088631bfa1f404f770497fd29460386d946c1022c6b6518c9c638b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af9a393fcbaabbb5cf7071017111c57ff97db5c444ee41387c55e22599f0fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdfd452f951b571bd948909a26de15f9f38e508875fab47096c171ca82a6873c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBasicConstraints")
    def reset_basic_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicConstraints", []))

    @jsii.member(jsii_name="resetExpiryDate")
    def reset_expiry_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiryDate", []))

    @jsii.member(jsii_name="resetIssuer")
    def reset_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuer", []))

    @jsii.member(jsii_name="resetIsValid")
    def reset_is_valid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsValid", []))

    @jsii.member(jsii_name="resetPublicKey")
    def reset_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKey", []))

    @jsii.member(jsii_name="resetSerialNumber")
    def reset_serial_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSerialNumber", []))

    @jsii.member(jsii_name="resetSigAlgName")
    def reset_sig_alg_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSigAlgName", []))

    @jsii.member(jsii_name="resetSubject")
    def reset_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubject", []))

    @jsii.member(jsii_name="resetSubjectAlternativeNames")
    def reset_subject_alternative_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAlternativeNames", []))

    @jsii.member(jsii_name="resetValidFrom")
    def reset_valid_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidFrom", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="basicConstraintsInput")
    def basic_constraints_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "basicConstraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="expiryDateInput")
    def expiry_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expiryDateInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="isValidInput")
    def is_valid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isValidInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="serialNumberInput")
    def serial_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serialNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="sigAlgNameInput")
    def sig_alg_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sigAlgNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNamesInput")
    def subject_alternative_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subjectAlternativeNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectInput")
    def subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subjectInput"))

    @builtins.property
    @jsii.member(jsii_name="validFromInput")
    def valid_from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "validFromInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="basicConstraints")
    def basic_constraints(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "basicConstraints"))

    @basic_constraints.setter
    def basic_constraints(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d75787c7f9b47b8aba1eb46ab35edbb36c47fca36bd9d5de641a23fda08b051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicConstraints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiryDate")
    def expiry_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiryDate"))

    @expiry_date.setter
    def expiry_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93712e87cf9b910eb95443e3c111b636edc10ecffb7a7058cc09adee2b73b3a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiryDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd0384af2c373abb7195623ce4b22265cb8c10c58479ae83bf4a5dd183a0612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isValid")
    def is_valid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isValid"))

    @is_valid.setter
    def is_valid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6a7a12b2ee7cf97c66d2918019e2d7e304d16a213623cf846516913fefaac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8483c1885767484ff3f4d9037b88d69d2d397c646c686c17962a932f1e0e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @serial_number.setter
    def serial_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7052d7c88f43f773b125d28ccdbdf57e2303a7e0aa1050b338145f8ec6b754cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serialNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sigAlgName")
    def sig_alg_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sigAlgName"))

    @sig_alg_name.setter
    def sig_alg_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b38322b29f40023cd97189b3f7d3ad67ed82a051cd5148ddc8574c527daaab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sigAlgName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943e20679b4e50b36ea28dfd848e01e6702bfd000317dd8230301ec627af41d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subjectAlternativeNames"))

    @subject_alternative_names.setter
    def subject_alternative_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad7777da120148e83edc18d0b6cb469b1ab591aff65378658cf533081868fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectAlternativeNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validFrom")
    def valid_from(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validFrom"))

    @valid_from.setter
    def valid_from(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afa044ba776b9ecaee17142c30a883d7834ec2245c58dfff4656d4c1847f5de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validFrom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @version.setter
    def version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd336cad984d418544a4a6d772d027f392352a03856b124df786e381ac441b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69733185e283b3f376f157c549b5737bb841aec9135a01345a7fd66678081745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0cebb99865651ebfd2edc85a4df0ddf02e4ab4992781998ac96859861a5269c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertInfo")
    def put_cert_info(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0961b6715704c1b4b0f333635d6d2b5c12694e07d9dea7e7dbaed679e14ab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertInfo", [value]))

    @jsii.member(jsii_name="resetCertInfo")
    def reset_cert_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertInfo", []))

    @builtins.property
    @jsii.member(jsii_name="certInfo")
    def cert_info(self) -> ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList:
        return typing.cast(ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList, jsii.get(self, "certInfo"))

    @builtins.property
    @jsii.member(jsii_name="certInfoInput")
    def cert_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]], jsii.get(self, "certInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApigeeKeystoresAliasesKeyCertFileCertsInfo]:
        return typing.cast(typing.Optional[ApigeeKeystoresAliasesKeyCertFileCertsInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApigeeKeystoresAliasesKeyCertFileCertsInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8803223059c2426f6b18153865e13254985ee85c8d66fc6fb3a2dd1eebee3c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFileConfig",
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
        "cert": "cert",
        "environment": "environment",
        "keystore": "keystore",
        "org_id": "orgId",
        "certs_info": "certsInfo",
        "id": "id",
        "key": "key",
        "password": "password",
        "timeouts": "timeouts",
    },
)
class ApigeeKeystoresAliasesKeyCertFileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cert: builtins.str,
        environment: builtins.str,
        keystore: builtins.str,
        org_id: builtins.str,
        certs_info: typing.Optional[typing.Union[ApigeeKeystoresAliasesKeyCertFileCertsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApigeeKeystoresAliasesKeyCertFileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param alias: Alias Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#alias ApigeeKeystoresAliasesKeyCertFile#alias}
        :param cert: Cert content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#cert ApigeeKeystoresAliasesKeyCertFile#cert}
        :param environment: Environment associated with the alias. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#environment ApigeeKeystoresAliasesKeyCertFile#environment}
        :param keystore: Keystore Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#keystore ApigeeKeystoresAliasesKeyCertFile#keystore}
        :param org_id: Organization ID associated with the alias. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#org_id ApigeeKeystoresAliasesKeyCertFile#org_id}
        :param certs_info: certs_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#certs_info ApigeeKeystoresAliasesKeyCertFile#certs_info}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#id ApigeeKeystoresAliasesKeyCertFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key: Private Key content, omit if uploading to truststore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#key ApigeeKeystoresAliasesKeyCertFile#key}
        :param password: Password for the Private Key if it's encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#password ApigeeKeystoresAliasesKeyCertFile#password}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#timeouts ApigeeKeystoresAliasesKeyCertFile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(certs_info, dict):
            certs_info = ApigeeKeystoresAliasesKeyCertFileCertsInfo(**certs_info)
        if isinstance(timeouts, dict):
            timeouts = ApigeeKeystoresAliasesKeyCertFileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10cdf7b549187873cba9dba787cee31cd257c264db5b8367d4f8e8c1641eca56)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument keystore", value=keystore, expected_type=type_hints["keystore"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument certs_info", value=certs_info, expected_type=type_hints["certs_info"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias": alias,
            "cert": cert,
            "environment": environment,
            "keystore": keystore,
            "org_id": org_id,
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
        if certs_info is not None:
            self._values["certs_info"] = certs_info
        if id is not None:
            self._values["id"] = id
        if key is not None:
            self._values["key"] = key
        if password is not None:
            self._values["password"] = password
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
        '''Alias Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#alias ApigeeKeystoresAliasesKeyCertFile#alias}
        '''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cert(self) -> builtins.str:
        '''Cert content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#cert ApigeeKeystoresAliasesKeyCertFile#cert}
        '''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(self) -> builtins.str:
        '''Environment associated with the alias.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#environment ApigeeKeystoresAliasesKeyCertFile#environment}
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keystore(self) -> builtins.str:
        '''Keystore Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#keystore ApigeeKeystoresAliasesKeyCertFile#keystore}
        '''
        result = self._values.get("keystore")
        assert result is not None, "Required property 'keystore' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''Organization ID associated with the alias.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#org_id ApigeeKeystoresAliasesKeyCertFile#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certs_info(self) -> typing.Optional[ApigeeKeystoresAliasesKeyCertFileCertsInfo]:
        '''certs_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#certs_info ApigeeKeystoresAliasesKeyCertFile#certs_info}
        '''
        result = self._values.get("certs_info")
        return typing.cast(typing.Optional[ApigeeKeystoresAliasesKeyCertFileCertsInfo], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#id ApigeeKeystoresAliasesKeyCertFile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Private Key content, omit if uploading to truststore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#key ApigeeKeystoresAliasesKeyCertFile#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the Private Key if it's encrypted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#password ApigeeKeystoresAliasesKeyCertFile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApigeeKeystoresAliasesKeyCertFileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#timeouts ApigeeKeystoresAliasesKeyCertFile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApigeeKeystoresAliasesKeyCertFileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesKeyCertFileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFileTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApigeeKeystoresAliasesKeyCertFileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#create ApigeeKeystoresAliasesKeyCertFile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#delete ApigeeKeystoresAliasesKeyCertFile#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#read ApigeeKeystoresAliasesKeyCertFile#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#update ApigeeKeystoresAliasesKeyCertFile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f1a9e438fdfd62412ffb582ac80db3eabf88e4e0f0a16556aa3d82b2a7c3f9)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#create ApigeeKeystoresAliasesKeyCertFile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#delete ApigeeKeystoresAliasesKeyCertFile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#read ApigeeKeystoresAliasesKeyCertFile#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/apigee_keystores_aliases_key_cert_file#update ApigeeKeystoresAliasesKeyCertFile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApigeeKeystoresAliasesKeyCertFileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.apigeeKeystoresAliasesKeyCertFile.ApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32cd763cd747b9d98c870b12b9d67ce4ce8e51936f45f8e2b1046ccba2faaab7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__72b753edb75c672ccb21d4f25bb7f3acf9531fd334f9dccca88548951f27ee68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb0cca309d78fd7040dd18975929713108e47a3d0614eb4aae543c2ada431e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b4bcbceb2c3504d306d84507277e78b2dc0da6c357904d74e062bbc7423e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15384617a43144df680f1c2beea43231188455c7ab2acf5574a1f0044c728abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesKeyCertFileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesKeyCertFileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesKeyCertFileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c185d0ffb2b5c2b1dbbdd99c02d07bafc445b82daa811ef7d379b58164f78d55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApigeeKeystoresAliasesKeyCertFile",
    "ApigeeKeystoresAliasesKeyCertFileCertsInfo",
    "ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo",
    "ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList",
    "ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference",
    "ApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference",
    "ApigeeKeystoresAliasesKeyCertFileConfig",
    "ApigeeKeystoresAliasesKeyCertFileTimeouts",
    "ApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3340e8d44501faa51d2bf6b2af9ebc82826118275fd6e49caa0266f9e6557b68(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    alias: builtins.str,
    cert: builtins.str,
    environment: builtins.str,
    keystore: builtins.str,
    org_id: builtins.str,
    certs_info: typing.Optional[typing.Union[ApigeeKeystoresAliasesKeyCertFileCertsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeKeystoresAliasesKeyCertFileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bb655abdc775dcd32114fdf8b5fb16ced6c4b055a0e3d8a649b143ba61d3a2b4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5502411992055d6c3f10540269a30eebfa8123f35a4cbc8e34002f62aa85cdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5154e9474746f5804d78a1665681bb5acc3a51badfbb59be3d6b8178394233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d02eb0467cebe0cf9ed77b8f43f69fe7b08b4a6d99c54d4d4d95088579eb8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9105125d85cea74e6f29b5731534d6fcbc3cfa0c4bdb207cc197c0d2d03a0e44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcb46654a835b9a47cf5a2957e7feee56c9c45c7ced7072cb809053833dcda6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cf634edbdc2c70a9aa751f6c7761dfd422475389c1d3790b8d5af416cb215e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2648fbd1881b11550a778ec396f07d5ad82d8ffbdc28caca2b37b3e204fe81bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc6260d3beef936bed5b5bed8ef3005481205cf03b9764777dee56e55e67c80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345c60a0c60a56c9f803060f691230ed09af7526fda8e532de4f8e49fa894784(
    *,
    cert_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b524324c1d572fc2bf7eec87e72aafe8ed2ecf87397a8717ddc7e65dd21a00a7(
    *,
    basic_constraints: typing.Optional[builtins.str] = None,
    expiry_date: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    is_valid: typing.Optional[builtins.str] = None,
    public_key: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    sig_alg_name: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    valid_from: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ba3535b96df5dd7a2b72e5bb26bdeffbd125d36b5c8eb231901b39bf9345a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f19047f6e2300ea30d91274e476a8babc6ae4a2eb09a812e370c41477c7e040(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63616813a7485b6e5c251d76f331986a228824f506982d0d1208c90ffb9c7df1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d42425ac30337dfd63343ac9c1569bc676474bf265f6659e0caed338080555(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa66755e2c088631bfa1f404f770497fd29460386d946c1022c6b6518c9c638b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af9a393fcbaabbb5cf7071017111c57ff97db5c444ee41387c55e22599f0fd9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfd452f951b571bd948909a26de15f9f38e508875fab47096c171ca82a6873c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d75787c7f9b47b8aba1eb46ab35edbb36c47fca36bd9d5de641a23fda08b051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93712e87cf9b910eb95443e3c111b636edc10ecffb7a7058cc09adee2b73b3a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd0384af2c373abb7195623ce4b22265cb8c10c58479ae83bf4a5dd183a0612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6a7a12b2ee7cf97c66d2918019e2d7e304d16a213623cf846516913fefaac9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8483c1885767484ff3f4d9037b88d69d2d397c646c686c17962a932f1e0e47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7052d7c88f43f773b125d28ccdbdf57e2303a7e0aa1050b338145f8ec6b754cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b38322b29f40023cd97189b3f7d3ad67ed82a051cd5148ddc8574c527daaab1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943e20679b4e50b36ea28dfd848e01e6702bfd000317dd8230301ec627af41d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad7777da120148e83edc18d0b6cb469b1ab591aff65378658cf533081868fb5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afa044ba776b9ecaee17142c30a883d7834ec2245c58dfff4656d4c1847f5de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd336cad984d418544a4a6d772d027f392352a03856b124df786e381ac441b8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69733185e283b3f376f157c549b5737bb841aec9135a01345a7fd66678081745(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cebb99865651ebfd2edc85a4df0ddf02e4ab4992781998ac96859861a5269c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0961b6715704c1b4b0f333635d6d2b5c12694e07d9dea7e7dbaed679e14ab8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8803223059c2426f6b18153865e13254985ee85c8d66fc6fb3a2dd1eebee3c6(
    value: typing.Optional[ApigeeKeystoresAliasesKeyCertFileCertsInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cdf7b549187873cba9dba787cee31cd257c264db5b8367d4f8e8c1641eca56(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    alias: builtins.str,
    cert: builtins.str,
    environment: builtins.str,
    keystore: builtins.str,
    org_id: builtins.str,
    certs_info: typing.Optional[typing.Union[ApigeeKeystoresAliasesKeyCertFileCertsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApigeeKeystoresAliasesKeyCertFileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f1a9e438fdfd62412ffb582ac80db3eabf88e4e0f0a16556aa3d82b2a7c3f9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cd763cd747b9d98c870b12b9d67ce4ce8e51936f45f8e2b1046ccba2faaab7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b753edb75c672ccb21d4f25bb7f3acf9531fd334f9dccca88548951f27ee68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb0cca309d78fd7040dd18975929713108e47a3d0614eb4aae543c2ada431e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b4bcbceb2c3504d306d84507277e78b2dc0da6c357904d74e062bbc7423e70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15384617a43144df680f1c2beea43231188455c7ab2acf5574a1f0044c728abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c185d0ffb2b5c2b1dbbdd99c02d07bafc445b82daa811ef7d379b58164f78d55(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApigeeKeystoresAliasesKeyCertFileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
