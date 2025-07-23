r'''
# `google_kms_ekm_connection`

Refer to the Terraform Registry for docs: [`google_kms_ekm_connection`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection).
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


class KmsEkmConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection google_kms_ekm_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        service_resolvers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KmsEkmConnectionServiceResolvers", typing.Dict[builtins.str, typing.Any]]]],
        crypto_space_path: typing.Optional[builtins.str] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        key_management_mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KmsEkmConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection google_kms_ekm_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location for the EkmConnection. A full list of valid locations can be found by running 'gcloud kms locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#location KmsEkmConnection#location}
        :param name: The resource name for the EkmConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#name KmsEkmConnection#name}
        :param service_resolvers: service_resolvers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#service_resolvers KmsEkmConnection#service_resolvers}
        :param crypto_space_path: Optional. Identifies the EKM Crypto Space that this EkmConnection maps to. Note: This field is required if KeyManagementMode is CLOUD_KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#crypto_space_path KmsEkmConnection#crypto_space_path}
        :param etag: Optional. Etag of the currently stored EkmConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#etag KmsEkmConnection#etag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#id KmsEkmConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_management_mode: Optional. Describes who can perform control plane operations on the EKM. If unset, this defaults to MANUAL Default value: "MANUAL" Possible values: ["MANUAL", "CLOUD_KMS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#key_management_mode KmsEkmConnection#key_management_mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#project KmsEkmConnection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#timeouts KmsEkmConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae12cf2a9064e8a31c8b30ee56e1093f1bcab330df06762bb7efa9398aba781)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KmsEkmConnectionConfig(
            location=location,
            name=name,
            service_resolvers=service_resolvers,
            crypto_space_path=crypto_space_path,
            etag=etag,
            id=id,
            key_management_mode=key_management_mode,
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
        '''Generates CDKTF code for importing a KmsEkmConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KmsEkmConnection to import.
        :param import_from_id: The id of the existing KmsEkmConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KmsEkmConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abaf2b675c02aac93331eec133c7952df3dd131ec94288bf7b8c6456fbcea78b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putServiceResolvers")
    def put_service_resolvers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KmsEkmConnectionServiceResolvers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1db00369ddb82dce878640312a79c321e93a787e53f0b962bc3eeb6ba0b82f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceResolvers", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#create KmsEkmConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#delete KmsEkmConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#update KmsEkmConnection#update}.
        '''
        value = KmsEkmConnectionTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCryptoSpacePath")
    def reset_crypto_space_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCryptoSpacePath", []))

    @jsii.member(jsii_name="resetEtag")
    def reset_etag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEtag", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeyManagementMode")
    def reset_key_management_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyManagementMode", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="serviceResolvers")
    def service_resolvers(self) -> "KmsEkmConnectionServiceResolversList":
        return typing.cast("KmsEkmConnectionServiceResolversList", jsii.get(self, "serviceResolvers"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KmsEkmConnectionTimeoutsOutputReference":
        return typing.cast("KmsEkmConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cryptoSpacePathInput")
    def crypto_space_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cryptoSpacePathInput"))

    @builtins.property
    @jsii.member(jsii_name="etagInput")
    def etag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "etagInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyManagementModeInput")
    def key_management_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyManagementModeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceResolversInput")
    def service_resolvers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KmsEkmConnectionServiceResolvers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KmsEkmConnectionServiceResolvers"]]], jsii.get(self, "serviceResolversInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KmsEkmConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KmsEkmConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cryptoSpacePath")
    def crypto_space_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cryptoSpacePath"))

    @crypto_space_path.setter
    def crypto_space_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5ed46e1eb16c9831e39fbaf6e01e1521756b159c26f00057926a81af9cf41f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cryptoSpacePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @etag.setter
    def etag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185bd22a62cc5471d4f08ae083ef20a45524e3438cb5e17c83e8f90429dc454f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "etag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db8963959610a5697f17618c1d7d307a8ee93d9c6ce0dabedf3c229b5c4ef550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyManagementMode")
    def key_management_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyManagementMode"))

    @key_management_mode.setter
    def key_management_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef4fbf6bb61b922ca8e3aa897fe1a5d2932908fb0d3c35da648b0b325c59a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyManagementMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8099f8a7e1831bebb62789213b7ded2c7c256e47f84cf7672f86721d2db6c9d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8b2f72888e73d1cd8460c3a1a6c604f2e0f3874f9046367edde5ef46e4c780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3c6801b4a304b83068a8ca571a3a937726b232d1f6a93f83fbcae6cca838ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionConfig",
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
        "name": "name",
        "service_resolvers": "serviceResolvers",
        "crypto_space_path": "cryptoSpacePath",
        "etag": "etag",
        "id": "id",
        "key_management_mode": "keyManagementMode",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class KmsEkmConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        service_resolvers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KmsEkmConnectionServiceResolvers", typing.Dict[builtins.str, typing.Any]]]],
        crypto_space_path: typing.Optional[builtins.str] = None,
        etag: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        key_management_mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["KmsEkmConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location for the EkmConnection. A full list of valid locations can be found by running 'gcloud kms locations list'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#location KmsEkmConnection#location}
        :param name: The resource name for the EkmConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#name KmsEkmConnection#name}
        :param service_resolvers: service_resolvers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#service_resolvers KmsEkmConnection#service_resolvers}
        :param crypto_space_path: Optional. Identifies the EKM Crypto Space that this EkmConnection maps to. Note: This field is required if KeyManagementMode is CLOUD_KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#crypto_space_path KmsEkmConnection#crypto_space_path}
        :param etag: Optional. Etag of the currently stored EkmConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#etag KmsEkmConnection#etag}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#id KmsEkmConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key_management_mode: Optional. Describes who can perform control plane operations on the EKM. If unset, this defaults to MANUAL Default value: "MANUAL" Possible values: ["MANUAL", "CLOUD_KMS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#key_management_mode KmsEkmConnection#key_management_mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#project KmsEkmConnection#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#timeouts KmsEkmConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = KmsEkmConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2638bdf80fd303f6133fceb41479b04faf51d475585b65c8d6a62216256684)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_resolvers", value=service_resolvers, expected_type=type_hints["service_resolvers"])
            check_type(argname="argument crypto_space_path", value=crypto_space_path, expected_type=type_hints["crypto_space_path"])
            check_type(argname="argument etag", value=etag, expected_type=type_hints["etag"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key_management_mode", value=key_management_mode, expected_type=type_hints["key_management_mode"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "service_resolvers": service_resolvers,
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
        if crypto_space_path is not None:
            self._values["crypto_space_path"] = crypto_space_path
        if etag is not None:
            self._values["etag"] = etag
        if id is not None:
            self._values["id"] = id
        if key_management_mode is not None:
            self._values["key_management_mode"] = key_management_mode
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
    def location(self) -> builtins.str:
        '''The location for the EkmConnection. A full list of valid locations can be found by running 'gcloud kms locations list'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#location KmsEkmConnection#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name for the EkmConnection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#name KmsEkmConnection#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_resolvers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KmsEkmConnectionServiceResolvers"]]:
        '''service_resolvers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#service_resolvers KmsEkmConnection#service_resolvers}
        '''
        result = self._values.get("service_resolvers")
        assert result is not None, "Required property 'service_resolvers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KmsEkmConnectionServiceResolvers"]], result)

    @builtins.property
    def crypto_space_path(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Identifies the EKM Crypto Space that this EkmConnection maps to. Note: This field is required if KeyManagementMode is CLOUD_KMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#crypto_space_path KmsEkmConnection#crypto_space_path}
        '''
        result = self._values.get("crypto_space_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def etag(self) -> typing.Optional[builtins.str]:
        '''Optional. Etag of the currently stored EkmConnection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#etag KmsEkmConnection#etag}
        '''
        result = self._values.get("etag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#id KmsEkmConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_management_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        Describes who can perform control plane operations on the EKM. If unset, this defaults to MANUAL Default value: "MANUAL" Possible values: ["MANUAL", "CLOUD_KMS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#key_management_mode KmsEkmConnection#key_management_mode}
        '''
        result = self._values.get("key_management_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#project KmsEkmConnection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KmsEkmConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#timeouts KmsEkmConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KmsEkmConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsEkmConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionServiceResolvers",
    jsii_struct_bases=[],
    name_mapping={
        "hostname": "hostname",
        "server_certificates": "serverCertificates",
        "service_directory_service": "serviceDirectoryService",
        "endpoint_filter": "endpointFilter",
    },
)
class KmsEkmConnectionServiceResolvers:
    def __init__(
        self,
        *,
        hostname: builtins.str,
        server_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KmsEkmConnectionServiceResolversServerCertificates", typing.Dict[builtins.str, typing.Any]]]],
        service_directory_service: builtins.str,
        endpoint_filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hostname: Required. The hostname of the EKM replica used at TLS and HTTP layers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#hostname KmsEkmConnection#hostname}
        :param server_certificates: server_certificates block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#server_certificates KmsEkmConnection#server_certificates}
        :param service_directory_service: Required. The resource name of the Service Directory service pointing to an EKM replica, in the format projects/* /locations/* /namespaces/* /services/* Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#service_directory_service KmsEkmConnection#service_directory_service} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param endpoint_filter: Optional. The filter applied to the endpoints of the resolved service. If no filter is specified, all endpoints will be considered. An endpoint will be chosen arbitrarily from the filtered list for each request. For endpoint filter syntax and examples, see https://cloud.google.com/service-directory/docs/reference/rpc/google.cloud.servicedirectory.v1#resolveservicerequest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#endpoint_filter KmsEkmConnection#endpoint_filter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0c72469e561773db1cab537638931e03c4e7c81258f7e25a0bcdf31a736549)
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument server_certificates", value=server_certificates, expected_type=type_hints["server_certificates"])
            check_type(argname="argument service_directory_service", value=service_directory_service, expected_type=type_hints["service_directory_service"])
            check_type(argname="argument endpoint_filter", value=endpoint_filter, expected_type=type_hints["endpoint_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
            "server_certificates": server_certificates,
            "service_directory_service": service_directory_service,
        }
        if endpoint_filter is not None:
            self._values["endpoint_filter"] = endpoint_filter

    @builtins.property
    def hostname(self) -> builtins.str:
        '''Required. The hostname of the EKM replica used at TLS and HTTP layers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#hostname KmsEkmConnection#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_certificates(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KmsEkmConnectionServiceResolversServerCertificates"]]:
        '''server_certificates block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#server_certificates KmsEkmConnection#server_certificates}
        '''
        result = self._values.get("server_certificates")
        assert result is not None, "Required property 'server_certificates' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KmsEkmConnectionServiceResolversServerCertificates"]], result)

    @builtins.property
    def service_directory_service(self) -> builtins.str:
        '''Required.

        The resource name of the Service Directory service pointing to an EKM replica, in the format projects/* /locations/* /namespaces/* /services/*

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#service_directory_service KmsEkmConnection#service_directory_service}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("service_directory_service")
        assert result is not None, "Required property 'service_directory_service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_filter(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The filter applied to the endpoints of the resolved service. If no filter is specified, all endpoints will be considered. An endpoint will be chosen arbitrarily from the filtered list for each request. For endpoint filter syntax and examples, see https://cloud.google.com/service-directory/docs/reference/rpc/google.cloud.servicedirectory.v1#resolveservicerequest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#endpoint_filter KmsEkmConnection#endpoint_filter}
        '''
        result = self._values.get("endpoint_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsEkmConnectionServiceResolvers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsEkmConnectionServiceResolversList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionServiceResolversList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31db8008d60448656552980ee9666eade9bae9e9cb68e2473f3ea5a674926a42)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KmsEkmConnectionServiceResolversOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba7de142f699facf54d72d6a69ac86e0769ccf236b6edebd7bb1dcaaed64acc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KmsEkmConnectionServiceResolversOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ceea09d90a926dbed924b7a03e23f5b537bf949eccac234963c80173d201c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63582dce9334c05b645ede0ec6aa0386dd8fd2b34dad3985ef9b3ec1f853b80d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86d0fcf4079e1272191bb5be03adff1b98806b23f7c04abec7f357b7e11e73af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KmsEkmConnectionServiceResolvers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KmsEkmConnectionServiceResolvers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KmsEkmConnectionServiceResolvers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c2c43b60a8f4dd4cf1a498dff69ecab05374933ba8f8f96913fce8d0bd7cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KmsEkmConnectionServiceResolversOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionServiceResolversOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d384daba86a2d474cfd5c5ef736c56101f7b0ef7b637f8ed3da3f19d7d528f12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putServerCertificates")
    def put_server_certificates(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KmsEkmConnectionServiceResolversServerCertificates", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffae549a9b5bd25fb93ecdd89a8f1ab17080edb9ee6bad54ca281ed285cd3b24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServerCertificates", [value]))

    @jsii.member(jsii_name="resetEndpointFilter")
    def reset_endpoint_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointFilter", []))

    @builtins.property
    @jsii.member(jsii_name="serverCertificates")
    def server_certificates(
        self,
    ) -> "KmsEkmConnectionServiceResolversServerCertificatesList":
        return typing.cast("KmsEkmConnectionServiceResolversServerCertificatesList", jsii.get(self, "serverCertificates"))

    @builtins.property
    @jsii.member(jsii_name="endpointFilterInput")
    def endpoint_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="serverCertificatesInput")
    def server_certificates_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KmsEkmConnectionServiceResolversServerCertificates"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KmsEkmConnectionServiceResolversServerCertificates"]]], jsii.get(self, "serverCertificatesInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryServiceInput")
    def service_directory_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceDirectoryServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointFilter")
    def endpoint_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointFilter"))

    @endpoint_filter.setter
    def endpoint_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c71aee2465f53b4e9383d1a13c03f58397955efad6cb9664647968a7ba1f23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae669a55479e5ab4457a787e7efea29747f20cd6178d1eea0f1cf56ac42c150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceDirectoryService")
    def service_directory_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceDirectoryService"))

    @service_directory_service.setter
    def service_directory_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54412bf8979883de5921b24b007f154e8506ba80a43eaba0c2eb9fa0dce92221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceDirectoryService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionServiceResolvers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionServiceResolvers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionServiceResolvers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760a9af39ee5f3fc056ab2ae1043de692238947391254d3767c998b28e96bdf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionServiceResolversServerCertificates",
    jsii_struct_bases=[],
    name_mapping={
        "raw_der": "rawDer",
        "subject_alternative_dns_names": "subjectAlternativeDnsNames",
    },
)
class KmsEkmConnectionServiceResolversServerCertificates:
    def __init__(
        self,
        *,
        raw_der: builtins.str,
        subject_alternative_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param raw_der: Required. The raw certificate bytes in DER format. A base64-encoded string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#raw_der KmsEkmConnection#raw_der}
        :param subject_alternative_dns_names: Output only. The subject Alternative DNS names. Only present if parsed is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#subject_alternative_dns_names KmsEkmConnection#subject_alternative_dns_names}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900b02b6367b006ca74fcc13d287962955fe3520802bf4c358a18708ff82c3fc)
            check_type(argname="argument raw_der", value=raw_der, expected_type=type_hints["raw_der"])
            check_type(argname="argument subject_alternative_dns_names", value=subject_alternative_dns_names, expected_type=type_hints["subject_alternative_dns_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "raw_der": raw_der,
        }
        if subject_alternative_dns_names is not None:
            self._values["subject_alternative_dns_names"] = subject_alternative_dns_names

    @builtins.property
    def raw_der(self) -> builtins.str:
        '''Required. The raw certificate bytes in DER format. A base64-encoded string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#raw_der KmsEkmConnection#raw_der}
        '''
        result = self._values.get("raw_der")
        assert result is not None, "Required property 'raw_der' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject_alternative_dns_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Output only. The subject Alternative DNS names. Only present if parsed is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#subject_alternative_dns_names KmsEkmConnection#subject_alternative_dns_names}
        '''
        result = self._values.get("subject_alternative_dns_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsEkmConnectionServiceResolversServerCertificates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsEkmConnectionServiceResolversServerCertificatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionServiceResolversServerCertificatesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30422d6032cae561ae595519a2b92725f67630db97840a264bea270c8b9d0c88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KmsEkmConnectionServiceResolversServerCertificatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286f0ba4da131df567f6f5b2b10dbd798573ae71574c8e525487c8e2e7d70f34)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KmsEkmConnectionServiceResolversServerCertificatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b328c44a4d452c3513b815e28fe3f7f70b396cf1c464394f50b6d0c2152a709e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9269b0607e8d8b49ffa73d1614f4fbe488ba89026346f23c02b36273b1f5af3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__faa6b8f7e7d670af6600212bc7f8c627b5ac828d0ffcdf6969cb9e4fe39b3016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KmsEkmConnectionServiceResolversServerCertificates]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KmsEkmConnectionServiceResolversServerCertificates]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KmsEkmConnectionServiceResolversServerCertificates]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f97e2b0cf5371a7afbf8dd4a421b639bbc84238d2b566e240e5c5842e7352273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KmsEkmConnectionServiceResolversServerCertificatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionServiceResolversServerCertificatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29bcfac7b5571e4448050d93b970157497f0c029f38ee917d86044c75c25baaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubjectAlternativeDnsNames")
    def reset_subject_alternative_dns_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubjectAlternativeDnsNames", []))

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @builtins.property
    @jsii.member(jsii_name="notAfterTime")
    def not_after_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notAfterTime"))

    @builtins.property
    @jsii.member(jsii_name="notBeforeTime")
    def not_before_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notBeforeTime"))

    @builtins.property
    @jsii.member(jsii_name="parsed")
    def parsed(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "parsed"))

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serialNumber"))

    @builtins.property
    @jsii.member(jsii_name="sha256Fingerprint")
    def sha256_fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Fingerprint"))

    @builtins.property
    @jsii.member(jsii_name="subject")
    def subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subject"))

    @builtins.property
    @jsii.member(jsii_name="rawDerInput")
    def raw_der_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rawDerInput"))

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeDnsNamesInput")
    def subject_alternative_dns_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subjectAlternativeDnsNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="rawDer")
    def raw_der(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rawDer"))

    @raw_der.setter
    def raw_der(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eecbe0b7e0c6757d9563d5693a497b59147990352c46167e5f54d6b17843432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rawDer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subjectAlternativeDnsNames")
    def subject_alternative_dns_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subjectAlternativeDnsNames"))

    @subject_alternative_dns_names.setter
    def subject_alternative_dns_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c853e1d35df61cddaab938b6a5dc3d72bd79f74683ff300b03997e505f762ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subjectAlternativeDnsNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionServiceResolversServerCertificates]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionServiceResolversServerCertificates]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionServiceResolversServerCertificates]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c048895a6380d2661b73743e665ba3d050cf6165dee08e5cad35bdb67a827f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KmsEkmConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#create KmsEkmConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#delete KmsEkmConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#update KmsEkmConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfa73516f5112b4a0bcf3f06dcd3973b34f4584b623c1c58308bf93a5f64af1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#create KmsEkmConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#delete KmsEkmConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/kms_ekm_connection#update KmsEkmConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KmsEkmConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KmsEkmConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.kmsEkmConnection.KmsEkmConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a1f51a3309a832994c34e9c81b8112c9260c51fa87b267132dd2a3a1843eca5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6cd9c9a76807913f9c32e1e03551564c90ca5457a6d9a6a5dd22a4544f952b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe79099af20a58286bef91543f1d1ff462a82f62a386ca35c6ca127c47e635f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc591c8acc0eebceb4bad183ece9ee35a3c0991fadb92415f9bd42f9fd204f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae0e540ce2d5ec3dfdba85444c27c5885f9b8e7331551f3207ac5d568e25499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KmsEkmConnection",
    "KmsEkmConnectionConfig",
    "KmsEkmConnectionServiceResolvers",
    "KmsEkmConnectionServiceResolversList",
    "KmsEkmConnectionServiceResolversOutputReference",
    "KmsEkmConnectionServiceResolversServerCertificates",
    "KmsEkmConnectionServiceResolversServerCertificatesList",
    "KmsEkmConnectionServiceResolversServerCertificatesOutputReference",
    "KmsEkmConnectionTimeouts",
    "KmsEkmConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dae12cf2a9064e8a31c8b30ee56e1093f1bcab330df06762bb7efa9398aba781(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    service_resolvers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KmsEkmConnectionServiceResolvers, typing.Dict[builtins.str, typing.Any]]]],
    crypto_space_path: typing.Optional[builtins.str] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    key_management_mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KmsEkmConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__abaf2b675c02aac93331eec133c7952df3dd131ec94288bf7b8c6456fbcea78b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db00369ddb82dce878640312a79c321e93a787e53f0b962bc3eeb6ba0b82f84(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KmsEkmConnectionServiceResolvers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5ed46e1eb16c9831e39fbaf6e01e1521756b159c26f00057926a81af9cf41f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185bd22a62cc5471d4f08ae083ef20a45524e3438cb5e17c83e8f90429dc454f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8963959610a5697f17618c1d7d307a8ee93d9c6ce0dabedf3c229b5c4ef550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef4fbf6bb61b922ca8e3aa897fe1a5d2932908fb0d3c35da648b0b325c59a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8099f8a7e1831bebb62789213b7ded2c7c256e47f84cf7672f86721d2db6c9d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8b2f72888e73d1cd8460c3a1a6c604f2e0f3874f9046367edde5ef46e4c780(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3c6801b4a304b83068a8ca571a3a937726b232d1f6a93f83fbcae6cca838ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2638bdf80fd303f6133fceb41479b04faf51d475585b65c8d6a62216256684(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    service_resolvers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KmsEkmConnectionServiceResolvers, typing.Dict[builtins.str, typing.Any]]]],
    crypto_space_path: typing.Optional[builtins.str] = None,
    etag: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    key_management_mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[KmsEkmConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0c72469e561773db1cab537638931e03c4e7c81258f7e25a0bcdf31a736549(
    *,
    hostname: builtins.str,
    server_certificates: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KmsEkmConnectionServiceResolversServerCertificates, typing.Dict[builtins.str, typing.Any]]]],
    service_directory_service: builtins.str,
    endpoint_filter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31db8008d60448656552980ee9666eade9bae9e9cb68e2473f3ea5a674926a42(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba7de142f699facf54d72d6a69ac86e0769ccf236b6edebd7bb1dcaaed64acc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ceea09d90a926dbed924b7a03e23f5b537bf949eccac234963c80173d201c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63582dce9334c05b645ede0ec6aa0386dd8fd2b34dad3985ef9b3ec1f853b80d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d0fcf4079e1272191bb5be03adff1b98806b23f7c04abec7f357b7e11e73af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c2c43b60a8f4dd4cf1a498dff69ecab05374933ba8f8f96913fce8d0bd7cf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KmsEkmConnectionServiceResolvers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d384daba86a2d474cfd5c5ef736c56101f7b0ef7b637f8ed3da3f19d7d528f12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffae549a9b5bd25fb93ecdd89a8f1ab17080edb9ee6bad54ca281ed285cd3b24(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KmsEkmConnectionServiceResolversServerCertificates, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c71aee2465f53b4e9383d1a13c03f58397955efad6cb9664647968a7ba1f23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae669a55479e5ab4457a787e7efea29747f20cd6178d1eea0f1cf56ac42c150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54412bf8979883de5921b24b007f154e8506ba80a43eaba0c2eb9fa0dce92221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760a9af39ee5f3fc056ab2ae1043de692238947391254d3767c998b28e96bdf2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionServiceResolvers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900b02b6367b006ca74fcc13d287962955fe3520802bf4c358a18708ff82c3fc(
    *,
    raw_der: builtins.str,
    subject_alternative_dns_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30422d6032cae561ae595519a2b92725f67630db97840a264bea270c8b9d0c88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286f0ba4da131df567f6f5b2b10dbd798573ae71574c8e525487c8e2e7d70f34(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b328c44a4d452c3513b815e28fe3f7f70b396cf1c464394f50b6d0c2152a709e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9269b0607e8d8b49ffa73d1614f4fbe488ba89026346f23c02b36273b1f5af3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa6b8f7e7d670af6600212bc7f8c627b5ac828d0ffcdf6969cb9e4fe39b3016(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97e2b0cf5371a7afbf8dd4a421b639bbc84238d2b566e240e5c5842e7352273(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KmsEkmConnectionServiceResolversServerCertificates]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29bcfac7b5571e4448050d93b970157497f0c029f38ee917d86044c75c25baaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eecbe0b7e0c6757d9563d5693a497b59147990352c46167e5f54d6b17843432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c853e1d35df61cddaab938b6a5dc3d72bd79f74683ff300b03997e505f762ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c048895a6380d2661b73743e665ba3d050cf6165dee08e5cad35bdb67a827f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionServiceResolversServerCertificates]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfa73516f5112b4a0bcf3f06dcd3973b34f4584b623c1c58308bf93a5f64af1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1f51a3309a832994c34e9c81b8112c9260c51fa87b267132dd2a3a1843eca5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6cd9c9a76807913f9c32e1e03551564c90ca5457a6d9a6a5dd22a4544f952b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe79099af20a58286bef91543f1d1ff462a82f62a386ca35c6ca127c47e635f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc591c8acc0eebceb4bad183ece9ee35a3c0991fadb92415f9bd42f9fd204f8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae0e540ce2d5ec3dfdba85444c27c5885f9b8e7331551f3207ac5d568e25499(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KmsEkmConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
