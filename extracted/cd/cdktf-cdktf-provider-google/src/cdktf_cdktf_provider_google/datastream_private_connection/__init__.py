r'''
# `google_datastream_private_connection`

Refer to the Terraform Registry for docs: [`google_datastream_private_connection`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection).
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


class DatastreamPrivateConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection google_datastream_private_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        private_connection_id: builtins.str,
        create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_interface_config: typing.Optional[typing.Union["DatastreamPrivateConnectionPscInterfaceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DatastreamPrivateConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_peering_config: typing.Optional[typing.Union["DatastreamPrivateConnectionVpcPeeringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection google_datastream_private_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#display_name DatastreamPrivateConnection#display_name}
        :param location: The name of the location this private connection is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#location DatastreamPrivateConnection#location}
        :param private_connection_id: The private connectivity identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#private_connection_id DatastreamPrivateConnection#private_connection_id}
        :param create_without_validation: If set to true, will skip validations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#create_without_validation DatastreamPrivateConnection#create_without_validation}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#id DatastreamPrivateConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#labels DatastreamPrivateConnection#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#project DatastreamPrivateConnection#project}.
        :param psc_interface_config: psc_interface_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#psc_interface_config DatastreamPrivateConnection#psc_interface_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#timeouts DatastreamPrivateConnection#timeouts}
        :param vpc_peering_config: vpc_peering_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#vpc_peering_config DatastreamPrivateConnection#vpc_peering_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791184888d611905098e1550b8a8e7bddc76987bc0dcfe0ba8289e6b98e52c8a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DatastreamPrivateConnectionConfig(
            display_name=display_name,
            location=location,
            private_connection_id=private_connection_id,
            create_without_validation=create_without_validation,
            id=id,
            labels=labels,
            project=project,
            psc_interface_config=psc_interface_config,
            timeouts=timeouts,
            vpc_peering_config=vpc_peering_config,
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
        '''Generates CDKTF code for importing a DatastreamPrivateConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DatastreamPrivateConnection to import.
        :param import_from_id: The id of the existing DatastreamPrivateConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DatastreamPrivateConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2513816c47072db14379e7d5f3749490bd9ab50a2fdd371b00561aa5b8cd58f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPscInterfaceConfig")
    def put_psc_interface_config(self, *, network_attachment: builtins.str) -> None:
        '''
        :param network_attachment: Fully qualified name of the network attachment that Datastream will connect to. Format: projects/{project}/regions/{region}/networkAttachments/{name}. To get Datastream project for the accepted list: 'gcloud datastream private-connections create [PC ID] --location=[LOCATION] --network-attachment=[NA URI] --validate-only --display-name=[ANY STRING]' Add Datastream project to the attachment accepted list: 'gcloud compute network-attachments update [NA URI] --region=[NA region] --producer-accept-list=[TP from prev command]' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#network_attachment DatastreamPrivateConnection#network_attachment}
        '''
        value = DatastreamPrivateConnectionPscInterfaceConfig(
            network_attachment=network_attachment
        )

        return typing.cast(None, jsii.invoke(self, "putPscInterfaceConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#create DatastreamPrivateConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#delete DatastreamPrivateConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#update DatastreamPrivateConnection#update}.
        '''
        value = DatastreamPrivateConnectionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVpcPeeringConfig")
    def put_vpc_peering_config(
        self,
        *,
        subnet: builtins.str,
        vpc: builtins.str,
    ) -> None:
        '''
        :param subnet: A free subnet for peering. (CIDR of /29). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#subnet DatastreamPrivateConnection#subnet}
        :param vpc: Fully qualified name of the VPC that Datastream will peer to. Format: projects/{project}/global/{networks}/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#vpc DatastreamPrivateConnection#vpc}
        '''
        value = DatastreamPrivateConnectionVpcPeeringConfig(subnet=subnet, vpc=vpc)

        return typing.cast(None, jsii.invoke(self, "putVpcPeeringConfig", [value]))

    @jsii.member(jsii_name="resetCreateWithoutValidation")
    def reset_create_without_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateWithoutValidation", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPscInterfaceConfig")
    def reset_psc_interface_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscInterfaceConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVpcPeeringConfig")
    def reset_vpc_peering_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcPeeringConfig", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(self) -> "DatastreamPrivateConnectionErrorList":
        return typing.cast("DatastreamPrivateConnectionErrorList", jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="pscInterfaceConfig")
    def psc_interface_config(
        self,
    ) -> "DatastreamPrivateConnectionPscInterfaceConfigOutputReference":
        return typing.cast("DatastreamPrivateConnectionPscInterfaceConfigOutputReference", jsii.get(self, "pscInterfaceConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DatastreamPrivateConnectionTimeoutsOutputReference":
        return typing.cast("DatastreamPrivateConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vpcPeeringConfig")
    def vpc_peering_config(
        self,
    ) -> "DatastreamPrivateConnectionVpcPeeringConfigOutputReference":
        return typing.cast("DatastreamPrivateConnectionVpcPeeringConfigOutputReference", jsii.get(self, "vpcPeeringConfig"))

    @builtins.property
    @jsii.member(jsii_name="createWithoutValidationInput")
    def create_without_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createWithoutValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="privateConnectionIdInput")
    def private_connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateConnectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pscInterfaceConfigInput")
    def psc_interface_config_input(
        self,
    ) -> typing.Optional["DatastreamPrivateConnectionPscInterfaceConfig"]:
        return typing.cast(typing.Optional["DatastreamPrivateConnectionPscInterfaceConfig"], jsii.get(self, "pscInterfaceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatastreamPrivateConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatastreamPrivateConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcPeeringConfigInput")
    def vpc_peering_config_input(
        self,
    ) -> typing.Optional["DatastreamPrivateConnectionVpcPeeringConfig"]:
        return typing.cast(typing.Optional["DatastreamPrivateConnectionVpcPeeringConfig"], jsii.get(self, "vpcPeeringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="createWithoutValidation")
    def create_without_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createWithoutValidation"))

    @create_without_validation.setter
    def create_without_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e408e51a47d91e36970c8400e3fb18b44b7d99e27505b5e58e6c8f374d5a97d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createWithoutValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57bd9ab4de2eaf8cde8b429763282835198e83cdef27cdc6c4e69df623aa6b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9318febe81c550b540393d1a2ae3105b1ce3d5d3636139c9c023cc980036eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e78ea3352ef4e5216848abf6c244fa8eec2969b76e72ce8ad51d82c844422b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524d6d19073f8b72ecabb7d336f17b812e9b6b4aec83ffd78f02abff32c14be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateConnectionId")
    def private_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateConnectionId"))

    @private_connection_id.setter
    def private_connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e55ac9b08a1cb432b89e9412440104448522067abf50edfc75d3382919a040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateConnectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99855daf73e2e865ae2612bddf8378f1a92ff3152b542a6f2c9da5037d3daa09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "location": "location",
        "private_connection_id": "privateConnectionId",
        "create_without_validation": "createWithoutValidation",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "psc_interface_config": "pscInterfaceConfig",
        "timeouts": "timeouts",
        "vpc_peering_config": "vpcPeeringConfig",
    },
)
class DatastreamPrivateConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        location: builtins.str,
        private_connection_id: builtins.str,
        create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_interface_config: typing.Optional[typing.Union["DatastreamPrivateConnectionPscInterfaceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DatastreamPrivateConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_peering_config: typing.Optional[typing.Union["DatastreamPrivateConnectionVpcPeeringConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#display_name DatastreamPrivateConnection#display_name}
        :param location: The name of the location this private connection is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#location DatastreamPrivateConnection#location}
        :param private_connection_id: The private connectivity identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#private_connection_id DatastreamPrivateConnection#private_connection_id}
        :param create_without_validation: If set to true, will skip validations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#create_without_validation DatastreamPrivateConnection#create_without_validation}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#id DatastreamPrivateConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#labels DatastreamPrivateConnection#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#project DatastreamPrivateConnection#project}.
        :param psc_interface_config: psc_interface_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#psc_interface_config DatastreamPrivateConnection#psc_interface_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#timeouts DatastreamPrivateConnection#timeouts}
        :param vpc_peering_config: vpc_peering_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#vpc_peering_config DatastreamPrivateConnection#vpc_peering_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(psc_interface_config, dict):
            psc_interface_config = DatastreamPrivateConnectionPscInterfaceConfig(**psc_interface_config)
        if isinstance(timeouts, dict):
            timeouts = DatastreamPrivateConnectionTimeouts(**timeouts)
        if isinstance(vpc_peering_config, dict):
            vpc_peering_config = DatastreamPrivateConnectionVpcPeeringConfig(**vpc_peering_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8c3585071bb13ae0fb73ba035cc464db906607d2bf6c95e8990a9ef448bd9c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument private_connection_id", value=private_connection_id, expected_type=type_hints["private_connection_id"])
            check_type(argname="argument create_without_validation", value=create_without_validation, expected_type=type_hints["create_without_validation"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument psc_interface_config", value=psc_interface_config, expected_type=type_hints["psc_interface_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vpc_peering_config", value=vpc_peering_config, expected_type=type_hints["vpc_peering_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "location": location,
            "private_connection_id": private_connection_id,
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
        if create_without_validation is not None:
            self._values["create_without_validation"] = create_without_validation
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if psc_interface_config is not None:
            self._values["psc_interface_config"] = psc_interface_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vpc_peering_config is not None:
            self._values["vpc_peering_config"] = vpc_peering_config

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
    def display_name(self) -> builtins.str:
        '''Display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#display_name DatastreamPrivateConnection#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this private connection is located in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#location DatastreamPrivateConnection#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_connection_id(self) -> builtins.str:
        '''The private connectivity identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#private_connection_id DatastreamPrivateConnection#private_connection_id}
        '''
        result = self._values.get("private_connection_id")
        assert result is not None, "Required property 'private_connection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def create_without_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, will skip validations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#create_without_validation DatastreamPrivateConnection#create_without_validation}
        '''
        result = self._values.get("create_without_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#id DatastreamPrivateConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#labels DatastreamPrivateConnection#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#project DatastreamPrivateConnection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_interface_config(
        self,
    ) -> typing.Optional["DatastreamPrivateConnectionPscInterfaceConfig"]:
        '''psc_interface_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#psc_interface_config DatastreamPrivateConnection#psc_interface_config}
        '''
        result = self._values.get("psc_interface_config")
        return typing.cast(typing.Optional["DatastreamPrivateConnectionPscInterfaceConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DatastreamPrivateConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#timeouts DatastreamPrivateConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DatastreamPrivateConnectionTimeouts"], result)

    @builtins.property
    def vpc_peering_config(
        self,
    ) -> typing.Optional["DatastreamPrivateConnectionVpcPeeringConfig"]:
        '''vpc_peering_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#vpc_peering_config DatastreamPrivateConnection#vpc_peering_config}
        '''
        result = self._values.get("vpc_peering_config")
        return typing.cast(typing.Optional["DatastreamPrivateConnectionVpcPeeringConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamPrivateConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionError",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatastreamPrivateConnectionError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamPrivateConnectionError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamPrivateConnectionErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f2345e81816417405082dd7f2e84eecffddc9f59eeb2251bcbaf062a5a50af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamPrivateConnectionErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f24b989c7487fe94181547620cb898f84317485250ee7c15554baa09cf86ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamPrivateConnectionErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb2bd4fcc1a7c7098f151c0fea63bd7bccf789aa9efadc3e2f5d71f540025f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19bf9f74297c68537b42ea4573b6b0c136a4191ee793c44abf1c8974aaec8a66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69cd35451c7a484ff96c23fefe143d7aa5426cfd4b997ee5e849ac8e4440aa24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DatastreamPrivateConnectionErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77028d290872a06282e3d6d80fb9663e661d66117e488fba63d6ba949e84beaa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatastreamPrivateConnectionError]:
        return typing.cast(typing.Optional[DatastreamPrivateConnectionError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamPrivateConnectionError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0629d3b332383f394c0d985e5ed6a4b0d76c86c0202f32080361bbeedd8f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionPscInterfaceConfig",
    jsii_struct_bases=[],
    name_mapping={"network_attachment": "networkAttachment"},
)
class DatastreamPrivateConnectionPscInterfaceConfig:
    def __init__(self, *, network_attachment: builtins.str) -> None:
        '''
        :param network_attachment: Fully qualified name of the network attachment that Datastream will connect to. Format: projects/{project}/regions/{region}/networkAttachments/{name}. To get Datastream project for the accepted list: 'gcloud datastream private-connections create [PC ID] --location=[LOCATION] --network-attachment=[NA URI] --validate-only --display-name=[ANY STRING]' Add Datastream project to the attachment accepted list: 'gcloud compute network-attachments update [NA URI] --region=[NA region] --producer-accept-list=[TP from prev command]' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#network_attachment DatastreamPrivateConnection#network_attachment}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01c30b1af3a147e5e2ef2d3eade858af25aeeefdfc85d428764ce5e0cfc58f1)
            check_type(argname="argument network_attachment", value=network_attachment, expected_type=type_hints["network_attachment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_attachment": network_attachment,
        }

    @builtins.property
    def network_attachment(self) -> builtins.str:
        '''Fully qualified name of the network attachment that Datastream will connect to. Format: projects/{project}/regions/{region}/networkAttachments/{name}.

        To get Datastream project for the accepted list:
        'gcloud datastream private-connections create [PC ID] --location=[LOCATION] --network-attachment=[NA URI] --validate-only --display-name=[ANY STRING]'
        Add Datastream project to the attachment accepted list:
        'gcloud compute network-attachments update [NA URI] --region=[NA region] --producer-accept-list=[TP from prev command]'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#network_attachment DatastreamPrivateConnection#network_attachment}
        '''
        result = self._values.get("network_attachment")
        assert result is not None, "Required property 'network_attachment' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamPrivateConnectionPscInterfaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamPrivateConnectionPscInterfaceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionPscInterfaceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01fcae75110f8d6946d38ed91321cd7f8984e20f48377dae25d4f4835142a09b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="networkAttachmentInput")
    def network_attachment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkAttachmentInput"))

    @builtins.property
    @jsii.member(jsii_name="networkAttachment")
    def network_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkAttachment"))

    @network_attachment.setter
    def network_attachment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb641d734af2182e91d52ee8240a47a04a05aa9b1a87d904eaae151334aeb961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkAttachment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamPrivateConnectionPscInterfaceConfig]:
        return typing.cast(typing.Optional[DatastreamPrivateConnectionPscInterfaceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamPrivateConnectionPscInterfaceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42cdadf82d8741b0fdd8ba24e63d6414a081f4abf3839263d8f4faaafd97f4e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DatastreamPrivateConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#create DatastreamPrivateConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#delete DatastreamPrivateConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#update DatastreamPrivateConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34f0eac934d22eda8ada46299147a5fa9540ecf7a1a7f0727f2696477c6d136)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#create DatastreamPrivateConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#delete DatastreamPrivateConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#update DatastreamPrivateConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamPrivateConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamPrivateConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34ca5c8454d8349341373e054be33c3766ab98048e3915193fbd6095cdb114ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4878c8c7f7bb8fc90927b59c883570f8bed219f41b033e73c66a55c3e9319e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55a2bd8e8cc34547c2b6c7cac4e3ea76555cfed2a81c6483032a51d24c5b3b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2387d4d893a4166984baf4fb73ec9baf95be9781fb2a4917d3acc420bc51b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamPrivateConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamPrivateConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamPrivateConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adde50014a213b0156c0a2544951d3d4f0c1da3c5166411bcdc22823b507ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionVpcPeeringConfig",
    jsii_struct_bases=[],
    name_mapping={"subnet": "subnet", "vpc": "vpc"},
)
class DatastreamPrivateConnectionVpcPeeringConfig:
    def __init__(self, *, subnet: builtins.str, vpc: builtins.str) -> None:
        '''
        :param subnet: A free subnet for peering. (CIDR of /29). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#subnet DatastreamPrivateConnection#subnet}
        :param vpc: Fully qualified name of the VPC that Datastream will peer to. Format: projects/{project}/global/{networks}/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#vpc DatastreamPrivateConnection#vpc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80a967ebe261a07cb9d7742d4c0b4d97c4db5545fff3423fdd0f682e8642a6a2)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet": subnet,
            "vpc": vpc,
        }

    @builtins.property
    def subnet(self) -> builtins.str:
        '''A free subnet for peering. (CIDR of /29).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#subnet DatastreamPrivateConnection#subnet}
        '''
        result = self._values.get("subnet")
        assert result is not None, "Required property 'subnet' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> builtins.str:
        '''Fully qualified name of the VPC that Datastream will peer to. Format: projects/{project}/global/{networks}/{name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/datastream_private_connection#vpc DatastreamPrivateConnection#vpc}
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamPrivateConnectionVpcPeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamPrivateConnectionVpcPeeringConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamPrivateConnection.DatastreamPrivateConnectionVpcPeeringConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae6c02b8cbe5df828dff5fcd5a8cf4a524622c09a376fa8820bf92c335f45167)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="subnetInput")
    def subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="subnet")
    def subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnet"))

    @subnet.setter
    def subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6c5c89af251299006a7188bcea1322a6fd44515190472f62ef73c2a4658f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90618fb80aad66bafcebca19a6ecba81d9e4ddf7add55e3a6a2f562bbcb96e2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamPrivateConnectionVpcPeeringConfig]:
        return typing.cast(typing.Optional[DatastreamPrivateConnectionVpcPeeringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamPrivateConnectionVpcPeeringConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeea821fe4ffa81623ff5fecd76de0e1d73c01e56c0bc6aa9329e41926d416a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DatastreamPrivateConnection",
    "DatastreamPrivateConnectionConfig",
    "DatastreamPrivateConnectionError",
    "DatastreamPrivateConnectionErrorList",
    "DatastreamPrivateConnectionErrorOutputReference",
    "DatastreamPrivateConnectionPscInterfaceConfig",
    "DatastreamPrivateConnectionPscInterfaceConfigOutputReference",
    "DatastreamPrivateConnectionTimeouts",
    "DatastreamPrivateConnectionTimeoutsOutputReference",
    "DatastreamPrivateConnectionVpcPeeringConfig",
    "DatastreamPrivateConnectionVpcPeeringConfigOutputReference",
]

publication.publish()

def _typecheckingstub__791184888d611905098e1550b8a8e7bddc76987bc0dcfe0ba8289e6b98e52c8a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    private_connection_id: builtins.str,
    create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_interface_config: typing.Optional[typing.Union[DatastreamPrivateConnectionPscInterfaceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DatastreamPrivateConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_peering_config: typing.Optional[typing.Union[DatastreamPrivateConnectionVpcPeeringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2513816c47072db14379e7d5f3749490bd9ab50a2fdd371b00561aa5b8cd58f0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e408e51a47d91e36970c8400e3fb18b44b7d99e27505b5e58e6c8f374d5a97d9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57bd9ab4de2eaf8cde8b429763282835198e83cdef27cdc6c4e69df623aa6b8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9318febe81c550b540393d1a2ae3105b1ce3d5d3636139c9c023cc980036eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e78ea3352ef4e5216848abf6c244fa8eec2969b76e72ce8ad51d82c844422b80(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524d6d19073f8b72ecabb7d336f17b812e9b6b4aec83ffd78f02abff32c14be7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e55ac9b08a1cb432b89e9412440104448522067abf50edfc75d3382919a040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99855daf73e2e865ae2612bddf8378f1a92ff3152b542a6f2c9da5037d3daa09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8c3585071bb13ae0fb73ba035cc464db906607d2bf6c95e8990a9ef448bd9c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    location: builtins.str,
    private_connection_id: builtins.str,
    create_without_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_interface_config: typing.Optional[typing.Union[DatastreamPrivateConnectionPscInterfaceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DatastreamPrivateConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_peering_config: typing.Optional[typing.Union[DatastreamPrivateConnectionVpcPeeringConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f2345e81816417405082dd7f2e84eecffddc9f59eeb2251bcbaf062a5a50af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f24b989c7487fe94181547620cb898f84317485250ee7c15554baa09cf86ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb2bd4fcc1a7c7098f151c0fea63bd7bccf789aa9efadc3e2f5d71f540025f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bf9f74297c68537b42ea4573b6b0c136a4191ee793c44abf1c8974aaec8a66(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cd35451c7a484ff96c23fefe143d7aa5426cfd4b997ee5e849ac8e4440aa24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77028d290872a06282e3d6d80fb9663e661d66117e488fba63d6ba949e84beaa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0629d3b332383f394c0d985e5ed6a4b0d76c86c0202f32080361bbeedd8f82(
    value: typing.Optional[DatastreamPrivateConnectionError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01c30b1af3a147e5e2ef2d3eade858af25aeeefdfc85d428764ce5e0cfc58f1(
    *,
    network_attachment: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01fcae75110f8d6946d38ed91321cd7f8984e20f48377dae25d4f4835142a09b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb641d734af2182e91d52ee8240a47a04a05aa9b1a87d904eaae151334aeb961(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cdadf82d8741b0fdd8ba24e63d6414a081f4abf3839263d8f4faaafd97f4e7(
    value: typing.Optional[DatastreamPrivateConnectionPscInterfaceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34f0eac934d22eda8ada46299147a5fa9540ecf7a1a7f0727f2696477c6d136(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ca5c8454d8349341373e054be33c3766ab98048e3915193fbd6095cdb114ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4878c8c7f7bb8fc90927b59c883570f8bed219f41b033e73c66a55c3e9319e36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55a2bd8e8cc34547c2b6c7cac4e3ea76555cfed2a81c6483032a51d24c5b3b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2387d4d893a4166984baf4fb73ec9baf95be9781fb2a4917d3acc420bc51b01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adde50014a213b0156c0a2544951d3d4f0c1da3c5166411bcdc22823b507ff0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamPrivateConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a967ebe261a07cb9d7742d4c0b4d97c4db5545fff3423fdd0f682e8642a6a2(
    *,
    subnet: builtins.str,
    vpc: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6c02b8cbe5df828dff5fcd5a8cf4a524622c09a376fa8820bf92c335f45167(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6c5c89af251299006a7188bcea1322a6fd44515190472f62ef73c2a4658f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90618fb80aad66bafcebca19a6ecba81d9e4ddf7add55e3a6a2f562bbcb96e2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeea821fe4ffa81623ff5fecd76de0e1d73c01e56c0bc6aa9329e41926d416a5(
    value: typing.Optional[DatastreamPrivateConnectionVpcPeeringConfig],
) -> None:
    """Type checking stubs"""
    pass
