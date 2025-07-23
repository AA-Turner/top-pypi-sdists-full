r'''
# `google_document_ai_warehouse_location`

Refer to the Terraform Registry for docs: [`google_document_ai_warehouse_location`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location).
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


class DocumentAiWarehouseLocation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseLocation.DocumentAiWarehouseLocation",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location google_document_ai_warehouse_location}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_control_mode: builtins.str,
        database_type: builtins.str,
        location: builtins.str,
        project_number: builtins.str,
        document_creator_default_role: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DocumentAiWarehouseLocationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location google_document_ai_warehouse_location} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_control_mode: The access control mode for accessing the customer data. Possible values: ["ACL_MODE_DOCUMENT_LEVEL_ACCESS_CONTROL_GCI", "ACL_MODE_DOCUMENT_LEVEL_ACCESS_CONTROL_BYOID", "ACL_MODE_UNIVERSAL_ACCESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#access_control_mode DocumentAiWarehouseLocation#access_control_mode}
        :param database_type: The type of database used to store customer data. Possible values: ["DB_INFRA_SPANNER", "DB_CLOUD_SQL_POSTGRES"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#database_type DocumentAiWarehouseLocation#database_type}
        :param location: The location in which the instance is to be provisioned. It takes the form projects/{projectNumber}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#location DocumentAiWarehouseLocation#location}
        :param project_number: The unique identifier of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#project_number DocumentAiWarehouseLocation#project_number}
        :param document_creator_default_role: The default role for the person who create a document. Possible values: ["DOCUMENT_ADMIN", "DOCUMENT_EDITOR", "DOCUMENT_VIEWER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#document_creator_default_role DocumentAiWarehouseLocation#document_creator_default_role}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#id DocumentAiWarehouseLocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: The KMS key used for CMEK encryption. It is required that the kms key is in the same region as the endpoint. The same key will be used for all provisioned resources, if encryption is available. If the kmsKey is left empty, no encryption will be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#kms_key DocumentAiWarehouseLocation#kms_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#timeouts DocumentAiWarehouseLocation#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c99eaf489fbfb94342f377b86eeb09d48dc0a1131bfc12c28250ef19c91e56b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DocumentAiWarehouseLocationConfig(
            access_control_mode=access_control_mode,
            database_type=database_type,
            location=location,
            project_number=project_number,
            document_creator_default_role=document_creator_default_role,
            id=id,
            kms_key=kms_key,
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
        '''Generates CDKTF code for importing a DocumentAiWarehouseLocation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DocumentAiWarehouseLocation to import.
        :param import_from_id: The id of the existing DocumentAiWarehouseLocation that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DocumentAiWarehouseLocation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be85a446bd36110c6341579fd02386e1505a01e116447a5aa7d0246a85133699)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#create DocumentAiWarehouseLocation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#delete DocumentAiWarehouseLocation#delete}.
        '''
        value = DocumentAiWarehouseLocationTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDocumentCreatorDefaultRole")
    def reset_document_creator_default_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentCreatorDefaultRole", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DocumentAiWarehouseLocationTimeoutsOutputReference":
        return typing.cast("DocumentAiWarehouseLocationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessControlModeInput")
    def access_control_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessControlModeInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseTypeInput")
    def database_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="documentCreatorDefaultRoleInput")
    def document_creator_default_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentCreatorDefaultRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectNumberInput")
    def project_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DocumentAiWarehouseLocationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DocumentAiWarehouseLocationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessControlMode")
    def access_control_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessControlMode"))

    @access_control_mode.setter
    def access_control_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e544148d48f926dc6b2dd3c70a29477e2ce3bc741fa05b8fe1a45191c0b11484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessControlMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseType")
    def database_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseType"))

    @database_type.setter
    def database_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea535f926bf3fe2194ebff7ccb8d8440e352796e5cfee3ee80ab69c349e0393c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="documentCreatorDefaultRole")
    def document_creator_default_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentCreatorDefaultRole"))

    @document_creator_default_role.setter
    def document_creator_default_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c61b6444f589406f616fbaf7d3e9476a6ce05ca3dd98ab4b54d4f31631bc8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentCreatorDefaultRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2856b5b405a7a43134d3828278ad6385c88823a856203d3666b5513646b7b5ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13b34b093f37da4ba906aabe8542cdc4d3daf66e83d8cc3fe60f803716befa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eaefcf1b8984f8d428ed6364cb12f1e1aab320c83f0e829b6acba2f09233112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectNumber")
    def project_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectNumber"))

    @project_number.setter
    def project_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5e6409aeb42c81202651b4e0471f588fc0d277a52785564d26ff3a5d5b3d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectNumber", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseLocation.DocumentAiWarehouseLocationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_control_mode": "accessControlMode",
        "database_type": "databaseType",
        "location": "location",
        "project_number": "projectNumber",
        "document_creator_default_role": "documentCreatorDefaultRole",
        "id": "id",
        "kms_key": "kmsKey",
        "timeouts": "timeouts",
    },
)
class DocumentAiWarehouseLocationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_control_mode: builtins.str,
        database_type: builtins.str,
        location: builtins.str,
        project_number: builtins.str,
        document_creator_default_role: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DocumentAiWarehouseLocationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_control_mode: The access control mode for accessing the customer data. Possible values: ["ACL_MODE_DOCUMENT_LEVEL_ACCESS_CONTROL_GCI", "ACL_MODE_DOCUMENT_LEVEL_ACCESS_CONTROL_BYOID", "ACL_MODE_UNIVERSAL_ACCESS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#access_control_mode DocumentAiWarehouseLocation#access_control_mode}
        :param database_type: The type of database used to store customer data. Possible values: ["DB_INFRA_SPANNER", "DB_CLOUD_SQL_POSTGRES"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#database_type DocumentAiWarehouseLocation#database_type}
        :param location: The location in which the instance is to be provisioned. It takes the form projects/{projectNumber}/locations/{location}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#location DocumentAiWarehouseLocation#location}
        :param project_number: The unique identifier of the project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#project_number DocumentAiWarehouseLocation#project_number}
        :param document_creator_default_role: The default role for the person who create a document. Possible values: ["DOCUMENT_ADMIN", "DOCUMENT_EDITOR", "DOCUMENT_VIEWER"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#document_creator_default_role DocumentAiWarehouseLocation#document_creator_default_role}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#id DocumentAiWarehouseLocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key: The KMS key used for CMEK encryption. It is required that the kms key is in the same region as the endpoint. The same key will be used for all provisioned resources, if encryption is available. If the kmsKey is left empty, no encryption will be enforced. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#kms_key DocumentAiWarehouseLocation#kms_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#timeouts DocumentAiWarehouseLocation#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DocumentAiWarehouseLocationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c94373e6798b32c1ac69a6fa0a273cdacf1f35cc68badc6a57f84dd4d9d697)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_control_mode", value=access_control_mode, expected_type=type_hints["access_control_mode"])
            check_type(argname="argument database_type", value=database_type, expected_type=type_hints["database_type"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project_number", value=project_number, expected_type=type_hints["project_number"])
            check_type(argname="argument document_creator_default_role", value=document_creator_default_role, expected_type=type_hints["document_creator_default_role"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_control_mode": access_control_mode,
            "database_type": database_type,
            "location": location,
            "project_number": project_number,
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
        if document_creator_default_role is not None:
            self._values["document_creator_default_role"] = document_creator_default_role
        if id is not None:
            self._values["id"] = id
        if kms_key is not None:
            self._values["kms_key"] = kms_key
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
    def access_control_mode(self) -> builtins.str:
        '''The access control mode for accessing the customer data. Possible values: ["ACL_MODE_DOCUMENT_LEVEL_ACCESS_CONTROL_GCI", "ACL_MODE_DOCUMENT_LEVEL_ACCESS_CONTROL_BYOID", "ACL_MODE_UNIVERSAL_ACCESS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#access_control_mode DocumentAiWarehouseLocation#access_control_mode}
        '''
        result = self._values.get("access_control_mode")
        assert result is not None, "Required property 'access_control_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_type(self) -> builtins.str:
        '''The type of database used to store customer data. Possible values: ["DB_INFRA_SPANNER", "DB_CLOUD_SQL_POSTGRES"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#database_type DocumentAiWarehouseLocation#database_type}
        '''
        result = self._values.get("database_type")
        assert result is not None, "Required property 'database_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location in which the instance is to be provisioned. It takes the form projects/{projectNumber}/locations/{location}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#location DocumentAiWarehouseLocation#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_number(self) -> builtins.str:
        '''The unique identifier of the project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#project_number DocumentAiWarehouseLocation#project_number}
        '''
        result = self._values.get("project_number")
        assert result is not None, "Required property 'project_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def document_creator_default_role(self) -> typing.Optional[builtins.str]:
        '''The default role for the person who create a document. Possible values: ["DOCUMENT_ADMIN", "DOCUMENT_EDITOR", "DOCUMENT_VIEWER"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#document_creator_default_role DocumentAiWarehouseLocation#document_creator_default_role}
        '''
        result = self._values.get("document_creator_default_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#id DocumentAiWarehouseLocation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The KMS key used for CMEK encryption.

        It is required that
        the kms key is in the same region as the endpoint. The
        same key will be used for all provisioned resources, if
        encryption is available. If the kmsKey is left empty, no
        encryption will be enforced.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#kms_key DocumentAiWarehouseLocation#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DocumentAiWarehouseLocationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#timeouts DocumentAiWarehouseLocation#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DocumentAiWarehouseLocationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseLocationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.documentAiWarehouseLocation.DocumentAiWarehouseLocationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class DocumentAiWarehouseLocationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#create DocumentAiWarehouseLocation#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#delete DocumentAiWarehouseLocation#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688d8f14c4b5e7c250b02cab5b185604f7688282be009f3675436d57bc630811)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#create DocumentAiWarehouseLocation#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/document_ai_warehouse_location#delete DocumentAiWarehouseLocation#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocumentAiWarehouseLocationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DocumentAiWarehouseLocationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.documentAiWarehouseLocation.DocumentAiWarehouseLocationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6e42cd153ab1afd9f60b300082059c4aa54f60a998560c29d1b6f2a363ed9ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c139e7c86bffdc5dccb5d6ac274e0287de036bc85217e942e1324815cfd0556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cbb0842fb4d4d664ae8d7c8fd07618d7ce7f360127f2c6c82a95151c520986a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseLocationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseLocationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseLocationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbcdce8912633d02b8db9dca93e07b6776d2ec4c9f4725306c4cc4bb44babd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DocumentAiWarehouseLocation",
    "DocumentAiWarehouseLocationConfig",
    "DocumentAiWarehouseLocationTimeouts",
    "DocumentAiWarehouseLocationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6c99eaf489fbfb94342f377b86eeb09d48dc0a1131bfc12c28250ef19c91e56b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_control_mode: builtins.str,
    database_type: builtins.str,
    location: builtins.str,
    project_number: builtins.str,
    document_creator_default_role: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DocumentAiWarehouseLocationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__be85a446bd36110c6341579fd02386e1505a01e116447a5aa7d0246a85133699(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e544148d48f926dc6b2dd3c70a29477e2ce3bc741fa05b8fe1a45191c0b11484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea535f926bf3fe2194ebff7ccb8d8440e352796e5cfee3ee80ab69c349e0393c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c61b6444f589406f616fbaf7d3e9476a6ce05ca3dd98ab4b54d4f31631bc8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2856b5b405a7a43134d3828278ad6385c88823a856203d3666b5513646b7b5ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13b34b093f37da4ba906aabe8542cdc4d3daf66e83d8cc3fe60f803716befa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eaefcf1b8984f8d428ed6364cb12f1e1aab320c83f0e829b6acba2f09233112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5e6409aeb42c81202651b4e0471f588fc0d277a52785564d26ff3a5d5b3d5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c94373e6798b32c1ac69a6fa0a273cdacf1f35cc68badc6a57f84dd4d9d697(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_control_mode: builtins.str,
    database_type: builtins.str,
    location: builtins.str,
    project_number: builtins.str,
    document_creator_default_role: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DocumentAiWarehouseLocationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688d8f14c4b5e7c250b02cab5b185604f7688282be009f3675436d57bc630811(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e42cd153ab1afd9f60b300082059c4aa54f60a998560c29d1b6f2a363ed9ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c139e7c86bffdc5dccb5d6ac274e0287de036bc85217e942e1324815cfd0556(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbb0842fb4d4d664ae8d7c8fd07618d7ce7f360127f2c6c82a95151c520986a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbcdce8912633d02b8db9dca93e07b6776d2ec4c9f4725306c4cc4bb44babd8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DocumentAiWarehouseLocationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
