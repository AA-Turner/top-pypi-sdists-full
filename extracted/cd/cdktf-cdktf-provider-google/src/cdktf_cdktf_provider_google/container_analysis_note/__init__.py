r'''
# `google_container_analysis_note`

Refer to the Terraform Registry for docs: [`google_container_analysis_note`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note).
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


class ContainerAnalysisNote(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNote",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note google_container_analysis_note}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        attestation_authority: typing.Union["ContainerAnalysisNoteAttestationAuthority", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        long_description: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        related_note_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        related_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAnalysisNoteRelatedUrl", typing.Dict[builtins.str, typing.Any]]]]] = None,
        short_description: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAnalysisNoteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note google_container_analysis_note} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param attestation_authority: attestation_authority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#attestation_authority ContainerAnalysisNote#attestation_authority}
        :param name: The name of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#name ContainerAnalysisNote#name}
        :param expiration_time: Time of expiration for this note. Leave empty if note does not expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#expiration_time ContainerAnalysisNote#expiration_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#id ContainerAnalysisNote#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param long_description: A detailed description of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#long_description ContainerAnalysisNote#long_description}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#project ContainerAnalysisNote#project}.
        :param related_note_names: Names of other notes related to this note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#related_note_names ContainerAnalysisNote#related_note_names}
        :param related_url: related_url block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#related_url ContainerAnalysisNote#related_url}
        :param short_description: A one sentence description of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#short_description ContainerAnalysisNote#short_description}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#timeouts ContainerAnalysisNote#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0832456248cf413a873542c00712eb4c448bffafba87efb19ba0233a063fdfb8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerAnalysisNoteConfig(
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
        '''Generates CDKTF code for importing a ContainerAnalysisNote resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAnalysisNote to import.
        :param import_from_id: The id of the existing ContainerAnalysisNote that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAnalysisNote to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4355a7fb720bcdf96f57ef9197c455e774ca35728a8a518088f7a14c845eef9d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAttestationAuthority")
    def put_attestation_authority(
        self,
        *,
        hint: typing.Union["ContainerAnalysisNoteAttestationAuthorityHint", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hint: hint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#hint ContainerAnalysisNote#hint}
        '''
        value = ContainerAnalysisNoteAttestationAuthority(hint=hint)

        return typing.cast(None, jsii.invoke(self, "putAttestationAuthority", [value]))

    @jsii.member(jsii_name="putRelatedUrl")
    def put_related_url(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAnalysisNoteRelatedUrl", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6076f9da9037cc8cb637e786b9c5f34cbbbf76b5e7edf6292039a7dc5c4a37)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#create ContainerAnalysisNote#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#delete ContainerAnalysisNote#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#update ContainerAnalysisNote#update}.
        '''
        value = ContainerAnalysisNoteTimeouts(
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
    ) -> "ContainerAnalysisNoteAttestationAuthorityOutputReference":
        return typing.cast("ContainerAnalysisNoteAttestationAuthorityOutputReference", jsii.get(self, "attestationAuthority"))

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
    def related_url(self) -> "ContainerAnalysisNoteRelatedUrlList":
        return typing.cast("ContainerAnalysisNoteRelatedUrlList", jsii.get(self, "relatedUrl"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerAnalysisNoteTimeoutsOutputReference":
        return typing.cast("ContainerAnalysisNoteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="attestationAuthorityInput")
    def attestation_authority_input(
        self,
    ) -> typing.Optional["ContainerAnalysisNoteAttestationAuthority"]:
        return typing.cast(typing.Optional["ContainerAnalysisNoteAttestationAuthority"], jsii.get(self, "attestationAuthorityInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAnalysisNoteRelatedUrl"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAnalysisNoteRelatedUrl"]]], jsii.get(self, "relatedUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="shortDescriptionInput")
    def short_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shortDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAnalysisNoteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAnalysisNoteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationTime")
    def expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationTime"))

    @expiration_time.setter
    def expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e2ccc1551417597c1bbf47781946df861088fa632e254049800b25369c7ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd6c1400698ab7734e11c5457a7a0b0c4dd5baad4be84eb5cedccc86e8f3f4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longDescription")
    def long_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "longDescription"))

    @long_description.setter
    def long_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35abbe117d2a42ed87cd4e392c2082751645868f61405622fe571c0ce9aa30e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900d57c8d6a2e673e765d53953d9601919963cc1502b2f21f026495159694f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b385ff9b208c31d51bddae8561d0253077f55913748d8b810d55d66ea4a257de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="relatedNoteNames")
    def related_note_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "relatedNoteNames"))

    @related_note_names.setter
    def related_note_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a652143d7258b8e7d44a1ae3da5edf18ecb25a74faa9df97edceb91123ad13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "relatedNoteNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shortDescription")
    def short_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shortDescription"))

    @short_description.setter
    def short_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3b339f2fa04a59a0ab06e4b67f47592d808f184b3718e83ac97ebf72798130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shortDescription", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteAttestationAuthority",
    jsii_struct_bases=[],
    name_mapping={"hint": "hint"},
)
class ContainerAnalysisNoteAttestationAuthority:
    def __init__(
        self,
        *,
        hint: typing.Union["ContainerAnalysisNoteAttestationAuthorityHint", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param hint: hint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#hint ContainerAnalysisNote#hint}
        '''
        if isinstance(hint, dict):
            hint = ContainerAnalysisNoteAttestationAuthorityHint(**hint)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab69e3f589659584536f7145be6c02103ece4f62c3e97eae9a3e955a4a32e64)
            check_type(argname="argument hint", value=hint, expected_type=type_hints["hint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hint": hint,
        }

    @builtins.property
    def hint(self) -> "ContainerAnalysisNoteAttestationAuthorityHint":
        '''hint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#hint ContainerAnalysisNote#hint}
        '''
        result = self._values.get("hint")
        assert result is not None, "Required property 'hint' is missing"
        return typing.cast("ContainerAnalysisNoteAttestationAuthorityHint", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisNoteAttestationAuthority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteAttestationAuthorityHint",
    jsii_struct_bases=[],
    name_mapping={"human_readable_name": "humanReadableName"},
)
class ContainerAnalysisNoteAttestationAuthorityHint:
    def __init__(self, *, human_readable_name: builtins.str) -> None:
        '''
        :param human_readable_name: The human readable name of this Attestation Authority, for example "qa". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#human_readable_name ContainerAnalysisNote#human_readable_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2cd15d82f6b630c7fd59d393be54f2c3a4dc3c6397b5af41aea2a8e506478c2)
            check_type(argname="argument human_readable_name", value=human_readable_name, expected_type=type_hints["human_readable_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "human_readable_name": human_readable_name,
        }

    @builtins.property
    def human_readable_name(self) -> builtins.str:
        '''The human readable name of this Attestation Authority, for example "qa".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#human_readable_name ContainerAnalysisNote#human_readable_name}
        '''
        result = self._values.get("human_readable_name")
        assert result is not None, "Required property 'human_readable_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisNoteAttestationAuthorityHint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAnalysisNoteAttestationAuthorityHintOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteAttestationAuthorityHintOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9201cd36b4468effda16f55cd6b9179f3470de0d3f4b0450cad3e9cfb71606c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__344244498396992486bf6db5c0cf8b9ba05b2af25c041c5974d73a1e558a805c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "humanReadableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAnalysisNoteAttestationAuthorityHint]:
        return typing.cast(typing.Optional[ContainerAnalysisNoteAttestationAuthorityHint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAnalysisNoteAttestationAuthorityHint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310a758ed9f9f824be8b56c3b8cfa1fa87784673ef954eaa926910025081a008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAnalysisNoteAttestationAuthorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteAttestationAuthorityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8774ceab44fe8f5442fd737d15f29e22d903693c35268e7306b80154ec15f35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHint")
    def put_hint(self, *, human_readable_name: builtins.str) -> None:
        '''
        :param human_readable_name: The human readable name of this Attestation Authority, for example "qa". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#human_readable_name ContainerAnalysisNote#human_readable_name}
        '''
        value = ContainerAnalysisNoteAttestationAuthorityHint(
            human_readable_name=human_readable_name
        )

        return typing.cast(None, jsii.invoke(self, "putHint", [value]))

    @builtins.property
    @jsii.member(jsii_name="hint")
    def hint(self) -> ContainerAnalysisNoteAttestationAuthorityHintOutputReference:
        return typing.cast(ContainerAnalysisNoteAttestationAuthorityHintOutputReference, jsii.get(self, "hint"))

    @builtins.property
    @jsii.member(jsii_name="hintInput")
    def hint_input(
        self,
    ) -> typing.Optional[ContainerAnalysisNoteAttestationAuthorityHint]:
        return typing.cast(typing.Optional[ContainerAnalysisNoteAttestationAuthorityHint], jsii.get(self, "hintInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAnalysisNoteAttestationAuthority]:
        return typing.cast(typing.Optional[ContainerAnalysisNoteAttestationAuthority], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAnalysisNoteAttestationAuthority],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49da5f080e86179a4a485d60acbc44fcf83f3732f23b41f53bef0a0cd2929ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteConfig",
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
class ContainerAnalysisNoteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        attestation_authority: typing.Union[ContainerAnalysisNoteAttestationAuthority, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        expiration_time: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        long_description: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        related_note_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        related_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAnalysisNoteRelatedUrl", typing.Dict[builtins.str, typing.Any]]]]] = None,
        short_description: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAnalysisNoteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param attestation_authority: attestation_authority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#attestation_authority ContainerAnalysisNote#attestation_authority}
        :param name: The name of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#name ContainerAnalysisNote#name}
        :param expiration_time: Time of expiration for this note. Leave empty if note does not expire. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#expiration_time ContainerAnalysisNote#expiration_time}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#id ContainerAnalysisNote#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param long_description: A detailed description of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#long_description ContainerAnalysisNote#long_description}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#project ContainerAnalysisNote#project}.
        :param related_note_names: Names of other notes related to this note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#related_note_names ContainerAnalysisNote#related_note_names}
        :param related_url: related_url block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#related_url ContainerAnalysisNote#related_url}
        :param short_description: A one sentence description of the note. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#short_description ContainerAnalysisNote#short_description}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#timeouts ContainerAnalysisNote#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(attestation_authority, dict):
            attestation_authority = ContainerAnalysisNoteAttestationAuthority(**attestation_authority)
        if isinstance(timeouts, dict):
            timeouts = ContainerAnalysisNoteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179433793f33119dbb162d1b22e65058cd8dd0f9f0e61ad035ad96e54dc4ba67)
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
    def attestation_authority(self) -> ContainerAnalysisNoteAttestationAuthority:
        '''attestation_authority block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#attestation_authority ContainerAnalysisNote#attestation_authority}
        '''
        result = self._values.get("attestation_authority")
        assert result is not None, "Required property 'attestation_authority' is missing"
        return typing.cast(ContainerAnalysisNoteAttestationAuthority, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#name ContainerAnalysisNote#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_time(self) -> typing.Optional[builtins.str]:
        '''Time of expiration for this note. Leave empty if note does not expire.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#expiration_time ContainerAnalysisNote#expiration_time}
        '''
        result = self._values.get("expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#id ContainerAnalysisNote#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_description(self) -> typing.Optional[builtins.str]:
        '''A detailed description of the note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#long_description ContainerAnalysisNote#long_description}
        '''
        result = self._values.get("long_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#project ContainerAnalysisNote#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def related_note_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of other notes related to this note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#related_note_names ContainerAnalysisNote#related_note_names}
        '''
        result = self._values.get("related_note_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def related_url(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAnalysisNoteRelatedUrl"]]]:
        '''related_url block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#related_url ContainerAnalysisNote#related_url}
        '''
        result = self._values.get("related_url")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAnalysisNoteRelatedUrl"]]], result)

    @builtins.property
    def short_description(self) -> typing.Optional[builtins.str]:
        '''A one sentence description of the note.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#short_description ContainerAnalysisNote#short_description}
        '''
        result = self._values.get("short_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAnalysisNoteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#timeouts ContainerAnalysisNote#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAnalysisNoteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisNoteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteRelatedUrl",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "label": "label"},
)
class ContainerAnalysisNoteRelatedUrl:
    def __init__(
        self,
        *,
        url: builtins.str,
        label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: Specific URL associated with the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#url ContainerAnalysisNote#url}
        :param label: Label to describe usage of the URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#label ContainerAnalysisNote#label}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3c28b2475c62eca5976570744dc762e3ab752b1a75211fdc1e927b03def9cc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#url ContainerAnalysisNote#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Label to describe usage of the URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#label ContainerAnalysisNote#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisNoteRelatedUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAnalysisNoteRelatedUrlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteRelatedUrlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30af03d21a4542226654d57f391ba9037e69946ca0021f768e982c897a3dab23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAnalysisNoteRelatedUrlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e9191dc3573ea6a28c824bac373a8fe0f0677b8236fdf822f07a977aa985f8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAnalysisNoteRelatedUrlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ab92c349390653470f0b559e8c6ca63c088c01831c45ada4a3f09caa21908a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__120a764b19560cdaf7cd015234cb9e731505db087121db20e9932b56f845f6aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74d78a278e2183ca0711adb35928268c4bc016145b4f8524ad060140d791c8cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAnalysisNoteRelatedUrl]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAnalysisNoteRelatedUrl]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAnalysisNoteRelatedUrl]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57404ce9d3aca00e73f1d329da05f3af99a3231ae50f3329f3294e44b06a9926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAnalysisNoteRelatedUrlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteRelatedUrlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c58d7d5d19b71c56d553acc69a3af0d44d0a7ff8e8a05e24ad52e4c7f34bad27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b90811479f928ae0fd75b6a7cbc9d23bd46f8e31403472205ffabc7728a841e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0d4c998054ba3d26de453a76f59dbd66e91bb1e929dde490f2619b0a4e71bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisNoteRelatedUrl]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisNoteRelatedUrl]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisNoteRelatedUrl]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3491fe4fbbe41f5237dc3217f8a95c1b83c3fcb8d381406567543871340abcc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerAnalysisNoteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#create ContainerAnalysisNote#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#delete ContainerAnalysisNote#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#update ContainerAnalysisNote#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1f2b1c4b5b331b8ae987164d1633785dd000900df2334bf0b31b866edc1f36)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#create ContainerAnalysisNote#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#delete ContainerAnalysisNote#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_analysis_note#update ContainerAnalysisNote#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAnalysisNoteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAnalysisNoteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAnalysisNote.ContainerAnalysisNoteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bb8f2e37b99a342850cb59319a51d10569cc26592c27433e059e3701dc9d481)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94efbfe23ffcfd9f81172c0476ff1c850a4dce35edc17e4160dfbf06659ad371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ddf9a35040377c817b1ade654cb6b728772ca723ed32ee63e948de2fc3e3b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422181e927955bae9f4b35b11deed672cf0fad1c89a6ea461d76413f50ca58c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisNoteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisNoteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisNoteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7557a1c2fd6f9a5eea1f0fe82a1da0690cd85bb96003ebf4510ad3d90384eee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAnalysisNote",
    "ContainerAnalysisNoteAttestationAuthority",
    "ContainerAnalysisNoteAttestationAuthorityHint",
    "ContainerAnalysisNoteAttestationAuthorityHintOutputReference",
    "ContainerAnalysisNoteAttestationAuthorityOutputReference",
    "ContainerAnalysisNoteConfig",
    "ContainerAnalysisNoteRelatedUrl",
    "ContainerAnalysisNoteRelatedUrlList",
    "ContainerAnalysisNoteRelatedUrlOutputReference",
    "ContainerAnalysisNoteTimeouts",
    "ContainerAnalysisNoteTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0832456248cf413a873542c00712eb4c448bffafba87efb19ba0233a063fdfb8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    attestation_authority: typing.Union[ContainerAnalysisNoteAttestationAuthority, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    expiration_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    long_description: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    related_note_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    related_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAnalysisNoteRelatedUrl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    short_description: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAnalysisNoteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4355a7fb720bcdf96f57ef9197c455e774ca35728a8a518088f7a14c845eef9d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6076f9da9037cc8cb637e786b9c5f34cbbbf76b5e7edf6292039a7dc5c4a37(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAnalysisNoteRelatedUrl, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e2ccc1551417597c1bbf47781946df861088fa632e254049800b25369c7ac0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd6c1400698ab7734e11c5457a7a0b0c4dd5baad4be84eb5cedccc86e8f3f4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35abbe117d2a42ed87cd4e392c2082751645868f61405622fe571c0ce9aa30e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900d57c8d6a2e673e765d53953d9601919963cc1502b2f21f026495159694f19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b385ff9b208c31d51bddae8561d0253077f55913748d8b810d55d66ea4a257de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a652143d7258b8e7d44a1ae3da5edf18ecb25a74faa9df97edceb91123ad13(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3b339f2fa04a59a0ab06e4b67f47592d808f184b3718e83ac97ebf72798130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab69e3f589659584536f7145be6c02103ece4f62c3e97eae9a3e955a4a32e64(
    *,
    hint: typing.Union[ContainerAnalysisNoteAttestationAuthorityHint, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cd15d82f6b630c7fd59d393be54f2c3a4dc3c6397b5af41aea2a8e506478c2(
    *,
    human_readable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9201cd36b4468effda16f55cd6b9179f3470de0d3f4b0450cad3e9cfb71606c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344244498396992486bf6db5c0cf8b9ba05b2af25c041c5974d73a1e558a805c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310a758ed9f9f824be8b56c3b8cfa1fa87784673ef954eaa926910025081a008(
    value: typing.Optional[ContainerAnalysisNoteAttestationAuthorityHint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8774ceab44fe8f5442fd737d15f29e22d903693c35268e7306b80154ec15f35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49da5f080e86179a4a485d60acbc44fcf83f3732f23b41f53bef0a0cd2929ed(
    value: typing.Optional[ContainerAnalysisNoteAttestationAuthority],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179433793f33119dbb162d1b22e65058cd8dd0f9f0e61ad035ad96e54dc4ba67(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    attestation_authority: typing.Union[ContainerAnalysisNoteAttestationAuthority, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    expiration_time: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    long_description: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    related_note_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    related_url: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAnalysisNoteRelatedUrl, typing.Dict[builtins.str, typing.Any]]]]] = None,
    short_description: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAnalysisNoteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3c28b2475c62eca5976570744dc762e3ab752b1a75211fdc1e927b03def9cc(
    *,
    url: builtins.str,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30af03d21a4542226654d57f391ba9037e69946ca0021f768e982c897a3dab23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e9191dc3573ea6a28c824bac373a8fe0f0677b8236fdf822f07a977aa985f8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ab92c349390653470f0b559e8c6ca63c088c01831c45ada4a3f09caa21908a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120a764b19560cdaf7cd015234cb9e731505db087121db20e9932b56f845f6aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d78a278e2183ca0711adb35928268c4bc016145b4f8524ad060140d791c8cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57404ce9d3aca00e73f1d329da05f3af99a3231ae50f3329f3294e44b06a9926(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAnalysisNoteRelatedUrl]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58d7d5d19b71c56d553acc69a3af0d44d0a7ff8e8a05e24ad52e4c7f34bad27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90811479f928ae0fd75b6a7cbc9d23bd46f8e31403472205ffabc7728a841e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0d4c998054ba3d26de453a76f59dbd66e91bb1e929dde490f2619b0a4e71bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3491fe4fbbe41f5237dc3217f8a95c1b83c3fcb8d381406567543871340abcc5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisNoteRelatedUrl]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1f2b1c4b5b331b8ae987164d1633785dd000900df2334bf0b31b866edc1f36(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb8f2e37b99a342850cb59319a51d10569cc26592c27433e059e3701dc9d481(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94efbfe23ffcfd9f81172c0476ff1c850a4dce35edc17e4160dfbf06659ad371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ddf9a35040377c817b1ade654cb6b728772ca723ed32ee63e948de2fc3e3b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422181e927955bae9f4b35b11deed672cf0fad1c89a6ea461d76413f50ca58c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7557a1c2fd6f9a5eea1f0fe82a1da0690cd85bb96003ebf4510ad3d90384eee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAnalysisNoteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
