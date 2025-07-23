r'''
# `google_network_connectivity_service_connection_policy`

Refer to the Terraform Registry for docs: [`google_network_connectivity_service_connection_policy`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy).
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


class NetworkConnectivityServiceConnectionPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy google_network_connectivity_service_connection_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        network: builtins.str,
        service_class: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["NetworkConnectivityServiceConnectionPolicyPscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectivityServiceConnectionPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy google_network_connectivity_service_connection_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the ServiceConnectionPolicy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#location NetworkConnectivityServiceConnectionPolicy#location}
        :param name: The name of a ServiceConnectionPolicy. Format: projects/{project}/locations/{location}/serviceConnectionPolicies/{service_connection_policy} See: https://google.aip.dev/122#fields-representing-resource-names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#name NetworkConnectivityServiceConnectionPolicy#name}
        :param network: The resource path of the consumer network. Example: - projects/{projectNumOrId}/global/networks/{resourceId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#network NetworkConnectivityServiceConnectionPolicy#network}
        :param service_class: The service class identifier for which this ServiceConnectionPolicy is for. The service class identifier is a unique, symbolic representation of a ServiceClass. It is provided by the Service Producer. Google services have a prefix of gcp. For example, gcp-cloud-sql. 3rd party services do not. For example, test-service-a3dfcx. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#service_class NetworkConnectivityServiceConnectionPolicy#service_class}
        :param description: Free-text description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#description NetworkConnectivityServiceConnectionPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#id NetworkConnectivityServiceConnectionPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#labels NetworkConnectivityServiceConnectionPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#project NetworkConnectivityServiceConnectionPolicy#project}.
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#psc_config NetworkConnectivityServiceConnectionPolicy#psc_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#timeouts NetworkConnectivityServiceConnectionPolicy#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dda34d34e224a1a73853010e2b811be91afb25bc95074ddb5e7c7eacd4ae1d7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkConnectivityServiceConnectionPolicyConfig(
            location=location,
            name=name,
            network=network,
            service_class=service_class,
            description=description,
            id=id,
            labels=labels,
            project=project,
            psc_config=psc_config,
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
        '''Generates CDKTF code for importing a NetworkConnectivityServiceConnectionPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkConnectivityServiceConnectionPolicy to import.
        :param import_from_id: The id of the existing NetworkConnectivityServiceConnectionPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkConnectivityServiceConnectionPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee22efe6af096870c5dff2e30b4b3ff926326702954665e60d214aaf5d9eb45)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPscConfig")
    def put_psc_config(
        self,
        *,
        subnetworks: typing.Sequence[builtins.str],
        allowed_google_producers_resource_hierarchy_level: typing.Optional[typing.Sequence[builtins.str]] = None,
        limit: typing.Optional[builtins.str] = None,
        producer_instance_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subnetworks: IDs of the subnetworks or fully qualified identifiers for the subnetworks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#subnetworks NetworkConnectivityServiceConnectionPolicy#subnetworks}
        :param allowed_google_producers_resource_hierarchy_level: List of Projects, Folders, or Organizations from where the Producer instance can be within. For example, a network administrator can provide both 'organizations/foo' and 'projects/bar' as allowed_google_producers_resource_hierarchy_levels. This allowlists this network to connect with any Producer instance within the 'foo' organization or the 'bar' project. By default, allowedGoogleProducersResourceHierarchyLevel is empty. The format for each allowedGoogleProducersResourceHierarchyLevel is / where is one of 'projects', 'folders', or 'organizations' and is either the ID or the number of the resource type. Format for each allowedGoogleProducersResourceHierarchyLevel value: 'projects/' or 'folders/' or 'organizations/' Eg. [projects/my-project-id, projects/567, folders/891, organizations/123] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#allowed_google_producers_resource_hierarchy_level NetworkConnectivityServiceConnectionPolicy#allowed_google_producers_resource_hierarchy_level}
        :param limit: Max number of PSC connections for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#limit NetworkConnectivityServiceConnectionPolicy#limit}
        :param producer_instance_location: ProducerInstanceLocation is used to specify which authorization mechanism to use to determine which projects the Producer instance can be within. Possible values: ["PRODUCER_INSTANCE_LOCATION_UNSPECIFIED", "CUSTOM_RESOURCE_HIERARCHY_LEVELS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#producer_instance_location NetworkConnectivityServiceConnectionPolicy#producer_instance_location}
        '''
        value = NetworkConnectivityServiceConnectionPolicyPscConfig(
            subnetworks=subnetworks,
            allowed_google_producers_resource_hierarchy_level=allowed_google_producers_resource_hierarchy_level,
            limit=limit,
            producer_instance_location=producer_instance_location,
        )

        return typing.cast(None, jsii.invoke(self, "putPscConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#create NetworkConnectivityServiceConnectionPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#delete NetworkConnectivityServiceConnectionPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#update NetworkConnectivityServiceConnectionPolicy#update}.
        '''
        value = NetworkConnectivityServiceConnectionPolicyTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPscConfig")
    def reset_psc_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPscConfig", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="infrastructure")
    def infrastructure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "infrastructure"))

    @builtins.property
    @jsii.member(jsii_name="pscConfig")
    def psc_config(
        self,
    ) -> "NetworkConnectivityServiceConnectionPolicyPscConfigOutputReference":
        return typing.cast("NetworkConnectivityServiceConnectionPolicyPscConfigOutputReference", jsii.get(self, "pscConfig"))

    @builtins.property
    @jsii.member(jsii_name="pscConnections")
    def psc_connections(
        self,
    ) -> "NetworkConnectivityServiceConnectionPolicyPscConnectionsList":
        return typing.cast("NetworkConnectivityServiceConnectionPolicyPscConnectionsList", jsii.get(self, "pscConnections"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "NetworkConnectivityServiceConnectionPolicyTimeoutsOutputReference":
        return typing.cast("NetworkConnectivityServiceConnectionPolicyTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pscConfigInput")
    def psc_config_input(
        self,
    ) -> typing.Optional["NetworkConnectivityServiceConnectionPolicyPscConfig"]:
        return typing.cast(typing.Optional["NetworkConnectivityServiceConnectionPolicyPscConfig"], jsii.get(self, "pscConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceClassInput")
    def service_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceClassInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectivityServiceConnectionPolicyTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkConnectivityServiceConnectionPolicyTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df059fd3d89da3bb21af79c99f9440b48feabf957db6fa42a2cf3b33ec2c6f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d35e7f6d6e16edd1a94f6e7a95ef4e5d0feeb1086a1e477303f6b68ec51234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ad376dd1dbb7ab07f7a147f56b5de38daef754eaebc42118e8a4e830bd1ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0692aaf94477bc55807a029feb592ed7ba3365d3dd60f83354c40b1badb350b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f09505ae80210b30be59b5182bc52915d68f004c45d16f3a80cba8931fec8df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c50f171eaa273103088b964b98c305d8111a242751e94bedca9b8014ee32a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832befd477608d38646b289f4f3ce51c69979c01fcebbd3e921c9d89f2bcc040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceClass")
    def service_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceClass"))

    @service_class.setter
    def service_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe03707cef3a5c92d14e5a01e943cac3d3f50bc0e35cc178d36484396782b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceClass", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyConfig",
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
        "network": "network",
        "service_class": "serviceClass",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "psc_config": "pscConfig",
        "timeouts": "timeouts",
    },
)
class NetworkConnectivityServiceConnectionPolicyConfig(
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
        name: builtins.str,
        network: builtins.str,
        service_class: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        psc_config: typing.Optional[typing.Union["NetworkConnectivityServiceConnectionPolicyPscConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["NetworkConnectivityServiceConnectionPolicyTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the ServiceConnectionPolicy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#location NetworkConnectivityServiceConnectionPolicy#location}
        :param name: The name of a ServiceConnectionPolicy. Format: projects/{project}/locations/{location}/serviceConnectionPolicies/{service_connection_policy} See: https://google.aip.dev/122#fields-representing-resource-names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#name NetworkConnectivityServiceConnectionPolicy#name}
        :param network: The resource path of the consumer network. Example: - projects/{projectNumOrId}/global/networks/{resourceId}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#network NetworkConnectivityServiceConnectionPolicy#network}
        :param service_class: The service class identifier for which this ServiceConnectionPolicy is for. The service class identifier is a unique, symbolic representation of a ServiceClass. It is provided by the Service Producer. Google services have a prefix of gcp. For example, gcp-cloud-sql. 3rd party services do not. For example, test-service-a3dfcx. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#service_class NetworkConnectivityServiceConnectionPolicy#service_class}
        :param description: Free-text description of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#description NetworkConnectivityServiceConnectionPolicy#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#id NetworkConnectivityServiceConnectionPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#labels NetworkConnectivityServiceConnectionPolicy#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#project NetworkConnectivityServiceConnectionPolicy#project}.
        :param psc_config: psc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#psc_config NetworkConnectivityServiceConnectionPolicy#psc_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#timeouts NetworkConnectivityServiceConnectionPolicy#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(psc_config, dict):
            psc_config = NetworkConnectivityServiceConnectionPolicyPscConfig(**psc_config)
        if isinstance(timeouts, dict):
            timeouts = NetworkConnectivityServiceConnectionPolicyTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ef0cabee387c59d3e9afe5a646d1b9f43158422723ba9c66cf0bfaef7e3ddc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument service_class", value=service_class, expected_type=type_hints["service_class"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument psc_config", value=psc_config, expected_type=type_hints["psc_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "network": network,
            "service_class": service_class,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if psc_config is not None:
            self._values["psc_config"] = psc_config
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
        '''The location of the ServiceConnectionPolicy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#location NetworkConnectivityServiceConnectionPolicy#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a ServiceConnectionPolicy. Format: projects/{project}/locations/{location}/serviceConnectionPolicies/{service_connection_policy} See: https://google.aip.dev/122#fields-representing-resource-names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#name NetworkConnectivityServiceConnectionPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''The resource path of the consumer network. Example: - projects/{projectNumOrId}/global/networks/{resourceId}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#network NetworkConnectivityServiceConnectionPolicy#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_class(self) -> builtins.str:
        '''The service class identifier for which this ServiceConnectionPolicy is for.

        The service class identifier is a unique, symbolic representation of a ServiceClass.
        It is provided by the Service Producer. Google services have a prefix of gcp. For example, gcp-cloud-sql. 3rd party services do not. For example, test-service-a3dfcx.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#service_class NetworkConnectivityServiceConnectionPolicy#service_class}
        '''
        result = self._values.get("service_class")
        assert result is not None, "Required property 'service_class' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Free-text description of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#description NetworkConnectivityServiceConnectionPolicy#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#id NetworkConnectivityServiceConnectionPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#labels NetworkConnectivityServiceConnectionPolicy#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#project NetworkConnectivityServiceConnectionPolicy#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def psc_config(
        self,
    ) -> typing.Optional["NetworkConnectivityServiceConnectionPolicyPscConfig"]:
        '''psc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#psc_config NetworkConnectivityServiceConnectionPolicy#psc_config}
        '''
        result = self._values.get("psc_config")
        return typing.cast(typing.Optional["NetworkConnectivityServiceConnectionPolicyPscConfig"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["NetworkConnectivityServiceConnectionPolicyTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#timeouts NetworkConnectivityServiceConnectionPolicy#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkConnectivityServiceConnectionPolicyTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityServiceConnectionPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConfig",
    jsii_struct_bases=[],
    name_mapping={
        "subnetworks": "subnetworks",
        "allowed_google_producers_resource_hierarchy_level": "allowedGoogleProducersResourceHierarchyLevel",
        "limit": "limit",
        "producer_instance_location": "producerInstanceLocation",
    },
)
class NetworkConnectivityServiceConnectionPolicyPscConfig:
    def __init__(
        self,
        *,
        subnetworks: typing.Sequence[builtins.str],
        allowed_google_producers_resource_hierarchy_level: typing.Optional[typing.Sequence[builtins.str]] = None,
        limit: typing.Optional[builtins.str] = None,
        producer_instance_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param subnetworks: IDs of the subnetworks or fully qualified identifiers for the subnetworks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#subnetworks NetworkConnectivityServiceConnectionPolicy#subnetworks}
        :param allowed_google_producers_resource_hierarchy_level: List of Projects, Folders, or Organizations from where the Producer instance can be within. For example, a network administrator can provide both 'organizations/foo' and 'projects/bar' as allowed_google_producers_resource_hierarchy_levels. This allowlists this network to connect with any Producer instance within the 'foo' organization or the 'bar' project. By default, allowedGoogleProducersResourceHierarchyLevel is empty. The format for each allowedGoogleProducersResourceHierarchyLevel is / where is one of 'projects', 'folders', or 'organizations' and is either the ID or the number of the resource type. Format for each allowedGoogleProducersResourceHierarchyLevel value: 'projects/' or 'folders/' or 'organizations/' Eg. [projects/my-project-id, projects/567, folders/891, organizations/123] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#allowed_google_producers_resource_hierarchy_level NetworkConnectivityServiceConnectionPolicy#allowed_google_producers_resource_hierarchy_level}
        :param limit: Max number of PSC connections for this policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#limit NetworkConnectivityServiceConnectionPolicy#limit}
        :param producer_instance_location: ProducerInstanceLocation is used to specify which authorization mechanism to use to determine which projects the Producer instance can be within. Possible values: ["PRODUCER_INSTANCE_LOCATION_UNSPECIFIED", "CUSTOM_RESOURCE_HIERARCHY_LEVELS"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#producer_instance_location NetworkConnectivityServiceConnectionPolicy#producer_instance_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce56d3b04bf2992128a9be6ce773fbf20e9b7b522b17477eca3e4c3f9114693)
            check_type(argname="argument subnetworks", value=subnetworks, expected_type=type_hints["subnetworks"])
            check_type(argname="argument allowed_google_producers_resource_hierarchy_level", value=allowed_google_producers_resource_hierarchy_level, expected_type=type_hints["allowed_google_producers_resource_hierarchy_level"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument producer_instance_location", value=producer_instance_location, expected_type=type_hints["producer_instance_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnetworks": subnetworks,
        }
        if allowed_google_producers_resource_hierarchy_level is not None:
            self._values["allowed_google_producers_resource_hierarchy_level"] = allowed_google_producers_resource_hierarchy_level
        if limit is not None:
            self._values["limit"] = limit
        if producer_instance_location is not None:
            self._values["producer_instance_location"] = producer_instance_location

    @builtins.property
    def subnetworks(self) -> typing.List[builtins.str]:
        '''IDs of the subnetworks or fully qualified identifiers for the subnetworks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#subnetworks NetworkConnectivityServiceConnectionPolicy#subnetworks}
        '''
        result = self._values.get("subnetworks")
        assert result is not None, "Required property 'subnetworks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_google_producers_resource_hierarchy_level(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''List of Projects, Folders, or Organizations from where the Producer instance can be within.

        For example,
        a network administrator can provide both 'organizations/foo' and 'projects/bar' as
        allowed_google_producers_resource_hierarchy_levels. This allowlists this network to connect with any Producer
        instance within the 'foo' organization or the 'bar' project. By default,
        allowedGoogleProducersResourceHierarchyLevel is empty. The format for each
        allowedGoogleProducersResourceHierarchyLevel is / where is one of 'projects', 'folders', or 'organizations'
        and is either the ID or the number of the resource type. Format for each
        allowedGoogleProducersResourceHierarchyLevel value: 'projects/' or 'folders/' or 'organizations/' Eg.
        [projects/my-project-id, projects/567, folders/891, organizations/123]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#allowed_google_producers_resource_hierarchy_level NetworkConnectivityServiceConnectionPolicy#allowed_google_producers_resource_hierarchy_level}
        '''
        result = self._values.get("allowed_google_producers_resource_hierarchy_level")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def limit(self) -> typing.Optional[builtins.str]:
        '''Max number of PSC connections for this policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#limit NetworkConnectivityServiceConnectionPolicy#limit}
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def producer_instance_location(self) -> typing.Optional[builtins.str]:
        '''ProducerInstanceLocation is used to specify which authorization mechanism to use to determine which projects the Producer instance can be within.

        Possible values: ["PRODUCER_INSTANCE_LOCATION_UNSPECIFIED", "CUSTOM_RESOURCE_HIERARCHY_LEVELS"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#producer_instance_location NetworkConnectivityServiceConnectionPolicy#producer_instance_location}
        '''
        result = self._values.get("producer_instance_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityServiceConnectionPolicyPscConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityServiceConnectionPolicyPscConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bdc743e7e33da88dce74411c4a5239da027c0ee5d3049e1b3588daf7eb3fce6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedGoogleProducersResourceHierarchyLevel")
    def reset_allowed_google_producers_resource_hierarchy_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedGoogleProducersResourceHierarchyLevel", []))

    @jsii.member(jsii_name="resetLimit")
    def reset_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimit", []))

    @jsii.member(jsii_name="resetProducerInstanceLocation")
    def reset_producer_instance_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProducerInstanceLocation", []))

    @builtins.property
    @jsii.member(jsii_name="allowedGoogleProducersResourceHierarchyLevelInput")
    def allowed_google_producers_resource_hierarchy_level_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedGoogleProducersResourceHierarchyLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="producerInstanceLocationInput")
    def producer_instance_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "producerInstanceLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworksInput")
    def subnetworks_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetworksInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedGoogleProducersResourceHierarchyLevel")
    def allowed_google_producers_resource_hierarchy_level(
        self,
    ) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedGoogleProducersResourceHierarchyLevel"))

    @allowed_google_producers_resource_hierarchy_level.setter
    def allowed_google_producers_resource_hierarchy_level(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2073b745f0dec088a924828ecad267b2c622c32879033ced9999f3a93108e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedGoogleProducersResourceHierarchyLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47736e5276994ecdfc296c3c242aaa84099d0503822badd1ff6edc5c43d72c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="producerInstanceLocation")
    def producer_instance_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "producerInstanceLocation"))

    @producer_instance_location.setter
    def producer_instance_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a66777b1e1c414af20e856313e262e053e3d42f0b1f93ce381e5ae0df7b0826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "producerInstanceLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworks")
    def subnetworks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetworks"))

    @subnetworks.setter
    def subnetworks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bde9f27d2907a0b936254ccb80742e91a8cf2e704356cc4550ee3a8c9fb5557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConfig]:
        return typing.cast(typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85db3003f737c6ddf7de76fde79a74f8ceb69075c8941aaf06904a22133a4045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnections",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetworkConnectivityServiceConnectionPolicyPscConnections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityServiceConnectionPolicyPscConnections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnectionsError",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetworkConnectivityServiceConnectionPolicyPscConnectionsError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityServiceConnectionPolicyPscConnectionsError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__019561054bc5aa9f9d2670c5d5a0a0f15343b2fa255fa80ea06501d0c1c7370d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ace130257fded4a473a3b9e3010f95ec960dc82f310ddc586cab0bfbb80e747)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca048939a4386a588c2f93d852e5a574eed75ce36a80079dc817c4ed6155e22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa21f18156ae67a57f49b12c64cad40e37152f98b2fd0ef905de6a45549b032)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9df1effe05e62d37b5f718394b7e4e237c1b78a46bacfefb55c26836e5c4f8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23ba7db80c313230aba76c76e2e9f1cb5b38cf611e7b26ad9b44a9ee95bfe6d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfo]:
        return typing.cast(typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a88fdb33a59f73974edbffc2279ccc85f03ec50c7bdffd302b6ed091ced0a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d653413e7bee19c1f323ccaf49f72144a3a9b1ffa017b8788b46ff314db8fb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3798f56ca4b2501ce9f56e840b52c8f643eac9d419491e1f63383522718523b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f7502aeef5b76155a6c5fbe4c0609afb3d9be4d4f0da6d4081568d7f30f878)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c25b2a3d167df49c1501c3426e614f032ac9df133c117c45c7e22d807c7e2763)
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
            type_hints = typing.get_type_hints(_typecheckingstub__416a8faa129f7d0fa878c185901fb05c422ab4407aef4721159cc9c085ac17a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__403941995c9932b6308c48d96fe271a706128603faa56603638314bc640888b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> _cdktf_9a9027ec.StringMapList:
        return typing.cast(_cdktf_9a9027ec.StringMapList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnectionsError]:
        return typing.cast(typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnectionsError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnectionsError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f00a48bef13c9c7bebc12f309352bdc1f6ad9f3623ea4701519fedf12acc0f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivityServiceConnectionPolicyPscConnectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52403366203c8f67f0ea1ffbcc8492cf420639a27ede68c3f66156ebf4930b56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkConnectivityServiceConnectionPolicyPscConnectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c3ad3bcadc8fab381a97513a78bc8b2cce037e58dfbb00f1256ff13f88814a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkConnectivityServiceConnectionPolicyPscConnectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a51dda486def893dbf33ca685dbec5f2b9126f18790ff08ad2b3378bcd0606c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ededbcb72ff3851d6b0219aaf411bbeb7f18f9e8d895527f1a939789ebe82d3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32f3711e60bc354628742056c7e4d9c5c6e3c80864012890f98cba73f3f9bd0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class NetworkConnectivityServiceConnectionPolicyPscConnectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyPscConnectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f497d1836d4619e93b8bbe57ba75b51bfd8208706b0b48202d6946454483db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="consumerAddress")
    def consumer_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerAddress"))

    @builtins.property
    @jsii.member(jsii_name="consumerForwardingRule")
    def consumer_forwarding_rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerForwardingRule"))

    @builtins.property
    @jsii.member(jsii_name="consumerTargetProject")
    def consumer_target_project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerTargetProject"))

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorList:
        return typing.cast(NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorList, jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="errorInfo")
    def error_info(
        self,
    ) -> NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoList:
        return typing.cast(NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoList, jsii.get(self, "errorInfo"))

    @builtins.property
    @jsii.member(jsii_name="errorType")
    def error_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorType"))

    @builtins.property
    @jsii.member(jsii_name="gceOperation")
    def gce_operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gceOperation"))

    @builtins.property
    @jsii.member(jsii_name="pscConnectionId")
    def psc_connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pscConnectionId"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnections]:
        return typing.cast(typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f568a201f2b0c11b8e5baf1e6c3e7db04f2d93058e6f9f46fd3510fe3c30c9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkConnectivityServiceConnectionPolicyTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#create NetworkConnectivityServiceConnectionPolicy#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#delete NetworkConnectivityServiceConnectionPolicy#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#update NetworkConnectivityServiceConnectionPolicy#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25a0312c586f51bd90e4c05a476f6625f8423f501d6e30d2d3785996be3f543)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#create NetworkConnectivityServiceConnectionPolicy#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#delete NetworkConnectivityServiceConnectionPolicy#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_connectivity_service_connection_policy#update NetworkConnectivityServiceConnectionPolicy#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkConnectivityServiceConnectionPolicyTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkConnectivityServiceConnectionPolicyTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkConnectivityServiceConnectionPolicy.NetworkConnectivityServiceConnectionPolicyTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c88d0887c9da3c8c25531eb3bf8f164cd3c9c99a863ed5244ee0e4e7d3198ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f126305c412aff9222075e1734030d034dd02cbd368f038dc4f8ff3dfcead59f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bebe174be653a7179f166774267090149899a0b8eb236d7bd6f9290515da7889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef86e7b946c8be241a450161769f32beb5881f22525059687634d012173bdbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityServiceConnectionPolicyTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityServiceConnectionPolicyTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityServiceConnectionPolicyTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489e81996c3e1730fa2edb497be735eee40c3f3a0c4e3b5928f49d0388d40f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkConnectivityServiceConnectionPolicy",
    "NetworkConnectivityServiceConnectionPolicyConfig",
    "NetworkConnectivityServiceConnectionPolicyPscConfig",
    "NetworkConnectivityServiceConnectionPolicyPscConfigOutputReference",
    "NetworkConnectivityServiceConnectionPolicyPscConnections",
    "NetworkConnectivityServiceConnectionPolicyPscConnectionsError",
    "NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfo",
    "NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoList",
    "NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfoOutputReference",
    "NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorList",
    "NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorOutputReference",
    "NetworkConnectivityServiceConnectionPolicyPscConnectionsList",
    "NetworkConnectivityServiceConnectionPolicyPscConnectionsOutputReference",
    "NetworkConnectivityServiceConnectionPolicyTimeouts",
    "NetworkConnectivityServiceConnectionPolicyTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5dda34d34e224a1a73853010e2b811be91afb25bc95074ddb5e7c7eacd4ae1d7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    network: builtins.str,
    service_class: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[NetworkConnectivityServiceConnectionPolicyPscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectivityServiceConnectionPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4ee22efe6af096870c5dff2e30b4b3ff926326702954665e60d214aaf5d9eb45(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df059fd3d89da3bb21af79c99f9440b48feabf957db6fa42a2cf3b33ec2c6f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d35e7f6d6e16edd1a94f6e7a95ef4e5d0feeb1086a1e477303f6b68ec51234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ad376dd1dbb7ab07f7a147f56b5de38daef754eaebc42118e8a4e830bd1ffa(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0692aaf94477bc55807a029feb592ed7ba3365d3dd60f83354c40b1badb350b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f09505ae80210b30be59b5182bc52915d68f004c45d16f3a80cba8931fec8df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c50f171eaa273103088b964b98c305d8111a242751e94bedca9b8014ee32a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832befd477608d38646b289f4f3ce51c69979c01fcebbd3e921c9d89f2bcc040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe03707cef3a5c92d14e5a01e943cac3d3f50bc0e35cc178d36484396782b07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ef0cabee387c59d3e9afe5a646d1b9f43158422723ba9c66cf0bfaef7e3ddc(
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
    network: builtins.str,
    service_class: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    psc_config: typing.Optional[typing.Union[NetworkConnectivityServiceConnectionPolicyPscConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[NetworkConnectivityServiceConnectionPolicyTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce56d3b04bf2992128a9be6ce773fbf20e9b7b522b17477eca3e4c3f9114693(
    *,
    subnetworks: typing.Sequence[builtins.str],
    allowed_google_producers_resource_hierarchy_level: typing.Optional[typing.Sequence[builtins.str]] = None,
    limit: typing.Optional[builtins.str] = None,
    producer_instance_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdc743e7e33da88dce74411c4a5239da027c0ee5d3049e1b3588daf7eb3fce6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2073b745f0dec088a924828ecad267b2c622c32879033ced9999f3a93108e87(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47736e5276994ecdfc296c3c242aaa84099d0503822badd1ff6edc5c43d72c9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a66777b1e1c414af20e856313e262e053e3d42f0b1f93ce381e5ae0df7b0826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bde9f27d2907a0b936254ccb80742e91a8cf2e704356cc4550ee3a8c9fb5557(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85db3003f737c6ddf7de76fde79a74f8ceb69075c8941aaf06904a22133a4045(
    value: typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019561054bc5aa9f9d2670c5d5a0a0f15343b2fa255fa80ea06501d0c1c7370d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ace130257fded4a473a3b9e3010f95ec960dc82f310ddc586cab0bfbb80e747(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca048939a4386a588c2f93d852e5a574eed75ce36a80079dc817c4ed6155e22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa21f18156ae67a57f49b12c64cad40e37152f98b2fd0ef905de6a45549b032(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9df1effe05e62d37b5f718394b7e4e237c1b78a46bacfefb55c26836e5c4f8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ba7db80c313230aba76c76e2e9f1cb5b38cf611e7b26ad9b44a9ee95bfe6d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a88fdb33a59f73974edbffc2279ccc85f03ec50c7bdffd302b6ed091ced0a1(
    value: typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnectionsErrorInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d653413e7bee19c1f323ccaf49f72144a3a9b1ffa017b8788b46ff314db8fb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3798f56ca4b2501ce9f56e840b52c8f643eac9d419491e1f63383522718523b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f7502aeef5b76155a6c5fbe4c0609afb3d9be4d4f0da6d4081568d7f30f878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25b2a3d167df49c1501c3426e614f032ac9df133c117c45c7e22d807c7e2763(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416a8faa129f7d0fa878c185901fb05c422ab4407aef4721159cc9c085ac17a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403941995c9932b6308c48d96fe271a706128603faa56603638314bc640888b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f00a48bef13c9c7bebc12f309352bdc1f6ad9f3623ea4701519fedf12acc0f8(
    value: typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnectionsError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52403366203c8f67f0ea1ffbcc8492cf420639a27ede68c3f66156ebf4930b56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c3ad3bcadc8fab381a97513a78bc8b2cce037e58dfbb00f1256ff13f88814a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51dda486def893dbf33ca685dbec5f2b9126f18790ff08ad2b3378bcd0606c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ededbcb72ff3851d6b0219aaf411bbeb7f18f9e8d895527f1a939789ebe82d3c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f3711e60bc354628742056c7e4d9c5c6e3c80864012890f98cba73f3f9bd0f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f497d1836d4619e93b8bbe57ba75b51bfd8208706b0b48202d6946454483db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f568a201f2b0c11b8e5baf1e6c3e7db04f2d93058e6f9f46fd3510fe3c30c9e(
    value: typing.Optional[NetworkConnectivityServiceConnectionPolicyPscConnections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25a0312c586f51bd90e4c05a476f6625f8423f501d6e30d2d3785996be3f543(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c88d0887c9da3c8c25531eb3bf8f164cd3c9c99a863ed5244ee0e4e7d3198ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f126305c412aff9222075e1734030d034dd02cbd368f038dc4f8ff3dfcead59f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bebe174be653a7179f166774267090149899a0b8eb236d7bd6f9290515da7889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef86e7b946c8be241a450161769f32beb5881f22525059687634d012173bdbe6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489e81996c3e1730fa2edb497be735eee40c3f3a0c4e3b5928f49d0388d40f8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkConnectivityServiceConnectionPolicyTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
