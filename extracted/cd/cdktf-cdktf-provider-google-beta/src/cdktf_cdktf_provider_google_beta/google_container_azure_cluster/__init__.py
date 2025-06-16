r'''
# `google_container_azure_cluster`

Refer to the Terraform Registry for docs: [`google_container_azure_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster).
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


class GoogleContainerAzureCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster google_container_azure_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization: typing.Union["GoogleContainerAzureClusterAuthorization", typing.Dict[builtins.str, typing.Any]],
        azure_region: builtins.str,
        control_plane: typing.Union["GoogleContainerAzureClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["GoogleContainerAzureClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["GoogleContainerAzureClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        resource_group_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        azure_services_authentication: typing.Optional[typing.Union["GoogleContainerAzureClusterAzureServicesAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["GoogleContainerAzureClusterLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAzureClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster google_container_azure_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#authorization GoogleContainerAzureCluster#authorization}
        :param azure_region: The Azure region where the cluster runs. Each Google Cloud region supports a subset of nearby Azure regions. You can call to list all supported Azure regions within a given Google Cloud region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#azure_region GoogleContainerAzureCluster#azure_region}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#control_plane GoogleContainerAzureCluster#control_plane}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#fleet GoogleContainerAzureCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#location GoogleContainerAzureCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#name GoogleContainerAzureCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#networking GoogleContainerAzureCluster#networking}
        :param resource_group_id: The ARM ID of the resource group where the cluster resources are deployed. For example: ``/subscriptions/* /resourceGroups/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#resource_group_id GoogleContainerAzureCluster#resource_group_id} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Keys can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#annotations GoogleContainerAzureCluster#annotations}
        :param azure_services_authentication: azure_services_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#azure_services_authentication GoogleContainerAzureCluster#azure_services_authentication}
        :param client: Name of the AzureClient. The ``AzureClient`` resource must reside on the same GCP project and region as the ``AzureCluster``. ``AzureClient`` names are formatted as ``projects/<project-number>/locations/<region>/azureClients/<client-id>``. See Resource Names (https:cloud.google.com/apis/design/resource_names) for more details on Google Cloud resource names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#client GoogleContainerAzureCluster#client}
        :param description: Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#description GoogleContainerAzureCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#id GoogleContainerAzureCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#logging_config GoogleContainerAzureCluster#logging_config}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#project GoogleContainerAzureCluster#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#timeouts GoogleContainerAzureCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f832561e1296062901c1dd06b3e3c42bae31efcf7577ef56fdd6171e3929fbe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleContainerAzureClusterConfig(
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
            logging_config=logging_config,
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
        '''Generates CDKTF code for importing a GoogleContainerAzureCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleContainerAzureCluster to import.
        :param import_from_id: The id of the existing GoogleContainerAzureCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleContainerAzureCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e327754b623f234aed311dddd892dc4d2d78a876f256b87cf27dd474798bca41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAzureClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
        admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAzureClusterAuthorizationAdminGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#admin_users GoogleContainerAzureCluster#admin_users}
        :param admin_groups: admin_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#admin_groups GoogleContainerAzureCluster#admin_groups}
        '''
        value = GoogleContainerAzureClusterAuthorization(
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
        :param application_id: The Azure Active Directory Application ID for Authentication configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#application_id GoogleContainerAzureCluster#application_id}
        :param tenant_id: The Azure Active Directory Tenant ID for Authentication configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#tenant_id GoogleContainerAzureCluster#tenant_id}
        '''
        value = GoogleContainerAzureClusterAzureServicesAuthentication(
            application_id=application_id, tenant_id=tenant_id
        )

        return typing.cast(None, jsii.invoke(self, "putAzureServicesAuthentication", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        ssh_config: typing.Union["GoogleContainerAzureClusterControlPlaneSshConfig", typing.Dict[builtins.str, typing.Any]],
        subnet_id: builtins.str,
        version: builtins.str,
        database_encryption: typing.Optional[typing.Union["GoogleContainerAzureClusterControlPlaneDatabaseEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        main_volume: typing.Optional[typing.Union["GoogleContainerAzureClusterControlPlaneMainVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy_config: typing.Optional[typing.Union["GoogleContainerAzureClusterControlPlaneProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        replica_placements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAzureClusterControlPlaneReplicaPlacements", typing.Dict[builtins.str, typing.Any]]]]] = None,
        root_volume: typing.Optional[typing.Union["GoogleContainerAzureClusterControlPlaneRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vm_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#ssh_config GoogleContainerAzureCluster#ssh_config}
        :param subnet_id: The ARM ID of the subnet where the control plane VMs are deployed. Example: ``/subscriptions//resourceGroups//providers/Microsoft.Network/virtualNetworks//subnets/default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#subnet_id GoogleContainerAzureCluster#subnet_id}
        :param version: The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAzureServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#version GoogleContainerAzureCluster#version}
        :param database_encryption: database_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#database_encryption GoogleContainerAzureCluster#database_encryption}
        :param main_volume: main_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#main_volume GoogleContainerAzureCluster#main_volume}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#proxy_config GoogleContainerAzureCluster#proxy_config}
        :param replica_placements: replica_placements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#replica_placements GoogleContainerAzureCluster#replica_placements}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#root_volume GoogleContainerAzureCluster#root_volume}
        :param tags: Optional. A set of tags to apply to all underlying control plane Azure resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#tags GoogleContainerAzureCluster#tags}
        :param vm_size: Optional. The Azure VM size name. Example: ``Standard_DS2_v2``. For available VM sizes, see https://docs.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions. When unspecified, it defaults to ``Standard_DS2_v2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#vm_size GoogleContainerAzureCluster#vm_size}
        '''
        value = GoogleContainerAzureClusterControlPlane(
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
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#project GoogleContainerAzureCluster#project}
        '''
        value = GoogleContainerAzureClusterFleet(project=project)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        component_config: typing.Optional[typing.Union["GoogleContainerAzureClusterLoggingConfigComponentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param component_config: component_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#component_config GoogleContainerAzureCluster#component_config}
        '''
        value = GoogleContainerAzureClusterLoggingConfig(
            component_config=component_config
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="putNetworking")
    def put_networking(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: The IP address range of the pods in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All pods in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#pod_address_cidr_blocks GoogleContainerAzureCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: The IP address range for services in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All services in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creating a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#service_address_cidr_blocks GoogleContainerAzureCluster#service_address_cidr_blocks}
        :param virtual_network_id: The Azure Resource Manager (ARM) ID of the VNet associated with your cluster. All components in the cluster (i.e. control plane and node pools) run on a single VNet. Example: ``/subscriptions/* /resourceGroups/* /providers/Microsoft.Network/virtualNetworks/*`` This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#virtual_network_id GoogleContainerAzureCluster#virtual_network_id} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        value = GoogleContainerAzureClusterNetworking(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#create GoogleContainerAzureCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#delete GoogleContainerAzureCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#update GoogleContainerAzureCluster#update}.
        '''
        value = GoogleContainerAzureClusterTimeouts(
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

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

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
    def authorization(
        self,
    ) -> "GoogleContainerAzureClusterAuthorizationOutputReference":
        return typing.cast("GoogleContainerAzureClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="azureServicesAuthentication")
    def azure_services_authentication(
        self,
    ) -> "GoogleContainerAzureClusterAzureServicesAuthenticationOutputReference":
        return typing.cast("GoogleContainerAzureClusterAzureServicesAuthenticationOutputReference", jsii.get(self, "azureServicesAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> "GoogleContainerAzureClusterControlPlaneOutputReference":
        return typing.cast("GoogleContainerAzureClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

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
    def fleet(self) -> "GoogleContainerAzureClusterFleetOutputReference":
        return typing.cast("GoogleContainerAzureClusterFleetOutputReference", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(
        self,
    ) -> "GoogleContainerAzureClusterLoggingConfigOutputReference":
        return typing.cast("GoogleContainerAzureClusterLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="networking")
    def networking(self) -> "GoogleContainerAzureClusterNetworkingOutputReference":
        return typing.cast("GoogleContainerAzureClusterNetworkingOutputReference", jsii.get(self, "networking"))

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
    def timeouts(self) -> "GoogleContainerAzureClusterTimeoutsOutputReference":
        return typing.cast("GoogleContainerAzureClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> "GoogleContainerAzureClusterWorkloadIdentityConfigList":
        return typing.cast("GoogleContainerAzureClusterWorkloadIdentityConfigList", jsii.get(self, "workloadIdentityConfig"))

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
    ) -> typing.Optional["GoogleContainerAzureClusterAuthorization"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="azureRegionInput")
    def azure_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azureRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="azureServicesAuthenticationInput")
    def azure_services_authentication_input(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterAzureServicesAuthentication"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterAzureServicesAuthentication"], jsii.get(self, "azureServicesAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientInput")
    def client_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterControlPlane"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetInput")
    def fleet_input(self) -> typing.Optional["GoogleContainerAzureClusterFleet"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterFleet"], jsii.get(self, "fleetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterLoggingConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkingInput")
    def networking_input(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterNetworking"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterNetworking"], jsii.get(self, "networkingInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAzureClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAzureClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855d9eae150ca7358b3e2185c5bc159cf421ec960702c36fec9074d3e4ce6467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="azureRegion")
    def azure_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "azureRegion"))

    @azure_region.setter
    def azure_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8bcb44d10c61b9d8ffa04e04475fddf21635ff37f5746b5be8d796433edca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="client")
    def client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "client"))

    @client.setter
    def client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265b7507e8d672aef0b9075d578edbc987a965c9369a3d9456b5b796c35505ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "client", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ea104da716818e31c905e5dd50aa4ca9197c90594b743f8e6888b316f8888c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fce849d094c48fe91a2b2038910a4dbcd2cb0cca04d1855e75b0569f1a36a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56dcea84ce4ce8a4b0530d38c29cee784b0c73bf73993668af5781573222100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed139e283a5cde135a8627eff7a2876c59791ac3b9fffe0be823bcad0e75cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c61ecf1b4808cc34c5bde9ebe5a4db8bd5347dcfbc5617a32e52af4806400b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupId")
    def resource_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupId"))

    @resource_group_id.setter
    def resource_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b639f9873a50c67d9e1692228e29d09872797e802ed72e22e56819831d2c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers", "admin_groups": "adminGroups"},
)
class GoogleContainerAzureClusterAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAzureClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
        admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAzureClusterAuthorizationAdminGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#admin_users GoogleContainerAzureCluster#admin_users}
        :param admin_groups: admin_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#admin_groups GoogleContainerAzureCluster#admin_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df80c996004bf0c028b988636f281ee13c0e57d6349b684583850b1181a36b1)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAzureClusterAuthorizationAdminUsers"]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#admin_users GoogleContainerAzureCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAzureClusterAuthorizationAdminUsers"]], result)

    @builtins.property
    def admin_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAzureClusterAuthorizationAdminGroups"]]]:
        '''admin_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#admin_groups GoogleContainerAzureCluster#admin_groups}
        '''
        result = self._values.get("admin_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAzureClusterAuthorizationAdminGroups"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAuthorizationAdminGroups",
    jsii_struct_bases=[],
    name_mapping={"group": "group"},
)
class GoogleContainerAzureClusterAuthorizationAdminGroups:
    def __init__(self, *, group: builtins.str) -> None:
        '''
        :param group: The name of the group, e.g. ``my-group@domain.com``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#group GoogleContainerAzureCluster#group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0a043c2a0201245242962a62f44c6886f5da2f5af68f6ccf6a4e71d81532eb)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
        }

    @builtins.property
    def group(self) -> builtins.str:
        '''The name of the group, e.g. ``my-group@domain.com``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#group GoogleContainerAzureCluster#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterAuthorizationAdminGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterAuthorizationAdminGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAuthorizationAdminGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90bb015b08a6cc55f032e65c53cb9341ac32ad74b7eb488acc46c7550d019b86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAzureClusterAuthorizationAdminGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d371c4d619d9954fb40d070c16317d43ae2d7e9e3a8845b18ad2a6ebb2c001a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAzureClusterAuthorizationAdminGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b7f33814f0434dc5a982884bf31172a657290b912ee6390370bf60b447e6b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eec2cb545e7b3c3e1b67529a38b79787bf9a6cdf813ec01cf7b17a1c8a3f4f2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae555424cc25cee19e534d842fafdd403ba388d4d981af124831796b87a3b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b53f5edd8efe9dbdccaf3c328410f17a7a6715934fb7aa3a32500c5bb18451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAzureClusterAuthorizationAdminGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAuthorizationAdminGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4503c77ba37c4d654bf9a243607fe0019fbcce4c425c06b67be0cddb11bfa9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9f05e4fa728abfbe98fc7d7bbd62338a9f923e393ca04bdba7b830c201bdb06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterAuthorizationAdminGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterAuthorizationAdminGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterAuthorizationAdminGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c361a02c81a430974e4f37cb177943d692c564c8ae2802156f7f996aeea4942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GoogleContainerAzureClusterAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. ``my-gcp-id@gmail.com``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#username GoogleContainerAzureCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8574e7f8b3111a2517c1266862c90ea7d37d83b77d8642f46db613c4f8b89da4)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. ``my-gcp-id@gmail.com``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#username GoogleContainerAzureCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4595df510ca9bf5929db49faf13c229ce540f2f42d2f7f0b83e5ba1ba9f5db40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAzureClusterAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a10a40d50d47fbb3c09a3bda1780bb0bb25d95568e30c409479fe5dbab0914e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAzureClusterAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9abceec4599240df98638ec781adf8bd0b410cc31156348128e1b6bd709f14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e398cdfd9187baf525a8e37dce2c93b68e3bedef8a2d6b8cc22577c7c966ba9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb269321ae749221d9d0f1e9ef951d24af265eb1750a5ec875658bb2dac5d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282e1d0aecdfd90bebfa9e71041b4dfae2cb314f47ffc564d2c912d52aa0698d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAzureClusterAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c24e2a633efa0f344bac1acf14eac89d61b73e1bff1d4542318f9b3b91b10e6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c13d9ce91daa8450456519a84c1416d4efa9bbab656c68da88d6a0de2164c81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8a4f7527c50c5d87bbd965d1bcf9e37f1b893bca7d08117bf608b4690eafcd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAzureClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d75b1bcc0c68a4e915fb625586b8ca4ab9379b40be1e40853c550ebcfeef1df0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminGroups")
    def put_admin_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAzureClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01e761c93615a5350d78a5149866edb3e669209ea786cf65d672564679a301b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminGroups", [value]))

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAzureClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b485f75789480e1665f42157c02939727ae8e136fc43ef72cf524772e471b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @jsii.member(jsii_name="resetAdminGroups")
    def reset_admin_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminGroups", []))

    @builtins.property
    @jsii.member(jsii_name="adminGroups")
    def admin_groups(self) -> GoogleContainerAzureClusterAuthorizationAdminGroupsList:
        return typing.cast(GoogleContainerAzureClusterAuthorizationAdminGroupsList, jsii.get(self, "adminGroups"))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> GoogleContainerAzureClusterAuthorizationAdminUsersList:
        return typing.cast(GoogleContainerAzureClusterAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminGroupsInput")
    def admin_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminGroups]]], jsii.get(self, "adminGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterAuthorization]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a36c04c0d676032db41af0e4727de0ee98b7e0a44d6a0dee8e5874fb0db7af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAzureServicesAuthentication",
    jsii_struct_bases=[],
    name_mapping={"application_id": "applicationId", "tenant_id": "tenantId"},
)
class GoogleContainerAzureClusterAzureServicesAuthentication:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param application_id: The Azure Active Directory Application ID for Authentication configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#application_id GoogleContainerAzureCluster#application_id}
        :param tenant_id: The Azure Active Directory Tenant ID for Authentication configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#tenant_id GoogleContainerAzureCluster#tenant_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c951f40988a4b87861b3bb73a7f6a110fe8d97a5e5f173bade1dda73d15d948f)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "tenant_id": tenant_id,
        }

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The Azure Active Directory Application ID for Authentication configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#application_id GoogleContainerAzureCluster#application_id}
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''The Azure Active Directory Tenant ID for Authentication configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#tenant_id GoogleContainerAzureCluster#tenant_id}
        '''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterAzureServicesAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterAzureServicesAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterAzureServicesAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41087aec097aa3d546dd00d0ff2b8e55ea8c6e7ca2d69ffa96bc6433eeb77cfa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b177ddd25ece80c4cb862417cdf20775ba3233f3a42f1d05efd6fa9c370d616f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5b2d2f39aaa5d873cd475b42084afa7273d37b5319ce9da4cace521c8a8aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterAzureServicesAuthentication]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterAzureServicesAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterAzureServicesAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc92b8c5b5408f815edd44ab698eb01763caf346cf69a2dafdc9a59b1fc4b20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterConfig",
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
        "logging_config": "loggingConfig",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleContainerAzureClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization: typing.Union[GoogleContainerAzureClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
        azure_region: builtins.str,
        control_plane: typing.Union["GoogleContainerAzureClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["GoogleContainerAzureClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["GoogleContainerAzureClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        resource_group_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        azure_services_authentication: typing.Optional[typing.Union[GoogleContainerAzureClusterAzureServicesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["GoogleContainerAzureClusterLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAzureClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#authorization GoogleContainerAzureCluster#authorization}
        :param azure_region: The Azure region where the cluster runs. Each Google Cloud region supports a subset of nearby Azure regions. You can call to list all supported Azure regions within a given Google Cloud region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#azure_region GoogleContainerAzureCluster#azure_region}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#control_plane GoogleContainerAzureCluster#control_plane}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#fleet GoogleContainerAzureCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#location GoogleContainerAzureCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#name GoogleContainerAzureCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#networking GoogleContainerAzureCluster#networking}
        :param resource_group_id: The ARM ID of the resource group where the cluster resources are deployed. For example: ``/subscriptions/* /resourceGroups/*``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#resource_group_id GoogleContainerAzureCluster#resource_group_id} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Keys can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#annotations GoogleContainerAzureCluster#annotations}
        :param azure_services_authentication: azure_services_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#azure_services_authentication GoogleContainerAzureCluster#azure_services_authentication}
        :param client: Name of the AzureClient. The ``AzureClient`` resource must reside on the same GCP project and region as the ``AzureCluster``. ``AzureClient`` names are formatted as ``projects/<project-number>/locations/<region>/azureClients/<client-id>``. See Resource Names (https:cloud.google.com/apis/design/resource_names) for more details on Google Cloud resource names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#client GoogleContainerAzureCluster#client}
        :param description: Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#description GoogleContainerAzureCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#id GoogleContainerAzureCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#logging_config GoogleContainerAzureCluster#logging_config}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#project GoogleContainerAzureCluster#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#timeouts GoogleContainerAzureCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authorization, dict):
            authorization = GoogleContainerAzureClusterAuthorization(**authorization)
        if isinstance(control_plane, dict):
            control_plane = GoogleContainerAzureClusterControlPlane(**control_plane)
        if isinstance(fleet, dict):
            fleet = GoogleContainerAzureClusterFleet(**fleet)
        if isinstance(networking, dict):
            networking = GoogleContainerAzureClusterNetworking(**networking)
        if isinstance(azure_services_authentication, dict):
            azure_services_authentication = GoogleContainerAzureClusterAzureServicesAuthentication(**azure_services_authentication)
        if isinstance(logging_config, dict):
            logging_config = GoogleContainerAzureClusterLoggingConfig(**logging_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleContainerAzureClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6da5163c6a69cb7728506a93ed722079ca0cc80d04054345d8dc7111dd4dbca)
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
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
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
        if logging_config is not None:
            self._values["logging_config"] = logging_config
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
    def authorization(self) -> GoogleContainerAzureClusterAuthorization:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#authorization GoogleContainerAzureCluster#authorization}
        '''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(GoogleContainerAzureClusterAuthorization, result)

    @builtins.property
    def azure_region(self) -> builtins.str:
        '''The Azure region where the cluster runs.

        Each Google Cloud region supports a subset of nearby Azure regions. You can call to list all supported Azure regions within a given Google Cloud region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#azure_region GoogleContainerAzureCluster#azure_region}
        '''
        result = self._values.get("azure_region")
        assert result is not None, "Required property 'azure_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane(self) -> "GoogleContainerAzureClusterControlPlane":
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#control_plane GoogleContainerAzureCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        assert result is not None, "Required property 'control_plane' is missing"
        return typing.cast("GoogleContainerAzureClusterControlPlane", result)

    @builtins.property
    def fleet(self) -> "GoogleContainerAzureClusterFleet":
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#fleet GoogleContainerAzureCluster#fleet}
        '''
        result = self._values.get("fleet")
        assert result is not None, "Required property 'fleet' is missing"
        return typing.cast("GoogleContainerAzureClusterFleet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#location GoogleContainerAzureCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#name GoogleContainerAzureCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def networking(self) -> "GoogleContainerAzureClusterNetworking":
        '''networking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#networking GoogleContainerAzureCluster#networking}
        '''
        result = self._values.get("networking")
        assert result is not None, "Required property 'networking' is missing"
        return typing.cast("GoogleContainerAzureClusterNetworking", result)

    @builtins.property
    def resource_group_id(self) -> builtins.str:
        '''The ARM ID of the resource group where the cluster resources are deployed. For example: ``/subscriptions/* /resourceGroups/*``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#resource_group_id GoogleContainerAzureCluster#resource_group_id}

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#annotations GoogleContainerAzureCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def azure_services_authentication(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterAzureServicesAuthentication]:
        '''azure_services_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#azure_services_authentication GoogleContainerAzureCluster#azure_services_authentication}
        '''
        result = self._values.get("azure_services_authentication")
        return typing.cast(typing.Optional[GoogleContainerAzureClusterAzureServicesAuthentication], result)

    @builtins.property
    def client(self) -> typing.Optional[builtins.str]:
        '''Name of the AzureClient.

        The ``AzureClient`` resource must reside on the same GCP project and region as the ``AzureCluster``. ``AzureClient`` names are formatted as ``projects/<project-number>/locations/<region>/azureClients/<client-id>``. See Resource Names (https:cloud.google.com/apis/design/resource_names) for more details on Google Cloud resource names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#client GoogleContainerAzureCluster#client}
        '''
        result = self._values.get("client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#description GoogleContainerAzureCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#id GoogleContainerAzureCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#logging_config GoogleContainerAzureCluster#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["GoogleContainerAzureClusterLoggingConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#project GoogleContainerAzureCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleContainerAzureClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#timeouts GoogleContainerAzureCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleContainerAzureClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlane",
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
class GoogleContainerAzureClusterControlPlane:
    def __init__(
        self,
        *,
        ssh_config: typing.Union["GoogleContainerAzureClusterControlPlaneSshConfig", typing.Dict[builtins.str, typing.Any]],
        subnet_id: builtins.str,
        version: builtins.str,
        database_encryption: typing.Optional[typing.Union["GoogleContainerAzureClusterControlPlaneDatabaseEncryption", typing.Dict[builtins.str, typing.Any]]] = None,
        main_volume: typing.Optional[typing.Union["GoogleContainerAzureClusterControlPlaneMainVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy_config: typing.Optional[typing.Union["GoogleContainerAzureClusterControlPlaneProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        replica_placements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAzureClusterControlPlaneReplicaPlacements", typing.Dict[builtins.str, typing.Any]]]]] = None,
        root_volume: typing.Optional[typing.Union["GoogleContainerAzureClusterControlPlaneRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vm_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#ssh_config GoogleContainerAzureCluster#ssh_config}
        :param subnet_id: The ARM ID of the subnet where the control plane VMs are deployed. Example: ``/subscriptions//resourceGroups//providers/Microsoft.Network/virtualNetworks//subnets/default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#subnet_id GoogleContainerAzureCluster#subnet_id}
        :param version: The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAzureServerConfig. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#version GoogleContainerAzureCluster#version}
        :param database_encryption: database_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#database_encryption GoogleContainerAzureCluster#database_encryption}
        :param main_volume: main_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#main_volume GoogleContainerAzureCluster#main_volume}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#proxy_config GoogleContainerAzureCluster#proxy_config}
        :param replica_placements: replica_placements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#replica_placements GoogleContainerAzureCluster#replica_placements}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#root_volume GoogleContainerAzureCluster#root_volume}
        :param tags: Optional. A set of tags to apply to all underlying control plane Azure resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#tags GoogleContainerAzureCluster#tags}
        :param vm_size: Optional. The Azure VM size name. Example: ``Standard_DS2_v2``. For available VM sizes, see https://docs.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions. When unspecified, it defaults to ``Standard_DS2_v2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#vm_size GoogleContainerAzureCluster#vm_size}
        '''
        if isinstance(ssh_config, dict):
            ssh_config = GoogleContainerAzureClusterControlPlaneSshConfig(**ssh_config)
        if isinstance(database_encryption, dict):
            database_encryption = GoogleContainerAzureClusterControlPlaneDatabaseEncryption(**database_encryption)
        if isinstance(main_volume, dict):
            main_volume = GoogleContainerAzureClusterControlPlaneMainVolume(**main_volume)
        if isinstance(proxy_config, dict):
            proxy_config = GoogleContainerAzureClusterControlPlaneProxyConfig(**proxy_config)
        if isinstance(root_volume, dict):
            root_volume = GoogleContainerAzureClusterControlPlaneRootVolume(**root_volume)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be16250f126926182c485593fcc235b9121cf3c52e84cab4b39927733b617553)
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
    def ssh_config(self) -> "GoogleContainerAzureClusterControlPlaneSshConfig":
        '''ssh_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#ssh_config GoogleContainerAzureCluster#ssh_config}
        '''
        result = self._values.get("ssh_config")
        assert result is not None, "Required property 'ssh_config' is missing"
        return typing.cast("GoogleContainerAzureClusterControlPlaneSshConfig", result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The ARM ID of the subnet where the control plane VMs are deployed. Example: ``/subscriptions//resourceGroups//providers/Microsoft.Network/virtualNetworks//subnets/default``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#subnet_id GoogleContainerAzureCluster#subnet_id}
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling GetAzureServerConfig.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#version GoogleContainerAzureCluster#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_encryption(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterControlPlaneDatabaseEncryption"]:
        '''database_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#database_encryption GoogleContainerAzureCluster#database_encryption}
        '''
        result = self._values.get("database_encryption")
        return typing.cast(typing.Optional["GoogleContainerAzureClusterControlPlaneDatabaseEncryption"], result)

    @builtins.property
    def main_volume(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterControlPlaneMainVolume"]:
        '''main_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#main_volume GoogleContainerAzureCluster#main_volume}
        '''
        result = self._values.get("main_volume")
        return typing.cast(typing.Optional["GoogleContainerAzureClusterControlPlaneMainVolume"], result)

    @builtins.property
    def proxy_config(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterControlPlaneProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#proxy_config GoogleContainerAzureCluster#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["GoogleContainerAzureClusterControlPlaneProxyConfig"], result)

    @builtins.property
    def replica_placements(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAzureClusterControlPlaneReplicaPlacements"]]]:
        '''replica_placements block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#replica_placements GoogleContainerAzureCluster#replica_placements}
        '''
        result = self._values.get("replica_placements")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAzureClusterControlPlaneReplicaPlacements"]]], result)

    @builtins.property
    def root_volume(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterControlPlaneRootVolume"]:
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#root_volume GoogleContainerAzureCluster#root_volume}
        '''
        result = self._values.get("root_volume")
        return typing.cast(typing.Optional["GoogleContainerAzureClusterControlPlaneRootVolume"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. A set of tags to apply to all underlying control plane Azure resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#tags GoogleContainerAzureCluster#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vm_size(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Azure VM size name. Example: ``Standard_DS2_v2``. For available VM sizes, see https://docs.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions. When unspecified, it defaults to ``Standard_DS2_v2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#vm_size GoogleContainerAzureCluster#vm_size}
        '''
        result = self._values.get("vm_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneDatabaseEncryption",
    jsii_struct_bases=[],
    name_mapping={"key_id": "keyId"},
)
class GoogleContainerAzureClusterControlPlaneDatabaseEncryption:
    def __init__(self, *, key_id: builtins.str) -> None:
        '''
        :param key_id: The ARM ID of the Azure Key Vault key to encrypt / decrypt data. For example: ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.KeyVault/vaults/<key-vault-id>/keys/<key-name>`` Encryption will always take the latest version of the key and hence specific version is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#key_id GoogleContainerAzureCluster#key_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb9776e8bb66649d88eba6b51c3c8ab437526c88b364ab6dd973a371d3dd15d)
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_id": key_id,
        }

    @builtins.property
    def key_id(self) -> builtins.str:
        '''The ARM ID of the Azure Key Vault key to encrypt / decrypt data.

        For example: ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.KeyVault/vaults/<key-vault-id>/keys/<key-name>`` Encryption will always take the latest version of the key and hence specific version is not supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#key_id GoogleContainerAzureCluster#key_id}
        '''
        result = self._values.get("key_id")
        assert result is not None, "Required property 'key_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterControlPlaneDatabaseEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b837ac4e6df7174c236254e31645787a51a65461ae8d73faefcc05364d750c79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0227e2bac0dfa9d75d40914751a689a3608a31fea5a3992fc6a47dbff96323e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterControlPlaneDatabaseEncryption]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterControlPlaneDatabaseEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterControlPlaneDatabaseEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24399b26c077c26ddccfbb6431180fbb71c53459fc238b5955c76341a98e0503)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneMainVolume",
    jsii_struct_bases=[],
    name_mapping={"size_gib": "sizeGib"},
)
class GoogleContainerAzureClusterControlPlaneMainVolume:
    def __init__(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#size_gib GoogleContainerAzureCluster#size_gib}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750dda3f725d714ace9ec4441623c559d84632236dcf78b44f33a47a04e41efc)
            check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size_gib is not None:
            self._values["size_gib"] = size_gib

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#size_gib GoogleContainerAzureCluster#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterControlPlaneMainVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterControlPlaneMainVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneMainVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0353f33345fdc0db433ea550a350cff5201bbcb6ddbca674f49a7f6ced3d219)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a28d622947b023a104dd0d5cf61bc902cbd54e9d6df91325b7036fe891a104f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterControlPlaneMainVolume]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterControlPlaneMainVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterControlPlaneMainVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d74dcab1cbb9f82bee2cd0fc58955d45bde0adf90f1cbd662986a6e29ce0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAzureClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5485600f02db32e9eaba712871f363e3b29c9c90fa769c1d7ea0aefd14a60372)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatabaseEncryption")
    def put_database_encryption(self, *, key_id: builtins.str) -> None:
        '''
        :param key_id: The ARM ID of the Azure Key Vault key to encrypt / decrypt data. For example: ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-id>/providers/Microsoft.KeyVault/vaults/<key-vault-id>/keys/<key-name>`` Encryption will always take the latest version of the key and hence specific version is not supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#key_id GoogleContainerAzureCluster#key_id}
        '''
        value = GoogleContainerAzureClusterControlPlaneDatabaseEncryption(
            key_id=key_id
        )

        return typing.cast(None, jsii.invoke(self, "putDatabaseEncryption", [value]))

    @jsii.member(jsii_name="putMainVolume")
    def put_main_volume(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#size_gib GoogleContainerAzureCluster#size_gib}
        '''
        value = GoogleContainerAzureClusterControlPlaneMainVolume(size_gib=size_gib)

        return typing.cast(None, jsii.invoke(self, "putMainVolume", [value]))

    @jsii.member(jsii_name="putProxyConfig")
    def put_proxy_config(
        self,
        *,
        resource_group_id: builtins.str,
        secret_id: builtins.str,
    ) -> None:
        '''
        :param resource_group_id: The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#resource_group_id GoogleContainerAzureCluster#resource_group_id}
        :param secret_id: The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#secret_id GoogleContainerAzureCluster#secret_id}
        '''
        value = GoogleContainerAzureClusterControlPlaneProxyConfig(
            resource_group_id=resource_group_id, secret_id=secret_id
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfig", [value]))

    @jsii.member(jsii_name="putReplicaPlacements")
    def put_replica_placements(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAzureClusterControlPlaneReplicaPlacements", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd908d0cb950190570a1b87ec7e19825e00a2dd98e5aa5bc7f490b6a35876cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReplicaPlacements", [value]))

    @jsii.member(jsii_name="putRootVolume")
    def put_root_volume(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#size_gib GoogleContainerAzureCluster#size_gib}
        '''
        value = GoogleContainerAzureClusterControlPlaneRootVolume(size_gib=size_gib)

        return typing.cast(None, jsii.invoke(self, "putRootVolume", [value]))

    @jsii.member(jsii_name="putSshConfig")
    def put_ssh_config(self, *, authorized_key: builtins.str) -> None:
        '''
        :param authorized_key: The SSH public key data for VMs managed by Anthos. This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#authorized_key GoogleContainerAzureCluster#authorized_key}
        '''
        value = GoogleContainerAzureClusterControlPlaneSshConfig(
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
    ) -> GoogleContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference:
        return typing.cast(GoogleContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference, jsii.get(self, "databaseEncryption"))

    @builtins.property
    @jsii.member(jsii_name="mainVolume")
    def main_volume(
        self,
    ) -> GoogleContainerAzureClusterControlPlaneMainVolumeOutputReference:
        return typing.cast(GoogleContainerAzureClusterControlPlaneMainVolumeOutputReference, jsii.get(self, "mainVolume"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(
        self,
    ) -> "GoogleContainerAzureClusterControlPlaneProxyConfigOutputReference":
        return typing.cast("GoogleContainerAzureClusterControlPlaneProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="replicaPlacements")
    def replica_placements(
        self,
    ) -> "GoogleContainerAzureClusterControlPlaneReplicaPlacementsList":
        return typing.cast("GoogleContainerAzureClusterControlPlaneReplicaPlacementsList", jsii.get(self, "replicaPlacements"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(
        self,
    ) -> "GoogleContainerAzureClusterControlPlaneRootVolumeOutputReference":
        return typing.cast("GoogleContainerAzureClusterControlPlaneRootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="sshConfig")
    def ssh_config(
        self,
    ) -> "GoogleContainerAzureClusterControlPlaneSshConfigOutputReference":
        return typing.cast("GoogleContainerAzureClusterControlPlaneSshConfigOutputReference", jsii.get(self, "sshConfig"))

    @builtins.property
    @jsii.member(jsii_name="databaseEncryptionInput")
    def database_encryption_input(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterControlPlaneDatabaseEncryption]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterControlPlaneDatabaseEncryption], jsii.get(self, "databaseEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="mainVolumeInput")
    def main_volume_input(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterControlPlaneMainVolume]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterControlPlaneMainVolume], jsii.get(self, "mainVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfigInput")
    def proxy_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterControlPlaneProxyConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterControlPlaneProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="replicaPlacementsInput")
    def replica_placements_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAzureClusterControlPlaneReplicaPlacements"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAzureClusterControlPlaneReplicaPlacements"]]], jsii.get(self, "replicaPlacementsInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterControlPlaneRootVolume"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterControlPlaneRootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="sshConfigInput")
    def ssh_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterControlPlaneSshConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAzureClusterControlPlaneSshConfig"], jsii.get(self, "sshConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a46197fbbe05a0d22729d63400542170bc54386a374693701bb49c309b2b2990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42f38ca7d7055ea0e011a4766537436315b9f1784f5aad7a66bb095d90ce90c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfcf3296804a682a07ea00424c387f1a78144c3215c05813bff369084f16f0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vmSize")
    def vm_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vmSize"))

    @vm_size.setter
    def vm_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6d41ed00544581fb5604b224143a2e233892675ee971c78c2385edab33b5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterControlPlane]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7f868bbc08022a1ac7b77d000142fbaff00165134d9ff4d03b2f90a49457ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"resource_group_id": "resourceGroupId", "secret_id": "secretId"},
)
class GoogleContainerAzureClusterControlPlaneProxyConfig:
    def __init__(
        self,
        *,
        resource_group_id: builtins.str,
        secret_id: builtins.str,
    ) -> None:
        '''
        :param resource_group_id: The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#resource_group_id GoogleContainerAzureCluster#resource_group_id}
        :param secret_id: The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#secret_id GoogleContainerAzureCluster#secret_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286f25d5640c8f25018b1bba9d9c4b6573c88031036c67181f20a228d021ed64)
            check_type(argname="argument resource_group_id", value=resource_group_id, expected_type=type_hints["resource_group_id"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_group_id": resource_group_id,
            "secret_id": secret_id,
        }

    @builtins.property
    def resource_group_id(self) -> builtins.str:
        '''The ARM ID the of the resource group containing proxy keyvault. Resource group ids are formatted as ``/subscriptions/<subscription-id>/resourceGroups/<resource-group-name>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#resource_group_id GoogleContainerAzureCluster#resource_group_id}
        '''
        result = self._values.get("resource_group_id")
        assert result is not None, "Required property 'resource_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''The URL the of the proxy setting secret with its version. Secret ids are formatted as ``https:<key-vault-name>.vault.azure.net/secrets/<secret-name>/<secret-version>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#secret_id GoogleContainerAzureCluster#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterControlPlaneProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterControlPlaneProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98b558b9279cc00db4bc2ee7e860239f2671a583992b905d257f7796d88f69d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__552dcfd0addc0a948a0be947cb49fc3ab49cc21a6dbe350441ea339abbd7bf2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f053e5fe495540b8cc5a6fafbfb3e61660a07c3bb3454e2a4e826ed2d340acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterControlPlaneProxyConfig]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterControlPlaneProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterControlPlaneProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba751181ce5e96decd18d09e6c8faea403d964d9ba19f7344fe168b968209379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneReplicaPlacements",
    jsii_struct_bases=[],
    name_mapping={
        "azure_availability_zone": "azureAvailabilityZone",
        "subnet_id": "subnetId",
    },
)
class GoogleContainerAzureClusterControlPlaneReplicaPlacements:
    def __init__(
        self,
        *,
        azure_availability_zone: builtins.str,
        subnet_id: builtins.str,
    ) -> None:
        '''
        :param azure_availability_zone: For a given replica, the Azure availability zone where to provision the control plane VM and the ETCD disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#azure_availability_zone GoogleContainerAzureCluster#azure_availability_zone}
        :param subnet_id: For a given replica, the ARM ID of the subnet where the control plane VM is deployed. Make sure it's a subnet under the virtual network in the cluster configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#subnet_id GoogleContainerAzureCluster#subnet_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cbf4d9d15b80e409ecea34f9de389ad2111471a41443cddd2d37e1e38f5e328)
            check_type(argname="argument azure_availability_zone", value=azure_availability_zone, expected_type=type_hints["azure_availability_zone"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "azure_availability_zone": azure_availability_zone,
            "subnet_id": subnet_id,
        }

    @builtins.property
    def azure_availability_zone(self) -> builtins.str:
        '''For a given replica, the Azure availability zone where to provision the control plane VM and the ETCD disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#azure_availability_zone GoogleContainerAzureCluster#azure_availability_zone}
        '''
        result = self._values.get("azure_availability_zone")
        assert result is not None, "Required property 'azure_availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''For a given replica, the ARM ID of the subnet where the control plane VM is deployed.

        Make sure it's a subnet under the virtual network in the cluster configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#subnet_id GoogleContainerAzureCluster#subnet_id}
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterControlPlaneReplicaPlacements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterControlPlaneReplicaPlacementsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneReplicaPlacementsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd6bed46e4a15f34aa1eb120bca176ecc618221dbd215eab28c2a6998824cac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAzureClusterControlPlaneReplicaPlacementsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d839e9c41b6898b08d89ddbade2adf6f9012fd4e3ba31abfcdeb793cbe35f369)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAzureClusterControlPlaneReplicaPlacementsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d1cd62919369c88216461007537dbf9cb588c9b754d294061fb0e9514691f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a37511181cd231c453c59d5b012bd0c025292ecf6dedfc25b4c07793ee98b3b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b783ca098347d68cb2498ea6bbb9e08fb39491fdd864e61e9e12259553b4311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterControlPlaneReplicaPlacements]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterControlPlaneReplicaPlacements]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterControlPlaneReplicaPlacements]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff3c94a1d020f63053b39f741a7a3dd2768ba9a91cdc78401c6d4f1a84cefec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAzureClusterControlPlaneReplicaPlacementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneReplicaPlacementsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c104b666a929e0ad867e14e2d139059300f39aa1ec580e1240d2e0cca1ad91a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2d1f0e4eb5adb3b9c89524cc9ec39879b90166b91255b23a6e02c55c76c09e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureAvailabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37ded5eda369d896b2eacd78c5d0ceca5c949fbb704dd17be7bbf03f5c9bde9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterControlPlaneReplicaPlacements]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterControlPlaneReplicaPlacements]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterControlPlaneReplicaPlacements]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6498b45872cab7687baa9fd017c656dea229454c73a69fd0a2505d33f2809d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneRootVolume",
    jsii_struct_bases=[],
    name_mapping={"size_gib": "sizeGib"},
)
class GoogleContainerAzureClusterControlPlaneRootVolume:
    def __init__(self, *, size_gib: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param size_gib: Optional. The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#size_gib GoogleContainerAzureCluster#size_gib}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cfcf67df85cae8b7b319df5b52e688132f1c91186c50e10eca196ff4ee92b6)
            check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if size_gib is not None:
            self._values["size_gib"] = size_gib

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the disk, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#size_gib GoogleContainerAzureCluster#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterControlPlaneRootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterControlPlaneRootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneRootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04afbef1d544dce16db1301717b11b6fc657ebe2a5fc69985f08a59877b3cb7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d9f7714d086d915183488151ae8056e662521c27d11cf53206552fa13d062ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterControlPlaneRootVolume]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterControlPlaneRootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterControlPlaneRootVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9daaa04fc4f87d0164f3bc6ebdf4c5cee470b6b4793f6d50d064a702da2e47bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneSshConfig",
    jsii_struct_bases=[],
    name_mapping={"authorized_key": "authorizedKey"},
)
class GoogleContainerAzureClusterControlPlaneSshConfig:
    def __init__(self, *, authorized_key: builtins.str) -> None:
        '''
        :param authorized_key: The SSH public key data for VMs managed by Anthos. This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#authorized_key GoogleContainerAzureCluster#authorized_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7b17d5956833fa71536b9042f00314274b228b286908b57feb021b5affad74)
            check_type(argname="argument authorized_key", value=authorized_key, expected_type=type_hints["authorized_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorized_key": authorized_key,
        }

    @builtins.property
    def authorized_key(self) -> builtins.str:
        '''The SSH public key data for VMs managed by Anthos.

        This accepts the authorized_keys file format used in OpenSSH according to the sshd(8) manual page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#authorized_key GoogleContainerAzureCluster#authorized_key}
        '''
        result = self._values.get("authorized_key")
        assert result is not None, "Required property 'authorized_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterControlPlaneSshConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterControlPlaneSshConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterControlPlaneSshConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a07f24a6ecf8fd1c11ca40e2f4728e47cfa9ec7cd039a9a3275964630a5f12ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dbe531df977302f6d89a1aa8076dfb328532f321a3e9415ec4d849a1489befa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterControlPlaneSshConfig]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterControlPlaneSshConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterControlPlaneSshConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca125e29dc1c6c020167a0cd94c1f43a52a60ae259559a530bda050487c6ffdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterFleet",
    jsii_struct_bases=[],
    name_mapping={"project": "project"},
)
class GoogleContainerAzureClusterFleet:
    def __init__(self, *, project: typing.Optional[builtins.str] = None) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#project GoogleContainerAzureCluster#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11445d38daf7d00c441827575100ad21a15f7438b5f0052ce3d3ba585996e6da)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The number of the Fleet host project where this cluster will be registered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#project GoogleContainerAzureCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fdef21663e3004b4abe5e97252a8fa021dd3f983f0db1e6e652de862d977f5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__936ee6050cff22ae3373031aea5fcd8a9e6f0a7f9dd3735f41a129f2fb75eb42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAzureClusterFleet]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859b891d4c845f0506d07890fa48a55868b0b780a2d1e296de24f3b8129e424a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"component_config": "componentConfig"},
)
class GoogleContainerAzureClusterLoggingConfig:
    def __init__(
        self,
        *,
        component_config: typing.Optional[typing.Union["GoogleContainerAzureClusterLoggingConfigComponentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param component_config: component_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#component_config GoogleContainerAzureCluster#component_config}
        '''
        if isinstance(component_config, dict):
            component_config = GoogleContainerAzureClusterLoggingConfigComponentConfig(**component_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d9a1f1ab0c1f98311fcde96f67af5d3d14b1840f87ea217a259225af35c1b6)
            check_type(argname="argument component_config", value=component_config, expected_type=type_hints["component_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if component_config is not None:
            self._values["component_config"] = component_config

    @builtins.property
    def component_config(
        self,
    ) -> typing.Optional["GoogleContainerAzureClusterLoggingConfigComponentConfig"]:
        '''component_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#component_config GoogleContainerAzureCluster#component_config}
        '''
        result = self._values.get("component_config")
        return typing.cast(typing.Optional["GoogleContainerAzureClusterLoggingConfigComponentConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterLoggingConfigComponentConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_components": "enableComponents"},
)
class GoogleContainerAzureClusterLoggingConfigComponentConfig:
    def __init__(
        self,
        *,
        enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_components: Components of the logging configuration to be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#enable_components GoogleContainerAzureCluster#enable_components}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff2910b08d5688c26853cec4e2021a6d06a8ab9667020c9182d6e2245e2ad2d)
            check_type(argname="argument enable_components", value=enable_components, expected_type=type_hints["enable_components"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_components is not None:
            self._values["enable_components"] = enable_components

    @builtins.property
    def enable_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Components of the logging configuration to be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#enable_components GoogleContainerAzureCluster#enable_components}
        '''
        result = self._values.get("enable_components")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterLoggingConfigComponentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterLoggingConfigComponentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterLoggingConfigComponentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a981ac2d5908882f1d017b00ce96a2ef8d259cbe6bc40201348aee077577c32f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableComponents")
    def reset_enable_components(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableComponents", []))

    @builtins.property
    @jsii.member(jsii_name="enableComponentsInput")
    def enable_components_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enableComponentsInput"))

    @builtins.property
    @jsii.member(jsii_name="enableComponents")
    def enable_components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enableComponents"))

    @enable_components.setter
    def enable_components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab143404aa450047641b977e8b80960a52354c9a2f9b5c19cc0b9178e7a1224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableComponents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterLoggingConfigComponentConfig]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterLoggingConfigComponentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterLoggingConfigComponentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f330f671940e738c0f579f73468bcd51e6ffb9f88fd7625a67e60760955e0e0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAzureClusterLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef3669ac9893de3de99779de8728a98775245466d6903f48d044c947a8d31a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putComponentConfig")
    def put_component_config(
        self,
        *,
        enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_components: Components of the logging configuration to be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#enable_components GoogleContainerAzureCluster#enable_components}
        '''
        value = GoogleContainerAzureClusterLoggingConfigComponentConfig(
            enable_components=enable_components
        )

        return typing.cast(None, jsii.invoke(self, "putComponentConfig", [value]))

    @jsii.member(jsii_name="resetComponentConfig")
    def reset_component_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComponentConfig", []))

    @builtins.property
    @jsii.member(jsii_name="componentConfig")
    def component_config(
        self,
    ) -> GoogleContainerAzureClusterLoggingConfigComponentConfigOutputReference:
        return typing.cast(GoogleContainerAzureClusterLoggingConfigComponentConfigOutputReference, jsii.get(self, "componentConfig"))

    @builtins.property
    @jsii.member(jsii_name="componentConfigInput")
    def component_config_input(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterLoggingConfigComponentConfig]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterLoggingConfigComponentConfig], jsii.get(self, "componentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAzureClusterLoggingConfig]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a082a5448f1374576ee05feb63ce67a47a41eedc6778bd603bca8c1a2f1244d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterNetworking",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
        "virtual_network_id": "virtualNetworkId",
    },
)
class GoogleContainerAzureClusterNetworking:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        virtual_network_id: builtins.str,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: The IP address range of the pods in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All pods in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#pod_address_cidr_blocks GoogleContainerAzureCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: The IP address range for services in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All services in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creating a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#service_address_cidr_blocks GoogleContainerAzureCluster#service_address_cidr_blocks}
        :param virtual_network_id: The Azure Resource Manager (ARM) ID of the VNet associated with your cluster. All components in the cluster (i.e. control plane and node pools) run on a single VNet. Example: ``/subscriptions/* /resourceGroups/* /providers/Microsoft.Network/virtualNetworks/*`` This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#virtual_network_id GoogleContainerAzureCluster#virtual_network_id} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4f510031fdf41f8b83c2a9fdb050e22c641e96cbd7d8f37d32a75c33a5785a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#pod_address_cidr_blocks GoogleContainerAzureCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''The IP address range for services in this cluster, in CIDR notation (e.g. ``10.96.0.0/14``). All services in the cluster get assigned a unique RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creating a cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#service_address_cidr_blocks GoogleContainerAzureCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def virtual_network_id(self) -> builtins.str:
        '''The Azure Resource Manager (ARM) ID of the VNet associated with your cluster.

        All components in the cluster (i.e. control plane and node pools) run on a single VNet. Example: ``/subscriptions/* /resourceGroups/* /providers/Microsoft.Network/virtualNetworks/*`` This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#virtual_network_id GoogleContainerAzureCluster#virtual_network_id}

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
        return "GoogleContainerAzureClusterNetworking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterNetworkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterNetworkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4f388de96fcbb56e53c216671de828c72302992b0bbea25ded8009e2aa059f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__570e30e5b9fb781ce71dce0fbdb3ae33dfa8d75b82d4b0a95c9813fdbeb01823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e0f614e80fd47d2f9b8eca3f69fd6498ac27846e294720badc1b2a8658277c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkId")
    def virtual_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkId"))

    @virtual_network_id.setter
    def virtual_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba9f275af9cbf78802bb14ff0595ca31c755d5dee53b4a67726b7346ce8a4ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAzureClusterNetworking]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterNetworking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterNetworking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc48fd681cdbba5952e6bb3e23cef3e015efd1cac817e51772468e478871606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleContainerAzureClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#create GoogleContainerAzureCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#delete GoogleContainerAzureCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#update GoogleContainerAzureCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f312ef413eae4d71300bcc8a80dd424b5c4abaa4e28c93b04a170ab99d03d382)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#create GoogleContainerAzureCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#delete GoogleContainerAzureCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_azure_cluster#update GoogleContainerAzureCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aadac0f3e7af7b50437330a8076f29da2f572908926dfbb0106006ca3d81686)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2765c09a4def3fa518f9af6ae85b4d430ab083ba5ac8cd836f0e89197e610ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12afcbd0b2a643fe193e2d0b6200645cded7cada073a04339caff2ef90296664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd2b63ab01f39050b520b57452e2a63835a62c607afa9f4f094f7ad5e9b5387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901a0c5a8df9481d7021d4f4a7e86ba5361f5b7587eaddc9610061ddf9c7fc6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterWorkloadIdentityConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleContainerAzureClusterWorkloadIdentityConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAzureClusterWorkloadIdentityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAzureClusterWorkloadIdentityConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterWorkloadIdentityConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed7669ce63e413ed1c715eaebdd8c9d75c975743255498b8a4c8de5bedb5cdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAzureClusterWorkloadIdentityConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90824ffae51ab7343dcc54b793275132fed0131c24c1a3315d79a6d1887553af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAzureClusterWorkloadIdentityConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c959ef3a914e78df635c839723bd19baebcadd27d88c27970c66c655b6c1fd46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f3711664f429678a31e14ad1f17dc9824e04c1b7701cdf52746c610ba0a648a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1dfd4a4de224cd6996443a886b90029159cafb0af68a63122fcb8112ce65b47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAzureClusterWorkloadIdentityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAzureCluster.GoogleContainerAzureClusterWorkloadIdentityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1b4339ac7d069c319746d55c2a315b20a71f1cf8fb50bd7152afe290060f0d5)
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
    ) -> typing.Optional[GoogleContainerAzureClusterWorkloadIdentityConfig]:
        return typing.cast(typing.Optional[GoogleContainerAzureClusterWorkloadIdentityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAzureClusterWorkloadIdentityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b460cfe1ccd32ba09725adbca22c56c97c2efcd3ea60c3ab3497197295ecacf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleContainerAzureCluster",
    "GoogleContainerAzureClusterAuthorization",
    "GoogleContainerAzureClusterAuthorizationAdminGroups",
    "GoogleContainerAzureClusterAuthorizationAdminGroupsList",
    "GoogleContainerAzureClusterAuthorizationAdminGroupsOutputReference",
    "GoogleContainerAzureClusterAuthorizationAdminUsers",
    "GoogleContainerAzureClusterAuthorizationAdminUsersList",
    "GoogleContainerAzureClusterAuthorizationAdminUsersOutputReference",
    "GoogleContainerAzureClusterAuthorizationOutputReference",
    "GoogleContainerAzureClusterAzureServicesAuthentication",
    "GoogleContainerAzureClusterAzureServicesAuthenticationOutputReference",
    "GoogleContainerAzureClusterConfig",
    "GoogleContainerAzureClusterControlPlane",
    "GoogleContainerAzureClusterControlPlaneDatabaseEncryption",
    "GoogleContainerAzureClusterControlPlaneDatabaseEncryptionOutputReference",
    "GoogleContainerAzureClusterControlPlaneMainVolume",
    "GoogleContainerAzureClusterControlPlaneMainVolumeOutputReference",
    "GoogleContainerAzureClusterControlPlaneOutputReference",
    "GoogleContainerAzureClusterControlPlaneProxyConfig",
    "GoogleContainerAzureClusterControlPlaneProxyConfigOutputReference",
    "GoogleContainerAzureClusterControlPlaneReplicaPlacements",
    "GoogleContainerAzureClusterControlPlaneReplicaPlacementsList",
    "GoogleContainerAzureClusterControlPlaneReplicaPlacementsOutputReference",
    "GoogleContainerAzureClusterControlPlaneRootVolume",
    "GoogleContainerAzureClusterControlPlaneRootVolumeOutputReference",
    "GoogleContainerAzureClusterControlPlaneSshConfig",
    "GoogleContainerAzureClusterControlPlaneSshConfigOutputReference",
    "GoogleContainerAzureClusterFleet",
    "GoogleContainerAzureClusterFleetOutputReference",
    "GoogleContainerAzureClusterLoggingConfig",
    "GoogleContainerAzureClusterLoggingConfigComponentConfig",
    "GoogleContainerAzureClusterLoggingConfigComponentConfigOutputReference",
    "GoogleContainerAzureClusterLoggingConfigOutputReference",
    "GoogleContainerAzureClusterNetworking",
    "GoogleContainerAzureClusterNetworkingOutputReference",
    "GoogleContainerAzureClusterTimeouts",
    "GoogleContainerAzureClusterTimeoutsOutputReference",
    "GoogleContainerAzureClusterWorkloadIdentityConfig",
    "GoogleContainerAzureClusterWorkloadIdentityConfigList",
    "GoogleContainerAzureClusterWorkloadIdentityConfigOutputReference",
]

publication.publish()

def _typecheckingstub__6f832561e1296062901c1dd06b3e3c42bae31efcf7577ef56fdd6171e3929fbe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization: typing.Union[GoogleContainerAzureClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    azure_region: builtins.str,
    control_plane: typing.Union[GoogleContainerAzureClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[GoogleContainerAzureClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[GoogleContainerAzureClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    resource_group_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    azure_services_authentication: typing.Optional[typing.Union[GoogleContainerAzureClusterAzureServicesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[GoogleContainerAzureClusterLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAzureClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e327754b623f234aed311dddd892dc4d2d78a876f256b87cf27dd474798bca41(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855d9eae150ca7358b3e2185c5bc159cf421ec960702c36fec9074d3e4ce6467(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8bcb44d10c61b9d8ffa04e04475fddf21635ff37f5746b5be8d796433edca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265b7507e8d672aef0b9075d578edbc987a965c9369a3d9456b5b796c35505ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ea104da716818e31c905e5dd50aa4ca9197c90594b743f8e6888b316f8888c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fce849d094c48fe91a2b2038910a4dbcd2cb0cca04d1855e75b0569f1a36a92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56dcea84ce4ce8a4b0530d38c29cee784b0c73bf73993668af5781573222100(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed139e283a5cde135a8627eff7a2876c59791ac3b9fffe0be823bcad0e75cdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c61ecf1b4808cc34c5bde9ebe5a4db8bd5347dcfbc5617a32e52af4806400b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b639f9873a50c67d9e1692228e29d09872797e802ed72e22e56819831d2c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df80c996004bf0c028b988636f281ee13c0e57d6349b684583850b1181a36b1(
    *,
    admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAzureClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAzureClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0a043c2a0201245242962a62f44c6886f5da2f5af68f6ccf6a4e71d81532eb(
    *,
    group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bb015b08a6cc55f032e65c53cb9341ac32ad74b7eb488acc46c7550d019b86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d371c4d619d9954fb40d070c16317d43ae2d7e9e3a8845b18ad2a6ebb2c001a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b7f33814f0434dc5a982884bf31172a657290b912ee6390370bf60b447e6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec2cb545e7b3c3e1b67529a38b79787bf9a6cdf813ec01cf7b17a1c8a3f4f2f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae555424cc25cee19e534d842fafdd403ba388d4d981af124831796b87a3b8e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b53f5edd8efe9dbdccaf3c328410f17a7a6715934fb7aa3a32500c5bb18451(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4503c77ba37c4d654bf9a243607fe0019fbcce4c425c06b67be0cddb11bfa9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f05e4fa728abfbe98fc7d7bbd62338a9f923e393ca04bdba7b830c201bdb06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c361a02c81a430974e4f37cb177943d692c564c8ae2802156f7f996aeea4942(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterAuthorizationAdminGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8574e7f8b3111a2517c1266862c90ea7d37d83b77d8642f46db613c4f8b89da4(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4595df510ca9bf5929db49faf13c229ce540f2f42d2f7f0b83e5ba1ba9f5db40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a10a40d50d47fbb3c09a3bda1780bb0bb25d95568e30c409479fe5dbab0914e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9abceec4599240df98638ec781adf8bd0b410cc31156348128e1b6bd709f14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e398cdfd9187baf525a8e37dce2c93b68e3bedef8a2d6b8cc22577c7c966ba9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb269321ae749221d9d0f1e9ef951d24af265eb1750a5ec875658bb2dac5d7d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282e1d0aecdfd90bebfa9e71041b4dfae2cb314f47ffc564d2c912d52aa0698d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24e2a633efa0f344bac1acf14eac89d61b73e1bff1d4542318f9b3b91b10e6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13d9ce91daa8450456519a84c1416d4efa9bbab656c68da88d6a0de2164c81c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a4f7527c50c5d87bbd965d1bcf9e37f1b893bca7d08117bf608b4690eafcd3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75b1bcc0c68a4e915fb625586b8ca4ab9379b40be1e40853c550ebcfeef1df0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01e761c93615a5350d78a5149866edb3e669209ea786cf65d672564679a301b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAzureClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b485f75789480e1665f42157c02939727ae8e136fc43ef72cf524772e471b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAzureClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a36c04c0d676032db41af0e4727de0ee98b7e0a44d6a0dee8e5874fb0db7af(
    value: typing.Optional[GoogleContainerAzureClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c951f40988a4b87861b3bb73a7f6a110fe8d97a5e5f173bade1dda73d15d948f(
    *,
    application_id: builtins.str,
    tenant_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41087aec097aa3d546dd00d0ff2b8e55ea8c6e7ca2d69ffa96bc6433eeb77cfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b177ddd25ece80c4cb862417cdf20775ba3233f3a42f1d05efd6fa9c370d616f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5b2d2f39aaa5d873cd475b42084afa7273d37b5319ce9da4cace521c8a8aca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc92b8c5b5408f815edd44ab698eb01763caf346cf69a2dafdc9a59b1fc4b20d(
    value: typing.Optional[GoogleContainerAzureClusterAzureServicesAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6da5163c6a69cb7728506a93ed722079ca0cc80d04054345d8dc7111dd4dbca(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization: typing.Union[GoogleContainerAzureClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    azure_region: builtins.str,
    control_plane: typing.Union[GoogleContainerAzureClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[GoogleContainerAzureClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[GoogleContainerAzureClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    resource_group_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    azure_services_authentication: typing.Optional[typing.Union[GoogleContainerAzureClusterAzureServicesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[GoogleContainerAzureClusterLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAzureClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be16250f126926182c485593fcc235b9121cf3c52e84cab4b39927733b617553(
    *,
    ssh_config: typing.Union[GoogleContainerAzureClusterControlPlaneSshConfig, typing.Dict[builtins.str, typing.Any]],
    subnet_id: builtins.str,
    version: builtins.str,
    database_encryption: typing.Optional[typing.Union[GoogleContainerAzureClusterControlPlaneDatabaseEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    main_volume: typing.Optional[typing.Union[GoogleContainerAzureClusterControlPlaneMainVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    proxy_config: typing.Optional[typing.Union[GoogleContainerAzureClusterControlPlaneProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    replica_placements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAzureClusterControlPlaneReplicaPlacements, typing.Dict[builtins.str, typing.Any]]]]] = None,
    root_volume: typing.Optional[typing.Union[GoogleContainerAzureClusterControlPlaneRootVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vm_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb9776e8bb66649d88eba6b51c3c8ab437526c88b364ab6dd973a371d3dd15d(
    *,
    key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b837ac4e6df7174c236254e31645787a51a65461ae8d73faefcc05364d750c79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0227e2bac0dfa9d75d40914751a689a3608a31fea5a3992fc6a47dbff96323e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24399b26c077c26ddccfbb6431180fbb71c53459fc238b5955c76341a98e0503(
    value: typing.Optional[GoogleContainerAzureClusterControlPlaneDatabaseEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750dda3f725d714ace9ec4441623c559d84632236dcf78b44f33a47a04e41efc(
    *,
    size_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0353f33345fdc0db433ea550a350cff5201bbcb6ddbca674f49a7f6ced3d219(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a28d622947b023a104dd0d5cf61bc902cbd54e9d6df91325b7036fe891a104f6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d74dcab1cbb9f82bee2cd0fc58955d45bde0adf90f1cbd662986a6e29ce0af(
    value: typing.Optional[GoogleContainerAzureClusterControlPlaneMainVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5485600f02db32e9eaba712871f363e3b29c9c90fa769c1d7ea0aefd14a60372(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd908d0cb950190570a1b87ec7e19825e00a2dd98e5aa5bc7f490b6a35876cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAzureClusterControlPlaneReplicaPlacements, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46197fbbe05a0d22729d63400542170bc54386a374693701bb49c309b2b2990(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f38ca7d7055ea0e011a4766537436315b9f1784f5aad7a66bb095d90ce90c6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfcf3296804a682a07ea00424c387f1a78144c3215c05813bff369084f16f0aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6d41ed00544581fb5604b224143a2e233892675ee971c78c2385edab33b5e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7f868bbc08022a1ac7b77d000142fbaff00165134d9ff4d03b2f90a49457ed(
    value: typing.Optional[GoogleContainerAzureClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286f25d5640c8f25018b1bba9d9c4b6573c88031036c67181f20a228d021ed64(
    *,
    resource_group_id: builtins.str,
    secret_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b558b9279cc00db4bc2ee7e860239f2671a583992b905d257f7796d88f69d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552dcfd0addc0a948a0be947cb49fc3ab49cc21a6dbe350441ea339abbd7bf2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f053e5fe495540b8cc5a6fafbfb3e61660a07c3bb3454e2a4e826ed2d340acc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba751181ce5e96decd18d09e6c8faea403d964d9ba19f7344fe168b968209379(
    value: typing.Optional[GoogleContainerAzureClusterControlPlaneProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cbf4d9d15b80e409ecea34f9de389ad2111471a41443cddd2d37e1e38f5e328(
    *,
    azure_availability_zone: builtins.str,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd6bed46e4a15f34aa1eb120bca176ecc618221dbd215eab28c2a6998824cac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d839e9c41b6898b08d89ddbade2adf6f9012fd4e3ba31abfcdeb793cbe35f369(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d1cd62919369c88216461007537dbf9cb588c9b754d294061fb0e9514691f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37511181cd231c453c59d5b012bd0c025292ecf6dedfc25b4c07793ee98b3b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b783ca098347d68cb2498ea6bbb9e08fb39491fdd864e61e9e12259553b4311(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff3c94a1d020f63053b39f741a7a3dd2768ba9a91cdc78401c6d4f1a84cefec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAzureClusterControlPlaneReplicaPlacements]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c104b666a929e0ad867e14e2d139059300f39aa1ec580e1240d2e0cca1ad91a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d1f0e4eb5adb3b9c89524cc9ec39879b90166b91255b23a6e02c55c76c09e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37ded5eda369d896b2eacd78c5d0ceca5c949fbb704dd17be7bbf03f5c9bde9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6498b45872cab7687baa9fd017c656dea229454c73a69fd0a2505d33f2809d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterControlPlaneReplicaPlacements]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cfcf67df85cae8b7b319df5b52e688132f1c91186c50e10eca196ff4ee92b6(
    *,
    size_gib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04afbef1d544dce16db1301717b11b6fc657ebe2a5fc69985f08a59877b3cb7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9f7714d086d915183488151ae8056e662521c27d11cf53206552fa13d062ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9daaa04fc4f87d0164f3bc6ebdf4c5cee470b6b4793f6d50d064a702da2e47bd(
    value: typing.Optional[GoogleContainerAzureClusterControlPlaneRootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7b17d5956833fa71536b9042f00314274b228b286908b57feb021b5affad74(
    *,
    authorized_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07f24a6ecf8fd1c11ca40e2f4728e47cfa9ec7cd039a9a3275964630a5f12ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbe531df977302f6d89a1aa8076dfb328532f321a3e9415ec4d849a1489befa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca125e29dc1c6c020167a0cd94c1f43a52a60ae259559a530bda050487c6ffdf(
    value: typing.Optional[GoogleContainerAzureClusterControlPlaneSshConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11445d38daf7d00c441827575100ad21a15f7438b5f0052ce3d3ba585996e6da(
    *,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdef21663e3004b4abe5e97252a8fa021dd3f983f0db1e6e652de862d977f5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936ee6050cff22ae3373031aea5fcd8a9e6f0a7f9dd3735f41a129f2fb75eb42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859b891d4c845f0506d07890fa48a55868b0b780a2d1e296de24f3b8129e424a(
    value: typing.Optional[GoogleContainerAzureClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d9a1f1ab0c1f98311fcde96f67af5d3d14b1840f87ea217a259225af35c1b6(
    *,
    component_config: typing.Optional[typing.Union[GoogleContainerAzureClusterLoggingConfigComponentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff2910b08d5688c26853cec4e2021a6d06a8ab9667020c9182d6e2245e2ad2d(
    *,
    enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a981ac2d5908882f1d017b00ce96a2ef8d259cbe6bc40201348aee077577c32f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab143404aa450047641b977e8b80960a52354c9a2f9b5c19cc0b9178e7a1224(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f330f671940e738c0f579f73468bcd51e6ffb9f88fd7625a67e60760955e0e0f(
    value: typing.Optional[GoogleContainerAzureClusterLoggingConfigComponentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef3669ac9893de3de99779de8728a98775245466d6903f48d044c947a8d31a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a082a5448f1374576ee05feb63ce67a47a41eedc6778bd603bca8c1a2f1244d(
    value: typing.Optional[GoogleContainerAzureClusterLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4f510031fdf41f8b83c2a9fdb050e22c641e96cbd7d8f37d32a75c33a5785a(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
    virtual_network_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f388de96fcbb56e53c216671de828c72302992b0bbea25ded8009e2aa059f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570e30e5b9fb781ce71dce0fbdb3ae33dfa8d75b82d4b0a95c9813fdbeb01823(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e0f614e80fd47d2f9b8eca3f69fd6498ac27846e294720badc1b2a8658277c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba9f275af9cbf78802bb14ff0595ca31c755d5dee53b4a67726b7346ce8a4ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc48fd681cdbba5952e6bb3e23cef3e015efd1cac817e51772468e478871606(
    value: typing.Optional[GoogleContainerAzureClusterNetworking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f312ef413eae4d71300bcc8a80dd424b5c4abaa4e28c93b04a170ab99d03d382(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aadac0f3e7af7b50437330a8076f29da2f572908926dfbb0106006ca3d81686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2765c09a4def3fa518f9af6ae85b4d430ab083ba5ac8cd836f0e89197e610ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12afcbd0b2a643fe193e2d0b6200645cded7cada073a04339caff2ef90296664(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd2b63ab01f39050b520b57452e2a63835a62c607afa9f4f094f7ad5e9b5387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901a0c5a8df9481d7021d4f4a7e86ba5361f5b7587eaddc9610061ddf9c7fc6d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAzureClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed7669ce63e413ed1c715eaebdd8c9d75c975743255498b8a4c8de5bedb5cdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90824ffae51ab7343dcc54b793275132fed0131c24c1a3315d79a6d1887553af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c959ef3a914e78df635c839723bd19baebcadd27d88c27970c66c655b6c1fd46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3711664f429678a31e14ad1f17dc9824e04c1b7701cdf52746c610ba0a648a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dfd4a4de224cd6996443a886b90029159cafb0af68a63122fcb8112ce65b47(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b4339ac7d069c319746d55c2a315b20a71f1cf8fb50bd7152afe290060f0d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b460cfe1ccd32ba09725adbca22c56c97c2efcd3ea60c3ab3497197295ecacf(
    value: typing.Optional[GoogleContainerAzureClusterWorkloadIdentityConfig],
) -> None:
    """Type checking stubs"""
    pass
