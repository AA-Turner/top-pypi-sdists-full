r'''
# `google_bigtable_authorized_view`

Refer to the Terraform Registry for docs: [`google_bigtable_authorized_view`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view).
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


class BigtableAuthorizedView(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedView",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view google_bigtable_authorized_view}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_name: builtins.str,
        name: builtins.str,
        table_name: builtins.str,
        deletion_protection: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        subset_view: typing.Optional[typing.Union["BigtableAuthorizedViewSubsetView", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigtableAuthorizedViewTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view google_bigtable_authorized_view} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_name: The name of the Bigtable instance in which the authorized view belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#instance_name BigtableAuthorizedView#instance_name}
        :param name: The name of the authorized view. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#name BigtableAuthorizedView#name}
        :param table_name: The name of the Bigtable table in which the authorized view belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#table_name BigtableAuthorizedView#table_name}
        :param deletion_protection: A field to make the authorized view protected against data loss i.e. when set to PROTECTED, deleting the authorized view, the table containing the authorized view, and the instance containing the authorized view would be prohibited. If not provided, currently deletion protection will be set to UNPROTECTED as it is the API default value. Note this field configs the deletion protection provided by the API in the backend, and should not be confused with Terraform-side deletion protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#deletion_protection BigtableAuthorizedView#deletion_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#id BigtableAuthorizedView#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#project BigtableAuthorizedView#project}
        :param subset_view: subset_view block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#subset_view BigtableAuthorizedView#subset_view}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#timeouts BigtableAuthorizedView#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea1e77cf10aa3e3156a90636fc0b05881da887a31a29ec867b7c01229bcb2c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigtableAuthorizedViewConfig(
            instance_name=instance_name,
            name=name,
            table_name=table_name,
            deletion_protection=deletion_protection,
            id=id,
            project=project,
            subset_view=subset_view,
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
        '''Generates CDKTF code for importing a BigtableAuthorizedView resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigtableAuthorizedView to import.
        :param import_from_id: The id of the existing BigtableAuthorizedView that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigtableAuthorizedView to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f29fa2755c7b6791b7480a41879a8423cfcfb670475b9be3afa09fc1199e79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSubsetView")
    def put_subset_view(
        self,
        *,
        family_subsets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigtableAuthorizedViewSubsetViewFamilySubsets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        row_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param family_subsets: family_subsets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#family_subsets BigtableAuthorizedView#family_subsets}
        :param row_prefixes: Base64-encoded row prefixes to be included in the authorized view. To provide access to all rows, include the empty string as a prefix (""). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#row_prefixes BigtableAuthorizedView#row_prefixes}
        '''
        value = BigtableAuthorizedViewSubsetView(
            family_subsets=family_subsets, row_prefixes=row_prefixes
        )

        return typing.cast(None, jsii.invoke(self, "putSubsetView", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#create BigtableAuthorizedView#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#update BigtableAuthorizedView#update}.
        '''
        value = BigtableAuthorizedViewTimeouts(create=create, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSubsetView")
    def reset_subset_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubsetView", []))

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
    @jsii.member(jsii_name="subsetView")
    def subset_view(self) -> "BigtableAuthorizedViewSubsetViewOutputReference":
        return typing.cast("BigtableAuthorizedViewSubsetViewOutputReference", jsii.get(self, "subsetView"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigtableAuthorizedViewTimeoutsOutputReference":
        return typing.cast("BigtableAuthorizedViewTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceNameInput")
    def instance_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="subsetViewInput")
    def subset_view_input(self) -> typing.Optional["BigtableAuthorizedViewSubsetView"]:
        return typing.cast(typing.Optional["BigtableAuthorizedViewSubsetView"], jsii.get(self, "subsetViewInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigtableAuthorizedViewTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigtableAuthorizedViewTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3486e349c25e3a2415c5d65168d8417591f826e14d44ab43a12629274f424e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a24efe9780ab289a81d7620d821ae684f2571d15915cf5d5a021103a4dee7c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceName")
    def instance_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceName"))

    @instance_name.setter
    def instance_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c2c5afcc0f31f3c3d79de873a628088d019d8baa56ba9e35e3cbc213e440af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a7f43bb3fc80b6f8f35f37bc28e35e5cdd2c80eceeb5fe827640182da5f3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eadae0cdd062472fe999a8b9c596b3f01530013de57d621923b20b8dfaa1b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093c73163487b1a2f44c907ef70b173468ac313c04a0eea8215bc5cf3bacb023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedViewConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_name": "instanceName",
        "name": "name",
        "table_name": "tableName",
        "deletion_protection": "deletionProtection",
        "id": "id",
        "project": "project",
        "subset_view": "subsetView",
        "timeouts": "timeouts",
    },
)
class BigtableAuthorizedViewConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_name: builtins.str,
        name: builtins.str,
        table_name: builtins.str,
        deletion_protection: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        subset_view: typing.Optional[typing.Union["BigtableAuthorizedViewSubsetView", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigtableAuthorizedViewTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_name: The name of the Bigtable instance in which the authorized view belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#instance_name BigtableAuthorizedView#instance_name}
        :param name: The name of the authorized view. Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#name BigtableAuthorizedView#name}
        :param table_name: The name of the Bigtable table in which the authorized view belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#table_name BigtableAuthorizedView#table_name}
        :param deletion_protection: A field to make the authorized view protected against data loss i.e. when set to PROTECTED, deleting the authorized view, the table containing the authorized view, and the instance containing the authorized view would be prohibited. If not provided, currently deletion protection will be set to UNPROTECTED as it is the API default value. Note this field configs the deletion protection provided by the API in the backend, and should not be confused with Terraform-side deletion protection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#deletion_protection BigtableAuthorizedView#deletion_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#id BigtableAuthorizedView#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the resource belongs. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#project BigtableAuthorizedView#project}
        :param subset_view: subset_view block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#subset_view BigtableAuthorizedView#subset_view}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#timeouts BigtableAuthorizedView#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(subset_view, dict):
            subset_view = BigtableAuthorizedViewSubsetView(**subset_view)
        if isinstance(timeouts, dict):
            timeouts = BigtableAuthorizedViewTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb316e5c40de6d46c99aed28c77a0e282642361104a8318254cbd109a826e9da)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument subset_view", value=subset_view, expected_type=type_hints["subset_view"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_name": instance_name,
            "name": name,
            "table_name": table_name,
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
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if subset_view is not None:
            self._values["subset_view"] = subset_view
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
    def instance_name(self) -> builtins.str:
        '''The name of the Bigtable instance in which the authorized view belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#instance_name BigtableAuthorizedView#instance_name}
        '''
        result = self._values.get("instance_name")
        assert result is not None, "Required property 'instance_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the authorized view.

        Must be 1-50 characters and must only contain hyphens, underscores, periods, letters and numbers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#name BigtableAuthorizedView#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''The name of the Bigtable table in which the authorized view belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#table_name BigtableAuthorizedView#table_name}
        '''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.str]:
        '''A field to make the authorized view protected against data loss i.e. when set to PROTECTED, deleting the authorized view, the table containing the authorized view, and the instance containing the authorized view would be prohibited. If not provided, currently deletion protection will be set to UNPROTECTED as it is the API default value. Note this field configs the deletion protection provided by the API in the backend, and should not be confused with Terraform-side deletion protection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#deletion_protection BigtableAuthorizedView#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#id BigtableAuthorizedView#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the resource belongs.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#project BigtableAuthorizedView#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subset_view(self) -> typing.Optional["BigtableAuthorizedViewSubsetView"]:
        '''subset_view block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#subset_view BigtableAuthorizedView#subset_view}
        '''
        result = self._values.get("subset_view")
        return typing.cast(typing.Optional["BigtableAuthorizedViewSubsetView"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigtableAuthorizedViewTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#timeouts BigtableAuthorizedView#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigtableAuthorizedViewTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableAuthorizedViewConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedViewSubsetView",
    jsii_struct_bases=[],
    name_mapping={"family_subsets": "familySubsets", "row_prefixes": "rowPrefixes"},
)
class BigtableAuthorizedViewSubsetView:
    def __init__(
        self,
        *,
        family_subsets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigtableAuthorizedViewSubsetViewFamilySubsets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        row_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param family_subsets: family_subsets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#family_subsets BigtableAuthorizedView#family_subsets}
        :param row_prefixes: Base64-encoded row prefixes to be included in the authorized view. To provide access to all rows, include the empty string as a prefix (""). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#row_prefixes BigtableAuthorizedView#row_prefixes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13bedd5db978bc4029e9244abf3c68337bedebbe764aeb74027e5c9b83126137)
            check_type(argname="argument family_subsets", value=family_subsets, expected_type=type_hints["family_subsets"])
            check_type(argname="argument row_prefixes", value=row_prefixes, expected_type=type_hints["row_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if family_subsets is not None:
            self._values["family_subsets"] = family_subsets
        if row_prefixes is not None:
            self._values["row_prefixes"] = row_prefixes

    @builtins.property
    def family_subsets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigtableAuthorizedViewSubsetViewFamilySubsets"]]]:
        '''family_subsets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#family_subsets BigtableAuthorizedView#family_subsets}
        '''
        result = self._values.get("family_subsets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigtableAuthorizedViewSubsetViewFamilySubsets"]]], result)

    @builtins.property
    def row_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Base64-encoded row prefixes to be included in the authorized view.

        To provide access to all rows, include the empty string as a prefix ("").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#row_prefixes BigtableAuthorizedView#row_prefixes}
        '''
        result = self._values.get("row_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableAuthorizedViewSubsetView(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedViewSubsetViewFamilySubsets",
    jsii_struct_bases=[],
    name_mapping={
        "family_name": "familyName",
        "qualifier_prefixes": "qualifierPrefixes",
        "qualifiers": "qualifiers",
    },
)
class BigtableAuthorizedViewSubsetViewFamilySubsets:
    def __init__(
        self,
        *,
        family_name: builtins.str,
        qualifier_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        qualifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param family_name: Name of the column family to be included in the authorized view. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#family_name BigtableAuthorizedView#family_name}
        :param qualifier_prefixes: Base64-encoded prefixes for qualifiers of the column family to be included in the authorized view. Every qualifier starting with one of these prefixes is included in the authorized view. To provide access to all qualifiers, include the empty string as a prefix (""). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#qualifier_prefixes BigtableAuthorizedView#qualifier_prefixes}
        :param qualifiers: Base64-encoded individual exact column qualifiers of the column family to be included in the authorized view. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#qualifiers BigtableAuthorizedView#qualifiers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7317994fa38d8e646346d52905a198592c3683a6ebb6f998b364d37c676c351f)
            check_type(argname="argument family_name", value=family_name, expected_type=type_hints["family_name"])
            check_type(argname="argument qualifier_prefixes", value=qualifier_prefixes, expected_type=type_hints["qualifier_prefixes"])
            check_type(argname="argument qualifiers", value=qualifiers, expected_type=type_hints["qualifiers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "family_name": family_name,
        }
        if qualifier_prefixes is not None:
            self._values["qualifier_prefixes"] = qualifier_prefixes
        if qualifiers is not None:
            self._values["qualifiers"] = qualifiers

    @builtins.property
    def family_name(self) -> builtins.str:
        '''Name of the column family to be included in the authorized view.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#family_name BigtableAuthorizedView#family_name}
        '''
        result = self._values.get("family_name")
        assert result is not None, "Required property 'family_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qualifier_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Base64-encoded prefixes for qualifiers of the column family to be included in the authorized view.

        Every qualifier starting with one of these prefixes is included in the authorized view. To provide access to all qualifiers, include the empty string as a prefix ("").

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#qualifier_prefixes BigtableAuthorizedView#qualifier_prefixes}
        '''
        result = self._values.get("qualifier_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def qualifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Base64-encoded individual exact column qualifiers of the column family to be included in the authorized view.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#qualifiers BigtableAuthorizedView#qualifiers}
        '''
        result = self._values.get("qualifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableAuthorizedViewSubsetViewFamilySubsets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableAuthorizedViewSubsetViewFamilySubsetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedViewSubsetViewFamilySubsetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97c126cd7c0dfcc8304db4ea74d15eaf6209b97006d06d5f64143c6f9bb6b75c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BigtableAuthorizedViewSubsetViewFamilySubsetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e98b0f1de2b9f10bc4e8deec516016fd202270af1226c9d3dbc4c3ae50dffe5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigtableAuthorizedViewSubsetViewFamilySubsetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4739618e860cd273f4456de0c0a687efb84904af8ee3c0df559ace341e8d6510)
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
            type_hints = typing.get_type_hints(_typecheckingstub__289ce32a388d35856b0d0afec5ba9ba3980e3acdd9533134364b92d92a1d25f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3c197618ebbcf177be0b4a1519c0e2cce63abd229a45ecb6a2970b89b792a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableAuthorizedViewSubsetViewFamilySubsets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableAuthorizedViewSubsetViewFamilySubsets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableAuthorizedViewSubsetViewFamilySubsets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82851f77eed7be863cf86f0aeaccf4efb2e158a4a7201acfb1fc85c75034e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigtableAuthorizedViewSubsetViewFamilySubsetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedViewSubsetViewFamilySubsetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__caa81da54dd05db938d04f2abd767fd19d8d1f3db55bd66f125f194e0d6e1f67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetQualifierPrefixes")
    def reset_qualifier_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQualifierPrefixes", []))

    @jsii.member(jsii_name="resetQualifiers")
    def reset_qualifiers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQualifiers", []))

    @builtins.property
    @jsii.member(jsii_name="familyNameInput")
    def family_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "familyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="qualifierPrefixesInput")
    def qualifier_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "qualifierPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="qualifiersInput")
    def qualifiers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "qualifiersInput"))

    @builtins.property
    @jsii.member(jsii_name="familyName")
    def family_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "familyName"))

    @family_name.setter
    def family_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5590a751f1ac3ff8c82a78af40771cc8574d0b3418f9a57ede6fd9d64f10fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "familyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qualifierPrefixes")
    def qualifier_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "qualifierPrefixes"))

    @qualifier_prefixes.setter
    def qualifier_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbca245beaac5145a26b3da927a764f734219c777e407244586d086fc1f1acf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifierPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qualifiers")
    def qualifiers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "qualifiers"))

    @qualifiers.setter
    def qualifiers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2483ac41b6e7231d1bc6657aa4fc71c9bc935ab296b67ba9afc38abe9c9345e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifiers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableAuthorizedViewSubsetViewFamilySubsets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableAuthorizedViewSubsetViewFamilySubsets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableAuthorizedViewSubsetViewFamilySubsets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69bcb48fc2e2bdb6006e8997dbaf96dd8af684cbc83b74dc38fa5d1ee91c239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigtableAuthorizedViewSubsetViewOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedViewSubsetViewOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cbe89cce42da62f64580d287d5bcaa35c40b139b49227d34317df4555812071)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFamilySubsets")
    def put_family_subsets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableAuthorizedViewSubsetViewFamilySubsets, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb179bf99390d3bc0e9f1176b826424776d44ab41fce1a0169e5d9e7fbdb291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFamilySubsets", [value]))

    @jsii.member(jsii_name="resetFamilySubsets")
    def reset_family_subsets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFamilySubsets", []))

    @jsii.member(jsii_name="resetRowPrefixes")
    def reset_row_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowPrefixes", []))

    @builtins.property
    @jsii.member(jsii_name="familySubsets")
    def family_subsets(self) -> BigtableAuthorizedViewSubsetViewFamilySubsetsList:
        return typing.cast(BigtableAuthorizedViewSubsetViewFamilySubsetsList, jsii.get(self, "familySubsets"))

    @builtins.property
    @jsii.member(jsii_name="familySubsetsInput")
    def family_subsets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableAuthorizedViewSubsetViewFamilySubsets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableAuthorizedViewSubsetViewFamilySubsets]]], jsii.get(self, "familySubsetsInput"))

    @builtins.property
    @jsii.member(jsii_name="rowPrefixesInput")
    def row_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rowPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="rowPrefixes")
    def row_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rowPrefixes"))

    @row_prefixes.setter
    def row_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b7c8d63029950c03743ecc075b20fe6790c96e98ee57b0b5d5dc20395cdc58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rowPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigtableAuthorizedViewSubsetView]:
        return typing.cast(typing.Optional[BigtableAuthorizedViewSubsetView], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigtableAuthorizedViewSubsetView],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90744dd1becee56b9efcba9611c08bf014db2aedf34929e8b8483046a2cbea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedViewTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "update": "update"},
)
class BigtableAuthorizedViewTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#create BigtableAuthorizedView#create}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#update BigtableAuthorizedView#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54055ffd4a1eca8a1fd0fa7fc46b87bf79a92038ac125c0eaa62a6128750f9f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#create BigtableAuthorizedView#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigtable_authorized_view#update BigtableAuthorizedView#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigtableAuthorizedViewTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigtableAuthorizedViewTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigtableAuthorizedView.BigtableAuthorizedViewTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__05030c7721b9b0b66c69c68a5d582f2204716fa952b767091f5d9a648774d0b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9ee8f736d3363df201fc7875e04c472047cdec98c06f70073432a3bb4147aa8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31b78cb2d7caa89c1657502d76ce980df73f524af1c9f36328f0f490bdeb3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableAuthorizedViewTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableAuthorizedViewTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableAuthorizedViewTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83761049605e56900588f7d2e0d39592f44a12b4a4b0d070153408758952ef16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigtableAuthorizedView",
    "BigtableAuthorizedViewConfig",
    "BigtableAuthorizedViewSubsetView",
    "BigtableAuthorizedViewSubsetViewFamilySubsets",
    "BigtableAuthorizedViewSubsetViewFamilySubsetsList",
    "BigtableAuthorizedViewSubsetViewFamilySubsetsOutputReference",
    "BigtableAuthorizedViewSubsetViewOutputReference",
    "BigtableAuthorizedViewTimeouts",
    "BigtableAuthorizedViewTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__eea1e77cf10aa3e3156a90636fc0b05881da887a31a29ec867b7c01229bcb2c0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_name: builtins.str,
    name: builtins.str,
    table_name: builtins.str,
    deletion_protection: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    subset_view: typing.Optional[typing.Union[BigtableAuthorizedViewSubsetView, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigtableAuthorizedViewTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__61f29fa2755c7b6791b7480a41879a8423cfcfb670475b9be3afa09fc1199e79(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3486e349c25e3a2415c5d65168d8417591f826e14d44ab43a12629274f424e68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a24efe9780ab289a81d7620d821ae684f2571d15915cf5d5a021103a4dee7c1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c2c5afcc0f31f3c3d79de873a628088d019d8baa56ba9e35e3cbc213e440af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a7f43bb3fc80b6f8f35f37bc28e35e5cdd2c80eceeb5fe827640182da5f3ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eadae0cdd062472fe999a8b9c596b3f01530013de57d621923b20b8dfaa1b81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093c73163487b1a2f44c907ef70b173468ac313c04a0eea8215bc5cf3bacb023(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb316e5c40de6d46c99aed28c77a0e282642361104a8318254cbd109a826e9da(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_name: builtins.str,
    name: builtins.str,
    table_name: builtins.str,
    deletion_protection: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    subset_view: typing.Optional[typing.Union[BigtableAuthorizedViewSubsetView, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigtableAuthorizedViewTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13bedd5db978bc4029e9244abf3c68337bedebbe764aeb74027e5c9b83126137(
    *,
    family_subsets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableAuthorizedViewSubsetViewFamilySubsets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    row_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7317994fa38d8e646346d52905a198592c3683a6ebb6f998b364d37c676c351f(
    *,
    family_name: builtins.str,
    qualifier_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    qualifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c126cd7c0dfcc8304db4ea74d15eaf6209b97006d06d5f64143c6f9bb6b75c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e98b0f1de2b9f10bc4e8deec516016fd202270af1226c9d3dbc4c3ae50dffe5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4739618e860cd273f4456de0c0a687efb84904af8ee3c0df559ace341e8d6510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__289ce32a388d35856b0d0afec5ba9ba3980e3acdd9533134364b92d92a1d25f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c197618ebbcf177be0b4a1519c0e2cce63abd229a45ecb6a2970b89b792a58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82851f77eed7be863cf86f0aeaccf4efb2e158a4a7201acfb1fc85c75034e4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigtableAuthorizedViewSubsetViewFamilySubsets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa81da54dd05db938d04f2abd767fd19d8d1f3db55bd66f125f194e0d6e1f67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5590a751f1ac3ff8c82a78af40771cc8574d0b3418f9a57ede6fd9d64f10fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbca245beaac5145a26b3da927a764f734219c777e407244586d086fc1f1acf6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2483ac41b6e7231d1bc6657aa4fc71c9bc935ab296b67ba9afc38abe9c9345e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69bcb48fc2e2bdb6006e8997dbaf96dd8af684cbc83b74dc38fa5d1ee91c239(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableAuthorizedViewSubsetViewFamilySubsets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbe89cce42da62f64580d287d5bcaa35c40b139b49227d34317df4555812071(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb179bf99390d3bc0e9f1176b826424776d44ab41fce1a0169e5d9e7fbdb291(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigtableAuthorizedViewSubsetViewFamilySubsets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b7c8d63029950c03743ecc075b20fe6790c96e98ee57b0b5d5dc20395cdc58(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90744dd1becee56b9efcba9611c08bf014db2aedf34929e8b8483046a2cbea6(
    value: typing.Optional[BigtableAuthorizedViewSubsetView],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54055ffd4a1eca8a1fd0fa7fc46b87bf79a92038ac125c0eaa62a6128750f9f(
    *,
    create: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05030c7721b9b0b66c69c68a5d582f2204716fa952b767091f5d9a648774d0b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee8f736d3363df201fc7875e04c472047cdec98c06f70073432a3bb4147aa8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31b78cb2d7caa89c1657502d76ce980df73f524af1c9f36328f0f490bdeb3cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83761049605e56900588f7d2e0d39592f44a12b4a4b0d070153408758952ef16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigtableAuthorizedViewTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
