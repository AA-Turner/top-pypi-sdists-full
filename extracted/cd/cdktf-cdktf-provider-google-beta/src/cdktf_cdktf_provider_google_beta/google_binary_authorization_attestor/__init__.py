r'''
# `google_binary_authorization_attestor`

Refer to the Terraform Registry for docs: [`google_binary_authorization_attestor`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor).
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


class GoogleBinaryAuthorizationAttestor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestor",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor google_binary_authorization_attestor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        attestation_authority_note: typing.Union["GoogleBinaryAuthorizationAttestorAttestationAuthorityNote", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBinaryAuthorizationAttestorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor google_binary_authorization_attestor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param attestation_authority_note: attestation_authority_note block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#attestation_authority_note GoogleBinaryAuthorizationAttestor#attestation_authority_note}
        :param name: The resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#name GoogleBinaryAuthorizationAttestor#name}
        :param description: A descriptive comment. This field may be updated. The field may be displayed in chooser dialogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#description GoogleBinaryAuthorizationAttestor#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#id GoogleBinaryAuthorizationAttestor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#project GoogleBinaryAuthorizationAttestor#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#timeouts GoogleBinaryAuthorizationAttestor#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a6a76e9c49a7bd4f321cbf83eaa8694c29fbbbe13b139bd4bae45974fc296f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBinaryAuthorizationAttestorConfig(
            attestation_authority_note=attestation_authority_note,
            name=name,
            description=description,
            id=id,
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
        '''Generates CDKTF code for importing a GoogleBinaryAuthorizationAttestor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBinaryAuthorizationAttestor to import.
        :param import_from_id: The id of the existing GoogleBinaryAuthorizationAttestor that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBinaryAuthorizationAttestor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d18179651f42e5b038217b0c91af3546d0fe391b3bae3a05c5be444017e38c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAttestationAuthorityNote")
    def put_attestation_authority_note(
        self,
        *,
        note_reference: builtins.str,
        public_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param note_reference: The resource name of a ATTESTATION_AUTHORITY Note, created by the user. If the Note is in a different project from the Attestor, it should be specified in the format 'projects/* /notes/*' (or the legacy 'providers/* /notes/*'). This field may not be updated. An attestation by this attestor is stored as a Container Analysis ATTESTATION_AUTHORITY Occurrence that names a container image and that links to this Note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#note_reference GoogleBinaryAuthorizationAttestor#note_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param public_keys: public_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#public_keys GoogleBinaryAuthorizationAttestor#public_keys}
        '''
        value = GoogleBinaryAuthorizationAttestorAttestationAuthorityNote(
            note_reference=note_reference, public_keys=public_keys
        )

        return typing.cast(None, jsii.invoke(self, "putAttestationAuthorityNote", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#create GoogleBinaryAuthorizationAttestor#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#delete GoogleBinaryAuthorizationAttestor#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#update GoogleBinaryAuthorizationAttestor#update}.
        '''
        value = GoogleBinaryAuthorizationAttestorTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="attestationAuthorityNote")
    def attestation_authority_note(
        self,
    ) -> "GoogleBinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference":
        return typing.cast("GoogleBinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference", jsii.get(self, "attestationAuthorityNote"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBinaryAuthorizationAttestorTimeoutsOutputReference":
        return typing.cast("GoogleBinaryAuthorizationAttestorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="attestationAuthorityNoteInput")
    def attestation_authority_note_input(
        self,
    ) -> typing.Optional["GoogleBinaryAuthorizationAttestorAttestationAuthorityNote"]:
        return typing.cast(typing.Optional["GoogleBinaryAuthorizationAttestorAttestationAuthorityNote"], jsii.get(self, "attestationAuthorityNoteInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBinaryAuthorizationAttestorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBinaryAuthorizationAttestorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ab4e887f427401d75b3f6896924be06d030660c3554157176676cfb6a6930b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1932da81f9fe48872f15ed0a93168d95db2fb4b4e79f26e9bfac694538383ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de535051a66a8cd9e2a99a211c11b0a45baf16ad02b02596a24f6abf827c574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798807a5d5859c73772735aa6985717673e6977378a4b6242b8d807fb96acd24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorAttestationAuthorityNote",
    jsii_struct_bases=[],
    name_mapping={"note_reference": "noteReference", "public_keys": "publicKeys"},
)
class GoogleBinaryAuthorizationAttestorAttestationAuthorityNote:
    def __init__(
        self,
        *,
        note_reference: builtins.str,
        public_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param note_reference: The resource name of a ATTESTATION_AUTHORITY Note, created by the user. If the Note is in a different project from the Attestor, it should be specified in the format 'projects/* /notes/*' (or the legacy 'providers/* /notes/*'). This field may not be updated. An attestation by this attestor is stored as a Container Analysis ATTESTATION_AUTHORITY Occurrence that names a container image and that links to this Note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#note_reference GoogleBinaryAuthorizationAttestor#note_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param public_keys: public_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#public_keys GoogleBinaryAuthorizationAttestor#public_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02735779df0ce53869d2909f295b45c98e8cf2080dffd1550d8abb515acc6e60)
            check_type(argname="argument note_reference", value=note_reference, expected_type=type_hints["note_reference"])
            check_type(argname="argument public_keys", value=public_keys, expected_type=type_hints["public_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "note_reference": note_reference,
        }
        if public_keys is not None:
            self._values["public_keys"] = public_keys

    @builtins.property
    def note_reference(self) -> builtins.str:
        '''The resource name of a ATTESTATION_AUTHORITY Note, created by the user.

        If the Note is in a different project from the Attestor, it
        should be specified in the format 'projects/* /notes/*' (or the legacy
        'providers/* /notes/*'). This field may not be updated.
        An attestation by this attestor is stored as a Container Analysis
        ATTESTATION_AUTHORITY Occurrence that names a container image
        and that links to this Note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#note_reference GoogleBinaryAuthorizationAttestor#note_reference}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("note_reference")
        assert result is not None, "Required property 'note_reference' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def public_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys"]]]:
        '''public_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#public_keys GoogleBinaryAuthorizationAttestor#public_keys}
        '''
        result = self._values.get("public_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationAttestorAttestationAuthorityNote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ba6ecc658d19926c4efb197a3b22f9db5e073bc29683d7fc3617a3e94225865)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPublicKeys")
    def put_public_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5608b21d785499536040f9394d147a913fa7205723b401ef873651da9ce4e2b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPublicKeys", [value]))

    @jsii.member(jsii_name="resetPublicKeys")
    def reset_public_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKeys", []))

    @builtins.property
    @jsii.member(jsii_name="delegationServiceAccountEmail")
    def delegation_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delegationServiceAccountEmail"))

    @builtins.property
    @jsii.member(jsii_name="publicKeys")
    def public_keys(
        self,
    ) -> "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList":
        return typing.cast("GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList", jsii.get(self, "publicKeys"))

    @builtins.property
    @jsii.member(jsii_name="noteReferenceInput")
    def note_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noteReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeysInput")
    def public_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys"]]], jsii.get(self, "publicKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="noteReference")
    def note_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noteReference"))

    @note_reference.setter
    def note_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2be8f403d14084ac18a649c5c9b7edb983f5466b043f77dc9230d8518784524)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noteReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBinaryAuthorizationAttestorAttestationAuthorityNote]:
        return typing.cast(typing.Optional[GoogleBinaryAuthorizationAttestorAttestationAuthorityNote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBinaryAuthorizationAttestorAttestationAuthorityNote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377e3f49e6db80257f2d023a91a47e9e600cecd88c720399fff584c46e36f0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys",
    jsii_struct_bases=[],
    name_mapping={
        "ascii_armored_pgp_public_key": "asciiArmoredPgpPublicKey",
        "comment": "comment",
        "id": "id",
        "pkix_public_key": "pkixPublicKey",
    },
)
class GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys:
    def __init__(
        self,
        *,
        ascii_armored_pgp_public_key: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pkix_public_key: typing.Optional[typing.Union["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ascii_armored_pgp_public_key: ASCII-armored representation of a PGP public key, as the entire output by the command 'gpg --export --armor foo@example.com' (either LF or CRLF line endings). When using this field, id should be left blank. The BinAuthz API handlers will calculate the ID and fill it in automatically. BinAuthz computes this ID as the OpenPGP RFC4880 V4 fingerprint, represented as upper-case hex. If id is provided by the caller, it will be overwritten by the API-calculated ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#ascii_armored_pgp_public_key GoogleBinaryAuthorizationAttestor#ascii_armored_pgp_public_key}
        :param comment: A descriptive comment. This field may be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#comment GoogleBinaryAuthorizationAttestor#comment}
        :param id: The ID of this public key. Signatures verified by BinAuthz must include the ID of the public key that can be used to verify them, and that ID must match the contents of this field exactly. Additional restrictions on this field can be imposed based on which public key type is encapsulated. See the documentation on publicKey cases below for details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#id GoogleBinaryAuthorizationAttestor#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pkix_public_key: pkix_public_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#pkix_public_key GoogleBinaryAuthorizationAttestor#pkix_public_key}
        '''
        if isinstance(pkix_public_key, dict):
            pkix_public_key = GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey(**pkix_public_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48561a603c167cf2fdbd6004397a06c27f6e3a41202dd8d37ebce967dedf305b)
            check_type(argname="argument ascii_armored_pgp_public_key", value=ascii_armored_pgp_public_key, expected_type=type_hints["ascii_armored_pgp_public_key"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pkix_public_key", value=pkix_public_key, expected_type=type_hints["pkix_public_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ascii_armored_pgp_public_key is not None:
            self._values["ascii_armored_pgp_public_key"] = ascii_armored_pgp_public_key
        if comment is not None:
            self._values["comment"] = comment
        if id is not None:
            self._values["id"] = id
        if pkix_public_key is not None:
            self._values["pkix_public_key"] = pkix_public_key

    @builtins.property
    def ascii_armored_pgp_public_key(self) -> typing.Optional[builtins.str]:
        '''ASCII-armored representation of a PGP public key, as the entire output by the command 'gpg --export --armor foo@example.com' (either LF or CRLF line endings). When using this field, id should be left blank. The BinAuthz API handlers will calculate the ID and fill it in automatically. BinAuthz computes this ID as the OpenPGP RFC4880 V4 fingerprint, represented as upper-case hex. If id is provided by the caller, it will be overwritten by the API-calculated ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#ascii_armored_pgp_public_key GoogleBinaryAuthorizationAttestor#ascii_armored_pgp_public_key}
        '''
        result = self._values.get("ascii_armored_pgp_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''A descriptive comment. This field may be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#comment GoogleBinaryAuthorizationAttestor#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The ID of this public key.

        Signatures verified by BinAuthz
        must include the ID of the public key that can be used to
        verify them, and that ID must match the contents of this
        field exactly. Additional restrictions on this field can
        be imposed based on which public key type is encapsulated.
        See the documentation on publicKey cases below for details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#id GoogleBinaryAuthorizationAttestor#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pkix_public_key(
        self,
    ) -> typing.Optional["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey"]:
        '''pkix_public_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#pkix_public_key GoogleBinaryAuthorizationAttestor#pkix_public_key}
        '''
        result = self._values.get("pkix_public_key")
        return typing.cast(typing.Optional["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57de146f2f6580d6c86c0211096c78cf8f3bc3cbbc7a214dc984fa14f7517249)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682b956e1bf6f3fba877389fc39a11389c1668bc42ab174155fc81a1c39d6108)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f934bb92aa25e7bff3aa05db7bcb550ddf64977ffb2a1dc5e4a56a0e6db86019)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fab06f01fcc8c84049a503e74286eabe5327be703c62d64e7a25f7d059a1b35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89b1d013befc41dbf30d015ea17bceaf45fd9e2d64a14eb5205229546bbfc909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e0b5248283ff4c0064e26ccc6df488e2f9d51574a923eaba486ce67d762ad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b47393c3e679c2cb4b130470352205aa63cc675d0384cac077bbece474331257)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPkixPublicKey")
    def put_pkix_public_key(
        self,
        *,
        public_key_pem: typing.Optional[builtins.str] = None,
        signature_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_key_pem: A PEM-encoded public key, as described in 'https://tools.ietf.org/html/rfc7468#section-13'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#public_key_pem GoogleBinaryAuthorizationAttestor#public_key_pem}
        :param signature_algorithm: The signature algorithm used to verify a message against a signature using this key. These signature algorithm must match the structure and any object identifiers encoded in publicKeyPem (i.e. this algorithm must match that of the public key). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#signature_algorithm GoogleBinaryAuthorizationAttestor#signature_algorithm}
        '''
        value = GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey(
            public_key_pem=public_key_pem, signature_algorithm=signature_algorithm
        )

        return typing.cast(None, jsii.invoke(self, "putPkixPublicKey", [value]))

    @jsii.member(jsii_name="resetAsciiArmoredPgpPublicKey")
    def reset_ascii_armored_pgp_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsciiArmoredPgpPublicKey", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPkixPublicKey")
    def reset_pkix_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPkixPublicKey", []))

    @builtins.property
    @jsii.member(jsii_name="pkixPublicKey")
    def pkix_public_key(
        self,
    ) -> "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference":
        return typing.cast("GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference", jsii.get(self, "pkixPublicKey"))

    @builtins.property
    @jsii.member(jsii_name="asciiArmoredPgpPublicKeyInput")
    def ascii_armored_pgp_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "asciiArmoredPgpPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="pkixPublicKeyInput")
    def pkix_public_key_input(
        self,
    ) -> typing.Optional["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey"]:
        return typing.cast(typing.Optional["GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey"], jsii.get(self, "pkixPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="asciiArmoredPgpPublicKey")
    def ascii_armored_pgp_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "asciiArmoredPgpPublicKey"))

    @ascii_armored_pgp_public_key.setter
    def ascii_armored_pgp_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d313336d679562ec8e0d33d0e9cbb57b8990413c067af7ab436a47c4e628e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asciiArmoredPgpPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6df20856574d121505ac12f8d13cae8945d77d99f3367c3056a4e4d45b0f7d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0733b584924e7c491c78d6dc063daba3d8dca7deecd6b9a095d9c3e0f8f9d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba58085de05386c67277191dbf99e3ec3a2167677bdd26da34773558272fa51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey",
    jsii_struct_bases=[],
    name_mapping={
        "public_key_pem": "publicKeyPem",
        "signature_algorithm": "signatureAlgorithm",
    },
)
class GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey:
    def __init__(
        self,
        *,
        public_key_pem: typing.Optional[builtins.str] = None,
        signature_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_key_pem: A PEM-encoded public key, as described in 'https://tools.ietf.org/html/rfc7468#section-13'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#public_key_pem GoogleBinaryAuthorizationAttestor#public_key_pem}
        :param signature_algorithm: The signature algorithm used to verify a message against a signature using this key. These signature algorithm must match the structure and any object identifiers encoded in publicKeyPem (i.e. this algorithm must match that of the public key). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#signature_algorithm GoogleBinaryAuthorizationAttestor#signature_algorithm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9a0049769f376a77c7159ccb69ffb8410f5e04707b81f96c5e2241c280550b)
            check_type(argname="argument public_key_pem", value=public_key_pem, expected_type=type_hints["public_key_pem"])
            check_type(argname="argument signature_algorithm", value=signature_algorithm, expected_type=type_hints["signature_algorithm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_key_pem is not None:
            self._values["public_key_pem"] = public_key_pem
        if signature_algorithm is not None:
            self._values["signature_algorithm"] = signature_algorithm

    @builtins.property
    def public_key_pem(self) -> typing.Optional[builtins.str]:
        '''A PEM-encoded public key, as described in 'https://tools.ietf.org/html/rfc7468#section-13'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#public_key_pem GoogleBinaryAuthorizationAttestor#public_key_pem}
        '''
        result = self._values.get("public_key_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_algorithm(self) -> typing.Optional[builtins.str]:
        '''The signature algorithm used to verify a message against a signature using this key.

        These signature algorithm must
        match the structure and any object identifiers encoded in
        publicKeyPem (i.e. this algorithm must match that of the
        public key).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#signature_algorithm GoogleBinaryAuthorizationAttestor#signature_algorithm}
        '''
        result = self._values.get("signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d96c6b3ab6cd1e8d7502b9b1fff76a1b91c55c5e8dd358fdaefd9693ea4b793)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPublicKeyPem")
    def reset_public_key_pem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKeyPem", []))

    @jsii.member(jsii_name="resetSignatureAlgorithm")
    def reset_signature_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignatureAlgorithm", []))

    @builtins.property
    @jsii.member(jsii_name="publicKeyPemInput")
    def public_key_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyPemInput"))

    @builtins.property
    @jsii.member(jsii_name="signatureAlgorithmInput")
    def signature_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signatureAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyPem")
    def public_key_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKeyPem"))

    @public_key_pem.setter
    def public_key_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7550648ccbf09ed7f9edbf247c6ff2573fd09b4567ea721d87e2de24da336616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKeyPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signatureAlgorithm")
    def signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signatureAlgorithm"))

    @signature_algorithm.setter
    def signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3f70cee76fe54d79354e0d0adf1551069283779901869a3fbe06bf5b71f3f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey]:
        return typing.cast(typing.Optional[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafe96623b8038ef0cc9d8749b31e45c1bdd6e5822d693116f7623e0b228e70e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "attestation_authority_note": "attestationAuthorityNote",
        "name": "name",
        "description": "description",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleBinaryAuthorizationAttestorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        attestation_authority_note: typing.Union[GoogleBinaryAuthorizationAttestorAttestationAuthorityNote, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBinaryAuthorizationAttestorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param attestation_authority_note: attestation_authority_note block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#attestation_authority_note GoogleBinaryAuthorizationAttestor#attestation_authority_note}
        :param name: The resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#name GoogleBinaryAuthorizationAttestor#name}
        :param description: A descriptive comment. This field may be updated. The field may be displayed in chooser dialogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#description GoogleBinaryAuthorizationAttestor#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#id GoogleBinaryAuthorizationAttestor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#project GoogleBinaryAuthorizationAttestor#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#timeouts GoogleBinaryAuthorizationAttestor#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(attestation_authority_note, dict):
            attestation_authority_note = GoogleBinaryAuthorizationAttestorAttestationAuthorityNote(**attestation_authority_note)
        if isinstance(timeouts, dict):
            timeouts = GoogleBinaryAuthorizationAttestorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fb2508c56f470f626b88e9bf6018c91983d0933feaa20722e6e3372b4333769)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument attestation_authority_note", value=attestation_authority_note, expected_type=type_hints["attestation_authority_note"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attestation_authority_note": attestation_authority_note,
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
    def attestation_authority_note(
        self,
    ) -> GoogleBinaryAuthorizationAttestorAttestationAuthorityNote:
        '''attestation_authority_note block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#attestation_authority_note GoogleBinaryAuthorizationAttestor#attestation_authority_note}
        '''
        result = self._values.get("attestation_authority_note")
        assert result is not None, "Required property 'attestation_authority_note' is missing"
        return typing.cast(GoogleBinaryAuthorizationAttestorAttestationAuthorityNote, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#name GoogleBinaryAuthorizationAttestor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A descriptive comment. This field may be updated. The field may be displayed in chooser dialogs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#description GoogleBinaryAuthorizationAttestor#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#id GoogleBinaryAuthorizationAttestor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#project GoogleBinaryAuthorizationAttestor#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBinaryAuthorizationAttestorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#timeouts GoogleBinaryAuthorizationAttestor#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBinaryAuthorizationAttestorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationAttestorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBinaryAuthorizationAttestorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#create GoogleBinaryAuthorizationAttestor#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#delete GoogleBinaryAuthorizationAttestor#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#update GoogleBinaryAuthorizationAttestor#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e6858f5a76ad0fa066fdb73143f36b13dc4ea7ba5948358c7289f5f049b4f3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#create GoogleBinaryAuthorizationAttestor#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#delete GoogleBinaryAuthorizationAttestor#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_binary_authorization_attestor#update GoogleBinaryAuthorizationAttestor#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBinaryAuthorizationAttestorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBinaryAuthorizationAttestorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBinaryAuthorizationAttestor.GoogleBinaryAuthorizationAttestorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81862566597fee5839a9b363f749aaac160ab1983473cb14678a269e29dd8a46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49862445dc52e4315db1c78830a24d45c3382e13a1f113dfb5dd849bcea24c43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34bcf90b0fcf0598fe8dd97d01c50137a5b03381ee3e2bd6e9d348791502c790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47fdbfdd707cad2c78ecbdcff182ce17a203b0a8a47614e2779cd69ff92a1ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationAttestorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationAttestorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationAttestorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1c905cbc4ff11fe68c37b035f715ac1e7d2f4bc672d2b09a32794a33b957d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBinaryAuthorizationAttestor",
    "GoogleBinaryAuthorizationAttestorAttestationAuthorityNote",
    "GoogleBinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference",
    "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys",
    "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList",
    "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference",
    "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey",
    "GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference",
    "GoogleBinaryAuthorizationAttestorConfig",
    "GoogleBinaryAuthorizationAttestorTimeouts",
    "GoogleBinaryAuthorizationAttestorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__82a6a76e9c49a7bd4f321cbf83eaa8694c29fbbbe13b139bd4bae45974fc296f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    attestation_authority_note: typing.Union[GoogleBinaryAuthorizationAttestorAttestationAuthorityNote, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBinaryAuthorizationAttestorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__92d18179651f42e5b038217b0c91af3546d0fe391b3bae3a05c5be444017e38c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ab4e887f427401d75b3f6896924be06d030660c3554157176676cfb6a6930b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1932da81f9fe48872f15ed0a93168d95db2fb4b4e79f26e9bfac694538383ef4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de535051a66a8cd9e2a99a211c11b0a45baf16ad02b02596a24f6abf827c574(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798807a5d5859c73772735aa6985717673e6977378a4b6242b8d807fb96acd24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02735779df0ce53869d2909f295b45c98e8cf2080dffd1550d8abb515acc6e60(
    *,
    note_reference: builtins.str,
    public_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba6ecc658d19926c4efb197a3b22f9db5e073bc29683d7fc3617a3e94225865(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5608b21d785499536040f9394d147a913fa7205723b401ef873651da9ce4e2b4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2be8f403d14084ac18a649c5c9b7edb983f5466b043f77dc9230d8518784524(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377e3f49e6db80257f2d023a91a47e9e600cecd88c720399fff584c46e36f0d7(
    value: typing.Optional[GoogleBinaryAuthorizationAttestorAttestationAuthorityNote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48561a603c167cf2fdbd6004397a06c27f6e3a41202dd8d37ebce967dedf305b(
    *,
    ascii_armored_pgp_public_key: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pkix_public_key: typing.Optional[typing.Union[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57de146f2f6580d6c86c0211096c78cf8f3bc3cbbc7a214dc984fa14f7517249(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682b956e1bf6f3fba877389fc39a11389c1668bc42ab174155fc81a1c39d6108(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f934bb92aa25e7bff3aa05db7bcb550ddf64977ffb2a1dc5e4a56a0e6db86019(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fab06f01fcc8c84049a503e74286eabe5327be703c62d64e7a25f7d059a1b35(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b1d013befc41dbf30d015ea17bceaf45fd9e2d64a14eb5205229546bbfc909(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e0b5248283ff4c0064e26ccc6df488e2f9d51574a923eaba486ce67d762ad3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47393c3e679c2cb4b130470352205aa63cc675d0384cac077bbece474331257(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d313336d679562ec8e0d33d0e9cbb57b8990413c067af7ab436a47c4e628e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6df20856574d121505ac12f8d13cae8945d77d99f3367c3056a4e4d45b0f7d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0733b584924e7c491c78d6dc063daba3d8dca7deecd6b9a095d9c3e0f8f9d1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba58085de05386c67277191dbf99e3ec3a2167677bdd26da34773558272fa51(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9a0049769f376a77c7159ccb69ffb8410f5e04707b81f96c5e2241c280550b(
    *,
    public_key_pem: typing.Optional[builtins.str] = None,
    signature_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d96c6b3ab6cd1e8d7502b9b1fff76a1b91c55c5e8dd358fdaefd9693ea4b793(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7550648ccbf09ed7f9edbf247c6ff2573fd09b4567ea721d87e2de24da336616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3f70cee76fe54d79354e0d0adf1551069283779901869a3fbe06bf5b71f3f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafe96623b8038ef0cc9d8749b31e45c1bdd6e5822d693116f7623e0b228e70e(
    value: typing.Optional[GoogleBinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fb2508c56f470f626b88e9bf6018c91983d0933feaa20722e6e3372b4333769(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    attestation_authority_note: typing.Union[GoogleBinaryAuthorizationAttestorAttestationAuthorityNote, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBinaryAuthorizationAttestorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e6858f5a76ad0fa066fdb73143f36b13dc4ea7ba5948358c7289f5f049b4f3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81862566597fee5839a9b363f749aaac160ab1983473cb14678a269e29dd8a46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49862445dc52e4315db1c78830a24d45c3382e13a1f113dfb5dd849bcea24c43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34bcf90b0fcf0598fe8dd97d01c50137a5b03381ee3e2bd6e9d348791502c790(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47fdbfdd707cad2c78ecbdcff182ce17a203b0a8a47614e2779cd69ff92a1ba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1c905cbc4ff11fe68c37b035f715ac1e7d2f4bc672d2b09a32794a33b957d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBinaryAuthorizationAttestorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
