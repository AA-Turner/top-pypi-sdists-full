r'''
# `data_google_oracle_database_autonomous_database`

Refer to the Terraform Registry for docs: [`data_google_oracle_database_autonomous_database`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database).
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


class DataGoogleOracleDatabaseAutonomousDatabase(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database google_oracle_database_autonomous_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        autonomous_database_id: builtins.str,
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database google_oracle_database_autonomous_database} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param autonomous_database_id: The ID of the Autonomous Database to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#autonomous_database_id DataGoogleOracleDatabaseAutonomousDatabase#autonomous_database_id}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#location DataGoogleOracleDatabaseAutonomousDatabase#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#id DataGoogleOracleDatabaseAutonomousDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#project DataGoogleOracleDatabaseAutonomousDatabase#project}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a3e6fff09404d05486c6c0442559a9e4257cd146ff1af3e4ece5f24e3372f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataGoogleOracleDatabaseAutonomousDatabaseConfig(
            autonomous_database_id=autonomous_database_id,
            location=location,
            id=id,
            project=project,
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
        '''Generates CDKTF code for importing a DataGoogleOracleDatabaseAutonomousDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataGoogleOracleDatabaseAutonomousDatabase to import.
        :param import_from_id: The id of the existing DataGoogleOracleDatabaseAutonomousDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataGoogleOracleDatabaseAutonomousDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09289cfd6032797c03255b73f413537ba459b4e7b5981075abc3dc40452b0945)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "deletionProtection"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="entitlementId")
    def entitlement_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entitlementId"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="autonomousDatabaseIdInput")
    def autonomous_database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autonomousDatabaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="autonomousDatabaseId")
    def autonomous_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autonomousDatabaseId"))

    @autonomous_database_id.setter
    def autonomous_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d29ba101a4ca92279ce479cd80082d502f4caf877ee5a28de6f903338e422d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autonomousDatabaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e66184b9b9203003c539a348b03f6ea2e16077fc51ebc888d2ac075920cbf2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d3e53316fcf95a9351eed0aac8f9c872d802d9c16a928f42dfc138e79ad77e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98f3c5c4c2fddb50c1c654dc77ead3b8715219a3321df5529bbf1114f80efe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "autonomous_database_id": "autonomousDatabaseId",
        "location": "location",
        "id": "id",
        "project": "project",
    },
)
class DataGoogleOracleDatabaseAutonomousDatabaseConfig(
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
        autonomous_database_id: builtins.str,
        location: builtins.str,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param autonomous_database_id: The ID of the Autonomous Database to create. This value is restricted to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63 characters in length. The value must start with a letter and end with a letter or a number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#autonomous_database_id DataGoogleOracleDatabaseAutonomousDatabase#autonomous_database_id}
        :param location: Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#location DataGoogleOracleDatabaseAutonomousDatabase#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#id DataGoogleOracleDatabaseAutonomousDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#project DataGoogleOracleDatabaseAutonomousDatabase#project}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510538d3dcc5639c01f05715afaff66c1983b881fca4d0a6189df5c7ce62a8a7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument autonomous_database_id", value=autonomous_database_id, expected_type=type_hints["autonomous_database_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autonomous_database_id": autonomous_database_id,
            "location": location,
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
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project

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
    def autonomous_database_id(self) -> builtins.str:
        '''The ID of the Autonomous Database to create.

        This value is restricted
        to (^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$) and must be a maximum of 63
        characters in length. The value must start with a letter and end with
        a letter or a number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#autonomous_database_id DataGoogleOracleDatabaseAutonomousDatabase#autonomous_database_id}
        '''
        result = self._values.get("autonomous_database_id")
        assert result is not None, "Required property 'autonomous_database_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Resource ID segment making up resource 'name'. See documentation for resource type 'oracledatabase.googleapis.com/AutonomousDatabaseBackup'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#location DataGoogleOracleDatabaseAutonomousDatabase#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#id DataGoogleOracleDatabaseAutonomousDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_database#project DataGoogleOracleDatabaseAutonomousDatabase#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabaseProperties",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabaseProperties:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabaseProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33a945eb6584e65cd9ecc0fdca16ac77c5a60ad019a64b286eb63fe83afb0398)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719943fb9c70cfab200877326f4f2a9ddda50bc08b0c6484d12dff9e69d8227a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbb9b530599949460c810bec015571ba610eac38430a66ef12f0317f386dd60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3492b32fa029428ec9dc80a7fda1318e98ecffee59041d2309139491d1bcb3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9039af3b215f044df1026cc97b08b643b554afc403c30a0d35d61892108bbe5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b54e71f8bf9179daa8df5132f2342aadf4df375b6e65ce2979978efc57d473d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="apexVersion")
    def apex_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apexVersion"))

    @builtins.property
    @jsii.member(jsii_name="ordsVersion")
    def ords_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ordsVersion"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72584ba4d0909b781e80d2d7594f9e23e15c5075309f4caa42ccada49e4b2027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1fecbc63fcfcc7d3ac026955dc16f6a9514263eeb66e103bc435698a70bfb33)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d6ce7612c3bb046de5033e07b3abbe2d2f993538c56c1118caa6f8fe348b46)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f33f8e752ab212097f069a000f5796c9ae62fb1bf97810fe268bfb0268c9e1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e25619450379104fb67b06a8438d3b200c0eef7f965cdb312342c99bad8316f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff7b1ac957ea5ccc71e58f88c0f950347e0d07781b3b03905ce7d1606068301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21ebddc9bf945a75f6c81fc4c1baa6d64fe72dd4d4089e195162ad9ea757f4e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="high")
    def high(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "high"))

    @builtins.property
    @jsii.member(jsii_name="low")
    def low(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "low"))

    @builtins.property
    @jsii.member(jsii_name="medium")
    def medium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "medium"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771ff867dad1f6ba186bb4626397933283b89869c8e94b5701faa78c23ea9afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc47e47c5a77462d157ad99043375f2df7b228a3353c9729edbe97954062379f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d8823ee5bce4133bf009dc7b5ff10df1e908a53abba92661867d1ed95b0429)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12b65a1d4ed7c9d7153285ca7a279afb38b098e2a9078aa404f152e7ea06ff2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b8c1fd096ef2449dfe3daca4206d6fcc65b3b8eaed2096fae5e2ddaa485d628)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65edd9f49c20514a04198a85169bd4ee7b27060d0027e63d1cf94ac7ef877af7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83825c95dd75fee8ecd9f5e44a77356fb78e1830b5b3088e8c10dade15e603a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allConnectionStrings")
    def all_connection_strings(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList, jsii.get(self, "allConnectionStrings"))

    @builtins.property
    @jsii.member(jsii_name="dedicated")
    def dedicated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicated"))

    @builtins.property
    @jsii.member(jsii_name="high")
    def high(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "high"))

    @builtins.property
    @jsii.member(jsii_name="low")
    def low(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "low"))

    @builtins.property
    @jsii.member(jsii_name="medium")
    def medium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "medium"))

    @builtins.property
    @jsii.member(jsii_name="profiles")
    def profiles(
        self,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList", jsii.get(self, "profiles"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788ee390042b308228efb07acded8d23f2a48e22bc904513988aa10f1f9ed697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d1e82ae6fdd7660b32956535ae4595b23c731b0fd57b240b83cbe3785d9a465)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91de740216e82a4b6e1e61b27877875be7d39360af250b852650e6306598aac5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a4427cb4ca14dd1532ebe3423572b8871c48e847bbb73fbbbd6b83b422093e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ad9c88b2a892d0ba1ce2e8cc4f35d686e41a5d2b21380c8e3285e0ad17fc997)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c185f5532565ba6b3e7ece8d736e5c54986df7b236e0c863dea5bb572b8bafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09812b687b8fb2f119d4cd2a7d9c16f64ee6d26ff9df4232a57106061b51bdf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="consumerGroup")
    def consumer_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroup"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="hostFormat")
    def host_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostFormat"))

    @builtins.property
    @jsii.member(jsii_name="isRegional")
    def is_regional(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isRegional"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="sessionMode")
    def session_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionMode"))

    @builtins.property
    @jsii.member(jsii_name="syntaxFormat")
    def syntax_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syntaxFormat"))

    @builtins.property
    @jsii.member(jsii_name="tlsAuthentication")
    def tls_authentication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc65f563d9fda2a637cfe94064b3ef95d4e578d268a7afc927b5a527f98b88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0c1064bb789e23c90a1745294fb1b8b4520ddcf19761a050e98cbba8ecf2278)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ea60cd286e67c12c948b46173a2ef5654bc7826442006425fff0f766e88a8b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fcc885dcff81236e8cfbfdd3246ad5c5fc51737cef9a324c85aac856611edf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f456be71b64f987727a6194604b2dce48718e7f7656d89d6d182981faf116e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b5698b4c55a3e3a465b527d97c7b99c39c6cc64f4ee4b9a1df8dd320635e5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11d3886bd22b35cd4598420b39afd4c924b150ac6253b2e213ee64f112b62239)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="apexUri")
    def apex_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apexUri"))

    @builtins.property
    @jsii.member(jsii_name="databaseTransformsUri")
    def database_transforms_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseTransformsUri"))

    @builtins.property
    @jsii.member(jsii_name="graphStudioUri")
    def graph_studio_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "graphStudioUri"))

    @builtins.property
    @jsii.member(jsii_name="machineLearningNotebookUri")
    def machine_learning_notebook_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineLearningNotebookUri"))

    @builtins.property
    @jsii.member(jsii_name="machineLearningUserManagementUri")
    def machine_learning_user_management_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineLearningUserManagementUri"))

    @builtins.property
    @jsii.member(jsii_name="mongoDbUri")
    def mongo_db_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mongoDbUri"))

    @builtins.property
    @jsii.member(jsii_name="ordsUri")
    def ords_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ordsUri"))

    @builtins.property
    @jsii.member(jsii_name="sqlDevWebUri")
    def sql_dev_web_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlDevWebUri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53019cc70115ca75c2af55fed8045808a6b396aa6aff926f4cd7ff1849babf1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__64ac46880073f8451e2f42b06d5d0947ab626c5f2026afcd5479bafe8801b4e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf5b5d0f05048154daeaff0b5ff84b84738147fbdb10f700cd91d725a2e2d2f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa3f993fd4ae6b5813521133f97a4fcdb4e898a96b90e59dda8f797d6607ed8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__579ed17b6f284e53513314d5adf673e2bca1f6797d73fcb21a81973b70d3a55f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d25dc31c4048e5dac6ce45d564b3ea78de11aa46f7ce2eb92b2d4efd9c90f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9298698de524de9c765b395f567d7459903a23f04a12a18506e3de3a821639a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57056d7e2b48d886fcda885264471b6ec73eb4c1f2e23869428fc372059bd73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1a7431b344ccd68c20252ba2f9de54f5b62bb424561db9c9d2a56ebc2a1617f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f38767ef5b6cbe236c36e29e057470184163ee48c8e0fc99798b16ca9fe5cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad83f30c4fcf88494f877c6e2c3e1a773c281f6f9277e437511adb32ec9f219)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b02b524fe0777fcdcc9a5d3318eb4d1bdce6cf3e9d60fc77c99ba05e8bb9bf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__794df2b61236c642e9d9266740735b90217b47a500e4b6f535b38cbb4893df34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3d39031761d3ef1b7327c20819614342b910f17b31579fc6f67c47bc59c2be9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9463b188d8eccc18b6abfff981af8f3c5959132f633190e8751c2f7e5efceb3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c80d3c57319ad5e29acfad085b2904b2b5adbaac47f50612c9d5213fce20ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6230f9205c6ccea62fabe356f4077dd79f37803e00968c4fef63e02cc385f2fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25175dad989d994445f98cacd442d14ab4d5fcfb84f2663fc94169e52475b528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda09e0ab901cead09d17c6292680f487106c19456395ce34934b9c51af79903)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataGuardRoleChangedTime")
    def data_guard_role_changed_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataGuardRoleChangedTime"))

    @builtins.property
    @jsii.member(jsii_name="disasterRecoveryRoleChangedTime")
    def disaster_recovery_role_changed_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "disasterRecoveryRoleChangedTime"))

    @builtins.property
    @jsii.member(jsii_name="lagTimeDuration")
    def lag_time_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lagTimeDuration"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleDetails")
    def lifecycle_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleDetails"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d090a49ea336b44ee7d4e2bbc149f7cb8c184447e6067da22d21e4e1c5c45c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6def33e2ba4e601abe17134c38e0f117e0bcf6038017bee0069ce9e381229aa7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actualUsedDataStorageSizeTb")
    def actual_used_data_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "actualUsedDataStorageSizeTb"))

    @builtins.property
    @jsii.member(jsii_name="allocatedStorageSizeTb")
    def allocated_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocatedStorageSizeTb"))

    @builtins.property
    @jsii.member(jsii_name="apexDetails")
    def apex_details(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList, jsii.get(self, "apexDetails"))

    @builtins.property
    @jsii.member(jsii_name="arePrimaryAllowlistedIpsUsed")
    def are_primary_allowlisted_ips_used(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "arePrimaryAllowlistedIpsUsed"))

    @builtins.property
    @jsii.member(jsii_name="autonomousContainerDatabaseId")
    def autonomous_container_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autonomousContainerDatabaseId"))

    @builtins.property
    @jsii.member(jsii_name="availableUpgradeVersions")
    def available_upgrade_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availableUpgradeVersions"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriodDays")
    def backup_retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetentionPeriodDays"))

    @builtins.property
    @jsii.member(jsii_name="characterSet")
    def character_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "characterSet"))

    @builtins.property
    @jsii.member(jsii_name="computeCount")
    def compute_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeCount"))

    @builtins.property
    @jsii.member(jsii_name="connectionStrings")
    def connection_strings(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList, jsii.get(self, "connectionStrings"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrls")
    def connection_urls(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList, jsii.get(self, "connectionUrls"))

    @builtins.property
    @jsii.member(jsii_name="customerContacts")
    def customer_contacts(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList, jsii.get(self, "customerContacts"))

    @builtins.property
    @jsii.member(jsii_name="databaseManagementState")
    def database_management_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseManagementState"))

    @builtins.property
    @jsii.member(jsii_name="dataSafeState")
    def data_safe_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSafeState"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeGb")
    def data_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeTb")
    def data_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeTb"))

    @builtins.property
    @jsii.member(jsii_name="dbEdition")
    def db_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbEdition"))

    @builtins.property
    @jsii.member(jsii_name="dbVersion")
    def db_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbVersion"))

    @builtins.property
    @jsii.member(jsii_name="dbWorkload")
    def db_workload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbWorkload"))

    @builtins.property
    @jsii.member(jsii_name="failedDataRecoveryDuration")
    def failed_data_recovery_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failedDataRecoveryDuration"))

    @builtins.property
    @jsii.member(jsii_name="isAutoScalingEnabled")
    def is_auto_scaling_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isAutoScalingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="isLocalDataGuardEnabled")
    def is_local_data_guard_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isLocalDataGuardEnabled"))

    @builtins.property
    @jsii.member(jsii_name="isStorageAutoScalingEnabled")
    def is_storage_auto_scaling_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isStorageAutoScalingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleDetails")
    def lifecycle_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleDetails"))

    @builtins.property
    @jsii.member(jsii_name="localAdgAutoFailoverMaxDataLossLimit")
    def local_adg_auto_failover_max_data_loss_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "localAdgAutoFailoverMaxDataLossLimit"))

    @builtins.property
    @jsii.member(jsii_name="localDisasterRecoveryType")
    def local_disaster_recovery_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localDisasterRecoveryType"))

    @builtins.property
    @jsii.member(jsii_name="localStandbyDb")
    def local_standby_db(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList, jsii.get(self, "localStandbyDb"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceBeginTime")
    def maintenance_begin_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceBeginTime"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceEndTime")
    def maintenance_end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceEndTime"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceScheduleType")
    def maintenance_schedule_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceScheduleType"))

    @builtins.property
    @jsii.member(jsii_name="memoryPerOracleComputeUnitGbs")
    def memory_per_oracle_compute_unit_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryPerOracleComputeUnitGbs"))

    @builtins.property
    @jsii.member(jsii_name="memoryTableGbs")
    def memory_table_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryTableGbs"))

    @builtins.property
    @jsii.member(jsii_name="mtlsConnectionRequired")
    def mtls_connection_required(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "mtlsConnectionRequired"))

    @builtins.property
    @jsii.member(jsii_name="nCharacterSet")
    def n_character_set(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nCharacterSet"))

    @builtins.property
    @jsii.member(jsii_name="nextLongTermBackupTime")
    def next_long_term_backup_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextLongTermBackupTime"))

    @builtins.property
    @jsii.member(jsii_name="ocid")
    def ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocid"))

    @builtins.property
    @jsii.member(jsii_name="ociUrl")
    def oci_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociUrl"))

    @builtins.property
    @jsii.member(jsii_name="openMode")
    def open_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openMode"))

    @builtins.property
    @jsii.member(jsii_name="operationsInsightsState")
    def operations_insights_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationsInsightsState"))

    @builtins.property
    @jsii.member(jsii_name="peerDbIds")
    def peer_db_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "peerDbIds"))

    @builtins.property
    @jsii.member(jsii_name="permissionLevel")
    def permission_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissionLevel"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpoint")
    def private_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpointIp")
    def private_endpoint_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpointIp"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpointLabel")
    def private_endpoint_label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateEndpointLabel"))

    @builtins.property
    @jsii.member(jsii_name="refreshableMode")
    def refreshable_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshableMode"))

    @builtins.property
    @jsii.member(jsii_name="refreshableState")
    def refreshable_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "refreshableState"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="scheduledOperationDetails")
    def scheduled_operation_details(
        self,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList", jsii.get(self, "scheduledOperationDetails"))

    @builtins.property
    @jsii.member(jsii_name="sqlWebDeveloperUrl")
    def sql_web_developer_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlWebDeveloperUrl"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="supportedCloneRegions")
    def supported_clone_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "supportedCloneRegions"))

    @builtins.property
    @jsii.member(jsii_name="totalAutoBackupStorageSizeGbs")
    def total_auto_backup_storage_size_gbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalAutoBackupStorageSizeGbs"))

    @builtins.property
    @jsii.member(jsii_name="usedDataStorageSizeTbs")
    def used_data_storage_size_tbs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "usedDataStorageSizeTbs"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabaseProperties]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabaseProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabaseProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12643994fa419c294b09ba0f025204c12b0717c402d7522135b27912e84e73b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6bda50e220306ddef9d67f18123aafd162f7b3bbc0e29bf877a4455996b1890)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f39d08d6a3fc519a5205d7dcf734e671dfcf1b80935e033bbe41d007acc2714)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d325d6e4b381b4975f96863fc1c11ced7721e0ce9b8f54ff00e15363bb932e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d48f70549a9f3eede6520828bd342f25a35f063346d176754d705e6310ef21b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__211159dd468ae0a7174fc2ed3180548394430ceb5087a305634b0206c527ddd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d83cc0dbb004e57131a4ce7922b81315716db8eb73721a8a331510ccc07dc24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(
        self,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="stopTime")
    def stop_time(
        self,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList", jsii.get(self, "stopTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0dac9f0b6bf005d2b2f6c3aef3d845c1ff5000b741a9aaaac4fd44745212c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ada76e7c3fee9071929e2ca08d60b7a4075bab4fd20f85ebc7dbaad6dbdfe1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d9fae691a79fae3e2a388b4017c98a671fa51effc6c91e2f39ea8ac2fe6588f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032bb4f04ac0e15d0a3d69bbdc2f6362af3f983bdea58ce487268b4bd297250c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e655e3a100e3744f9a58dbc39b179d1e0fabc5c3e2c49e647d5478deb2bdec2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__305089456ca2db2011696be326dfc5cd9173148beb7a580582ee07476d0322fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc048dc9923bef4e7bd8bfaa0a109432b4d9ebf81c5ad02a78a4ff2ef36a9cc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316e98a52a0bd617f6ddc36f256f5ca86cbc466b80a253f9993d453660ca9c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c96fca30076301e4e2d72109da3201cbca330b0e4085321ea9291f3ade11f35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7708838c61dd952a77ae96259a5a03a43812767fde66e4aade80a533c3719d7b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d4dc93a67a7035113700822180128a7577a7f9b55cedbba8d463093a5f0efb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8383b405e803de387b8b946662deebe183f2894bec11d1f51ad05746fe3f7cd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e9c01c4388e7c01fd47544cca7831462bc9ab8529665f3a8338e11c6843b85d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabase.DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32af3b1dbcdb8ea50bff625e67f6f2308a271e1930effcfb36c6420a1f79b65b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1126a794e6fcdd032490910328acc9fdc51d47ae7aee7ca790b70521857b1dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataGoogleOracleDatabaseAutonomousDatabase",
    "DataGoogleOracleDatabaseAutonomousDatabaseConfig",
    "DataGoogleOracleDatabaseAutonomousDatabaseProperties",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetailsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStringsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfilesOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrlsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContactsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDbOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTimeOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeList",
    "DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTimeOutputReference",
]

