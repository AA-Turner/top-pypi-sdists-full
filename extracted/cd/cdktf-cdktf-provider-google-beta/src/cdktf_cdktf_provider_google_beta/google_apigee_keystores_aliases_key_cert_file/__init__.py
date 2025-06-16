r'''
# `google_apigee_keystores_aliases_key_cert_file`

Refer to the Terraform Registry for docs: [`google_apigee_keystores_aliases_key_cert_file`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file).
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


class GoogleApigeeKeystoresAliasesKeyCertFile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file google_apigee_keystores_aliases_key_cert_file}.'''

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
        certs_info: typing.Optional[typing.Union["GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeKeystoresAliasesKeyCertFileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file google_apigee_keystores_aliases_key_cert_file} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#alias GoogleApigeeKeystoresAliasesKeyCertFile#alias}
        :param cert: Cert content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#cert GoogleApigeeKeystoresAliasesKeyCertFile#cert}
        :param environment: Environment associated with the alias. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#environment GoogleApigeeKeystoresAliasesKeyCertFile#environment}
        :param keystore: Keystore Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#keystore GoogleApigeeKeystoresAliasesKeyCertFile#keystore}
        :param org_id: Organization ID associated with the alias. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#org_id GoogleApigeeKeystoresAliasesKeyCertFile#org_id}
        :param certs_info: certs_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#certs_info GoogleApigeeKeystoresAliasesKeyCertFile#certs_info}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#id GoogleApigeeKeystoresAliasesKeyCertFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key: Private Key content, omit if uploading to truststore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#key GoogleApigeeKeystoresAliasesKeyCertFile#key}
        :param password: Password for the Private Key if it's encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#password GoogleApigeeKeystoresAliasesKeyCertFile#password}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#timeouts GoogleApigeeKeystoresAliasesKeyCertFile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9616867104020a7250849818c439b00149f247df40355ccc5b624a8349889f34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApigeeKeystoresAliasesKeyCertFileConfig(
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
        '''Generates CDKTF code for importing a GoogleApigeeKeystoresAliasesKeyCertFile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApigeeKeystoresAliasesKeyCertFile to import.
        :param import_from_id: The id of the existing GoogleApigeeKeystoresAliasesKeyCertFile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApigeeKeystoresAliasesKeyCertFile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ae4fbd691c44a085e32acd3f9381f1c60dc625fa6360d13e2cda1f5d943365)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCertsInfo")
    def put_certs_info(
        self,
        *,
        cert_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cert_info: cert_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#cert_info GoogleApigeeKeystoresAliasesKeyCertFile#cert_info}
        '''
        value = GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo(cert_info=cert_info)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#create GoogleApigeeKeystoresAliasesKeyCertFile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#delete GoogleApigeeKeystoresAliasesKeyCertFile#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#read GoogleApigeeKeystoresAliasesKeyCertFile#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#update GoogleApigeeKeystoresAliasesKeyCertFile#update}.
        '''
        value = GoogleApigeeKeystoresAliasesKeyCertFileTimeouts(
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
    def certs_info(
        self,
    ) -> "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference":
        return typing.cast("GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference", jsii.get(self, "certsInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference":
        return typing.cast("GoogleApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo"]:
        return typing.cast(typing.Optional["GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo"], jsii.get(self, "certsInfoInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeKeystoresAliasesKeyCertFileTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApigeeKeystoresAliasesKeyCertFileTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab89cd3792d9b6a3b17471a2b4ab71861ef27d2017d2daa1c525592e224dde62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cert"))

    @cert.setter
    def cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d670a0193b4db04f430a6d769eacd664fd21522b86bfb9236e0e1a2e7257a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9435111d611a7bdd260f4ca5fea758bdcb106a9af5333e95e83136b97babd5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dceff8d7e67835616a6ae36c0f119f7578fc94a9795f9cc104c380078fb616d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07e11a1268785b15b983c6cc3b08b35cae1cc9f6f79823ee1be0d6729bacaca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keystore")
    def keystore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keystore"))

    @keystore.setter
    def keystore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b734d18748750ca95990140b027209daed23aad2ae69ad2fc28fbfe3e12fd12d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keystore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681bcf6aa2be78dad2bd5c9b6bf86441c309768d1dbbf55b7e1f4b0a5d602293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2826888c99575c63f11d2000ae7f6da9f0685d4abccadf2321fb60fb9f7809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo",
    jsii_struct_bases=[],
    name_mapping={"cert_info": "certInfo"},
)
class GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo:
    def __init__(
        self,
        *,
        cert_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cert_info: cert_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#cert_info GoogleApigeeKeystoresAliasesKeyCertFile#cert_info}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced25291f3783dcbe954944193aa25105f831484f070ff84840761f91c7c18b5)
            check_type(argname="argument cert_info", value=cert_info, expected_type=type_hints["cert_info"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cert_info is not None:
            self._values["cert_info"] = cert_info

    @builtins.property
    def cert_info(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo"]]]:
        '''cert_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#cert_info GoogleApigeeKeystoresAliasesKeyCertFile#cert_info}
        '''
        result = self._values.get("cert_info")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo",
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
class GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo:
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
        :param basic_constraints: X.509 basic constraints extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#basic_constraints GoogleApigeeKeystoresAliasesKeyCertFile#basic_constraints}
        :param expiry_date: X.509 notAfter validity period in milliseconds since epoch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#expiry_date GoogleApigeeKeystoresAliasesKeyCertFile#expiry_date}
        :param issuer: X.509 issuer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#issuer GoogleApigeeKeystoresAliasesKeyCertFile#issuer}
        :param is_valid: Flag that specifies whether the certificate is valid. Flag is set to Yes if the certificate is valid, No if expired, or Not yet if not yet valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#is_valid GoogleApigeeKeystoresAliasesKeyCertFile#is_valid}
        :param public_key: Public key component of the X.509 subject public key info. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#public_key GoogleApigeeKeystoresAliasesKeyCertFile#public_key}
        :param serial_number: X.509 serial number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#serial_number GoogleApigeeKeystoresAliasesKeyCertFile#serial_number}
        :param sig_alg_name: X.509 signatureAlgorithm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#sig_alg_name GoogleApigeeKeystoresAliasesKeyCertFile#sig_alg_name}
        :param subject: X.509 subject. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#subject GoogleApigeeKeystoresAliasesKeyCertFile#subject}
        :param subject_alternative_names: X.509 subject alternative names (SANs) extension. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#subject_alternative_names GoogleApigeeKeystoresAliasesKeyCertFile#subject_alternative_names}
        :param valid_from: X.509 notBefore validity period in milliseconds since epoch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#valid_from GoogleApigeeKeystoresAliasesKeyCertFile#valid_from}
        :param version: X.509 version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#version GoogleApigeeKeystoresAliasesKeyCertFile#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72693781855d45c475471acfedaff367b74659894c6ea56c540c5fac61ea8fd6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#basic_constraints GoogleApigeeKeystoresAliasesKeyCertFile#basic_constraints}
        '''
        result = self._values.get("basic_constraints")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiry_date(self) -> typing.Optional[builtins.str]:
        '''X.509 notAfter validity period in milliseconds since epoch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#expiry_date GoogleApigeeKeystoresAliasesKeyCertFile#expiry_date}
        '''
        result = self._values.get("expiry_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''X.509 issuer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#issuer GoogleApigeeKeystoresAliasesKeyCertFile#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_valid(self) -> typing.Optional[builtins.str]:
        '''Flag that specifies whether the certificate is valid.

        Flag is set to Yes if the certificate is valid, No if expired, or Not yet if not yet valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#is_valid GoogleApigeeKeystoresAliasesKeyCertFile#is_valid}
        '''
        result = self._values.get("is_valid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key(self) -> typing.Optional[builtins.str]:
        '''Public key component of the X.509 subject public key info.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#public_key GoogleApigeeKeystoresAliasesKeyCertFile#public_key}
        '''
        result = self._values.get("public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_number(self) -> typing.Optional[builtins.str]:
        '''X.509 serial number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#serial_number GoogleApigeeKeystoresAliasesKeyCertFile#serial_number}
        '''
        result = self._values.get("serial_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sig_alg_name(self) -> typing.Optional[builtins.str]:
        '''X.509 signatureAlgorithm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#sig_alg_name GoogleApigeeKeystoresAliasesKeyCertFile#sig_alg_name}
        '''
        result = self._values.get("sig_alg_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        '''X.509 subject.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#subject GoogleApigeeKeystoresAliasesKeyCertFile#subject}
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''X.509 subject alternative names (SANs) extension.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#subject_alternative_names GoogleApigeeKeystoresAliasesKeyCertFile#subject_alternative_names}
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def valid_from(self) -> typing.Optional[builtins.str]:
        '''X.509 notBefore validity period in milliseconds since epoch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#valid_from GoogleApigeeKeystoresAliasesKeyCertFile#valid_from}
        '''
        result = self._values.get("valid_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[jsii.Number]:
        '''X.509 version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#version GoogleApigeeKeystoresAliasesKeyCertFile#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b67e3701cb448372d527839e1a38a497fccced44a74f9ff2d30183dc2445bc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b82904e0c6226ddcbb1674c5fb1ddc635513d1ea49e695db6ca239a784c975)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c044c4f5728ef597ba95f7ed2fadf8a295bd3a18b88873054d9e0d9283d56899)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66b6857b52f86f677f06483aacaf681646958b2ed21debab595a57e705040092)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46d8a8b26bb673c183a41caae8ed2fe0841b4b094f3132e40e0c4552b34e7e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195b0ef7d3d0b88b9f6d3cd0eaec78ff8840a6eb045db6c470885204fa121655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e234908910e699227f4975c2097bb09dd25517f6822f22f920b5b8e1b4f82c7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3500650851cc5856560664d445214115f8d27e48ec5237c2dfc9cf9c7b085f28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicConstraints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiryDate")
    def expiry_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiryDate"))

    @expiry_date.setter
    def expiry_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ac030dc44c92035ce18dfc4d21df5726cd18f645448ed73a42b8b144bd0946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiryDate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc289a352e1b2a2a7913c10683ef69dbd3d128e69db8219086eec8bbc31e50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isValid")
    def is_valid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isValid"))

    @is_valid.setter
    def is_valid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6478e50ca29020df41d19de67fcc3ccb746e94850f5ad0c4bcb24bdfed2e55e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isValid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af7726471b30893492121c963876a7c138de29401cca07559ca135c9d393ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @serial_number.setter
    def serial_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77725497419c3a973dcacdcfe2d3ff411de0a5a629fddd613872a439ca549f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serialNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sigAlgName")
    def sig_alg_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sigAlgName"))

    @sig_alg_name.setter
    def sig_alg_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a0b677d5a94b179e1782a83ffab9e0dd85420e786a5d8d33fb349a6d22ac56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sigAlgName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @subject.setter
    def subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fad2b5f6125a965936d5ac6a50f498e8fc995c0753a7d34467c6829ca5cff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeNames")
    def subject_alternative_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subjectAlternativeNames"))

    @subject_alternative_names.setter
    def subject_alternative_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbcf18dbe9fa23c0b5b24af54a5a044b978c7fc14bf5303ed68d3885343aa70f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectAlternativeNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validFrom")
    def valid_from(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "validFrom"))

    @valid_from.setter
    def valid_from(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ba152c5173a3e3e39fa88b513b2385766bbaeb0b35fdbd218d36b00461c33d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validFrom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @version.setter
    def version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187188a22ee1b2140de5aea43dd761d585e912a6652f9b84312e31ba73a8ca31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd541ceabe972f4a742c2e857a7bc66b00fee5439909f725851ad5a1796857b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c0375050d00e78c85163f2f01b19fd2b6020243cf22a459843995cd1da868a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCertInfo")
    def put_cert_info(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0aca292df0f43ade4f207d13f6cf762ffd5c40507bbc25e964e0dd5e8ade07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCertInfo", [value]))

    @jsii.member(jsii_name="resetCertInfo")
    def reset_cert_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertInfo", []))

    @builtins.property
    @jsii.member(jsii_name="certInfo")
    def cert_info(self) -> GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList:
        return typing.cast(GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList, jsii.get(self, "certInfo"))

    @builtins.property
    @jsii.member(jsii_name="certInfoInput")
    def cert_info_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]], jsii.get(self, "certInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo]:
        return typing.cast(typing.Optional[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1e56d3a31801ada2904e3945cd04f4bc9a766d29c9c31f982d81dd52483950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFileConfig",
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
class GoogleApigeeKeystoresAliasesKeyCertFileConfig(
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
        cert: builtins.str,
        environment: builtins.str,
        keystore: builtins.str,
        org_id: builtins.str,
        certs_info: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApigeeKeystoresAliasesKeyCertFileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param alias: Alias Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#alias GoogleApigeeKeystoresAliasesKeyCertFile#alias}
        :param cert: Cert content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#cert GoogleApigeeKeystoresAliasesKeyCertFile#cert}
        :param environment: Environment associated with the alias. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#environment GoogleApigeeKeystoresAliasesKeyCertFile#environment}
        :param keystore: Keystore Name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#keystore GoogleApigeeKeystoresAliasesKeyCertFile#keystore}
        :param org_id: Organization ID associated with the alias. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#org_id GoogleApigeeKeystoresAliasesKeyCertFile#org_id}
        :param certs_info: certs_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#certs_info GoogleApigeeKeystoresAliasesKeyCertFile#certs_info}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#id GoogleApigeeKeystoresAliasesKeyCertFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key: Private Key content, omit if uploading to truststore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#key GoogleApigeeKeystoresAliasesKeyCertFile#key}
        :param password: Password for the Private Key if it's encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#password GoogleApigeeKeystoresAliasesKeyCertFile#password}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#timeouts GoogleApigeeKeystoresAliasesKeyCertFile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(certs_info, dict):
            certs_info = GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo(**certs_info)
        if isinstance(timeouts, dict):
            timeouts = GoogleApigeeKeystoresAliasesKeyCertFileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a0928fc833b1934468affce0f0a862f4933e573368b6430d0a9b503634c5c4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#alias GoogleApigeeKeystoresAliasesKeyCertFile#alias}
        '''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cert(self) -> builtins.str:
        '''Cert content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#cert GoogleApigeeKeystoresAliasesKeyCertFile#cert}
        '''
        result = self._values.get("cert")
        assert result is not None, "Required property 'cert' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(self) -> builtins.str:
        '''Environment associated with the alias.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#environment GoogleApigeeKeystoresAliasesKeyCertFile#environment}
        '''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keystore(self) -> builtins.str:
        '''Keystore Name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#keystore GoogleApigeeKeystoresAliasesKeyCertFile#keystore}
        '''
        result = self._values.get("keystore")
        assert result is not None, "Required property 'keystore' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''Organization ID associated with the alias.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#org_id GoogleApigeeKeystoresAliasesKeyCertFile#org_id}
        '''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certs_info(
        self,
    ) -> typing.Optional[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo]:
        '''certs_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#certs_info GoogleApigeeKeystoresAliasesKeyCertFile#certs_info}
        '''
        result = self._values.get("certs_info")
        return typing.cast(typing.Optional[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#id GoogleApigeeKeystoresAliasesKeyCertFile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Private Key content, omit if uploading to truststore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#key GoogleApigeeKeystoresAliasesKeyCertFile#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the Private Key if it's encrypted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#password GoogleApigeeKeystoresAliasesKeyCertFile#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleApigeeKeystoresAliasesKeyCertFileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#timeouts GoogleApigeeKeystoresAliasesKeyCertFile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApigeeKeystoresAliasesKeyCertFileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesKeyCertFileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFileTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class GoogleApigeeKeystoresAliasesKeyCertFileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#create GoogleApigeeKeystoresAliasesKeyCertFile#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#delete GoogleApigeeKeystoresAliasesKeyCertFile#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#read GoogleApigeeKeystoresAliasesKeyCertFile#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#update GoogleApigeeKeystoresAliasesKeyCertFile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244f4542afb876e959e251b480310ec6863d0a0273006393fbfdbc3bcd38190d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#create GoogleApigeeKeystoresAliasesKeyCertFile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#delete GoogleApigeeKeystoresAliasesKeyCertFile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#read GoogleApigeeKeystoresAliasesKeyCertFile#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_apigee_keystores_aliases_key_cert_file#update GoogleApigeeKeystoresAliasesKeyCertFile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApigeeKeystoresAliasesKeyCertFileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApigeeKeystoresAliasesKeyCertFile.GoogleApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5b8a670e69507115625c49ca00d1a935de56ebe73d5c22930fd06f8b0506cc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94c2702c8c92d30df387db53d7ac07f3c4c295e7a257d60897529c9cc3ad192c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1fbae691feb620bd342a9df3e88ac0cbfec708bedba1c96f32c2c1b0cd4d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c865c42787cc9444b1a12b23a67d34a47a44a4fc349de071340d870148f67032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cca38dffbc0e6252ad50930a4939cf04341d0a5e6d3b6da302a281b0f58a06f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesKeyCertFileTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesKeyCertFileTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesKeyCertFileTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e4af2252b3e89b30f802f550c4d8cf92e91aeda9c8b5cd3c85faa43cb2646c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApigeeKeystoresAliasesKeyCertFile",
    "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo",
    "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo",
    "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoList",
    "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfoOutputReference",
    "GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoOutputReference",
    "GoogleApigeeKeystoresAliasesKeyCertFileConfig",
    "GoogleApigeeKeystoresAliasesKeyCertFileTimeouts",
    "GoogleApigeeKeystoresAliasesKeyCertFileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__9616867104020a7250849818c439b00149f247df40355ccc5b624a8349889f34(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    alias: builtins.str,
    cert: builtins.str,
    environment: builtins.str,
    keystore: builtins.str,
    org_id: builtins.str,
    certs_info: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesKeyCertFileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__48ae4fbd691c44a085e32acd3f9381f1c60dc625fa6360d13e2cda1f5d943365(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab89cd3792d9b6a3b17471a2b4ab71861ef27d2017d2daa1c525592e224dde62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d670a0193b4db04f430a6d769eacd664fd21522b86bfb9236e0e1a2e7257a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9435111d611a7bdd260f4ca5fea758bdcb106a9af5333e95e83136b97babd5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dceff8d7e67835616a6ae36c0f119f7578fc94a9795f9cc104c380078fb616d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07e11a1268785b15b983c6cc3b08b35cae1cc9f6f79823ee1be0d6729bacaca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b734d18748750ca95990140b027209daed23aad2ae69ad2fc28fbfe3e12fd12d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681bcf6aa2be78dad2bd5c9b6bf86441c309768d1dbbf55b7e1f4b0a5d602293(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2826888c99575c63f11d2000ae7f6da9f0685d4abccadf2321fb60fb9f7809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced25291f3783dcbe954944193aa25105f831484f070ff84840761f91c7c18b5(
    *,
    cert_info: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72693781855d45c475471acfedaff367b74659894c6ea56c540c5fac61ea8fd6(
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

def _typecheckingstub__2b67e3701cb448372d527839e1a38a497fccced44a74f9ff2d30183dc2445bc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b82904e0c6226ddcbb1674c5fb1ddc635513d1ea49e695db6ca239a784c975(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c044c4f5728ef597ba95f7ed2fadf8a295bd3a18b88873054d9e0d9283d56899(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b6857b52f86f677f06483aacaf681646958b2ed21debab595a57e705040092(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d8a8b26bb673c183a41caae8ed2fe0841b4b094f3132e40e0c4552b34e7e8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195b0ef7d3d0b88b9f6d3cd0eaec78ff8840a6eb045db6c470885204fa121655(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e234908910e699227f4975c2097bb09dd25517f6822f22f920b5b8e1b4f82c7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3500650851cc5856560664d445214115f8d27e48ec5237c2dfc9cf9c7b085f28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ac030dc44c92035ce18dfc4d21df5726cd18f645448ed73a42b8b144bd0946(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc289a352e1b2a2a7913c10683ef69dbd3d128e69db8219086eec8bbc31e50b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6478e50ca29020df41d19de67fcc3ccb746e94850f5ad0c4bcb24bdfed2e55e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af7726471b30893492121c963876a7c138de29401cca07559ca135c9d393ba3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77725497419c3a973dcacdcfe2d3ff411de0a5a629fddd613872a439ca549f32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a0b677d5a94b179e1782a83ffab9e0dd85420e786a5d8d33fb349a6d22ac56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fad2b5f6125a965936d5ac6a50f498e8fc995c0753a7d34467c6829ca5cff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbcf18dbe9fa23c0b5b24af54a5a044b978c7fc14bf5303ed68d3885343aa70f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ba152c5173a3e3e39fa88b513b2385766bbaeb0b35fdbd218d36b00461c33d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187188a22ee1b2140de5aea43dd761d585e912a6652f9b84312e31ba73a8ca31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd541ceabe972f4a742c2e857a7bc66b00fee5439909f725851ad5a1796857b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c0375050d00e78c85163f2f01b19fd2b6020243cf22a459843995cd1da868a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0aca292df0f43ade4f207d13f6cf762ffd5c40507bbc25e964e0dd5e8ade07a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfoCertInfo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1e56d3a31801ada2904e3945cd04f4bc9a766d29c9c31f982d81dd52483950(
    value: typing.Optional[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a0928fc833b1934468affce0f0a862f4933e573368b6430d0a9b503634c5c4(
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
    certs_info: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesKeyCertFileCertsInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApigeeKeystoresAliasesKeyCertFileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244f4542afb876e959e251b480310ec6863d0a0273006393fbfdbc3bcd38190d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b8a670e69507115625c49ca00d1a935de56ebe73d5c22930fd06f8b0506cc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c2702c8c92d30df387db53d7ac07f3c4c295e7a257d60897529c9cc3ad192c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1fbae691feb620bd342a9df3e88ac0cbfec708bedba1c96f32c2c1b0cd4d6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c865c42787cc9444b1a12b23a67d34a47a44a4fc349de071340d870148f67032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cca38dffbc0e6252ad50930a4939cf04341d0a5e6d3b6da302a281b0f58a06f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e4af2252b3e89b30f802f550c4d8cf92e91aeda9c8b5cd3c85faa43cb2646c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApigeeKeystoresAliasesKeyCertFileTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
