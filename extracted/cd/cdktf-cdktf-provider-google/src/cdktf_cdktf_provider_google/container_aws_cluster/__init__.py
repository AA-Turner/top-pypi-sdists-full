r'''
# `google_container_aws_cluster`

Refer to the Terraform Registry for docs: [`google_container_aws_cluster`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster).
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


class ContainerAwsCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster google_container_aws_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization: typing.Union["ContainerAwsClusterAuthorization", typing.Dict[builtins.str, typing.Any]],
        aws_region: builtins.str,
        control_plane: typing.Union["ContainerAwsClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["ContainerAwsClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["ContainerAwsClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union["ContainerAwsClusterBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAwsClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster google_container_aws_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#authorization ContainerAwsCluster#authorization}
        :param aws_region: The AWS region where the cluster runs. Each Google Cloud region supports a subset of nearby AWS regions. You can call to list all supported AWS regions within a given Google Cloud region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#aws_region ContainerAwsCluster#aws_region}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#control_plane ContainerAwsCluster#control_plane}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#fleet ContainerAwsCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#location ContainerAwsCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#name ContainerAwsCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#networking ContainerAwsCluster#networking}
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#annotations ContainerAwsCluster#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#binary_authorization ContainerAwsCluster#binary_authorization}
        :param description: Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#description ContainerAwsCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#id ContainerAwsCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#project ContainerAwsCluster#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#timeouts ContainerAwsCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5403434afce948419e99fc6044f81c8e2fe9eae277f50bf4358fd8bde54813)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerAwsClusterConfig(
            authorization=authorization,
            aws_region=aws_region,
            control_plane=control_plane,
            fleet=fleet,
            location=location,
            name=name,
            networking=networking,
            annotations=annotations,
            binary_authorization=binary_authorization,
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
        '''Generates CDKTF code for importing a ContainerAwsCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAwsCluster to import.
        :param import_from_id: The id of the existing ContainerAwsCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAwsCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0deeb78c047bb6241b1f9a0e5f09e45743fac19fb53c4ccd494ae61885449453)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAwsClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
        admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAwsClusterAuthorizationAdminGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#admin_users ContainerAwsCluster#admin_users}
        :param admin_groups: admin_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#admin_groups ContainerAwsCluster#admin_groups}
        '''
        value = ContainerAwsClusterAuthorization(
            admin_users=admin_users, admin_groups=admin_groups
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="putBinaryAuthorization")
    def put_binary_authorization(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for Binary Authorization policy evaluation. Possible values: DISABLED, PROJECT_SINGLETON_POLICY_ENFORCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#evaluation_mode ContainerAwsCluster#evaluation_mode}
        '''
        value = ContainerAwsClusterBinaryAuthorization(evaluation_mode=evaluation_mode)

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        aws_services_authentication: typing.Union["ContainerAwsClusterControlPlaneAwsServicesAuthentication", typing.Dict[builtins.str, typing.Any]],
        config_encryption: typing.Union["ContainerAwsClusterControlPlaneConfigEncryption", typing.Dict[builtins.str, typing.Any]],
        database_encryption: typing.Union["ContainerAwsClusterControlPlaneDatabaseEncryption", typing.Dict[builtins.str, typing.Any]],
        iam_instance_profile: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        version: builtins.str,
        instance_type: typing.Optional[builtins.str] = None,
        main_volume: typing.Optional[typing.Union["ContainerAwsClusterControlPlaneMainVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAwsClusterControlPlaneProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["ContainerAwsClusterControlPlaneRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_config: typing.Optional[typing.Union["ContainerAwsClusterControlPlaneSshConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param aws_services_authentication: aws_services_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#aws_services_authentication ContainerAwsCluster#aws_services_authentication}
        :param config_encryption: config_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#config_encryption ContainerAwsCluster#config_encryption}
        :param database_encryption: database_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#database_encryption ContainerAwsCluster#database_encryption}
        :param iam_instance_profile: The name of the AWS IAM instance pofile to assign to each control plane replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iam_instance_profile ContainerAwsCluster#iam_instance_profile}
        :param subnet_ids: The list of subnets where control plane replicas will run. A replica will be provisioned on each subnet and up to three values can be provided. Each subnet must be in a different AWS Availability Zone (AZ). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#subnet_ids ContainerAwsCluster#subnet_ids}
        :param version: The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#version ContainerAwsCluster#version}
        :param instance_type: Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#instance_type ContainerAwsCluster#instance_type}
        :param main_volume: main_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#main_volume ContainerAwsCluster#main_volume}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#proxy_config ContainerAwsCluster#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#root_volume ContainerAwsCluster#root_volume}
        :param security_group_ids: Optional. The IDs of additional security groups to add to control plane replicas. The Anthos Multi-Cloud API will automatically create and manage security groups with the minimum rules needed for a functioning cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#security_group_ids ContainerAwsCluster#security_group_ids}
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#ssh_config ContainerAwsCluster#ssh_config}
        :param tags: Optional. A set of AWS resource tags to propagate to all underlying managed AWS resources. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#tags ContainerAwsCluster#tags}
        '''
        value = ContainerAwsClusterControlPlane(
            aws_services_authentication=aws_services_authentication,
            config_encryption=config_encryption,
            database_encryption=database_encryption,
            iam_instance_profile=iam_instance_profile,
            subnet_ids=subnet_ids,
            version=version,
            instance_type=instance_type,
            main_volume=main_volume,
            proxy_config=proxy_config,
            root_volume=root_volume,
            security_group_ids=security_group_ids,
            ssh_config=ssh_config,
            tags=tags,
        )

        return typing.cast(None, jsii.invoke(self, "putControlPlane", [value]))

    @jsii.member(jsii_name="putFleet")
    def put_fleet(self, *, project: typing.Optional[builtins.str] = None) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#project ContainerAwsCluster#project}
        '''
        value = ContainerAwsClusterFleet(project=project)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putNetworking")
    def put_networking(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
        per_node_pool_sg_rules_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#pod_address_cidr_blocks ContainerAwsCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#service_address_cidr_blocks ContainerAwsCluster#service_address_cidr_blocks}
        :param vpc_id: The VPC associated with the cluster. All component clusters (i.e. control plane and node pools) run on a single VPC. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#vpc_id ContainerAwsCluster#vpc_id}
        :param per_node_pool_sg_rules_disabled: Disable the per node pool subnet security group rules on the control plane security group. When set to true, you must also provide one or more security groups that ensure node pools are able to send requests to the control plane on TCP/443 and TCP/8132. Failure to do so may result in unavailable node pools. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#per_node_pool_sg_rules_disabled ContainerAwsCluster#per_node_pool_sg_rules_disabled}
        '''
        value = ContainerAwsClusterNetworking(
            pod_address_cidr_blocks=pod_address_cidr_blocks,
            service_address_cidr_blocks=service_address_cidr_blocks,
            vpc_id=vpc_id,
            per_node_pool_sg_rules_disabled=per_node_pool_sg_rules_disabled,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#create ContainerAwsCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#delete ContainerAwsCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#update ContainerAwsCluster#update}.
        '''
        value = ContainerAwsClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBinaryAuthorization")
    def reset_binary_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorization", []))

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
    def authorization(self) -> "ContainerAwsClusterAuthorizationOutputReference":
        return typing.cast("ContainerAwsClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorization")
    def binary_authorization(
        self,
    ) -> "ContainerAwsClusterBinaryAuthorizationOutputReference":
        return typing.cast("ContainerAwsClusterBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> "ContainerAwsClusterControlPlaneOutputReference":
        return typing.cast("ContainerAwsClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

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
    def fleet(self) -> "ContainerAwsClusterFleetOutputReference":
        return typing.cast("ContainerAwsClusterFleetOutputReference", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="networking")
    def networking(self) -> "ContainerAwsClusterNetworkingOutputReference":
        return typing.cast("ContainerAwsClusterNetworkingOutputReference", jsii.get(self, "networking"))

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
    def timeouts(self) -> "ContainerAwsClusterTimeoutsOutputReference":
        return typing.cast("ContainerAwsClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> "ContainerAwsClusterWorkloadIdentityConfigList":
        return typing.cast("ContainerAwsClusterWorkloadIdentityConfigList", jsii.get(self, "workloadIdentityConfig"))

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
    ) -> typing.Optional["ContainerAwsClusterAuthorization"]:
        return typing.cast(typing.Optional["ContainerAwsClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegionInput")
    def aws_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationInput")
    def binary_authorization_input(
        self,
    ) -> typing.Optional["ContainerAwsClusterBinaryAuthorization"]:
        return typing.cast(typing.Optional["ContainerAwsClusterBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(self) -> typing.Optional["ContainerAwsClusterControlPlane"]:
        return typing.cast(typing.Optional["ContainerAwsClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetInput")
    def fleet_input(self) -> typing.Optional["ContainerAwsClusterFleet"]:
        return typing.cast(typing.Optional["ContainerAwsClusterFleet"], jsii.get(self, "fleetInput"))

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
    def networking_input(self) -> typing.Optional["ContainerAwsClusterNetworking"]:
        return typing.cast(typing.Optional["ContainerAwsClusterNetworking"], jsii.get(self, "networkingInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAwsClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAwsClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159adcd002b48eac55a52764b029458eda73a617a800847b76b64ee28ac00027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a07649d99c121f7e7d458fed96c016da7cca05401397975b8e452941bc0621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2503e81249e9002e2bd74f26c33b7052a6aa4da2a66e27776cb303004949b8b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f91883033675255d5fbd63cacd96421354ceea953271d818638775dedadc0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945146b8fbffb9f7f1d63652b718e87b811d32fb6aec90868e8eccff6de1734c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb4939dcad1f003a73a63bf733f31305991268a9f1bf93ab1a4cc2e4f1eb7ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90177da73bbbd9585da69fae9899f7e6dd495b53a44da6ab78eba66e37389205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers", "admin_groups": "adminGroups"},
)
class ContainerAwsClusterAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAwsClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
        admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAwsClusterAuthorizationAdminGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#admin_users ContainerAwsCluster#admin_users}
        :param admin_groups: admin_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#admin_groups ContainerAwsCluster#admin_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf0099a6cad5d06cfff9deeab64e906db1ced5328819fc3155b1ad840ba9097)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAwsClusterAuthorizationAdminUsers"]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#admin_users ContainerAwsCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAwsClusterAuthorizationAdminUsers"]], result)

    @builtins.property
    def admin_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAwsClusterAuthorizationAdminGroups"]]]:
        '''admin_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#admin_groups ContainerAwsCluster#admin_groups}
        '''
        result = self._values.get("admin_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAwsClusterAuthorizationAdminGroups"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterAuthorizationAdminGroups",
    jsii_struct_bases=[],
    name_mapping={"group": "group"},
)
class ContainerAwsClusterAuthorizationAdminGroups:
    def __init__(self, *, group: builtins.str) -> None:
        '''
        :param group: The name of the group, e.g. ``my-group@domain.com``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#group ContainerAwsCluster#group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791368bc52b403f619b003463687b530ea28d6a6d624a0f91415d8ecce300f63)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
        }

    @builtins.property
    def group(self) -> builtins.str:
        '''The name of the group, e.g. ``my-group@domain.com``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#group ContainerAwsCluster#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterAuthorizationAdminGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterAuthorizationAdminGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterAuthorizationAdminGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1eb69d05d5691ab66510d479a747089f5f3c2a4da329a7c60e6c04bd82dc774e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAwsClusterAuthorizationAdminGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6a88491c0992d533f4bf59a90ff422e0c307778bd5a43f73c1d179fa9fb8e7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAwsClusterAuthorizationAdminGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ece578f9f3c8d5b6a875700cd2ea656cb0b58fc6d0f57d2bcab4cc614d08e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8d4eec84c7e43bd174701035614512f26408a8d7cff869817821026425e19c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67299d0c6ce226b3fe84af7510ac104fdc1d284c18e7fbc9ca626d9fc79eaf78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b418802aa5938b2bc4880e2789a3a3d8238f1aeb6f5d214e3da5560ef8515a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAwsClusterAuthorizationAdminGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterAuthorizationAdminGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e09d306ac7a0a2d2044f418db06639791b78ca9ab8fe2a9ac618b15853d28e51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__219543d11a2cd2d5ede7482880d1d1b44360ff80bbd018f7805f3ce74047d193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterAuthorizationAdminGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterAuthorizationAdminGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterAuthorizationAdminGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71f8b0b02d9de58a2a65cab1b844fc770742253fb53599a5bfcd3a9ee2e0586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class ContainerAwsClusterAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. ``my-gcp-id@gmail.com``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#username ContainerAwsCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e4befe4ff1a71d6a059ec4f700a6eeb510018bea8d0a2bcf2ade32b4da6f38)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. ``my-gcp-id@gmail.com``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#username ContainerAwsCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db83f453e546c165c761cff2779e46431408e978e3df022c3ed4bd1eebff549a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAwsClusterAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6242a196da9f40313ddbed27fb4c08149047d1e57163d67d2b358289490ede)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAwsClusterAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebdafe1479d96b731933cb1c27f45db6e976fd6563ee9d86c3da462d4c4dd5c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ae42a9905d248e8fb2cc7837484ab37d13937e6cf8411ef66a9a3c0cc6289f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da5e4a71f18cb0a74c444aa1948ce3665a5369320c162e3e7083764632792951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f01e66daab430a6332bcec079fba8174d4b90019cbff1c5da7f44ae6be3aef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAwsClusterAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__966f05563395a12d7bd3f65dd97ea624384286116acf16d013840e6c94aee435)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0281100ff92502ee76a67b1897d7be33552b8454399d6321e7303374f3ea4f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b7ea639525aa580f1e4b3e3dd35a909c4ac32fee6823fc1a5531be605c3eb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAwsClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb54f79b7712b07e1243365ef16739be9fa9a36e99cfc57f031191c7cc39a2e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminGroups")
    def put_admin_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAwsClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdfd8fd60449e0554d9444346bee87b3ba7777893e9246d6886a10f96c3292bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminGroups", [value]))

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAwsClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e2153aefd12f0012b8dea9a512332d2cef82987d2b274856f5c5a9f3dd953c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @jsii.member(jsii_name="resetAdminGroups")
    def reset_admin_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminGroups", []))

    @builtins.property
    @jsii.member(jsii_name="adminGroups")
    def admin_groups(self) -> ContainerAwsClusterAuthorizationAdminGroupsList:
        return typing.cast(ContainerAwsClusterAuthorizationAdminGroupsList, jsii.get(self, "adminGroups"))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> ContainerAwsClusterAuthorizationAdminUsersList:
        return typing.cast(ContainerAwsClusterAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminGroupsInput")
    def admin_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminGroups]]], jsii.get(self, "adminGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsClusterAuthorization]:
        return typing.cast(typing.Optional[ContainerAwsClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba35ca0833a15f0e581ae04c5243dcf1eba663f98de6ab542cefffebc0f2fb3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={"evaluation_mode": "evaluationMode"},
)
class ContainerAwsClusterBinaryAuthorization:
    def __init__(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for Binary Authorization policy evaluation. Possible values: DISABLED, PROJECT_SINGLETON_POLICY_ENFORCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#evaluation_mode ContainerAwsCluster#evaluation_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24a0840ae0d3665a38b0ae8ca3fb4b7715167398d14b64e62f78bb265ef138b)
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_mode is not None:
            self._values["evaluation_mode"] = evaluation_mode

    @builtins.property
    def evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Mode of operation for Binary Authorization policy evaluation. Possible values: DISABLED, PROJECT_SINGLETON_POLICY_ENFORCE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#evaluation_mode ContainerAwsCluster#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46a661f602850044c0c34e5fc9f671f830f733e55a10c8a0c3bda8c9bd1bb87d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEvaluationMode")
    def reset_evaluation_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationMode", []))

    @builtins.property
    @jsii.member(jsii_name="evaluationModeInput")
    def evaluation_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "evaluationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationMode")
    def evaluation_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "evaluationMode"))

    @evaluation_mode.setter
    def evaluation_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c8dfa63e004cda8b81d86a0fbe4872ebd586f3ed87a0bb88c97c59212570a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsClusterBinaryAuthorization]:
        return typing.cast(typing.Optional[ContainerAwsClusterBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7285689a21d8d485449d7a297dfda4c6247799d5b38ac50dbe214a8531920f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterConfig",
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
        "aws_region": "awsRegion",
        "control_plane": "controlPlane",
        "fleet": "fleet",
        "location": "location",
        "name": "name",
        "networking": "networking",
        "annotations": "annotations",
        "binary_authorization": "binaryAuthorization",
        "description": "description",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class ContainerAwsClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization: typing.Union[ContainerAwsClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
        aws_region: builtins.str,
        control_plane: typing.Union["ContainerAwsClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["ContainerAwsClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["ContainerAwsClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union[ContainerAwsClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ContainerAwsClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#authorization ContainerAwsCluster#authorization}
        :param aws_region: The AWS region where the cluster runs. Each Google Cloud region supports a subset of nearby AWS regions. You can call to list all supported AWS regions within a given Google Cloud region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#aws_region ContainerAwsCluster#aws_region}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#control_plane ContainerAwsCluster#control_plane}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#fleet ContainerAwsCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#location ContainerAwsCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#name ContainerAwsCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#networking ContainerAwsCluster#networking}
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#annotations ContainerAwsCluster#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#binary_authorization ContainerAwsCluster#binary_authorization}
        :param description: Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#description ContainerAwsCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#id ContainerAwsCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#project ContainerAwsCluster#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#timeouts ContainerAwsCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authorization, dict):
            authorization = ContainerAwsClusterAuthorization(**authorization)
        if isinstance(control_plane, dict):
            control_plane = ContainerAwsClusterControlPlane(**control_plane)
        if isinstance(fleet, dict):
            fleet = ContainerAwsClusterFleet(**fleet)
        if isinstance(networking, dict):
            networking = ContainerAwsClusterNetworking(**networking)
        if isinstance(binary_authorization, dict):
            binary_authorization = ContainerAwsClusterBinaryAuthorization(**binary_authorization)
        if isinstance(timeouts, dict):
            timeouts = ContainerAwsClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d922196e9d9338ab2696e21d7847dee63542136c5129cf965d6bb6bcecf7b364)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument aws_region", value=aws_region, expected_type=type_hints["aws_region"])
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument fleet", value=fleet, expected_type=type_hints["fleet"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument networking", value=networking, expected_type=type_hints["networking"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument binary_authorization", value=binary_authorization, expected_type=type_hints["binary_authorization"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization": authorization,
            "aws_region": aws_region,
            "control_plane": control_plane,
            "fleet": fleet,
            "location": location,
            "name": name,
            "networking": networking,
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
        if binary_authorization is not None:
            self._values["binary_authorization"] = binary_authorization
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
    def authorization(self) -> ContainerAwsClusterAuthorization:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#authorization ContainerAwsCluster#authorization}
        '''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(ContainerAwsClusterAuthorization, result)

    @builtins.property
    def aws_region(self) -> builtins.str:
        '''The AWS region where the cluster runs.

        Each Google Cloud region supports a subset of nearby AWS regions. You can call to list all supported AWS regions within a given Google Cloud region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#aws_region ContainerAwsCluster#aws_region}
        '''
        result = self._values.get("aws_region")
        assert result is not None, "Required property 'aws_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane(self) -> "ContainerAwsClusterControlPlane":
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#control_plane ContainerAwsCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        assert result is not None, "Required property 'control_plane' is missing"
        return typing.cast("ContainerAwsClusterControlPlane", result)

    @builtins.property
    def fleet(self) -> "ContainerAwsClusterFleet":
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#fleet ContainerAwsCluster#fleet}
        '''
        result = self._values.get("fleet")
        assert result is not None, "Required property 'fleet' is missing"
        return typing.cast("ContainerAwsClusterFleet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#location ContainerAwsCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#name ContainerAwsCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def networking(self) -> "ContainerAwsClusterNetworking":
        '''networking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#networking ContainerAwsCluster#networking}
        '''
        result = self._values.get("networking")
        assert result is not None, "Required property 'networking' is missing"
        return typing.cast("ContainerAwsClusterNetworking", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field ``effective_annotations`` for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#annotations ContainerAwsCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[ContainerAwsClusterBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#binary_authorization ContainerAwsCluster#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[ContainerAwsClusterBinaryAuthorization], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#description ContainerAwsCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#id ContainerAwsCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#project ContainerAwsCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAwsClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#timeouts ContainerAwsCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAwsClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={
        "aws_services_authentication": "awsServicesAuthentication",
        "config_encryption": "configEncryption",
        "database_encryption": "databaseEncryption",
        "iam_instance_profile": "iamInstanceProfile",
        "subnet_ids": "subnetIds",
        "version": "version",
        "instance_type": "instanceType",
        "main_volume": "mainVolume",
        "proxy_config": "proxyConfig",
        "root_volume": "rootVolume",
        "security_group_ids": "securityGroupIds",
        "ssh_config": "sshConfig",
        "tags": "tags",
    },
)
class ContainerAwsClusterControlPlane:
    def __init__(
        self,
        *,
        aws_services_authentication: typing.Union["ContainerAwsClusterControlPlaneAwsServicesAuthentication", typing.Dict[builtins.str, typing.Any]],
        config_encryption: typing.Union["ContainerAwsClusterControlPlaneConfigEncryption", typing.Dict[builtins.str, typing.Any]],
        database_encryption: typing.Union["ContainerAwsClusterControlPlaneDatabaseEncryption", typing.Dict[builtins.str, typing.Any]],
        iam_instance_profile: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        version: builtins.str,
        instance_type: typing.Optional[builtins.str] = None,
        main_volume: typing.Optional[typing.Union["ContainerAwsClusterControlPlaneMainVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy_config: typing.Optional[typing.Union["ContainerAwsClusterControlPlaneProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["ContainerAwsClusterControlPlaneRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_config: typing.Optional[typing.Union["ContainerAwsClusterControlPlaneSshConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param aws_services_authentication: aws_services_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#aws_services_authentication ContainerAwsCluster#aws_services_authentication}
        :param config_encryption: config_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#config_encryption ContainerAwsCluster#config_encryption}
        :param database_encryption: database_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#database_encryption ContainerAwsCluster#database_encryption}
        :param iam_instance_profile: The name of the AWS IAM instance pofile to assign to each control plane replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iam_instance_profile ContainerAwsCluster#iam_instance_profile}
        :param subnet_ids: The list of subnets where control plane replicas will run. A replica will be provisioned on each subnet and up to three values can be provided. Each subnet must be in a different AWS Availability Zone (AZ). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#subnet_ids ContainerAwsCluster#subnet_ids}
        :param version: The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#version ContainerAwsCluster#version}
        :param instance_type: Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#instance_type ContainerAwsCluster#instance_type}
        :param main_volume: main_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#main_volume ContainerAwsCluster#main_volume}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#proxy_config ContainerAwsCluster#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#root_volume ContainerAwsCluster#root_volume}
        :param security_group_ids: Optional. The IDs of additional security groups to add to control plane replicas. The Anthos Multi-Cloud API will automatically create and manage security groups with the minimum rules needed for a functioning cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#security_group_ids ContainerAwsCluster#security_group_ids}
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#ssh_config ContainerAwsCluster#ssh_config}
        :param tags: Optional. A set of AWS resource tags to propagate to all underlying managed AWS resources. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#tags ContainerAwsCluster#tags}
        '''
        if isinstance(aws_services_authentication, dict):
            aws_services_authentication = ContainerAwsClusterControlPlaneAwsServicesAuthentication(**aws_services_authentication)
        if isinstance(config_encryption, dict):
            config_encryption = ContainerAwsClusterControlPlaneConfigEncryption(**config_encryption)
        if isinstance(database_encryption, dict):
            database_encryption = ContainerAwsClusterControlPlaneDatabaseEncryption(**database_encryption)
        if isinstance(main_volume, dict):
            main_volume = ContainerAwsClusterControlPlaneMainVolume(**main_volume)
        if isinstance(proxy_config, dict):
            proxy_config = ContainerAwsClusterControlPlaneProxyConfig(**proxy_config)
        if isinstance(root_volume, dict):
            root_volume = ContainerAwsClusterControlPlaneRootVolume(**root_volume)
        if isinstance(ssh_config, dict):
            ssh_config = ContainerAwsClusterControlPlaneSshConfig(**ssh_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8274f700ccb45f1a5a41ca44fc03404d3000c7231b4c66f6b27bfd32521c3de)
            check_type(argname="argument aws_services_authentication", value=aws_services_authentication, expected_type=type_hints["aws_services_authentication"])
            check_type(argname="argument config_encryption", value=config_encryption, expected_type=type_hints["config_encryption"])
            check_type(argname="argument database_encryption", value=database_encryption, expected_type=type_hints["database_encryption"])
            check_type(argname="argument iam_instance_profile", value=iam_instance_profile, expected_type=type_hints["iam_instance_profile"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument main_volume", value=main_volume, expected_type=type_hints["main_volume"])
            check_type(argname="argument proxy_config", value=proxy_config, expected_type=type_hints["proxy_config"])
            check_type(argname="argument root_volume", value=root_volume, expected_type=type_hints["root_volume"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument ssh_config", value=ssh_config, expected_type=type_hints["ssh_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_services_authentication": aws_services_authentication,
            "config_encryption": config_encryption,
            "database_encryption": database_encryption,
            "iam_instance_profile": iam_instance_profile,
            "subnet_ids": subnet_ids,
            "version": version,
        }
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if main_volume is not None:
            self._values["main_volume"] = main_volume
        if proxy_config is not None:
            self._values["proxy_config"] = proxy_config
        if root_volume is not None:
            self._values["root_volume"] = root_volume
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if ssh_config is not None:
            self._values["ssh_config"] = ssh_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def aws_services_authentication(
        self,
    ) -> "ContainerAwsClusterControlPlaneAwsServicesAuthentication":
        '''aws_services_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#aws_services_authentication ContainerAwsCluster#aws_services_authentication}
        '''
        result = self._values.get("aws_services_authentication")
        assert result is not None, "Required property 'aws_services_authentication' is missing"
        return typing.cast("ContainerAwsClusterControlPlaneAwsServicesAuthentication", result)

    @builtins.property
    def config_encryption(self) -> "ContainerAwsClusterControlPlaneConfigEncryption":
        '''config_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#config_encryption ContainerAwsCluster#config_encryption}
        '''
        result = self._values.get("config_encryption")
        assert result is not None, "Required property 'config_encryption' is missing"
        return typing.cast("ContainerAwsClusterControlPlaneConfigEncryption", result)

    @builtins.property
    def database_encryption(
        self,
    ) -> "ContainerAwsClusterControlPlaneDatabaseEncryption":
        '''database_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#database_encryption ContainerAwsCluster#database_encryption}
        '''
        result = self._values.get("database_encryption")
        assert result is not None, "Required property 'database_encryption' is missing"
        return typing.cast("ContainerAwsClusterControlPlaneDatabaseEncryption", result)

    @builtins.property
    def iam_instance_profile(self) -> builtins.str:
        '''The name of the AWS IAM instance pofile to assign to each control plane replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iam_instance_profile ContainerAwsCluster#iam_instance_profile}
        '''
        result = self._values.get("iam_instance_profile")
        assert result is not None, "Required property 'iam_instance_profile' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''The list of subnets where control plane replicas will run.

        A replica will be provisioned on each subnet and up to three values can be provided. Each subnet must be in a different AWS Availability Zone (AZ).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#subnet_ids ContainerAwsCluster#subnet_ids}
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling .

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#version ContainerAwsCluster#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#instance_type ContainerAwsCluster#instance_type}
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_volume(
        self,
    ) -> typing.Optional["ContainerAwsClusterControlPlaneMainVolume"]:
        '''main_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#main_volume ContainerAwsCluster#main_volume}
        '''
        result = self._values.get("main_volume")
        return typing.cast(typing.Optional["ContainerAwsClusterControlPlaneMainVolume"], result)

    @builtins.property
    def proxy_config(
        self,
    ) -> typing.Optional["ContainerAwsClusterControlPlaneProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#proxy_config ContainerAwsCluster#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["ContainerAwsClusterControlPlaneProxyConfig"], result)

    @builtins.property
    def root_volume(
        self,
    ) -> typing.Optional["ContainerAwsClusterControlPlaneRootVolume"]:
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#root_volume ContainerAwsCluster#root_volume}
        '''
        result = self._values.get("root_volume")
        return typing.cast(typing.Optional["ContainerAwsClusterControlPlaneRootVolume"], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The IDs of additional security groups to add to control plane replicas. The Anthos Multi-Cloud API will automatically create and manage security groups with the minimum rules needed for a functioning cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#security_group_ids ContainerAwsCluster#security_group_ids}
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssh_config(self) -> typing.Optional["ContainerAwsClusterControlPlaneSshConfig"]:
        '''ssh_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#ssh_config ContainerAwsCluster#ssh_config}
        '''
        result = self._values.get("ssh_config")
        return typing.cast(typing.Optional["ContainerAwsClusterControlPlaneSshConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A set of AWS resource tags to propagate to all underlying managed AWS resources. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#tags ContainerAwsCluster#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneAwsServicesAuthentication",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "role_session_name": "roleSessionName"},
)
class ContainerAwsClusterControlPlaneAwsServicesAuthentication:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        role_session_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: The Amazon Resource Name (ARN) of the role that the Anthos Multi-Cloud API will assume when managing AWS resources on your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#role_arn ContainerAwsCluster#role_arn}
        :param role_session_name: Optional. An identifier for the assumed role session. When unspecified, it defaults to ``multicloud-service-agent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#role_session_name ContainerAwsCluster#role_session_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeaf682d9106f1085c435b19fa97f87fee52fcb4c0e04e145301596d78beecea)
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument role_session_name", value=role_session_name, expected_type=type_hints["role_session_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_arn": role_arn,
        }
        if role_session_name is not None:
            self._values["role_session_name"] = role_session_name

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the role that the Anthos Multi-Cloud API will assume when managing AWS resources on your account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#role_arn ContainerAwsCluster#role_arn}
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_session_name(self) -> typing.Optional[builtins.str]:
        '''Optional. An identifier for the assumed role session. When unspecified, it defaults to ``multicloud-service-agent``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#role_session_name ContainerAwsCluster#role_session_name}
        '''
        result = self._values.get("role_session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterControlPlaneAwsServicesAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__888c3e38d12dc1098007ea97c7c1c2ec5c574916a1e0e098105c3c3b5705d420)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRoleSessionName")
    def reset_role_session_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleSessionName", []))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleSessionNameInput")
    def role_session_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleSessionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a7040e028db19d88543a8f46c79406b7daf1654b844b14d08f67d56e0976532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleSessionName")
    def role_session_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleSessionName"))

    @role_session_name.setter
    def role_session_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d1189c0a79ceeca592e7e56ce901c3acec3198341be2ce7bcf567139437450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleSessionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneAwsServicesAuthentication]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneAwsServicesAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterControlPlaneAwsServicesAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780b475f4acaba8131c530b5a5ed9da6bb261bfa6dfd569c8cbbf1fd452d455f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneConfigEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn"},
)
class ContainerAwsClusterControlPlaneConfigEncryption:
    def __init__(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt cluster configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c072a9b0608ad9fe56e2251905254dae4ba300859465c6c24aacca904f15759)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_arn": kms_key_arn,
        }

    @builtins.property
    def kms_key_arn(self) -> builtins.str:
        '''The ARN of the AWS KMS key used to encrypt cluster configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        assert result is not None, "Required property 'kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterControlPlaneConfigEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterControlPlaneConfigEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneConfigEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fd4eedc90140710e17b8c421940ddbe503c1ceba460c7387f9e902397329b0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbf046fec55fbe5702d98a5163bce3258f317e661d727c2420b946e6cdb8bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneConfigEncryption]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneConfigEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterControlPlaneConfigEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ab73509bb23305e2971cc81f2fb8dc547e21dcc8a2292cdc5c9f0f99461f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneDatabaseEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn"},
)
class ContainerAwsClusterControlPlaneDatabaseEncryption:
    def __init__(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt cluster secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f382bfb085b4100d54dce166bab4f72acbefab7734531468275981272773b757)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_arn": kms_key_arn,
        }

    @builtins.property
    def kms_key_arn(self) -> builtins.str:
        '''The ARN of the AWS KMS key used to encrypt cluster secrets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        assert result is not None, "Required property 'kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterControlPlaneDatabaseEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d928c64d6502c3ead671c35ae8e8a09cb2e635ca5f77d05cc8da03da77eb107a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ec6d2f46ccc5371015add337040810467f67130156a1197349dc880b340837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneDatabaseEncryption]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneDatabaseEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterControlPlaneDatabaseEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1870cf63de2098c3b5c557a6366214b240bb8b1d0bfa69ab63c127f32b3279a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneMainVolume",
    jsii_struct_bases=[],
    name_mapping={
        "iops": "iops",
        "kms_key_arn": "kmsKeyArn",
        "size_gib": "sizeGib",
        "throughput": "throughput",
        "volume_type": "volumeType",
    },
)
class ContainerAwsClusterControlPlaneMainVolume:
    def __init__(
        self,
        *,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        size_gib: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iops ContainerAwsCluster#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#size_gib ContainerAwsCluster#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#throughput ContainerAwsCluster#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#volume_type ContainerAwsCluster#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0cfea3edb00f2606aa5a8e92ce731c460e91008dcd529628dc03534ab02c8a)
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iops is not None:
            self._values["iops"] = iops
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if size_gib is not None:
            self._values["size_gib"] = size_gib
        if throughput is not None:
            self._values["throughput"] = throughput
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iops ContainerAwsCluster#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#size_gib ContainerAwsCluster#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#throughput ContainerAwsCluster#throughput}
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#volume_type ContainerAwsCluster#volume_type}
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterControlPlaneMainVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterControlPlaneMainVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneMainVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56ecaafbf7e8b2b0603f15497ad562f4d679312de9ee97c3c3dd099611d16195)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIops")
    def reset_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIops", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetSizeGib")
    def reset_size_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeGib", []))

    @jsii.member(jsii_name="resetThroughput")
    def reset_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughput", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

    @builtins.property
    @jsii.member(jsii_name="iopsInput")
    def iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iopsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGibInput")
    def size_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGibInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputInput")
    def throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @iops.setter
    def iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de0cb3d978b2a1a563a68f9627650b70795108b4987ae182c65eeb6288d40b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfb43f7c652ea249c098bee9a99bf67f28c4fd0e49c57676aa31a38c81779db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2d5661f0650f3c2756911145b9a7db8ef9ae7f72eab180d00309919f37a19e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__505e1c2fd80224ce57b04c95910f8701c01793a2f35872139f16bc08a5b33699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09914ada1cafd3c26a8346e5872cad2307cc64956bcbaa409001a6aff42af12a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneMainVolume]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneMainVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterControlPlaneMainVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17bb72466f30c1a1ec15a4b63ffaca9208c0f9260ff0f4326d2ffa355b98351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAwsClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a8f7fc3fb956eb647cd9c0772f8afb431046dd7fa0f044bba25983661e6f870)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsServicesAuthentication")
    def put_aws_services_authentication(
        self,
        *,
        role_arn: builtins.str,
        role_session_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: The Amazon Resource Name (ARN) of the role that the Anthos Multi-Cloud API will assume when managing AWS resources on your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#role_arn ContainerAwsCluster#role_arn}
        :param role_session_name: Optional. An identifier for the assumed role session. When unspecified, it defaults to ``multicloud-service-agent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#role_session_name ContainerAwsCluster#role_session_name}
        '''
        value = ContainerAwsClusterControlPlaneAwsServicesAuthentication(
            role_arn=role_arn, role_session_name=role_session_name
        )

        return typing.cast(None, jsii.invoke(self, "putAwsServicesAuthentication", [value]))

    @jsii.member(jsii_name="putConfigEncryption")
    def put_config_encryption(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt cluster configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        '''
        value = ContainerAwsClusterControlPlaneConfigEncryption(
            kms_key_arn=kms_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putConfigEncryption", [value]))

    @jsii.member(jsii_name="putDatabaseEncryption")
    def put_database_encryption(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt cluster secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        '''
        value = ContainerAwsClusterControlPlaneDatabaseEncryption(
            kms_key_arn=kms_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putDatabaseEncryption", [value]))

    @jsii.member(jsii_name="putMainVolume")
    def put_main_volume(
        self,
        *,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        size_gib: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iops ContainerAwsCluster#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#size_gib ContainerAwsCluster#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#throughput ContainerAwsCluster#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#volume_type ContainerAwsCluster#volume_type}
        '''
        value = ContainerAwsClusterControlPlaneMainVolume(
            iops=iops,
            kms_key_arn=kms_key_arn,
            size_gib=size_gib,
            throughput=throughput,
            volume_type=volume_type,
        )

        return typing.cast(None, jsii.invoke(self, "putMainVolume", [value]))

    @jsii.member(jsii_name="putProxyConfig")
    def put_proxy_config(
        self,
        *,
        secret_arn: builtins.str,
        secret_version: builtins.str,
    ) -> None:
        '''
        :param secret_arn: The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#secret_arn ContainerAwsCluster#secret_arn}
        :param secret_version: The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#secret_version ContainerAwsCluster#secret_version}
        '''
        value = ContainerAwsClusterControlPlaneProxyConfig(
            secret_arn=secret_arn, secret_version=secret_version
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfig", [value]))

    @jsii.member(jsii_name="putRootVolume")
    def put_root_volume(
        self,
        *,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        size_gib: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iops ContainerAwsCluster#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#size_gib ContainerAwsCluster#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#throughput ContainerAwsCluster#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#volume_type ContainerAwsCluster#volume_type}
        '''
        value = ContainerAwsClusterControlPlaneRootVolume(
            iops=iops,
            kms_key_arn=kms_key_arn,
            size_gib=size_gib,
            throughput=throughput,
            volume_type=volume_type,
        )

        return typing.cast(None, jsii.invoke(self, "putRootVolume", [value]))

    @jsii.member(jsii_name="putSshConfig")
    def put_ssh_config(self, *, ec2_key_pair: builtins.str) -> None:
        '''
        :param ec2_key_pair: The name of the EC2 key pair used to login into cluster machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#ec2_key_pair ContainerAwsCluster#ec2_key_pair}
        '''
        value = ContainerAwsClusterControlPlaneSshConfig(ec2_key_pair=ec2_key_pair)

        return typing.cast(None, jsii.invoke(self, "putSshConfig", [value]))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetMainVolume")
    def reset_main_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainVolume", []))

    @jsii.member(jsii_name="resetProxyConfig")
    def reset_proxy_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyConfig", []))

    @jsii.member(jsii_name="resetRootVolume")
    def reset_root_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootVolume", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @jsii.member(jsii_name="resetSshConfig")
    def reset_ssh_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshConfig", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="awsServicesAuthentication")
    def aws_services_authentication(
        self,
    ) -> ContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference:
        return typing.cast(ContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference, jsii.get(self, "awsServicesAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="configEncryption")
    def config_encryption(
        self,
    ) -> ContainerAwsClusterControlPlaneConfigEncryptionOutputReference:
        return typing.cast(ContainerAwsClusterControlPlaneConfigEncryptionOutputReference, jsii.get(self, "configEncryption"))

    @builtins.property
    @jsii.member(jsii_name="databaseEncryption")
    def database_encryption(
        self,
    ) -> ContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference:
        return typing.cast(ContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference, jsii.get(self, "databaseEncryption"))

    @builtins.property
    @jsii.member(jsii_name="mainVolume")
    def main_volume(self) -> ContainerAwsClusterControlPlaneMainVolumeOutputReference:
        return typing.cast(ContainerAwsClusterControlPlaneMainVolumeOutputReference, jsii.get(self, "mainVolume"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(
        self,
    ) -> "ContainerAwsClusterControlPlaneProxyConfigOutputReference":
        return typing.cast("ContainerAwsClusterControlPlaneProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(self) -> "ContainerAwsClusterControlPlaneRootVolumeOutputReference":
        return typing.cast("ContainerAwsClusterControlPlaneRootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="sshConfig")
    def ssh_config(self) -> "ContainerAwsClusterControlPlaneSshConfigOutputReference":
        return typing.cast("ContainerAwsClusterControlPlaneSshConfigOutputReference", jsii.get(self, "sshConfig"))

    @builtins.property
    @jsii.member(jsii_name="awsServicesAuthenticationInput")
    def aws_services_authentication_input(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneAwsServicesAuthentication]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneAwsServicesAuthentication], jsii.get(self, "awsServicesAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="configEncryptionInput")
    def config_encryption_input(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneConfigEncryption]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneConfigEncryption], jsii.get(self, "configEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseEncryptionInput")
    def database_encryption_input(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneDatabaseEncryption]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneDatabaseEncryption], jsii.get(self, "databaseEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInstanceProfileInput")
    def iam_instance_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamInstanceProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mainVolumeInput")
    def main_volume_input(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneMainVolume]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneMainVolume], jsii.get(self, "mainVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfigInput")
    def proxy_config_input(
        self,
    ) -> typing.Optional["ContainerAwsClusterControlPlaneProxyConfig"]:
        return typing.cast(typing.Optional["ContainerAwsClusterControlPlaneProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(
        self,
    ) -> typing.Optional["ContainerAwsClusterControlPlaneRootVolume"]:
        return typing.cast(typing.Optional["ContainerAwsClusterControlPlaneRootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshConfigInput")
    def ssh_config_input(
        self,
    ) -> typing.Optional["ContainerAwsClusterControlPlaneSshConfig"]:
        return typing.cast(typing.Optional["ContainerAwsClusterControlPlaneSshConfig"], jsii.get(self, "sshConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInstanceProfile")
    def iam_instance_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamInstanceProfile"))

    @iam_instance_profile.setter
    def iam_instance_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac38bb5fb8e74eb51ee70ecf9173c8238ecd573c6d014de32fbded4d8d24b9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamInstanceProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe21a529deb28b3d8000c5898744e395a544ba029945e7534a61fb09c0212b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a733e896a0ad100a6b99c055d8709fe907e89adbcfe5d0421da0b440399a7e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7fc3d3aa8f7f6224c0b619ebd2582df9f7998a5352b68e55a422dd40ca8bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151a8acbe464653accef01cd6b80e19b51c27c53bbfb384ee2a1a11342159316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cba41d073df1161078c35a3003412b8378f402759479e3485b446bfdc489ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsClusterControlPlane]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a74e5e4a5a5a37b6dc3d80d1294b4bd04d800d7b03ffc7a1f2283ed7f04b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"secret_arn": "secretArn", "secret_version": "secretVersion"},
)
class ContainerAwsClusterControlPlaneProxyConfig:
    def __init__(
        self,
        *,
        secret_arn: builtins.str,
        secret_version: builtins.str,
    ) -> None:
        '''
        :param secret_arn: The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#secret_arn ContainerAwsCluster#secret_arn}
        :param secret_version: The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#secret_version ContainerAwsCluster#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2560a2b6c5595d0e5137f70809ddf578881ab16b8afd3ff3410b1858c1778d2)
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_arn": secret_arn,
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#secret_arn ContainerAwsCluster#secret_arn}
        '''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#secret_version ContainerAwsCluster#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterControlPlaneProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterControlPlaneProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8b19e28ed8502c48455b86c60bc70c1eaefe2313077835e183680a253f15f2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretArnInput")
    def secret_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretArnInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @secret_arn.setter
    def secret_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c247dbc2b515bd26b4e96f151785947615fc4aef2ae91ccec8a696962a67a3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230f4b1fc923c9ee992226ca719ec77820759df5982610360d80fdf2577497bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneProxyConfig]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterControlPlaneProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357254d10b515fa4e9da820a68c8d457649d17b650ad1494f43cc704618bf711)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneRootVolume",
    jsii_struct_bases=[],
    name_mapping={
        "iops": "iops",
        "kms_key_arn": "kmsKeyArn",
        "size_gib": "sizeGib",
        "throughput": "throughput",
        "volume_type": "volumeType",
    },
)
class ContainerAwsClusterControlPlaneRootVolume:
    def __init__(
        self,
        *,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        size_gib: typing.Optional[jsii.Number] = None,
        throughput: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iops ContainerAwsCluster#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#size_gib ContainerAwsCluster#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#throughput ContainerAwsCluster#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#volume_type ContainerAwsCluster#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e78001df423c3d70f5badc454c52e20cf3cc91bc0a2cdff494e0cb23e8b5c71)
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
            check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iops is not None:
            self._values["iops"] = iops
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if size_gib is not None:
            self._values["size_gib"] = size_gib
        if throughput is not None:
            self._values["throughput"] = throughput
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#iops ContainerAwsCluster#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#kms_key_arn ContainerAwsCluster#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#size_gib ContainerAwsCluster#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#throughput ContainerAwsCluster#throughput}
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#volume_type ContainerAwsCluster#volume_type}
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterControlPlaneRootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterControlPlaneRootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneRootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d2e1ebb2cbd49ebc0be901d4354e56442b1abda5923127eb777a965421b2565)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIops")
    def reset_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIops", []))

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetSizeGib")
    def reset_size_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeGib", []))

    @jsii.member(jsii_name="resetThroughput")
    def reset_throughput(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughput", []))

    @jsii.member(jsii_name="resetVolumeType")
    def reset_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeType", []))

    @builtins.property
    @jsii.member(jsii_name="iopsInput")
    def iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iopsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGibInput")
    def size_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGibInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputInput")
    def throughput_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeTypeInput")
    def volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @iops.setter
    def iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ea467464acc547da18aee94882b733dca04b578296f11bc6f5090736ac566d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d3c34d2e46ae9fafa9bc9edbdcfea809f8936f948b8b5280254975778d3045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe46efb4c7f45f3594b06c29e04bee8ee1a25e6473464d067b03c82a4aed5fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e66f889df17568ec2bb05716a9c87bf733aeab78efcd371b3aba33c528267f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617a4ff2f0bf9b6bd262bbc3fc29ea7b9ad7554aa02d4d9b84a21feeb53fca7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneRootVolume]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneRootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterControlPlaneRootVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0112cc7d19d11cb92315a37d8d4b10d31aa9486250d01183860f34b6f29d5677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneSshConfig",
    jsii_struct_bases=[],
    name_mapping={"ec2_key_pair": "ec2KeyPair"},
)
class ContainerAwsClusterControlPlaneSshConfig:
    def __init__(self, *, ec2_key_pair: builtins.str) -> None:
        '''
        :param ec2_key_pair: The name of the EC2 key pair used to login into cluster machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#ec2_key_pair ContainerAwsCluster#ec2_key_pair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbeb8f7f6478a2becf76f024e1665ea0def9778d7af4840f1bfbf5647b4c81a0)
            check_type(argname="argument ec2_key_pair", value=ec2_key_pair, expected_type=type_hints["ec2_key_pair"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_key_pair": ec2_key_pair,
        }

    @builtins.property
    def ec2_key_pair(self) -> builtins.str:
        '''The name of the EC2 key pair used to login into cluster machines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#ec2_key_pair ContainerAwsCluster#ec2_key_pair}
        '''
        result = self._values.get("ec2_key_pair")
        assert result is not None, "Required property 'ec2_key_pair' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterControlPlaneSshConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterControlPlaneSshConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterControlPlaneSshConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e0fbdcb34963b16ac54064cc1b8258491e6bdf360412a79c86899a90c00f565)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="ec2KeyPairInput")
    def ec2_key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2KeyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2KeyPair")
    def ec2_key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ec2KeyPair"))

    @ec2_key_pair.setter
    def ec2_key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f322d3f4d17e679943d2f54f273a80c2051cc2be38ffdfb4682198cafffb36a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2KeyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ContainerAwsClusterControlPlaneSshConfig]:
        return typing.cast(typing.Optional[ContainerAwsClusterControlPlaneSshConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterControlPlaneSshConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e790650d5ba8082fbd997c13a6e0718d05dc8f011839720fa2dc7e277ba1f87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterFleet",
    jsii_struct_bases=[],
    name_mapping={"project": "project"},
)
class ContainerAwsClusterFleet:
    def __init__(self, *, project: typing.Optional[builtins.str] = None) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#project ContainerAwsCluster#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e09f1324b2742635e0ce26c3ac04b2d77188e26c87dce49c06b274fc9521cb5)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The number of the Fleet host project where this cluster will be registered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#project ContainerAwsCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3f20b02ec6bf9528970ecc03ff1fb615a4f74f5b74ba9c77b326209a2f9e81e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e793925ef3ebfc3f002382853e4b58b0d5342d57d5136cbf7e757a3764127076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsClusterFleet]:
        return typing.cast(typing.Optional[ContainerAwsClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ContainerAwsClusterFleet]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763cb22c2440b2926c231dc6ce1aeaf283598532e5e48e45e7b55aea05864a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterNetworking",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
        "vpc_id": "vpcId",
        "per_node_pool_sg_rules_disabled": "perNodePoolSgRulesDisabled",
    },
)
class ContainerAwsClusterNetworking:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
        per_node_pool_sg_rules_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#pod_address_cidr_blocks ContainerAwsCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#service_address_cidr_blocks ContainerAwsCluster#service_address_cidr_blocks}
        :param vpc_id: The VPC associated with the cluster. All component clusters (i.e. control plane and node pools) run on a single VPC. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#vpc_id ContainerAwsCluster#vpc_id}
        :param per_node_pool_sg_rules_disabled: Disable the per node pool subnet security group rules on the control plane security group. When set to true, you must also provide one or more security groups that ensure node pools are able to send requests to the control plane on TCP/443 and TCP/8132. Failure to do so may result in unavailable node pools. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#per_node_pool_sg_rules_disabled ContainerAwsCluster#per_node_pool_sg_rules_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f2cbe0f9098a888523167cb2060e871f996a61e290d70ac5a46e34098983ca)
            check_type(argname="argument pod_address_cidr_blocks", value=pod_address_cidr_blocks, expected_type=type_hints["pod_address_cidr_blocks"])
            check_type(argname="argument service_address_cidr_blocks", value=service_address_cidr_blocks, expected_type=type_hints["service_address_cidr_blocks"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument per_node_pool_sg_rules_disabled", value=per_node_pool_sg_rules_disabled, expected_type=type_hints["per_node_pool_sg_rules_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pod_address_cidr_blocks": pod_address_cidr_blocks,
            "service_address_cidr_blocks": service_address_cidr_blocks,
            "vpc_id": vpc_id,
        }
        if per_node_pool_sg_rules_disabled is not None:
            self._values["per_node_pool_sg_rules_disabled"] = per_node_pool_sg_rules_disabled

    @builtins.property
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        Only a single range is supported. This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#pod_address_cidr_blocks ContainerAwsCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        Only a single range is supported. This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#service_address_cidr_blocks ContainerAwsCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The VPC associated with the cluster.

        All component clusters (i.e. control plane and node pools) run on a single VPC. This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#vpc_id ContainerAwsCluster#vpc_id}
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def per_node_pool_sg_rules_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the per node pool subnet security group rules on the control plane security group.

        When set to true, you must also provide one or more security groups that ensure node pools are able to send requests to the control plane on TCP/443 and TCP/8132. Failure to do so may result in unavailable node pools.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#per_node_pool_sg_rules_disabled ContainerAwsCluster#per_node_pool_sg_rules_disabled}
        '''
        result = self._values.get("per_node_pool_sg_rules_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterNetworking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterNetworkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterNetworkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6620c6863c6fc668d90d74460648076b81415dc3284586f75990422bde25cbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPerNodePoolSgRulesDisabled")
    def reset_per_node_pool_sg_rules_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerNodePoolSgRulesDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="perNodePoolSgRulesDisabledInput")
    def per_node_pool_sg_rules_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "perNodePoolSgRulesDisabledInput"))

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
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="perNodePoolSgRulesDisabled")
    def per_node_pool_sg_rules_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "perNodePoolSgRulesDisabled"))

    @per_node_pool_sg_rules_disabled.setter
    def per_node_pool_sg_rules_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8745bbc13918b5d9f1c770688bfb1d8ee39c5eba9aee76bbb9a8856bbda0b80b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perNodePoolSgRulesDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podAddressCidrBlocks")
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "podAddressCidrBlocks"))

    @pod_address_cidr_blocks.setter
    def pod_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e461cf675e3b97ce27b14ce74534a8d2de4c90172ae96dd7328e866c86f00182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a026622bc8212e2509ee36a3dc81f036f6812cce1047d5a320ab63b700590e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438a5a8bdadf27d463a9391efe72f42c75630792df536ae3ea88553eefd5a970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ContainerAwsClusterNetworking]:
        return typing.cast(typing.Optional[ContainerAwsClusterNetworking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterNetworking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dccb02bb6d7fbbfd37f575e5905d9f4921c02a3f2d19894086c6d8914a05e19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ContainerAwsClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#create ContainerAwsCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#delete ContainerAwsCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#update ContainerAwsCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53bcbe025f2d097f2aa3436fd1cd47ced8e0294a101bdee65ee28c9cdf9eec5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#create ContainerAwsCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#delete ContainerAwsCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/container_aws_cluster#update ContainerAwsCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__070d455391720a7fbae6dbcdb5293810d8d04081730ca048115bb47f28a363a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53f708676dfeae4e04bb5b1dc9e675b8228329c781ad639c1d7683ebf632ba46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81404f6e5b508ef743415dfbba28f464a194ab3e60b78761ec08e080b8ee90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48307749aeff83fbf02abc35d1d2d6b2e4c4b8136d700c6b925f8187d34d5bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e19110ef23283964e148f7190b097047e99a18de1cd5184fc5e91b1961b5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterWorkloadIdentityConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class ContainerAwsClusterWorkloadIdentityConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAwsClusterWorkloadIdentityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAwsClusterWorkloadIdentityConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterWorkloadIdentityConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25a60c4fe292e40ad4b015c1577683d651f55ac182e4dc0b201bc9aa7e52b826)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAwsClusterWorkloadIdentityConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b86190dfc6c3acc968c1231f1b53d8b294a93932c8a1b7e9d42d66319f2e6c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAwsClusterWorkloadIdentityConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81303a7b7f0d6b6e939b901d939905b4bf6b78a9dfc892eef25755a34c3d6e0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7efebed11f5be3a440700dff4ed3e58b3f9f7a2a9fb6e41b992080894af2e53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae08e3ae4d822dc28f3e2a3002c1c43ebd61b42198e400e8468188694217e39b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ContainerAwsClusterWorkloadIdentityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.containerAwsCluster.ContainerAwsClusterWorkloadIdentityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1813ae9f02576cf3d47c7d5be4ecda86c8a3ecd912d70acce8845748c34a0ab1)
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
    ) -> typing.Optional[ContainerAwsClusterWorkloadIdentityConfig]:
        return typing.cast(typing.Optional[ContainerAwsClusterWorkloadIdentityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ContainerAwsClusterWorkloadIdentityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635064716ff5294fa9c05dab37f0c6cb8da225d4d4876c46e263d0d65586f269)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAwsCluster",
    "ContainerAwsClusterAuthorization",
    "ContainerAwsClusterAuthorizationAdminGroups",
    "ContainerAwsClusterAuthorizationAdminGroupsList",
    "ContainerAwsClusterAuthorizationAdminGroupsOutputReference",
    "ContainerAwsClusterAuthorizationAdminUsers",
    "ContainerAwsClusterAuthorizationAdminUsersList",
    "ContainerAwsClusterAuthorizationAdminUsersOutputReference",
    "ContainerAwsClusterAuthorizationOutputReference",
    "ContainerAwsClusterBinaryAuthorization",
    "ContainerAwsClusterBinaryAuthorizationOutputReference",
    "ContainerAwsClusterConfig",
    "ContainerAwsClusterControlPlane",
    "ContainerAwsClusterControlPlaneAwsServicesAuthentication",
    "ContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference",
    "ContainerAwsClusterControlPlaneConfigEncryption",
    "ContainerAwsClusterControlPlaneConfigEncryptionOutputReference",
    "ContainerAwsClusterControlPlaneDatabaseEncryption",
    "ContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference",
    "ContainerAwsClusterControlPlaneMainVolume",
    "ContainerAwsClusterControlPlaneMainVolumeOutputReference",
    "ContainerAwsClusterControlPlaneOutputReference",
    "ContainerAwsClusterControlPlaneProxyConfig",
    "ContainerAwsClusterControlPlaneProxyConfigOutputReference",
    "ContainerAwsClusterControlPlaneRootVolume",
    "ContainerAwsClusterControlPlaneRootVolumeOutputReference",
    "ContainerAwsClusterControlPlaneSshConfig",
    "ContainerAwsClusterControlPlaneSshConfigOutputReference",
    "ContainerAwsClusterFleet",
    "ContainerAwsClusterFleetOutputReference",
    "ContainerAwsClusterNetworking",
    "ContainerAwsClusterNetworkingOutputReference",
    "ContainerAwsClusterTimeouts",
    "ContainerAwsClusterTimeoutsOutputReference",
    "ContainerAwsClusterWorkloadIdentityConfig",
    "ContainerAwsClusterWorkloadIdentityConfigList",
    "ContainerAwsClusterWorkloadIdentityConfigOutputReference",
]

publication.publish()

def _typecheckingstub__1b5403434afce948419e99fc6044f81c8e2fe9eae277f50bf4358fd8bde54813(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization: typing.Union[ContainerAwsClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    aws_region: builtins.str,
    control_plane: typing.Union[ContainerAwsClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[ContainerAwsClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[ContainerAwsClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[ContainerAwsClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAwsClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0deeb78c047bb6241b1f9a0e5f09e45743fac19fb53c4ccd494ae61885449453(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159adcd002b48eac55a52764b029458eda73a617a800847b76b64ee28ac00027(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a07649d99c121f7e7d458fed96c016da7cca05401397975b8e452941bc0621(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2503e81249e9002e2bd74f26c33b7052a6aa4da2a66e27776cb303004949b8b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f91883033675255d5fbd63cacd96421354ceea953271d818638775dedadc0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945146b8fbffb9f7f1d63652b718e87b811d32fb6aec90868e8eccff6de1734c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb4939dcad1f003a73a63bf733f31305991268a9f1bf93ab1a4cc2e4f1eb7ea4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90177da73bbbd9585da69fae9899f7e6dd495b53a44da6ab78eba66e37389205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf0099a6cad5d06cfff9deeab64e906db1ced5328819fc3155b1ad840ba9097(
    *,
    admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAwsClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAwsClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791368bc52b403f619b003463687b530ea28d6a6d624a0f91415d8ecce300f63(
    *,
    group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb69d05d5691ab66510d479a747089f5f3c2a4da329a7c60e6c04bd82dc774e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6a88491c0992d533f4bf59a90ff422e0c307778bd5a43f73c1d179fa9fb8e7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ece578f9f3c8d5b6a875700cd2ea656cb0b58fc6d0f57d2bcab4cc614d08e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d4eec84c7e43bd174701035614512f26408a8d7cff869817821026425e19c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67299d0c6ce226b3fe84af7510ac104fdc1d284c18e7fbc9ca626d9fc79eaf78(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b418802aa5938b2bc4880e2789a3a3d8238f1aeb6f5d214e3da5560ef8515a7b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09d306ac7a0a2d2044f418db06639791b78ca9ab8fe2a9ac618b15853d28e51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219543d11a2cd2d5ede7482880d1d1b44360ff80bbd018f7805f3ce74047d193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71f8b0b02d9de58a2a65cab1b844fc770742253fb53599a5bfcd3a9ee2e0586(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterAuthorizationAdminGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e4befe4ff1a71d6a059ec4f700a6eeb510018bea8d0a2bcf2ade32b4da6f38(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db83f453e546c165c761cff2779e46431408e978e3df022c3ed4bd1eebff549a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6242a196da9f40313ddbed27fb4c08149047d1e57163d67d2b358289490ede(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdafe1479d96b731933cb1c27f45db6e976fd6563ee9d86c3da462d4c4dd5c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae42a9905d248e8fb2cc7837484ab37d13937e6cf8411ef66a9a3c0cc6289f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5e4a71f18cb0a74c444aa1948ce3665a5369320c162e3e7083764632792951(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f01e66daab430a6332bcec079fba8174d4b90019cbff1c5da7f44ae6be3aef0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAwsClusterAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966f05563395a12d7bd3f65dd97ea624384286116acf16d013840e6c94aee435(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0281100ff92502ee76a67b1897d7be33552b8454399d6321e7303374f3ea4f90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b7ea639525aa580f1e4b3e3dd35a909c4ac32fee6823fc1a5531be605c3eb1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb54f79b7712b07e1243365ef16739be9fa9a36e99cfc57f031191c7cc39a2e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfd8fd60449e0554d9444346bee87b3ba7777893e9246d6886a10f96c3292bf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAwsClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e2153aefd12f0012b8dea9a512332d2cef82987d2b274856f5c5a9f3dd953c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAwsClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba35ca0833a15f0e581ae04c5243dcf1eba663f98de6ab542cefffebc0f2fb3d(
    value: typing.Optional[ContainerAwsClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24a0840ae0d3665a38b0ae8ca3fb4b7715167398d14b64e62f78bb265ef138b(
    *,
    evaluation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a661f602850044c0c34e5fc9f671f830f733e55a10c8a0c3bda8c9bd1bb87d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c8dfa63e004cda8b81d86a0fbe4872ebd586f3ed87a0bb88c97c59212570a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7285689a21d8d485449d7a297dfda4c6247799d5b38ac50dbe214a8531920f(
    value: typing.Optional[ContainerAwsClusterBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d922196e9d9338ab2696e21d7847dee63542136c5129cf965d6bb6bcecf7b364(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization: typing.Union[ContainerAwsClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    aws_region: builtins.str,
    control_plane: typing.Union[ContainerAwsClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[ContainerAwsClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[ContainerAwsClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[ContainerAwsClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ContainerAwsClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8274f700ccb45f1a5a41ca44fc03404d3000c7231b4c66f6b27bfd32521c3de(
    *,
    aws_services_authentication: typing.Union[ContainerAwsClusterControlPlaneAwsServicesAuthentication, typing.Dict[builtins.str, typing.Any]],
    config_encryption: typing.Union[ContainerAwsClusterControlPlaneConfigEncryption, typing.Dict[builtins.str, typing.Any]],
    database_encryption: typing.Union[ContainerAwsClusterControlPlaneDatabaseEncryption, typing.Dict[builtins.str, typing.Any]],
    iam_instance_profile: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    version: builtins.str,
    instance_type: typing.Optional[builtins.str] = None,
    main_volume: typing.Optional[typing.Union[ContainerAwsClusterControlPlaneMainVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    proxy_config: typing.Optional[typing.Union[ContainerAwsClusterControlPlaneProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    root_volume: typing.Optional[typing.Union[ContainerAwsClusterControlPlaneRootVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssh_config: typing.Optional[typing.Union[ContainerAwsClusterControlPlaneSshConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeaf682d9106f1085c435b19fa97f87fee52fcb4c0e04e145301596d78beecea(
    *,
    role_arn: builtins.str,
    role_session_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888c3e38d12dc1098007ea97c7c1c2ec5c574916a1e0e098105c3c3b5705d420(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a7040e028db19d88543a8f46c79406b7daf1654b844b14d08f67d56e0976532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d1189c0a79ceeca592e7e56ce901c3acec3198341be2ce7bcf567139437450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780b475f4acaba8131c530b5a5ed9da6bb261bfa6dfd569c8cbbf1fd452d455f(
    value: typing.Optional[ContainerAwsClusterControlPlaneAwsServicesAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c072a9b0608ad9fe56e2251905254dae4ba300859465c6c24aacca904f15759(
    *,
    kms_key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd4eedc90140710e17b8c421940ddbe503c1ceba460c7387f9e902397329b0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbf046fec55fbe5702d98a5163bce3258f317e661d727c2420b946e6cdb8bee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ab73509bb23305e2971cc81f2fb8dc547e21dcc8a2292cdc5c9f0f99461f73(
    value: typing.Optional[ContainerAwsClusterControlPlaneConfigEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f382bfb085b4100d54dce166bab4f72acbefab7734531468275981272773b757(
    *,
    kms_key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d928c64d6502c3ead671c35ae8e8a09cb2e635ca5f77d05cc8da03da77eb107a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ec6d2f46ccc5371015add337040810467f67130156a1197349dc880b340837(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1870cf63de2098c3b5c557a6366214b240bb8b1d0bfa69ab63c127f32b3279a(
    value: typing.Optional[ContainerAwsClusterControlPlaneDatabaseEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0cfea3edb00f2606aa5a8e92ce731c460e91008dcd529628dc03534ab02c8a(
    *,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    size_gib: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ecaafbf7e8b2b0603f15497ad562f4d679312de9ee97c3c3dd099611d16195(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de0cb3d978b2a1a563a68f9627650b70795108b4987ae182c65eeb6288d40b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfb43f7c652ea249c098bee9a99bf67f28c4fd0e49c57676aa31a38c81779db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2d5661f0650f3c2756911145b9a7db8ef9ae7f72eab180d00309919f37a19e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__505e1c2fd80224ce57b04c95910f8701c01793a2f35872139f16bc08a5b33699(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09914ada1cafd3c26a8346e5872cad2307cc64956bcbaa409001a6aff42af12a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17bb72466f30c1a1ec15a4b63ffaca9208c0f9260ff0f4326d2ffa355b98351(
    value: typing.Optional[ContainerAwsClusterControlPlaneMainVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8f7fc3fb956eb647cd9c0772f8afb431046dd7fa0f044bba25983661e6f870(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac38bb5fb8e74eb51ee70ecf9173c8238ecd573c6d014de32fbded4d8d24b9ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe21a529deb28b3d8000c5898744e395a544ba029945e7534a61fb09c0212b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a733e896a0ad100a6b99c055d8709fe907e89adbcfe5d0421da0b440399a7e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7fc3d3aa8f7f6224c0b619ebd2582df9f7998a5352b68e55a422dd40ca8bda(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151a8acbe464653accef01cd6b80e19b51c27c53bbfb384ee2a1a11342159316(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cba41d073df1161078c35a3003412b8378f402759479e3485b446bfdc489ef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a74e5e4a5a5a37b6dc3d80d1294b4bd04d800d7b03ffc7a1f2283ed7f04b4c(
    value: typing.Optional[ContainerAwsClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2560a2b6c5595d0e5137f70809ddf578881ab16b8afd3ff3410b1858c1778d2(
    *,
    secret_arn: builtins.str,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b19e28ed8502c48455b86c60bc70c1eaefe2313077835e183680a253f15f2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c247dbc2b515bd26b4e96f151785947615fc4aef2ae91ccec8a696962a67a3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230f4b1fc923c9ee992226ca719ec77820759df5982610360d80fdf2577497bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357254d10b515fa4e9da820a68c8d457649d17b650ad1494f43cc704618bf711(
    value: typing.Optional[ContainerAwsClusterControlPlaneProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e78001df423c3d70f5badc454c52e20cf3cc91bc0a2cdff494e0cb23e8b5c71(
    *,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    size_gib: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2e1ebb2cbd49ebc0be901d4354e56442b1abda5923127eb777a965421b2565(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ea467464acc547da18aee94882b733dca04b578296f11bc6f5090736ac566d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d3c34d2e46ae9fafa9bc9edbdcfea809f8936f948b8b5280254975778d3045(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe46efb4c7f45f3594b06c29e04bee8ee1a25e6473464d067b03c82a4aed5fe5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e66f889df17568ec2bb05716a9c87bf733aeab78efcd371b3aba33c528267f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617a4ff2f0bf9b6bd262bbc3fc29ea7b9ad7554aa02d4d9b84a21feeb53fca7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0112cc7d19d11cb92315a37d8d4b10d31aa9486250d01183860f34b6f29d5677(
    value: typing.Optional[ContainerAwsClusterControlPlaneRootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbeb8f7f6478a2becf76f024e1665ea0def9778d7af4840f1bfbf5647b4c81a0(
    *,
    ec2_key_pair: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0fbdcb34963b16ac54064cc1b8258491e6bdf360412a79c86899a90c00f565(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f322d3f4d17e679943d2f54f273a80c2051cc2be38ffdfb4682198cafffb36a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e790650d5ba8082fbd997c13a6e0718d05dc8f011839720fa2dc7e277ba1f87e(
    value: typing.Optional[ContainerAwsClusterControlPlaneSshConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e09f1324b2742635e0ce26c3ac04b2d77188e26c87dce49c06b274fc9521cb5(
    *,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f20b02ec6bf9528970ecc03ff1fb615a4f74f5b74ba9c77b326209a2f9e81e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e793925ef3ebfc3f002382853e4b58b0d5342d57d5136cbf7e757a3764127076(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763cb22c2440b2926c231dc6ce1aeaf283598532e5e48e45e7b55aea05864a20(
    value: typing.Optional[ContainerAwsClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f2cbe0f9098a888523167cb2060e871f996a61e290d70ac5a46e34098983ca(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
    vpc_id: builtins.str,
    per_node_pool_sg_rules_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6620c6863c6fc668d90d74460648076b81415dc3284586f75990422bde25cbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8745bbc13918b5d9f1c770688bfb1d8ee39c5eba9aee76bbb9a8856bbda0b80b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e461cf675e3b97ce27b14ce74534a8d2de4c90172ae96dd7328e866c86f00182(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a026622bc8212e2509ee36a3dc81f036f6812cce1047d5a320ab63b700590e49(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438a5a8bdadf27d463a9391efe72f42c75630792df536ae3ea88553eefd5a970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dccb02bb6d7fbbfd37f575e5905d9f4921c02a3f2d19894086c6d8914a05e19(
    value: typing.Optional[ContainerAwsClusterNetworking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53bcbe025f2d097f2aa3436fd1cd47ced8e0294a101bdee65ee28c9cdf9eec5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070d455391720a7fbae6dbcdb5293810d8d04081730ca048115bb47f28a363a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f708676dfeae4e04bb5b1dc9e675b8228329c781ad639c1d7683ebf632ba46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81404f6e5b508ef743415dfbba28f464a194ab3e60b78761ec08e080b8ee90a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48307749aeff83fbf02abc35d1d2d6b2e4c4b8136d700c6b925f8187d34d5bcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e19110ef23283964e148f7190b097047e99a18de1cd5184fc5e91b1961b5aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAwsClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a60c4fe292e40ad4b015c1577683d651f55ac182e4dc0b201bc9aa7e52b826(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b86190dfc6c3acc968c1231f1b53d8b294a93932c8a1b7e9d42d66319f2e6c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81303a7b7f0d6b6e939b901d939905b4bf6b78a9dfc892eef25755a34c3d6e0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7efebed11f5be3a440700dff4ed3e58b3f9f7a2a9fb6e41b992080894af2e53(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae08e3ae4d822dc28f3e2a3002c1c43ebd61b42198e400e8468188694217e39b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1813ae9f02576cf3d47c7d5be4ecda86c8a3ecd912d70acce8845748c34a0ab1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635064716ff5294fa9c05dab37f0c6cb8da225d4d4876c46e263d0d65586f269(
    value: typing.Optional[ContainerAwsClusterWorkloadIdentityConfig],
) -> None:
    """Type checking stubs"""
    pass
