r'''
# `google_binary_authorization_attestor`

Refer to the Terraform Registry for docs: [`google_binary_authorization_attestor`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor).
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


class BinaryAuthorizationAttestor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestor",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor google_binary_authorization_attestor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        attestation_authority_note: typing.Union["BinaryAuthorizationAttestorAttestationAuthorityNote", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BinaryAuthorizationAttestorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor google_binary_authorization_attestor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param attestation_authority_note: attestation_authority_note block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#attestation_authority_note BinaryAuthorizationAttestor#attestation_authority_note}
        :param name: The resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#name BinaryAuthorizationAttestor#name}
        :param description: A descriptive comment. This field may be updated. The field may be displayed in chooser dialogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#description BinaryAuthorizationAttestor#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#id BinaryAuthorizationAttestor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#project BinaryAuthorizationAttestor#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#timeouts BinaryAuthorizationAttestor#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f567e71805e07d1afbd3b4aa9c3bc0f4794fa1d3d7c31d1599ac4f38a53fd0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BinaryAuthorizationAttestorConfig(
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
        '''Generates CDKTF code for importing a BinaryAuthorizationAttestor resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BinaryAuthorizationAttestor to import.
        :param import_from_id: The id of the existing BinaryAuthorizationAttestor that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BinaryAuthorizationAttestor to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a77513520a54c808c066bdfdde8cc058f465f6db789bde5e6f19d328393af2)
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
        public_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param note_reference: The resource name of a ATTESTATION_AUTHORITY Note, created by the user. If the Note is in a different project from the Attestor, it should be specified in the format 'projects/* /notes/*' (or the legacy 'providers/* /notes/*'). This field may not be updated. An attestation by this attestor is stored as a Container Analysis ATTESTATION_AUTHORITY Occurrence that names a container image and that links to this Note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#note_reference BinaryAuthorizationAttestor#note_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param public_keys: public_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#public_keys BinaryAuthorizationAttestor#public_keys}
        '''
        value = BinaryAuthorizationAttestorAttestationAuthorityNote(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#create BinaryAuthorizationAttestor#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#delete BinaryAuthorizationAttestor#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#update BinaryAuthorizationAttestor#update}.
        '''
        value = BinaryAuthorizationAttestorTimeouts(
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
    ) -> "BinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference":
        return typing.cast("BinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference", jsii.get(self, "attestationAuthorityNote"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BinaryAuthorizationAttestorTimeoutsOutputReference":
        return typing.cast("BinaryAuthorizationAttestorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="attestationAuthorityNoteInput")
    def attestation_authority_note_input(
        self,
    ) -> typing.Optional["BinaryAuthorizationAttestorAttestationAuthorityNote"]:
        return typing.cast(typing.Optional["BinaryAuthorizationAttestorAttestationAuthorityNote"], jsii.get(self, "attestationAuthorityNoteInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BinaryAuthorizationAttestorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BinaryAuthorizationAttestorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f5be465e66c7bbcc1f8d85dc2e8654a8a43ef2770e53ade71a07cfb23bd04d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd966f6c883f4fd267895f91cc2003c615b0079c7b7debf55b14716c3fe3fa13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae07463e5e83c2da163297094a215a3e2e5d5a8565ab0d69c2bbd0d2c552b0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a26bde8e66c6d4011e8c383aee03362a3487c8c1935219b1a52c7fbab0c4959)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorAttestationAuthorityNote",
    jsii_struct_bases=[],
    name_mapping={"note_reference": "noteReference", "public_keys": "publicKeys"},
)
class BinaryAuthorizationAttestorAttestationAuthorityNote:
    def __init__(
        self,
        *,
        note_reference: builtins.str,
        public_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param note_reference: The resource name of a ATTESTATION_AUTHORITY Note, created by the user. If the Note is in a different project from the Attestor, it should be specified in the format 'projects/* /notes/*' (or the legacy 'providers/* /notes/*'). This field may not be updated. An attestation by this attestor is stored as a Container Analysis ATTESTATION_AUTHORITY Occurrence that names a container image and that links to this Note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#note_reference BinaryAuthorizationAttestor#note_reference} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param public_keys: public_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#public_keys BinaryAuthorizationAttestor#public_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41433a8229313046fa8a947407db85a03f371778a6e9482a5e00ce2e72347729)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#note_reference BinaryAuthorizationAttestor#note_reference}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("note_reference")
        assert result is not None, "Required property 'note_reference' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def public_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys"]]]:
        '''public_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#public_keys BinaryAuthorizationAttestor#public_keys}
        '''
        result = self._values.get("public_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationAttestorAttestationAuthorityNote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a44281a0ec0f1554ad306251acbac72a1dfcc7699d505772388b5bff440e12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPublicKeys")
    def put_public_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2769313748417212d174e128cce1bab8f482295d9aa359e510ef8da9e02bf20e)
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
    ) -> "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList":
        return typing.cast("BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList", jsii.get(self, "publicKeys"))

    @builtins.property
    @jsii.member(jsii_name="noteReferenceInput")
    def note_reference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noteReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeysInput")
    def public_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys"]]], jsii.get(self, "publicKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="noteReference")
    def note_reference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noteReference"))

    @note_reference.setter
    def note_reference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639bd9d4adee9a2642dd5acc51a9d168f4b8879b9745fe2b0cd45159ca376d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noteReference", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BinaryAuthorizationAttestorAttestationAuthorityNote]:
        return typing.cast(typing.Optional[BinaryAuthorizationAttestorAttestationAuthorityNote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BinaryAuthorizationAttestorAttestationAuthorityNote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a248ea9909dad509d98a6cdc726deb9323b5ef8766a7f71a70ebddcfe8345f85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys",
    jsii_struct_bases=[],
    name_mapping={
        "ascii_armored_pgp_public_key": "asciiArmoredPgpPublicKey",
        "comment": "comment",
        "id": "id",
        "pkix_public_key": "pkixPublicKey",
    },
)
class BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys:
    def __init__(
        self,
        *,
        ascii_armored_pgp_public_key: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pkix_public_key: typing.Optional[typing.Union["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ascii_armored_pgp_public_key: ASCII-armored representation of a PGP public key, as the entire output by the command 'gpg --export --armor foo@example.com' (either LF or CRLF line endings). When using this field, id should be left blank. The BinAuthz API handlers will calculate the ID and fill it in automatically. BinAuthz computes this ID as the OpenPGP RFC4880 V4 fingerprint, represented as upper-case hex. If id is provided by the caller, it will be overwritten by the API-calculated ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#ascii_armored_pgp_public_key BinaryAuthorizationAttestor#ascii_armored_pgp_public_key}
        :param comment: A descriptive comment. This field may be updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#comment BinaryAuthorizationAttestor#comment}
        :param id: The ID of this public key. Signatures verified by BinAuthz must include the ID of the public key that can be used to verify them, and that ID must match the contents of this field exactly. Additional restrictions on this field can be imposed based on which public key type is encapsulated. See the documentation on publicKey cases below for details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#id BinaryAuthorizationAttestor#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pkix_public_key: pkix_public_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#pkix_public_key BinaryAuthorizationAttestor#pkix_public_key}
        '''
        if isinstance(pkix_public_key, dict):
            pkix_public_key = BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey(**pkix_public_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dcbf83f71d8572184e01e017266b6d39d743e62543a1a44225ff08d88b059bb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#ascii_armored_pgp_public_key BinaryAuthorizationAttestor#ascii_armored_pgp_public_key}
        '''
        result = self._values.get("ascii_armored_pgp_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''A descriptive comment. This field may be updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#comment BinaryAuthorizationAttestor#comment}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#id BinaryAuthorizationAttestor#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pkix_public_key(
        self,
    ) -> typing.Optional["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey"]:
        '''pkix_public_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#pkix_public_key BinaryAuthorizationAttestor#pkix_public_key}
        '''
        result = self._values.get("pkix_public_key")
        return typing.cast(typing.Optional["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4f2d18dc1e323c2a9c2ce14d813bab5e037305a0606c732be2d341f40870756)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce3242738c21bf544ce4639103f709aa7bffb4ae9c892178c7f7677b4164e54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2707dee90dc8f9756dabc249a328ef89732df103ba712f75cccdc686924d9f59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1efa569c4c226b20088ecc9c1a4cfef1b0e8f0e1a85b68963689a0987ba499d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc33fbd821e0fd9fb25839dfed61d230781f3324255bb654f53ca3b6d8efaad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89a5cde05ff1891b03498777599789481feebbcfd95ed657b6b091fc609316f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f31f5d7d699baaa9e874cb8795fdc3c966660a97bb2ad9a4a3e044e6263b86e)
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
        :param public_key_pem: A PEM-encoded public key, as described in 'https://tools.ietf.org/html/rfc7468#section-13'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#public_key_pem BinaryAuthorizationAttestor#public_key_pem}
        :param signature_algorithm: The signature algorithm used to verify a message against a signature using this key. These signature algorithm must match the structure and any object identifiers encoded in publicKeyPem (i.e. this algorithm must match that of the public key). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#signature_algorithm BinaryAuthorizationAttestor#signature_algorithm}
        '''
        value = BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey(
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
    ) -> "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference":
        return typing.cast("BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference", jsii.get(self, "pkixPublicKey"))

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
    ) -> typing.Optional["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey"]:
        return typing.cast(typing.Optional["BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey"], jsii.get(self, "pkixPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="asciiArmoredPgpPublicKey")
    def ascii_armored_pgp_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "asciiArmoredPgpPublicKey"))

    @ascii_armored_pgp_public_key.setter
    def ascii_armored_pgp_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc6fe2f83fffbfc7cb4309f6e1457eeb32085ff57d6e44d0b9148d3db8dc752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asciiArmoredPgpPublicKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2f09a37560183ca7d4ba0383221e8877d66367c3f78946c3330c99fa5000b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31d823fc846aa3c0085dc1e6c08a8d9e256ae8552d20d65b7b9526a0b740f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c510601b4cf49e8c28d3df06a0c221f399e49d793c48c79f7a3a23050e582f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey",
    jsii_struct_bases=[],
    name_mapping={
        "public_key_pem": "publicKeyPem",
        "signature_algorithm": "signatureAlgorithm",
    },
)
class BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey:
    def __init__(
        self,
        *,
        public_key_pem: typing.Optional[builtins.str] = None,
        signature_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_key_pem: A PEM-encoded public key, as described in 'https://tools.ietf.org/html/rfc7468#section-13'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#public_key_pem BinaryAuthorizationAttestor#public_key_pem}
        :param signature_algorithm: The signature algorithm used to verify a message against a signature using this key. These signature algorithm must match the structure and any object identifiers encoded in publicKeyPem (i.e. this algorithm must match that of the public key). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#signature_algorithm BinaryAuthorizationAttestor#signature_algorithm}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae325955736f1711b3154cd3fb68bb7f8d3296324a6f0afa6d96fc95d979b451)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#public_key_pem BinaryAuthorizationAttestor#public_key_pem}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#signature_algorithm BinaryAuthorizationAttestor#signature_algorithm}
        '''
        result = self._values.get("signature_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38c7fa30fb4d6639dec3a1d4c2ffdf1b8bf35efef17e3e7aa4223a5b61c46fe1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af3d80e99914c1d5bb3befe5f1df635f14b1013123ab653eb668f981274b4ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKeyPem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signatureAlgorithm")
    def signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signatureAlgorithm"))

    @signature_algorithm.setter
    def signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f23457a9e6066a8136a731e30c5607cf3f1371d8416c152c7a21c8d4cd8d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signatureAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey]:
        return typing.cast(typing.Optional[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d03528d12253ff11b9334b444150cfe73d4a085f39983166a92badb3d2acb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorConfig",
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
class BinaryAuthorizationAttestorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        attestation_authority_note: typing.Union[BinaryAuthorizationAttestorAttestationAuthorityNote, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BinaryAuthorizationAttestorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param attestation_authority_note: attestation_authority_note block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#attestation_authority_note BinaryAuthorizationAttestor#attestation_authority_note}
        :param name: The resource name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#name BinaryAuthorizationAttestor#name}
        :param description: A descriptive comment. This field may be updated. The field may be displayed in chooser dialogs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#description BinaryAuthorizationAttestor#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#id BinaryAuthorizationAttestor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#project BinaryAuthorizationAttestor#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#timeouts BinaryAuthorizationAttestor#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(attestation_authority_note, dict):
            attestation_authority_note = BinaryAuthorizationAttestorAttestationAuthorityNote(**attestation_authority_note)
        if isinstance(timeouts, dict):
            timeouts = BinaryAuthorizationAttestorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1673a4578bb004bc09372b7aa10b90696efd75018777a565b4e72ba92953bf49)
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
    ) -> BinaryAuthorizationAttestorAttestationAuthorityNote:
        '''attestation_authority_note block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#attestation_authority_note BinaryAuthorizationAttestor#attestation_authority_note}
        '''
        result = self._values.get("attestation_authority_note")
        assert result is not None, "Required property 'attestation_authority_note' is missing"
        return typing.cast(BinaryAuthorizationAttestorAttestationAuthorityNote, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#name BinaryAuthorizationAttestor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A descriptive comment. This field may be updated. The field may be displayed in chooser dialogs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#description BinaryAuthorizationAttestor#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#id BinaryAuthorizationAttestor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#project BinaryAuthorizationAttestor#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BinaryAuthorizationAttestorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#timeouts BinaryAuthorizationAttestor#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BinaryAuthorizationAttestorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationAttestorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BinaryAuthorizationAttestorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#create BinaryAuthorizationAttestor#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#delete BinaryAuthorizationAttestor#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#update BinaryAuthorizationAttestor#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba9bcaf8c63e9473aceae7724ae341a2b0768477eaa29919a4c52a9e66a9b34)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#create BinaryAuthorizationAttestor#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#delete BinaryAuthorizationAttestor#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/binary_authorization_attestor#update BinaryAuthorizationAttestor#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BinaryAuthorizationAttestorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BinaryAuthorizationAttestorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.binaryAuthorizationAttestor.BinaryAuthorizationAttestorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20fc1f2b4ec3fb4eda72236f5b8b2d4df7dabd4f81d801b19624f9d7fee9354f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18949f5b5dc18a907bb2350ef9ec850db6c016bd535c2a68469f308a21f8292f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cebf1550b0318e12d379795bcec08c2558ae07c585a56b7cd08bf40d40c4f502)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d2e615de801004b37375bfe414dae096ac70907856ce6b9f620ba502fdba29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationAttestorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationAttestorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationAttestorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a183a67ca9dbabbfbd2434c146cf94d9907b2d9453eae221c5ca4f17dcba6200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BinaryAuthorizationAttestor",
    "BinaryAuthorizationAttestorAttestationAuthorityNote",
    "BinaryAuthorizationAttestorAttestationAuthorityNoteOutputReference",
    "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys",
    "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysList",
    "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysOutputReference",
    "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey",
    "BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKeyOutputReference",
    "BinaryAuthorizationAttestorConfig",
    "BinaryAuthorizationAttestorTimeouts",
    "BinaryAuthorizationAttestorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__90f567e71805e07d1afbd3b4aa9c3bc0f4794fa1d3d7c31d1599ac4f38a53fd0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    attestation_authority_note: typing.Union[BinaryAuthorizationAttestorAttestationAuthorityNote, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BinaryAuthorizationAttestorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__81a77513520a54c808c066bdfdde8cc058f465f6db789bde5e6f19d328393af2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f5be465e66c7bbcc1f8d85dc2e8654a8a43ef2770e53ade71a07cfb23bd04d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd966f6c883f4fd267895f91cc2003c615b0079c7b7debf55b14716c3fe3fa13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae07463e5e83c2da163297094a215a3e2e5d5a8565ab0d69c2bbd0d2c552b0f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a26bde8e66c6d4011e8c383aee03362a3487c8c1935219b1a52c7fbab0c4959(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41433a8229313046fa8a947407db85a03f371778a6e9482a5e00ce2e72347729(
    *,
    note_reference: builtins.str,
    public_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a44281a0ec0f1554ad306251acbac72a1dfcc7699d505772388b5bff440e12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2769313748417212d174e128cce1bab8f482295d9aa359e510ef8da9e02bf20e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639bd9d4adee9a2642dd5acc51a9d168f4b8879b9745fe2b0cd45159ca376d5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a248ea9909dad509d98a6cdc726deb9323b5ef8766a7f71a70ebddcfe8345f85(
    value: typing.Optional[BinaryAuthorizationAttestorAttestationAuthorityNote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dcbf83f71d8572184e01e017266b6d39d743e62543a1a44225ff08d88b059bb(
    *,
    ascii_armored_pgp_public_key: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pkix_public_key: typing.Optional[typing.Union[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f2d18dc1e323c2a9c2ce14d813bab5e037305a0606c732be2d341f40870756(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce3242738c21bf544ce4639103f709aa7bffb4ae9c892178c7f7677b4164e54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2707dee90dc8f9756dabc249a328ef89732df103ba712f75cccdc686924d9f59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1efa569c4c226b20088ecc9c1a4cfef1b0e8f0e1a85b68963689a0987ba499d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc33fbd821e0fd9fb25839dfed61d230781f3324255bb654f53ca3b6d8efaad8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89a5cde05ff1891b03498777599789481feebbcfd95ed657b6b091fc609316f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f31f5d7d699baaa9e874cb8795fdc3c966660a97bb2ad9a4a3e044e6263b86e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc6fe2f83fffbfc7cb4309f6e1457eeb32085ff57d6e44d0b9148d3db8dc752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2f09a37560183ca7d4ba0383221e8877d66367c3f78946c3330c99fa5000b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31d823fc846aa3c0085dc1e6c08a8d9e256ae8552d20d65b7b9526a0b740f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c510601b4cf49e8c28d3df06a0c221f399e49d793c48c79f7a3a23050e582f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeys]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae325955736f1711b3154cd3fb68bb7f8d3296324a6f0afa6d96fc95d979b451(
    *,
    public_key_pem: typing.Optional[builtins.str] = None,
    signature_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c7fa30fb4d6639dec3a1d4c2ffdf1b8bf35efef17e3e7aa4223a5b61c46fe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3d80e99914c1d5bb3befe5f1df635f14b1013123ab653eb668f981274b4ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f23457a9e6066a8136a731e30c5607cf3f1371d8416c152c7a21c8d4cd8d70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d03528d12253ff11b9334b444150cfe73d4a085f39983166a92badb3d2acb6(
    value: typing.Optional[BinaryAuthorizationAttestorAttestationAuthorityNotePublicKeysPkixPublicKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1673a4578bb004bc09372b7aa10b90696efd75018777a565b4e72ba92953bf49(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    attestation_authority_note: typing.Union[BinaryAuthorizationAttestorAttestationAuthorityNote, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BinaryAuthorizationAttestorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba9bcaf8c63e9473aceae7724ae341a2b0768477eaa29919a4c52a9e66a9b34(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fc1f2b4ec3fb4eda72236f5b8b2d4df7dabd4f81d801b19624f9d7fee9354f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18949f5b5dc18a907bb2350ef9ec850db6c016bd535c2a68469f308a21f8292f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebf1550b0318e12d379795bcec08c2558ae07c585a56b7cd08bf40d40c4f502(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d2e615de801004b37375bfe414dae096ac70907856ce6b9f620ba502fdba29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a183a67ca9dbabbfbd2434c146cf94d9907b2d9453eae221c5ca4f17dcba6200(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BinaryAuthorizationAttestorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
