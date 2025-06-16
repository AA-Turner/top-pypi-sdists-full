r'''
# `google_container_aws_cluster`

Refer to the Terraform Registry for docs: [`google_container_aws_cluster`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster).
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


class GoogleContainerAwsCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster google_container_aws_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        authorization: typing.Union["GoogleContainerAwsClusterAuthorization", typing.Dict[builtins.str, typing.Any]],
        aws_region: builtins.str,
        control_plane: typing.Union["GoogleContainerAwsClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["GoogleContainerAwsClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["GoogleContainerAwsClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union["GoogleContainerAwsClusterBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["GoogleContainerAwsClusterLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAwsClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster google_container_aws_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#authorization GoogleContainerAwsCluster#authorization}
        :param aws_region: The AWS region where the cluster runs. Each Google Cloud region supports a subset of nearby AWS regions. You can call to list all supported AWS regions within a given Google Cloud region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#aws_region GoogleContainerAwsCluster#aws_region}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#control_plane GoogleContainerAwsCluster#control_plane}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#fleet GoogleContainerAwsCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#location GoogleContainerAwsCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#name GoogleContainerAwsCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#networking GoogleContainerAwsCluster#networking}
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#annotations GoogleContainerAwsCluster#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#binary_authorization GoogleContainerAwsCluster#binary_authorization}
        :param description: Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#description GoogleContainerAwsCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#id GoogleContainerAwsCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#logging_config GoogleContainerAwsCluster#logging_config}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#project GoogleContainerAwsCluster#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#timeouts GoogleContainerAwsCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52929c353d6e6f063d353c91495b7143158fd964832db3e8c96a0429d7c641f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleContainerAwsClusterConfig(
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
        '''Generates CDKTF code for importing a GoogleContainerAwsCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleContainerAwsCluster to import.
        :param import_from_id: The id of the existing GoogleContainerAwsCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleContainerAwsCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f7f6a65dc16965e48449a1cf4553bfa69628610de00781fb9afaacca63e170)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAwsClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
        admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAwsClusterAuthorizationAdminGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#admin_users GoogleContainerAwsCluster#admin_users}
        :param admin_groups: admin_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#admin_groups GoogleContainerAwsCluster#admin_groups}
        '''
        value = GoogleContainerAwsClusterAuthorization(
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
        :param evaluation_mode: Mode of operation for Binary Authorization policy evaluation. Possible values: DISABLED, PROJECT_SINGLETON_POLICY_ENFORCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#evaluation_mode GoogleContainerAwsCluster#evaluation_mode}
        '''
        value = GoogleContainerAwsClusterBinaryAuthorization(
            evaluation_mode=evaluation_mode
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putControlPlane")
    def put_control_plane(
        self,
        *,
        aws_services_authentication: typing.Union["GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication", typing.Dict[builtins.str, typing.Any]],
        config_encryption: typing.Union["GoogleContainerAwsClusterControlPlaneConfigEncryption", typing.Dict[builtins.str, typing.Any]],
        database_encryption: typing.Union["GoogleContainerAwsClusterControlPlaneDatabaseEncryption", typing.Dict[builtins.str, typing.Any]],
        iam_instance_profile: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        version: builtins.str,
        instance_placement: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneInstancePlacement", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        main_volume: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneMainVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy_config: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_config: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneSshConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param aws_services_authentication: aws_services_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#aws_services_authentication GoogleContainerAwsCluster#aws_services_authentication}
        :param config_encryption: config_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#config_encryption GoogleContainerAwsCluster#config_encryption}
        :param database_encryption: database_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#database_encryption GoogleContainerAwsCluster#database_encryption}
        :param iam_instance_profile: The name of the AWS IAM instance pofile to assign to each control plane replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iam_instance_profile GoogleContainerAwsCluster#iam_instance_profile}
        :param subnet_ids: The list of subnets where control plane replicas will run. A replica will be provisioned on each subnet and up to three values can be provided. Each subnet must be in a different AWS Availability Zone (AZ). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#subnet_ids GoogleContainerAwsCluster#subnet_ids}
        :param version: The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#version GoogleContainerAwsCluster#version}
        :param instance_placement: instance_placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#instance_placement GoogleContainerAwsCluster#instance_placement}
        :param instance_type: Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#instance_type GoogleContainerAwsCluster#instance_type}
        :param main_volume: main_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#main_volume GoogleContainerAwsCluster#main_volume}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#proxy_config GoogleContainerAwsCluster#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#root_volume GoogleContainerAwsCluster#root_volume}
        :param security_group_ids: Optional. The IDs of additional security groups to add to control plane replicas. The Anthos Multi-Cloud API will automatically create and manage security groups with the minimum rules needed for a functioning cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#security_group_ids GoogleContainerAwsCluster#security_group_ids}
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#ssh_config GoogleContainerAwsCluster#ssh_config}
        :param tags: Optional. A set of AWS resource tags to propagate to all underlying managed AWS resources. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#tags GoogleContainerAwsCluster#tags}
        '''
        value = GoogleContainerAwsClusterControlPlane(
            aws_services_authentication=aws_services_authentication,
            config_encryption=config_encryption,
            database_encryption=database_encryption,
            iam_instance_profile=iam_instance_profile,
            subnet_ids=subnet_ids,
            version=version,
            instance_placement=instance_placement,
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
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#project GoogleContainerAwsCluster#project}
        '''
        value = GoogleContainerAwsClusterFleet(project=project)

        return typing.cast(None, jsii.invoke(self, "putFleet", [value]))

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        component_config: typing.Optional[typing.Union["GoogleContainerAwsClusterLoggingConfigComponentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param component_config: component_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#component_config GoogleContainerAwsCluster#component_config}
        '''
        value = GoogleContainerAwsClusterLoggingConfig(
            component_config=component_config
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

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
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#pod_address_cidr_blocks GoogleContainerAwsCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#service_address_cidr_blocks GoogleContainerAwsCluster#service_address_cidr_blocks}
        :param vpc_id: The VPC associated with the cluster. All component clusters (i.e. control plane and node pools) run on a single VPC. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#vpc_id GoogleContainerAwsCluster#vpc_id}
        :param per_node_pool_sg_rules_disabled: Disable the per node pool subnet security group rules on the control plane security group. When set to true, you must also provide one or more security groups that ensure node pools are able to send requests to the control plane on TCP/443 and TCP/8132. Failure to do so may result in unavailable node pools. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#per_node_pool_sg_rules_disabled GoogleContainerAwsCluster#per_node_pool_sg_rules_disabled}
        '''
        value = GoogleContainerAwsClusterNetworking(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#create GoogleContainerAwsCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#delete GoogleContainerAwsCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#update GoogleContainerAwsCluster#update}.
        '''
        value = GoogleContainerAwsClusterTimeouts(
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
    def authorization(self) -> "GoogleContainerAwsClusterAuthorizationOutputReference":
        return typing.cast("GoogleContainerAwsClusterAuthorizationOutputReference", jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorization")
    def binary_authorization(
        self,
    ) -> "GoogleContainerAwsClusterBinaryAuthorizationOutputReference":
        return typing.cast("GoogleContainerAwsClusterBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> "GoogleContainerAwsClusterControlPlaneOutputReference":
        return typing.cast("GoogleContainerAwsClusterControlPlaneOutputReference", jsii.get(self, "controlPlane"))

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
    def fleet(self) -> "GoogleContainerAwsClusterFleetOutputReference":
        return typing.cast("GoogleContainerAwsClusterFleetOutputReference", jsii.get(self, "fleet"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> "GoogleContainerAwsClusterLoggingConfigOutputReference":
        return typing.cast("GoogleContainerAwsClusterLoggingConfigOutputReference", jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="networking")
    def networking(self) -> "GoogleContainerAwsClusterNetworkingOutputReference":
        return typing.cast("GoogleContainerAwsClusterNetworkingOutputReference", jsii.get(self, "networking"))

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
    def timeouts(self) -> "GoogleContainerAwsClusterTimeoutsOutputReference":
        return typing.cast("GoogleContainerAwsClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> "GoogleContainerAwsClusterWorkloadIdentityConfigList":
        return typing.cast("GoogleContainerAwsClusterWorkloadIdentityConfigList", jsii.get(self, "workloadIdentityConfig"))

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
    ) -> typing.Optional["GoogleContainerAwsClusterAuthorization"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterAuthorization"], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegionInput")
    def aws_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryAuthorizationInput")
    def binary_authorization_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterBinaryAuthorization"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlane"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlane"], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetInput")
    def fleet_input(self) -> typing.Optional["GoogleContainerAwsClusterFleet"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterFleet"], jsii.get(self, "fleetInput"))

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
    ) -> typing.Optional["GoogleContainerAwsClusterLoggingConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterLoggingConfig"], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkingInput")
    def networking_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterNetworking"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterNetworking"], jsii.get(self, "networkingInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAwsClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleContainerAwsClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a4a971f61aef9b4f6f64cf320e17976cdc9cc1453182bc28009e7c4a318c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="awsRegion")
    def aws_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRegion"))

    @aws_region.setter
    def aws_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f31ececaba9ea23363e23ade7948668e4ecd7168e6a11e1b7ec5691ffecdf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99616f886aa58056bcc4aa41f6d33479f8968a8281130473e4bb28fd5c43d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7c062823ca093ebef09053056703e8efeaac68f63a45e97377fa680d940311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d60173d2472f3c164f864a0102187bb50b5ce93dbc5a7d4449a7d5fb9a5d73bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a8edb0b2ba55b2d754ca9aacaf4f3d58742a7d9f2cf256d4874e1ea09b002a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a90ef392b4cff53cf4ec2c56a54eff0181a65776fad606c4b0e5cb620f0817d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterAuthorization",
    jsii_struct_bases=[],
    name_mapping={"admin_users": "adminUsers", "admin_groups": "adminGroups"},
)
class GoogleContainerAwsClusterAuthorization:
    def __init__(
        self,
        *,
        admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAwsClusterAuthorizationAdminUsers", typing.Dict[builtins.str, typing.Any]]]],
        admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleContainerAwsClusterAuthorizationAdminGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param admin_users: admin_users block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#admin_users GoogleContainerAwsCluster#admin_users}
        :param admin_groups: admin_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#admin_groups GoogleContainerAwsCluster#admin_groups}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af3a6f05423bd407a27c1c021407a63fe039e54a02a4c140f7fdebc453e4a5d)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAwsClusterAuthorizationAdminUsers"]]:
        '''admin_users block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#admin_users GoogleContainerAwsCluster#admin_users}
        '''
        result = self._values.get("admin_users")
        assert result is not None, "Required property 'admin_users' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAwsClusterAuthorizationAdminUsers"]], result)

    @builtins.property
    def admin_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAwsClusterAuthorizationAdminGroups"]]]:
        '''admin_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#admin_groups GoogleContainerAwsCluster#admin_groups}
        '''
        result = self._values.get("admin_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleContainerAwsClusterAuthorizationAdminGroups"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterAuthorizationAdminGroups",
    jsii_struct_bases=[],
    name_mapping={"group": "group"},
)
class GoogleContainerAwsClusterAuthorizationAdminGroups:
    def __init__(self, *, group: builtins.str) -> None:
        '''
        :param group: The name of the group, e.g. ``my-group@domain.com``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#group GoogleContainerAwsCluster#group}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d405d3a7924aeb06fc81a2ca0af5c9f40bd573a9c517b2e27e5738e85c78c841)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group": group,
        }

    @builtins.property
    def group(self) -> builtins.str:
        '''The name of the group, e.g. ``my-group@domain.com``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#group GoogleContainerAwsCluster#group}
        '''
        result = self._values.get("group")
        assert result is not None, "Required property 'group' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterAuthorizationAdminGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterAuthorizationAdminGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterAuthorizationAdminGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__303ed26817fca852e23a859d7a762ccd7a56ade02ed8eff36af68a134875eb3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAwsClusterAuthorizationAdminGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37554904e2778336f24576990f07124154dc32a7967a29f8e8d62282a62552ec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAwsClusterAuthorizationAdminGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3a5a1f1972ed1daea778c6c183358cd774ba00472eb1524bf7bdd1b3810775)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6ffab0ebb4254e402e8266307759988a6e6c505ee89680a4b5e30620a851931)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fb20fcc513be55be45ed63aa5ad5a04e9ba8a3650a43b61d577c4e5dd112945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65428ed0c9a1480541876a796ceeb33e84fe8d037ab116359cf1ba23ce3dfc0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAwsClusterAuthorizationAdminGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterAuthorizationAdminGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d7672ba212b25806d25126738dd37ca97f618d0cf209e74219c41069e6237b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cb35a876b2ea00b6683889cab2f8c2600c8033557ba3f8337e5f87dbbf8b281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "group", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterAuthorizationAdminGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterAuthorizationAdminGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterAuthorizationAdminGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc734cecf3d1474257f27052226e889f0d3b33d39c6115d945325180d13d249a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterAuthorizationAdminUsers",
    jsii_struct_bases=[],
    name_mapping={"username": "username"},
)
class GoogleContainerAwsClusterAuthorizationAdminUsers:
    def __init__(self, *, username: builtins.str) -> None:
        '''
        :param username: The name of the user, e.g. ``my-gcp-id@gmail.com``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#username GoogleContainerAwsCluster#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d863b0763a3f769d0cf750b49fcda15c972be811ab1b06567144289ce737ae53)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }

    @builtins.property
    def username(self) -> builtins.str:
        '''The name of the user, e.g. ``my-gcp-id@gmail.com``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#username GoogleContainerAwsCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterAuthorizationAdminUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterAuthorizationAdminUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterAuthorizationAdminUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97ca74af68fcff99fa2423517e607ec40621cbcaf0bc9cc42c2ec5ce561cf487)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAwsClusterAuthorizationAdminUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222ffe327845a5a64898886b4bb757fb27b780e9a509d083796dab7a79a458e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAwsClusterAuthorizationAdminUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611d8a0fb1d120ecf48233a01289da33030d491e1145aff2c389a67f485d18bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30366d027757a495460a1de4bcfd0f94b41f6a66cba3634866af9283a25a645c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a45d7321a2a61fd2f79c328f1ec741a83151554a6576d7db8fd4d3a63d81bfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminUsers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminUsers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430c717bae7dbd9d4445868e677b10d1536ce0becd4cdbaa8efff5c4ca64a0f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAwsClusterAuthorizationAdminUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterAuthorizationAdminUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d3514251f4f706c1ca6e111a6b344d7a0d53ebe868cddc66f2cbcecc1450d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89e391add4db85b6eed42d69bf58796ba9caaf1597d70898173421826784148c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterAuthorizationAdminUsers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterAuthorizationAdminUsers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterAuthorizationAdminUsers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50e680d1e517380296dc0afd91eb1b271fafbcf8ade3a4b2325dd87291062ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAwsClusterAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b169550a78d698663a82036d210388398f49917fa99969f48f56b33f650ce2e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdminGroups")
    def put_admin_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAwsClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a3a505aaa7998602b3abf6712db088b7770f4d5a718356714009ee9e92f152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminGroups", [value]))

    @jsii.member(jsii_name="putAdminUsers")
    def put_admin_users(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAwsClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a31af21bbec966089b38bd75289f6b810aa65a1600c4e8c1b2aad71ae9edce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdminUsers", [value]))

    @jsii.member(jsii_name="resetAdminGroups")
    def reset_admin_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminGroups", []))

    @builtins.property
    @jsii.member(jsii_name="adminGroups")
    def admin_groups(self) -> GoogleContainerAwsClusterAuthorizationAdminGroupsList:
        return typing.cast(GoogleContainerAwsClusterAuthorizationAdminGroupsList, jsii.get(self, "adminGroups"))

    @builtins.property
    @jsii.member(jsii_name="adminUsers")
    def admin_users(self) -> GoogleContainerAwsClusterAuthorizationAdminUsersList:
        return typing.cast(GoogleContainerAwsClusterAuthorizationAdminUsersList, jsii.get(self, "adminUsers"))

    @builtins.property
    @jsii.member(jsii_name="adminGroupsInput")
    def admin_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminGroups]]], jsii.get(self, "adminGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="adminUsersInput")
    def admin_users_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminUsers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminUsers]]], jsii.get(self, "adminUsersInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAwsClusterAuthorization]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfe8ebdbf37f2a2fb301f74d132c4d551a5928d377d8809caebf8a9ffd15a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={"evaluation_mode": "evaluationMode"},
)
class GoogleContainerAwsClusterBinaryAuthorization:
    def __init__(
        self,
        *,
        evaluation_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param evaluation_mode: Mode of operation for Binary Authorization policy evaluation. Possible values: DISABLED, PROJECT_SINGLETON_POLICY_ENFORCE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#evaluation_mode GoogleContainerAwsCluster#evaluation_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea104be39dc90a670cabc703607c367f03f41c0e4ad173257f01d4f79fb91062)
            check_type(argname="argument evaluation_mode", value=evaluation_mode, expected_type=type_hints["evaluation_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if evaluation_mode is not None:
            self._values["evaluation_mode"] = evaluation_mode

    @builtins.property
    def evaluation_mode(self) -> typing.Optional[builtins.str]:
        '''Mode of operation for Binary Authorization policy evaluation. Possible values: DISABLED, PROJECT_SINGLETON_POLICY_ENFORCE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#evaluation_mode GoogleContainerAwsCluster#evaluation_mode}
        '''
        result = self._values.get("evaluation_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c686afbe1f5c7afcbf94bc440b6b0c6b67ccdd1b4ebee9413a609ef1f19b8b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47d4d1e899f2b5367feb8e94b2e4766463f4daa10e073cce17c3f611e0f2582f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterBinaryAuthorization]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72369e2eda54ea2b3c1de56facad14c54cc2caca1011ce23b7da47481fd842c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterConfig",
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
        "logging_config": "loggingConfig",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleContainerAwsClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        authorization: typing.Union[GoogleContainerAwsClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
        aws_region: builtins.str,
        control_plane: typing.Union["GoogleContainerAwsClusterControlPlane", typing.Dict[builtins.str, typing.Any]],
        fleet: typing.Union["GoogleContainerAwsClusterFleet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        networking: typing.Union["GoogleContainerAwsClusterNetworking", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union[GoogleContainerAwsClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        logging_config: typing.Optional[typing.Union["GoogleContainerAwsClusterLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleContainerAwsClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#authorization GoogleContainerAwsCluster#authorization}
        :param aws_region: The AWS region where the cluster runs. Each Google Cloud region supports a subset of nearby AWS regions. You can call to list all supported AWS regions within a given Google Cloud region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#aws_region GoogleContainerAwsCluster#aws_region}
        :param control_plane: control_plane block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#control_plane GoogleContainerAwsCluster#control_plane}
        :param fleet: fleet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#fleet GoogleContainerAwsCluster#fleet}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#location GoogleContainerAwsCluster#location}
        :param name: The name of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#name GoogleContainerAwsCluster#name}
        :param networking: networking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#networking GoogleContainerAwsCluster#networking}
        :param annotations: Optional. Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field ``effective_annotations`` for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#annotations GoogleContainerAwsCluster#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#binary_authorization GoogleContainerAwsCluster#binary_authorization}
        :param description: Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#description GoogleContainerAwsCluster#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#id GoogleContainerAwsCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#logging_config GoogleContainerAwsCluster#logging_config}
        :param project: The project for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#project GoogleContainerAwsCluster#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#timeouts GoogleContainerAwsCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authorization, dict):
            authorization = GoogleContainerAwsClusterAuthorization(**authorization)
        if isinstance(control_plane, dict):
            control_plane = GoogleContainerAwsClusterControlPlane(**control_plane)
        if isinstance(fleet, dict):
            fleet = GoogleContainerAwsClusterFleet(**fleet)
        if isinstance(networking, dict):
            networking = GoogleContainerAwsClusterNetworking(**networking)
        if isinstance(binary_authorization, dict):
            binary_authorization = GoogleContainerAwsClusterBinaryAuthorization(**binary_authorization)
        if isinstance(logging_config, dict):
            logging_config = GoogleContainerAwsClusterLoggingConfig(**logging_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleContainerAwsClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3efa2adbfd437ca5f27e2d10766f4f76fc2d937e8e77d0ec9ce838e849a45e1)
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
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
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
    def authorization(self) -> GoogleContainerAwsClusterAuthorization:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#authorization GoogleContainerAwsCluster#authorization}
        '''
        result = self._values.get("authorization")
        assert result is not None, "Required property 'authorization' is missing"
        return typing.cast(GoogleContainerAwsClusterAuthorization, result)

    @builtins.property
    def aws_region(self) -> builtins.str:
        '''The AWS region where the cluster runs.

        Each Google Cloud region supports a subset of nearby AWS regions. You can call to list all supported AWS regions within a given Google Cloud region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#aws_region GoogleContainerAwsCluster#aws_region}
        '''
        result = self._values.get("aws_region")
        assert result is not None, "Required property 'aws_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_plane(self) -> "GoogleContainerAwsClusterControlPlane":
        '''control_plane block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#control_plane GoogleContainerAwsCluster#control_plane}
        '''
        result = self._values.get("control_plane")
        assert result is not None, "Required property 'control_plane' is missing"
        return typing.cast("GoogleContainerAwsClusterControlPlane", result)

    @builtins.property
    def fleet(self) -> "GoogleContainerAwsClusterFleet":
        '''fleet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#fleet GoogleContainerAwsCluster#fleet}
        '''
        result = self._values.get("fleet")
        assert result is not None, "Required property 'fleet' is missing"
        return typing.cast("GoogleContainerAwsClusterFleet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#location GoogleContainerAwsCluster#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#name GoogleContainerAwsCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def networking(self) -> "GoogleContainerAwsClusterNetworking":
        '''networking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#networking GoogleContainerAwsCluster#networking}
        '''
        result = self._values.get("networking")
        assert result is not None, "Required property 'networking' is missing"
        return typing.cast("GoogleContainerAwsClusterNetworking", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        Annotations on the cluster. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field ``effective_annotations`` for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#annotations GoogleContainerAwsCluster#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#binary_authorization GoogleContainerAwsCluster#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[GoogleContainerAwsClusterBinaryAuthorization], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. A human readable description of this cluster. Cannot be longer than 255 UTF-8 encoded bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#description GoogleContainerAwsCluster#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#id GoogleContainerAwsCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#logging_config GoogleContainerAwsCluster#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["GoogleContainerAwsClusterLoggingConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#project GoogleContainerAwsCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleContainerAwsClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#timeouts GoogleContainerAwsCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleContainerAwsClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlane",
    jsii_struct_bases=[],
    name_mapping={
        "aws_services_authentication": "awsServicesAuthentication",
        "config_encryption": "configEncryption",
        "database_encryption": "databaseEncryption",
        "iam_instance_profile": "iamInstanceProfile",
        "subnet_ids": "subnetIds",
        "version": "version",
        "instance_placement": "instancePlacement",
        "instance_type": "instanceType",
        "main_volume": "mainVolume",
        "proxy_config": "proxyConfig",
        "root_volume": "rootVolume",
        "security_group_ids": "securityGroupIds",
        "ssh_config": "sshConfig",
        "tags": "tags",
    },
)
class GoogleContainerAwsClusterControlPlane:
    def __init__(
        self,
        *,
        aws_services_authentication: typing.Union["GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication", typing.Dict[builtins.str, typing.Any]],
        config_encryption: typing.Union["GoogleContainerAwsClusterControlPlaneConfigEncryption", typing.Dict[builtins.str, typing.Any]],
        database_encryption: typing.Union["GoogleContainerAwsClusterControlPlaneDatabaseEncryption", typing.Dict[builtins.str, typing.Any]],
        iam_instance_profile: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        version: builtins.str,
        instance_placement: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneInstancePlacement", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[builtins.str] = None,
        main_volume: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneMainVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        proxy_config: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneProxyConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        root_volume: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneRootVolume", typing.Dict[builtins.str, typing.Any]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_config: typing.Optional[typing.Union["GoogleContainerAwsClusterControlPlaneSshConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param aws_services_authentication: aws_services_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#aws_services_authentication GoogleContainerAwsCluster#aws_services_authentication}
        :param config_encryption: config_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#config_encryption GoogleContainerAwsCluster#config_encryption}
        :param database_encryption: database_encryption block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#database_encryption GoogleContainerAwsCluster#database_encryption}
        :param iam_instance_profile: The name of the AWS IAM instance pofile to assign to each control plane replica. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iam_instance_profile GoogleContainerAwsCluster#iam_instance_profile}
        :param subnet_ids: The list of subnets where control plane replicas will run. A replica will be provisioned on each subnet and up to three values can be provided. Each subnet must be in a different AWS Availability Zone (AZ). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#subnet_ids GoogleContainerAwsCluster#subnet_ids}
        :param version: The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling . Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#version GoogleContainerAwsCluster#version}
        :param instance_placement: instance_placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#instance_placement GoogleContainerAwsCluster#instance_placement}
        :param instance_type: Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#instance_type GoogleContainerAwsCluster#instance_type}
        :param main_volume: main_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#main_volume GoogleContainerAwsCluster#main_volume}
        :param proxy_config: proxy_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#proxy_config GoogleContainerAwsCluster#proxy_config}
        :param root_volume: root_volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#root_volume GoogleContainerAwsCluster#root_volume}
        :param security_group_ids: Optional. The IDs of additional security groups to add to control plane replicas. The Anthos Multi-Cloud API will automatically create and manage security groups with the minimum rules needed for a functioning cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#security_group_ids GoogleContainerAwsCluster#security_group_ids}
        :param ssh_config: ssh_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#ssh_config GoogleContainerAwsCluster#ssh_config}
        :param tags: Optional. A set of AWS resource tags to propagate to all underlying managed AWS resources. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#tags GoogleContainerAwsCluster#tags}
        '''
        if isinstance(aws_services_authentication, dict):
            aws_services_authentication = GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication(**aws_services_authentication)
        if isinstance(config_encryption, dict):
            config_encryption = GoogleContainerAwsClusterControlPlaneConfigEncryption(**config_encryption)
        if isinstance(database_encryption, dict):
            database_encryption = GoogleContainerAwsClusterControlPlaneDatabaseEncryption(**database_encryption)
        if isinstance(instance_placement, dict):
            instance_placement = GoogleContainerAwsClusterControlPlaneInstancePlacement(**instance_placement)
        if isinstance(main_volume, dict):
            main_volume = GoogleContainerAwsClusterControlPlaneMainVolume(**main_volume)
        if isinstance(proxy_config, dict):
            proxy_config = GoogleContainerAwsClusterControlPlaneProxyConfig(**proxy_config)
        if isinstance(root_volume, dict):
            root_volume = GoogleContainerAwsClusterControlPlaneRootVolume(**root_volume)
        if isinstance(ssh_config, dict):
            ssh_config = GoogleContainerAwsClusterControlPlaneSshConfig(**ssh_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42bcdfca5a765c1e423b3108be90f10a24dbece3cc50d71600395339def315a)
            check_type(argname="argument aws_services_authentication", value=aws_services_authentication, expected_type=type_hints["aws_services_authentication"])
            check_type(argname="argument config_encryption", value=config_encryption, expected_type=type_hints["config_encryption"])
            check_type(argname="argument database_encryption", value=database_encryption, expected_type=type_hints["database_encryption"])
            check_type(argname="argument iam_instance_profile", value=iam_instance_profile, expected_type=type_hints["iam_instance_profile"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument instance_placement", value=instance_placement, expected_type=type_hints["instance_placement"])
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
        if instance_placement is not None:
            self._values["instance_placement"] = instance_placement
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
    ) -> "GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication":
        '''aws_services_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#aws_services_authentication GoogleContainerAwsCluster#aws_services_authentication}
        '''
        result = self._values.get("aws_services_authentication")
        assert result is not None, "Required property 'aws_services_authentication' is missing"
        return typing.cast("GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication", result)

    @builtins.property
    def config_encryption(
        self,
    ) -> "GoogleContainerAwsClusterControlPlaneConfigEncryption":
        '''config_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#config_encryption GoogleContainerAwsCluster#config_encryption}
        '''
        result = self._values.get("config_encryption")
        assert result is not None, "Required property 'config_encryption' is missing"
        return typing.cast("GoogleContainerAwsClusterControlPlaneConfigEncryption", result)

    @builtins.property
    def database_encryption(
        self,
    ) -> "GoogleContainerAwsClusterControlPlaneDatabaseEncryption":
        '''database_encryption block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#database_encryption GoogleContainerAwsCluster#database_encryption}
        '''
        result = self._values.get("database_encryption")
        assert result is not None, "Required property 'database_encryption' is missing"
        return typing.cast("GoogleContainerAwsClusterControlPlaneDatabaseEncryption", result)

    @builtins.property
    def iam_instance_profile(self) -> builtins.str:
        '''The name of the AWS IAM instance pofile to assign to each control plane replica.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iam_instance_profile GoogleContainerAwsCluster#iam_instance_profile}
        '''
        result = self._values.get("iam_instance_profile")
        assert result is not None, "Required property 'iam_instance_profile' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''The list of subnets where control plane replicas will run.

        A replica will be provisioned on each subnet and up to three values can be provided. Each subnet must be in a different AWS Availability Zone (AZ).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#subnet_ids GoogleContainerAwsCluster#subnet_ids}
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Kubernetes version to run on control plane replicas (e.g. ``1.19.10-gke.1000``). You can list all supported versions on a given Google Cloud region by calling .

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#version GoogleContainerAwsCluster#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_placement(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlaneInstancePlacement"]:
        '''instance_placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#instance_placement GoogleContainerAwsCluster#instance_placement}
        '''
        result = self._values.get("instance_placement")
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlaneInstancePlacement"], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Optional. The AWS instance type. When unspecified, it defaults to ``m5.large``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#instance_type GoogleContainerAwsCluster#instance_type}
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_volume(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlaneMainVolume"]:
        '''main_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#main_volume GoogleContainerAwsCluster#main_volume}
        '''
        result = self._values.get("main_volume")
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlaneMainVolume"], result)

    @builtins.property
    def proxy_config(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlaneProxyConfig"]:
        '''proxy_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#proxy_config GoogleContainerAwsCluster#proxy_config}
        '''
        result = self._values.get("proxy_config")
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlaneProxyConfig"], result)

    @builtins.property
    def root_volume(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlaneRootVolume"]:
        '''root_volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#root_volume GoogleContainerAwsCluster#root_volume}
        '''
        result = self._values.get("root_volume")
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlaneRootVolume"], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The IDs of additional security groups to add to control plane replicas. The Anthos Multi-Cloud API will automatically create and manage security groups with the minimum rules needed for a functioning cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#security_group_ids GoogleContainerAwsCluster#security_group_ids}
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssh_config(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlaneSshConfig"]:
        '''ssh_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#ssh_config GoogleContainerAwsCluster#ssh_config}
        '''
        result = self._values.get("ssh_config")
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlaneSshConfig"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A set of AWS resource tags to propagate to all underlying managed AWS resources. Specify at most 50 pairs containing alphanumerics, spaces, and symbols (.+-=_:@/). Keys can be up to 127 Unicode characters. Values can be up to 255 Unicode characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#tags GoogleContainerAwsCluster#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication",
    jsii_struct_bases=[],
    name_mapping={"role_arn": "roleArn", "role_session_name": "roleSessionName"},
)
class GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication:
    def __init__(
        self,
        *,
        role_arn: builtins.str,
        role_session_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param role_arn: The Amazon Resource Name (ARN) of the role that the Anthos Multi-Cloud API will assume when managing AWS resources on your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#role_arn GoogleContainerAwsCluster#role_arn}
        :param role_session_name: Optional. An identifier for the assumed role session. When unspecified, it defaults to ``multicloud-service-agent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#role_session_name GoogleContainerAwsCluster#role_session_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4dbb1cdc94affb96204523bdf8f54694d917da63292d7b21d4f88d57ee631c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#role_arn GoogleContainerAwsCluster#role_arn}
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_session_name(self) -> typing.Optional[builtins.str]:
        '''Optional. An identifier for the assumed role session. When unspecified, it defaults to ``multicloud-service-agent``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#role_session_name GoogleContainerAwsCluster#role_session_name}
        '''
        result = self._values.get("role_session_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96c23f81d0f593a53f0fb9604e47f0fed594dc45cf8bca4ca5824b8923dd620d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63aad1436485e01ac6378d83b5ec0969e168b0087f3ab80f749464e52344ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleSessionName")
    def role_session_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleSessionName"))

    @role_session_name.setter
    def role_session_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec6d0c8bd981f9eef4b6827e3fbbbdae617eabbc34e25ce37558de865a21145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleSessionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8247a2a5a001b71c23c2701afcd02204a7f486389b954a8d9a7d77c77f8d6ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneConfigEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn"},
)
class GoogleContainerAwsClusterControlPlaneConfigEncryption:
    def __init__(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt cluster configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175f1cf82153701e086a5af526ada749a008a631fd5d6c1b5193adb24e3a7d35)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_arn": kms_key_arn,
        }

    @builtins.property
    def kms_key_arn(self) -> builtins.str:
        '''The ARN of the AWS KMS key used to encrypt cluster configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        assert result is not None, "Required property 'kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlaneConfigEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterControlPlaneConfigEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneConfigEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__441910ffa932ae370be1f513fe35a8d0c714b004c62ec221f8a7ec323fd69387)
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
            type_hints = typing.get_type_hints(_typecheckingstub__267bd0868c4c8513a6be41b05c2a93d834f4a9279ccf897e4db070642ec7ac9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneConfigEncryption]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneConfigEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlaneConfigEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2088d328e220428295213114f51c6630634b9396aa0fada01ad76b52472177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneDatabaseEncryption",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn"},
)
class GoogleContainerAwsClusterControlPlaneDatabaseEncryption:
    def __init__(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt cluster secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef1429928587108a3e7aecaa91ec415c05cd0dbea1e10c2f149782c9dc293ae)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_arn": kms_key_arn,
        }

    @builtins.property
    def kms_key_arn(self) -> builtins.str:
        '''The ARN of the AWS KMS key used to encrypt cluster secrets.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        assert result is not None, "Required property 'kms_key_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlaneDatabaseEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__726e88f836feaa8c2afb56956142898e39d91ead8d41643a188f3e62a82143be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54147e54613bcb81e914a770b9947f0649626aa6ba1ce07b00a06a48d810ac99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneDatabaseEncryption]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneDatabaseEncryption], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlaneDatabaseEncryption],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54b18d8e63ceefd3aae72beefd1230ab2ca6d716a11ecca8b3c8f2f511c1eba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneInstancePlacement",
    jsii_struct_bases=[],
    name_mapping={"tenancy": "tenancy"},
)
class GoogleContainerAwsClusterControlPlaneInstancePlacement:
    def __init__(self, *, tenancy: typing.Optional[builtins.str] = None) -> None:
        '''
        :param tenancy: The tenancy for the instance. Possible values: TENANCY_UNSPECIFIED, DEFAULT, DEDICATED, HOST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#tenancy GoogleContainerAwsCluster#tenancy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29f35f946ad78dd1176c431b01c33e079ad6c11996a6460f63978502b7046d6)
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tenancy is not None:
            self._values["tenancy"] = tenancy

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''The tenancy for the instance. Possible values: TENANCY_UNSPECIFIED, DEFAULT, DEDICATED, HOST.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#tenancy GoogleContainerAwsCluster#tenancy}
        '''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlaneInstancePlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterControlPlaneInstancePlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneInstancePlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4706ccc36f7eef28f5bf65da15e2ea1a365e0d683671244aed446f0b3f2ff48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTenancy")
    def reset_tenancy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenancy", []))

    @builtins.property
    @jsii.member(jsii_name="tenancyInput")
    def tenancy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenancyInput"))

    @builtins.property
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenancy"))

    @tenancy.setter
    def tenancy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7050481573444a5c2cc82a95247ad2262a6c92fe31054be918e913b96ae2ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenancy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneInstancePlacement]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneInstancePlacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlaneInstancePlacement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f6d35825f08634d5cdf9e82ebe02ec13a5d53352f5e15d63e5ff68809db557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneMainVolume",
    jsii_struct_bases=[],
    name_mapping={
        "iops": "iops",
        "kms_key_arn": "kmsKeyArn",
        "size_gib": "sizeGib",
        "throughput": "throughput",
        "volume_type": "volumeType",
    },
)
class GoogleContainerAwsClusterControlPlaneMainVolume:
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
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iops GoogleContainerAwsCluster#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#size_gib GoogleContainerAwsCluster#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#throughput GoogleContainerAwsCluster#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#volume_type GoogleContainerAwsCluster#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231333bbae1fbd466117cc30bf3d4cfe8ed63989dbae845b5e509b43a61f45fb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iops GoogleContainerAwsCluster#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#size_gib GoogleContainerAwsCluster#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#throughput GoogleContainerAwsCluster#throughput}
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#volume_type GoogleContainerAwsCluster#volume_type}
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlaneMainVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterControlPlaneMainVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneMainVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f1cabb2a701465a8ae8cfadf5a9541e099a13063bf0ad57d4d4efc6375780a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f901a35c71e9d3c6f385892f17763cc8a7461e2a1b9d62ad6af312bd48f4b426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae09add4519377a30b9976c1b9d1cc90aec5228ffd5185e42e023763b236b55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4050d0d9f066594ca40d9e4cbfeb4db13124f2f3d3f55b823dc45547748447f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154512e8cf7aa8406aead93c23cd523890ffac6c0bce55c5f8cb60e3b62c3c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc1588d607a57deed323f0b19fdf03293e420aff9ff4aac4661056bc26398f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneMainVolume]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneMainVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlaneMainVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bdbfe9879e9742cb7c90196cb938773e3e8f641d71b294fec7c3d14056c289c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAwsClusterControlPlaneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__653bfed173aebbfcf188359ad99af80b5842d0c355aec6f2f3e8ef502ea8c592)
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
        :param role_arn: The Amazon Resource Name (ARN) of the role that the Anthos Multi-Cloud API will assume when managing AWS resources on your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#role_arn GoogleContainerAwsCluster#role_arn}
        :param role_session_name: Optional. An identifier for the assumed role session. When unspecified, it defaults to ``multicloud-service-agent``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#role_session_name GoogleContainerAwsCluster#role_session_name}
        '''
        value = GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication(
            role_arn=role_arn, role_session_name=role_session_name
        )

        return typing.cast(None, jsii.invoke(self, "putAwsServicesAuthentication", [value]))

    @jsii.member(jsii_name="putConfigEncryption")
    def put_config_encryption(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt cluster configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        '''
        value = GoogleContainerAwsClusterControlPlaneConfigEncryption(
            kms_key_arn=kms_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putConfigEncryption", [value]))

    @jsii.member(jsii_name="putDatabaseEncryption")
    def put_database_encryption(self, *, kms_key_arn: builtins.str) -> None:
        '''
        :param kms_key_arn: The ARN of the AWS KMS key used to encrypt cluster secrets. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        '''
        value = GoogleContainerAwsClusterControlPlaneDatabaseEncryption(
            kms_key_arn=kms_key_arn
        )

        return typing.cast(None, jsii.invoke(self, "putDatabaseEncryption", [value]))

    @jsii.member(jsii_name="putInstancePlacement")
    def put_instance_placement(
        self,
        *,
        tenancy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tenancy: The tenancy for the instance. Possible values: TENANCY_UNSPECIFIED, DEFAULT, DEDICATED, HOST. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#tenancy GoogleContainerAwsCluster#tenancy}
        '''
        value = GoogleContainerAwsClusterControlPlaneInstancePlacement(tenancy=tenancy)

        return typing.cast(None, jsii.invoke(self, "putInstancePlacement", [value]))

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
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iops GoogleContainerAwsCluster#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#size_gib GoogleContainerAwsCluster#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#throughput GoogleContainerAwsCluster#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#volume_type GoogleContainerAwsCluster#volume_type}
        '''
        value = GoogleContainerAwsClusterControlPlaneMainVolume(
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
        :param secret_arn: The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#secret_arn GoogleContainerAwsCluster#secret_arn}
        :param secret_version: The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#secret_version GoogleContainerAwsCluster#secret_version}
        '''
        value = GoogleContainerAwsClusterControlPlaneProxyConfig(
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
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iops GoogleContainerAwsCluster#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#size_gib GoogleContainerAwsCluster#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#throughput GoogleContainerAwsCluster#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#volume_type GoogleContainerAwsCluster#volume_type}
        '''
        value = GoogleContainerAwsClusterControlPlaneRootVolume(
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
        :param ec2_key_pair: The name of the EC2 key pair used to login into cluster machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#ec2_key_pair GoogleContainerAwsCluster#ec2_key_pair}
        '''
        value = GoogleContainerAwsClusterControlPlaneSshConfig(
            ec2_key_pair=ec2_key_pair
        )

        return typing.cast(None, jsii.invoke(self, "putSshConfig", [value]))

    @jsii.member(jsii_name="resetInstancePlacement")
    def reset_instance_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstancePlacement", []))

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
    ) -> GoogleContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference:
        return typing.cast(GoogleContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference, jsii.get(self, "awsServicesAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="configEncryption")
    def config_encryption(
        self,
    ) -> GoogleContainerAwsClusterControlPlaneConfigEncryptionOutputReference:
        return typing.cast(GoogleContainerAwsClusterControlPlaneConfigEncryptionOutputReference, jsii.get(self, "configEncryption"))

    @builtins.property
    @jsii.member(jsii_name="databaseEncryption")
    def database_encryption(
        self,
    ) -> GoogleContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference:
        return typing.cast(GoogleContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference, jsii.get(self, "databaseEncryption"))

    @builtins.property
    @jsii.member(jsii_name="instancePlacement")
    def instance_placement(
        self,
    ) -> GoogleContainerAwsClusterControlPlaneInstancePlacementOutputReference:
        return typing.cast(GoogleContainerAwsClusterControlPlaneInstancePlacementOutputReference, jsii.get(self, "instancePlacement"))

    @builtins.property
    @jsii.member(jsii_name="mainVolume")
    def main_volume(
        self,
    ) -> GoogleContainerAwsClusterControlPlaneMainVolumeOutputReference:
        return typing.cast(GoogleContainerAwsClusterControlPlaneMainVolumeOutputReference, jsii.get(self, "mainVolume"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfig")
    def proxy_config(
        self,
    ) -> "GoogleContainerAwsClusterControlPlaneProxyConfigOutputReference":
        return typing.cast("GoogleContainerAwsClusterControlPlaneProxyConfigOutputReference", jsii.get(self, "proxyConfig"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(
        self,
    ) -> "GoogleContainerAwsClusterControlPlaneRootVolumeOutputReference":
        return typing.cast("GoogleContainerAwsClusterControlPlaneRootVolumeOutputReference", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="sshConfig")
    def ssh_config(
        self,
    ) -> "GoogleContainerAwsClusterControlPlaneSshConfigOutputReference":
        return typing.cast("GoogleContainerAwsClusterControlPlaneSshConfigOutputReference", jsii.get(self, "sshConfig"))

    @builtins.property
    @jsii.member(jsii_name="awsServicesAuthenticationInput")
    def aws_services_authentication_input(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication], jsii.get(self, "awsServicesAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="configEncryptionInput")
    def config_encryption_input(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneConfigEncryption]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneConfigEncryption], jsii.get(self, "configEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseEncryptionInput")
    def database_encryption_input(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneDatabaseEncryption]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneDatabaseEncryption], jsii.get(self, "databaseEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInstanceProfileInput")
    def iam_instance_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamInstanceProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="instancePlacementInput")
    def instance_placement_input(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneInstancePlacement]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneInstancePlacement], jsii.get(self, "instancePlacementInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="mainVolumeInput")
    def main_volume_input(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneMainVolume]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneMainVolume], jsii.get(self, "mainVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfigInput")
    def proxy_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlaneProxyConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlaneProxyConfig"], jsii.get(self, "proxyConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="rootVolumeInput")
    def root_volume_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlaneRootVolume"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlaneRootVolume"], jsii.get(self, "rootVolumeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshConfigInput")
    def ssh_config_input(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterControlPlaneSshConfig"]:
        return typing.cast(typing.Optional["GoogleContainerAwsClusterControlPlaneSshConfig"], jsii.get(self, "sshConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d7e93c08dcec102ceb3d0ca57ca7f84324a74dd1e64eae87e58a57850647068b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamInstanceProfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e03743f1a4f646d30a131131a0d5c46c78ee77ccc2f0faa6ccb0b503bf23c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e78e3ac3aaa279ad32640c5d1b20557d6d2c3fac5db05be764e65e870dde4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f6d0a96c3c1d4259c77f2228db5d6c4385edf714787f4f4c275e6560779799)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296815efa8d2bf02fe040ddbab840a663e8850a115415787fc2f330b4bf6bd8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b463d636b5266b6ba670ec24e8d4318af82087213dd8b226a932a426572654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAwsClusterControlPlane]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlane], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlane],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1d06ca7583cc13d18d2438b0a79062cdf096cd410370ecd071f1c73f870d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneProxyConfig",
    jsii_struct_bases=[],
    name_mapping={"secret_arn": "secretArn", "secret_version": "secretVersion"},
)
class GoogleContainerAwsClusterControlPlaneProxyConfig:
    def __init__(
        self,
        *,
        secret_arn: builtins.str,
        secret_version: builtins.str,
    ) -> None:
        '''
        :param secret_arn: The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#secret_arn GoogleContainerAwsCluster#secret_arn}
        :param secret_version: The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#secret_version GoogleContainerAwsCluster#secret_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82bb63c8bd12177f1ef8738a171b620f35822ef844244a317d67ef9846dfc779)
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_arn": secret_arn,
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''The ARN of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#secret_arn GoogleContainerAwsCluster#secret_arn}
        '''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The version string of the AWS Secret Manager secret that contains the HTTP(S) proxy configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#secret_version GoogleContainerAwsCluster#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlaneProxyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterControlPlaneProxyConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneProxyConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99d406074f0a9ed5de65641e1570fcb7b90d9f4a6b667034faeed000dae8ea25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4744b673d8c15bfc1f8875abd867ab7df3538ec1bbbd539944069019159201f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2137a8830fbc2be0605f3f9fa4dd581c8bb158b9f2a9ad8fc7e994efb1901ad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneProxyConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneProxyConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlaneProxyConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2386ed3b898ece6bcb94bd357bfa85777013118155839062994389ec15d5bb8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneRootVolume",
    jsii_struct_bases=[],
    name_mapping={
        "iops": "iops",
        "kms_key_arn": "kmsKeyArn",
        "size_gib": "sizeGib",
        "throughput": "throughput",
        "volume_type": "volumeType",
    },
)
class GoogleContainerAwsClusterControlPlaneRootVolume:
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
        :param iops: Optional. The number of I/O operations per second (IOPS) to provision for GP3 volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iops GoogleContainerAwsCluster#iops}
        :param kms_key_arn: Optional. The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        :param size_gib: Optional. The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#size_gib GoogleContainerAwsCluster#size_gib}
        :param throughput: Optional. The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#throughput GoogleContainerAwsCluster#throughput}
        :param volume_type: Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#volume_type GoogleContainerAwsCluster#volume_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b68942c15991720bfe03393760c614f52b68e8748e32068e903b61685a5860a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#iops GoogleContainerAwsCluster#iops}
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The Amazon Resource Name (ARN) of the Customer Managed Key (CMK) used to encrypt AWS EBS volumes. If not specified, the default Amazon managed key associated to the AWS region where this cluster runs will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#kms_key_arn GoogleContainerAwsCluster#kms_key_arn}
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_gib(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The size of the volume, in GiBs. When unspecified, a default value is provided. See the specific reference in the parent resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#size_gib GoogleContainerAwsCluster#size_gib}
        '''
        result = self._values.get("size_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def throughput(self) -> typing.Optional[jsii.Number]:
        '''Optional.

        The throughput to provision for the volume, in MiB/s. Only valid if the volume type is GP3. If volume type is gp3 and throughput is not specified, the throughput will defaults to 125.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#throughput GoogleContainerAwsCluster#throughput}
        '''
        result = self._values.get("throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Type of the EBS volume. When unspecified, it defaults to GP2 volume. Possible values: VOLUME_TYPE_UNSPECIFIED, GP2, GP3.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#volume_type GoogleContainerAwsCluster#volume_type}
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlaneRootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterControlPlaneRootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneRootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c3667a5835c79aec88624bb66b856740624b91a68a79ff5122b9e80da073508)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b2d7c6ee88dd9d23ba8c27c59d7343ce1c2909361ac4ee046517baedc388eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e5829547b0c92ec474cf95d6c57b21fa73ab801538e4fe37201efe1352e1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeGib")
    def size_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGib"))

    @size_gib.setter
    def size_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ad4da6d95fba1f97c86928795968b09e32bc38008906edba9c9f74503cff23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGib", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughput")
    def throughput(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughput"))

    @throughput.setter
    def throughput(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7c7c1155b75e09e5cf64505a351502b0c60c18c9128ff11fba043a8bd88513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeType")
    def volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeType"))

    @volume_type.setter
    def volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d9b90523b1b637d2283fe09bc123ce76b0d91d3ea39450183b9f0c28f64732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneRootVolume]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneRootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlaneRootVolume],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b97fd6b527a204f5f2407864693df409b0a1c931a4ab28e6f07eb1656e679d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneSshConfig",
    jsii_struct_bases=[],
    name_mapping={"ec2_key_pair": "ec2KeyPair"},
)
class GoogleContainerAwsClusterControlPlaneSshConfig:
    def __init__(self, *, ec2_key_pair: builtins.str) -> None:
        '''
        :param ec2_key_pair: The name of the EC2 key pair used to login into cluster machines. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#ec2_key_pair GoogleContainerAwsCluster#ec2_key_pair}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bf69dc688e34002d269ea56242e68f76c2536c93c26d133e414ce5e752bb22)
            check_type(argname="argument ec2_key_pair", value=ec2_key_pair, expected_type=type_hints["ec2_key_pair"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_key_pair": ec2_key_pair,
        }

    @builtins.property
    def ec2_key_pair(self) -> builtins.str:
        '''The name of the EC2 key pair used to login into cluster machines.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#ec2_key_pair GoogleContainerAwsCluster#ec2_key_pair}
        '''
        result = self._values.get("ec2_key_pair")
        assert result is not None, "Required property 'ec2_key_pair' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterControlPlaneSshConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterControlPlaneSshConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterControlPlaneSshConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ba4a3b8325e42e1ac96402b23ec1fc2843d0504517386f17da09695119da272)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f73b3beb0d1d68a1ee1e4c1827323d63536a5ce09ce858408baa4f7db8b1ffda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2KeyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterControlPlaneSshConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterControlPlaneSshConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterControlPlaneSshConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beebfa337ca4c385f2c6d0fcb093b9362c395ae539e6cd435213d2a875ef99e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterFleet",
    jsii_struct_bases=[],
    name_mapping={"project": "project"},
)
class GoogleContainerAwsClusterFleet:
    def __init__(self, *, project: typing.Optional[builtins.str] = None) -> None:
        '''
        :param project: The number of the Fleet host project where this cluster will be registered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#project GoogleContainerAwsCluster#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f898f003447f983bf9e94f0271d8ce4adb9cb1ef45febae26f34c1ab4a3bcaec)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The number of the Fleet host project where this cluster will be registered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#project GoogleContainerAwsCluster#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterFleet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterFleetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterFleetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0673509501e5530ccd5c0ca7e541603ac7ddf138233d00a75a77ef8118106d92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa79dc37dada077b7563a00b3f0ef98d8cb917b3201eb2e9bd7d5f8428b107b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAwsClusterFleet]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterFleet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterFleet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59df2e25879a8046d7500ce420f46a1b3c995644dab6fa5850c8a5f63c29f6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"component_config": "componentConfig"},
)
class GoogleContainerAwsClusterLoggingConfig:
    def __init__(
        self,
        *,
        component_config: typing.Optional[typing.Union["GoogleContainerAwsClusterLoggingConfigComponentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param component_config: component_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#component_config GoogleContainerAwsCluster#component_config}
        '''
        if isinstance(component_config, dict):
            component_config = GoogleContainerAwsClusterLoggingConfigComponentConfig(**component_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca2591e0f1992c3050bcc1ae7d12ae5c80aa556fc646fc611f298b8f8fd487e0)
            check_type(argname="argument component_config", value=component_config, expected_type=type_hints["component_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if component_config is not None:
            self._values["component_config"] = component_config

    @builtins.property
    def component_config(
        self,
    ) -> typing.Optional["GoogleContainerAwsClusterLoggingConfigComponentConfig"]:
        '''component_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#component_config GoogleContainerAwsCluster#component_config}
        '''
        result = self._values.get("component_config")
        return typing.cast(typing.Optional["GoogleContainerAwsClusterLoggingConfigComponentConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterLoggingConfigComponentConfig",
    jsii_struct_bases=[],
    name_mapping={"enable_components": "enableComponents"},
)
class GoogleContainerAwsClusterLoggingConfigComponentConfig:
    def __init__(
        self,
        *,
        enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_components: Components of the logging configuration to be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#enable_components GoogleContainerAwsCluster#enable_components}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad30ec73a729a1a9932d57f1ebe184d6648bf3fd91b8756bf65d888995d4baf)
            check_type(argname="argument enable_components", value=enable_components, expected_type=type_hints["enable_components"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_components is not None:
            self._values["enable_components"] = enable_components

    @builtins.property
    def enable_components(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Components of the logging configuration to be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#enable_components GoogleContainerAwsCluster#enable_components}
        '''
        result = self._values.get("enable_components")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterLoggingConfigComponentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterLoggingConfigComponentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterLoggingConfigComponentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d59645e8000e1bc169db32e0020f7ecbdb88c2bb90f992704dba6069f4bc912)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b4fa1668658e1e7fd5b92703f52b61f494bfa4e0a3e7f32dccf671e0e786fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableComponents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterLoggingConfigComponentConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterLoggingConfigComponentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterLoggingConfigComponentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6413438fbc90e59973f7c7bf68d5229c1bbf4c78f8af404ad215f3b9bef13498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAwsClusterLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a1ec62f0980057746f3ea74521b549552e179869c492dc4e40dea135a5cae10)
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
        :param enable_components: Components of the logging configuration to be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#enable_components GoogleContainerAwsCluster#enable_components}
        '''
        value = GoogleContainerAwsClusterLoggingConfigComponentConfig(
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
    ) -> GoogleContainerAwsClusterLoggingConfigComponentConfigOutputReference:
        return typing.cast(GoogleContainerAwsClusterLoggingConfigComponentConfigOutputReference, jsii.get(self, "componentConfig"))

    @builtins.property
    @jsii.member(jsii_name="componentConfigInput")
    def component_config_input(
        self,
    ) -> typing.Optional[GoogleContainerAwsClusterLoggingConfigComponentConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterLoggingConfigComponentConfig], jsii.get(self, "componentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAwsClusterLoggingConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77507b4c79fa6ddf83e9cfdf0192aa82106b1f55274ab67c9e20c80e2c73a1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterNetworking",
    jsii_struct_bases=[],
    name_mapping={
        "pod_address_cidr_blocks": "podAddressCidrBlocks",
        "service_address_cidr_blocks": "serviceAddressCidrBlocks",
        "vpc_id": "vpcId",
        "per_node_pool_sg_rules_disabled": "perNodePoolSgRulesDisabled",
    },
)
class GoogleContainerAwsClusterNetworking:
    def __init__(
        self,
        *,
        pod_address_cidr_blocks: typing.Sequence[builtins.str],
        service_address_cidr_blocks: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
        per_node_pool_sg_rules_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param pod_address_cidr_blocks: All pods in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#pod_address_cidr_blocks GoogleContainerAwsCluster#pod_address_cidr_blocks}
        :param service_address_cidr_blocks: All services in the cluster are assigned an RFC1918 IPv4 address from these ranges. Only a single range is supported. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#service_address_cidr_blocks GoogleContainerAwsCluster#service_address_cidr_blocks}
        :param vpc_id: The VPC associated with the cluster. All component clusters (i.e. control plane and node pools) run on a single VPC. This field cannot be changed after creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#vpc_id GoogleContainerAwsCluster#vpc_id}
        :param per_node_pool_sg_rules_disabled: Disable the per node pool subnet security group rules on the control plane security group. When set to true, you must also provide one or more security groups that ensure node pools are able to send requests to the control plane on TCP/443 and TCP/8132. Failure to do so may result in unavailable node pools. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#per_node_pool_sg_rules_disabled GoogleContainerAwsCluster#per_node_pool_sg_rules_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8747a6f1922e759bc830a96adcf73251cbeac62dc228be2518c373ab34ac5c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#pod_address_cidr_blocks GoogleContainerAwsCluster#pod_address_cidr_blocks}
        '''
        result = self._values.get("pod_address_cidr_blocks")
        assert result is not None, "Required property 'pod_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        '''All services in the cluster are assigned an RFC1918 IPv4 address from these ranges.

        Only a single range is supported. This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#service_address_cidr_blocks GoogleContainerAwsCluster#service_address_cidr_blocks}
        '''
        result = self._values.get("service_address_cidr_blocks")
        assert result is not None, "Required property 'service_address_cidr_blocks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The VPC associated with the cluster.

        All component clusters (i.e. control plane and node pools) run on a single VPC. This field cannot be changed after creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#vpc_id GoogleContainerAwsCluster#vpc_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#per_node_pool_sg_rules_disabled GoogleContainerAwsCluster#per_node_pool_sg_rules_disabled}
        '''
        result = self._values.get("per_node_pool_sg_rules_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterNetworking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterNetworkingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterNetworkingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a755e224065ae58fb9bcfd75f4f5420fdb25a58e426c300a2a840c5a53f4376)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7a94c5009d1589690fad09c5b1c87a5cb6f8970328b52590fdc66f4c27c5264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perNodePoolSgRulesDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podAddressCidrBlocks")
    def pod_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "podAddressCidrBlocks"))

    @pod_address_cidr_blocks.setter
    def pod_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8702110ef28cd9744ceef0f793e2a2ba8deaa70d57cea357ad543f7514a30c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAddressCidrBlocks")
    def service_address_cidr_blocks(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serviceAddressCidrBlocks"))

    @service_address_cidr_blocks.setter
    def service_address_cidr_blocks(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54630463bcb31f7720f6559e926cdf3004067a8e72737b2ac7d383f61f608b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAddressCidrBlocks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26a7aecd08a2a693970d7ffcea88dab0911f318b471bdad74ef86c16727fea19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleContainerAwsClusterNetworking]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterNetworking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterNetworking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2272be9bfeb7a210dc0047ac205e12dc4f4f18acbb4fa3675e5b155194d1fd1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleContainerAwsClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#create GoogleContainerAwsCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#delete GoogleContainerAwsCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#update GoogleContainerAwsCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb80057353ff608652a50100d403b39a2aaefa02e59db9168e2dc80878d2f0af)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#create GoogleContainerAwsCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#delete GoogleContainerAwsCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_container_aws_cluster#update GoogleContainerAwsCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d49158df955e0c69771ab038e795eaf9a6e13f1875e4e45e2f4bad5b3e7c79ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6c60202909e5abe82be94f5a3af0a9391ed912f0a142c463465d251fa02f72f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad3ec13b58a636ac14714903d8a96ed674f40ac69a11b21389dedb6f19eb973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44dd44aa0e48bbe9143adeba8c9c789ec80b90154b53acf633c0fa6734666f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdaf0bc55debeafb1c43077af04849adb9e893720ba1a3b03912d1255b1e0121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterWorkloadIdentityConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleContainerAwsClusterWorkloadIdentityConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleContainerAwsClusterWorkloadIdentityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleContainerAwsClusterWorkloadIdentityConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterWorkloadIdentityConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1324c4a2da4b0bc02e183a0629498d7783b3976836c8762672c6b2880709db53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleContainerAwsClusterWorkloadIdentityConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b392773c261a9e28f9a145cea38ab2db1017194be133516a2fcb341eabc654)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleContainerAwsClusterWorkloadIdentityConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a003f02d9ec61deece72f8cadb36fd76a139d5f10406d0345ed667b0febc65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76f476edfe04f18c6b6a8622b9ac439ed759140b9b6908120f7ace4567a213a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80a1d4ec3245dea3dbc604dd3373feb4b1839ffe8bf9a4e859541832f23c42bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleContainerAwsClusterWorkloadIdentityConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleContainerAwsCluster.GoogleContainerAwsClusterWorkloadIdentityConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd203fee16c56759b9f4589892b7dc6bb745793adbff97136a7d7b2f54cbadfc)
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
    ) -> typing.Optional[GoogleContainerAwsClusterWorkloadIdentityConfig]:
        return typing.cast(typing.Optional[GoogleContainerAwsClusterWorkloadIdentityConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleContainerAwsClusterWorkloadIdentityConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed51d76f704ec877532f39213510e284211ce54d7f7fda112eca29193ae7f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleContainerAwsCluster",
    "GoogleContainerAwsClusterAuthorization",
    "GoogleContainerAwsClusterAuthorizationAdminGroups",
    "GoogleContainerAwsClusterAuthorizationAdminGroupsList",
    "GoogleContainerAwsClusterAuthorizationAdminGroupsOutputReference",
    "GoogleContainerAwsClusterAuthorizationAdminUsers",
    "GoogleContainerAwsClusterAuthorizationAdminUsersList",
    "GoogleContainerAwsClusterAuthorizationAdminUsersOutputReference",
    "GoogleContainerAwsClusterAuthorizationOutputReference",
    "GoogleContainerAwsClusterBinaryAuthorization",
    "GoogleContainerAwsClusterBinaryAuthorizationOutputReference",
    "GoogleContainerAwsClusterConfig",
    "GoogleContainerAwsClusterControlPlane",
    "GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication",
    "GoogleContainerAwsClusterControlPlaneAwsServicesAuthenticationOutputReference",
    "GoogleContainerAwsClusterControlPlaneConfigEncryption",
    "GoogleContainerAwsClusterControlPlaneConfigEncryptionOutputReference",
    "GoogleContainerAwsClusterControlPlaneDatabaseEncryption",
    "GoogleContainerAwsClusterControlPlaneDatabaseEncryptionOutputReference",
    "GoogleContainerAwsClusterControlPlaneInstancePlacement",
    "GoogleContainerAwsClusterControlPlaneInstancePlacementOutputReference",
    "GoogleContainerAwsClusterControlPlaneMainVolume",
    "GoogleContainerAwsClusterControlPlaneMainVolumeOutputReference",
    "GoogleContainerAwsClusterControlPlaneOutputReference",
    "GoogleContainerAwsClusterControlPlaneProxyConfig",
    "GoogleContainerAwsClusterControlPlaneProxyConfigOutputReference",
    "GoogleContainerAwsClusterControlPlaneRootVolume",
    "GoogleContainerAwsClusterControlPlaneRootVolumeOutputReference",
    "GoogleContainerAwsClusterControlPlaneSshConfig",
    "GoogleContainerAwsClusterControlPlaneSshConfigOutputReference",
    "GoogleContainerAwsClusterFleet",
    "GoogleContainerAwsClusterFleetOutputReference",
    "GoogleContainerAwsClusterLoggingConfig",
    "GoogleContainerAwsClusterLoggingConfigComponentConfig",
    "GoogleContainerAwsClusterLoggingConfigComponentConfigOutputReference",
    "GoogleContainerAwsClusterLoggingConfigOutputReference",
    "GoogleContainerAwsClusterNetworking",
    "GoogleContainerAwsClusterNetworkingOutputReference",
    "GoogleContainerAwsClusterTimeouts",
    "GoogleContainerAwsClusterTimeoutsOutputReference",
    "GoogleContainerAwsClusterWorkloadIdentityConfig",
    "GoogleContainerAwsClusterWorkloadIdentityConfigList",
    "GoogleContainerAwsClusterWorkloadIdentityConfigOutputReference",
]

publication.publish()

def _typecheckingstub__52929c353d6e6f063d353c91495b7143158fd964832db3e8c96a0429d7c641f8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    authorization: typing.Union[GoogleContainerAwsClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    aws_region: builtins.str,
    control_plane: typing.Union[GoogleContainerAwsClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[GoogleContainerAwsClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[GoogleContainerAwsClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[GoogleContainerAwsClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[GoogleContainerAwsClusterLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAwsClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__28f7f6a65dc16965e48449a1cf4553bfa69628610de00781fb9afaacca63e170(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a4a971f61aef9b4f6f64cf320e17976cdc9cc1453182bc28009e7c4a318c87(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f31ececaba9ea23363e23ade7948668e4ecd7168e6a11e1b7ec5691ffecdf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99616f886aa58056bcc4aa41f6d33479f8968a8281130473e4bb28fd5c43d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7c062823ca093ebef09053056703e8efeaac68f63a45e97377fa680d940311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60173d2472f3c164f864a0102187bb50b5ce93dbc5a7d4449a7d5fb9a5d73bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a8edb0b2ba55b2d754ca9aacaf4f3d58742a7d9f2cf256d4874e1ea09b002a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a90ef392b4cff53cf4ec2c56a54eff0181a65776fad606c4b0e5cb620f0817d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af3a6f05423bd407a27c1c021407a63fe039e54a02a4c140f7fdebc453e4a5d(
    *,
    admin_users: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAwsClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
    admin_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAwsClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d405d3a7924aeb06fc81a2ca0af5c9f40bd573a9c517b2e27e5738e85c78c841(
    *,
    group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303ed26817fca852e23a859d7a762ccd7a56ade02ed8eff36af68a134875eb3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37554904e2778336f24576990f07124154dc32a7967a29f8e8d62282a62552ec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3a5a1f1972ed1daea778c6c183358cd774ba00472eb1524bf7bdd1b3810775(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ffab0ebb4254e402e8266307759988a6e6c505ee89680a4b5e30620a851931(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb20fcc513be55be45ed63aa5ad5a04e9ba8a3650a43b61d577c4e5dd112945(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65428ed0c9a1480541876a796ceeb33e84fe8d037ab116359cf1ba23ce3dfc0b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7672ba212b25806d25126738dd37ca97f618d0cf209e74219c41069e6237b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb35a876b2ea00b6683889cab2f8c2600c8033557ba3f8337e5f87dbbf8b281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc734cecf3d1474257f27052226e889f0d3b33d39c6115d945325180d13d249a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterAuthorizationAdminGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d863b0763a3f769d0cf750b49fcda15c972be811ab1b06567144289ce737ae53(
    *,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ca74af68fcff99fa2423517e607ec40621cbcaf0bc9cc42c2ec5ce561cf487(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222ffe327845a5a64898886b4bb757fb27b780e9a509d083796dab7a79a458e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611d8a0fb1d120ecf48233a01289da33030d491e1145aff2c389a67f485d18bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30366d027757a495460a1de4bcfd0f94b41f6a66cba3634866af9283a25a645c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a45d7321a2a61fd2f79c328f1ec741a83151554a6576d7db8fd4d3a63d81bfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430c717bae7dbd9d4445868e677b10d1536ce0becd4cdbaa8efff5c4ca64a0f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleContainerAwsClusterAuthorizationAdminUsers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d3514251f4f706c1ca6e111a6b344d7a0d53ebe868cddc66f2cbcecc1450d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e391add4db85b6eed42d69bf58796ba9caaf1597d70898173421826784148c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50e680d1e517380296dc0afd91eb1b271fafbcf8ade3a4b2325dd87291062ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterAuthorizationAdminUsers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b169550a78d698663a82036d210388398f49917fa99969f48f56b33f650ce2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a3a505aaa7998602b3abf6712db088b7770f4d5a718356714009ee9e92f152(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAwsClusterAuthorizationAdminGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a31af21bbec966089b38bd75289f6b810aa65a1600c4e8c1b2aad71ae9edce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleContainerAwsClusterAuthorizationAdminUsers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfe8ebdbf37f2a2fb301f74d132c4d551a5928d377d8809caebf8a9ffd15a36(
    value: typing.Optional[GoogleContainerAwsClusterAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea104be39dc90a670cabc703607c367f03f41c0e4ad173257f01d4f79fb91062(
    *,
    evaluation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c686afbe1f5c7afcbf94bc440b6b0c6b67ccdd1b4ebee9413a609ef1f19b8b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d4d1e899f2b5367feb8e94b2e4766463f4daa10e073cce17c3f611e0f2582f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72369e2eda54ea2b3c1de56facad14c54cc2caca1011ce23b7da47481fd842c1(
    value: typing.Optional[GoogleContainerAwsClusterBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3efa2adbfd437ca5f27e2d10766f4f76fc2d937e8e77d0ec9ce838e849a45e1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    authorization: typing.Union[GoogleContainerAwsClusterAuthorization, typing.Dict[builtins.str, typing.Any]],
    aws_region: builtins.str,
    control_plane: typing.Union[GoogleContainerAwsClusterControlPlane, typing.Dict[builtins.str, typing.Any]],
    fleet: typing.Union[GoogleContainerAwsClusterFleet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    networking: typing.Union[GoogleContainerAwsClusterNetworking, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[GoogleContainerAwsClusterBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logging_config: typing.Optional[typing.Union[GoogleContainerAwsClusterLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleContainerAwsClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42bcdfca5a765c1e423b3108be90f10a24dbece3cc50d71600395339def315a(
    *,
    aws_services_authentication: typing.Union[GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication, typing.Dict[builtins.str, typing.Any]],
    config_encryption: typing.Union[GoogleContainerAwsClusterControlPlaneConfigEncryption, typing.Dict[builtins.str, typing.Any]],
    database_encryption: typing.Union[GoogleContainerAwsClusterControlPlaneDatabaseEncryption, typing.Dict[builtins.str, typing.Any]],
    iam_instance_profile: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    version: builtins.str,
    instance_placement: typing.Optional[typing.Union[GoogleContainerAwsClusterControlPlaneInstancePlacement, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    main_volume: typing.Optional[typing.Union[GoogleContainerAwsClusterControlPlaneMainVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    proxy_config: typing.Optional[typing.Union[GoogleContainerAwsClusterControlPlaneProxyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    root_volume: typing.Optional[typing.Union[GoogleContainerAwsClusterControlPlaneRootVolume, typing.Dict[builtins.str, typing.Any]]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssh_config: typing.Optional[typing.Union[GoogleContainerAwsClusterControlPlaneSshConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4dbb1cdc94affb96204523bdf8f54694d917da63292d7b21d4f88d57ee631c(
    *,
    role_arn: builtins.str,
    role_session_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c23f81d0f593a53f0fb9604e47f0fed594dc45cf8bca4ca5824b8923dd620d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63aad1436485e01ac6378d83b5ec0969e168b0087f3ab80f749464e52344ca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec6d0c8bd981f9eef4b6827e3fbbbdae617eabbc34e25ce37558de865a21145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8247a2a5a001b71c23c2701afcd02204a7f486389b954a8d9a7d77c77f8d6ac5(
    value: typing.Optional[GoogleContainerAwsClusterControlPlaneAwsServicesAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175f1cf82153701e086a5af526ada749a008a631fd5d6c1b5193adb24e3a7d35(
    *,
    kms_key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441910ffa932ae370be1f513fe35a8d0c714b004c62ec221f8a7ec323fd69387(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267bd0868c4c8513a6be41b05c2a93d834f4a9279ccf897e4db070642ec7ac9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2088d328e220428295213114f51c6630634b9396aa0fada01ad76b52472177(
    value: typing.Optional[GoogleContainerAwsClusterControlPlaneConfigEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef1429928587108a3e7aecaa91ec415c05cd0dbea1e10c2f149782c9dc293ae(
    *,
    kms_key_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726e88f836feaa8c2afb56956142898e39d91ead8d41643a188f3e62a82143be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54147e54613bcb81e914a770b9947f0649626aa6ba1ce07b00a06a48d810ac99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54b18d8e63ceefd3aae72beefd1230ab2ca6d716a11ecca8b3c8f2f511c1eba(
    value: typing.Optional[GoogleContainerAwsClusterControlPlaneDatabaseEncryption],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29f35f946ad78dd1176c431b01c33e079ad6c11996a6460f63978502b7046d6(
    *,
    tenancy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4706ccc36f7eef28f5bf65da15e2ea1a365e0d683671244aed446f0b3f2ff48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7050481573444a5c2cc82a95247ad2262a6c92fe31054be918e913b96ae2ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f6d35825f08634d5cdf9e82ebe02ec13a5d53352f5e15d63e5ff68809db557(
    value: typing.Optional[GoogleContainerAwsClusterControlPlaneInstancePlacement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231333bbae1fbd466117cc30bf3d4cfe8ed63989dbae845b5e509b43a61f45fb(
    *,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    size_gib: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f1cabb2a701465a8ae8cfadf5a9541e099a13063bf0ad57d4d4efc6375780a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f901a35c71e9d3c6f385892f17763cc8a7461e2a1b9d62ad6af312bd48f4b426(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae09add4519377a30b9976c1b9d1cc90aec5228ffd5185e42e023763b236b55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4050d0d9f066594ca40d9e4cbfeb4db13124f2f3d3f55b823dc45547748447f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154512e8cf7aa8406aead93c23cd523890ffac6c0bce55c5f8cb60e3b62c3c6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc1588d607a57deed323f0b19fdf03293e420aff9ff4aac4661056bc26398f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdbfe9879e9742cb7c90196cb938773e3e8f641d71b294fec7c3d14056c289c(
    value: typing.Optional[GoogleContainerAwsClusterControlPlaneMainVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653bfed173aebbfcf188359ad99af80b5842d0c355aec6f2f3e8ef502ea8c592(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e93c08dcec102ceb3d0ca57ca7f84324a74dd1e64eae87e58a57850647068b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e03743f1a4f646d30a131131a0d5c46c78ee77ccc2f0faa6ccb0b503bf23c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e78e3ac3aaa279ad32640c5d1b20557d6d2c3fac5db05be764e65e870dde4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f6d0a96c3c1d4259c77f2228db5d6c4385edf714787f4f4c275e6560779799(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296815efa8d2bf02fe040ddbab840a663e8850a115415787fc2f330b4bf6bd8f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b463d636b5266b6ba670ec24e8d4318af82087213dd8b226a932a426572654(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1d06ca7583cc13d18d2438b0a79062cdf096cd410370ecd071f1c73f870d7d(
    value: typing.Optional[GoogleContainerAwsClusterControlPlane],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bb63c8bd12177f1ef8738a171b620f35822ef844244a317d67ef9846dfc779(
    *,
    secret_arn: builtins.str,
    secret_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d406074f0a9ed5de65641e1570fcb7b90d9f4a6b667034faeed000dae8ea25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4744b673d8c15bfc1f8875abd867ab7df3538ec1bbbd539944069019159201f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2137a8830fbc2be0605f3f9fa4dd581c8bb158b9f2a9ad8fc7e994efb1901ad7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2386ed3b898ece6bcb94bd357bfa85777013118155839062994389ec15d5bb8e(
    value: typing.Optional[GoogleContainerAwsClusterControlPlaneProxyConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b68942c15991720bfe03393760c614f52b68e8748e32068e903b61685a5860a(
    *,
    iops: typing.Optional[jsii.Number] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    size_gib: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3667a5835c79aec88624bb66b856740624b91a68a79ff5122b9e80da073508(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2d7c6ee88dd9d23ba8c27c59d7343ce1c2909361ac4ee046517baedc388eca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e5829547b0c92ec474cf95d6c57b21fa73ab801538e4fe37201efe1352e1c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ad4da6d95fba1f97c86928795968b09e32bc38008906edba9c9f74503cff23(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7c7c1155b75e09e5cf64505a351502b0c60c18c9128ff11fba043a8bd88513(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d9b90523b1b637d2283fe09bc123ce76b0d91d3ea39450183b9f0c28f64732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b97fd6b527a204f5f2407864693df409b0a1c931a4ab28e6f07eb1656e679d1(
    value: typing.Optional[GoogleContainerAwsClusterControlPlaneRootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bf69dc688e34002d269ea56242e68f76c2536c93c26d133e414ce5e752bb22(
    *,
    ec2_key_pair: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba4a3b8325e42e1ac96402b23ec1fc2843d0504517386f17da09695119da272(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73b3beb0d1d68a1ee1e4c1827323d63536a5ce09ce858408baa4f7db8b1ffda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beebfa337ca4c385f2c6d0fcb093b9362c395ae539e6cd435213d2a875ef99e6(
    value: typing.Optional[GoogleContainerAwsClusterControlPlaneSshConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f898f003447f983bf9e94f0271d8ce4adb9cb1ef45febae26f34c1ab4a3bcaec(
    *,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0673509501e5530ccd5c0ca7e541603ac7ddf138233d00a75a77ef8118106d92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa79dc37dada077b7563a00b3f0ef98d8cb917b3201eb2e9bd7d5f8428b107b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59df2e25879a8046d7500ce420f46a1b3c995644dab6fa5850c8a5f63c29f6fd(
    value: typing.Optional[GoogleContainerAwsClusterFleet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2591e0f1992c3050bcc1ae7d12ae5c80aa556fc646fc611f298b8f8fd487e0(
    *,
    component_config: typing.Optional[typing.Union[GoogleContainerAwsClusterLoggingConfigComponentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad30ec73a729a1a9932d57f1ebe184d6648bf3fd91b8756bf65d888995d4baf(
    *,
    enable_components: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d59645e8000e1bc169db32e0020f7ecbdb88c2bb90f992704dba6069f4bc912(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4fa1668658e1e7fd5b92703f52b61f494bfa4e0a3e7f32dccf671e0e786fb8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6413438fbc90e59973f7c7bf68d5229c1bbf4c78f8af404ad215f3b9bef13498(
    value: typing.Optional[GoogleContainerAwsClusterLoggingConfigComponentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1ec62f0980057746f3ea74521b549552e179869c492dc4e40dea135a5cae10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77507b4c79fa6ddf83e9cfdf0192aa82106b1f55274ab67c9e20c80e2c73a1c5(
    value: typing.Optional[GoogleContainerAwsClusterLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8747a6f1922e759bc830a96adcf73251cbeac62dc228be2518c373ab34ac5c(
    *,
    pod_address_cidr_blocks: typing.Sequence[builtins.str],
    service_address_cidr_blocks: typing.Sequence[builtins.str],
    vpc_id: builtins.str,
    per_node_pool_sg_rules_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a755e224065ae58fb9bcfd75f4f5420fdb25a58e426c300a2a840c5a53f4376(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a94c5009d1589690fad09c5b1c87a5cb6f8970328b52590fdc66f4c27c5264(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8702110ef28cd9744ceef0f793e2a2ba8deaa70d57cea357ad543f7514a30c63(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54630463bcb31f7720f6559e926cdf3004067a8e72737b2ac7d383f61f608b22(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a7aecd08a2a693970d7ffcea88dab0911f318b471bdad74ef86c16727fea19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2272be9bfeb7a210dc0047ac205e12dc4f4f18acbb4fa3675e5b155194d1fd1c(
    value: typing.Optional[GoogleContainerAwsClusterNetworking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb80057353ff608652a50100d403b39a2aaefa02e59db9168e2dc80878d2f0af(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49158df955e0c69771ab038e795eaf9a6e13f1875e4e45e2f4bad5b3e7c79ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c60202909e5abe82be94f5a3af0a9391ed912f0a142c463465d251fa02f72f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad3ec13b58a636ac14714903d8a96ed674f40ac69a11b21389dedb6f19eb973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44dd44aa0e48bbe9143adeba8c9c789ec80b90154b53acf633c0fa6734666f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdaf0bc55debeafb1c43077af04849adb9e893720ba1a3b03912d1255b1e0121(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleContainerAwsClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1324c4a2da4b0bc02e183a0629498d7783b3976836c8762672c6b2880709db53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b392773c261a9e28f9a145cea38ab2db1017194be133516a2fcb341eabc654(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a003f02d9ec61deece72f8cadb36fd76a139d5f10406d0345ed667b0febc65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f476edfe04f18c6b6a8622b9ac439ed759140b9b6908120f7ace4567a213a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a1d4ec3245dea3dbc604dd3373feb4b1839ffe8bf9a4e859541832f23c42bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd203fee16c56759b9f4589892b7dc6bb745793adbff97136a7d7b2f54cbadfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed51d76f704ec877532f39213510e284211ce54d7f7fda112eca29193ae7f56(
    value: typing.Optional[GoogleContainerAwsClusterWorkloadIdentityConfig],
) -> None:
    """Type checking stubs"""
    pass
