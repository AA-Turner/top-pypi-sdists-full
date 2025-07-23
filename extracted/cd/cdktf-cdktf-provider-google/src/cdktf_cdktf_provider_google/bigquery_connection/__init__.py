r'''
# `google_bigquery_connection`

Refer to the Terraform Registry for docs: [`google_bigquery_connection`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection).
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


class BigqueryConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnection",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection google_bigquery_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        aws: typing.Optional[typing.Union["BigqueryConnectionAws", typing.Dict[builtins.str, typing.Any]]] = None,
        azure: typing.Optional[typing.Union["BigqueryConnectionAzure", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_resource: typing.Optional[typing.Union["BigqueryConnectionCloudResource", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_spanner: typing.Optional[typing.Union["BigqueryConnectionCloudSpanner", typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_sql: typing.Optional[typing.Union["BigqueryConnectionCloudSql", typing.Dict[builtins.str, typing.Any]]] = None,
        connection_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spark: typing.Optional[typing.Union["BigqueryConnectionSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigqueryConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection google_bigquery_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#aws BigqueryConnection#aws}
        :param azure: azure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#azure BigqueryConnection#azure}
        :param cloud_resource: cloud_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_resource BigqueryConnection#cloud_resource}
        :param cloud_spanner: cloud_spanner block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_spanner BigqueryConnection#cloud_spanner}
        :param cloud_sql: cloud_sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_sql BigqueryConnection#cloud_sql}
        :param connection_id: Optional connection id that should be assigned to the created connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#connection_id BigqueryConnection#connection_id}
        :param description: A descriptive description for the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#description BigqueryConnection#description}
        :param friendly_name: A descriptive name for the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#friendly_name BigqueryConnection#friendly_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#id BigqueryConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: Optional. The Cloud KMS key that is used for encryption. Example: projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#kms_key_name BigqueryConnection#kms_key_name}
        :param location: The geographic location where the connection should reside. Cloud SQL instance must be in the same location as the connection with following exceptions: Cloud SQL us-central1 maps to BigQuery US, Cloud SQL europe-west1 maps to BigQuery EU. Examples: US, EU, asia-northeast1, us-central1, europe-west1. Spanner Connections same as spanner region AWS allowed regions are aws-us-east-1 Azure allowed regions are azure-eastus2 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#location BigqueryConnection#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#project BigqueryConnection#project}.
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#spark BigqueryConnection#spark}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#timeouts BigqueryConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f2d61e5ca7e04dd63633186fd07c52ef22872e0d18462677aed81403df9898d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryConnectionConfig(
            aws=aws,
            azure=azure,
            cloud_resource=cloud_resource,
            cloud_spanner=cloud_spanner,
            cloud_sql=cloud_sql,
            connection_id=connection_id,
            description=description,
            friendly_name=friendly_name,
            id=id,
            kms_key_name=kms_key_name,
            location=location,
            project=project,
            spark=spark,
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
        '''Generates CDKTF code for importing a BigqueryConnection resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigqueryConnection to import.
        :param import_from_id: The id of the existing BigqueryConnection that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigqueryConnection to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dcda366192c9dedcfe270d7e06afed548741da8b2ff11f1e76cba81cab0ce8b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAws")
    def put_aws(
        self,
        *,
        access_role: typing.Union["BigqueryConnectionAwsAccessRole", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param access_role: access_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#access_role BigqueryConnection#access_role}
        '''
        value = BigqueryConnectionAws(access_role=access_role)

        return typing.cast(None, jsii.invoke(self, "putAws", [value]))

    @jsii.member(jsii_name="putAzure")
    def put_azure(
        self,
        *,
        customer_tenant_id: builtins.str,
        federated_application_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param customer_tenant_id: The id of customer's directory that host the data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#customer_tenant_id BigqueryConnection#customer_tenant_id}
        :param federated_application_client_id: The Azure Application (client) ID where the federated credentials will be hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#federated_application_client_id BigqueryConnection#federated_application_client_id}
        '''
        value = BigqueryConnectionAzure(
            customer_tenant_id=customer_tenant_id,
            federated_application_client_id=federated_application_client_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAzure", [value]))

    @jsii.member(jsii_name="putCloudResource")
    def put_cloud_resource(self) -> None:
        value = BigqueryConnectionCloudResource()

        return typing.cast(None, jsii.invoke(self, "putCloudResource", [value]))

    @jsii.member(jsii_name="putCloudSpanner")
    def put_cloud_spanner(
        self,
        *,
        database: builtins.str,
        database_role: typing.Optional[builtins.str] = None,
        max_parallelism: typing.Optional[jsii.Number] = None,
        use_data_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_parallelism: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_serverless_analytics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param database: Cloud Spanner database in the form 'project/instance/database'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database BigqueryConnection#database}
        :param database_role: Cloud Spanner database role for fine-grained access control. The Cloud Spanner admin should have provisioned the database role with appropriate permissions, such as 'SELECT' and 'INSERT'. Other users should only use roles provided by their Cloud Spanner admins. The database role name must start with a letter, and can only contain letters, numbers, and underscores. For more details, see https://cloud.google.com/spanner/docs/fgac-about. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database_role BigqueryConnection#database_role}
        :param max_parallelism: Allows setting max parallelism per query when executing on Spanner independent compute resources. If unspecified, default values of parallelism are chosen that are dependent on the Cloud Spanner instance configuration. 'useParallelism' and 'useDataBoost' must be set when setting max parallelism. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#max_parallelism BigqueryConnection#max_parallelism}
        :param use_data_boost: If set, the request will be executed via Spanner independent compute resources. 'use_parallelism' must be set when using data boost. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_data_boost BigqueryConnection#use_data_boost}
        :param use_parallelism: If parallelism should be used when reading from Cloud Spanner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_parallelism BigqueryConnection#use_parallelism}
        :param use_serverless_analytics: If the serverless analytics service should be used to read data from Cloud Spanner. 'useParallelism' must be set when using serverless analytics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_serverless_analytics BigqueryConnection#use_serverless_analytics}
        '''
        value = BigqueryConnectionCloudSpanner(
            database=database,
            database_role=database_role,
            max_parallelism=max_parallelism,
            use_data_boost=use_data_boost,
            use_parallelism=use_parallelism,
            use_serverless_analytics=use_serverless_analytics,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudSpanner", [value]))

    @jsii.member(jsii_name="putCloudSql")
    def put_cloud_sql(
        self,
        *,
        credential: typing.Union["BigqueryConnectionCloudSqlCredential", typing.Dict[builtins.str, typing.Any]],
        database: builtins.str,
        instance_id: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param credential: credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#credential BigqueryConnection#credential}
        :param database: Database name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database BigqueryConnection#database}
        :param instance_id: Cloud SQL instance ID in the form project:location:instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#instance_id BigqueryConnection#instance_id}
        :param type: Type of the Cloud SQL database. Possible values: ["DATABASE_TYPE_UNSPECIFIED", "POSTGRES", "MYSQL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#type BigqueryConnection#type}
        '''
        value = BigqueryConnectionCloudSql(
            credential=credential,
            database=database,
            instance_id=instance_id,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudSql", [value]))

    @jsii.member(jsii_name="putSpark")
    def put_spark(
        self,
        *,
        metastore_service_config: typing.Optional[typing.Union["BigqueryConnectionSparkMetastoreServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_history_server_config: typing.Optional[typing.Union["BigqueryConnectionSparkSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service_config: metastore_service_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#metastore_service_config BigqueryConnection#metastore_service_config}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#spark_history_server_config BigqueryConnection#spark_history_server_config}
        '''
        value = BigqueryConnectionSpark(
            metastore_service_config=metastore_service_config,
            spark_history_server_config=spark_history_server_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSpark", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#create BigqueryConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#delete BigqueryConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#update BigqueryConnection#update}.
        '''
        value = BigqueryConnectionTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAws")
    def reset_aws(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAws", []))

    @jsii.member(jsii_name="resetAzure")
    def reset_azure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzure", []))

    @jsii.member(jsii_name="resetCloudResource")
    def reset_cloud_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudResource", []))

    @jsii.member(jsii_name="resetCloudSpanner")
    def reset_cloud_spanner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSpanner", []))

    @jsii.member(jsii_name="resetCloudSql")
    def reset_cloud_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSql", []))

    @jsii.member(jsii_name="resetConnectionId")
    def reset_connection_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetFriendlyName")
    def reset_friendly_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFriendlyName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSpark")
    def reset_spark(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpark", []))

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
    @jsii.member(jsii_name="aws")
    def aws(self) -> "BigqueryConnectionAwsOutputReference":
        return typing.cast("BigqueryConnectionAwsOutputReference", jsii.get(self, "aws"))

    @builtins.property
    @jsii.member(jsii_name="azure")
    def azure(self) -> "BigqueryConnectionAzureOutputReference":
        return typing.cast("BigqueryConnectionAzureOutputReference", jsii.get(self, "azure"))

    @builtins.property
    @jsii.member(jsii_name="cloudResource")
    def cloud_resource(self) -> "BigqueryConnectionCloudResourceOutputReference":
        return typing.cast("BigqueryConnectionCloudResourceOutputReference", jsii.get(self, "cloudResource"))

    @builtins.property
    @jsii.member(jsii_name="cloudSpanner")
    def cloud_spanner(self) -> "BigqueryConnectionCloudSpannerOutputReference":
        return typing.cast("BigqueryConnectionCloudSpannerOutputReference", jsii.get(self, "cloudSpanner"))

    @builtins.property
    @jsii.member(jsii_name="cloudSql")
    def cloud_sql(self) -> "BigqueryConnectionCloudSqlOutputReference":
        return typing.cast("BigqueryConnectionCloudSqlOutputReference", jsii.get(self, "cloudSql"))

    @builtins.property
    @jsii.member(jsii_name="hasCredential")
    def has_credential(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hasCredential"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="spark")
    def spark(self) -> "BigqueryConnectionSparkOutputReference":
        return typing.cast("BigqueryConnectionSparkOutputReference", jsii.get(self, "spark"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryConnectionTimeoutsOutputReference":
        return typing.cast("BigqueryConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="awsInput")
    def aws_input(self) -> typing.Optional["BigqueryConnectionAws"]:
        return typing.cast(typing.Optional["BigqueryConnectionAws"], jsii.get(self, "awsInput"))

    @builtins.property
    @jsii.member(jsii_name="azureInput")
    def azure_input(self) -> typing.Optional["BigqueryConnectionAzure"]:
        return typing.cast(typing.Optional["BigqueryConnectionAzure"], jsii.get(self, "azureInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudResourceInput")
    def cloud_resource_input(
        self,
    ) -> typing.Optional["BigqueryConnectionCloudResource"]:
        return typing.cast(typing.Optional["BigqueryConnectionCloudResource"], jsii.get(self, "cloudResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSpannerInput")
    def cloud_spanner_input(self) -> typing.Optional["BigqueryConnectionCloudSpanner"]:
        return typing.cast(typing.Optional["BigqueryConnectionCloudSpanner"], jsii.get(self, "cloudSpannerInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInput")
    def cloud_sql_input(self) -> typing.Optional["BigqueryConnectionCloudSql"]:
        return typing.cast(typing.Optional["BigqueryConnectionCloudSql"], jsii.get(self, "cloudSqlInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="friendlyNameInput")
    def friendly_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "friendlyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkInput")
    def spark_input(self) -> typing.Optional["BigqueryConnectionSpark"]:
        return typing.cast(typing.Optional["BigqueryConnectionSpark"], jsii.get(self, "sparkInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryConnectionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryConnectionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc1dd18b16cd7fc132be09a3a6e1ea72d75de86204ac58316ca8f8b955fd7ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7f5c0e2cae69025b662d21d59f9092a4acf6105d4a7e7ca8f4a587a69ca85c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="friendlyName")
    def friendly_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "friendlyName"))

    @friendly_name.setter
    def friendly_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b995a680c07834f113e522624e1a95117a66c8582c4a96eb11a8836cdb76995c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "friendlyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583bd5c3481341457aa5173a432d5694803eb946a66c17f34de9caa653ae8473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9036e6f581b11b6a224bab77543d3c2f6ffffef55bb4719e99e346caa1f4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5db4f2d1f0811bdb0a7ac6648cb9099d1618d9d00b1b730e1599251b28ad9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27c3386056359d56c5a046fb75a19e425e4301e58f8efc34638a0a0886ac53f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionAws",
    jsii_struct_bases=[],
    name_mapping={"access_role": "accessRole"},
)
class BigqueryConnectionAws:
    def __init__(
        self,
        *,
        access_role: typing.Union["BigqueryConnectionAwsAccessRole", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param access_role: access_role block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#access_role BigqueryConnection#access_role}
        '''
        if isinstance(access_role, dict):
            access_role = BigqueryConnectionAwsAccessRole(**access_role)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656e4eb650b5b8553ab86557f84644b43a3afd777dc8ffe17b63d5bf5219cca0)
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_role": access_role,
        }

    @builtins.property
    def access_role(self) -> "BigqueryConnectionAwsAccessRole":
        '''access_role block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#access_role BigqueryConnection#access_role}
        '''
        result = self._values.get("access_role")
        assert result is not None, "Required property 'access_role' is missing"
        return typing.cast("BigqueryConnectionAwsAccessRole", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionAws(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionAwsAccessRole",
    jsii_struct_bases=[],
    name_mapping={"iam_role_id": "iamRoleId"},
)
class BigqueryConnectionAwsAccessRole:
    def __init__(self, *, iam_role_id: builtins.str) -> None:
        '''
        :param iam_role_id: The user’s AWS IAM Role that trusts the Google-owned AWS IAM user Connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#iam_role_id BigqueryConnection#iam_role_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca50f36ba55f0f14083d1b991acda779d24b9b895a069f6ec02447aa9a80c44)
            check_type(argname="argument iam_role_id", value=iam_role_id, expected_type=type_hints["iam_role_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iam_role_id": iam_role_id,
        }

    @builtins.property
    def iam_role_id(self) -> builtins.str:
        '''The user’s AWS IAM Role that trusts the Google-owned AWS IAM user Connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#iam_role_id BigqueryConnection#iam_role_id}
        '''
        result = self._values.get("iam_role_id")
        assert result is not None, "Required property 'iam_role_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionAwsAccessRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryConnectionAwsAccessRoleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionAwsAccessRoleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90cca491cfaaf354af8f8ced17fddd45d82e55ebe3a6d1b7d37b327d3e3cbcb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="iamRoleIdInput")
    def iam_role_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="iamRoleId")
    def iam_role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamRoleId"))

    @iam_role_id.setter
    def iam_role_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e27a9f1b340bf7e78bf623dbd53cdf34023ee2333b249b7425a51ab06cdba73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryConnectionAwsAccessRole]:
        return typing.cast(typing.Optional[BigqueryConnectionAwsAccessRole], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryConnectionAwsAccessRole],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e52f4f182a46b16729ea0f36d1f5bc22bcb5122930e1987989e316fe392c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryConnectionAwsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionAwsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41903db56867d8be6082524ad20ff8a68cfed0247b0f6ee113ef99c22a764cf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessRole")
    def put_access_role(self, *, iam_role_id: builtins.str) -> None:
        '''
        :param iam_role_id: The user’s AWS IAM Role that trusts the Google-owned AWS IAM user Connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#iam_role_id BigqueryConnection#iam_role_id}
        '''
        value = BigqueryConnectionAwsAccessRole(iam_role_id=iam_role_id)

        return typing.cast(None, jsii.invoke(self, "putAccessRole", [value]))

    @builtins.property
    @jsii.member(jsii_name="accessRole")
    def access_role(self) -> BigqueryConnectionAwsAccessRoleOutputReference:
        return typing.cast(BigqueryConnectionAwsAccessRoleOutputReference, jsii.get(self, "accessRole"))

    @builtins.property
    @jsii.member(jsii_name="accessRoleInput")
    def access_role_input(self) -> typing.Optional[BigqueryConnectionAwsAccessRole]:
        return typing.cast(typing.Optional[BigqueryConnectionAwsAccessRole], jsii.get(self, "accessRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryConnectionAws]:
        return typing.cast(typing.Optional[BigqueryConnectionAws], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BigqueryConnectionAws]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feaf8ab1b3dc9e3163afbe334612bbb5048fdb456905b1857373e8dff49667ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionAzure",
    jsii_struct_bases=[],
    name_mapping={
        "customer_tenant_id": "customerTenantId",
        "federated_application_client_id": "federatedApplicationClientId",
    },
)
class BigqueryConnectionAzure:
    def __init__(
        self,
        *,
        customer_tenant_id: builtins.str,
        federated_application_client_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param customer_tenant_id: The id of customer's directory that host the data. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#customer_tenant_id BigqueryConnection#customer_tenant_id}
        :param federated_application_client_id: The Azure Application (client) ID where the federated credentials will be hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#federated_application_client_id BigqueryConnection#federated_application_client_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed92463a64d6ee4938fe682495b06306043ae337ea40011fa504adb61358bbb)
            check_type(argname="argument customer_tenant_id", value=customer_tenant_id, expected_type=type_hints["customer_tenant_id"])
            check_type(argname="argument federated_application_client_id", value=federated_application_client_id, expected_type=type_hints["federated_application_client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_tenant_id": customer_tenant_id,
        }
        if federated_application_client_id is not None:
            self._values["federated_application_client_id"] = federated_application_client_id

    @builtins.property
    def customer_tenant_id(self) -> builtins.str:
        '''The id of customer's directory that host the data.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#customer_tenant_id BigqueryConnection#customer_tenant_id}
        '''
        result = self._values.get("customer_tenant_id")
        assert result is not None, "Required property 'customer_tenant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def federated_application_client_id(self) -> typing.Optional[builtins.str]:
        '''The Azure Application (client) ID where the federated credentials will be hosted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#federated_application_client_id BigqueryConnection#federated_application_client_id}
        '''
        result = self._values.get("federated_application_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionAzure(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryConnectionAzureOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionAzureOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df5d70f5b09eecfd31c3d89a8f75a22c136773994b586b82aee04f230608c3ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFederatedApplicationClientId")
    def reset_federated_application_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFederatedApplicationClientId", []))

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="redirectUri")
    def redirect_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redirectUri"))

    @builtins.property
    @jsii.member(jsii_name="customerTenantIdInput")
    def customer_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="federatedApplicationClientIdInput")
    def federated_application_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "federatedApplicationClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customerTenantId")
    def customer_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerTenantId"))

    @customer_tenant_id.setter
    def customer_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c75e79370dfca3a1bfe01dc84e315ee6037962964b0cb431880af30949069d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="federatedApplicationClientId")
    def federated_application_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "federatedApplicationClientId"))

    @federated_application_client_id.setter
    def federated_application_client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__436244f195b8840e52bd6142bbb5f94bcc1d3149189bc8df495e019f56f09f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "federatedApplicationClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryConnectionAzure]:
        return typing.cast(typing.Optional[BigqueryConnectionAzure], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BigqueryConnectionAzure]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7fde7f0842b759648183d3e91aa21cd6ed4fe845241e0febaa49173cc47688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionCloudResource",
    jsii_struct_bases=[],
    name_mapping={},
)
class BigqueryConnectionCloudResource:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionCloudResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryConnectionCloudResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionCloudResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2de76faef8a0d29983de8ce0f4ba0ab8c8d66b3eef5f62e2d66ffd10a733bd53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="serviceAccountId")
    def service_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryConnectionCloudResource]:
        return typing.cast(typing.Optional[BigqueryConnectionCloudResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryConnectionCloudResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d00ca62925b67320bd471f345389fc75d68c1244076e64996ed71192b0cda4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionCloudSpanner",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "database_role": "databaseRole",
        "max_parallelism": "maxParallelism",
        "use_data_boost": "useDataBoost",
        "use_parallelism": "useParallelism",
        "use_serverless_analytics": "useServerlessAnalytics",
    },
)
class BigqueryConnectionCloudSpanner:
    def __init__(
        self,
        *,
        database: builtins.str,
        database_role: typing.Optional[builtins.str] = None,
        max_parallelism: typing.Optional[jsii.Number] = None,
        use_data_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_parallelism: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_serverless_analytics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param database: Cloud Spanner database in the form 'project/instance/database'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database BigqueryConnection#database}
        :param database_role: Cloud Spanner database role for fine-grained access control. The Cloud Spanner admin should have provisioned the database role with appropriate permissions, such as 'SELECT' and 'INSERT'. Other users should only use roles provided by their Cloud Spanner admins. The database role name must start with a letter, and can only contain letters, numbers, and underscores. For more details, see https://cloud.google.com/spanner/docs/fgac-about. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database_role BigqueryConnection#database_role}
        :param max_parallelism: Allows setting max parallelism per query when executing on Spanner independent compute resources. If unspecified, default values of parallelism are chosen that are dependent on the Cloud Spanner instance configuration. 'useParallelism' and 'useDataBoost' must be set when setting max parallelism. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#max_parallelism BigqueryConnection#max_parallelism}
        :param use_data_boost: If set, the request will be executed via Spanner independent compute resources. 'use_parallelism' must be set when using data boost. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_data_boost BigqueryConnection#use_data_boost}
        :param use_parallelism: If parallelism should be used when reading from Cloud Spanner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_parallelism BigqueryConnection#use_parallelism}
        :param use_serverless_analytics: If the serverless analytics service should be used to read data from Cloud Spanner. 'useParallelism' must be set when using serverless analytics. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_serverless_analytics BigqueryConnection#use_serverless_analytics}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a473ee01013972421466caa2dedbc31ac641b8f4f65ceda882bf70f0bf3bbadf)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument database_role", value=database_role, expected_type=type_hints["database_role"])
            check_type(argname="argument max_parallelism", value=max_parallelism, expected_type=type_hints["max_parallelism"])
            check_type(argname="argument use_data_boost", value=use_data_boost, expected_type=type_hints["use_data_boost"])
            check_type(argname="argument use_parallelism", value=use_parallelism, expected_type=type_hints["use_parallelism"])
            check_type(argname="argument use_serverless_analytics", value=use_serverless_analytics, expected_type=type_hints["use_serverless_analytics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
        }
        if database_role is not None:
            self._values["database_role"] = database_role
        if max_parallelism is not None:
            self._values["max_parallelism"] = max_parallelism
        if use_data_boost is not None:
            self._values["use_data_boost"] = use_data_boost
        if use_parallelism is not None:
            self._values["use_parallelism"] = use_parallelism
        if use_serverless_analytics is not None:
            self._values["use_serverless_analytics"] = use_serverless_analytics

    @builtins.property
    def database(self) -> builtins.str:
        '''Cloud Spanner database in the form 'project/instance/database'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database BigqueryConnection#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_role(self) -> typing.Optional[builtins.str]:
        '''Cloud Spanner database role for fine-grained access control.

        The Cloud Spanner admin should have provisioned the database role with appropriate permissions, such as 'SELECT' and 'INSERT'. Other users should only use roles provided by their Cloud Spanner admins. The database role name must start with a letter, and can only contain letters, numbers, and underscores. For more details, see https://cloud.google.com/spanner/docs/fgac-about.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database_role BigqueryConnection#database_role}
        '''
        result = self._values.get("database_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_parallelism(self) -> typing.Optional[jsii.Number]:
        '''Allows setting max parallelism per query when executing on Spanner independent compute resources.

        If unspecified, default values of parallelism are chosen that are dependent on the Cloud Spanner instance configuration. 'useParallelism' and 'useDataBoost' must be set when setting max parallelism.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#max_parallelism BigqueryConnection#max_parallelism}
        '''
        result = self._values.get("max_parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_data_boost(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, the request will be executed via Spanner independent compute resources.

        'use_parallelism' must be set when using data boost.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_data_boost BigqueryConnection#use_data_boost}
        '''
        result = self._values.get("use_data_boost")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_parallelism(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If parallelism should be used when reading from Cloud Spanner.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_parallelism BigqueryConnection#use_parallelism}
        '''
        result = self._values.get("use_parallelism")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_serverless_analytics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the serverless analytics service should be used to read data from Cloud Spanner.

        'useParallelism' must be set when using serverless analytics.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#use_serverless_analytics BigqueryConnection#use_serverless_analytics}
        '''
        result = self._values.get("use_serverless_analytics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionCloudSpanner(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryConnectionCloudSpannerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionCloudSpannerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb9edb09aa623ffcd27109be257b6f9fb20b1a1cce497f269fd270b8dae924a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatabaseRole")
    def reset_database_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseRole", []))

    @jsii.member(jsii_name="resetMaxParallelism")
    def reset_max_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxParallelism", []))

    @jsii.member(jsii_name="resetUseDataBoost")
    def reset_use_data_boost(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseDataBoost", []))

    @jsii.member(jsii_name="resetUseParallelism")
    def reset_use_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseParallelism", []))

    @jsii.member(jsii_name="resetUseServerlessAnalytics")
    def reset_use_serverless_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseServerlessAnalytics", []))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseRoleInput")
    def database_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="maxParallelismInput")
    def max_parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxParallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="useDataBoostInput")
    def use_data_boost_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useDataBoostInput"))

    @builtins.property
    @jsii.member(jsii_name="useParallelismInput")
    def use_parallelism_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useParallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="useServerlessAnalyticsInput")
    def use_serverless_analytics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useServerlessAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a5088d8afe87fc68c21357bf05dc40ad4e970e83206a2c5fca8671bad5b474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseRole")
    def database_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseRole"))

    @database_role.setter
    def database_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbf9911e6f04d02493deb0c192ba9ca537201a9c32518aec34be80af5941411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxParallelism")
    def max_parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxParallelism"))

    @max_parallelism.setter
    def max_parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2cd2aa9a9b709d3081778ba906e07617b60c779cbc05a99f6111fed62b1865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxParallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDataBoost")
    def use_data_boost(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useDataBoost"))

    @use_data_boost.setter
    def use_data_boost(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af1ffe83a04925cbb4f1c058e60a3abb0842a5f73eeaff6b604c701b2f676e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDataBoost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useParallelism")
    def use_parallelism(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useParallelism"))

    @use_parallelism.setter
    def use_parallelism(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efb6b4c903a3e20b504e3bdad23fd684b0d68a3d19ef96a1f6415a0b8d8bdfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useParallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useServerlessAnalytics")
    def use_serverless_analytics(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useServerlessAnalytics"))

    @use_serverless_analytics.setter
    def use_serverless_analytics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073ca51e0df7b3a2b7471ac24345f25b3845656e0a83144c21931edff1ab00fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useServerlessAnalytics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryConnectionCloudSpanner]:
        return typing.cast(typing.Optional[BigqueryConnectionCloudSpanner], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryConnectionCloudSpanner],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af43c0dac3d0abe34cbdfeef96110cc6b87ce0716ee48bbab14e2b160da58655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionCloudSql",
    jsii_struct_bases=[],
    name_mapping={
        "credential": "credential",
        "database": "database",
        "instance_id": "instanceId",
        "type": "type",
    },
)
class BigqueryConnectionCloudSql:
    def __init__(
        self,
        *,
        credential: typing.Union["BigqueryConnectionCloudSqlCredential", typing.Dict[builtins.str, typing.Any]],
        database: builtins.str,
        instance_id: builtins.str,
        type: builtins.str,
    ) -> None:
        '''
        :param credential: credential block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#credential BigqueryConnection#credential}
        :param database: Database name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database BigqueryConnection#database}
        :param instance_id: Cloud SQL instance ID in the form project:location:instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#instance_id BigqueryConnection#instance_id}
        :param type: Type of the Cloud SQL database. Possible values: ["DATABASE_TYPE_UNSPECIFIED", "POSTGRES", "MYSQL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#type BigqueryConnection#type}
        '''
        if isinstance(credential, dict):
            credential = BigqueryConnectionCloudSqlCredential(**credential)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e98b3dce4f34468759826a5c99e017296f561e9ac2d8f1e221368489d1ed27a)
            check_type(argname="argument credential", value=credential, expected_type=type_hints["credential"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credential": credential,
            "database": database,
            "instance_id": instance_id,
            "type": type,
        }

    @builtins.property
    def credential(self) -> "BigqueryConnectionCloudSqlCredential":
        '''credential block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#credential BigqueryConnection#credential}
        '''
        result = self._values.get("credential")
        assert result is not None, "Required property 'credential' is missing"
        return typing.cast("BigqueryConnectionCloudSqlCredential", result)

    @builtins.property
    def database(self) -> builtins.str:
        '''Database name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#database BigqueryConnection#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''Cloud SQL instance ID in the form project:location:instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#instance_id BigqueryConnection#instance_id}
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of the Cloud SQL database. Possible values: ["DATABASE_TYPE_UNSPECIFIED", "POSTGRES", "MYSQL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#type BigqueryConnection#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionCloudSql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionCloudSqlCredential",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class BigqueryConnectionCloudSqlCredential:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Password for database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#password BigqueryConnection#password}
        :param username: Username for database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#username BigqueryConnection#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e784851f1be13b5788cb9446f25609e95efa4c2bc476bb437ea791ef6ea24b5b)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Password for database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#password BigqueryConnection#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#username BigqueryConnection#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionCloudSqlCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryConnectionCloudSqlCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionCloudSqlCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd08f1573f15adc474c3f917b3c52ca67f644d13c4875017711b3969481743e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1955ab3223628245616cc1fa3466c75a8b5d271f13880522ebfc41d1e9f622ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67488bb5d14159e030158424ff5f63730eae715c096c9616f134666138cd762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryConnectionCloudSqlCredential]:
        return typing.cast(typing.Optional[BigqueryConnectionCloudSqlCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryConnectionCloudSqlCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6bc5074560bed52bdb24b2ff38c10fb6f4bddc16922ba7c82a105167764fce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryConnectionCloudSqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionCloudSqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d36e2ff1f267a0e686f408df81bb21bb046946ab38ee223aa0061614f256b105)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredential")
    def put_credential(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Password for database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#password BigqueryConnection#password}
        :param username: Username for database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#username BigqueryConnection#username}
        '''
        value = BigqueryConnectionCloudSqlCredential(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putCredential", [value]))

    @builtins.property
    @jsii.member(jsii_name="credential")
    def credential(self) -> BigqueryConnectionCloudSqlCredentialOutputReference:
        return typing.cast(BigqueryConnectionCloudSqlCredentialOutputReference, jsii.get(self, "credential"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountId")
    def service_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountId"))

    @builtins.property
    @jsii.member(jsii_name="credentialInput")
    def credential_input(self) -> typing.Optional[BigqueryConnectionCloudSqlCredential]:
        return typing.cast(typing.Optional[BigqueryConnectionCloudSqlCredential], jsii.get(self, "credentialInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c0655fa69a570895b650b666ea1f0a94203859a6726c8aecc0a2bf289bda415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d795c61766795eb793bd58fdf4c0d8216f989e7fbffef824be2f3859b21dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606764daf3bafe1ebd4293250c0c395710b8a989b80d54394b1df955638f2445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryConnectionCloudSql]:
        return typing.cast(typing.Optional[BigqueryConnectionCloudSql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryConnectionCloudSql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689599d4386b141d8df444225326653ffa1bffe849b5d06a173ae44d8a99e614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "aws": "aws",
        "azure": "azure",
        "cloud_resource": "cloudResource",
        "cloud_spanner": "cloudSpanner",
        "cloud_sql": "cloudSql",
        "connection_id": "connectionId",
        "description": "description",
        "friendly_name": "friendlyName",
        "id": "id",
        "kms_key_name": "kmsKeyName",
        "location": "location",
        "project": "project",
        "spark": "spark",
        "timeouts": "timeouts",
    },
)
class BigqueryConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        aws: typing.Optional[typing.Union[BigqueryConnectionAws, typing.Dict[builtins.str, typing.Any]]] = None,
        azure: typing.Optional[typing.Union[BigqueryConnectionAzure, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_resource: typing.Optional[typing.Union[BigqueryConnectionCloudResource, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_spanner: typing.Optional[typing.Union[BigqueryConnectionCloudSpanner, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_sql: typing.Optional[typing.Union[BigqueryConnectionCloudSql, typing.Dict[builtins.str, typing.Any]]] = None,
        connection_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        friendly_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        spark: typing.Optional[typing.Union["BigqueryConnectionSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigqueryConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#aws BigqueryConnection#aws}
        :param azure: azure block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#azure BigqueryConnection#azure}
        :param cloud_resource: cloud_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_resource BigqueryConnection#cloud_resource}
        :param cloud_spanner: cloud_spanner block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_spanner BigqueryConnection#cloud_spanner}
        :param cloud_sql: cloud_sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_sql BigqueryConnection#cloud_sql}
        :param connection_id: Optional connection id that should be assigned to the created connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#connection_id BigqueryConnection#connection_id}
        :param description: A descriptive description for the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#description BigqueryConnection#description}
        :param friendly_name: A descriptive name for the connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#friendly_name BigqueryConnection#friendly_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#id BigqueryConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: Optional. The Cloud KMS key that is used for encryption. Example: projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#kms_key_name BigqueryConnection#kms_key_name}
        :param location: The geographic location where the connection should reside. Cloud SQL instance must be in the same location as the connection with following exceptions: Cloud SQL us-central1 maps to BigQuery US, Cloud SQL europe-west1 maps to BigQuery EU. Examples: US, EU, asia-northeast1, us-central1, europe-west1. Spanner Connections same as spanner region AWS allowed regions are aws-us-east-1 Azure allowed regions are azure-eastus2 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#location BigqueryConnection#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#project BigqueryConnection#project}.
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#spark BigqueryConnection#spark}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#timeouts BigqueryConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws, dict):
            aws = BigqueryConnectionAws(**aws)
        if isinstance(azure, dict):
            azure = BigqueryConnectionAzure(**azure)
        if isinstance(cloud_resource, dict):
            cloud_resource = BigqueryConnectionCloudResource(**cloud_resource)
        if isinstance(cloud_spanner, dict):
            cloud_spanner = BigqueryConnectionCloudSpanner(**cloud_spanner)
        if isinstance(cloud_sql, dict):
            cloud_sql = BigqueryConnectionCloudSql(**cloud_sql)
        if isinstance(spark, dict):
            spark = BigqueryConnectionSpark(**spark)
        if isinstance(timeouts, dict):
            timeouts = BigqueryConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed1f366444797fb6a14be346129526f7d1bf78b7ee39f2ee28052d1090e516c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument aws", value=aws, expected_type=type_hints["aws"])
            check_type(argname="argument azure", value=azure, expected_type=type_hints["azure"])
            check_type(argname="argument cloud_resource", value=cloud_resource, expected_type=type_hints["cloud_resource"])
            check_type(argname="argument cloud_spanner", value=cloud_spanner, expected_type=type_hints["cloud_spanner"])
            check_type(argname="argument cloud_sql", value=cloud_sql, expected_type=type_hints["cloud_sql"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument friendly_name", value=friendly_name, expected_type=type_hints["friendly_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument spark", value=spark, expected_type=type_hints["spark"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if aws is not None:
            self._values["aws"] = aws
        if azure is not None:
            self._values["azure"] = azure
        if cloud_resource is not None:
            self._values["cloud_resource"] = cloud_resource
        if cloud_spanner is not None:
            self._values["cloud_spanner"] = cloud_spanner
        if cloud_sql is not None:
            self._values["cloud_sql"] = cloud_sql
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if description is not None:
            self._values["description"] = description
        if friendly_name is not None:
            self._values["friendly_name"] = friendly_name
        if id is not None:
            self._values["id"] = id
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if spark is not None:
            self._values["spark"] = spark
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
    def aws(self) -> typing.Optional[BigqueryConnectionAws]:
        '''aws block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#aws BigqueryConnection#aws}
        '''
        result = self._values.get("aws")
        return typing.cast(typing.Optional[BigqueryConnectionAws], result)

    @builtins.property
    def azure(self) -> typing.Optional[BigqueryConnectionAzure]:
        '''azure block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#azure BigqueryConnection#azure}
        '''
        result = self._values.get("azure")
        return typing.cast(typing.Optional[BigqueryConnectionAzure], result)

    @builtins.property
    def cloud_resource(self) -> typing.Optional[BigqueryConnectionCloudResource]:
        '''cloud_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_resource BigqueryConnection#cloud_resource}
        '''
        result = self._values.get("cloud_resource")
        return typing.cast(typing.Optional[BigqueryConnectionCloudResource], result)

    @builtins.property
    def cloud_spanner(self) -> typing.Optional[BigqueryConnectionCloudSpanner]:
        '''cloud_spanner block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_spanner BigqueryConnection#cloud_spanner}
        '''
        result = self._values.get("cloud_spanner")
        return typing.cast(typing.Optional[BigqueryConnectionCloudSpanner], result)

    @builtins.property
    def cloud_sql(self) -> typing.Optional[BigqueryConnectionCloudSql]:
        '''cloud_sql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#cloud_sql BigqueryConnection#cloud_sql}
        '''
        result = self._values.get("cloud_sql")
        return typing.cast(typing.Optional[BigqueryConnectionCloudSql], result)

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''Optional connection id that should be assigned to the created connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#connection_id BigqueryConnection#connection_id}
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A descriptive description for the connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#description BigqueryConnection#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def friendly_name(self) -> typing.Optional[builtins.str]:
        '''A descriptive name for the connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#friendly_name BigqueryConnection#friendly_name}
        '''
        result = self._values.get("friendly_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#id BigqueryConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Optional. The Cloud KMS key that is used for encryption.

        Example: projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#kms_key_name BigqueryConnection#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The geographic location where the connection should reside.

        Cloud SQL instance must be in the same location as the connection
        with following exceptions: Cloud SQL us-central1 maps to BigQuery US, Cloud SQL europe-west1 maps to BigQuery EU.
        Examples: US, EU, asia-northeast1, us-central1, europe-west1.
        Spanner Connections same as spanner region
        AWS allowed regions are aws-us-east-1
        Azure allowed regions are azure-eastus2

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#location BigqueryConnection#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#project BigqueryConnection#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark(self) -> typing.Optional["BigqueryConnectionSpark"]:
        '''spark block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#spark BigqueryConnection#spark}
        '''
        result = self._values.get("spark")
        return typing.cast(typing.Optional["BigqueryConnectionSpark"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#timeouts BigqueryConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionSpark",
    jsii_struct_bases=[],
    name_mapping={
        "metastore_service_config": "metastoreServiceConfig",
        "spark_history_server_config": "sparkHistoryServerConfig",
    },
)
class BigqueryConnectionSpark:
    def __init__(
        self,
        *,
        metastore_service_config: typing.Optional[typing.Union["BigqueryConnectionSparkMetastoreServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_history_server_config: typing.Optional[typing.Union["BigqueryConnectionSparkSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service_config: metastore_service_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#metastore_service_config BigqueryConnection#metastore_service_config}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#spark_history_server_config BigqueryConnection#spark_history_server_config}
        '''
        if isinstance(metastore_service_config, dict):
            metastore_service_config = BigqueryConnectionSparkMetastoreServiceConfig(**metastore_service_config)
        if isinstance(spark_history_server_config, dict):
            spark_history_server_config = BigqueryConnectionSparkSparkHistoryServerConfig(**spark_history_server_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d455d158f797090ace2e81f1d409636a7fd002dae6a32c6d33de041fdaa0c774)
            check_type(argname="argument metastore_service_config", value=metastore_service_config, expected_type=type_hints["metastore_service_config"])
            check_type(argname="argument spark_history_server_config", value=spark_history_server_config, expected_type=type_hints["spark_history_server_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metastore_service_config is not None:
            self._values["metastore_service_config"] = metastore_service_config
        if spark_history_server_config is not None:
            self._values["spark_history_server_config"] = spark_history_server_config

    @builtins.property
    def metastore_service_config(
        self,
    ) -> typing.Optional["BigqueryConnectionSparkMetastoreServiceConfig"]:
        '''metastore_service_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#metastore_service_config BigqueryConnection#metastore_service_config}
        '''
        result = self._values.get("metastore_service_config")
        return typing.cast(typing.Optional["BigqueryConnectionSparkMetastoreServiceConfig"], result)

    @builtins.property
    def spark_history_server_config(
        self,
    ) -> typing.Optional["BigqueryConnectionSparkSparkHistoryServerConfig"]:
        '''spark_history_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#spark_history_server_config BigqueryConnection#spark_history_server_config}
        '''
        result = self._values.get("spark_history_server_config")
        return typing.cast(typing.Optional["BigqueryConnectionSparkSparkHistoryServerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionSpark(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionSparkMetastoreServiceConfig",
    jsii_struct_bases=[],
    name_mapping={"metastore_service": "metastoreService"},
)
class BigqueryConnectionSparkMetastoreServiceConfig:
    def __init__(
        self,
        *,
        metastore_service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service in the form of projects/[projectId]/locations/[region]/services/[serviceId]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#metastore_service BigqueryConnection#metastore_service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3c6d9d2b24f2a47fe4ade46f8812eeecedef7f390595b26aa65a31a9c1cbf8)
            check_type(argname="argument metastore_service", value=metastore_service, expected_type=type_hints["metastore_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metastore_service is not None:
            self._values["metastore_service"] = metastore_service

    @builtins.property
    def metastore_service(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Metastore service in the form of projects/[projectId]/locations/[region]/services/[serviceId].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#metastore_service BigqueryConnection#metastore_service}
        '''
        result = self._values.get("metastore_service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionSparkMetastoreServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryConnectionSparkMetastoreServiceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionSparkMetastoreServiceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed02d1c9848e9cdb7445b3616f2b2b3b88344297c562949b7f3e5e80c0f7462)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetastoreService")
    def reset_metastore_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreService", []))

    @builtins.property
    @jsii.member(jsii_name="metastoreServiceInput")
    def metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreService")
    def metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metastoreService"))

    @metastore_service.setter
    def metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6732175b07bb9bb4c64fc2451cbd3d8eeb817b7c211b3e87bd6ecd88bffd54db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metastoreService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryConnectionSparkMetastoreServiceConfig]:
        return typing.cast(typing.Optional[BigqueryConnectionSparkMetastoreServiceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryConnectionSparkMetastoreServiceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c2d291880514ee4bbb7f07b277d0d3371dd9705da64efe86d02ed12df1e047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryConnectionSparkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionSparkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e86af97eac16bc11c16671c42e4b8d918381f661a49cd57b5329bb25890138d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetastoreServiceConfig")
    def put_metastore_service_config(
        self,
        *,
        metastore_service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service in the form of projects/[projectId]/locations/[region]/services/[serviceId]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#metastore_service BigqueryConnection#metastore_service}
        '''
        value = BigqueryConnectionSparkMetastoreServiceConfig(
            metastore_service=metastore_service
        )

        return typing.cast(None, jsii.invoke(self, "putMetastoreServiceConfig", [value]))

    @jsii.member(jsii_name="putSparkHistoryServerConfig")
    def put_spark_history_server_config(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the connection if the form of projects/[projectId]/regions/[region]/clusters/[cluster_name]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#dataproc_cluster BigqueryConnection#dataproc_cluster}
        '''
        value = BigqueryConnectionSparkSparkHistoryServerConfig(
            dataproc_cluster=dataproc_cluster
        )

        return typing.cast(None, jsii.invoke(self, "putSparkHistoryServerConfig", [value]))

    @jsii.member(jsii_name="resetMetastoreServiceConfig")
    def reset_metastore_service_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreServiceConfig", []))

    @jsii.member(jsii_name="resetSparkHistoryServerConfig")
    def reset_spark_history_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkHistoryServerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="metastoreServiceConfig")
    def metastore_service_config(
        self,
    ) -> BigqueryConnectionSparkMetastoreServiceConfigOutputReference:
        return typing.cast(BigqueryConnectionSparkMetastoreServiceConfigOutputReference, jsii.get(self, "metastoreServiceConfig"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountId")
    def service_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccountId"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfig")
    def spark_history_server_config(
        self,
    ) -> "BigqueryConnectionSparkSparkHistoryServerConfigOutputReference":
        return typing.cast("BigqueryConnectionSparkSparkHistoryServerConfigOutputReference", jsii.get(self, "sparkHistoryServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreServiceConfigInput")
    def metastore_service_config_input(
        self,
    ) -> typing.Optional[BigqueryConnectionSparkMetastoreServiceConfig]:
        return typing.cast(typing.Optional[BigqueryConnectionSparkMetastoreServiceConfig], jsii.get(self, "metastoreServiceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfigInput")
    def spark_history_server_config_input(
        self,
    ) -> typing.Optional["BigqueryConnectionSparkSparkHistoryServerConfig"]:
        return typing.cast(typing.Optional["BigqueryConnectionSparkSparkHistoryServerConfig"], jsii.get(self, "sparkHistoryServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryConnectionSpark]:
        return typing.cast(typing.Optional[BigqueryConnectionSpark], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BigqueryConnectionSpark]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f6cfe467bff0525569378c8e9d6937c2947fb57d753176395162b7b64e83b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionSparkSparkHistoryServerConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_cluster": "dataprocCluster"},
)
class BigqueryConnectionSparkSparkHistoryServerConfig:
    def __init__(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the connection if the form of projects/[projectId]/regions/[region]/clusters/[cluster_name]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#dataproc_cluster BigqueryConnection#dataproc_cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc09f1865048c41a4a5407aee64d8c7f0892f5ff3eec965259db9d8fd14d1b1)
            check_type(argname="argument dataproc_cluster", value=dataproc_cluster, expected_type=type_hints["dataproc_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_cluster is not None:
            self._values["dataproc_cluster"] = dataproc_cluster

    @builtins.property
    def dataproc_cluster(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Cluster to act as a Spark History Server for the connection if the form of projects/[projectId]/regions/[region]/clusters/[cluster_name].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#dataproc_cluster BigqueryConnection#dataproc_cluster}
        '''
        result = self._values.get("dataproc_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionSparkSparkHistoryServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryConnectionSparkSparkHistoryServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionSparkSparkHistoryServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b6dca0095adb9af88cfe1f0b2b3bbb2e2d94304453ebfc890e5e8f2272a2bc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataprocCluster")
    def reset_dataproc_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocCluster", []))

    @builtins.property
    @jsii.member(jsii_name="dataprocClusterInput")
    def dataproc_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocCluster")
    def dataproc_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocCluster"))

    @dataproc_cluster.setter
    def dataproc_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340d121e59f90b51f0c52c0679d178d752c7c908eaf1e436cd1a03b869ee276e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[BigqueryConnectionSparkSparkHistoryServerConfig]:
        return typing.cast(typing.Optional[BigqueryConnectionSparkSparkHistoryServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryConnectionSparkSparkHistoryServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb92ac4a2e1afcf6aa9fc684e4ea287d309e7b2086d493b7ca11b66f092eb88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#create BigqueryConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#delete BigqueryConnection#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#update BigqueryConnection#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ffb45006839be3319e1f470fb146f902067bc06d2473700502ae10267159fb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#create BigqueryConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#delete BigqueryConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_connection#update BigqueryConnection#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryConnection.BigqueryConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbd39cb92c50d65efd9be9c7675b54f22b91a904032a61db768ab56a248bed79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d734b84e3a589dae872343857b57e2bea3b9a2d1299fc3ce489575ed5e7e077a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecf670acf51aa98d53a2fad14d75dde654ef2093d7f6b5627c988f86e7ac015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ad6f2ca114326b25bae8375c5af731149ba80324c9ccfd10bf809f65def48e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryConnectionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryConnectionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryConnectionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db90398ed6832a700d7aa9306ead1b1d78ce29437f8ae5bfa51b65ed7a291c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigqueryConnection",
    "BigqueryConnectionAws",
    "BigqueryConnectionAwsAccessRole",
    "BigqueryConnectionAwsAccessRoleOutputReference",
    "BigqueryConnectionAwsOutputReference",
    "BigqueryConnectionAzure",
    "BigqueryConnectionAzureOutputReference",
    "BigqueryConnectionCloudResource",
    "BigqueryConnectionCloudResourceOutputReference",
    "BigqueryConnectionCloudSpanner",
    "BigqueryConnectionCloudSpannerOutputReference",
    "BigqueryConnectionCloudSql",
    "BigqueryConnectionCloudSqlCredential",
    "BigqueryConnectionCloudSqlCredentialOutputReference",
    "BigqueryConnectionCloudSqlOutputReference",
    "BigqueryConnectionConfig",
    "BigqueryConnectionSpark",
    "BigqueryConnectionSparkMetastoreServiceConfig",
    "BigqueryConnectionSparkMetastoreServiceConfigOutputReference",
    "BigqueryConnectionSparkOutputReference",
    "BigqueryConnectionSparkSparkHistoryServerConfig",
    "BigqueryConnectionSparkSparkHistoryServerConfigOutputReference",
    "BigqueryConnectionTimeouts",
    "BigqueryConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0f2d61e5ca7e04dd63633186fd07c52ef22872e0d18462677aed81403df9898d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    aws: typing.Optional[typing.Union[BigqueryConnectionAws, typing.Dict[builtins.str, typing.Any]]] = None,
    azure: typing.Optional[typing.Union[BigqueryConnectionAzure, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_resource: typing.Optional[typing.Union[BigqueryConnectionCloudResource, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_spanner: typing.Optional[typing.Union[BigqueryConnectionCloudSpanner, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_sql: typing.Optional[typing.Union[BigqueryConnectionCloudSql, typing.Dict[builtins.str, typing.Any]]] = None,
    connection_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spark: typing.Optional[typing.Union[BigqueryConnectionSpark, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigqueryConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2dcda366192c9dedcfe270d7e06afed548741da8b2ff11f1e76cba81cab0ce8b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc1dd18b16cd7fc132be09a3a6e1ea72d75de86204ac58316ca8f8b955fd7ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7f5c0e2cae69025b662d21d59f9092a4acf6105d4a7e7ca8f4a587a69ca85c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b995a680c07834f113e522624e1a95117a66c8582c4a96eb11a8836cdb76995c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583bd5c3481341457aa5173a432d5694803eb946a66c17f34de9caa653ae8473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9036e6f581b11b6a224bab77543d3c2f6ffffef55bb4719e99e346caa1f4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5db4f2d1f0811bdb0a7ac6648cb9099d1618d9d00b1b730e1599251b28ad9ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27c3386056359d56c5a046fb75a19e425e4301e58f8efc34638a0a0886ac53f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656e4eb650b5b8553ab86557f84644b43a3afd777dc8ffe17b63d5bf5219cca0(
    *,
    access_role: typing.Union[BigqueryConnectionAwsAccessRole, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca50f36ba55f0f14083d1b991acda779d24b9b895a069f6ec02447aa9a80c44(
    *,
    iam_role_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90cca491cfaaf354af8f8ced17fddd45d82e55ebe3a6d1b7d37b327d3e3cbcb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e27a9f1b340bf7e78bf623dbd53cdf34023ee2333b249b7425a51ab06cdba73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e52f4f182a46b16729ea0f36d1f5bc22bcb5122930e1987989e316fe392c9f(
    value: typing.Optional[BigqueryConnectionAwsAccessRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41903db56867d8be6082524ad20ff8a68cfed0247b0f6ee113ef99c22a764cf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feaf8ab1b3dc9e3163afbe334612bbb5048fdb456905b1857373e8dff49667ff(
    value: typing.Optional[BigqueryConnectionAws],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed92463a64d6ee4938fe682495b06306043ae337ea40011fa504adb61358bbb(
    *,
    customer_tenant_id: builtins.str,
    federated_application_client_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5d70f5b09eecfd31c3d89a8f75a22c136773994b586b82aee04f230608c3ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c75e79370dfca3a1bfe01dc84e315ee6037962964b0cb431880af30949069d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436244f195b8840e52bd6142bbb5f94bcc1d3149189bc8df495e019f56f09f96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7fde7f0842b759648183d3e91aa21cd6ed4fe845241e0febaa49173cc47688(
    value: typing.Optional[BigqueryConnectionAzure],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de76faef8a0d29983de8ce0f4ba0ab8c8d66b3eef5f62e2d66ffd10a733bd53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d00ca62925b67320bd471f345389fc75d68c1244076e64996ed71192b0cda4e(
    value: typing.Optional[BigqueryConnectionCloudResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a473ee01013972421466caa2dedbc31ac641b8f4f65ceda882bf70f0bf3bbadf(
    *,
    database: builtins.str,
    database_role: typing.Optional[builtins.str] = None,
    max_parallelism: typing.Optional[jsii.Number] = None,
    use_data_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_parallelism: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_serverless_analytics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9edb09aa623ffcd27109be257b6f9fb20b1a1cce497f269fd270b8dae924a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a5088d8afe87fc68c21357bf05dc40ad4e970e83206a2c5fca8671bad5b474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbf9911e6f04d02493deb0c192ba9ca537201a9c32518aec34be80af5941411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2cd2aa9a9b709d3081778ba906e07617b60c779cbc05a99f6111fed62b1865(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1ffe83a04925cbb4f1c058e60a3abb0842a5f73eeaff6b604c701b2f676e86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efb6b4c903a3e20b504e3bdad23fd684b0d68a3d19ef96a1f6415a0b8d8bdfd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073ca51e0df7b3a2b7471ac24345f25b3845656e0a83144c21931edff1ab00fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af43c0dac3d0abe34cbdfeef96110cc6b87ce0716ee48bbab14e2b160da58655(
    value: typing.Optional[BigqueryConnectionCloudSpanner],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e98b3dce4f34468759826a5c99e017296f561e9ac2d8f1e221368489d1ed27a(
    *,
    credential: typing.Union[BigqueryConnectionCloudSqlCredential, typing.Dict[builtins.str, typing.Any]],
    database: builtins.str,
    instance_id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e784851f1be13b5788cb9446f25609e95efa4c2bc476bb437ea791ef6ea24b5b(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd08f1573f15adc474c3f917b3c52ca67f644d13c4875017711b3969481743e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1955ab3223628245616cc1fa3466c75a8b5d271f13880522ebfc41d1e9f622ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67488bb5d14159e030158424ff5f63730eae715c096c9616f134666138cd762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6bc5074560bed52bdb24b2ff38c10fb6f4bddc16922ba7c82a105167764fce(
    value: typing.Optional[BigqueryConnectionCloudSqlCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36e2ff1f267a0e686f408df81bb21bb046946ab38ee223aa0061614f256b105(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0655fa69a570895b650b666ea1f0a94203859a6726c8aecc0a2bf289bda415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d795c61766795eb793bd58fdf4c0d8216f989e7fbffef824be2f3859b21dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606764daf3bafe1ebd4293250c0c395710b8a989b80d54394b1df955638f2445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689599d4386b141d8df444225326653ffa1bffe849b5d06a173ae44d8a99e614(
    value: typing.Optional[BigqueryConnectionCloudSql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed1f366444797fb6a14be346129526f7d1bf78b7ee39f2ee28052d1090e516c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aws: typing.Optional[typing.Union[BigqueryConnectionAws, typing.Dict[builtins.str, typing.Any]]] = None,
    azure: typing.Optional[typing.Union[BigqueryConnectionAzure, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_resource: typing.Optional[typing.Union[BigqueryConnectionCloudResource, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_spanner: typing.Optional[typing.Union[BigqueryConnectionCloudSpanner, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_sql: typing.Optional[typing.Union[BigqueryConnectionCloudSql, typing.Dict[builtins.str, typing.Any]]] = None,
    connection_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    friendly_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    spark: typing.Optional[typing.Union[BigqueryConnectionSpark, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigqueryConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d455d158f797090ace2e81f1d409636a7fd002dae6a32c6d33de041fdaa0c774(
    *,
    metastore_service_config: typing.Optional[typing.Union[BigqueryConnectionSparkMetastoreServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_history_server_config: typing.Optional[typing.Union[BigqueryConnectionSparkSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3c6d9d2b24f2a47fe4ade46f8812eeecedef7f390595b26aa65a31a9c1cbf8(
    *,
    metastore_service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed02d1c9848e9cdb7445b3616f2b2b3b88344297c562949b7f3e5e80c0f7462(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6732175b07bb9bb4c64fc2451cbd3d8eeb817b7c211b3e87bd6ecd88bffd54db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c2d291880514ee4bbb7f07b277d0d3371dd9705da64efe86d02ed12df1e047(
    value: typing.Optional[BigqueryConnectionSparkMetastoreServiceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86af97eac16bc11c16671c42e4b8d918381f661a49cd57b5329bb25890138d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f6cfe467bff0525569378c8e9d6937c2947fb57d753176395162b7b64e83b8(
    value: typing.Optional[BigqueryConnectionSpark],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc09f1865048c41a4a5407aee64d8c7f0892f5ff3eec965259db9d8fd14d1b1(
    *,
    dataproc_cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6dca0095adb9af88cfe1f0b2b3bbb2e2d94304453ebfc890e5e8f2272a2bc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340d121e59f90b51f0c52c0679d178d752c7c908eaf1e436cd1a03b869ee276e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb92ac4a2e1afcf6aa9fc684e4ea287d309e7b2086d493b7ca11b66f092eb88d(
    value: typing.Optional[BigqueryConnectionSparkSparkHistoryServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ffb45006839be3319e1f470fb146f902067bc06d2473700502ae10267159fb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd39cb92c50d65efd9be9c7675b54f22b91a904032a61db768ab56a248bed79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d734b84e3a589dae872343857b57e2bea3b9a2d1299fc3ce489575ed5e7e077a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecf670acf51aa98d53a2fad14d75dde654ef2093d7f6b5627c988f86e7ac015(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ad6f2ca114326b25bae8375c5af731149ba80324c9ccfd10bf809f65def48e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db90398ed6832a700d7aa9306ead1b1d78ce29437f8ae5bfa51b65ed7a291c10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryConnectionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
