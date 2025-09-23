r'''
# `aws_timestreaminfluxdb_db_cluster`

Refer to the Terraform Registry for docs: [`aws_timestreaminfluxdb_db_cluster`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster).
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


class TimestreaminfluxdbDbCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster aws_timestreaminfluxdb_db_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allocated_storage: jsii.Number,
        bucket: builtins.str,
        db_instance_type: builtins.str,
        name: builtins.str,
        organization: builtins.str,
        password: builtins.str,
        username: builtins.str,
        vpc_security_group_ids: typing.Sequence[builtins.str],
        vpc_subnet_ids: typing.Sequence[builtins.str],
        db_parameter_group_identifier: typing.Optional[builtins.str] = None,
        db_storage_type: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        failover_mode: typing.Optional[builtins.str] = None,
        log_delivery_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TimestreaminfluxdbDbClusterLogDeliveryConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_type: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["TimestreaminfluxdbDbClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster aws_timestreaminfluxdb_db_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param allocated_storage: The amount of storage to allocate for your DB storage type in GiB (gibibytes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#allocated_storage TimestreaminfluxdbDbCluster#allocated_storage}
        :param bucket: The name of the initial InfluxDB bucket. All InfluxDB data is stored in a bucket. A bucket combines the concept of a database and a retention period (the duration of time that each data point persists). A bucket belongs to an organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#bucket TimestreaminfluxdbDbCluster#bucket}
        :param db_instance_type: The Timestream for InfluxDB DB instance type to run InfluxDB on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_instance_type TimestreaminfluxdbDbCluster#db_instance_type}
        :param name: The name that uniquely identifies the DB cluster when interacting with the Amazon Timestream for InfluxDB API and CLI commands. This name will also be a prefix included in the endpoint. DB cluster names must be unique per customer and per region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#name TimestreaminfluxdbDbCluster#name}
        :param organization: The name of the initial organization for the initial admin user in InfluxDB. An InfluxDB organization is a workspace for a group of users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#organization TimestreaminfluxdbDbCluster#organization}
        :param password: The password of the initial admin user created in InfluxDB. This password will allow you to access the InfluxDB UI to perform various administrative tasks and also use the InfluxDB CLI to create an operator token. These attributes will be stored in a Secret created in AWS SecretManager in your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#password TimestreaminfluxdbDbCluster#password}
        :param username: The username of the initial admin user created in InfluxDB. Must start with a letter and can't end with a hyphen or contain two consecutive hyphens. For example, my-user1. This username will allow you to access the InfluxDB UI to perform various administrative tasks and also use the InfluxDB CLI to create an operator token. These attributes will be stored in a Secret created in Amazon Secrets Manager in your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#username TimestreaminfluxdbDbCluster#username}
        :param vpc_security_group_ids: A list of VPC security group IDs to associate with the Timestream for InfluxDB cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#vpc_security_group_ids TimestreaminfluxdbDbCluster#vpc_security_group_ids}
        :param vpc_subnet_ids: A list of VPC subnet IDs to associate with the DB cluster. Provide at least two VPC subnet IDs in different availability zones when deploying with a Multi-AZ standby. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#vpc_subnet_ids TimestreaminfluxdbDbCluster#vpc_subnet_ids}
        :param db_parameter_group_identifier: The ID of the DB parameter group to assign to your DB cluster. DB parameter groups specify how the database is configured. For example, DB parameter groups can specify the limit for query concurrency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_parameter_group_identifier TimestreaminfluxdbDbCluster#db_parameter_group_identifier}
        :param db_storage_type: The Timestream for InfluxDB DB storage type to read and write InfluxDB data. You can choose between 3 different types of provisioned Influx IOPS included storage according to your workloads requirements: Influx IO Included 3000 IOPS, Influx IO Included 12000 IOPS, Influx IO Included 16000 IOPS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_storage_type TimestreaminfluxdbDbCluster#db_storage_type}
        :param deployment_type: Specifies the type of cluster to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#deployment_type TimestreaminfluxdbDbCluster#deployment_type}
        :param failover_mode: Specifies the behavior of failure recovery when the primary node of the cluster fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#failover_mode TimestreaminfluxdbDbCluster#failover_mode}
        :param log_delivery_configuration: log_delivery_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#log_delivery_configuration TimestreaminfluxdbDbCluster#log_delivery_configuration}
        :param network_type: Specifies whether the networkType of the Timestream for InfluxDB cluster is IPV4, which can communicate over IPv4 protocol only, or DUAL, which can communicate over both IPv4 and IPv6 protocols. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#network_type TimestreaminfluxdbDbCluster#network_type}
        :param port: The port number on which InfluxDB accepts connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#port TimestreaminfluxdbDbCluster#port}
        :param publicly_accessible: Configures the Timestream for InfluxDB cluster with a public IP to facilitate access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#publicly_accessible TimestreaminfluxdbDbCluster#publicly_accessible}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#region TimestreaminfluxdbDbCluster#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#tags TimestreaminfluxdbDbCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#timeouts TimestreaminfluxdbDbCluster#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b8b4a41b10eb52a72200886980570872f2a0b08085ccde45be5dd0f56c3cfe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TimestreaminfluxdbDbClusterConfig(
            allocated_storage=allocated_storage,
            bucket=bucket,
            db_instance_type=db_instance_type,
            name=name,
            organization=organization,
            password=password,
            username=username,
            vpc_security_group_ids=vpc_security_group_ids,
            vpc_subnet_ids=vpc_subnet_ids,
            db_parameter_group_identifier=db_parameter_group_identifier,
            db_storage_type=db_storage_type,
            deployment_type=deployment_type,
            failover_mode=failover_mode,
            log_delivery_configuration=log_delivery_configuration,
            network_type=network_type,
            port=port,
            publicly_accessible=publicly_accessible,
            region=region,
            tags=tags,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a TimestreaminfluxdbDbCluster resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TimestreaminfluxdbDbCluster to import.
        :param import_from_id: The id of the existing TimestreaminfluxdbDbCluster that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TimestreaminfluxdbDbCluster to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6864c1517dfebbf4f54a197ce21f05662cc66515b8a580320b69a46efaacff51)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLogDeliveryConfiguration")
    def put_log_delivery_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TimestreaminfluxdbDbClusterLogDeliveryConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf474c54b20feacf0d0840d47987c816eff825d2ec3d154cdc3502bd1caa9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogDeliveryConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#create TimestreaminfluxdbDbCluster#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#delete TimestreaminfluxdbDbCluster#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#update TimestreaminfluxdbDbCluster#update}
        '''
        value = TimestreaminfluxdbDbClusterTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDbParameterGroupIdentifier")
    def reset_db_parameter_group_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbParameterGroupIdentifier", []))

    @jsii.member(jsii_name="resetDbStorageType")
    def reset_db_storage_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbStorageType", []))

    @jsii.member(jsii_name="resetDeploymentType")
    def reset_deployment_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentType", []))

    @jsii.member(jsii_name="resetFailoverMode")
    def reset_failover_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailoverMode", []))

    @jsii.member(jsii_name="resetLogDeliveryConfiguration")
    def reset_log_delivery_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDeliveryConfiguration", []))

    @jsii.member(jsii_name="resetNetworkType")
    def reset_network_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkType", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPubliclyAccessible")
    def reset_publicly_accessible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubliclyAccessible", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="influxAuthParametersSecretArn")
    def influx_auth_parameters_secret_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "influxAuthParametersSecretArn"))

    @builtins.property
    @jsii.member(jsii_name="logDeliveryConfiguration")
    def log_delivery_configuration(
        self,
    ) -> "TimestreaminfluxdbDbClusterLogDeliveryConfigurationList":
        return typing.cast("TimestreaminfluxdbDbClusterLogDeliveryConfigurationList", jsii.get(self, "logDeliveryConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="readerEndpoint")
    def reader_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readerEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "TimestreaminfluxdbDbClusterTimeoutsOutputReference":
        return typing.cast("TimestreaminfluxdbDbClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="allocatedStorageInput")
    def allocated_storage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocatedStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="dbInstanceTypeInput")
    def db_instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbInstanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="dbParameterGroupIdentifierInput")
    def db_parameter_group_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbParameterGroupIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="dbStorageTypeInput")
    def db_storage_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbStorageTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentTypeInput")
    def deployment_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="failoverModeInput")
    def failover_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failoverModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logDeliveryConfigurationInput")
    def log_delivery_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TimestreaminfluxdbDbClusterLogDeliveryConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TimestreaminfluxdbDbClusterLogDeliveryConfiguration"]]], jsii.get(self, "logDeliveryConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTypeInput")
    def network_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="publiclyAccessibleInput")
    def publicly_accessible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publiclyAccessibleInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TimestreaminfluxdbDbClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "TimestreaminfluxdbDbClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIdsInput")
    def vpc_security_group_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpcSecurityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcSubnetIdsInput")
    def vpc_subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpcSubnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="allocatedStorage")
    def allocated_storage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocatedStorage"))

    @allocated_storage.setter
    def allocated_storage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cead3528b977e6b62a9e61d2150994f6fb31d1cf704b6ca070d98e5e0c3b2240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocatedStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a02b77a04b25ebe9fc4f3d857c5e99f487c49dd69066ab29e6b237c1a65b9c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbInstanceType")
    def db_instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceType"))

    @db_instance_type.setter
    def db_instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea86a8c8bc3dc26d01b61e0886bf200a1556689787a9970f808eaff4ec4088ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbInstanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbParameterGroupIdentifier")
    def db_parameter_group_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbParameterGroupIdentifier"))

    @db_parameter_group_identifier.setter
    def db_parameter_group_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2691fe59372e0dc73d472c9a9b412026c2225937964a0c25b17de039d30ed2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbParameterGroupIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbStorageType")
    def db_storage_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbStorageType"))

    @db_storage_type.setter
    def db_storage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01d920ca18d457f7baa7ba41f516340be2fee1c16a468e8012b91bfcb99aa81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbStorageType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentType")
    def deployment_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentType"))

    @deployment_type.setter
    def deployment_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffbe7d1899595d828c4fcd3ecb19d632cebb9daf511f544106a88869fb2201bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failoverMode")
    def failover_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failoverMode"))

    @failover_mode.setter
    def failover_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23e4bb4b063b03a938e84abf6ca0089be95d3b0c549c70754d767bc50ecfc86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failoverMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da3b9499ef300ef5ddbac071b643e2f6c0467e6af12f4dc14e497cef4c02d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb9043ad8b2262494ba35ee01cc4b26ab8cb9b370fb141abaa8525f0855f8ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318dac6e234aad483dcfb6631644c5d34b73fe3c47b00abff7441465f59237c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organization", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24987a12ed992d589ece672bb162ae48f5d11b91201d1385cd4074382bd9ee11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99648cf2b9e503dfaffeabb27a5802ea4f59fb7093d992d2bea893f682d849d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publiclyAccessible"))

    @publicly_accessible.setter
    def publicly_accessible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d952f0f319eda57fac2a843f4d2c12890830a7207fd040f8d09a96fb244723d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publiclyAccessible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5824cad0605a433109a75d586bdd2addbe8045c9051a3f0626849e9e23719bbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8d0c4ee8ec42ea28c51e97beef4e2c7ed80b3b27cfed4705561b0c3d6b30c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b172da55e4ac76be4195d1e5e19a4bc5d08ceede1afa2792983715f18981d69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpcSecurityGroupIds"))

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5f60829bff7811ef065763264280033b1a770ce582085bf159dd43459ae255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcSecurityGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcSubnetIds")
    def vpc_subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vpcSubnetIds"))

    @vpc_subnet_ids.setter
    def vpc_subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebefc11220c0187b92b98b4df83f1f52d232835a3032254af1cb6301e3ea115b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcSubnetIds", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "allocated_storage": "allocatedStorage",
        "bucket": "bucket",
        "db_instance_type": "dbInstanceType",
        "name": "name",
        "organization": "organization",
        "password": "password",
        "username": "username",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
        "vpc_subnet_ids": "vpcSubnetIds",
        "db_parameter_group_identifier": "dbParameterGroupIdentifier",
        "db_storage_type": "dbStorageType",
        "deployment_type": "deploymentType",
        "failover_mode": "failoverMode",
        "log_delivery_configuration": "logDeliveryConfiguration",
        "network_type": "networkType",
        "port": "port",
        "publicly_accessible": "publiclyAccessible",
        "region": "region",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class TimestreaminfluxdbDbClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        allocated_storage: jsii.Number,
        bucket: builtins.str,
        db_instance_type: builtins.str,
        name: builtins.str,
        organization: builtins.str,
        password: builtins.str,
        username: builtins.str,
        vpc_security_group_ids: typing.Sequence[builtins.str],
        vpc_subnet_ids: typing.Sequence[builtins.str],
        db_parameter_group_identifier: typing.Optional[builtins.str] = None,
        db_storage_type: typing.Optional[builtins.str] = None,
        deployment_type: typing.Optional[builtins.str] = None,
        failover_mode: typing.Optional[builtins.str] = None,
        log_delivery_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TimestreaminfluxdbDbClusterLogDeliveryConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        network_type: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["TimestreaminfluxdbDbClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param allocated_storage: The amount of storage to allocate for your DB storage type in GiB (gibibytes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#allocated_storage TimestreaminfluxdbDbCluster#allocated_storage}
        :param bucket: The name of the initial InfluxDB bucket. All InfluxDB data is stored in a bucket. A bucket combines the concept of a database and a retention period (the duration of time that each data point persists). A bucket belongs to an organization. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#bucket TimestreaminfluxdbDbCluster#bucket}
        :param db_instance_type: The Timestream for InfluxDB DB instance type to run InfluxDB on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_instance_type TimestreaminfluxdbDbCluster#db_instance_type}
        :param name: The name that uniquely identifies the DB cluster when interacting with the Amazon Timestream for InfluxDB API and CLI commands. This name will also be a prefix included in the endpoint. DB cluster names must be unique per customer and per region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#name TimestreaminfluxdbDbCluster#name}
        :param organization: The name of the initial organization for the initial admin user in InfluxDB. An InfluxDB organization is a workspace for a group of users. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#organization TimestreaminfluxdbDbCluster#organization}
        :param password: The password of the initial admin user created in InfluxDB. This password will allow you to access the InfluxDB UI to perform various administrative tasks and also use the InfluxDB CLI to create an operator token. These attributes will be stored in a Secret created in AWS SecretManager in your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#password TimestreaminfluxdbDbCluster#password}
        :param username: The username of the initial admin user created in InfluxDB. Must start with a letter and can't end with a hyphen or contain two consecutive hyphens. For example, my-user1. This username will allow you to access the InfluxDB UI to perform various administrative tasks and also use the InfluxDB CLI to create an operator token. These attributes will be stored in a Secret created in Amazon Secrets Manager in your account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#username TimestreaminfluxdbDbCluster#username}
        :param vpc_security_group_ids: A list of VPC security group IDs to associate with the Timestream for InfluxDB cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#vpc_security_group_ids TimestreaminfluxdbDbCluster#vpc_security_group_ids}
        :param vpc_subnet_ids: A list of VPC subnet IDs to associate with the DB cluster. Provide at least two VPC subnet IDs in different availability zones when deploying with a Multi-AZ standby. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#vpc_subnet_ids TimestreaminfluxdbDbCluster#vpc_subnet_ids}
        :param db_parameter_group_identifier: The ID of the DB parameter group to assign to your DB cluster. DB parameter groups specify how the database is configured. For example, DB parameter groups can specify the limit for query concurrency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_parameter_group_identifier TimestreaminfluxdbDbCluster#db_parameter_group_identifier}
        :param db_storage_type: The Timestream for InfluxDB DB storage type to read and write InfluxDB data. You can choose between 3 different types of provisioned Influx IOPS included storage according to your workloads requirements: Influx IO Included 3000 IOPS, Influx IO Included 12000 IOPS, Influx IO Included 16000 IOPS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_storage_type TimestreaminfluxdbDbCluster#db_storage_type}
        :param deployment_type: Specifies the type of cluster to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#deployment_type TimestreaminfluxdbDbCluster#deployment_type}
        :param failover_mode: Specifies the behavior of failure recovery when the primary node of the cluster fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#failover_mode TimestreaminfluxdbDbCluster#failover_mode}
        :param log_delivery_configuration: log_delivery_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#log_delivery_configuration TimestreaminfluxdbDbCluster#log_delivery_configuration}
        :param network_type: Specifies whether the networkType of the Timestream for InfluxDB cluster is IPV4, which can communicate over IPv4 protocol only, or DUAL, which can communicate over both IPv4 and IPv6 protocols. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#network_type TimestreaminfluxdbDbCluster#network_type}
        :param port: The port number on which InfluxDB accepts connections. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#port TimestreaminfluxdbDbCluster#port}
        :param publicly_accessible: Configures the Timestream for InfluxDB cluster with a public IP to facilitate access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#publicly_accessible TimestreaminfluxdbDbCluster#publicly_accessible}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#region TimestreaminfluxdbDbCluster#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#tags TimestreaminfluxdbDbCluster#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#timeouts TimestreaminfluxdbDbCluster#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = TimestreaminfluxdbDbClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af8a3b18315b3be97d5793fca42940e8f6d9e970bbccedf20efd6cd16dd4c300)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument allocated_storage", value=allocated_storage, expected_type=type_hints["allocated_storage"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument db_instance_type", value=db_instance_type, expected_type=type_hints["db_instance_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
            check_type(argname="argument vpc_subnet_ids", value=vpc_subnet_ids, expected_type=type_hints["vpc_subnet_ids"])
            check_type(argname="argument db_parameter_group_identifier", value=db_parameter_group_identifier, expected_type=type_hints["db_parameter_group_identifier"])
            check_type(argname="argument db_storage_type", value=db_storage_type, expected_type=type_hints["db_storage_type"])
            check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
            check_type(argname="argument failover_mode", value=failover_mode, expected_type=type_hints["failover_mode"])
            check_type(argname="argument log_delivery_configuration", value=log_delivery_configuration, expected_type=type_hints["log_delivery_configuration"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allocated_storage": allocated_storage,
            "bucket": bucket,
            "db_instance_type": db_instance_type,
            "name": name,
            "organization": organization,
            "password": password,
            "username": username,
            "vpc_security_group_ids": vpc_security_group_ids,
            "vpc_subnet_ids": vpc_subnet_ids,
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
        if db_parameter_group_identifier is not None:
            self._values["db_parameter_group_identifier"] = db_parameter_group_identifier
        if db_storage_type is not None:
            self._values["db_storage_type"] = db_storage_type
        if deployment_type is not None:
            self._values["deployment_type"] = deployment_type
        if failover_mode is not None:
            self._values["failover_mode"] = failover_mode
        if log_delivery_configuration is not None:
            self._values["log_delivery_configuration"] = log_delivery_configuration
        if network_type is not None:
            self._values["network_type"] = network_type
        if port is not None:
            self._values["port"] = port
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
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
    def allocated_storage(self) -> jsii.Number:
        '''The amount of storage to allocate for your DB storage type in GiB (gibibytes).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#allocated_storage TimestreaminfluxdbDbCluster#allocated_storage}
        '''
        result = self._values.get("allocated_storage")
        assert result is not None, "Required property 'allocated_storage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def bucket(self) -> builtins.str:
        '''The name of the initial InfluxDB bucket.

        All InfluxDB data is stored in a bucket.
        A bucket combines the concept of a database and a retention period (the duration of time
        that each data point persists). A bucket belongs to an organization.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#bucket TimestreaminfluxdbDbCluster#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_instance_type(self) -> builtins.str:
        '''The Timestream for InfluxDB DB instance type to run InfluxDB on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_instance_type TimestreaminfluxdbDbCluster#db_instance_type}
        '''
        result = self._values.get("db_instance_type")
        assert result is not None, "Required property 'db_instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name that uniquely identifies the DB cluster when interacting with the  					Amazon Timestream for InfluxDB API and CLI commands.

        This name will also be a
        prefix included in the endpoint. DB cluster names must be unique per customer
        and per region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#name TimestreaminfluxdbDbCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''The name of the initial organization for the initial admin user in InfluxDB.

        An
        InfluxDB organization is a workspace for a group of users.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#organization TimestreaminfluxdbDbCluster#organization}
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''The password of the initial admin user created in InfluxDB.

        This password will
        allow you to access the InfluxDB UI to perform various administrative tasks and
        also use the InfluxDB CLI to create an operator token. These attributes will be
        stored in a Secret created in AWS SecretManager in your account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#password TimestreaminfluxdbDbCluster#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username of the initial admin user created in InfluxDB.

        Must start with a letter and can't end with a hyphen or contain two
        consecutive hyphens. For example, my-user1. This username will allow
        you to access the InfluxDB UI to perform various administrative tasks
        and also use the InfluxDB CLI to create an operator token. These
        attributes will be stored in a Secret created in Amazon Secrets
        Manager in your account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#username TimestreaminfluxdbDbCluster#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.List[builtins.str]:
        '''A list of VPC security group IDs to associate with the Timestream for InfluxDB cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#vpc_security_group_ids TimestreaminfluxdbDbCluster#vpc_security_group_ids}
        '''
        result = self._values.get("vpc_security_group_ids")
        assert result is not None, "Required property 'vpc_security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_subnet_ids(self) -> typing.List[builtins.str]:
        '''A list of VPC subnet IDs to associate with the DB cluster.

        Provide at least
        two VPC subnet IDs in different availability zones when deploying with a Multi-AZ standby.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#vpc_subnet_ids TimestreaminfluxdbDbCluster#vpc_subnet_ids}
        '''
        result = self._values.get("vpc_subnet_ids")
        assert result is not None, "Required property 'vpc_subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def db_parameter_group_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the DB parameter group to assign to your DB cluster.

        DB parameter groups specify how the database is configured. For example, DB parameter groups
        can specify the limit for query concurrency.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_parameter_group_identifier TimestreaminfluxdbDbCluster#db_parameter_group_identifier}
        '''
        result = self._values.get("db_parameter_group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_storage_type(self) -> typing.Optional[builtins.str]:
        '''The Timestream for InfluxDB DB storage type to read and write InfluxDB data.

        You can choose between 3 different types of provisioned Influx IOPS included storage according
        to your workloads requirements: Influx IO Included 3000 IOPS, Influx IO Included 12000 IOPS,
        Influx IO Included 16000 IOPS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#db_storage_type TimestreaminfluxdbDbCluster#db_storage_type}
        '''
        result = self._values.get("db_storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of cluster to create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#deployment_type TimestreaminfluxdbDbCluster#deployment_type}
        '''
        result = self._values.get("deployment_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failover_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of failure recovery when the primary node of the cluster 					fails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#failover_mode TimestreaminfluxdbDbCluster#failover_mode}
        '''
        result = self._values.get("failover_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TimestreaminfluxdbDbClusterLogDeliveryConfiguration"]]]:
        '''log_delivery_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#log_delivery_configuration TimestreaminfluxdbDbCluster#log_delivery_configuration}
        '''
        result = self._values.get("log_delivery_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TimestreaminfluxdbDbClusterLogDeliveryConfiguration"]]], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the networkType of the Timestream for InfluxDB cluster is  					IPV4, which can communicate over IPv4 protocol only, or DUAL, which can communicate  					over both IPv4 and IPv6 protocols.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#network_type TimestreaminfluxdbDbCluster#network_type}
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which InfluxDB accepts connections.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#port TimestreaminfluxdbDbCluster#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Configures the Timestream for InfluxDB cluster with a public IP to facilitate access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#publicly_accessible TimestreaminfluxdbDbCluster#publicly_accessible}
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#region TimestreaminfluxdbDbCluster#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#tags TimestreaminfluxdbDbCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["TimestreaminfluxdbDbClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#timeouts TimestreaminfluxdbDbCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["TimestreaminfluxdbDbClusterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TimestreaminfluxdbDbClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterLogDeliveryConfiguration",
    jsii_struct_bases=[],
    name_mapping={"s3_configuration": "s3Configuration"},
)
class TimestreaminfluxdbDbClusterLogDeliveryConfiguration:
    def __init__(
        self,
        *,
        s3_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#s3_configuration TimestreaminfluxdbDbCluster#s3_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6e5a741b2918043317ae54fa8891a28b67042d511a1b4e52c35a6cda3af9f8)
            check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_configuration is not None:
            self._values["s3_configuration"] = s3_configuration

    @builtins.property
    def s3_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration"]]]:
        '''s3_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#s3_configuration TimestreaminfluxdbDbCluster#s3_configuration}
        '''
        result = self._values.get("s3_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TimestreaminfluxdbDbClusterLogDeliveryConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TimestreaminfluxdbDbClusterLogDeliveryConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterLogDeliveryConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0a833beb2ee1dc040276506da978a1495aeafa0953e57d0baf19284d770cdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TimestreaminfluxdbDbClusterLogDeliveryConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae6c2a286d6cb474be2813fbaba607977eedd9c297a9cc91a8ec34bba5effe1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TimestreaminfluxdbDbClusterLogDeliveryConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f499625c25df62d818ceaa1fdc5e52cfdbec767fc63dce1f5a918005aa74de7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bdb6fcfd90d5f4b7afbfdc8d9bc20e9741545bdc402712c74a407d8b9d0e7c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ee16ba2f8be229526cd3a65b8a3441470728aa271254d11124b8ad1b10f09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TimestreaminfluxdbDbClusterLogDeliveryConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TimestreaminfluxdbDbClusterLogDeliveryConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TimestreaminfluxdbDbClusterLogDeliveryConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7694d8646c5791d324e692f05785dacc5a122c78f1c80671bc584d2074c17876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TimestreaminfluxdbDbClusterLogDeliveryConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterLogDeliveryConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35d37919479ba489928f49394e9f9b193f59739be8873a6e90853ed2b064e1ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putS3Configuration")
    def put_s3_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e90325e813b535ded458b7d9fd5fe8aca37b79138a2f7e69ca697cc1864ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3Configuration", [value]))

    @jsii.member(jsii_name="resetS3Configuration")
    def reset_s3_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Configuration", []))

    @builtins.property
    @jsii.member(jsii_name="s3Configuration")
    def s3_configuration(
        self,
    ) -> "TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationList":
        return typing.cast("TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationList", jsii.get(self, "s3Configuration"))

    @builtins.property
    @jsii.member(jsii_name="s3ConfigurationInput")
    def s3_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration"]]], jsii.get(self, "s3ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterLogDeliveryConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterLogDeliveryConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterLogDeliveryConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0755cbb56e066ad6ccd9493aa4b575603422f1e35aea15af6d545ac4df0057a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration",
    jsii_struct_bases=[],
    name_mapping={"bucket_name": "bucketName", "enabled": "enabled"},
)
class TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param bucket_name: The name of the S3 bucket to deliver logs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#bucket_name TimestreaminfluxdbDbCluster#bucket_name}
        :param enabled: Indicates whether log delivery to the S3 bucket is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#enabled TimestreaminfluxdbDbCluster#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__535cf7832a3543eed51f9c09925ff4a85e22c9248e49c386187fba4d1ef76ce6)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "enabled": enabled,
        }

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The name of the S3 bucket to deliver logs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#bucket_name TimestreaminfluxdbDbCluster#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether log delivery to the S3 bucket is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#enabled TimestreaminfluxdbDbCluster#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__146c3083a21d4f493487f097c53d64c884dc6a486109e886daf755698dc0096c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4be5d7228e877d419218c661f9934db53ebc58186c6c5bbbd2e8c842b70cc8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d701e146dbbc2bd74d5d3e191f7763caa84f124b0d1926477587e1e66e69747)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97bf09982a9c1c2cc4515eb504270704b713a1fef53983624c4d9f7fafe5213e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdff4ec9be479fb65e038860fc7f6c5dc43337987da8eff67f0d71ba1ca0e705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e1d117d030b3c868cc22c583ecb2de879c5a2d7d08f1799ce8f3f8c6cc0b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ea307bbbb4d1d8109d529c43b28b9eec6b36a86b790d3fbbaccad6f132d6f37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ca0c99f25b289cf24477be5f3c80e51174407c3340381e47ea1587140da375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c42390154012eba8bb3bd5251bd3688313fbc3cebf555eff23564015c7022ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27ef70802496f78d5ade66f8a8181013c0caf17b97d3dc50604cbcb3f8138c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class TimestreaminfluxdbDbClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#create TimestreaminfluxdbDbCluster#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#delete TimestreaminfluxdbDbCluster#delete}
        :param update: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#update TimestreaminfluxdbDbCluster#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a693343121a6559ef8ce786b80ae0e44be40af488ec0552a2df8139cbbb12d)
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
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#create TimestreaminfluxdbDbCluster#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#delete TimestreaminfluxdbDbCluster#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/timestreaminfluxdb_db_cluster#update TimestreaminfluxdbDbCluster#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TimestreaminfluxdbDbClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TimestreaminfluxdbDbClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.timestreaminfluxdbDbCluster.TimestreaminfluxdbDbClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2836032aa1084838d4bfa7e60447015974f9e1ea359a51e4f04046dd2fe0030a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e75b5bd6369b6b9fb72f848cbdc91db3af6c5fc38215b7170c3e7250db13b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da479adb4385068810007a7e34ff12af753b5bdfa9013951c33288a91a647a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984697184e95c654c9a325f8d36ff80d29dff72c5b3b538e584093e7adf5ae94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4a2bcca32ba174f416471135cc185f954772367e4c90aed62fc7361ef092eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TimestreaminfluxdbDbCluster",
    "TimestreaminfluxdbDbClusterConfig",
    "TimestreaminfluxdbDbClusterLogDeliveryConfiguration",
    "TimestreaminfluxdbDbClusterLogDeliveryConfigurationList",
    "TimestreaminfluxdbDbClusterLogDeliveryConfigurationOutputReference",
    "TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration",
    "TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationList",
    "TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3ConfigurationOutputReference",
    "TimestreaminfluxdbDbClusterTimeouts",
    "TimestreaminfluxdbDbClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__97b8b4a41b10eb52a72200886980570872f2a0b08085ccde45be5dd0f56c3cfe(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allocated_storage: jsii.Number,
    bucket: builtins.str,
    db_instance_type: builtins.str,
    name: builtins.str,
    organization: builtins.str,
    password: builtins.str,
    username: builtins.str,
    vpc_security_group_ids: typing.Sequence[builtins.str],
    vpc_subnet_ids: typing.Sequence[builtins.str],
    db_parameter_group_identifier: typing.Optional[builtins.str] = None,
    db_storage_type: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    failover_mode: typing.Optional[builtins.str] = None,
    log_delivery_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TimestreaminfluxdbDbClusterLogDeliveryConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_type: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[TimestreaminfluxdbDbClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6864c1517dfebbf4f54a197ce21f05662cc66515b8a580320b69a46efaacff51(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf474c54b20feacf0d0840d47987c816eff825d2ec3d154cdc3502bd1caa9b0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TimestreaminfluxdbDbClusterLogDeliveryConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cead3528b977e6b62a9e61d2150994f6fb31d1cf704b6ca070d98e5e0c3b2240(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a02b77a04b25ebe9fc4f3d857c5e99f487c49dd69066ab29e6b237c1a65b9c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea86a8c8bc3dc26d01b61e0886bf200a1556689787a9970f808eaff4ec4088ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2691fe59372e0dc73d472c9a9b412026c2225937964a0c25b17de039d30ed2e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01d920ca18d457f7baa7ba41f516340be2fee1c16a468e8012b91bfcb99aa81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbe7d1899595d828c4fcd3ecb19d632cebb9daf511f544106a88869fb2201bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23e4bb4b063b03a938e84abf6ca0089be95d3b0c549c70754d767bc50ecfc86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da3b9499ef300ef5ddbac071b643e2f6c0467e6af12f4dc14e497cef4c02d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb9043ad8b2262494ba35ee01cc4b26ab8cb9b370fb141abaa8525f0855f8ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318dac6e234aad483dcfb6631644c5d34b73fe3c47b00abff7441465f59237c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24987a12ed992d589ece672bb162ae48f5d11b91201d1385cd4074382bd9ee11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99648cf2b9e503dfaffeabb27a5802ea4f59fb7093d992d2bea893f682d849d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d952f0f319eda57fac2a843f4d2c12890830a7207fd040f8d09a96fb244723d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5824cad0605a433109a75d586bdd2addbe8045c9051a3f0626849e9e23719bbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d0c4ee8ec42ea28c51e97beef4e2c7ed80b3b27cfed4705561b0c3d6b30c01(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b172da55e4ac76be4195d1e5e19a4bc5d08ceede1afa2792983715f18981d69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5f60829bff7811ef065763264280033b1a770ce582085bf159dd43459ae255(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebefc11220c0187b92b98b4df83f1f52d232835a3032254af1cb6301e3ea115b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8a3b18315b3be97d5793fca42940e8f6d9e970bbccedf20efd6cd16dd4c300(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    allocated_storage: jsii.Number,
    bucket: builtins.str,
    db_instance_type: builtins.str,
    name: builtins.str,
    organization: builtins.str,
    password: builtins.str,
    username: builtins.str,
    vpc_security_group_ids: typing.Sequence[builtins.str],
    vpc_subnet_ids: typing.Sequence[builtins.str],
    db_parameter_group_identifier: typing.Optional[builtins.str] = None,
    db_storage_type: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    failover_mode: typing.Optional[builtins.str] = None,
    log_delivery_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TimestreaminfluxdbDbClusterLogDeliveryConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    network_type: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[TimestreaminfluxdbDbClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6e5a741b2918043317ae54fa8891a28b67042d511a1b4e52c35a6cda3af9f8(
    *,
    s3_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0a833beb2ee1dc040276506da978a1495aeafa0953e57d0baf19284d770cdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae6c2a286d6cb474be2813fbaba607977eedd9c297a9cc91a8ec34bba5effe1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f499625c25df62d818ceaa1fdc5e52cfdbec767fc63dce1f5a918005aa74de7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdb6fcfd90d5f4b7afbfdc8d9bc20e9741545bdc402712c74a407d8b9d0e7c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ee16ba2f8be229526cd3a65b8a3441470728aa271254d11124b8ad1b10f09f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7694d8646c5791d324e692f05785dacc5a122c78f1c80671bc584d2074c17876(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TimestreaminfluxdbDbClusterLogDeliveryConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d37919479ba489928f49394e9f9b193f59739be8873a6e90853ed2b064e1ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e90325e813b535ded458b7d9fd5fe8aca37b79138a2f7e69ca697cc1864ac9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0755cbb56e066ad6ccd9493aa4b575603422f1e35aea15af6d545ac4df0057a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterLogDeliveryConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__535cf7832a3543eed51f9c09925ff4a85e22c9248e49c386187fba4d1ef76ce6(
    *,
    bucket_name: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146c3083a21d4f493487f097c53d64c884dc6a486109e886daf755698dc0096c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4be5d7228e877d419218c661f9934db53ebc58186c6c5bbbd2e8c842b70cc8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d701e146dbbc2bd74d5d3e191f7763caa84f124b0d1926477587e1e66e69747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97bf09982a9c1c2cc4515eb504270704b713a1fef53983624c4d9f7fafe5213e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdff4ec9be479fb65e038860fc7f6c5dc43337987da8eff67f0d71ba1ca0e705(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e1d117d030b3c868cc22c583ecb2de879c5a2d7d08f1799ce8f3f8c6cc0b8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea307bbbb4d1d8109d529c43b28b9eec6b36a86b790d3fbbaccad6f132d6f37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ca0c99f25b289cf24477be5f3c80e51174407c3340381e47ea1587140da375(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c42390154012eba8bb3bd5251bd3688313fbc3cebf555eff23564015c7022ef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27ef70802496f78d5ade66f8a8181013c0caf17b97d3dc50604cbcb3f8138c5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterLogDeliveryConfigurationS3Configuration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a693343121a6559ef8ce786b80ae0e44be40af488ec0552a2df8139cbbb12d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2836032aa1084838d4bfa7e60447015974f9e1ea359a51e4f04046dd2fe0030a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e75b5bd6369b6b9fb72f848cbdc91db3af6c5fc38215b7170c3e7250db13b95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da479adb4385068810007a7e34ff12af753b5bdfa9013951c33288a91a647a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984697184e95c654c9a325f8d36ff80d29dff72c5b3b538e584093e7adf5ae94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4a2bcca32ba174f416471135cc185f954772367e4c90aed62fc7361ef092eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TimestreaminfluxdbDbClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
