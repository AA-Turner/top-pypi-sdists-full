r'''
# `google_container_azure_cluster`

Refer to the Terraform Registry for docs: [`google_container_azure_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster).
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


class ContainerAzureCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster google_container_azure_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization: typing.Union["ContainerAzureClusterAuthorization", typing.Dict[builtins.str, typing.Any]],
        azure_region: builtins.str,
        control_plane: typing.Union["ContainerAzureClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["ContainerAzureClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["ContainerAzureClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        resource_group_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        azure_services_authentication: typing.Optional[typing.Union["ContainerAzureClusterAzureServicesAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAzureClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster google_container_azure_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#authorization ContainerAzureCluster#authorization}
        :param azure_region: The Azure region where the cluster runs. Each Google Cloud region supports a subset of nearby Azure regions. You can call to list all supported Azure regions within a given Google Cloud region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#azure_region ContainerAzureCluster#azure_region}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#control_plane ContainerAzureCluster#control_plane}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#fleet ContainerAzureCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#location ContainerAzureCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#name ContainerAzureCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#networking ContainerAzureCluster#networking}
        :param resource_group_id: The ARM ID of the resource group where the cluster resources are deployed. For example: ``/subscriptions/* /resourceGroups/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#resource_group_id ContainerAzureCluster#resource_group_id} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Keys can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#annotations ContainerAzureCluster#annotations}
        :param azure_services_authentication: azure_services_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#azure_services_authentication ContainerAzureCluster#azure_services_authentication}
        :param client: Name of the AzureClient. The ``AzureClient`` resource must reside on the same GCP project and region as the ``AzureCluster``. ``AzureClient`` names are formatted as ``projects/<project-number>/locations/<region>/azureClients/<client-id>``. See Resource Names (https:cloud.google.com/apis/design/resource_names) for more details on Google Cloud resource names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#client ContainerAzureCluster#client}
        :param description: Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#description ContainerAzureCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#id ContainerAzureCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#project ContainerAzureCluster#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#timeouts ContainerAzureCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c11e721d46e3a7b82a123bcdcf802843c097210fc68f22232bbafb3a923d4c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerAzureClusterConfig(
            authorization=authorization,
            azure_region=azure_region,
            control_plane=control_plane,
            fleet=fleet,
            location=location,
            name=name,
            networking=networking,
            resource_group_id=resource_group_id,
            annotations=annotations,
            azure_services_authentication=azure_services_authentication,
            client=client,
            description=description,
            id=id,
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
        '''Generates CDKTF code for importing a ContainerAzureCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAzureCluster to import.
        :param import_from_id: The id of the existing ContainerAzureCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAzureCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d312089e27db042c8fc2110c0cda37b3a5af91417368ee7e3a1dfc4c3e3d739)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAzureClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
        admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAzureClusterAuthorizationAdminGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#admin_users ContainerAzureCluster#admin_users}
        :param admin_groups: admin_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#admin_groups ContainerAzureCluster#admin_groups}
        '''
        value = ContainerAzureClusterAuthorization(
            admin_users=admin_users, admin_groups=admin_groups
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putAzureServicesAuthentication")
    def put_azure_services_authentication(
        self,
        *,
        application_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param application_id: The Azure Active Directory Application ID for Authentication configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#application_id ContainerAzureCluster#application_id}
        :param tenant_id: The Azure Active Directory Tenant ID for Authentication configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#tenant_id ContainerAzureCluster#tenant_id}
        '''
        value = ContainerAzureClusterAzureServicesAuthentication(
            application_id=application_id, tenant_id=tenant_id
        )

        return typing.cast(None, jsii.invoke(self, "putAzureServicesAuthentication", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        ssh_config: typing.Union["ContainerAzureClusterControlPlaneSshConfig", typing.Dict[builtins.str, typing.Any]],
        subnet_id: builtins.str,
        version: builtins.str,
        database_encryption: typing.Optional[typing.Union["ContainerAzureClusterControlPlaneDatabaseEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        main_volume: typing.Optional[typing.Union["ContainerAzureClusterControlPlaneMainVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAzureClusterControlPlaneProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        replica_placements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAzureClusterControlPlaneReplicaPlacements", typing.Dict[builtins.str, typing.Any]]]]] = None,
        root_volume: typing.Optional[typing.Union["ContainerAzureClusterControlPlaneRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vm_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#ssh_config ContainerAzureCluster#ssh_config}
        :param subnet_id: The ARM ID of the subnet where the control plane VMs are deployed. Example: ``/subscriptions//resourceGroups//providers/Microsoft.Network/virtualNetworks//subnets/default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#subnet_id ContainerAzureCluster#subnet_id}
        :param version: The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAzureServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#version ContainerAzureCluster#version}
        :param database_encryption: database_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#database_encryption ContainerAzureCluster#database_encryption}
        :param main_volume: main_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#main_volume ContainerAzureCluster#main_volume}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#proxy_config ContainerAzureCluster#proxy_config}
        :param replica_placements: replica_placements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#replica_placements ContainerAzureCluster#replica_placements}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#root_volume ContainerAzureCluster#root_volume}
        :param tags: Optional. A set of tags to apply to all underlying control plane Azure resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#tags ContainerAzureCluster#tags}
        :param vm_size: Optional. The Azure VM size name. Example: ``Standard_DS2_v2``. For available VM sizes, see https://docs.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions. When unspecified, it defaults to ``Standard_DS2_v2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#vm_size ContainerAzureCluster#vm_size}
        '''
        value = ContainerAzureClusterControlPlane(
            ssh_config=ssh_config,
            subnet_id=subnet_id,
            version=version,
            database_encryption=database_encryption,
            main_volume=main_volume,
            proxy_config=proxy_config,
            replica_placements=replica_placements,
            root_volume=root_volume,
            tags=tags,
            vm_size=vm_size,
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putFleet")
    def put_fleet(self, *, project: typing.Optional[builtins.str] = None) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#project ContainerAzureCluster#project}
        '''
        value = ContainerAzureClusterFleet(project=project)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putNetworking")
    def put_networking(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: The IP address range of the pods in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All pods in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#pod_address_cidr_blocks ContainerAzureCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: The IP address range for services in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All services in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creating a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#service_address_cidr_blocks ContainerAzureCluster#service_address_cidr_blocks}
        :param virtual_network_id: The Azure Resource Manager (ARM) ID of the VNet associated with your cluster. All components in the cluster (i.e. control plane and node pools) run on a single VNet. Example: ``/subscriptions/* /resourceGroups/* /providers/Microsoft.Network/virtualNetworks/*`` This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#virtual_network_id ContainerAzureCluster#virtual_network_id} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = ContainerAzureClusterNetworking(
            pod_address_cidr_blocks=pod_address_cidr_blocks,
            service_address_cidr_blocks=service_address_cidr_blocks,
            virtual_network_id=virtual_network_id,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworking", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#create ContainerAzureCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#delete ContainerAzureCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#update ContainerAzureCluster#update}.
        '''
        value = ContainerAzureClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAzureServicesAuthentication")
    def reset_azure_services_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureServicesAuthentication", []))

    @jsii.member(jsii_name="resetClient")
    def reset_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClient", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="authorization")
    def authorization(self) -> "ContainerAzureClusterAuthorizationOutputReference":
        return typing.cast("ContainerAzureClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="azureServicesAuthentication")
    def azure_services_authentication(
        self,
    ) -> "ContainerAzureClusterAzureServicesAuthenticationOutputReference":
        return typing.cast("ContainerAzureClusterAzureServicesAuthenticationOutputReference", jsii.get(self, "azureServicesAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> "ContainerAzureClusterControlPlaneOutputReference":
        return typing.cast("ContainerAzureClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> "ContainerAzureClusterFleetOutputReference":
        return typing.cast("ContainerAzureClusterFleetOutputReference", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="networking")
    def networking(self) -> "ContainerAzureClusterNetworkingOutputReference":
        return typing.cast("ContainerAzureClusterNetworkingOutputReference", jsii.get(self, "networking"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerAzureClusterTimeoutsOutputReference":
        return typing.cast("ContainerAzureClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="workloadIdentityConfig")
    def workload_identity_config(
        self,
    ) -> "ContainerAzureClusterWorkloadIdentityConfigList":
        return typing.cast("ContainerAzureClusterWorkloadIdentityConfigList", jsii.get(self, "workloadIdentityConfig"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional["ContainerAzureClusterAuthorization"]:
        return typing.cast(typing.Optional["ContainerAzureClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="azureRegionInput")
    def azure_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="azureServicesAuthenticationInput")
    def azure_services_authentication_input(
        self,
    ) -> typing.Optional["ContainerAzureClusterAzureServicesAuthentication"]:
        return typing.cast(typing.Optional["ContainerAzureClusterAzureServicesAuthentication"], jsii.get(self, "azureServicesAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientInput")
    def client_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["ContainerAzureClusterControlPlane"]:
        return typing.cast(typing.Optional["ContainerAzureClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetInput")
    def fleet_input(self) -> typing.Optional["ContainerAzureClusterFleet"]:
        return typing.cast(typing.Optional["ContainerAzureClusterFleet"], jsii.get(self, "fleetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkingInput")
    def networking_input(self) -> typing.Optional["ContainerAzureClusterNetworking"]:
        return typing.cast(typing.Optional["ContainerAzureClusterNetworking"], jsii.get(self, "networkingInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupIdInput")
    def resource_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAzureClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAzureClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f471b5002f69a87a2c2fc982ce5b4ee51c1a68c40cb518ec853cfb51d2e5abf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureRegion")
    def azure_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureRegion"))

    @azure_region.setter
    def azure_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f79001d7d32f4d7520da2adfceb7026378e618e1804358ae53e18fcc83fab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="client")
    def client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "client"))

    @client.setter
    def client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fcfe9bbcf35986d41d8794db92451793edb5898009bc03a0e602ec1cf1569e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "client", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c16a68eb219ee30fd5a80bfce485ea3e24c36457f39c4d067d678e405a2bcbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e46a79a93b144e0230d4abafe304189b048e56ccb06609017c28c54971f0b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac711f221b1292e79b8716ecbd5623bf275a8dfa60027bf88a13d3e084603a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066fc0bf5c2f361b5593ee97fe72944b2a2c2fff2e7a888c7ca392cc7541eb0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f75ac2cb48f693a863943a43f2a8dd08f6ca38e7c59897c8902c47203824539)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupId"))

    @resource_group_id.setter
    def resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84589d5c9aa3659efd1a1cb755b0f9f6b35c82e12cd74465e6dbddd9998effd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers", "admin_groups": "adminGroups"},
)
class ContainerAzureClusterAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAzureClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
        admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAzureClusterAuthorizationAdminGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#admin_users ContainerAzureCluster#admin_users}
        :param admin_groups: admin_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#admin_groups ContainerAzureCluster#admin_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfec5578783816bcdcc9d454defedf21fb230508a8c1ef4401da92b1c363f37)
            check_type(argname="argument admin_users", value=admin_users, expected_type=type_hints["admin_users"])
            check_type(argname="argument admin_groups", value=admin_groups, expected_type=type_hints["admin_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_users": admin_users,
        }
        if admin_groups is not None:
            self._values["admin_groups"] = admin_groups

    @builtins.property
    def admin_users(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAzureClusterAuthorizationAdminUsers"]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#admin_users ContainerAzureCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAzureClusterAuthorizationAdminUsers"]], result)

    @builtins.property
    def admin_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAzureClusterAuthorizationAdminGroups"]]]:
        '''admin_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#admin_groups ContainerAzureCluster#admin_groups}
        '''
        result = self._values.get("admin_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAzureClusterAuthorizationAdminGroups"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAuthorizationAdminGroups",
    jsii_struct_bases=[],
    name_mapping={"group": "group"},
)
class ContainerAzureClusterAuthorizationAdminGroups:
    def __init__(self, *, group: builtins.str) -> None:
        '''
        :param group: The name of the group, e.g. ``my-group@domain.com``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#group ContainerAzureCluster#group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f0f609ad298c1ddd8b2f2e38dc827c1a07aaa7a3919a637159b69dc1e5692e)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
        }

    @builtins.property
    def group(self) -> builtins.str:
        '''The name of the group, e.g. ``my-group@domain.com``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#group ContainerAzureCluster#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterAuthorizationAdminGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterAuthorizationAdminGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAuthorizationAdminGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77fad1660610c5b58265c6c72df128c6b27ec9e506fe1575d87757d206e03662)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAzureClusterAuthorizationAdminGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053bc2293f35df004a6941792e22a516d47090018eb8f318a159f5398c3ba677)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAzureClusterAuthorizationAdminGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe967e8ed0527b6115c6212ba764bfc0d183aec794fd3c60b4d6c6aad890a4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d468067d38788851a0dfb13aa486287a83642587382517c76b4461c8000edb8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__180533a86109a3a72cbbad5d9a6f4601361498b6ea368c45396725408bcf646c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38939bb2897484a3a8baab3e8888090b5bee73cf1e3721b427c01707a5f8d2fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAzureClusterAuthorizationAdminGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAuthorizationAdminGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d7af2b8917f83334f2621088dead0811ac736eb36a848fd911d166a6434dd30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="groupInput")
    def group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupInput"))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "group"))

    @group.setter
    def group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991f7ae8d664a808dfe6374738230f3451005adf866ccc2dbc99019cd31043df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterAuthorizationAdminGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterAuthorizationAdminGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterAuthorizationAdminGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e2f8b588c98c00ead68731523b475f8be84227f5e2a696bb564707a4f798c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class ContainerAzureClusterAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. ``my-gcp-id@gmail.com``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#username ContainerAzureCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c44bffb63e1700fc95fcbc408d05a274044bfbb27c54a2c225c04ced0753c2)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. ``my-gcp-id@gmail.com``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#username ContainerAzureCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58d84dc5f2ae4123c2ff7b87c4bbb2d357adfb0667a295f7903b810da213af45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAzureClusterAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f245bff281b4105db302a8244a1124ed1c4182eba457b205a4e3625a595d2b22)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAzureClusterAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8050590e14d2e98c0b6126ee08fa98bf06b25054fb4ab1121b8c91ad35c02124)
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
            type_hints = typing.get_type_hints(_typecheckingstub__642a490b64317e19fa8eccdda512a8eb30b4d3d469565d340f9a9c00190bcf15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a85958a93e109dc57961b9d0be847a09a1ff0f73d60874a424407c0de2b2e3dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6d5acd944c81c45e21f16d8b78b5fb5483d59580aac70160307b65a67c8dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAzureClusterAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36df4ed242f3f202b8f00048b682a3c210e74784fb3ba3152ffd8fdd98e26e06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203355fddc7a70a2647477c76490b8fc4a8d9f5c1b82455ab6deb9ffff00d6bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0968af88984f524898b33dd0800c5c8596c3484fdd87079cba20918c064b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAzureClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c079a591d9f9194b5bb4ce25245ab79b97368a16bd7cc93131ad5cdb680b5d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminGroups")
    def put_admin_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAzureClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d6663d20dc7284b9cff89987da3a4748d530e8c012780acf5459e687b3bb1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminGroups", [value]))

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAzureClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217298e53d55f2512586333fa7e3071a1f4ed832fb5b8e2e386b77340b2b494c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @jsii.member(jsii_name="resetAdminGroups")
    def reset_admin_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminGroups", []))

    @builtins.property
    @jsii.member(jsii_name="adminGroups")
    def admin_groups(self) -> ContainerAzureClusterAuthorizationAdminGroupsList:
        return typing.cast(ContainerAzureClusterAuthorizationAdminGroupsList, jsii.get(self, "adminGroups"))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> ContainerAzureClusterAuthorizationAdminUsersList:
        return typing.cast(ContainerAzureClusterAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminGroupsInput")
    def admin_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminGroups]]], jsii.get(self, "adminGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureClusterAuthorization]:
        return typing.cast(typing.Optional[ContainerAzureClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38cbd07344bafa0e4572b548c5ed66b38e0cbf8a13ebafb283b233208e84a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAzureServicesAuthentication",
    jsii_struct_bases=[],
    name_mapping={"application_id": "applicationId", "tenant_id": "tenantId"},
)
class ContainerAzureClusterAzureServicesAuthentication:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param application_id: The Azure Active Directory Application ID for Authentication configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#application_id ContainerAzureCluster#application_id}
        :param tenant_id: The Azure Active Directory Tenant ID for Authentication configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#tenant_id ContainerAzureCluster#tenant_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38868def03206a5f573a2a5ec72d10e0e3210a236f83f87e156e049283f9ba86)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "tenant_id": tenant_id,
        }

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The Azure Active Directory Application ID for Authentication configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#application_id ContainerAzureCluster#application_id}
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''The Azure Active Directory Tenant ID for Authentication configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#tenant_id ContainerAzureCluster#tenant_id}
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterAzureServicesAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterAzureServicesAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterAzureServicesAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81f53d9e844a3711df1456f2a923baac24688ee62cff31d9e71479c2fdb92a7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="applicationIdInput")
    def application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149f4be564d00eb92e4821c01cf566f0254382b28b97e98b55c54cb87417b0a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a890094840ae7b5796e19467bbaf9a2ffa60cfdb47d8af94358908c2ae9f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureClusterAzureServicesAuthentication]:
        return typing.cast(typing.Optional[ContainerAzureClusterAzureServicesAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterAzureServicesAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f414ce57f5d4e14fa1916bb68a76371704272b1f4970b60a2432e522a1a4f07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "authorization": "authorization",
        "azure_region": "azureRegion",
        "control_plane": "controlPlane",
        "fleet": "fleet",
        "location": "location",
        "name": "name",
        "networking": "networking",
        "resource_group_id": "resourceGroupId",
        "annotations": "annotations",
        "azure_services_authentication": "azureServicesAuthentication",
        "client": "client",
        "description": "description",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ContainerAzureClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization: typing.Union[ContainerAzureClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
        azure_region: builtins.str,
        control_plane: typing.Union["ContainerAzureClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["ContainerAzureClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["ContainerAzureClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        resource_group_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        azure_services_authentication: typing.Optional[typing.Union[ContainerAzureClusterAzureServicesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAzureClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#authorization ContainerAzureCluster#authorization}
        :param azure_region: The Azure region where the cluster runs. Each Google Cloud region supports a subset of nearby Azure regions. You can call to list all supported Azure regions within a given Google Cloud region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#azure_region ContainerAzureCluster#azure_region}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#control_plane ContainerAzureCluster#control_plane}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#fleet ContainerAzureCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#location ContainerAzureCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#name ContainerAzureCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#networking ContainerAzureCluster#networking}
        :param resource_group_id: The ARM ID of the resource group where the cluster resources are deployed. For example: ``/subscriptions/* /resourceGroups/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#resource_group_id ContainerAzureCluster#resource_group_id} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Keys can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#annotations ContainerAzureCluster#annotations}
        :param azure_services_authentication: azure_services_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#azure_services_authentication ContainerAzureCluster#azure_services_authentication}
        :param client: Name of the AzureClient. The ``AzureClient`` resource must reside on the same GCP project and region as the ``AzureCluster``. ``AzureClient`` names are formatted as ``projects/<project-number>/locations/<region>/azureClients/<client-id>``. See Resource Names (https:cloud.google.com/apis/design/resource_names) for more details on Google Cloud resource names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#client ContainerAzureCluster#client}
        :param description: Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#description ContainerAzureCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#id ContainerAzureCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#project ContainerAzureCluster#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#timeouts ContainerAzureCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authorization, dict):
            authorization = ContainerAzureClusterAuthorization(**authorization)
        if isinstance(control_plane, dict):
            control_plane = ContainerAzureClusterControlPlane(**control_plane)
        if isinstance(fleet, dict):
            fleet = ContainerAzureClusterFleet(**fleet)
        if isinstance(networking, dict):
            networking = ContainerAzureClusterNetworking(**networking)
        if isinstance(azure_services_authentication, dict):
            azure_services_authentication = ContainerAzureClusterAzureServicesAuthentication(**azure_services_authentication)
        if isinstance(timeouts, dict):
            timeouts = ContainerAzureClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfd85a19224ad97387a1faf5b22ca112ee9fdc0bc47a5b46a0c5e336359a38d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument azure_region", value=azure_region, expected_type=type_hints["azure_region"])
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument fleet", value=fleet, expected_type=type_hints["fleet"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument networking", value=networking, expected_type=type_hints["networking"])
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument azure_services_authentication", value=azure_services_authentication, expected_type=type_hints["azure_services_authentication"])
            check_type(argname="argument client", value=client, expected_type=type_hints["client"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization": authorization,
            "azure_region": azure_region,
            "control_plane": control_plane,
            "fleet": fleet,
            "location": location,
            "name": name,
            "networking": networking,
            "resource_group_id": resource_group_id,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if azure_services_authentication is not None:
            self._values["azure_services_authentication"] = azure_services_authentication
        if client is not None:
            self._values["client"] = client
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
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
    def authorization(self) -> ContainerAzureClusterAuthorization:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#authorization ContainerAzureCluster#authorization}
        '''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(ContainerAzureClusterAuthorization, result)

    @builtins.property
    def azure_region(self) -> builtins.str:
        '''The Azure region where the cluster runs.

        Each Google Cloud region supports a subset of nearby Azure regions. You can call to list all supported Azure regions within a given Google Cloud region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#azure_region ContainerAzureCluster#azure_region}
        '''
        result = self._values.get("azure_region")
        assert result is not None, "Required property 'azure_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane(self) -> "ContainerAzureClusterControlPlane":
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#control_plane ContainerAzureCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        assert result is not None, "Required property 'control_plane' is missing"
        return typing.cast("ContainerAzureClusterControlPlane", result)

    @builtins.property
    def fleet(self) -> "ContainerAzureClusterFleet":
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#fleet ContainerAzureCluster#fleet}
        '''
        result = self._values.get("fleet")
        assert result is not None, "Required property 'fleet' is missing"
        return typing.cast("ContainerAzureClusterFleet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#location ContainerAzureCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#name ContainerAzureCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def networking(self) -> "ContainerAzureClusterNetworking":
        '''networking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#networking ContainerAzureCluster#networking}
        '''
        result = self._values.get("networking")
        assert result is not None, "Required property 'networking' is missing"
        return typing.cast("ContainerAzureClusterNetworking", result)

    @builtins.property
    def resource_group_id(self) -> builtins.str:
        '''The ARM ID of the resource group where the cluster resources are deployed. For example: ``/subscriptions/* /resourceGroups/*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#resource_group_id ContainerAzureCluster#resource_group_id}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("resource_group_id")
        assert result is not None, "Required property 'resource_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Keys can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field ``effective_annotations`` for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#annotations ContainerAzureCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def azure_services_authentication(
        self,
    ) -> typing.Optional[ContainerAzureClusterAzureServicesAuthentication]:
        '''azure_services_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#azure_services_authentication ContainerAzureCluster#azure_services_authentication}
        '''
        result = self._values.get("azure_services_authentication")
        return typing.cast(typing.Optional[ContainerAzureClusterAzureServicesAuthentication], result)

    @builtins.property
    def client(self) -> typing.Optional[builtins.str]:
        '''Name of the AzureClient.

        The ``AzureClient`` resource must reside on the same GCP project and region as the ``AzureCluster``. ``AzureClient`` names are formatted as ``projects/<project-number>/locations/<region>/azureClients/<client-id>``. See Resource Names (https:cloud.google.com/apis/design/resource_names) for more details on Google Cloud resource names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#client ContainerAzureCluster#client}
        '''
        result = self._values.get("client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#description ContainerAzureCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#id ContainerAzureCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#project ContainerAzureCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAzureClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#timeouts ContainerAzureCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAzureClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={
        "ssh_config": "sshConfig",
        "subnet_id": "subnetId",
        "version": "version",
        "database_encryption": "databaseEncryption",
        "main_volume": "mainVolume",
        "proxy_config": "proxyConfig",
        "replica_placements": "replicaPlacements",
        "root_volume": "rootVolume",
        "tags": "tags",
        "vm_size": "vmSize",
    },
)
class ContainerAzureClusterControlPlane:
    def __init__(
        self,
        *,
        ssh_config: typing.Union["ContainerAzureClusterControlPlaneSshConfig", typing.Dict[builtins.str, typing.Any]],
        subnet_id: builtins.str,
        version: builtins.str,
        database_encryption: typing.Optional[typing.Union["ContainerAzureClusterControlPlaneDatabaseEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        main_volume: typing.Optional[typing.Union["ContainerAzureClusterControlPlaneMainVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAzureClusterControlPlaneProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        replica_placements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAzureClusterControlPlaneReplicaPlacements", typing.Dict[builtins.str, typing.Any]]]]] = None,
        root_volume: typing.Optional[typing.Union["ContainerAzureClusterControlPlaneRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vm_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#ssh_config ContainerAzureCluster#ssh_config}
        :param subnet_id: The ARM ID of the subnet where the control plane VMs are deployed. Example: ``/subscriptions//resourceGroups//providers/Microsoft.Network/virtualNetworks//subnets/default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#subnet_id ContainerAzureCluster#subnet_id}
        :param version: The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAzureServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#version ContainerAzureCluster#version}
        :param database_encryption: database_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#database_encryption ContainerAzureCluster#database_encryption}
        :param main_volume: main_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#main_volume ContainerAzureCluster#main_volume}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#proxy_config ContainerAzureCluster#proxy_config}
        :param replica_placements: replica_placements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#replica_placements ContainerAzureCluster#replica_placements}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#root_volume ContainerAzureCluster#root_volume}
        :param tags: Optional. A set of tags to apply to all underlying control plane Azure resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#tags ContainerAzureCluster#tags}
        :param vm_size: Optional. The Azure VM size name. Example: ``Standard_DS2_v2``. For available VM sizes, see https://docs.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions. When unspecified, it defaults to ``Standard_DS2_v2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#vm_size ContainerAzureCluster#vm_size}
        '''
        if isinstance(ssh_config, dict):
            ssh_config = ContainerAzureClusterControlPlaneSshConfig(**ssh_config)
        if isinstance(database_encryption, dict):
            database_encryption = ContainerAzureClusterControlPlaneDatabaseEncryption(**database_encryption)
        if isinstance(main_volume, dict):
            main_volume = ContainerAzureClusterControlPlaneMainVolume(**main_volume)
        if isinstance(proxy_config, dict):
            proxy_config = ContainerAzureClusterControlPlaneProxyConfig(**proxy_config)
        if isinstance(root_volume, dict):
            root_volume = ContainerAzureClusterControlPlaneRootVolume(**root_volume)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6905c14dd4962a4798e242ea774b0fc8c353343430cb8088d487956765751835)
            check_type(argname="argument ssh_config", value=ssh_config, expected_type=type_hints["ssh_config"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument database_encryption", value=database_encryption, expected_type=type_hints["database_encryption"])
            check_type(argname="argument main_volume", value=main_volume, expected_type=type_hints["main_volume"])
            check_type(argname="argument proxy_config", value=proxy_config, expected_type=type_hints["proxy_config"])
            check_type(argname="argument replica_placements", value=replica_placements, expected_type=type_hints["replica_placements"])
            check_type(argname="argument root_volume", value=root_volume, expected_type=type_hints["root_volume"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vm_size", value=vm_size, expected_type=type_hints["vm_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ssh_config": ssh_config,
            "subnet_id": subnet_id,
            "version": version,
        }
        if database_encryption is not None:
            self._values["database_encryption"] = database_encryption
        if main_volume is not None:
            self._values["main_volume"] = main_volume
        if proxy_config is not None:
            self._values["proxy_config"] = proxy_config
        if replica_placements is not None:
            self._values["replica_placements"] = replica_placements
        if root_volume is not None:
            self._values["root_volume"] = root_volume
        if tags is not None:
            self._values["tags"] = tags
        if vm_size is not None:
            self._values["vm_size"] = vm_size

    @builtins.property
    def ssh_config(self) -> "ContainerAzureClusterControlPlaneSshConfig":
        '''ssh_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#ssh_config ContainerAzureCluster#ssh_config}
        '''
        result = self._values.get("ssh_config")
        assert result is not None, "Required property 'ssh_config' is missing"
        return typing.cast("ContainerAzureClusterControlPlaneSshConfig", result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The ARM ID of the subnet where the control plane VMs are deployed. Example: ``/subscriptions//resourceGroups//providers/Microsoft.Network/virtualNetworks//subnets/default``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#subnet_id ContainerAzureCluster#subnet_id}
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAzureServerConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#version ContainerAzureCluster#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_encryption(
        self,
    ) -> typing.Optional["ContainerAzureClusterControlPlaneDatabaseEncryption"]:
        '''database_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#database_encryption ContainerAzureCluster#database_encryption}
        '''
        result = self._values.get("database_encryption")
        return typing.cast(typing.Optional["ContainerAzureClusterControlPlaneDatabaseEncryption"], result)

    @builtins.property
    def main_volume(
        self,
    ) -> typing.Optional["ContainerAzureClusterControlPlaneMainVolume"]:
        '''main_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#main_volume ContainerAzureCluster#main_volume}
        '''
        result = self._values.get("main_volume")
        return typing.cast(typing.Optional["ContainerAzureClusterControlPlaneMainVolume"], result)

    @builtins.property
    def proxy_config(
        self,
    ) -> typing.Optional["ContainerAzureClusterControlPlaneProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#proxy_config ContainerAzureCluster#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["ContainerAzureClusterControlPlaneProxyConfig"], result)

    @builtins.property
    def replica_placements(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAzureClusterControlPlaneReplicaPlacements"]]]:
        '''replica_placements block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#replica_placements ContainerAzureCluster#replica_placements}
        '''
        result = self._values.get("replica_placements")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAzureClusterControlPlaneReplicaPlacements"]]], result)

    @builtins.property
    def root_volume(
        self,
    ) -> typing.Optional["ContainerAzureClusterControlPlaneRootVolume"]:
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#root_volume ContainerAzureCluster#root_volume}
        '''
        result = self._values.get("root_volume")
        return typing.cast(typing.Optional["ContainerAzureClusterControlPlaneRootVolume"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. A set of tags to apply to all underlying control plane Azure resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#tags ContainerAzureCluster#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vm_size(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Azure VM size name. Example: ``Standard_DS2_v2``. For available VM sizes, see https://docs.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions. When unspecified, it defaults to ``Standard_DS2_v2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#vm_size ContainerAzureCluster#vm_size}
        '''
        result = self._values.get("vm_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneDatabaseEncryption",
    jsii_struct_bases=[],
    name_mapping={"key_id": "keyId"},
)
class ContainerAzureClusterControlPlaneDatabaseEncryption:
    def __init__(self, *, key_id: builtins.str) -> None:
        '''
        :param key_id: The ARM ID of the Azure Key Vault key to encrypt / decrypt data. For example: ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.KeyVault/vaults/<key-vault-id>/keys/<key-name>`` Encryption will always take the latest version of the key and hence specific version is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#key_id ContainerAzureCluster#key_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08d91a7d90add13946128c6bdda801c1600095cb433b355630e500d74aa014f4)
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_id": key_id,
        }

    @builtins.property
    def key_id(self) -> builtins.str:
        '''The ARM ID of the Azure Key Vault key to encrypt / decrypt data.

        For example: ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.KeyVault/vaults/<key-vault-id>/keys/<key-name>`` Encryption will always take the latest version of the key and hence specific version is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#key_id ContainerAzureCluster#key_id}
        '''
        result = self._values.get("key_id")
        assert result is not None, "Required property 'key_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterControlPlaneDatabaseEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a35ffdd41735d05f0f9e45fe6e6f3eee99825c8b8394661ffa5412c46331948)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyIdInput")
    def key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2443dfd6f4a3fdcd5b6545693f293063d240141154e6073af61c389f27583989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureClusterControlPlaneDatabaseEncryption]:
        return typing.cast(typing.Optional[ContainerAzureClusterControlPlaneDatabaseEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterControlPlaneDatabaseEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fcb25b566f794a2e792be0f700d965069f1e9a1890a10945c9e0bb223d2a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneMainVolume",
    jsii_struct_bases=[],
    name_mapping={"size_gib": "sizeGib"},
)
class ContainerAzureClusterControlPlaneMainVolume:
    def __init__(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#size_gib ContainerAzureCluster#size_gib}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1c1d3c32b8e3d98ffea5b81fa58e4352c75af3674e88e3dd68eabb03b6041a)
            check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size_gib is not None:
            self._values["size_gib"] = size_gib

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#size_gib ContainerAzureCluster#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterControlPlaneMainVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterControlPlaneMainVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneMainVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dcad2b5266831d6de9689cc5a686fbb664cceab621fab16a123e16c7611b254)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSizeGib")
    def reset_size_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeGib", []))

    @builtins.property
    @jsii.member(jsii_name="sizeGibInput")
    def size_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGibInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed471944ab2a6acc72a433670acf07f0b62110185e7ca51e078c52579245bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureClusterControlPlaneMainVolume]:
        return typing.cast(typing.Optional[ContainerAzureClusterControlPlaneMainVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterControlPlaneMainVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4803ab17cd59a16246e74de0cdb8ef7d0f6c765d12e4da407ad4f13b8ca32b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAzureClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cf88a251e43ccea5910aa677e8c6c430a8f189ade4c09f364ac5e51bcbfcaa4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatabaseEncryption")
    def put_database_encryption(self, *, key_id: builtins.str) -> None:
        '''
        :param key_id: The ARM ID of the Azure Key Vault key to encrypt / decrypt data. For example: ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.KeyVault/vaults/<key-vault-id>/keys/<key-name>`` Encryption will always take the latest version of the key and hence specific version is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#key_id ContainerAzureCluster#key_id}
        '''
        value = ContainerAzureClusterControlPlaneDatabaseEncryption(key_id=key_id)

        return typing.cast(None, jsii.invoke(self, "putDatabaseEncryption", [value]))

    @jsii.member(jsii_name="putMainVolume")
    def put_main_volume(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#size_gib ContainerAzureCluster#size_gib}
        '''
        value = ContainerAzureClusterControlPlaneMainVolume(size_gib=size_gib)

        return typing.cast(None, jsii.invoke(self, "putMainVolume", [value]))

    @jsii.member(jsii_name="putProxyConfig")
    def put_proxy_config(
        self,
        *,
        resource_group_id: builtins.str,
        secret_id: builtins.str,
    ) -> None:
        '''
        :param resource_group_id: The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#resource_group_id ContainerAzureCluster#resource_group_id}
        :param secret_id: The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#secret_id ContainerAzureCluster#secret_id}
        '''
        value = ContainerAzureClusterControlPlaneProxyConfig(
            resource_group_id=resource_group_id, secret_id=secret_id
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfig", [value]))

    @jsii.member(jsii_name="putReplicaPlacements")
    def put_replica_placements(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAzureClusterControlPlaneReplicaPlacements", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389ad5488e7bca1149ca8881178f7f71f9755c55e0f7a6eb55b6f8bc110029fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReplicaPlacements", [value]))

    @jsii.member(jsii_name="putRootVolume")
    def put_root_volume(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#size_gib ContainerAzureCluster#size_gib}
        '''
        value = ContainerAzureClusterControlPlaneRootVolume(size_gib=size_gib)

        return typing.cast(None, jsii.invoke(self, "putRootVolume", [value]))

    @jsii.member(jsii_name="putSshConfig")
    def put_ssh_config(self, *, authorized_key: builtins.str) -> None:
        '''
        :param authorized_key: The SSH public key data for VMs managed by Anthos. This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#authorized_key ContainerAzureCluster#authorized_key}
        '''
        value = ContainerAzureClusterControlPlaneSshConfig(
            authorized_key=authorized_key
        )

        return typing.cast(None, jsii.invoke(self, "putSshConfig", [value]))

    @jsii.member(jsii_name="resetDatabaseEncryption")
    def reset_database_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseEncryption", []))

    @jsii.member(jsii_name="resetMainVolume")
    def reset_main_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainVolume", []))

    @jsii.member(jsii_name="resetProxyConfig")
    def reset_proxy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyConfig", []))

    @jsii.member(jsii_name="resetReplicaPlacements")
    def reset_replica_placements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicaPlacements", []))

    @jsii.member(jsii_name="resetRootVolume")
    def reset_root_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootVolume", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVmSize")
    def reset_vm_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVmSize", []))

    @builtins.property
    @jsii.member(jsii_name="databaseEncryption")
    def database_encryption(
        self,
    ) -> ContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference:
        return typing.cast(ContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference, jsii.get(self, "databaseEncryption"))

    @builtins.property
    @jsii.member(jsii_name="mainVolume")
    def main_volume(self) -> ContainerAzureClusterControlPlaneMainVolumeOutputReference:
        return typing.cast(ContainerAzureClusterControlPlaneMainVolumeOutputReference, jsii.get(self, "mainVolume"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(
        self,
    ) -> "ContainerAzureClusterControlPlaneProxyConfigOutputReference":
        return typing.cast("ContainerAzureClusterControlPlaneProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="replicaPlacements")
    def replica_placements(
        self,
    ) -> "ContainerAzureClusterControlPlaneReplicaPlacementsList":
        return typing.cast("ContainerAzureClusterControlPlaneReplicaPlacementsList", jsii.get(self, "replicaPlacements"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(
        self,
    ) -> "ContainerAzureClusterControlPlaneRootVolumeOutputReference":
        return typing.cast("ContainerAzureClusterControlPlaneRootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="sshConfig")
    def ssh_config(self) -> "ContainerAzureClusterControlPlaneSshConfigOutputReference":
        return typing.cast("ContainerAzureClusterControlPlaneSshConfigOutputReference", jsii.get(self, "sshConfig"))

    @builtins.property
    @jsii.member(jsii_name="databaseEncryptionInput")
    def database_encryption_input(
        self,
    ) -> typing.Optional[ContainerAzureClusterControlPlaneDatabaseEncryption]:
        return typing.cast(typing.Optional[ContainerAzureClusterControlPlaneDatabaseEncryption], jsii.get(self, "databaseEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="mainVolumeInput")
    def main_volume_input(
        self,
    ) -> typing.Optional[ContainerAzureClusterControlPlaneMainVolume]:
        return typing.cast(typing.Optional[ContainerAzureClusterControlPlaneMainVolume], jsii.get(self, "mainVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfigInput")
    def proxy_config_input(
        self,
    ) -> typing.Optional["ContainerAzureClusterControlPlaneProxyConfig"]:
        return typing.cast(typing.Optional["ContainerAzureClusterControlPlaneProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaPlacementsInput")
    def replica_placements_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAzureClusterControlPlaneReplicaPlacements"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAzureClusterControlPlaneReplicaPlacements"]]], jsii.get(self, "replicaPlacementsInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(
        self,
    ) -> typing.Optional["ContainerAzureClusterControlPlaneRootVolume"]:
        return typing.cast(typing.Optional["ContainerAzureClusterControlPlaneRootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="sshConfigInput")
    def ssh_config_input(
        self,
    ) -> typing.Optional["ContainerAzureClusterControlPlaneSshConfig"]:
        return typing.cast(typing.Optional["ContainerAzureClusterControlPlaneSshConfig"], jsii.get(self, "sshConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="vmSizeInput")
    def vm_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21b7aaf0272f6722a17354c127f64b1fb73f27ea6d8fa9966c26f0ca8d442bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2bb476ba4d10dff0f1804a63ab8e55e2ddcfe5664ed7269efd09e424b014e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3713440fcc67a5b570ae35ccb390032ed8aa4f7112fb1ad38fa83a467a54c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643694f5aadf6c19dc846f95d00f92ca8bf51ad0b1d772986d301f2e392396f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureClusterControlPlane]:
        return typing.cast(typing.Optional[ContainerAzureClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ed883e08ef88db105956601551688a393fda4d16e7d3f36a95410e4798ce68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"resource_group_id": "resourceGroupId", "secret_id": "secretId"},
)
class ContainerAzureClusterControlPlaneProxyConfig:
    def __init__(
        self,
        *,
        resource_group_id: builtins.str,
        secret_id: builtins.str,
    ) -> None:
        '''
        :param resource_group_id: The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#resource_group_id ContainerAzureCluster#resource_group_id}
        :param secret_id: The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#secret_id ContainerAzureCluster#secret_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c28bf6889b5137faf47c755b1a8d62c3a11a4269a4114debcbc36c04fe9798)
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_group_id": resource_group_id,
            "secret_id": secret_id,
        }

    @builtins.property
    def resource_group_id(self) -> builtins.str:
        '''The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#resource_group_id ContainerAzureCluster#resource_group_id}
        '''
        result = self._values.get("resource_group_id")
        assert result is not None, "Required property 'resource_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#secret_id ContainerAzureCluster#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterControlPlaneProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterControlPlaneProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7049b1c60c65dd5887049c68756890e594010bd12e30b6ca601486ebe3ddfb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceGroupIdInput")
    def resource_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretIdInput")
    def secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupId"))

    @resource_group_id.setter
    def resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836e4e9ba91a02a1f173431acd0d81b872202c5a99de2ded97dec0b37122dfc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce22d5dba3d7db693b78bdd19716267dfc30c735f7b3ac297593adb640c52878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureClusterControlPlaneProxyConfig]:
        return typing.cast(typing.Optional[ContainerAzureClusterControlPlaneProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterControlPlaneProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3df71362b49e03e1918c215aa379930a383757695aa74a53fa2c623c9a20e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneReplicaPlacements",
    jsii_struct_bases=[],
    name_mapping={
        "azure_availability_zone": "azureAvailabilityZone",
        "subnet_id": "subnetId",
    },
)
class ContainerAzureClusterControlPlaneReplicaPlacements:
    def __init__(
        self,
        *,
        azure_availability_zone: builtins.str,
        subnet_id: builtins.str,
    ) -> None:
        '''
        :param azure_availability_zone: For a given replica, the Azure availability zone where to provision the control plane VM and the ETCD disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#azure_availability_zone ContainerAzureCluster#azure_availability_zone}
        :param subnet_id: For a given replica, the ARM ID of the subnet where the control plane VM is deployed. Make sure it's a subnet under the virtual network in the cluster configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#subnet_id ContainerAzureCluster#subnet_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84c623ca9c1ac4809e720fd642eb83ba853e7ce59da2f9c707e9ad651ccf413)
            check_type(argname="argument azure_availability_zone", value=azure_availability_zone, expected_type=type_hints["azure_availability_zone"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "azure_availability_zone": azure_availability_zone,
            "subnet_id": subnet_id,
        }

    @builtins.property
    def azure_availability_zone(self) -> builtins.str:
        '''For a given replica, the Azure availability zone where to provision the control plane VM and the ETCD disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#azure_availability_zone ContainerAzureCluster#azure_availability_zone}
        '''
        result = self._values.get("azure_availability_zone")
        assert result is not None, "Required property 'azure_availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''For a given replica, the ARM ID of the subnet where the control plane VM is deployed.

        Make sure it's a subnet under the virtual network in the cluster configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#subnet_id ContainerAzureCluster#subnet_id}
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterControlPlaneReplicaPlacements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterControlPlaneReplicaPlacementsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneReplicaPlacementsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0252f2e64dc923feed5500f1b02b3630b0b357f87812dc172c3ddf42aba1cda7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAzureClusterControlPlaneReplicaPlacementsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77438495b31b89e003b25abec6d4600d2967a3fdd81d81cdbfabde878fa88e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAzureClusterControlPlaneReplicaPlacementsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3016589485e74941712c12cb36a7ac048984a7101e064a3595a3cb05aa026675)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a60354151d87308f2a9100588371e94ef2e620068ffc09b3ed5da52308a7187)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1db1a31aec47aaf2348c620b92c7732fae990fcc8d7896e0feaf50e115433bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterControlPlaneReplicaPlacements]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterControlPlaneReplicaPlacements]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterControlPlaneReplicaPlacements]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46f9e153930cf46be7437181353c7001752e5c5087fb21ca7685f7c5e5e636a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAzureClusterControlPlaneReplicaPlacementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneReplicaPlacementsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46a8a46b44074286558474524f29f7dcc61010c7a733432b1415966226131582)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="azureAvailabilityZoneInput")
    def azure_availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureAvailabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="azureAvailabilityZone")
    def azure_availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureAvailabilityZone"))

    @azure_availability_zone.setter
    def azure_availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc1ec03f8c1e54cedcfd45478c801317ba3b861dab26ce8e23a00e103e0a71a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureAvailabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e601525223ae6a9da9ec949c89a4d16ca75dd2ee59acd4c97c5f4699622fd096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterControlPlaneReplicaPlacements]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterControlPlaneReplicaPlacements]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterControlPlaneReplicaPlacements]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586e6343ac670a677062ab6d40f851158f956ecd6b1d5d4dcb4a451153e99c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneRootVolume",
    jsii_struct_bases=[],
    name_mapping={"size_gib": "sizeGib"},
)
class ContainerAzureClusterControlPlaneRootVolume:
    def __init__(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#size_gib ContainerAzureCluster#size_gib}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0d896115bd7ccd9fc4e79260b3a120b41175cd0ac253efeea4232f91eb26c4)
            check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size_gib is not None:
            self._values["size_gib"] = size_gib

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#size_gib ContainerAzureCluster#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterControlPlaneRootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterControlPlaneRootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneRootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b59f5f49355f5c8fc1788a086c8d9553f7e4bb918559878e042138a4c1af3cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSizeGib")
    def reset_size_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeGib", []))

    @builtins.property
    @jsii.member(jsii_name="sizeGibInput")
    def size_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGibInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28dffcf21d423382f2c8961d9b462c075c54d789f3030da2d6e25065aadb9099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureClusterControlPlaneRootVolume]:
        return typing.cast(typing.Optional[ContainerAzureClusterControlPlaneRootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterControlPlaneRootVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0593004eec3ff297883798e67bab2b225c95b710fbfd5d5bc8c0eba450efcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneSshConfig",
    jsii_struct_bases=[],
    name_mapping={"authorized_key": "authorizedKey"},
)
class ContainerAzureClusterControlPlaneSshConfig:
    def __init__(self, *, authorized_key: builtins.str) -> None:
        '''
        :param authorized_key: The SSH public key data for VMs managed by Anthos. This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#authorized_key ContainerAzureCluster#authorized_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e4ec456ed6a8b3f6cd3a77ba923ce40260ecf11b3c68b4a45a691243dec55e)
            check_type(argname="argument authorized_key", value=authorized_key, expected_type=type_hints["authorized_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorized_key": authorized_key,
        }

    @builtins.property
    def authorized_key(self) -> builtins.str:
        '''The SSH public key data for VMs managed by Anthos.

        This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#authorized_key ContainerAzureCluster#authorized_key}
        '''
        result = self._values.get("authorized_key")
        assert result is not None, "Required property 'authorized_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterControlPlaneSshConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterControlPlaneSshConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterControlPlaneSshConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4fe3ba0e86c1613d8b5b0d2ad6eef29823823a3a12f7cf09c4e71c4652b4fa0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="authorizedKeyInput")
    def authorized_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedKey")
    def authorized_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizedKey"))

    @authorized_key.setter
    def authorized_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8fa0a269589c3beda358bc83dd68966377d4b8a7a712cf690b95e1a568e284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureClusterControlPlaneSshConfig]:
        return typing.cast(typing.Optional[ContainerAzureClusterControlPlaneSshConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterControlPlaneSshConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052ea01e1717123735b8ade8a474d4f185a694c40b7cbd13bb1cdcfc67f6a0ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterFleet",
    jsii_struct_bases=[],
    name_mapping={"project": "project"},
)
class ContainerAzureClusterFleet:
    def __init__(self, *, project: typing.Optional[builtins.str] = None) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#project ContainerAzureCluster#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873dcd3f787cd3f6ad1bdadbf9bbdc918929286ddf294933dcac93e853a82808)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The number of the Fleet host project where this cluster will be registered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#project ContainerAzureCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dee0c8f0baf2df0288eca0e13e5522cca02bb558aeff96323cd199c830d70ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce04ad79ac1cd804a8b552b6c4582b269d1ab7b30235d68cd58895cb06888ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureClusterFleet]:
        return typing.cast(typing.Optional[ContainerAzureClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bedaedd28386a089a80a03b901abe6cfbab430890d01382481d41ae27c1d5a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterNetworking",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
        "virtual_network_id": "virtualNetworkId",
    },
)
class ContainerAzureClusterNetworking:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: The IP address range of the pods in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All pods in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#pod_address_cidr_blocks ContainerAzureCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: The IP address range for services in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All services in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creating a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#service_address_cidr_blocks ContainerAzureCluster#service_address_cidr_blocks}
        :param virtual_network_id: The Azure Resource Manager (ARM) ID of the VNet associated with your cluster. All components in the cluster (i.e. control plane and node pools) run on a single VNet. Example: ``/subscriptions/* /resourceGroups/* /providers/Microsoft.Network/virtualNetworks/*`` This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#virtual_network_id ContainerAzureCluster#virtual_network_id} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9441b83486675d1fd70ac0a05a2b267f64a921318dae14d4cf8671f21f2663c)
            check_type(argname="argument pod_address_cidr_blocks", value=pod_address_cidr_blocks, expected_type=type_hints["pod_address_cidr_blocks"])
            check_type(argname="argument service_address_cidr_blocks", value=service_address_cidr_blocks, expected_type=type_hints["service_address_cidr_blocks"])
            check_type(argname="argument virtual_network_id", value=virtual_network_id, expected_type=type_hints["virtual_network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pod_address_cidr_blocks": pod_address_cidr_blocks,
            "service_address_cidr_blocks": service_address_cidr_blocks,
            "virtual_network_id": virtual_network_id,
        }

    @builtins.property
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''The IP address range of the pods in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All pods in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#pod_address_cidr_blocks ContainerAzureCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''The IP address range for services in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All services in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creating a cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#service_address_cidr_blocks ContainerAzureCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''The Azure Resource Manager (ARM) ID of the VNet associated with your cluster.

        All components in the cluster (i.e. control plane and node pools) run on a single VNet. Example: ``/subscriptions/* /resourceGroups/* /providers/Microsoft.Network/virtualNetworks/*`` This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#virtual_network_id ContainerAzureCluster#virtual_network_id}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("virtual_network_id")
        assert result is not None, "Required property 'virtual_network_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterNetworking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterNetworkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterNetworkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72207d86d46d3b6f645d0cfc9e062ebce6ae93e8b4a1031dfcd5d98cd26a68c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="podAddressCidrBlocksInput")
    def pod_address_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "podAddressCidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocksInput")
    def service_address_cidr_blocks_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serviceAddressCidrBlocksInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkIdInput")
    def virtual_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="podAddressCidrBlocks")
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "podAddressCidrBlocks"))

    @pod_address_cidr_blocks.setter
    def pod_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4243786c64c2de68dc50815589c2c4097723e7bf9d21726a00734ee0bdb432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c603be8d4fb0739ceb04cec30f6b6247aa90ef1a1663d82afc0d0a111cffbce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bd4bf29ba15901c497c43f608d2ea56555d833d2d7bb088cad653187b8a972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAzureClusterNetworking]:
        return typing.cast(typing.Optional[ContainerAzureClusterNetworking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterNetworking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce982061ddb61e3e80dca25988d5751c7eb14fca4bd476aa75b42a2cfb69ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerAzureClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#create ContainerAzureCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#delete ContainerAzureCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#update ContainerAzureCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc341d92141a47526f3aaf30b88b0d5eca0c4a9b25844ba1d9a26a0c14109752)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#create ContainerAzureCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#delete ContainerAzureCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_azure_cluster#update ContainerAzureCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e763e03719186e578cfb8fea6e86c9698bbae1dfb08188651f0fc16590bb39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f89041c1595516e2aaf7df5a08417fdc353375ae8035040d79eac7b78c1e146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f683170cbed920f34de31ce32b5e7c9699c5d647820eb72057429f8c0ef7db4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57a78298d57623e3b7820763bff9df2ded9e07776021cddb682a5dffc5dbef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6039cdfbb6bc253893c11170fed3bb5dcd03ccaf22d84263ad5928171e81a958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterWorkloadIdentityConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class ContainerAzureClusterWorkloadIdentityConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAzureClusterWorkloadIdentityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAzureClusterWorkloadIdentityConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterWorkloadIdentityConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1613f3ee00a9a3cfaac307e4d4208746e80be9d2f34893dd225354fc200350d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAzureClusterWorkloadIdentityConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66bfcf2fa9f03edd8c67060d974779f9c69ba52bbd1b2ccc823bc0c6cbf5cda)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAzureClusterWorkloadIdentityConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7eddbd4ac0411aae407ddc460720b4aaad6faf4a05c0883d3e0d4c8414ce22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70e1f72779e0ea12c18eaf5b7a79485d757ca53a0bbe0d5ece4aa4eba881d7f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e834747f64ff727cf81b315adc614ff8418548af36dc3ad51b11fa25e781cc92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ContainerAzureClusterWorkloadIdentityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAzureCluster.ContainerAzureClusterWorkloadIdentityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae6604514a164e8537eb5afdc4fd963f6c0754f58049153e8f0def34fb0b47f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="identityProvider")
    def identity_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityProvider"))

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @builtins.property
    @jsii.member(jsii_name="workloadPool")
    def workload_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadPool"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAzureClusterWorkloadIdentityConfig]:
        return typing.cast(typing.Optional[ContainerAzureClusterWorkloadIdentityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAzureClusterWorkloadIdentityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5413304342b4d34832522cf0fe34d15397c1c3ecfcffb2d2dff607b8c993059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAzureCluster",
    "ContainerAzureClusterAuthorization",
    "ContainerAzureClusterAuthorizationAdminGroups",
    "ContainerAzureClusterAuthorizationAdminGroupsList",
    "ContainerAzureClusterAuthorizationAdminGroupsOutputReference",
    "ContainerAzureClusterAuthorizationAdminUsers",
    "ContainerAzureClusterAuthorizationAdminUsersList",
    "ContainerAzureClusterAuthorizationAdminUsersOutputReference",
    "ContainerAzureClusterAuthorizationOutputReference",
    "ContainerAzureClusterAzureServicesAuthentication",
    "ContainerAzureClusterAzureServicesAuthenticationOutputReference",
    "ContainerAzureClusterConfig",
    "ContainerAzureClusterControlPlane",
    "ContainerAzureClusterControlPlaneDatabaseEncryption",
    "ContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference",
    "ContainerAzureClusterControlPlaneMainVolume",
    "ContainerAzureClusterControlPlaneMainVolumeOutputReference",
    "ContainerAzureClusterControlPlaneOutputReference",
    "ContainerAzureClusterControlPlaneProxyConfig",
    "ContainerAzureClusterControlPlaneProxyConfigOutputReference",
    "ContainerAzureClusterControlPlaneReplicaPlacements",
    "ContainerAzureClusterControlPlaneReplicaPlacementsList",
    "ContainerAzureClusterControlPlaneReplicaPlacementsOutputReference",
    "ContainerAzureClusterControlPlaneRootVolume",
    "ContainerAzureClusterControlPlaneRootVolumeOutputReference",
    "ContainerAzureClusterControlPlaneSshConfig",
    "ContainerAzureClusterControlPlaneSshConfigOutputReference",
    "ContainerAzureClusterFleet",
    "ContainerAzureClusterFleetOutputReference",
    "ContainerAzureClusterNetworking",
    "ContainerAzureClusterNetworkingOutputReference",
    "ContainerAzureClusterTimeouts",
    "ContainerAzureClusterTimeoutsOutputReference",
    "ContainerAzureClusterWorkloadIdentityConfig",
    "ContainerAzureClusterWorkloadIdentityConfigList",
    "ContainerAzureClusterWorkloadIdentityConfigOutputReference",
]

publication.publish()

def _typecheckingstub__f3c11e721d46e3a7b82a123bcdcf802843c097210fc68f22232bbafb3a923d4c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization: typing.Union[ContainerAzureClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    azure_region: builtins.str,
    control_plane: typing.Union[ContainerAzureClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[ContainerAzureClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[ContainerAzureClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    resource_group_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    azure_services_authentication: typing.Optional[typing.Union[ContainerAzureClusterAzureServicesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAzureClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8d312089e27db042c8fc2110c0cda37b3a5af91417368ee7e3a1dfc4c3e3d739(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f471b5002f69a87a2c2fc982ce5b4ee51c1a68c40cb518ec853cfb51d2e5abf0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f79001d7d32f4d7520da2adfceb7026378e618e1804358ae53e18fcc83fab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fcfe9bbcf35986d41d8794db92451793edb5898009bc03a0e602ec1cf1569e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c16a68eb219ee30fd5a80bfce485ea3e24c36457f39c4d067d678e405a2bcbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e46a79a93b144e0230d4abafe304189b048e56ccb06609017c28c54971f0b41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac711f221b1292e79b8716ecbd5623bf275a8dfa60027bf88a13d3e084603a54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066fc0bf5c2f361b5593ee97fe72944b2a2c2fff2e7a888c7ca392cc7541eb0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f75ac2cb48f693a863943a43f2a8dd08f6ca38e7c59897c8902c47203824539(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84589d5c9aa3659efd1a1cb755b0f9f6b35c82e12cd74465e6dbddd9998effd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfec5578783816bcdcc9d454defedf21fb230508a8c1ef4401da92b1c363f37(
    *,
    admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAzureClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAzureClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f0f609ad298c1ddd8b2f2e38dc827c1a07aaa7a3919a637159b69dc1e5692e(
    *,
    group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fad1660610c5b58265c6c72df128c6b27ec9e506fe1575d87757d206e03662(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__053bc2293f35df004a6941792e22a516d47090018eb8f318a159f5398c3ba677(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe967e8ed0527b6115c6212ba764bfc0d183aec794fd3c60b4d6c6aad890a4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d468067d38788851a0dfb13aa486287a83642587382517c76b4461c8000edb8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180533a86109a3a72cbbad5d9a6f4601361498b6ea368c45396725408bcf646c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38939bb2897484a3a8baab3e8888090b5bee73cf1e3721b427c01707a5f8d2fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7af2b8917f83334f2621088dead0811ac736eb36a848fd911d166a6434dd30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991f7ae8d664a808dfe6374738230f3451005adf866ccc2dbc99019cd31043df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e2f8b588c98c00ead68731523b475f8be84227f5e2a696bb564707a4f798c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterAuthorizationAdminGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c44bffb63e1700fc95fcbc408d05a274044bfbb27c54a2c225c04ced0753c2(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d84dc5f2ae4123c2ff7b87c4bbb2d357adfb0667a295f7903b810da213af45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f245bff281b4105db302a8244a1124ed1c4182eba457b205a4e3625a595d2b22(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8050590e14d2e98c0b6126ee08fa98bf06b25054fb4ab1121b8c91ad35c02124(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642a490b64317e19fa8eccdda512a8eb30b4d3d469565d340f9a9c00190bcf15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85958a93e109dc57961b9d0be847a09a1ff0f73d60874a424407c0de2b2e3dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6d5acd944c81c45e21f16d8b78b5fb5483d59580aac70160307b65a67c8dfe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36df4ed242f3f202b8f00048b682a3c210e74784fb3ba3152ffd8fdd98e26e06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203355fddc7a70a2647477c76490b8fc4a8d9f5c1b82455ab6deb9ffff00d6bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0968af88984f524898b33dd0800c5c8596c3484fdd87079cba20918c064b1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c079a591d9f9194b5bb4ce25245ab79b97368a16bd7cc93131ad5cdb680b5d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d6663d20dc7284b9cff89987da3a4748d530e8c012780acf5459e687b3bb1a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAzureClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217298e53d55f2512586333fa7e3071a1f4ed832fb5b8e2e386b77340b2b494c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAzureClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38cbd07344bafa0e4572b548c5ed66b38e0cbf8a13ebafb283b233208e84a99(
    value: typing.Optional[ContainerAzureClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38868def03206a5f573a2a5ec72d10e0e3210a236f83f87e156e049283f9ba86(
    *,
    application_id: builtins.str,
    tenant_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f53d9e844a3711df1456f2a923baac24688ee62cff31d9e71479c2fdb92a7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149f4be564d00eb92e4821c01cf566f0254382b28b97e98b55c54cb87417b0a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a890094840ae7b5796e19467bbaf9a2ffa60cfdb47d8af94358908c2ae9f2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f414ce57f5d4e14fa1916bb68a76371704272b1f4970b60a2432e522a1a4f07(
    value: typing.Optional[ContainerAzureClusterAzureServicesAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfd85a19224ad97387a1faf5b22ca112ee9fdc0bc47a5b46a0c5e336359a38d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization: typing.Union[ContainerAzureClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    azure_region: builtins.str,
    control_plane: typing.Union[ContainerAzureClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[ContainerAzureClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[ContainerAzureClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    resource_group_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    azure_services_authentication: typing.Optional[typing.Union[ContainerAzureClusterAzureServicesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAzureClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6905c14dd4962a4798e242ea774b0fc8c353343430cb8088d487956765751835(
    *,
    ssh_config: typing.Union[ContainerAzureClusterControlPlaneSshConfig, typing.Dict[builtins.str, typing.Any]],
    subnet_id: builtins.str,
    version: builtins.str,
    database_encryption: typing.Optional[typing.Union[ContainerAzureClusterControlPlaneDatabaseEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    main_volume: typing.Optional[typing.Union[ContainerAzureClusterControlPlaneMainVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    proxy_config: typing.Optional[typing.Union[ContainerAzureClusterControlPlaneProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    replica_placements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAzureClusterControlPlaneReplicaPlacements, typing.Dict[builtins.str, typing.Any]]]]] = None,
    root_volume: typing.Optional[typing.Union[ContainerAzureClusterControlPlaneRootVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vm_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d91a7d90add13946128c6bdda801c1600095cb433b355630e500d74aa014f4(
    *,
    key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a35ffdd41735d05f0f9e45fe6e6f3eee99825c8b8394661ffa5412c46331948(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2443dfd6f4a3fdcd5b6545693f293063d240141154e6073af61c389f27583989(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fcb25b566f794a2e792be0f700d965069f1e9a1890a10945c9e0bb223d2a4d(
    value: typing.Optional[ContainerAzureClusterControlPlaneDatabaseEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1c1d3c32b8e3d98ffea5b81fa58e4352c75af3674e88e3dd68eabb03b6041a(
    *,
    size_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dcad2b5266831d6de9689cc5a686fbb664cceab621fab16a123e16c7611b254(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed471944ab2a6acc72a433670acf07f0b62110185e7ca51e078c52579245bc7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4803ab17cd59a16246e74de0cdb8ef7d0f6c765d12e4da407ad4f13b8ca32b08(
    value: typing.Optional[ContainerAzureClusterControlPlaneMainVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf88a251e43ccea5910aa677e8c6c430a8f189ade4c09f364ac5e51bcbfcaa4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389ad5488e7bca1149ca8881178f7f71f9755c55e0f7a6eb55b6f8bc110029fc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAzureClusterControlPlaneReplicaPlacements, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21b7aaf0272f6722a17354c127f64b1fb73f27ea6d8fa9966c26f0ca8d442bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2bb476ba4d10dff0f1804a63ab8e55e2ddcfe5664ed7269efd09e424b014e8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3713440fcc67a5b570ae35ccb390032ed8aa4f7112fb1ad38fa83a467a54c15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643694f5aadf6c19dc846f95d00f92ca8bf51ad0b1d772986d301f2e392396f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ed883e08ef88db105956601551688a393fda4d16e7d3f36a95410e4798ce68(
    value: typing.Optional[ContainerAzureClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c28bf6889b5137faf47c755b1a8d62c3a11a4269a4114debcbc36c04fe9798(
    *,
    resource_group_id: builtins.str,
    secret_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7049b1c60c65dd5887049c68756890e594010bd12e30b6ca601486ebe3ddfb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836e4e9ba91a02a1f173431acd0d81b872202c5a99de2ded97dec0b37122dfc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce22d5dba3d7db693b78bdd19716267dfc30c735f7b3ac297593adb640c52878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3df71362b49e03e1918c215aa379930a383757695aa74a53fa2c623c9a20e58(
    value: typing.Optional[ContainerAzureClusterControlPlaneProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84c623ca9c1ac4809e720fd642eb83ba853e7ce59da2f9c707e9ad651ccf413(
    *,
    azure_availability_zone: builtins.str,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0252f2e64dc923feed5500f1b02b3630b0b357f87812dc172c3ddf42aba1cda7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77438495b31b89e003b25abec6d4600d2967a3fdd81d81cdbfabde878fa88e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3016589485e74941712c12cb36a7ac048984a7101e064a3595a3cb05aa026675(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a60354151d87308f2a9100588371e94ef2e620068ffc09b3ed5da52308a7187(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1db1a31aec47aaf2348c620b92c7732fae990fcc8d7896e0feaf50e115433bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46f9e153930cf46be7437181353c7001752e5c5087fb21ca7685f7c5e5e636a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAzureClusterControlPlaneReplicaPlacements]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a8a46b44074286558474524f29f7dcc61010c7a733432b1415966226131582(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc1ec03f8c1e54cedcfd45478c801317ba3b861dab26ce8e23a00e103e0a71a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e601525223ae6a9da9ec949c89a4d16ca75dd2ee59acd4c97c5f4699622fd096(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586e6343ac670a677062ab6d40f851158f956ecd6b1d5d4dcb4a451153e99c2d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterControlPlaneReplicaPlacements]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0d896115bd7ccd9fc4e79260b3a120b41175cd0ac253efeea4232f91eb26c4(
    *,
    size_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b59f5f49355f5c8fc1788a086c8d9553f7e4bb918559878e042138a4c1af3cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28dffcf21d423382f2c8961d9b462c075c54d789f3030da2d6e25065aadb9099(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0593004eec3ff297883798e67bab2b225c95b710fbfd5d5bc8c0eba450efcc(
    value: typing.Optional[ContainerAzureClusterControlPlaneRootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e4ec456ed6a8b3f6cd3a77ba923ce40260ecf11b3c68b4a45a691243dec55e(
    *,
    authorized_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4fe3ba0e86c1613d8b5b0d2ad6eef29823823a3a12f7cf09c4e71c4652b4fa0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8fa0a269589c3beda358bc83dd68966377d4b8a7a712cf690b95e1a568e284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052ea01e1717123735b8ade8a474d4f185a694c40b7cbd13bb1cdcfc67f6a0ba(
    value: typing.Optional[ContainerAzureClusterControlPlaneSshConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873dcd3f787cd3f6ad1bdadbf9bbdc918929286ddf294933dcac93e853a82808(
    *,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dee0c8f0baf2df0288eca0e13e5522cca02bb558aeff96323cd199c830d70ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce04ad79ac1cd804a8b552b6c4582b269d1ab7b30235d68cd58895cb06888ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bedaedd28386a089a80a03b901abe6cfbab430890d01382481d41ae27c1d5a5(
    value: typing.Optional[ContainerAzureClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9441b83486675d1fd70ac0a05a2b267f64a921318dae14d4cf8671f21f2663c(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
    virtual_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72207d86d46d3b6f645d0cfc9e062ebce6ae93e8b4a1031dfcd5d98cd26a68c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4243786c64c2de68dc50815589c2c4097723e7bf9d21726a00734ee0bdb432(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c603be8d4fb0739ceb04cec30f6b6247aa90ef1a1663d82afc0d0a111cffbce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bd4bf29ba15901c497c43f608d2ea56555d833d2d7bb088cad653187b8a972(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce982061ddb61e3e80dca25988d5751c7eb14fca4bd476aa75b42a2cfb69ba9(
    value: typing.Optional[ContainerAzureClusterNetworking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc341d92141a47526f3aaf30b88b0d5eca0c4a9b25844ba1d9a26a0c14109752(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e763e03719186e578cfb8fea6e86c9698bbae1dfb08188651f0fc16590bb39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f89041c1595516e2aaf7df5a08417fdc353375ae8035040d79eac7b78c1e146(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f683170cbed920f34de31ce32b5e7c9699c5d647820eb72057429f8c0ef7db4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57a78298d57623e3b7820763bff9df2ded9e07776021cddb682a5dffc5dbef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6039cdfbb6bc253893c11170fed3bb5dcd03ccaf22d84263ad5928171e81a958(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAzureClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1613f3ee00a9a3cfaac307e4d4208746e80be9d2f34893dd225354fc200350d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66bfcf2fa9f03edd8c67060d974779f9c69ba52bbd1b2ccc823bc0c6cbf5cda(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7eddbd4ac0411aae407ddc460720b4aaad6faf4a05c0883d3e0d4c8414ce22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e1f72779e0ea12c18eaf5b7a79485d757ca53a0bbe0d5ece4aa4eba881d7f8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e834747f64ff727cf81b315adc614ff8418548af36dc3ad51b11fa25e781cc92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6604514a164e8537eb5afdc4fd963f6c0754f58049153e8f0def34fb0b47f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5413304342b4d34832522cf0fe34d15397c1c3ecfcffb2d2dff607b8c993059(
    value: typing.Optional[ContainerAzureClusterWorkloadIdentityConfig],
) -> None:
    """Type checking stubs"""
    pass