publication.publish()

def _typecheckingstub__91a3e6fff09404d05486c6c0442559a9e4257cd146ff1af3e4ece5f24e3372f0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    autonomous_database_id: builtins.str,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__09289cfd6032797c03255b73f413537ba459b4e7b5981075abc3dc40452b0945(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d29ba101a4ca92279ce479cd80082d502f4caf877ee5a28de6f903338e422d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e66184b9b9203003c539a348b03f6ea2e16077fc51ebc888d2ac075920cbf2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d3e53316fcf95a9351eed0aac8f9c872d802d9c16a928f42dfc138e79ad77e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98f3c5c4c2fddb50c1c654dc77ead3b8715219a3321df5529bbf1114f80efe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510538d3dcc5639c01f05715afaff66c1983b881fca4d0a6189df5c7ce62a8a7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    autonomous_database_id: builtins.str,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a945eb6584e65cd9ecc0fdca16ac77c5a60ad019a64b286eb63fe83afb0398(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719943fb9c70cfab200877326f4f2a9ddda50bc08b0c6484d12dff9e69d8227a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbb9b530599949460c810bec015571ba610eac38430a66ef12f0317f386dd60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3492b32fa029428ec9dc80a7fda1318e98ecffee59041d2309139491d1bcb3d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9039af3b215f044df1026cc97b08b643b554afc403c30a0d35d61892108bbe5f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b54e71f8bf9179daa8df5132f2342aadf4df375b6e65ce2979978efc57d473d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72584ba4d0909b781e80d2d7594f9e23e15c5075309f4caa42ccada49e4b2027(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesApexDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fecbc63fcfcc7d3ac026955dc16f6a9514263eeb66e103bc435698a70bfb33(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d6ce7612c3bb046de5033e07b3abbe2d2f993538c56c1118caa6f8fe348b46(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f33f8e752ab212097f069a000f5796c9ae62fb1bf97810fe268bfb0268c9e1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e25619450379104fb67b06a8438d3b200c0eef7f965cdb312342c99bad8316f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff7b1ac957ea5ccc71e58f88c0f950347e0d07781b3b03905ce7d1606068301(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ebddc9bf945a75f6c81fc4c1baa6d64fe72dd4d4089e195162ad9ea757f4e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771ff867dad1f6ba186bb4626397933283b89869c8e94b5701faa78c23ea9afd(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsAllConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc47e47c5a77462d157ad99043375f2df7b228a3353c9729edbe97954062379f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d8823ee5bce4133bf009dc7b5ff10df1e908a53abba92661867d1ed95b0429(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12b65a1d4ed7c9d7153285ca7a279afb38b098e2a9078aa404f152e7ea06ff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8c1fd096ef2449dfe3daca4206d6fcc65b3b8eaed2096fae5e2ddaa485d628(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65edd9f49c20514a04198a85169bd4ee7b27060d0027e63d1cf94ac7ef877af7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83825c95dd75fee8ecd9f5e44a77356fb78e1830b5b3088e8c10dade15e603a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788ee390042b308228efb07acded8d23f2a48e22bc904513988aa10f1f9ed697(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1e82ae6fdd7660b32956535ae4595b23c731b0fd57b240b83cbe3785d9a465(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91de740216e82a4b6e1e61b27877875be7d39360af250b852650e6306598aac5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a4427cb4ca14dd1532ebe3423572b8871c48e847bbb73fbbbd6b83b422093e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad9c88b2a892d0ba1ce2e8cc4f35d686e41a5d2b21380c8e3285e0ad17fc997(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c185f5532565ba6b3e7ece8d736e5c54986df7b236e0c863dea5bb572b8bafc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09812b687b8fb2f119d4cd2a7d9c16f64ee6d26ff9df4232a57106061b51bdf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc65f563d9fda2a637cfe94064b3ef95d4e578d268a7afc927b5a527f98b88e(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionStringsProfiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c1064bb789e23c90a1745294fb1b8b4520ddcf19761a050e98cbba8ecf2278(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ea60cd286e67c12c948b46173a2ef5654bc7826442006425fff0f766e88a8b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fcc885dcff81236e8cfbfdd3246ad5c5fc51737cef9a324c85aac856611edf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f456be71b64f987727a6194604b2dce48718e7f7656d89d6d182981faf116e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5698b4c55a3e3a465b527d97c7b99c39c6cc64f4ee4b9a1df8dd320635e5da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d3886bd22b35cd4598420b39afd4c924b150ac6253b2e213ee64f112b62239(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53019cc70115ca75c2af55fed8045808a6b396aa6aff926f4cd7ff1849babf1c(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesConnectionUrls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ac46880073f8451e2f42b06d5d0947ab626c5f2026afcd5479bafe8801b4e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf5b5d0f05048154daeaff0b5ff84b84738147fbdb10f700cd91d725a2e2d2f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa3f993fd4ae6b5813521133f97a4fcdb4e898a96b90e59dda8f797d6607ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579ed17b6f284e53513314d5adf673e2bca1f6797d73fcb21a81973b70d3a55f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d25dc31c4048e5dac6ce45d564b3ea78de11aa46f7ce2eb92b2d4efd9c90f50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9298698de524de9c765b395f567d7459903a23f04a12a18506e3de3a821639a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57056d7e2b48d886fcda885264471b6ec73eb4c1f2e23869428fc372059bd73(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesCustomerContacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a7431b344ccd68c20252ba2f9de54f5b62bb424561db9c9d2a56ebc2a1617f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f38767ef5b6cbe236c36e29e057470184163ee48c8e0fc99798b16ca9fe5cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad83f30c4fcf88494f877c6e2c3e1a773c281f6f9277e437511adb32ec9f219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b02b524fe0777fcdcc9a5d3318eb4d1bdce6cf3e9d60fc77c99ba05e8bb9bf0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794df2b61236c642e9d9266740735b90217b47a500e4b6f535b38cbb4893df34(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d39031761d3ef1b7327c20819614342b910f17b31579fc6f67c47bc59c2be9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9463b188d8eccc18b6abfff981af8f3c5959132f633190e8751c2f7e5efceb3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c80d3c57319ad5e29acfad085b2904b2b5adbaac47f50612c9d5213fce20ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6230f9205c6ccea62fabe356f4077dd79f37803e00968c4fef63e02cc385f2fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25175dad989d994445f98cacd442d14ab4d5fcfb84f2663fc94169e52475b528(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda09e0ab901cead09d17c6292680f487106c19456395ce34934b9c51af79903(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d090a49ea336b44ee7d4e2bbc149f7cb8c184447e6067da22d21e4e1c5c45c24(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesLocalStandbyDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6def33e2ba4e601abe17134c38e0f117e0bcf6038017bee0069ce9e381229aa7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12643994fa419c294b09ba0f025204c12b0717c402d7522135b27912e84e73b5(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabaseProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bda50e220306ddef9d67f18123aafd162f7b3bbc0e29bf877a4455996b1890(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f39d08d6a3fc519a5205d7dcf734e671dfcf1b80935e033bbe41d007acc2714(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d325d6e4b381b4975f96863fc1c11ced7721e0ce9b8f54ff00e15363bb932e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48f70549a9f3eede6520828bd342f25a35f063346d176754d705e6310ef21b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211159dd468ae0a7174fc2ed3180548394430ceb5087a305634b0206c527ddd5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d83cc0dbb004e57131a4ce7922b81315716db8eb73721a8a331510ccc07dc24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dac9f0b6bf005d2b2f6c3aef3d845c1ff5000b741a9aaaac4fd44745212c7d(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ada76e7c3fee9071929e2ca08d60b7a4075bab4fd20f85ebc7dbaad6dbdfe1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d9fae691a79fae3e2a388b4017c98a671fa51effc6c91e2f39ea8ac2fe6588f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032bb4f04ac0e15d0a3d69bbdc2f6362af3f983bdea58ce487268b4bd297250c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e655e3a100e3744f9a58dbc39b179d1e0fabc5c3e2c49e647d5478deb2bdec2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305089456ca2db2011696be326dfc5cd9173148beb7a580582ee07476d0322fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc048dc9923bef4e7bd8bfaa0a109432b4d9ebf81c5ad02a78a4ff2ef36a9cc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316e98a52a0bd617f6ddc36f256f5ca86cbc466b80a253f9993d453660ca9c73(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c96fca30076301e4e2d72109da3201cbca330b0e4085321ea9291f3ade11f35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7708838c61dd952a77ae96259a5a03a43812767fde66e4aade80a533c3719d7b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d4dc93a67a7035113700822180128a7577a7f9b55cedbba8d463093a5f0efb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8383b405e803de387b8b946662deebe183f2894bec11d1f51ad05746fe3f7cd8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9c01c4388e7c01fd47544cca7831462bc9ab8529665f3a8338e11c6843b85d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32af3b1dbcdb8ea50bff625e67f6f2308a271e1930effcfb36c6420a1f79b65b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1126a794e6fcdd032490910328acc9fdc51d47ae7aee7ca790b70521857b1dd1(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasePropertiesScheduledOperationDetailsStopTime],
) -> None:
    """Type checking stubs"""
    pass
