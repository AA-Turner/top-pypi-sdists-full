r'''
# `google_beyondcorp_app_connection`

Refer to the Terraform Registry for docs: [`google_beyondcorp_app_connection`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection).
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


class BeyondcorpAppConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpAppConnection.BeyondcorpAppConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection google_beyondcorp_app_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        application_endpoint: typing.Union["BeyondcorpAppConnectionApplicationEndpoint", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        connectors: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gateway: typing.Optional[typing.Union["BeyondcorpAppConnectionGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BeyondcorpAppConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection google_beyondcorp_app_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param application_endpoint: application_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#application_endpoint BeyondcorpAppConnection#application_endpoint}
        :param name: ID of the AppConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#name BeyondcorpAppConnection#name}
        :param connectors: List of AppConnectors that are authorised to be associated with this AppConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#connectors BeyondcorpAppConnection#connectors}
        :param display_name: An arbitrary user-provided name for the AppConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#display_name BeyondcorpAppConnection#display_name}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#gateway BeyondcorpAppConnection#gateway}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#id BeyondcorpAppConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#labels BeyondcorpAppConnection#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#project BeyondcorpAppConnection#project}.
        :param region: The region of the AppConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#region BeyondcorpAppConnection#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#timeouts BeyondcorpAppConnection#timeouts}
        :param type: The type of network connectivity used by the AppConnection. Refer to https://cloud.google.com/beyondcorp/docs/reference/rest/v1/projects.locations.appConnections#type for a list of possible values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#type BeyondcorpAppConnection#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443e10c08e37c77ac10ff5ee7026eb2fe5ea1c4fb6db91b4188a167c15c8789d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BeyondcorpAppConnectionConfig(
            application_endpoint=application_endpoint,
            name=name,
            connectors=connectors,
            display_name=display_name,
            gateway=gateway,
            id=id,
            labels=labels,
            project=project,
            region=region,
            timeouts=timeouts,
            type=type,
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
        '''Generates CDKTF code for importing a BeyondcorpAppConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BeyondcorpAppConnection to import.
        :param import_from_id: The id of the existing BeyondcorpAppConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BeyondcorpAppConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826d8006f5a4b060cbddb0dce0ba1fd345d0cdc46b1080d30511295553caa37f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApplicationEndpoint")
    def put_application_endpoint(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param host: Hostname or IP address of the remote application endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#host BeyondcorpAppConnection#host}
        :param port: Port of the remote application endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#port BeyondcorpAppConnection#port}
        '''
        value = BeyondcorpAppConnectionApplicationEndpoint(host=host, port=port)

        return typing.cast(None, jsii.invoke(self, "putApplicationEndpoint", [value]))

    @jsii.member(jsii_name="putGateway")
    def put_gateway(
        self,
        *,
        app_gateway: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_gateway: AppGateway name in following format: projects/{project_id}/locations/{locationId}/appgateways/{gateway_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#app_gateway BeyondcorpAppConnection#app_gateway}
        :param type: The type of hosting used by the gateway. Refer to https://cloud.google.com/beyondcorp/docs/reference/rest/v1/projects.locations.appConnections#Type_1 for a list of possible values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#type BeyondcorpAppConnection#type}
        '''
        value = BeyondcorpAppConnectionGateway(app_gateway=app_gateway, type=type)

        return typing.cast(None, jsii.invoke(self, "putGateway", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#create BeyondcorpAppConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#delete BeyondcorpAppConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#update BeyondcorpAppConnection#update}.
        '''
        value = BeyondcorpAppConnectionTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConnectors")
    def reset_connectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectors", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGateway")
    def reset_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGateway", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="applicationEndpoint")
    def application_endpoint(
        self,
    ) -> "BeyondcorpAppConnectionApplicationEndpointOutputReference":
        return typing.cast("BeyondcorpAppConnectionApplicationEndpointOutputReference", jsii.get(self, "applicationEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> "BeyondcorpAppConnectionGatewayOutputReference":
        return typing.cast("BeyondcorpAppConnectionGatewayOutputReference", jsii.get(self, "gateway"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BeyondcorpAppConnectionTimeoutsOutputReference":
        return typing.cast("BeyondcorpAppConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="applicationEndpointInput")
    def application_endpoint_input(
        self,
    ) -> typing.Optional["BeyondcorpAppConnectionApplicationEndpoint"]:
        return typing.cast(typing.Optional["BeyondcorpAppConnectionApplicationEndpoint"], jsii.get(self, "applicationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="connectorsInput")
    def connectors_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "connectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional["BeyondcorpAppConnectionGateway"]:
        return typing.cast(typing.Optional["BeyondcorpAppConnectionGateway"], jsii.get(self, "gatewayInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BeyondcorpAppConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BeyondcorpAppConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectors")
    def connectors(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "connectors"))

    @connectors.setter
    def connectors(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af98d29d7b78e10b30b391fce13835080cb0c74c8ecb42426e3e2ffcd2e23770)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1cadf21641839c60e85d4202146cdd21a9abb2cc9b30d42287cb006da653f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94fa37a860d2feb946419e3a969b29631688c938e7cf1a4eaec945b48373a5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a692a31dfadb2a7c06efa77ee505c43f450cc9ef025bc3c10564b79b6b7f5dcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dd9dafb7ee014962798789a84b17bca5f3ab296713f363bfaee8e5a2f9fe75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce5d5645d49c904203e7b8422eb6e4ab46905e2ec5f391f535a9744ea9c65b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe4c9f680fb30f91ee2247383f7e35be2fd5e2a3a6535cfe314cb456eaf20d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16632a564513377107b787821e214c290bf8f4aa65efd6e0e3d482449d7e5fb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpAppConnection.BeyondcorpAppConnectionApplicationEndpoint",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class BeyondcorpAppConnectionApplicationEndpoint:
    def __init__(self, *, host: builtins.str, port: jsii.Number) -> None:
        '''
        :param host: Hostname or IP address of the remote application endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#host BeyondcorpAppConnection#host}
        :param port: Port of the remote application endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#port BeyondcorpAppConnection#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd531c9e158c1058d2de5990741c72b6f69ef1ec388e9d010184e49b24c1f042)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "port": port,
        }

    @builtins.property
    def host(self) -> builtins.str:
        '''Hostname or IP address of the remote application endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#host BeyondcorpAppConnection#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Port of the remote application endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#port BeyondcorpAppConnection#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpAppConnectionApplicationEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BeyondcorpAppConnectionApplicationEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpAppConnection.BeyondcorpAppConnectionApplicationEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7dfc557e2c60778b52aa7a3d7a6fcdf8668cafbb709f9e1a42625e2275e9f6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8f012efbf2b7e1f821b994881725883b9feef9197113c539259982bea6fcb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d9d21f8612bc316180fd82c5adcb811ad7d2dda6e224d07ce1d2eab79601c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BeyondcorpAppConnectionApplicationEndpoint]:
        return typing.cast(typing.Optional[BeyondcorpAppConnectionApplicationEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BeyondcorpAppConnectionApplicationEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4786c0cc7df187b5e146f8c23a731836a35758f182c1e42ddbf55da478547af2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpAppConnection.BeyondcorpAppConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "application_endpoint": "applicationEndpoint",
        "name": "name",
        "connectors": "connectors",
        "display_name": "displayName",
        "gateway": "gateway",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
        "type": "type",
    },
)
class BeyondcorpAppConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        application_endpoint: typing.Union[BeyondcorpAppConnectionApplicationEndpoint, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        connectors: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gateway: typing.Optional[typing.Union["BeyondcorpAppConnectionGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BeyondcorpAppConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param application_endpoint: application_endpoint block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#application_endpoint BeyondcorpAppConnection#application_endpoint}
        :param name: ID of the AppConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#name BeyondcorpAppConnection#name}
        :param connectors: List of AppConnectors that are authorised to be associated with this AppConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#connectors BeyondcorpAppConnection#connectors}
        :param display_name: An arbitrary user-provided name for the AppConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#display_name BeyondcorpAppConnection#display_name}
        :param gateway: gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#gateway BeyondcorpAppConnection#gateway}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#id BeyondcorpAppConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#labels BeyondcorpAppConnection#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#project BeyondcorpAppConnection#project}.
        :param region: The region of the AppConnection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#region BeyondcorpAppConnection#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#timeouts BeyondcorpAppConnection#timeouts}
        :param type: The type of network connectivity used by the AppConnection. Refer to https://cloud.google.com/beyondcorp/docs/reference/rest/v1/projects.locations.appConnections#type for a list of possible values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#type BeyondcorpAppConnection#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(application_endpoint, dict):
            application_endpoint = BeyondcorpAppConnectionApplicationEndpoint(**application_endpoint)
        if isinstance(gateway, dict):
            gateway = BeyondcorpAppConnectionGateway(**gateway)
        if isinstance(timeouts, dict):
            timeouts = BeyondcorpAppConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd02d0d614e94cf2973de70e550abe25a79ddd8ed360da454391cc8624c7c5f3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument application_endpoint", value=application_endpoint, expected_type=type_hints["application_endpoint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument connectors", value=connectors, expected_type=type_hints["connectors"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_endpoint": application_endpoint,
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
        if connectors is not None:
            self._values["connectors"] = connectors
        if display_name is not None:
            self._values["display_name"] = display_name
        if gateway is not None:
            self._values["gateway"] = gateway
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type

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
    def application_endpoint(self) -> BeyondcorpAppConnectionApplicationEndpoint:
        '''application_endpoint block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#application_endpoint BeyondcorpAppConnection#application_endpoint}
        '''
        result = self._values.get("application_endpoint")
        assert result is not None, "Required property 'application_endpoint' is missing"
        return typing.cast(BeyondcorpAppConnectionApplicationEndpoint, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''ID of the AppConnection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#name BeyondcorpAppConnection#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connectors(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of AppConnectors that are authorised to be associated with this AppConnection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#connectors BeyondcorpAppConnection#connectors}
        '''
        result = self._values.get("connectors")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''An arbitrary user-provided name for the AppConnection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#display_name BeyondcorpAppConnection#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway(self) -> typing.Optional["BeyondcorpAppConnectionGateway"]:
        '''gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#gateway BeyondcorpAppConnection#gateway}
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional["BeyondcorpAppConnectionGateway"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#id BeyondcorpAppConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#labels BeyondcorpAppConnection#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#project BeyondcorpAppConnection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the AppConnection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#region BeyondcorpAppConnection#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BeyondcorpAppConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#timeouts BeyondcorpAppConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BeyondcorpAppConnectionTimeouts"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of network connectivity used by the AppConnection. Refer to https://cloud.google.com/beyondcorp/docs/reference/rest/v1/projects.locations.appConnections#type for a list of possible values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#type BeyondcorpAppConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpAppConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpAppConnection.BeyondcorpAppConnectionGateway",
    jsii_struct_bases=[],
    name_mapping={"app_gateway": "appGateway", "type": "type"},
)
class BeyondcorpAppConnectionGateway:
    def __init__(
        self,
        *,
        app_gateway: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_gateway: AppGateway name in following format: projects/{project_id}/locations/{locationId}/appgateways/{gateway_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#app_gateway BeyondcorpAppConnection#app_gateway}
        :param type: The type of hosting used by the gateway. Refer to https://cloud.google.com/beyondcorp/docs/reference/rest/v1/projects.locations.appConnections#Type_1 for a list of possible values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#type BeyondcorpAppConnection#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f2fe96d8cfecbb39d682b457d4b15b3878d4876f88390cbd268d6390f4b35f)
            check_type(argname="argument app_gateway", value=app_gateway, expected_type=type_hints["app_gateway"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_gateway": app_gateway,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def app_gateway(self) -> builtins.str:
        '''AppGateway name in following format: projects/{project_id}/locations/{locationId}/appgateways/{gateway_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#app_gateway BeyondcorpAppConnection#app_gateway}
        '''
        result = self._values.get("app_gateway")
        assert result is not None, "Required property 'app_gateway' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of hosting used by the gateway. Refer to https://cloud.google.com/beyondcorp/docs/reference/rest/v1/projects.locations.appConnections#Type_1 for a list of possible values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#type BeyondcorpAppConnection#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpAppConnectionGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BeyondcorpAppConnectionGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpAppConnection.BeyondcorpAppConnectionGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f27a98aa8c79d11c433030d07778ed927b3e4d07a5d23ec4f537e4166959e27f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="ingressPort")
    def ingress_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ingressPort"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="appGatewayInput")
    def app_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="appGateway")
    def app_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appGateway"))

    @app_gateway.setter
    def app_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2686d15c1c5a77d53c9102a9daa810c45455358266abccfe1864f3a6d7f7dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appGateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d64079f866eb6a7bf158efb809e3d14c6e198aa7da65097168cd81a13a4b613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BeyondcorpAppConnectionGateway]:
        return typing.cast(typing.Optional[BeyondcorpAppConnectionGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BeyondcorpAppConnectionGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b0792632170583cf224d5c3b145edf65ed0ffc35db31ae6384233ff3ee4d47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.beyondcorpAppConnection.BeyondcorpAppConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BeyondcorpAppConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#create BeyondcorpAppConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#delete BeyondcorpAppConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#update BeyondcorpAppConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fa82453c0421c106b9e3d87abb2d485b010922b805e0e10027f8b67d19084d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#create BeyondcorpAppConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#delete BeyondcorpAppConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/beyondcorp_app_connection#update BeyondcorpAppConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BeyondcorpAppConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BeyondcorpAppConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.beyondcorpAppConnection.BeyondcorpAppConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6192e2c5afdc42763c9c179064df523b80fd8316b051de6bff1d2bcd6322c6ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5ce7e9bc8d0bcdd1bf5ebcd9377ec9ffb620c3e9819f62bfe3149fdae5f8552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b69a2c506eac19cbf371ba24a4ee2f6ad09d31c380e03dda67e8492e7403867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5146e0f1301640e9664c7362930a02754ddcbe949736e1a0f503757504d9395f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpAppConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpAppConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpAppConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597fd6e9453479b478a97d04a6a62822432d8a75759446a40aa55a8880219e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BeyondcorpAppConnection",
    "BeyondcorpAppConnectionApplicationEndpoint",
    "BeyondcorpAppConnectionApplicationEndpointOutputReference",
    "BeyondcorpAppConnectionConfig",
    "BeyondcorpAppConnectionGateway",
    "BeyondcorpAppConnectionGatewayOutputReference",
    "BeyondcorpAppConnectionTimeouts",
    "BeyondcorpAppConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__443e10c08e37c77ac10ff5ee7026eb2fe5ea1c4fb6db91b4188a167c15c8789d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    application_endpoint: typing.Union[BeyondcorpAppConnectionApplicationEndpoint, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    connectors: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gateway: typing.Optional[typing.Union[BeyondcorpAppConnectionGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BeyondcorpAppConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__826d8006f5a4b060cbddb0dce0ba1fd345d0cdc46b1080d30511295553caa37f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af98d29d7b78e10b30b391fce13835080cb0c74c8ecb42426e3e2ffcd2e23770(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1cadf21641839c60e85d4202146cdd21a9abb2cc9b30d42287cb006da653f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fa37a860d2feb946419e3a969b29631688c938e7cf1a4eaec945b48373a5eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a692a31dfadb2a7c06efa77ee505c43f450cc9ef025bc3c10564b79b6b7f5dcf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dd9dafb7ee014962798789a84b17bca5f3ab296713f363bfaee8e5a2f9fe75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce5d5645d49c904203e7b8422eb6e4ab46905e2ec5f391f535a9744ea9c65b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe4c9f680fb30f91ee2247383f7e35be2fd5e2a3a6535cfe314cb456eaf20d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16632a564513377107b787821e214c290bf8f4aa65efd6e0e3d482449d7e5fb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd531c9e158c1058d2de5990741c72b6f69ef1ec388e9d010184e49b24c1f042(
    *,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dfc557e2c60778b52aa7a3d7a6fcdf8668cafbb709f9e1a42625e2275e9f6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8f012efbf2b7e1f821b994881725883b9feef9197113c539259982bea6fcb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d9d21f8612bc316180fd82c5adcb811ad7d2dda6e224d07ce1d2eab79601c4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4786c0cc7df187b5e146f8c23a731836a35758f182c1e42ddbf55da478547af2(
    value: typing.Optional[BeyondcorpAppConnectionApplicationEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd02d0d614e94cf2973de70e550abe25a79ddd8ed360da454391cc8624c7c5f3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_endpoint: typing.Union[BeyondcorpAppConnectionApplicationEndpoint, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    connectors: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gateway: typing.Optional[typing.Union[BeyondcorpAppConnectionGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BeyondcorpAppConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f2fe96d8cfecbb39d682b457d4b15b3878d4876f88390cbd268d6390f4b35f(
    *,
    app_gateway: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27a98aa8c79d11c433030d07778ed927b3e4d07a5d23ec4f537e4166959e27f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2686d15c1c5a77d53c9102a9daa810c45455358266abccfe1864f3a6d7f7dad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d64079f866eb6a7bf158efb809e3d14c6e198aa7da65097168cd81a13a4b613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b0792632170583cf224d5c3b145edf65ed0ffc35db31ae6384233ff3ee4d47(
    value: typing.Optional[BeyondcorpAppConnectionGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fa82453c0421c106b9e3d87abb2d485b010922b805e0e10027f8b67d19084d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6192e2c5afdc42763c9c179064df523b80fd8316b051de6bff1d2bcd6322c6ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5ce7e9bc8d0bcdd1bf5ebcd9377ec9ffb620c3e9819f62bfe3149fdae5f8552(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b69a2c506eac19cbf371ba24a4ee2f6ad09d31c380e03dda67e8492e7403867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5146e0f1301640e9664c7362930a02754ddcbe949736e1a0f503757504d9395f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597fd6e9453479b478a97d04a6a62822432d8a75759446a40aa55a8880219e1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BeyondcorpAppConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
