r'''
# `data_google_oracle_database_cloud_exadata_infrastructures`

Refer to the Terraform Registry for docs: [`data_google_oracle_database_cloud_exadata_infrastructures`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures).
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


class DataGoogleOracleDatabaseCloudExadataInfrastructures(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructures",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures google_oracle_database_cloud_exadata_infrastructures}.'''

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
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures google_oracle_database_cloud_exadata_infrastructures} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#location DataGoogleOracleDatabaseCloudExadataInfrastructures#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#id DataGoogleOracleDatabaseCloudExadataInfrastructures#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the dataset is located. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#project DataGoogleOracleDatabaseCloudExadataInfrastructures#project}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f9e5199c17d6dc39230a1fea56aaa8ce4344aa89a279e0e0840bf4046385b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataGoogleOracleDatabaseCloudExadataInfrastructuresConfig(
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
        '''Generates CDKTF code for importing a DataGoogleOracleDatabaseCloudExadataInfrastructures resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataGoogleOracleDatabaseCloudExadataInfrastructures to import.
        :param import_from_id: The id of the existing DataGoogleOracleDatabaseCloudExadataInfrastructures that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataGoogleOracleDatabaseCloudExadataInfrastructures to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9166054e2b5d704e59d3f44cecc840289fc21876980e3340d3fdfbf6aff8a27c)
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
    @jsii.member(jsii_name="cloudExadataInfrastructures")
    def cloud_exadata_infrastructures(
        self,
    ) -> "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresList":
        return typing.cast("DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresList", jsii.get(self, "cloudExadataInfrastructures"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b61d757e09eba5d0d709fc4d1f0783e26e5a63cde428aedc04f91da7e5416065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55bbbad15e2ce14c70d7c2c93d83b5fdd5e5c56b964c6dd05b3e52944266e8ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a39aafb15afe4dd7fe50fbb1f88c782431d8ab2d60a2d29e1f8c99995152e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructures",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructures:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a429010a5ce2d92a8142d1d17c9a4ca2a6a3195a089550cf13f22e17aa98cc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b628b4e9d5a9f439ee00e6b9ca0713fb3f80fecf503fd3bbdb738e10d40c30be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df9bb3df94879256e573d9d30fbe1a20e8875e267233b66ed8ca5988df37010)
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
            type_hints = typing.get_type_hints(_typecheckingstub__653058bffbf6c60314d85893e293de823860d6a25e590bdbe9f6fe76c3d9ab46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bfdb2671be6a7b3aa280d314c5365189ea27c144159e6b7b5acb8abf68a14e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fb94063754a45d93c831f0a6ce68206f6fa7d1667660da848fd96e12e6c20ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cloudExadataInfrastructureId")
    def cloud_exadata_infrastructure_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudExadataInfrastructureId"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

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
    @jsii.member(jsii_name="gcpOracleZone")
    def gcp_oracle_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpOracleZone"))

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
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesList":
        return typing.cast("DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesList", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructures]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructures], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructures],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1941aec16486abe9ea1e40f1cbd180a29d160f716eb6eeb7b62ae1e05fbc67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresProperties",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresProperties:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContacts",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContacts:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContacts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a04d83c06f7f6f12cac3c6507652c78151fb0b4f1e9d0b7525db7314441f9a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6adef2d99bfd4b63f5c07d180f0ea51fcfa9a2eccf3d962b0ff773b0ae3931)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c136770494b3c3b6548ee1e931236cf0e146467e1c8c684ca4f6e09c8b84db7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd87ebf9a241a17cc7b8e828b9a1f580020cfd8f4d6215009e54d92f7bf8ba8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db27a309e30ed951f3fa438948c99bf1896eb0e0ad8fc10383b38b2dedf8b4e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c0d56d24acdf4f55f0201559c30919d06d5be33d08d9bf321922d2e84129191)
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
    ) -> typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContacts]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContacts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContacts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03f1567a178cf604b4d7b082213300f692410548a7b89e4e61a5fe38c1e0d9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0233ca9b4bf47d4e9d1ea500c8fa67ae0b5b726625a31999dfeff3ce6c58c07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fc4919e2e0b7ef4b203250e281d8515a335b579ce286719c411b954f2f0f94)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa484b634a1d824d1712fb4e50164b530984e313bed8d213f18ed344871fe93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__017076ef025afb6ac205838a5fcf83d3e8948eaec4c44f2ad6c92bed021d53b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__246b1c59c032427d551ef6b9e2f99c54ed0f1b5b36b13918382e59d3da222755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindow:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0403f32fe3eb3ba3da8f69a56178a2acea06d9705d1c1ef018a008431a9fd7ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448118272759159b21bb96b70afceb4d905b66368b62d46278af6326fee43da1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc90f8d17bf3d8a89cad150bb8dfef5ae218a5604d1712a4230ee887db0fdf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__638d8a2aa471339ab7b8a1fb347c20ae5c0d10a6e6082086274dbca10116bf87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24a1c1b58917b01bd4d1a9960d1645c22454a2b44c5f928718984a4e3118a7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0756b363e167aa807f547ea0bf1498f3874939dfeaef188062e36e86d1c1ab94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="customActionTimeoutMins")
    def custom_action_timeout_mins(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "customActionTimeoutMins"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @builtins.property
    @jsii.member(jsii_name="hoursOfDay")
    def hours_of_day(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "hoursOfDay"))

    @builtins.property
    @jsii.member(jsii_name="isCustomActionTimeoutEnabled")
    def is_custom_action_timeout_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isCustomActionTimeoutEnabled"))

    @builtins.property
    @jsii.member(jsii_name="leadTimeWeek")
    def lead_time_week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "leadTimeWeek"))

    @builtins.property
    @jsii.member(jsii_name="months")
    def months(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "months"))

    @builtins.property
    @jsii.member(jsii_name="patchingMode")
    def patching_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "patchingMode"))

    @builtins.property
    @jsii.member(jsii_name="preference")
    def preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preference"))

    @builtins.property
    @jsii.member(jsii_name="weeksOfMonth")
    def weeks_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "weeksOfMonth"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindow]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c02153db592307e19bcea35ccac97db2dcc8f01c033b3fae47e8df71d40b874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99871d6bb9e208680e15d8d459db34c26c21154236d14848748fe193abc4e84d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="activatedStorageCount")
    def activated_storage_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "activatedStorageCount"))

    @builtins.property
    @jsii.member(jsii_name="additionalStorageCount")
    def additional_storage_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalStorageCount"))

    @builtins.property
    @jsii.member(jsii_name="availableStorageSizeGb")
    def available_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "availableStorageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="computeCount")
    def compute_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "computeCount"))

    @builtins.property
    @jsii.member(jsii_name="cpuCount")
    def cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCount"))

    @builtins.property
    @jsii.member(jsii_name="customerContacts")
    def customer_contacts(
        self,
    ) -> DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsList:
        return typing.cast(DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsList, jsii.get(self, "customerContacts"))

    @builtins.property
    @jsii.member(jsii_name="dataStorageSizeTb")
    def data_storage_size_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dataStorageSizeTb"))

    @builtins.property
    @jsii.member(jsii_name="dbNodeStorageSizeGb")
    def db_node_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dbNodeStorageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="dbServerVersion")
    def db_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbServerVersion"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowList:
        return typing.cast(DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowList, jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="maxCpuCount")
    def max_cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCpuCount"))

    @builtins.property
    @jsii.member(jsii_name="maxDataStorageTb")
    def max_data_storage_tb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDataStorageTb"))

    @builtins.property
    @jsii.member(jsii_name="maxDbNodeStorageSizeGb")
    def max_db_node_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDbNodeStorageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="maxMemoryGb")
    def max_memory_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMemoryGb"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeGb")
    def memory_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySizeGb"))

    @builtins.property
    @jsii.member(jsii_name="monthlyDbServerVersion")
    def monthly_db_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monthlyDbServerVersion"))

    @builtins.property
    @jsii.member(jsii_name="monthlyStorageServerVersion")
    def monthly_storage_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monthlyStorageServerVersion"))

    @builtins.property
    @jsii.member(jsii_name="nextMaintenanceRunId")
    def next_maintenance_run_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextMaintenanceRunId"))

    @builtins.property
    @jsii.member(jsii_name="nextMaintenanceRunTime")
    def next_maintenance_run_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextMaintenanceRunTime"))

    @builtins.property
    @jsii.member(jsii_name="nextSecurityMaintenanceRunTime")
    def next_security_maintenance_run_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextSecurityMaintenanceRunTime"))

    @builtins.property
    @jsii.member(jsii_name="ocid")
    def ocid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ocid"))

    @builtins.property
    @jsii.member(jsii_name="ociUrl")
    def oci_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociUrl"))

    @builtins.property
    @jsii.member(jsii_name="shape")
    def shape(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shape"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="storageCount")
    def storage_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageCount"))

    @builtins.property
    @jsii.member(jsii_name="storageServerVersion")
    def storage_server_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageServerVersion"))

    @builtins.property
    @jsii.member(jsii_name="totalStorageSizeGb")
    def total_storage_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "totalStorageSizeGb"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresProperties]:
        return typing.cast(typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e928ec8be1531ca8c0903435e54a440ce3857b74a3918a5faeaf4c4408d5580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataGoogleOracleDatabaseCloudExadataInfrastructures.DataGoogleOracleDatabaseCloudExadataInfrastructuresConfig",
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
class DataGoogleOracleDatabaseCloudExadataInfrastructuresConfig(
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
        :param location: location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#location DataGoogleOracleDatabaseCloudExadataInfrastructures#location}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#id DataGoogleOracleDatabaseCloudExadataInfrastructures#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The ID of the project in which the dataset is located. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#project DataGoogleOracleDatabaseCloudExadataInfrastructures#project}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d4e60cf87b87444cdc26216c431ea927f755509f34244e93b92719f3b4d409)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#location DataGoogleOracleDatabaseCloudExadataInfrastructures#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#id DataGoogleOracleDatabaseCloudExadataInfrastructures#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which the dataset is located.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/data-sources/oracle_database_cloud_exadata_infrastructures#project DataGoogleOracleDatabaseCloudExadataInfrastructures#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleOracleDatabaseCloudExadataInfrastructuresConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataGoogleOracleDatabaseCloudExadataInfrastructures",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructures",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresList",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresOutputReference",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresProperties",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContacts",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsList",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContactsOutputReference",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesList",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindow",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowList",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindowOutputReference",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesOutputReference",
    "DataGoogleOracleDatabaseCloudExadataInfrastructuresConfig",
]

publication.publish()

def _typecheckingstub__84f9e5199c17d6dc39230a1fea56aaa8ce4344aa89a279e0e0840bf4046385b1(
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

def _typecheckingstub__9166054e2b5d704e59d3f44cecc840289fc21876980e3340d3fdfbf6aff8a27c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61d757e09eba5d0d709fc4d1f0783e26e5a63cde428aedc04f91da7e5416065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bbbad15e2ce14c70d7c2c93d83b5fdd5e5c56b964c6dd05b3e52944266e8ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a39aafb15afe4dd7fe50fbb1f88c782431d8ab2d60a2d29e1f8c99995152e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a429010a5ce2d92a8142d1d17c9a4ca2a6a3195a089550cf13f22e17aa98cc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b628b4e9d5a9f439ee00e6b9ca0713fb3f80fecf503fd3bbdb738e10d40c30be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df9bb3df94879256e573d9d30fbe1a20e8875e267233b66ed8ca5988df37010(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653058bffbf6c60314d85893e293de823860d6a25e590bdbe9f6fe76c3d9ab46(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfdb2671be6a7b3aa280d314c5365189ea27c144159e6b7b5acb8abf68a14e1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb94063754a45d93c831f0a6ce68206f6fa7d1667660da848fd96e12e6c20ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1941aec16486abe9ea1e40f1cbd180a29d160f716eb6eeb7b62ae1e05fbc67(
    value: typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructures],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a04d83c06f7f6f12cac3c6507652c78151fb0b4f1e9d0b7525db7314441f9a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6adef2d99bfd4b63f5c07d180f0ea51fcfa9a2eccf3d962b0ff773b0ae3931(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c136770494b3c3b6548ee1e931236cf0e146467e1c8c684ca4f6e09c8b84db7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd87ebf9a241a17cc7b8e828b9a1f580020cfd8f4d6215009e54d92f7bf8ba8d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db27a309e30ed951f3fa438948c99bf1896eb0e0ad8fc10383b38b2dedf8b4e3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0d56d24acdf4f55f0201559c30919d06d5be33d08d9bf321922d2e84129191(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03f1567a178cf604b4d7b082213300f692410548a7b89e4e61a5fe38c1e0d9c(
    value: typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesCustomerContacts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0233ca9b4bf47d4e9d1ea500c8fa67ae0b5b726625a31999dfeff3ce6c58c07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fc4919e2e0b7ef4b203250e281d8515a335b579ce286719c411b954f2f0f94(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa484b634a1d824d1712fb4e50164b530984e313bed8d213f18ed344871fe93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017076ef025afb6ac205838a5fcf83d3e8948eaec4c44f2ad6c92bed021d53b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246b1c59c032427d551ef6b9e2f99c54ed0f1b5b36b13918382e59d3da222755(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0403f32fe3eb3ba3da8f69a56178a2acea06d9705d1c1ef018a008431a9fd7ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448118272759159b21bb96b70afceb4d905b66368b62d46278af6326fee43da1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc90f8d17bf3d8a89cad150bb8dfef5ae218a5604d1712a4230ee887db0fdf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638d8a2aa471339ab7b8a1fb347c20ae5c0d10a6e6082086274dbca10116bf87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a1c1b58917b01bd4d1a9960d1645c22454a2b44c5f928718984a4e3118a7e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0756b363e167aa807f547ea0bf1498f3874939dfeaef188062e36e86d1c1ab94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c02153db592307e19bcea35ccac97db2dcc8f01c033b3fae47e8df71d40b874(
    value: typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresPropertiesMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99871d6bb9e208680e15d8d459db34c26c21154236d14848748fe193abc4e84d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e928ec8be1531ca8c0903435e54a440ce3857b74a3918a5faeaf4c4408d5580(
    value: typing.Optional[DataGoogleOracleDatabaseCloudExadataInfrastructuresCloudExadataInfrastructuresProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d4e60cf87b87444cdc26216c431ea927f755509f34244e93b92719f3b4d409(
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
