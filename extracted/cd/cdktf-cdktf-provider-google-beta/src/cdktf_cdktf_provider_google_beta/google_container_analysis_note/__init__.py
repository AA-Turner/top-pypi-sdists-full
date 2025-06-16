r'''
# `google_container_analysis_note`

Refer to the Terraform Registry for docs: [`google_container_analysis_note`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note).
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


class GoogleContainerAnalysisNote(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNote",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note google_container_analysis_note}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        attestation_authority: typing.Union["GoogleContainerAnalysisNoteAttestationAuthority", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        long_description: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        related_note_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        related_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAnalysisNoteRelatedUrl", typing.Dict[builtins.str, typing.Any]]]]] = None,
        short_description: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAnalysisNoteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note google_container_analysis_note} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param attestation_authority: attestation_authority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#attestation_authority GoogleContainerAnalysisNote#attestation_authority}
        :param name: The name of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#name GoogleContainerAnalysisNote#name}
        :param expiration_time: Time of expiration for this note. Leave empty if note does not expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#expiration_time GoogleContainerAnalysisNote#expiration_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#id GoogleContainerAnalysisNote#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param long_description: A detailed description of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#long_description GoogleContainerAnalysisNote#long_description}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#project GoogleContainerAnalysisNote#project}.
        :param related_note_names: Names of other notes related to this note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#related_note_names GoogleContainerAnalysisNote#related_note_names}
        :param related_url: related_url block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#related_url GoogleContainerAnalysisNote#related_url}
        :param short_description: A one sentence description of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#short_description GoogleContainerAnalysisNote#short_description}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#timeouts GoogleContainerAnalysisNote#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2067233c5bd30060da0ef2b3289a1d8546bba306667bbf4b8ebcc8fa02845bb4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleContainerAnalysisNoteConfig(
            attestation_authority=attestation_authority,
            name=name,
            expiration_time=expiration_time,
            id=id,
            long_description=long_description,
            project=project,
            related_note_names=related_note_names,
            related_url=related_url,
            short_description=short_description,
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
        '''Generates CDKTF code for importing a GoogleContainerAnalysisNote resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleContainerAnalysisNote to import.
        :param import_from_id: The id of the existing GoogleContainerAnalysisNote that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleContainerAnalysisNote to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244d0daa8551827e9ad00f74c12d841e6280d3a927d1926d32ff1c4940f33073)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAttestationAuthority")
    def put_attestation_authority(
        self,
        *,
        hint: typing.Union["GoogleContainerAnalysisNoteAttestationAuthorityHint", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hint: hint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#hint GoogleContainerAnalysisNote#hint}
        '''
        value = GoogleContainerAnalysisNoteAttestationAuthority(hint=hint)

        return typing.cast(None, jsii.invoke(self, "putAttestationAuthority", [value]))

    @jsii.member(jsii_name="putRelatedUrl")
    def put_related_url(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAnalysisNoteRelatedUrl", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4586177a31afd08f5f7e52c8935bb743196a21acffc89780d86bf2c65d31e983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRelatedUrl", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#create GoogleContainerAnalysisNote#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#delete GoogleContainerAnalysisNote#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#update GoogleContainerAnalysisNote#update}.
        '''
        value = GoogleContainerAnalysisNoteTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetExpirationTime")
    def reset_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationTime", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLongDescription")
    def reset_long_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongDescription", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRelatedNoteNames")
    def reset_related_note_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelatedNoteNames", []))

    @jsii.member(jsii_name="resetRelatedUrl")
    def reset_related_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelatedUrl", []))

    @jsii.member(jsii_name="resetShortDescription")
    def reset_short_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShortDescription", []))

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
    @jsii.member(jsii_name="attestationAuthority")
    def attestation_authority(
        self,
    ) -> "GoogleContainerAnalysisNoteAttestationAuthorityOutputReference":
        return typing.cast("GoogleContainerAnalysisNoteAttestationAuthorityOutputReference", jsii.get(self, "attestationAuthority"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="relatedUrl")
    def related_url(self) -> "GoogleContainerAnalysisNoteRelatedUrlList":
        return typing.cast("GoogleContainerAnalysisNoteRelatedUrlList", jsii.get(self, "relatedUrl"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleContainerAnalysisNoteTimeoutsOutputReference":
        return typing.cast("GoogleContainerAnalysisNoteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="attestationAuthorityInput")
    def attestation_authority_input(
        self,
    ) -> typing.Optional["GoogleContainerAnalysisNoteAttestationAuthority"]:
        return typing.cast(typing.Optional["GoogleContainerAnalysisNoteAttestationAuthority"], jsii.get(self, "attestationAuthorityInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTimeInput")
    def expiration_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="longDescriptionInput")
    def long_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "longDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="relatedNoteNamesInput")
    def related_note_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "relatedNoteNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="relatedUrlInput")
    def related_url_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAnalysisNoteRelatedUrl"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAnalysisNoteRelatedUrl"]]], jsii.get(self, "relatedUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="shortDescriptionInput")
    def short_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shortDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAnalysisNoteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAnalysisNoteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @expiration_time.setter
    def expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1ae54ead3837ef78a7726403740e5ec15dcf86b0476c277889d08ceb6ba024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6fb6fcbe03bcf42fca5041376c1bafcd2f1a9582b258c74839792617d79d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longDescription")
    def long_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "longDescription"))

    @long_description.setter
    def long_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05659e38bf0fa299efb1f1be08922d370a87a05be3e13cbe59578286c58b801d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa0a29434e19576f430250307db373ffd17c81f5ba8dff1fd9619c154f85ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2c16471b78de1d86af0e69b56c2a9f594fe455ae72e92f1c4fbc4a4436b69f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relatedNoteNames")
    def related_note_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "relatedNoteNames"))

    @related_note_names.setter
    def related_note_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd11af5ecc6ee4b0729929351d892996c73e62811ca8aab736b49711933af71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relatedNoteNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shortDescription")
    def short_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shortDescription"))

    @short_description.setter
    def short_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6a9ee0bca46b75ed694a8aeb29381ee46ccca4628c6994f70aa17278dc410f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shortDescription", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteAttestationAuthority",
    jsii_struct_bases=[],
    name_mapping={"hint": "hint"},
)
class GoogleContainerAnalysisNoteAttestationAuthority:
    def __init__(
        self,
        *,
        hint: typing.Union["GoogleContainerAnalysisNoteAttestationAuthorityHint", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hint: hint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#hint GoogleContainerAnalysisNote#hint}
        '''
        if isinstance(hint, dict):
            hint = GoogleContainerAnalysisNoteAttestationAuthorityHint(**hint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8828c4ccfb5e15bc21e3ff2d965bb8d0733bbe45948f674d4afa8d0218ec7f)
            check_type(argname="argument hint", value=hint, expected_type=type_hints["hint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hint": hint,
        }

    @builtins.property
    def hint(self) -> "GoogleContainerAnalysisNoteAttestationAuthorityHint":
        '''hint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#hint GoogleContainerAnalysisNote#hint}
        '''
        result = self._values.get("hint")
        assert result is not None, "Required property 'hint' is missing"
        return typing.cast("GoogleContainerAnalysisNoteAttestationAuthorityHint", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAnalysisNoteAttestationAuthority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteAttestationAuthorityHint",
    jsii_struct_bases=[],
    name_mapping={"human_readable_name": "humanReadableName"},
)
class GoogleContainerAnalysisNoteAttestationAuthorityHint:
    def __init__(self, *, human_readable_name: builtins.str) -> None:
        '''
        :param human_readable_name: The human readable name of this Attestation Authority, for example "qa". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#human_readable_name GoogleContainerAnalysisNote#human_readable_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58564c3a777764adec323c2af0d2458a42c7f70b6e926ea2c6f1e7c3d30707bb)
            check_type(argname="argument human_readable_name", value=human_readable_name, expected_type=type_hints["human_readable_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "human_readable_name": human_readable_name,
        }

    @builtins.property
    def human_readable_name(self) -> builtins.str:
        '''The human readable name of this Attestation Authority, for example "qa".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#human_readable_name GoogleContainerAnalysisNote#human_readable_name}
        '''
        result = self._values.get("human_readable_name")
        assert result is not None, "Required property 'human_readable_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAnalysisNoteAttestationAuthorityHint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAnalysisNoteAttestationAuthorityHintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteAttestationAuthorityHintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99717ffa077f65d291f281717c79b4da6d3bc80be16815d15b3918992263858f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="humanReadableNameInput")
    def human_readable_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "humanReadableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="humanReadableName")
    def human_readable_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "humanReadableName"))

    @human_readable_name.setter
    def human_readable_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735f00053dff85892cd2a2f226dcc77c438ca45c925709b4b89397a0ad00e4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "humanReadableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAnalysisNoteAttestationAuthorityHint]:
        return typing.cast(typing.Optional[GoogleContainerAnalysisNoteAttestationAuthorityHint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAnalysisNoteAttestationAuthorityHint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3f09785409a0f482589abcfbdce5bfb8851d437477b88e9da1642e35594a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAnalysisNoteAttestationAuthorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteAttestationAuthorityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bceec43e5cb19ebf195c290d032872ed2529594135b487b58ce02a83c98ff2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHint")
    def put_hint(self, *, human_readable_name: builtins.str) -> None:
        '''
        :param human_readable_name: The human readable name of this Attestation Authority, for example "qa". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#human_readable_name GoogleContainerAnalysisNote#human_readable_name}
        '''
        value = GoogleContainerAnalysisNoteAttestationAuthorityHint(
            human_readable_name=human_readable_name
        )

        return typing.cast(None, jsii.invoke(self, "putHint", [value]))

    @builtins.property
    @jsii.member(jsii_name="hint")
    def hint(
        self,
    ) -> GoogleContainerAnalysisNoteAttestationAuthorityHintOutputReference:
        return typing.cast(GoogleContainerAnalysisNoteAttestationAuthorityHintOutputReference, jsii.get(self, "hint"))

    @builtins.property
    @jsii.member(jsii_name="hintInput")
    def hint_input(
        self,
    ) -> typing.Optional[GoogleContainerAnalysisNoteAttestationAuthorityHint]:
        return typing.cast(typing.Optional[GoogleContainerAnalysisNoteAttestationAuthorityHint], jsii.get(self, "hintInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAnalysisNoteAttestationAuthority]:
        return typing.cast(typing.Optional[GoogleContainerAnalysisNoteAttestationAuthority], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAnalysisNoteAttestationAuthority],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371a68631797ed8cc4b709859892d7ef946542ae9721371fe68aed42f0b89c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "attestation_authority": "attestationAuthority",
        "name": "name",
        "expiration_time": "expirationTime",
        "id": "id",
        "long_description": "longDescription",
        "project": "project",
        "related_note_names": "relatedNoteNames",
        "related_url": "relatedUrl",
        "short_description": "shortDescription",
        "timeouts": "timeouts",
    },
)
class GoogleContainerAnalysisNoteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        attestation_authority: typing.Union[GoogleContainerAnalysisNoteAttestationAuthority, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        long_description: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        related_note_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        related_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAnalysisNoteRelatedUrl", typing.Dict[builtins.str, typing.Any]]]]] = None,
        short_description: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAnalysisNoteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param attestation_authority: attestation_authority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#attestation_authority GoogleContainerAnalysisNote#attestation_authority}
        :param name: The name of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#name GoogleContainerAnalysisNote#name}
        :param expiration_time: Time of expiration for this note. Leave empty if note does not expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#expiration_time GoogleContainerAnalysisNote#expiration_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#id GoogleContainerAnalysisNote#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param long_description: A detailed description of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#long_description GoogleContainerAnalysisNote#long_description}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#project GoogleContainerAnalysisNote#project}.
        :param related_note_names: Names of other notes related to this note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#related_note_names GoogleContainerAnalysisNote#related_note_names}
        :param related_url: related_url block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#related_url GoogleContainerAnalysisNote#related_url}
        :param short_description: A one sentence description of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#short_description GoogleContainerAnalysisNote#short_description}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#timeouts GoogleContainerAnalysisNote#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(attestation_authority, dict):
            attestation_authority = GoogleContainerAnalysisNoteAttestationAuthority(**attestation_authority)
        if isinstance(timeouts, dict):
            timeouts = GoogleContainerAnalysisNoteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a8a9cf6a4826f9c0aa81a06572736bc669ea6563bcd281a9e8b2c77b2ab6d8d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument attestation_authority", value=attestation_authority, expected_type=type_hints["attestation_authority"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument expiration_time", value=expiration_time, expected_type=type_hints["expiration_time"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument long_description", value=long_description, expected_type=type_hints["long_description"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument related_note_names", value=related_note_names, expected_type=type_hints["related_note_names"])
            check_type(argname="argument related_url", value=related_url, expected_type=type_hints["related_url"])
            check_type(argname="argument short_description", value=short_description, expected_type=type_hints["short_description"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attestation_authority": attestation_authority,
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
        if expiration_time is not None:
            self._values["expiration_time"] = expiration_time
        if id is not None:
            self._values["id"] = id
        if long_description is not None:
            self._values["long_description"] = long_description
        if project is not None:
            self._values["project"] = project
        if related_note_names is not None:
            self._values["related_note_names"] = related_note_names
        if related_url is not None:
            self._values["related_url"] = related_url
        if short_description is not None:
            self._values["short_description"] = short_description
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
    def attestation_authority(self) -> GoogleContainerAnalysisNoteAttestationAuthority:
        '''attestation_authority block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#attestation_authority GoogleContainerAnalysisNote#attestation_authority}
        '''
        result = self._values.get("attestation_authority")
        assert result is not None, "Required property 'attestation_authority' is missing"
        return typing.cast(GoogleContainerAnalysisNoteAttestationAuthority, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#name GoogleContainerAnalysisNote#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[builtins.str]:
        '''Time of expiration for this note. Leave empty if note does not expire.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#expiration_time GoogleContainerAnalysisNote#expiration_time}
        '''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#id GoogleContainerAnalysisNote#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_description(self) -> typing.Optional[builtins.str]:
        '''A detailed description of the note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#long_description GoogleContainerAnalysisNote#long_description}
        '''
        result = self._values.get("long_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#project GoogleContainerAnalysisNote#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def related_note_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of other notes related to this note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#related_note_names GoogleContainerAnalysisNote#related_note_names}
        '''
        result = self._values.get("related_note_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def related_url(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAnalysisNoteRelatedUrl"]]]:
        '''related_url block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#related_url GoogleContainerAnalysisNote#related_url}
        '''
        result = self._values.get("related_url")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAnalysisNoteRelatedUrl"]]], result)

    @builtins.property
    def short_description(self) -> typing.Optional[builtins.str]:
        '''A one sentence description of the note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#short_description GoogleContainerAnalysisNote#short_description}
        '''
        result = self._values.get("short_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleContainerAnalysisNoteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#timeouts GoogleContainerAnalysisNote#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleContainerAnalysisNoteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAnalysisNoteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteRelatedUrl",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "label": "label"},
)
class GoogleContainerAnalysisNoteRelatedUrl:
    def __init__(
        self,
        *,
        url: builtins.str,
        label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: Specific URL associated with the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#url GoogleContainerAnalysisNote#url}
        :param label: Label to describe usage of the URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#label GoogleContainerAnalysisNote#label}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e76b0f6111a83ea137d5b8632d8e098e527fffaa1bfe8d53d7efc5a153819a7)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if label is not None:
            self._values["label"] = label

    @builtins.property
    def url(self) -> builtins.str:
        '''Specific URL associated with the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#url GoogleContainerAnalysisNote#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Label to describe usage of the URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#label GoogleContainerAnalysisNote#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAnalysisNoteRelatedUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAnalysisNoteRelatedUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteRelatedUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__253fb1d7be3446d95484ae48ccd737d09eb5d9e07f591a7ebf59c4ea9af03cfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAnalysisNoteRelatedUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f598e50bbd07dfcc27d3e86a28a30575ed21beaccd5b4a11b2edbc40cbe26a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAnalysisNoteRelatedUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5f5b1af2180d1bfe433c762cc0b00be445581329f002696e5fe6cd1de1bcd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5edbd5159d1fcc8e64cb8806eb348444894426b0614aefca1519d4f2be01439a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cab30b8cf3ce9bdcc47c896ee24c18a2bc9e30512c616c36d7eb554d57c9993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAnalysisNoteRelatedUrl]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAnalysisNoteRelatedUrl]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAnalysisNoteRelatedUrl]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2366e746fa6012657105f84365c5b4ea33751d9f7d8778f80225bdc4dbce2a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAnalysisNoteRelatedUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteRelatedUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2f9d3e066ee8fd7f90b416b1d5f8ffbf1c8654108bf3e3a505731c9b331d820)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c7057b9ae8584dc77ddd3818b5ff4ab5486dea14ae45573883b9f0ac2a92d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64db3622eea303e270d8baa83b38f98864dce0408a0c12cc0c37d4928d3af1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAnalysisNoteRelatedUrl]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAnalysisNoteRelatedUrl]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAnalysisNoteRelatedUrl]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa415e44454b5a67096c53fa71287fcc3fec878df653b630421001e4312c82c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleContainerAnalysisNoteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#create GoogleContainerAnalysisNote#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#delete GoogleContainerAnalysisNote#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#update GoogleContainerAnalysisNote#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231add8ce83b1d763fbad1201ef4e6a4ac8c25e4eb911fd02d484b070052f4d6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#create GoogleContainerAnalysisNote#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#delete GoogleContainerAnalysisNote#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_analysis_note#update GoogleContainerAnalysisNote#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAnalysisNoteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAnalysisNoteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAnalysisNote.GoogleContainerAnalysisNoteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2a195ca167b01e52b00a0138134dd6f2a5e60536e421f74bef48c123b273683)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acf47b323ebc7f66f92129ac053543ffa9c7c80c5ed7740e238951f841aed2f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49987eca9ca1935e3bfd5ab262f4198acc6f83f33f6e5214a59b64d1bf77be3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20607cb420677e6da52a80e1a2c167d1e3bbbebd0e5e18ac8c93caf84e01de3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAnalysisNoteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAnalysisNoteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAnalysisNoteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ad7f7a5815a61c8bb2dacb2da2b4ecb444cffe5c68e4278fb7367036309caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleContainerAnalysisNote",
    "GoogleContainerAnalysisNoteAttestationAuthority",
    "GoogleContainerAnalysisNoteAttestationAuthorityHint",
    "GoogleContainerAnalysisNoteAttestationAuthorityHintOutputReference",
    "GoogleContainerAnalysisNoteAttestationAuthorityOutputReference",
    "GoogleContainerAnalysisNoteConfig",
    "GoogleContainerAnalysisNoteRelatedUrl",
    "GoogleContainerAnalysisNoteRelatedUrlList",
    "GoogleContainerAnalysisNoteRelatedUrlOutputReference",
    "GoogleContainerAnalysisNoteTimeouts",
    "GoogleContainerAnalysisNoteTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2067233c5bd30060da0ef2b3289a1d8546bba306667bbf4b8ebcc8fa02845bb4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    attestation_authority: typing.Union[GoogleContainerAnalysisNoteAttestationAuthority, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    expiration_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    long_description: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    related_note_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    related_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAnalysisNoteRelatedUrl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    short_description: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAnalysisNoteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__244d0daa8551827e9ad00f74c12d841e6280d3a927d1926d32ff1c4940f33073(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4586177a31afd08f5f7e52c8935bb743196a21acffc89780d86bf2c65d31e983(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAnalysisNoteRelatedUrl, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1ae54ead3837ef78a7726403740e5ec15dcf86b0476c277889d08ceb6ba024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6fb6fcbe03bcf42fca5041376c1bafcd2f1a9582b258c74839792617d79d51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05659e38bf0fa299efb1f1be08922d370a87a05be3e13cbe59578286c58b801d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa0a29434e19576f430250307db373ffd17c81f5ba8dff1fd9619c154f85ed5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2c16471b78de1d86af0e69b56c2a9f594fe455ae72e92f1c4fbc4a4436b69f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd11af5ecc6ee4b0729929351d892996c73e62811ca8aab736b49711933af71(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6a9ee0bca46b75ed694a8aeb29381ee46ccca4628c6994f70aa17278dc410f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8828c4ccfb5e15bc21e3ff2d965bb8d0733bbe45948f674d4afa8d0218ec7f(
    *,
    hint: typing.Union[GoogleContainerAnalysisNoteAttestationAuthorityHint, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58564c3a777764adec323c2af0d2458a42c7f70b6e926ea2c6f1e7c3d30707bb(
    *,
    human_readable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99717ffa077f65d291f281717c79b4da6d3bc80be16815d15b3918992263858f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735f00053dff85892cd2a2f226dcc77c438ca45c925709b4b89397a0ad00e4e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3f09785409a0f482589abcfbdce5bfb8851d437477b88e9da1642e35594a80(
    value: typing.Optional[GoogleContainerAnalysisNoteAttestationAuthorityHint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bceec43e5cb19ebf195c290d032872ed2529594135b487b58ce02a83c98ff2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371a68631797ed8cc4b709859892d7ef946542ae9721371fe68aed42f0b89c7c(
    value: typing.Optional[GoogleContainerAnalysisNoteAttestationAuthority],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8a9cf6a4826f9c0aa81a06572736bc669ea6563bcd281a9e8b2c77b2ab6d8d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    attestation_authority: typing.Union[GoogleContainerAnalysisNoteAttestationAuthority, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    expiration_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    long_description: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    related_note_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    related_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAnalysisNoteRelatedUrl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    short_description: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAnalysisNoteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e76b0f6111a83ea137d5b8632d8e098e527fffaa1bfe8d53d7efc5a153819a7(
    *,
    url: builtins.str,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253fb1d7be3446d95484ae48ccd737d09eb5d9e07f591a7ebf59c4ea9af03cfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f598e50bbd07dfcc27d3e86a28a30575ed21beaccd5b4a11b2edbc40cbe26a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5f5b1af2180d1bfe433c762cc0b00be445581329f002696e5fe6cd1de1bcd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edbd5159d1fcc8e64cb8806eb348444894426b0614aefca1519d4f2be01439a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cab30b8cf3ce9bdcc47c896ee24c18a2bc9e30512c616c36d7eb554d57c9993(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2366e746fa6012657105f84365c5b4ea33751d9f7d8778f80225bdc4dbce2a04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAnalysisNoteRelatedUrl]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f9d3e066ee8fd7f90b416b1d5f8ffbf1c8654108bf3e3a505731c9b331d820(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c7057b9ae8584dc77ddd3818b5ff4ab5486dea14ae45573883b9f0ac2a92d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64db3622eea303e270d8baa83b38f98864dce0408a0c12cc0c37d4928d3af1aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa415e44454b5a67096c53fa71287fcc3fec878df653b630421001e4312c82c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAnalysisNoteRelatedUrl]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231add8ce83b1d763fbad1201ef4e6a4ac8c25e4eb911fd02d484b070052f4d6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a195ca167b01e52b00a0138134dd6f2a5e60536e421f74bef48c123b273683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf47b323ebc7f66f92129ac053543ffa9c7c80c5ed7740e238951f841aed2f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49987eca9ca1935e3bfd5ab262f4198acc6f83f33f6e5214a59b64d1bf77be3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20607cb420677e6da52a80e1a2c167d1e3bbbebd0e5e18ac8c93caf84e01de3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ad7f7a5815a61c8bb2dacb2da2b4ecb444cffe5c68e4278fb7367036309caf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAnalysisNoteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
