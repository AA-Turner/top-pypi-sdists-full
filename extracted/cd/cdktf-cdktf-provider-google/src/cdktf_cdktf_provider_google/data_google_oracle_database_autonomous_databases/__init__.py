r'''
# `data_google_oracle_database_autonomous_databases`

Refer to the Terraform Registry for docs: [`data_google_oracle_database_autonomous_databases`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases).
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


class DataGoogleOracleDatabaseAutonomousDatabases(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabases",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases google_oracle_database_autonomous_databases}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases google_oracle_database_autonomous_databases} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#location DataGoogleOracleDatabaseAutonomousDatabases#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#id DataGoogleOracleDatabaseAutonomousDatabases#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the dataset is located. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#project DataGoogleOracleDatabaseAutonomousDatabases#project}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5e55fa1ade1a0ec1fb3e62282afa92ff6dbd27e413b600722709d0a80f972e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataGoogleOracleDatabaseAutonomousDatabasesConfig(
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
        '''Generates CDKTF code for importing a DataGoogleOracleDatabaseAutonomousDatabases resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataGoogleOracleDatabaseAutonomousDatabases to import.
        :param import_from_id: The id of the existing DataGoogleOracleDatabaseAutonomousDatabases that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataGoogleOracleDatabaseAutonomousDatabases to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc4dd5a0e07b5f7313c00a9a3fa481b2c449ea5190fc809fb2e911678e77b9f)
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
    @jsii.member(jsii_name="autonomousDatabases")
    def autonomous_databases(
        self,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesList", jsii.get(self, "autonomousDatabases"))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14e62e237313ef46b59739b07d908ea525bded44039bbd21774904c96ca7bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccd8652dce095de916e0e6c1e0618bf3c07ca373ba795ba0f5ce93fb1b9a8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71da51ad89a65220026bc688880cc04484d5213b7e1d3a9b4091f21f637918fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabases",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabases:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d54927ad885f7eded708f5fd43795d76012dbc2f0ff026b232721670d44f3e65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e923222a370b89b861874377f5f677c527c87b6790a6eecf8b43f7663f8db8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3335ec29b228f1db73a37cedaa7bd3c636e47d9a27f5fa47003c4d617962e0d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e928ae9c4ea99bdb77f40f8a4d84d2a0ceeed94cbf8f0cc4b00b090c3c7d7053)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1354f2874b1c7eccb07e46bee4c4c236d4ef794650de3941ecbc1e19ee95482a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dfd9a66e0151edef52ab17aa00b0ca56ef244dbbb29355c4c9dea6e29ebebb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @builtins.property
    @jsii.member(jsii_name="autonomousDatabaseId")
    def autonomous_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autonomousDatabaseId"))

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
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabases]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabases], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabases],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb5cf14f03f15538ea69c2f9539da6808b8b26fc201d215257bd01fa161fd52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesProperties",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesProperties:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__610ffa87a16b35bc1f6adc1fb84723c698ca57e909596d9194deadd9abeeff70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d27e9b40a8dbe48b52a50c548b3e4a384ba8dbb2fa33d2c11f7eae98c1f8aa1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e12256add20f910f3ac3b6c480341a742b1f978b60df257283234adc44b403)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c543ad95c6e751464b2269603e947c411a0f3fd5f4b4c15c74a51027802672f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f2ac6fee343070caa641b9474cb1558d485057b0cc2a7f907cb663437b8ffbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cafbc29d06175361e0659f42d0a67f81351690214fbc768b45298f48a9d9d356)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetails]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62424e0c283bee963b0b1232102426928c71a0878cb860535f5015b60b20c80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38bbb2ab96d3c44bdd5e665acdee875bc5c9e6163fb3abcdbb356ca49020adcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2daf586ddc6bcc9747b75c91a89d18423331cfa604104b74c686e14a2315b0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05702f11b09e91011b64f2ab3bad15907073e79c248f86cc2e72786724f9cf85)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7ca789e4aa09bfc8bebd277c349a014216a2b38d23f90f8bea6e4c59fc05a36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7729ce018155c87b07b814978d5f0e9f481ac3c10e889c98f640b7cfad8995f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abcb7b21f8792d1e81b9b1258955333d8364741a523942bf929e38caad607b42)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStrings]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e36cd5f5597cf2cc7551e086c172b65a2ba87c65c1b86da0cf839f637cd52c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65ee68d32d5d045d30a669810d593a5b00276eeaf47e806e40555851c03f681c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594aa2342dd7f5b4eedbb16b9cd728128a6b2095969a487acbe377d88f76fb13)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40de190910037862214ed5f629572d2a2bd3d1cc46aec3cf2167c76f190ac4b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df8167f8e702780799c6d00074ba63d8394a79aba5b90f36e037d73a3450bcad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50eb39d1885610a8b487072642da46d5091ff9668a8736ce7fd1f7d4f0e06ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__228ff54a7c9501930207feee84ca797be14eb03e58bcd3882815c0daa9604e60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allConnectionStrings")
    def all_connection_strings(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsList, jsii.get(self, "allConnectionStrings"))

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
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesList", jsii.get(self, "profiles"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStrings]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad2502ebc776e92ae3d4ece36b009956344a53ecabc99c97c5b5bf4a9e0c920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfiles",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfiles:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfiles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e85505cfc01d3d57ebb669d9244386f6daea41c56c8782f5453749f19cb92083)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da50fe9f6e30d58f4476ccb7118adc10c7e9f8e77040d09c2bd50f71ab8535c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0138806baf3de1663bcacd1579367ec43a9293c8747b99bdb3fec68328da5c0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c5d2a52489b7a0dcb35f46fd11d71415a1764a71a3f5f337af208dd6d678861)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed1b881e4317b14419b0f5ff97bf1140b0fb201bdf99352bc7d40bec3dbecc72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaef2a56c5386e53ae6fcafb33b3b50533a6daecd4b7183fe0a2bf0533d5ed95)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfiles]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfiles], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfiles],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01475078d77017e13905400e223f3be81d2cc28e751781f0725741e252522494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrls",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrls:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__116f84f1db08bd6f21ca03620cbe56ad9803c460182cab2230fd68d2289d0c45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0226f96311d5522e818255e573a0e31b93b42c64eb4421fd430c61ea092e1f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca94cd2642eaa8127b9f9a99f65617870061c1df00e1c5d4dc86cdfd2c01a19c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__431b9f52f05594e37a0c37e457e73a6ac884ed21dd72b73340d1871ab15163a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9968b19e2d5b60c0f936a1733a59025ee3d9a103576702ade54bbb4af6615de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccac289c4df0dec4ee4abd2e0cdc25fa1c3ed0e55ef7fcc78c0e8b502dcce0bc)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrls]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a6e3f791ac57c957ebbdd8746d748059d28ab2af64a77dcd1de46379ebfcb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContacts",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContacts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3aba69094b6a177f3743f692d0583677d26a4c54fbd8a950c1bdc4bf23dfe4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10386f3f4b35465c8b4baf6d9a02659c8f857fd8b26f620382365340575ee6d3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9801d40dbae35649ae12b76f2c56d3b8c10d528359c22ff1622a515cb9fca4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cafbd0ecdb0b02ad093e631d3eeb1eb69aa8b524a3be2f7653900302ee51f55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73d4201ac0e8b51343dd6deaeb92709f015241d80a27b2edad9fd28e4bda96d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1346e14c44f40399af7fb1c2aaf93a16ed389470db853c31c765837da4df7d9d)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContacts]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContacts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContacts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29ad91beabae6e4ab314f23dc9c42e188d63a1bde13f03507f5c444d16dd3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66cbd30234b587a3eb3745cebb0745062d87b6b2b9c994deaf495644ddc8d86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7aa9ed5fb10b20c86114417733f24131156d6de9338eae41551b1617f83e3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ceac0d9826c9ae4ed921d9f4bde3e9cf472015030a9c0701939bd35b2a2f0e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a9cbf14c39f9682fb79576cdaff86089b3dee0189add9ba2a1e5acec41dcecf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92c4f25cc9da60618b69b990ffc24c053b051c0fa6ce36c7d895d650a52e870d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDb",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDb:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__726aea8b6062a075a768b5999ee8745e08a46013033b9889a945ca6fa09b3715)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efaad9ae26a3b84317abc89ab5cc39cd9bcc85f4bbd306fd18722acf9eac4044)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a2f59cf6f4e7fbbf2faa5586b8ca27a5cf95c16ea78f9a987f1e5d3a4b0fd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be12b46d6fb7d7af1757d66906eae2729513e74ba638b5c86a2c0a2a83bfeb1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78adf14fd7a7915b5ccad9b408f971a4edfaf62346a21f2489a11590e6e5fbb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__450fe43b5f25216c3bd66ac72cf018d08348276a3ff5ced357f551b636e34f69)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDb]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d20b3acc43574d808693ea676f5ac068e72b6916f7d7b47653b6bce7696f3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__141c1b2ddda2717e09badd0ddb94c5516e37035760204539a4c02c13ac1e3f85)
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
    ) -> DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsList, jsii.get(self, "apexDetails"))

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
    ) -> DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsList, jsii.get(self, "connectionStrings"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrls")
    def connection_urls(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsList, jsii.get(self, "connectionUrls"))

    @builtins.property
    @jsii.member(jsii_name="customerContacts")
    def customer_contacts(
        self,
    ) -> DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsList, jsii.get(self, "customerContacts"))

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
    ) -> DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbList:
        return typing.cast(DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbList, jsii.get(self, "localStandbyDb"))

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
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsList", jsii.get(self, "scheduledOperationDetails"))

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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesProperties]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3aae6a22b28b63f87d9186c5943e04a57ddff743089b10de0086cf3b85e6b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__609c1c8ed6e29346c5fe2b534bf357a5032befeecdc2eeeff5ab96c3e2fcb176)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e70cc7ab6a5f135e0789165fe7dfceb40e93c74634147e343078caab8ac8fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8613921f657e4ff1d542ce98c8b244985a8faa66ac1c99409d0fb2eb5b5363)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cf91e8d983ad0dbc81bd2af3f78f2a0db3dbd75049554e232cf755272a7e160)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb4f1f43622cd7a86f7d09a8aefd7bbed6d76928e3745ca4c18c56e3ebb2490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4da6818f35ffcffb94e28823c75edff077b76324d6b969f9400654d154f1c11c)
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
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeList", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="stopTime")
    def stop_time(
        self,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeList":
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeList", jsii.get(self, "stopTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetails]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf120d2933d077625b4a22e7e230788a4554f416e663f099b00dc69fbda978e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTime",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTime:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7e912b298fdd06bee425869e4964c6289335a51317b47c5eb02bdd009ab69e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9791ba5f2b152b5f99f3ca646fae42588bbc180237c0c3e9a52d61bdffa277c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccee85cd09dc45dd29b43f9b0f2bc4423fba8553d38d08a2508f4a86ab09571c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0368a2ea427d4e1988049d1f0dee2b7820229143e95bd24870603187a5dd239a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__487531a78b559ffd425206422fb6a5cf9050b459c115816b6a39cb24c7780511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__908f7c0f4df6437ba51145e5acd7bc2a55ea8be53083a474c1b9fad2539b0c5b)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTime]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329ceabe4f79911adadcef55993891ef7b10df27fbf88696275cb7e848bf50f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTime",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTime:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9519aad23fb2a74b0ce73e55eebbe9945fec70f9bd36ebc40cb8834b4e0c990c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a660dae18e7709ea1f1b2056adf8857b2c42dea5ddf25c1d4715cb2e57e14e0c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c157bec433a3f5798981c3a3b85011a47553e60021dbc8a50495378630363d9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11e9db1a3e8b42ee18c7f16995751dba23d7a9e0a44231098194c3a3bef2f265)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5e6c42c5a717ef820e3ab01f569ee135c179369fdc0926ac26b321cdac35646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa95986189b24c5b06099105f1482f6dd45f6664481d3742e9ff9d9d176e69e)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTime]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07e84307b55cddd2c52b245b16df1498aa246b928f51471bab50eb08947e4d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseAutonomousDatabases.DataGoogleOracleDatabaseAutonomousDatabasesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "id": "id",
        "project": "project",
    },
)
class DataGoogleOracleDatabaseAutonomousDatabasesConfig(
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
        :param location: location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#location DataGoogleOracleDatabaseAutonomousDatabases#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#id DataGoogleOracleDatabaseAutonomousDatabases#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the dataset is located. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#project DataGoogleOracleDatabaseAutonomousDatabases#project}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148da19cb2f8cab40478f83cd3ba69fa51f5442bd57aa0cc22747548bbfb3f53)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
    def location(self) -> builtins.str:
        '''location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#location DataGoogleOracleDatabaseAutonomousDatabases#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#id DataGoogleOracleDatabaseAutonomousDatabases#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the dataset is located.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_autonomous_databases#project DataGoogleOracleDatabaseAutonomousDatabases#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseAutonomousDatabasesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataGoogleOracleDatabaseAutonomousDatabases",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabases",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesProperties",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetails",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetailsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStrings",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStrings",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStringsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfiles",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfilesOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrls",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrlsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContacts",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContactsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDb",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDbOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetails",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTime",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTimeOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTime",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeList",
    "DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTimeOutputReference",
    "DataGoogleOracleDatabaseAutonomousDatabasesConfig",
]

publication.publish()

def _typecheckingstub__3a5e55fa1ade1a0ec1fb3e62282afa92ff6dbd27e413b600722709d0a80f972e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
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

def _typecheckingstub__ffc4dd5a0e07b5f7313c00a9a3fa481b2c449ea5190fc809fb2e911678e77b9f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14e62e237313ef46b59739b07d908ea525bded44039bbd21774904c96ca7bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccd8652dce095de916e0e6c1e0618bf3c07ca373ba795ba0f5ce93fb1b9a8e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71da51ad89a65220026bc688880cc04484d5213b7e1d3a9b4091f21f637918fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54927ad885f7eded708f5fd43795d76012dbc2f0ff026b232721670d44f3e65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e923222a370b89b861874377f5f677c527c87b6790a6eecf8b43f7663f8db8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3335ec29b228f1db73a37cedaa7bd3c636e47d9a27f5fa47003c4d617962e0d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e928ae9c4ea99bdb77f40f8a4d84d2a0ceeed94cbf8f0cc4b00b090c3c7d7053(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1354f2874b1c7eccb07e46bee4c4c236d4ef794650de3941ecbc1e19ee95482a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dfd9a66e0151edef52ab17aa00b0ca56ef244dbbb29355c4c9dea6e29ebebb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb5cf14f03f15538ea69c2f9539da6808b8b26fc201d215257bd01fa161fd52(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabases],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610ffa87a16b35bc1f6adc1fb84723c698ca57e909596d9194deadd9abeeff70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d27e9b40a8dbe48b52a50c548b3e4a384ba8dbb2fa33d2c11f7eae98c1f8aa1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e12256add20f910f3ac3b6c480341a742b1f978b60df257283234adc44b403(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c543ad95c6e751464b2269603e947c411a0f3fd5f4b4c15c74a51027802672f1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2ac6fee343070caa641b9474cb1558d485057b0cc2a7f907cb663437b8ffbc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafbc29d06175361e0659f42d0a67f81351690214fbc768b45298f48a9d9d356(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62424e0c283bee963b0b1232102426928c71a0878cb860535f5015b60b20c80(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesApexDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38bbb2ab96d3c44bdd5e665acdee875bc5c9e6163fb3abcdbb356ca49020adcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2daf586ddc6bcc9747b75c91a89d18423331cfa604104b74c686e14a2315b0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05702f11b09e91011b64f2ab3bad15907073e79c248f86cc2e72786724f9cf85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ca789e4aa09bfc8bebd277c349a014216a2b38d23f90f8bea6e4c59fc05a36(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7729ce018155c87b07b814978d5f0e9f481ac3c10e889c98f640b7cfad8995f7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcb7b21f8792d1e81b9b1258955333d8364741a523942bf929e38caad607b42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e36cd5f5597cf2cc7551e086c172b65a2ba87c65c1b86da0cf839f637cd52c3(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsAllConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ee68d32d5d045d30a669810d593a5b00276eeaf47e806e40555851c03f681c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594aa2342dd7f5b4eedbb16b9cd728128a6b2095969a487acbe377d88f76fb13(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40de190910037862214ed5f629572d2a2bd3d1cc46aec3cf2167c76f190ac4b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8167f8e702780799c6d00074ba63d8394a79aba5b90f36e037d73a3450bcad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50eb39d1885610a8b487072642da46d5091ff9668a8736ce7fd1f7d4f0e06ef8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228ff54a7c9501930207feee84ca797be14eb03e58bcd3882815c0daa9604e60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad2502ebc776e92ae3d4ece36b009956344a53ecabc99c97c5b5bf4a9e0c920(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85505cfc01d3d57ebb669d9244386f6daea41c56c8782f5453749f19cb92083(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da50fe9f6e30d58f4476ccb7118adc10c7e9f8e77040d09c2bd50f71ab8535c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0138806baf3de1663bcacd1579367ec43a9293c8747b99bdb3fec68328da5c0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5d2a52489b7a0dcb35f46fd11d71415a1764a71a3f5f337af208dd6d678861(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1b881e4317b14419b0f5ff97bf1140b0fb201bdf99352bc7d40bec3dbecc72(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaef2a56c5386e53ae6fcafb33b3b50533a6daecd4b7183fe0a2bf0533d5ed95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01475078d77017e13905400e223f3be81d2cc28e751781f0725741e252522494(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionStringsProfiles],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116f84f1db08bd6f21ca03620cbe56ad9803c460182cab2230fd68d2289d0c45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0226f96311d5522e818255e573a0e31b93b42c64eb4421fd430c61ea092e1f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca94cd2642eaa8127b9f9a99f65617870061c1df00e1c5d4dc86cdfd2c01a19c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431b9f52f05594e37a0c37e457e73a6ac884ed21dd72b73340d1871ab15163a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9968b19e2d5b60c0f936a1733a59025ee3d9a103576702ade54bbb4af6615de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccac289c4df0dec4ee4abd2e0cdc25fa1c3ed0e55ef7fcc78c0e8b502dcce0bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a6e3f791ac57c957ebbdd8746d748059d28ab2af64a77dcd1de46379ebfcb5(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesConnectionUrls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3aba69094b6a177f3743f692d0583677d26a4c54fbd8a950c1bdc4bf23dfe4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10386f3f4b35465c8b4baf6d9a02659c8f857fd8b26f620382365340575ee6d3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9801d40dbae35649ae12b76f2c56d3b8c10d528359c22ff1622a515cb9fca4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cafbd0ecdb0b02ad093e631d3eeb1eb69aa8b524a3be2f7653900302ee51f55(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d4201ac0e8b51343dd6deaeb92709f015241d80a27b2edad9fd28e4bda96d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1346e14c44f40399af7fb1c2aaf93a16ed389470db853c31c765837da4df7d9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29ad91beabae6e4ab314f23dc9c42e188d63a1bde13f03507f5c444d16dd3e4(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesCustomerContacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66cbd30234b587a3eb3745cebb0745062d87b6b2b9c994deaf495644ddc8d86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7aa9ed5fb10b20c86114417733f24131156d6de9338eae41551b1617f83e3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ceac0d9826c9ae4ed921d9f4bde3e9cf472015030a9c0701939bd35b2a2f0e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9cbf14c39f9682fb79576cdaff86089b3dee0189add9ba2a1e5acec41dcecf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c4f25cc9da60618b69b990ffc24c053b051c0fa6ce36c7d895d650a52e870d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726aea8b6062a075a768b5999ee8745e08a46013033b9889a945ca6fa09b3715(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efaad9ae26a3b84317abc89ab5cc39cd9bcc85f4bbd306fd18722acf9eac4044(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a2f59cf6f4e7fbbf2faa5586b8ca27a5cf95c16ea78f9a987f1e5d3a4b0fd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be12b46d6fb7d7af1757d66906eae2729513e74ba638b5c86a2c0a2a83bfeb1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78adf14fd7a7915b5ccad9b408f971a4edfaf62346a21f2489a11590e6e5fbb4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450fe43b5f25216c3bd66ac72cf018d08348276a3ff5ced357f551b636e34f69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d20b3acc43574d808693ea676f5ac068e72b6916f7d7b47653b6bce7696f3ea(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesLocalStandbyDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__141c1b2ddda2717e09badd0ddb94c5516e37035760204539a4c02c13ac1e3f85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3aae6a22b28b63f87d9186c5943e04a57ddff743089b10de0086cf3b85e6b6d(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609c1c8ed6e29346c5fe2b534bf357a5032befeecdc2eeeff5ab96c3e2fcb176(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e70cc7ab6a5f135e0789165fe7dfceb40e93c74634147e343078caab8ac8fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8613921f657e4ff1d542ce98c8b244985a8faa66ac1c99409d0fb2eb5b5363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf91e8d983ad0dbc81bd2af3f78f2a0db3dbd75049554e232cf755272a7e160(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb4f1f43622cd7a86f7d09a8aefd7bbed6d76928e3745ca4c18c56e3ebb2490(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da6818f35ffcffb94e28823c75edff077b76324d6b969f9400654d154f1c11c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf120d2933d077625b4a22e7e230788a4554f416e663f099b00dc69fbda978e(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e912b298fdd06bee425869e4964c6289335a51317b47c5eb02bdd009ab69e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9791ba5f2b152b5f99f3ca646fae42588bbc180237c0c3e9a52d61bdffa277c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccee85cd09dc45dd29b43f9b0f2bc4423fba8553d38d08a2508f4a86ab09571c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0368a2ea427d4e1988049d1f0dee2b7820229143e95bd24870603187a5dd239a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487531a78b559ffd425206422fb6a5cf9050b459c115816b6a39cb24c7780511(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908f7c0f4df6437ba51145e5acd7bc2a55ea8be53083a474c1b9fad2539b0c5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329ceabe4f79911adadcef55993891ef7b10df27fbf88696275cb7e848bf50f0(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9519aad23fb2a74b0ce73e55eebbe9945fec70f9bd36ebc40cb8834b4e0c990c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a660dae18e7709ea1f1b2056adf8857b2c42dea5ddf25c1d4715cb2e57e14e0c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c157bec433a3f5798981c3a3b85011a47553e60021dbc8a50495378630363d9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e9db1a3e8b42ee18c7f16995751dba23d7a9e0a44231098194c3a3bef2f265(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e6c42c5a717ef820e3ab01f569ee135c179369fdc0926ac26b321cdac35646(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa95986189b24c5b06099105f1482f6dd45f6664481d3742e9ff9d9d176e69e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07e84307b55cddd2c52b245b16df1498aa246b928f51471bab50eb08947e4d7(
    value: typing.Optional[DataGoogleOracleDatabaseAutonomousDatabasesAutonomousDatabasesPropertiesScheduledOperationDetailsStopTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148da19cb2f8cab40478f83cd3ba69fa51f5442bd57aa0cc22747548bbfb3f53(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
