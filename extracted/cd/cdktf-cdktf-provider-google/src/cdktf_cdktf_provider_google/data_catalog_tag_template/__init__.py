r'''
# `google_data_catalog_tag_template`

Refer to the Terraform Registry for docs: [`google_data_catalog_tag_template`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template).
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


class DataCatalogTagTemplate(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template google_data_catalog_tag_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        fields: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataCatalogTagTemplateFields", typing.Dict[builtins.str, typing.Any]]]],
        tag_template_id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataCatalogTagTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template google_data_catalog_tag_template} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param fields: fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#fields DataCatalogTagTemplate#fields}
        :param tag_template_id: The id of the tag template to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#tag_template_id DataCatalogTagTemplate#tag_template_id}
        :param display_name: The display name for this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#display_name DataCatalogTagTemplate#display_name}
        :param force_delete: This confirms the deletion of any possible tags using this template. Must be set to true in order to delete the tag template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#force_delete DataCatalogTagTemplate#force_delete}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#id DataCatalogTagTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#project DataCatalogTagTemplate#project}.
        :param region: Template location region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#region DataCatalogTagTemplate#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#timeouts DataCatalogTagTemplate#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a22c5b3088b2d3bfd4a95e54d7b4fd3e32c4bdc7d3f67c4f88c8506ece5d8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataCatalogTagTemplateConfig(
            fields=fields,
            tag_template_id=tag_template_id,
            display_name=display_name,
            force_delete=force_delete,
            id=id,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a DataCatalogTagTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataCatalogTagTemplate to import.
        :param import_from_id: The id of the existing DataCatalogTagTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataCatalogTagTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120f3b6aaff8bf68aa721ad3c298f4d2ed0adc4d850b27cb03d328f56ed4050f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFields")
    def put_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataCatalogTagTemplateFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310c6df21e6edaa80c091b08cfc77105afd13aee067a39315537ac8ca83944f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFields", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#create DataCatalogTagTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#delete DataCatalogTagTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#update DataCatalogTagTemplate#update}.
        '''
        value = DataCatalogTagTemplateTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetForceDelete")
    def reset_force_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDelete", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="fields")
    def fields(self) -> "DataCatalogTagTemplateFieldsList":
        return typing.cast("DataCatalogTagTemplateFieldsList", jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataCatalogTagTemplateTimeoutsOutputReference":
        return typing.cast("DataCatalogTagTemplateTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldsInput")
    def fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCatalogTagTemplateFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCatalogTagTemplateFields"]]], jsii.get(self, "fieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDeleteInput")
    def force_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagTemplateIdInput")
    def tag_template_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagTemplateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataCatalogTagTemplateTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataCatalogTagTemplateTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59a41d9fd7866df3d6d0934e628e7f00d3c7ab3b69a6a2e715677d0397a0543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceDelete")
    def force_delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDelete"))

    @force_delete.setter
    def force_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1992814ff2a9334fc93e4c6b8024cfd1f6925f476bb48dd3f29becbdda5e77a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408155f220e4f1fba2617f8a9b311b16baca935164a27f0760f4e831800d909b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa260d79e18e4730993e7a192b8cc43344228ebc20196f7ac24421c198ca5d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668a32e33a2154e1a2651de54e6b87588cf8765152da4d2451d78bb00c298506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagTemplateId")
    def tag_template_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagTemplateId"))

    @tag_template_id.setter
    def tag_template_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b4726b99cb9073a693f4c6614ee6f4f389ad64d67e953739589f1d529333ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagTemplateId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "fields": "fields",
        "tag_template_id": "tagTemplateId",
        "display_name": "displayName",
        "force_delete": "forceDelete",
        "id": "id",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class DataCatalogTagTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        fields: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataCatalogTagTemplateFields", typing.Dict[builtins.str, typing.Any]]]],
        tag_template_id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataCatalogTagTemplateTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param fields: fields block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#fields DataCatalogTagTemplate#fields}
        :param tag_template_id: The id of the tag template to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#tag_template_id DataCatalogTagTemplate#tag_template_id}
        :param display_name: The display name for this template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#display_name DataCatalogTagTemplate#display_name}
        :param force_delete: This confirms the deletion of any possible tags using this template. Must be set to true in order to delete the tag template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#force_delete DataCatalogTagTemplate#force_delete}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#id DataCatalogTagTemplate#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#project DataCatalogTagTemplate#project}.
        :param region: Template location region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#region DataCatalogTagTemplate#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#timeouts DataCatalogTagTemplate#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataCatalogTagTemplateTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4351e7cb7d29fa60f1727ebc490032226ff4fb635cb1c40dde78056082bc3b2c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument tag_template_id", value=tag_template_id, expected_type=type_hints["tag_template_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fields": fields,
            "tag_template_id": tag_template_id,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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
    def fields(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCatalogTagTemplateFields"]]:
        '''fields block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#fields DataCatalogTagTemplate#fields}
        '''
        result = self._values.get("fields")
        assert result is not None, "Required property 'fields' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCatalogTagTemplateFields"]], result)

    @builtins.property
    def tag_template_id(self) -> builtins.str:
        '''The id of the tag template to create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#tag_template_id DataCatalogTagTemplate#tag_template_id}
        '''
        result = self._values.get("tag_template_id")
        assert result is not None, "Required property 'tag_template_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name for this template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#display_name DataCatalogTagTemplate#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This confirms the deletion of any possible tags using this template.

        Must be set to true in order to delete the tag template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#force_delete DataCatalogTagTemplate#force_delete}
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#id DataCatalogTagTemplate#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#project DataCatalogTagTemplate#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Template location region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#region DataCatalogTagTemplate#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataCatalogTagTemplateTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#timeouts DataCatalogTagTemplate#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataCatalogTagTemplateTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogTagTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFields",
    jsii_struct_bases=[],
    name_mapping={
        "field_id": "fieldId",
        "type": "type",
        "description": "description",
        "display_name": "displayName",
        "is_required": "isRequired",
        "order": "order",
    },
)
class DataCatalogTagTemplateFields:
    def __init__(
        self,
        *,
        field_id: builtins.str,
        type: typing.Union["DataCatalogTagTemplateFieldsType", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param field_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#field_id DataCatalogTagTemplate#field_id}.
        :param type: type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#type DataCatalogTagTemplate#type}
        :param description: A description for this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#description DataCatalogTagTemplate#description}
        :param display_name: The display name for this field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#display_name DataCatalogTagTemplate#display_name}
        :param is_required: Whether this is a required field. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#is_required DataCatalogTagTemplate#is_required}
        :param order: The order of this field with respect to other fields in this tag template. A higher value indicates a more important field. The value can be negative. Multiple fields can have the same order, and field orders within a tag do not have to be sequential. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#order DataCatalogTagTemplate#order}
        '''
        if isinstance(type, dict):
            type = DataCatalogTagTemplateFieldsType(**type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4690d544a41063a3114976d85f7b987140496ec1480415900a671efc414d1e)
            check_type(argname="argument field_id", value=field_id, expected_type=type_hints["field_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument is_required", value=is_required, expected_type=type_hints["is_required"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_id": field_id,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if is_required is not None:
            self._values["is_required"] = is_required
        if order is not None:
            self._values["order"] = order

    @builtins.property
    def field_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#field_id DataCatalogTagTemplate#field_id}.'''
        result = self._values.get("field_id")
        assert result is not None, "Required property 'field_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "DataCatalogTagTemplateFieldsType":
        '''type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#type DataCatalogTagTemplate#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("DataCatalogTagTemplateFieldsType", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#description DataCatalogTagTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name for this field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#display_name DataCatalogTagTemplate#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this is a required field. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#is_required DataCatalogTagTemplate#is_required}
        '''
        result = self._values.get("is_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def order(self) -> typing.Optional[jsii.Number]:
        '''The order of this field with respect to other fields in this tag template.

        A higher value indicates a more important field. The value can be negative.
        Multiple fields can have the same order, and field orders within a tag do not have to be sequential.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#order DataCatalogTagTemplate#order}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogTagTemplateFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogTagTemplateFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1430967c042bc62cb8de598eeb5aa64749dc219a065fe9aefbdf84ae7417b0d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataCatalogTagTemplateFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df89e9bf70b0060875a7f50b5e090daaa79192aa33181c61a5f534264ec8ea9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCatalogTagTemplateFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b333865494a4a2bb9e53c6a0d3a2e500df8d5626a3a038445683e2dae56c306b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b02bc39b268d6d50b055c7f60f20f054d57c0803b3ca7897bd18b62f0aea8eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e792d48f6850b113dfa6d0eae20eb83c0505ab2aff75961452b98b033edda90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea745bd645f3a723eb23cf5d772c1fb43ec6c83536d64771a39527d775dbf30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataCatalogTagTemplateFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f40114745bf28394469b896b55ff3411b40dea749987e35845fad251c659de91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putType")
    def put_type(
        self,
        *,
        enum_type: typing.Optional[typing.Union["DataCatalogTagTemplateFieldsTypeEnumType", typing.Dict[builtins.str, typing.Any]]] = None,
        primitive_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enum_type: enum_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#enum_type DataCatalogTagTemplate#enum_type}
        :param primitive_type: Represents primitive types - string, bool etc. Exactly one of 'primitive_type' or 'enum_type' must be set Possible values: ["DOUBLE", "STRING", "BOOL", "TIMESTAMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#primitive_type DataCatalogTagTemplate#primitive_type}
        '''
        value = DataCatalogTagTemplateFieldsType(
            enum_type=enum_type, primitive_type=primitive_type
        )

        return typing.cast(None, jsii.invoke(self, "putType", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetIsRequired")
    def reset_is_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsRequired", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "DataCatalogTagTemplateFieldsTypeOutputReference":
        return typing.cast("DataCatalogTagTemplateFieldsTypeOutputReference", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldIdInput")
    def field_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldIdInput"))

    @builtins.property
    @jsii.member(jsii_name="isRequiredInput")
    def is_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional["DataCatalogTagTemplateFieldsType"]:
        return typing.cast(typing.Optional["DataCatalogTagTemplateFieldsType"], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0eb9c1169534a1d65026abcf3fa3e6de8a792163d6749fc0d726253de748da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c206829448306913152cb53c04d3fd8d3da0487583978caff46214b2e3f1093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldId")
    def field_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldId"))

    @field_id.setter
    def field_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf1f212241d3132a816b7d36e32ab31b56af8b20033a5cfd6cdefcd1a131a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isRequired")
    def is_required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isRequired"))

    @is_required.setter
    def is_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3aad4e8054ea094390c7d47ebc047a6d4bc38e9163e620218fc74a41e748f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "order"))

    @order.setter
    def order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72eacb3523246e5692b6880814f868c7c61df27b48a4dc1fea760ea3a1fa4b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateFields]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateFields]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateFields]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077dfae92ed4a23304e6d50af566749e8305312c982f511a601a08486d780eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsType",
    jsii_struct_bases=[],
    name_mapping={"enum_type": "enumType", "primitive_type": "primitiveType"},
)
class DataCatalogTagTemplateFieldsType:
    def __init__(
        self,
        *,
        enum_type: typing.Optional[typing.Union["DataCatalogTagTemplateFieldsTypeEnumType", typing.Dict[builtins.str, typing.Any]]] = None,
        primitive_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enum_type: enum_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#enum_type DataCatalogTagTemplate#enum_type}
        :param primitive_type: Represents primitive types - string, bool etc. Exactly one of 'primitive_type' or 'enum_type' must be set Possible values: ["DOUBLE", "STRING", "BOOL", "TIMESTAMP"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#primitive_type DataCatalogTagTemplate#primitive_type}
        '''
        if isinstance(enum_type, dict):
            enum_type = DataCatalogTagTemplateFieldsTypeEnumType(**enum_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3de175c491354fd67d213d6e236018ca358e1e7c9306616b1512d2866115a95)
            check_type(argname="argument enum_type", value=enum_type, expected_type=type_hints["enum_type"])
            check_type(argname="argument primitive_type", value=primitive_type, expected_type=type_hints["primitive_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enum_type is not None:
            self._values["enum_type"] = enum_type
        if primitive_type is not None:
            self._values["primitive_type"] = primitive_type

    @builtins.property
    def enum_type(self) -> typing.Optional["DataCatalogTagTemplateFieldsTypeEnumType"]:
        '''enum_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#enum_type DataCatalogTagTemplate#enum_type}
        '''
        result = self._values.get("enum_type")
        return typing.cast(typing.Optional["DataCatalogTagTemplateFieldsTypeEnumType"], result)

    @builtins.property
    def primitive_type(self) -> typing.Optional[builtins.str]:
        '''Represents primitive types - string, bool etc.

        Exactly one of 'primitive_type' or 'enum_type' must be set Possible values: ["DOUBLE", "STRING", "BOOL", "TIMESTAMP"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#primitive_type DataCatalogTagTemplate#primitive_type}
        '''
        result = self._values.get("primitive_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogTagTemplateFieldsType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsTypeEnumType",
    jsii_struct_bases=[],
    name_mapping={"allowed_values": "allowedValues"},
)
class DataCatalogTagTemplateFieldsTypeEnumType:
    def __init__(
        self,
        *,
        allowed_values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param allowed_values: allowed_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#allowed_values DataCatalogTagTemplate#allowed_values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83828b5d1ed347062238338c65a1d6b464d2f1639bdca16a31c94f9ba530b258)
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_values": allowed_values,
        }

    @builtins.property
    def allowed_values(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues"]]:
        '''allowed_values block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#allowed_values DataCatalogTagTemplate#allowed_values}
        '''
        result = self._values.get("allowed_values")
        assert result is not None, "Required property 'allowed_values' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogTagTemplateFieldsTypeEnumType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues",
    jsii_struct_bases=[],
    name_mapping={"display_name": "displayName"},
)
class DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues:
    def __init__(self, *, display_name: builtins.str) -> None:
        '''
        :param display_name: The display name of the enum value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#display_name DataCatalogTagTemplate#display_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e069dc8820bac8d93e6f29fb6652aa0b4ef243fb97586d24272c33cf24ead55a)
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
        }

    @builtins.property
    def display_name(self) -> builtins.str:
        '''The display name of the enum value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#display_name DataCatalogTagTemplate#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__459bc69410e4aed1ae7dc3ce7aef13bdaf379570774aca6ab3aca296cd68dc67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d034480dcdc6d8f6369d8c8f78086926d1e08e77c30a80e74fa41b4cee585c2b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e11aaf64bb9c646c9f102a57f49178b449f1fc298175888f408f6f84a901515)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c69eec2f76c58bda41974801d91098c257d4e49126be537cb29ed733abcef8d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b2add0eb38d53f303c5923338ccb7b5973b80235e1454377a54c60283b420ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7513274242acdf97d4d8a887d7227a79f547efeec3f5561eeac66a0c4659a09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee8a9caaed5a65b89474303f13ed5377ac3ec273bbff72e9fc914e3145acb248)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953a620306d560c61c9a710e1872bae60090030204e1c5a2b3e43d72a5d7183d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54b5c72cea91b7c595879398ee744b37abe82fe26c4018274c37989f9d6c6b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataCatalogTagTemplateFieldsTypeEnumTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsTypeEnumTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__083d9f1ddcc0ba4bd25d15431b35c3ae2c4cc1bbe4c2459e10ebf437e5e5644e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAllowedValues")
    def put_allowed_values(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b3d6f0862823118fb0e5067a110d7cfea53a131d566aeb87d947edb8b2a4ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowedValues", [value]))

    @builtins.property
    @jsii.member(jsii_name="allowedValues")
    def allowed_values(
        self,
    ) -> DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesList:
        return typing.cast(DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesList, jsii.get(self, "allowedValues"))

    @builtins.property
    @jsii.member(jsii_name="allowedValuesInput")
    def allowed_values_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]]], jsii.get(self, "allowedValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataCatalogTagTemplateFieldsTypeEnumType]:
        return typing.cast(typing.Optional[DataCatalogTagTemplateFieldsTypeEnumType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCatalogTagTemplateFieldsTypeEnumType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8978a744a282016ac88b177c22945902279ab626aea6d8ecc0d0a721a1f3723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataCatalogTagTemplateFieldsTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateFieldsTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e07c64c9bc342c5a5dd55de855ab1f2c1b915db73324dbba7ea08f5f27d5092f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnumType")
    def put_enum_type(
        self,
        *,
        allowed_values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param allowed_values: allowed_values block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#allowed_values DataCatalogTagTemplate#allowed_values}
        '''
        value = DataCatalogTagTemplateFieldsTypeEnumType(allowed_values=allowed_values)

        return typing.cast(None, jsii.invoke(self, "putEnumType", [value]))

    @jsii.member(jsii_name="resetEnumType")
    def reset_enum_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnumType", []))

    @jsii.member(jsii_name="resetPrimitiveType")
    def reset_primitive_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimitiveType", []))

    @builtins.property
    @jsii.member(jsii_name="enumType")
    def enum_type(self) -> DataCatalogTagTemplateFieldsTypeEnumTypeOutputReference:
        return typing.cast(DataCatalogTagTemplateFieldsTypeEnumTypeOutputReference, jsii.get(self, "enumType"))

    @builtins.property
    @jsii.member(jsii_name="enumTypeInput")
    def enum_type_input(
        self,
    ) -> typing.Optional[DataCatalogTagTemplateFieldsTypeEnumType]:
        return typing.cast(typing.Optional[DataCatalogTagTemplateFieldsTypeEnumType], jsii.get(self, "enumTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="primitiveTypeInput")
    def primitive_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primitiveTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="primitiveType")
    def primitive_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primitiveType"))

    @primitive_type.setter
    def primitive_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43230225304ba374c9cbb8f806983abd875df87aa4d83a4f6c194ad0f744efcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primitiveType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCatalogTagTemplateFieldsType]:
        return typing.cast(typing.Optional[DataCatalogTagTemplateFieldsType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCatalogTagTemplateFieldsType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3865be63516cd726644842e7fad5a778ef6320ae8225695f877b3ab1ac9dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataCatalogTagTemplateTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#create DataCatalogTagTemplate#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#delete DataCatalogTagTemplate#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#update DataCatalogTagTemplate#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965322e680979c4a8ab3e68a7248b7b0c87f7ac0277a072de8c27acdcc3e953d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#create DataCatalogTagTemplate#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#delete DataCatalogTagTemplate#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/data_catalog_tag_template#update DataCatalogTagTemplate#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogTagTemplateTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCatalogTagTemplateTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataCatalogTagTemplate.DataCatalogTagTemplateTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__334b06dd0bf0d7b6847e2b85f381188c3c9d7bf21a7d304b29282293637a9af8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b27552433031e85c000fcb6201b032ec711be4094abe0abf889c45e41c08666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aef00feae4fb67f9b915075f9a397dfe8e2e2095e42fda74f0fa8310b744e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da85bbf795e7b5adf5196d05672a88cbbc001cc5a8d9e5e6ebb5f09bea600a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e80551c5aee1bf3d969293252bc61bdcce9ba6420dadeb59c552fdef77a68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataCatalogTagTemplate",
    "DataCatalogTagTemplateConfig",
    "DataCatalogTagTemplateFields",
    "DataCatalogTagTemplateFieldsList",
    "DataCatalogTagTemplateFieldsOutputReference",
    "DataCatalogTagTemplateFieldsType",
    "DataCatalogTagTemplateFieldsTypeEnumType",
    "DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues",
    "DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesList",
    "DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValuesOutputReference",
    "DataCatalogTagTemplateFieldsTypeEnumTypeOutputReference",
    "DataCatalogTagTemplateFieldsTypeOutputReference",
    "DataCatalogTagTemplateTimeouts",
    "DataCatalogTagTemplateTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__40a22c5b3088b2d3bfd4a95e54d7b4fd3e32c4bdc7d3f67c4f88c8506ece5d8f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    fields: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCatalogTagTemplateFields, typing.Dict[builtins.str, typing.Any]]]],
    tag_template_id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataCatalogTagTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__120f3b6aaff8bf68aa721ad3c298f4d2ed0adc4d850b27cb03d328f56ed4050f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310c6df21e6edaa80c091b08cfc77105afd13aee067a39315537ac8ca83944f0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCatalogTagTemplateFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59a41d9fd7866df3d6d0934e628e7f00d3c7ab3b69a6a2e715677d0397a0543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1992814ff2a9334fc93e4c6b8024cfd1f6925f476bb48dd3f29becbdda5e77a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408155f220e4f1fba2617f8a9b311b16baca935164a27f0760f4e831800d909b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa260d79e18e4730993e7a192b8cc43344228ebc20196f7ac24421c198ca5d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668a32e33a2154e1a2651de54e6b87588cf8765152da4d2451d78bb00c298506(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4726b99cb9073a693f4c6614ee6f4f389ad64d67e953739589f1d529333ac3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4351e7cb7d29fa60f1727ebc490032226ff4fb635cb1c40dde78056082bc3b2c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fields: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCatalogTagTemplateFields, typing.Dict[builtins.str, typing.Any]]]],
    tag_template_id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataCatalogTagTemplateTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4690d544a41063a3114976d85f7b987140496ec1480415900a671efc414d1e(
    *,
    field_id: builtins.str,
    type: typing.Union[DataCatalogTagTemplateFieldsType, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    is_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1430967c042bc62cb8de598eeb5aa64749dc219a065fe9aefbdf84ae7417b0d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df89e9bf70b0060875a7f50b5e090daaa79192aa33181c61a5f534264ec8ea9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b333865494a4a2bb9e53c6a0d3a2e500df8d5626a3a038445683e2dae56c306b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b02bc39b268d6d50b055c7f60f20f054d57c0803b3ca7897bd18b62f0aea8eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e792d48f6850b113dfa6d0eae20eb83c0505ab2aff75961452b98b033edda90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea745bd645f3a723eb23cf5d772c1fb43ec6c83536d64771a39527d775dbf30(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40114745bf28394469b896b55ff3411b40dea749987e35845fad251c659de91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0eb9c1169534a1d65026abcf3fa3e6de8a792163d6749fc0d726253de748da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c206829448306913152cb53c04d3fd8d3da0487583978caff46214b2e3f1093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf1f212241d3132a816b7d36e32ab31b56af8b20033a5cfd6cdefcd1a131a64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3aad4e8054ea094390c7d47ebc047a6d4bc38e9163e620218fc74a41e748f0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72eacb3523246e5692b6880814f868c7c61df27b48a4dc1fea760ea3a1fa4b0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077dfae92ed4a23304e6d50af566749e8305312c982f511a601a08486d780eb3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateFields]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3de175c491354fd67d213d6e236018ca358e1e7c9306616b1512d2866115a95(
    *,
    enum_type: typing.Optional[typing.Union[DataCatalogTagTemplateFieldsTypeEnumType, typing.Dict[builtins.str, typing.Any]]] = None,
    primitive_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83828b5d1ed347062238338c65a1d6b464d2f1639bdca16a31c94f9ba530b258(
    *,
    allowed_values: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e069dc8820bac8d93e6f29fb6652aa0b4ef243fb97586d24272c33cf24ead55a(
    *,
    display_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459bc69410e4aed1ae7dc3ce7aef13bdaf379570774aca6ab3aca296cd68dc67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d034480dcdc6d8f6369d8c8f78086926d1e08e77c30a80e74fa41b4cee585c2b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e11aaf64bb9c646c9f102a57f49178b449f1fc298175888f408f6f84a901515(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69eec2f76c58bda41974801d91098c257d4e49126be537cb29ed733abcef8d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2add0eb38d53f303c5923338ccb7b5973b80235e1454377a54c60283b420ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7513274242acdf97d4d8a887d7227a79f547efeec3f5561eeac66a0c4659a09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8a9caaed5a65b89474303f13ed5377ac3ec273bbff72e9fc914e3145acb248(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953a620306d560c61c9a710e1872bae60090030204e1c5a2b3e43d72a5d7183d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54b5c72cea91b7c595879398ee744b37abe82fe26c4018274c37989f9d6c6b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083d9f1ddcc0ba4bd25d15431b35c3ae2c4cc1bbe4c2459e10ebf437e5e5644e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b3d6f0862823118fb0e5067a110d7cfea53a131d566aeb87d947edb8b2a4ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataCatalogTagTemplateFieldsTypeEnumTypeAllowedValues, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8978a744a282016ac88b177c22945902279ab626aea6d8ecc0d0a721a1f3723(
    value: typing.Optional[DataCatalogTagTemplateFieldsTypeEnumType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07c64c9bc342c5a5dd55de855ab1f2c1b915db73324dbba7ea08f5f27d5092f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43230225304ba374c9cbb8f806983abd875df87aa4d83a4f6c194ad0f744efcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3865be63516cd726644842e7fad5a778ef6320ae8225695f877b3ab1ac9dac(
    value: typing.Optional[DataCatalogTagTemplateFieldsType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965322e680979c4a8ab3e68a7248b7b0c87f7ac0277a072de8c27acdcc3e953d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334b06dd0bf0d7b6847e2b85f381188c3c9d7bf21a7d304b29282293637a9af8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b27552433031e85c000fcb6201b032ec711be4094abe0abf889c45e41c08666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aef00feae4fb67f9b915075f9a397dfe8e2e2095e42fda74f0fa8310b744e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da85bbf795e7b5adf5196d05672a88cbbc001cc5a8d9e5e6ebb5f09bea600a35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e80551c5aee1bf3d969293252bc61bdcce9ba6420dadeb59c552fdef77a68f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataCatalogTagTemplateTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
