r'''
# `aws_quicksight_data_source`

Refer to the Terraform Registry for docs: [`aws_quicksight_data_source`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source).
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


class QuicksightDataSource(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSource",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source aws_quicksight_data_source}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_source_id: builtins.str,
        name: builtins.str,
        parameters: typing.Union["QuicksightDataSourceParameters", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["QuicksightDataSourceCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSourcePermission", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssl_properties: typing.Optional[typing.Union["QuicksightDataSourceSslProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_connection_properties: typing.Optional[typing.Union["QuicksightDataSourceVpcConnectionProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source aws_quicksight_data_source} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_source_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#data_source_id QuicksightDataSource#data_source_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#name QuicksightDataSource#name}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#parameters QuicksightDataSource#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#type QuicksightDataSource#type}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aws_account_id QuicksightDataSource#aws_account_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#credentials QuicksightDataSource#credentials}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#id QuicksightDataSource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permission: permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#permission QuicksightDataSource#permission}
        :param ssl_properties: ssl_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#ssl_properties QuicksightDataSource#ssl_properties}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#tags QuicksightDataSource#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#tags_all QuicksightDataSource#tags_all}.
        :param vpc_connection_properties: vpc_connection_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#vpc_connection_properties QuicksightDataSource#vpc_connection_properties}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5fe7277a73407ec4dbd9499078245c5f6e63de15c139fd0a1611a48734ee96)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QuicksightDataSourceConfig(
            data_source_id=data_source_id,
            name=name,
            parameters=parameters,
            type=type,
            aws_account_id=aws_account_id,
            credentials=credentials,
            id=id,
            permission=permission,
            ssl_properties=ssl_properties,
            tags=tags,
            tags_all=tags_all,
            vpc_connection_properties=vpc_connection_properties,
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
        '''Generates CDKTF code for importing a QuicksightDataSource resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightDataSource to import.
        :param import_from_id: The id of the existing QuicksightDataSource that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightDataSource to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a250ae2b4458d6bb2bba18ff5ae123cd018fe88f30cb882c6f8be21b70b64fc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(
        self,
        *,
        copy_source_arn: typing.Optional[builtins.str] = None,
        credential_pair: typing.Optional[typing.Union["QuicksightDataSourceCredentialsCredentialPair", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param copy_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#copy_source_arn QuicksightDataSource#copy_source_arn}.
        :param credential_pair: credential_pair block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#credential_pair QuicksightDataSource#credential_pair}
        :param secret_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#secret_arn QuicksightDataSource#secret_arn}.
        '''
        value = QuicksightDataSourceCredentials(
            copy_source_arn=copy_source_arn,
            credential_pair=credential_pair,
            secret_arn=secret_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        amazon_elasticsearch: typing.Optional[typing.Union["QuicksightDataSourceParametersAmazonElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        athena: typing.Optional[typing.Union["QuicksightDataSourceParametersAthena", typing.Dict[builtins.str, typing.Any]]] = None,
        aurora: typing.Optional[typing.Union["QuicksightDataSourceParametersAurora", typing.Dict[builtins.str, typing.Any]]] = None,
        aurora_postgresql: typing.Optional[typing.Union["QuicksightDataSourceParametersAuroraPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_iot_analytics: typing.Optional[typing.Union["QuicksightDataSourceParametersAwsIotAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        databricks: typing.Optional[typing.Union["QuicksightDataSourceParametersDatabricks", typing.Dict[builtins.str, typing.Any]]] = None,
        jira: typing.Optional[typing.Union["QuicksightDataSourceParametersJira", typing.Dict[builtins.str, typing.Any]]] = None,
        maria_db: typing.Optional[typing.Union["QuicksightDataSourceParametersMariaDb", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql: typing.Optional[typing.Union["QuicksightDataSourceParametersMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle: typing.Optional[typing.Union["QuicksightDataSourceParametersOracle", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["QuicksightDataSourceParametersPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        presto: typing.Optional[typing.Union["QuicksightDataSourceParametersPresto", typing.Dict[builtins.str, typing.Any]]] = None,
        rds: typing.Optional[typing.Union["QuicksightDataSourceParametersRds", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["QuicksightDataSourceParametersRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["QuicksightDataSourceParametersS3", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["QuicksightDataSourceParametersServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["QuicksightDataSourceParametersSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        spark: typing.Optional[typing.Union["QuicksightDataSourceParametersSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_server: typing.Optional[typing.Union["QuicksightDataSourceParametersSqlServer", typing.Dict[builtins.str, typing.Any]]] = None,
        teradata: typing.Optional[typing.Union["QuicksightDataSourceParametersTeradata", typing.Dict[builtins.str, typing.Any]]] = None,
        twitter: typing.Optional[typing.Union["QuicksightDataSourceParametersTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amazon_elasticsearch: amazon_elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#amazon_elasticsearch QuicksightDataSource#amazon_elasticsearch}
        :param athena: athena block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#athena QuicksightDataSource#athena}
        :param aurora: aurora block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aurora QuicksightDataSource#aurora}
        :param aurora_postgresql: aurora_postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aurora_postgresql QuicksightDataSource#aurora_postgresql}
        :param aws_iot_analytics: aws_iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aws_iot_analytics QuicksightDataSource#aws_iot_analytics}
        :param databricks: databricks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#databricks QuicksightDataSource#databricks}
        :param jira: jira block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#jira QuicksightDataSource#jira}
        :param maria_db: maria_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#maria_db QuicksightDataSource#maria_db}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#mysql QuicksightDataSource#mysql}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#oracle QuicksightDataSource#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#postgresql QuicksightDataSource#postgresql}
        :param presto: presto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#presto QuicksightDataSource#presto}
        :param rds: rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#rds QuicksightDataSource#rds}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#redshift QuicksightDataSource#redshift}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#s3 QuicksightDataSource#s3}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#service_now QuicksightDataSource#service_now}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#snowflake QuicksightDataSource#snowflake}
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#spark QuicksightDataSource#spark}
        :param sql_server: sql_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#sql_server QuicksightDataSource#sql_server}
        :param teradata: teradata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#teradata QuicksightDataSource#teradata}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#twitter QuicksightDataSource#twitter}
        '''
        value = QuicksightDataSourceParameters(
            amazon_elasticsearch=amazon_elasticsearch,
            athena=athena,
            aurora=aurora,
            aurora_postgresql=aurora_postgresql,
            aws_iot_analytics=aws_iot_analytics,
            databricks=databricks,
            jira=jira,
            maria_db=maria_db,
            mysql=mysql,
            oracle=oracle,
            postgresql=postgresql,
            presto=presto,
            rds=rds,
            redshift=redshift,
            s3=s3,
            service_now=service_now,
            snowflake=snowflake,
            spark=spark,
            sql_server=sql_server,
            teradata=teradata,
            twitter=twitter,
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="putPermission")
    def put_permission(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSourcePermission", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38905942f7349aaa86ea38c3a9a28721ce04f9ff70a41b287205595773c369b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPermission", [value]))

    @jsii.member(jsii_name="putSslProperties")
    def put_ssl_properties(
        self,
        *,
        disable_ssl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disable_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#disable_ssl QuicksightDataSource#disable_ssl}.
        '''
        value = QuicksightDataSourceSslProperties(disable_ssl=disable_ssl)

        return typing.cast(None, jsii.invoke(self, "putSslProperties", [value]))

    @jsii.member(jsii_name="putVpcConnectionProperties")
    def put_vpc_connection_properties(
        self,
        *,
        vpc_connection_arn: builtins.str,
    ) -> None:
        '''
        :param vpc_connection_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#vpc_connection_arn QuicksightDataSource#vpc_connection_arn}.
        '''
        value = QuicksightDataSourceVpcConnectionProperties(
            vpc_connection_arn=vpc_connection_arn
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConnectionProperties", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPermission")
    def reset_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermission", []))

    @jsii.member(jsii_name="resetSslProperties")
    def reset_ssl_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslProperties", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetVpcConnectionProperties")
    def reset_vpc_connection_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcConnectionProperties", []))

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
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> "QuicksightDataSourceCredentialsOutputReference":
        return typing.cast("QuicksightDataSourceCredentialsOutputReference", jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "QuicksightDataSourceParametersOutputReference":
        return typing.cast("QuicksightDataSourceParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="permission")
    def permission(self) -> "QuicksightDataSourcePermissionList":
        return typing.cast("QuicksightDataSourcePermissionList", jsii.get(self, "permission"))

    @builtins.property
    @jsii.member(jsii_name="sslProperties")
    def ssl_properties(self) -> "QuicksightDataSourceSslPropertiesOutputReference":
        return typing.cast("QuicksightDataSourceSslPropertiesOutputReference", jsii.get(self, "sslProperties"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectionProperties")
    def vpc_connection_properties(
        self,
    ) -> "QuicksightDataSourceVpcConnectionPropertiesOutputReference":
        return typing.cast("QuicksightDataSourceVpcConnectionPropertiesOutputReference", jsii.get(self, "vpcConnectionProperties"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional["QuicksightDataSourceCredentials"]:
        return typing.cast(typing.Optional["QuicksightDataSourceCredentials"], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceIdInput")
    def data_source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional["QuicksightDataSourceParameters"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParameters"], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionInput")
    def permission_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSourcePermission"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSourcePermission"]]], jsii.get(self, "permissionInput"))

    @builtins.property
    @jsii.member(jsii_name="sslPropertiesInput")
    def ssl_properties_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceSslProperties"]:
        return typing.cast(typing.Optional["QuicksightDataSourceSslProperties"], jsii.get(self, "sslPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectionPropertiesInput")
    def vpc_connection_properties_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceVpcConnectionProperties"]:
        return typing.cast(typing.Optional["QuicksightDataSourceVpcConnectionProperties"], jsii.get(self, "vpcConnectionPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231d92da58bd56366dd194cfa88989be83bdd0318e729da2e21f86b02dbe7f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @data_source_id.setter
    def data_source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f9c5eb1a8fc19ff2c57348ba5ff59d770ef53f2337eb4244755694bff77795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bced0e57186cbe6824020d222e4da487a616d4a16686d385416c081bea835af4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3872557784bf849a99e80bc6e72f0ca23f36b6a7c2ab58623e812bd02baf218f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e27d42a148696eb245c3f02f4f817c7381d334e66c2c59e1d6c28af1118cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58c659e15cae5331df474dcc864160e04065bdc0e00231f295624700fb5b2a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87de4bc32e45a07b0dd1896f863b53baf28737d1316aaa7e621889cb2b4f3dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_source_id": "dataSourceId",
        "name": "name",
        "parameters": "parameters",
        "type": "type",
        "aws_account_id": "awsAccountId",
        "credentials": "credentials",
        "id": "id",
        "permission": "permission",
        "ssl_properties": "sslProperties",
        "tags": "tags",
        "tags_all": "tagsAll",
        "vpc_connection_properties": "vpcConnectionProperties",
    },
)
class QuicksightDataSourceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_source_id: builtins.str,
        name: builtins.str,
        parameters: typing.Union["QuicksightDataSourceParameters", typing.Dict[builtins.str, typing.Any]],
        type: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[typing.Union["QuicksightDataSourceCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSourcePermission", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssl_properties: typing.Optional[typing.Union["QuicksightDataSourceSslProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_connection_properties: typing.Optional[typing.Union["QuicksightDataSourceVpcConnectionProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_source_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#data_source_id QuicksightDataSource#data_source_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#name QuicksightDataSource#name}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#parameters QuicksightDataSource#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#type QuicksightDataSource#type}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aws_account_id QuicksightDataSource#aws_account_id}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#credentials QuicksightDataSource#credentials}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#id QuicksightDataSource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permission: permission block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#permission QuicksightDataSource#permission}
        :param ssl_properties: ssl_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#ssl_properties QuicksightDataSource#ssl_properties}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#tags QuicksightDataSource#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#tags_all QuicksightDataSource#tags_all}.
        :param vpc_connection_properties: vpc_connection_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#vpc_connection_properties QuicksightDataSource#vpc_connection_properties}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(parameters, dict):
            parameters = QuicksightDataSourceParameters(**parameters)
        if isinstance(credentials, dict):
            credentials = QuicksightDataSourceCredentials(**credentials)
        if isinstance(ssl_properties, dict):
            ssl_properties = QuicksightDataSourceSslProperties(**ssl_properties)
        if isinstance(vpc_connection_properties, dict):
            vpc_connection_properties = QuicksightDataSourceVpcConnectionProperties(**vpc_connection_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ace59ef2c12ecb11cbb9da48181caa9765125bf00a740d57655355c04cc9d509)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_source_id", value=data_source_id, expected_type=type_hints["data_source_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            check_type(argname="argument ssl_properties", value=ssl_properties, expected_type=type_hints["ssl_properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument vpc_connection_properties", value=vpc_connection_properties, expected_type=type_hints["vpc_connection_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_id": data_source_id,
            "name": name,
            "parameters": parameters,
            "type": type,
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
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if credentials is not None:
            self._values["credentials"] = credentials
        if id is not None:
            self._values["id"] = id
        if permission is not None:
            self._values["permission"] = permission
        if ssl_properties is not None:
            self._values["ssl_properties"] = ssl_properties
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if vpc_connection_properties is not None:
            self._values["vpc_connection_properties"] = vpc_connection_properties

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
    def data_source_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#data_source_id QuicksightDataSource#data_source_id}.'''
        result = self._values.get("data_source_id")
        assert result is not None, "Required property 'data_source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#name QuicksightDataSource#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> "QuicksightDataSourceParameters":
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#parameters QuicksightDataSource#parameters}
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast("QuicksightDataSourceParameters", result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#type QuicksightDataSource#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aws_account_id QuicksightDataSource#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional["QuicksightDataSourceCredentials"]:
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#credentials QuicksightDataSource#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["QuicksightDataSourceCredentials"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#id QuicksightDataSource#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSourcePermission"]]]:
        '''permission block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#permission QuicksightDataSource#permission}
        '''
        result = self._values.get("permission")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSourcePermission"]]], result)

    @builtins.property
    def ssl_properties(self) -> typing.Optional["QuicksightDataSourceSslProperties"]:
        '''ssl_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#ssl_properties QuicksightDataSource#ssl_properties}
        '''
        result = self._values.get("ssl_properties")
        return typing.cast(typing.Optional["QuicksightDataSourceSslProperties"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#tags QuicksightDataSource#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#tags_all QuicksightDataSource#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc_connection_properties(
        self,
    ) -> typing.Optional["QuicksightDataSourceVpcConnectionProperties"]:
        '''vpc_connection_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#vpc_connection_properties QuicksightDataSource#vpc_connection_properties}
        '''
        result = self._values.get("vpc_connection_properties")
        return typing.cast(typing.Optional["QuicksightDataSourceVpcConnectionProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "copy_source_arn": "copySourceArn",
        "credential_pair": "credentialPair",
        "secret_arn": "secretArn",
    },
)
class QuicksightDataSourceCredentials:
    def __init__(
        self,
        *,
        copy_source_arn: typing.Optional[builtins.str] = None,
        credential_pair: typing.Optional[typing.Union["QuicksightDataSourceCredentialsCredentialPair", typing.Dict[builtins.str, typing.Any]]] = None,
        secret_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param copy_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#copy_source_arn QuicksightDataSource#copy_source_arn}.
        :param credential_pair: credential_pair block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#credential_pair QuicksightDataSource#credential_pair}
        :param secret_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#secret_arn QuicksightDataSource#secret_arn}.
        '''
        if isinstance(credential_pair, dict):
            credential_pair = QuicksightDataSourceCredentialsCredentialPair(**credential_pair)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddcd7d18096e1a4599e7ade139321878a5e23b509830dd4e7bb5d700449b4eb9)
            check_type(argname="argument copy_source_arn", value=copy_source_arn, expected_type=type_hints["copy_source_arn"])
            check_type(argname="argument credential_pair", value=credential_pair, expected_type=type_hints["credential_pair"])
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if copy_source_arn is not None:
            self._values["copy_source_arn"] = copy_source_arn
        if credential_pair is not None:
            self._values["credential_pair"] = credential_pair
        if secret_arn is not None:
            self._values["secret_arn"] = secret_arn

    @builtins.property
    def copy_source_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#copy_source_arn QuicksightDataSource#copy_source_arn}.'''
        result = self._values.get("copy_source_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credential_pair(
        self,
    ) -> typing.Optional["QuicksightDataSourceCredentialsCredentialPair"]:
        '''credential_pair block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#credential_pair QuicksightDataSource#credential_pair}
        '''
        result = self._values.get("credential_pair")
        return typing.cast(typing.Optional["QuicksightDataSourceCredentialsCredentialPair"], result)

    @builtins.property
    def secret_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#secret_arn QuicksightDataSource#secret_arn}.'''
        result = self._values.get("secret_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceCredentialsCredentialPair",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class QuicksightDataSourceCredentialsCredentialPair:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#password QuicksightDataSource#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#username QuicksightDataSource#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1757a11c4883c42ef32dca254fca25071c4cc9a74465542166c5ccaf4bf97fa9)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#password QuicksightDataSource#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#username QuicksightDataSource#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceCredentialsCredentialPair(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceCredentialsCredentialPairOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceCredentialsCredentialPairOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57a2fcdb914042f805321a524ee401c226cd8ce05ef9be17fca4208cfc5414bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f75de464e7b3a93bc3173a5a394adfe4591fdc4348cdd1d6e2e81686c1ea9919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cfaeee11927cdd778498e732bac6262e6e89c58d078adf69deb3f5163d2670b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceCredentialsCredentialPair]:
        return typing.cast(typing.Optional[QuicksightDataSourceCredentialsCredentialPair], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceCredentialsCredentialPair],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13ddd504b8e0beb5f32b2395e7e73e3fadc935a3f7d48a8e797754ffcbd8582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSourceCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1baa26c34d191fc922ffc9dafb175f1e9988e45702c4fd0efcbb10efd796b445)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentialPair")
    def put_credential_pair(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#password QuicksightDataSource#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#username QuicksightDataSource#username}.
        '''
        value = QuicksightDataSourceCredentialsCredentialPair(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putCredentialPair", [value]))

    @jsii.member(jsii_name="resetCopySourceArn")
    def reset_copy_source_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopySourceArn", []))

    @jsii.member(jsii_name="resetCredentialPair")
    def reset_credential_pair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialPair", []))

    @jsii.member(jsii_name="resetSecretArn")
    def reset_secret_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretArn", []))

    @builtins.property
    @jsii.member(jsii_name="credentialPair")
    def credential_pair(
        self,
    ) -> QuicksightDataSourceCredentialsCredentialPairOutputReference:
        return typing.cast(QuicksightDataSourceCredentialsCredentialPairOutputReference, jsii.get(self, "credentialPair"))

    @builtins.property
    @jsii.member(jsii_name="copySourceArnInput")
    def copy_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copySourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialPairInput")
    def credential_pair_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceCredentialsCredentialPair]:
        return typing.cast(typing.Optional[QuicksightDataSourceCredentialsCredentialPair], jsii.get(self, "credentialPairInput"))

    @builtins.property
    @jsii.member(jsii_name="secretArnInput")
    def secret_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretArnInput"))

    @builtins.property
    @jsii.member(jsii_name="copySourceArn")
    def copy_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copySourceArn"))

    @copy_source_arn.setter
    def copy_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb80b38ec63cc32f9dfa35afd75eb393407aacfdba478c19eff871949b5e96c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copySourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @secret_arn.setter
    def secret_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55947bc272cc821aa6c5140dbbcb8c9a233d9cf85a179c218ad340b319717591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceCredentials]:
        return typing.cast(typing.Optional[QuicksightDataSourceCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174cb92add5ec4cc9b05fd12dc78b3bd42b2f12fba09b6a47f3f7cce3da13cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParameters",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_elasticsearch": "amazonElasticsearch",
        "athena": "athena",
        "aurora": "aurora",
        "aurora_postgresql": "auroraPostgresql",
        "aws_iot_analytics": "awsIotAnalytics",
        "databricks": "databricks",
        "jira": "jira",
        "maria_db": "mariaDb",
        "mysql": "mysql",
        "oracle": "oracle",
        "postgresql": "postgresql",
        "presto": "presto",
        "rds": "rds",
        "redshift": "redshift",
        "s3": "s3",
        "service_now": "serviceNow",
        "snowflake": "snowflake",
        "spark": "spark",
        "sql_server": "sqlServer",
        "teradata": "teradata",
        "twitter": "twitter",
    },
)
class QuicksightDataSourceParameters:
    def __init__(
        self,
        *,
        amazon_elasticsearch: typing.Optional[typing.Union["QuicksightDataSourceParametersAmazonElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        athena: typing.Optional[typing.Union["QuicksightDataSourceParametersAthena", typing.Dict[builtins.str, typing.Any]]] = None,
        aurora: typing.Optional[typing.Union["QuicksightDataSourceParametersAurora", typing.Dict[builtins.str, typing.Any]]] = None,
        aurora_postgresql: typing.Optional[typing.Union["QuicksightDataSourceParametersAuroraPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_iot_analytics: typing.Optional[typing.Union["QuicksightDataSourceParametersAwsIotAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        databricks: typing.Optional[typing.Union["QuicksightDataSourceParametersDatabricks", typing.Dict[builtins.str, typing.Any]]] = None,
        jira: typing.Optional[typing.Union["QuicksightDataSourceParametersJira", typing.Dict[builtins.str, typing.Any]]] = None,
        maria_db: typing.Optional[typing.Union["QuicksightDataSourceParametersMariaDb", typing.Dict[builtins.str, typing.Any]]] = None,
        mysql: typing.Optional[typing.Union["QuicksightDataSourceParametersMysql", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle: typing.Optional[typing.Union["QuicksightDataSourceParametersOracle", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql: typing.Optional[typing.Union["QuicksightDataSourceParametersPostgresql", typing.Dict[builtins.str, typing.Any]]] = None,
        presto: typing.Optional[typing.Union["QuicksightDataSourceParametersPresto", typing.Dict[builtins.str, typing.Any]]] = None,
        rds: typing.Optional[typing.Union["QuicksightDataSourceParametersRds", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["QuicksightDataSourceParametersRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["QuicksightDataSourceParametersS3", typing.Dict[builtins.str, typing.Any]]] = None,
        service_now: typing.Optional[typing.Union["QuicksightDataSourceParametersServiceNow", typing.Dict[builtins.str, typing.Any]]] = None,
        snowflake: typing.Optional[typing.Union["QuicksightDataSourceParametersSnowflake", typing.Dict[builtins.str, typing.Any]]] = None,
        spark: typing.Optional[typing.Union["QuicksightDataSourceParametersSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        sql_server: typing.Optional[typing.Union["QuicksightDataSourceParametersSqlServer", typing.Dict[builtins.str, typing.Any]]] = None,
        teradata: typing.Optional[typing.Union["QuicksightDataSourceParametersTeradata", typing.Dict[builtins.str, typing.Any]]] = None,
        twitter: typing.Optional[typing.Union["QuicksightDataSourceParametersTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param amazon_elasticsearch: amazon_elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#amazon_elasticsearch QuicksightDataSource#amazon_elasticsearch}
        :param athena: athena block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#athena QuicksightDataSource#athena}
        :param aurora: aurora block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aurora QuicksightDataSource#aurora}
        :param aurora_postgresql: aurora_postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aurora_postgresql QuicksightDataSource#aurora_postgresql}
        :param aws_iot_analytics: aws_iot_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aws_iot_analytics QuicksightDataSource#aws_iot_analytics}
        :param databricks: databricks block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#databricks QuicksightDataSource#databricks}
        :param jira: jira block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#jira QuicksightDataSource#jira}
        :param maria_db: maria_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#maria_db QuicksightDataSource#maria_db}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#mysql QuicksightDataSource#mysql}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#oracle QuicksightDataSource#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#postgresql QuicksightDataSource#postgresql}
        :param presto: presto block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#presto QuicksightDataSource#presto}
        :param rds: rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#rds QuicksightDataSource#rds}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#redshift QuicksightDataSource#redshift}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#s3 QuicksightDataSource#s3}
        :param service_now: service_now block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#service_now QuicksightDataSource#service_now}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#snowflake QuicksightDataSource#snowflake}
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#spark QuicksightDataSource#spark}
        :param sql_server: sql_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#sql_server QuicksightDataSource#sql_server}
        :param teradata: teradata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#teradata QuicksightDataSource#teradata}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#twitter QuicksightDataSource#twitter}
        '''
        if isinstance(amazon_elasticsearch, dict):
            amazon_elasticsearch = QuicksightDataSourceParametersAmazonElasticsearch(**amazon_elasticsearch)
        if isinstance(athena, dict):
            athena = QuicksightDataSourceParametersAthena(**athena)
        if isinstance(aurora, dict):
            aurora = QuicksightDataSourceParametersAurora(**aurora)
        if isinstance(aurora_postgresql, dict):
            aurora_postgresql = QuicksightDataSourceParametersAuroraPostgresql(**aurora_postgresql)
        if isinstance(aws_iot_analytics, dict):
            aws_iot_analytics = QuicksightDataSourceParametersAwsIotAnalytics(**aws_iot_analytics)
        if isinstance(databricks, dict):
            databricks = QuicksightDataSourceParametersDatabricks(**databricks)
        if isinstance(jira, dict):
            jira = QuicksightDataSourceParametersJira(**jira)
        if isinstance(maria_db, dict):
            maria_db = QuicksightDataSourceParametersMariaDb(**maria_db)
        if isinstance(mysql, dict):
            mysql = QuicksightDataSourceParametersMysql(**mysql)
        if isinstance(oracle, dict):
            oracle = QuicksightDataSourceParametersOracle(**oracle)
        if isinstance(postgresql, dict):
            postgresql = QuicksightDataSourceParametersPostgresql(**postgresql)
        if isinstance(presto, dict):
            presto = QuicksightDataSourceParametersPresto(**presto)
        if isinstance(rds, dict):
            rds = QuicksightDataSourceParametersRds(**rds)
        if isinstance(redshift, dict):
            redshift = QuicksightDataSourceParametersRedshift(**redshift)
        if isinstance(s3, dict):
            s3 = QuicksightDataSourceParametersS3(**s3)
        if isinstance(service_now, dict):
            service_now = QuicksightDataSourceParametersServiceNow(**service_now)
        if isinstance(snowflake, dict):
            snowflake = QuicksightDataSourceParametersSnowflake(**snowflake)
        if isinstance(spark, dict):
            spark = QuicksightDataSourceParametersSpark(**spark)
        if isinstance(sql_server, dict):
            sql_server = QuicksightDataSourceParametersSqlServer(**sql_server)
        if isinstance(teradata, dict):
            teradata = QuicksightDataSourceParametersTeradata(**teradata)
        if isinstance(twitter, dict):
            twitter = QuicksightDataSourceParametersTwitter(**twitter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431a5f681cfa628f670dcb629107ec26712fa153ee5e0558429a6a6db49745ef)
            check_type(argname="argument amazon_elasticsearch", value=amazon_elasticsearch, expected_type=type_hints["amazon_elasticsearch"])
            check_type(argname="argument athena", value=athena, expected_type=type_hints["athena"])
            check_type(argname="argument aurora", value=aurora, expected_type=type_hints["aurora"])
            check_type(argname="argument aurora_postgresql", value=aurora_postgresql, expected_type=type_hints["aurora_postgresql"])
            check_type(argname="argument aws_iot_analytics", value=aws_iot_analytics, expected_type=type_hints["aws_iot_analytics"])
            check_type(argname="argument databricks", value=databricks, expected_type=type_hints["databricks"])
            check_type(argname="argument jira", value=jira, expected_type=type_hints["jira"])
            check_type(argname="argument maria_db", value=maria_db, expected_type=type_hints["maria_db"])
            check_type(argname="argument mysql", value=mysql, expected_type=type_hints["mysql"])
            check_type(argname="argument oracle", value=oracle, expected_type=type_hints["oracle"])
            check_type(argname="argument postgresql", value=postgresql, expected_type=type_hints["postgresql"])
            check_type(argname="argument presto", value=presto, expected_type=type_hints["presto"])
            check_type(argname="argument rds", value=rds, expected_type=type_hints["rds"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument service_now", value=service_now, expected_type=type_hints["service_now"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
            check_type(argname="argument spark", value=spark, expected_type=type_hints["spark"])
            check_type(argname="argument sql_server", value=sql_server, expected_type=type_hints["sql_server"])
            check_type(argname="argument teradata", value=teradata, expected_type=type_hints["teradata"])
            check_type(argname="argument twitter", value=twitter, expected_type=type_hints["twitter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amazon_elasticsearch is not None:
            self._values["amazon_elasticsearch"] = amazon_elasticsearch
        if athena is not None:
            self._values["athena"] = athena
        if aurora is not None:
            self._values["aurora"] = aurora
        if aurora_postgresql is not None:
            self._values["aurora_postgresql"] = aurora_postgresql
        if aws_iot_analytics is not None:
            self._values["aws_iot_analytics"] = aws_iot_analytics
        if databricks is not None:
            self._values["databricks"] = databricks
        if jira is not None:
            self._values["jira"] = jira
        if maria_db is not None:
            self._values["maria_db"] = maria_db
        if mysql is not None:
            self._values["mysql"] = mysql
        if oracle is not None:
            self._values["oracle"] = oracle
        if postgresql is not None:
            self._values["postgresql"] = postgresql
        if presto is not None:
            self._values["presto"] = presto
        if rds is not None:
            self._values["rds"] = rds
        if redshift is not None:
            self._values["redshift"] = redshift
        if s3 is not None:
            self._values["s3"] = s3
        if service_now is not None:
            self._values["service_now"] = service_now
        if snowflake is not None:
            self._values["snowflake"] = snowflake
        if spark is not None:
            self._values["spark"] = spark
        if sql_server is not None:
            self._values["sql_server"] = sql_server
        if teradata is not None:
            self._values["teradata"] = teradata
        if twitter is not None:
            self._values["twitter"] = twitter

    @builtins.property
    def amazon_elasticsearch(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersAmazonElasticsearch"]:
        '''amazon_elasticsearch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#amazon_elasticsearch QuicksightDataSource#amazon_elasticsearch}
        '''
        result = self._values.get("amazon_elasticsearch")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAmazonElasticsearch"], result)

    @builtins.property
    def athena(self) -> typing.Optional["QuicksightDataSourceParametersAthena"]:
        '''athena block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#athena QuicksightDataSource#athena}
        '''
        result = self._values.get("athena")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAthena"], result)

    @builtins.property
    def aurora(self) -> typing.Optional["QuicksightDataSourceParametersAurora"]:
        '''aurora block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aurora QuicksightDataSource#aurora}
        '''
        result = self._values.get("aurora")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAurora"], result)

    @builtins.property
    def aurora_postgresql(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersAuroraPostgresql"]:
        '''aurora_postgresql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aurora_postgresql QuicksightDataSource#aurora_postgresql}
        '''
        result = self._values.get("aurora_postgresql")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAuroraPostgresql"], result)

    @builtins.property
    def aws_iot_analytics(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersAwsIotAnalytics"]:
        '''aws_iot_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#aws_iot_analytics QuicksightDataSource#aws_iot_analytics}
        '''
        result = self._values.get("aws_iot_analytics")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersAwsIotAnalytics"], result)

    @builtins.property
    def databricks(self) -> typing.Optional["QuicksightDataSourceParametersDatabricks"]:
        '''databricks block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#databricks QuicksightDataSource#databricks}
        '''
        result = self._values.get("databricks")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersDatabricks"], result)

    @builtins.property
    def jira(self) -> typing.Optional["QuicksightDataSourceParametersJira"]:
        '''jira block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#jira QuicksightDataSource#jira}
        '''
        result = self._values.get("jira")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersJira"], result)

    @builtins.property
    def maria_db(self) -> typing.Optional["QuicksightDataSourceParametersMariaDb"]:
        '''maria_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#maria_db QuicksightDataSource#maria_db}
        '''
        result = self._values.get("maria_db")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersMariaDb"], result)

    @builtins.property
    def mysql(self) -> typing.Optional["QuicksightDataSourceParametersMysql"]:
        '''mysql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#mysql QuicksightDataSource#mysql}
        '''
        result = self._values.get("mysql")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersMysql"], result)

    @builtins.property
    def oracle(self) -> typing.Optional["QuicksightDataSourceParametersOracle"]:
        '''oracle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#oracle QuicksightDataSource#oracle}
        '''
        result = self._values.get("oracle")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersOracle"], result)

    @builtins.property
    def postgresql(self) -> typing.Optional["QuicksightDataSourceParametersPostgresql"]:
        '''postgresql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#postgresql QuicksightDataSource#postgresql}
        '''
        result = self._values.get("postgresql")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersPostgresql"], result)

    @builtins.property
    def presto(self) -> typing.Optional["QuicksightDataSourceParametersPresto"]:
        '''presto block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#presto QuicksightDataSource#presto}
        '''
        result = self._values.get("presto")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersPresto"], result)

    @builtins.property
    def rds(self) -> typing.Optional["QuicksightDataSourceParametersRds"]:
        '''rds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#rds QuicksightDataSource#rds}
        '''
        result = self._values.get("rds")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersRds"], result)

    @builtins.property
    def redshift(self) -> typing.Optional["QuicksightDataSourceParametersRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#redshift QuicksightDataSource#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersRedshift"], result)

    @builtins.property
    def s3(self) -> typing.Optional["QuicksightDataSourceParametersS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#s3 QuicksightDataSource#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersS3"], result)

    @builtins.property
    def service_now(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersServiceNow"]:
        '''service_now block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#service_now QuicksightDataSource#service_now}
        '''
        result = self._values.get("service_now")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersServiceNow"], result)

    @builtins.property
    def snowflake(self) -> typing.Optional["QuicksightDataSourceParametersSnowflake"]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#snowflake QuicksightDataSource#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSnowflake"], result)

    @builtins.property
    def spark(self) -> typing.Optional["QuicksightDataSourceParametersSpark"]:
        '''spark block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#spark QuicksightDataSource#spark}
        '''
        result = self._values.get("spark")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSpark"], result)

    @builtins.property
    def sql_server(self) -> typing.Optional["QuicksightDataSourceParametersSqlServer"]:
        '''sql_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#sql_server QuicksightDataSource#sql_server}
        '''
        result = self._values.get("sql_server")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSqlServer"], result)

    @builtins.property
    def teradata(self) -> typing.Optional["QuicksightDataSourceParametersTeradata"]:
        '''teradata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#teradata QuicksightDataSource#teradata}
        '''
        result = self._values.get("teradata")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersTeradata"], result)

    @builtins.property
    def twitter(self) -> typing.Optional["QuicksightDataSourceParametersTwitter"]:
        '''twitter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#twitter QuicksightDataSource#twitter}
        '''
        result = self._values.get("twitter")
        return typing.cast(typing.Optional["QuicksightDataSourceParametersTwitter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAmazonElasticsearch",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain"},
)
class QuicksightDataSourceParametersAmazonElasticsearch:
    def __init__(self, *, domain: builtins.str) -> None:
        '''
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#domain QuicksightDataSource#domain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__482dcbb621ac863d7c60c3318c6307ab17613ebd14f228c5313361616f257721)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
        }

    @builtins.property
    def domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#domain QuicksightDataSource#domain}.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAmazonElasticsearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAmazonElasticsearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAmazonElasticsearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc4a8589d8734a004a2274e52a8b87d751f4f33a9755ef3cf064740a136cc303)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c21d0baad9fb3f249cfce4ff04628b6d5665acded4098531f87a26990085c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bafaf1c2adb10d2d1f55e9fb8aa224959e390e5ed9e7e9a6b8b2c71131082d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAthena",
    jsii_struct_bases=[],
    name_mapping={"work_group": "workGroup"},
)
class QuicksightDataSourceParametersAthena:
    def __init__(self, *, work_group: typing.Optional[builtins.str] = None) -> None:
        '''
        :param work_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#work_group QuicksightDataSource#work_group}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331d741e9d006e66ec2cf88a16dd5b4fea4a9e02ce95b713af7f7acf22bd2b98)
            check_type(argname="argument work_group", value=work_group, expected_type=type_hints["work_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if work_group is not None:
            self._values["work_group"] = work_group

    @builtins.property
    def work_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#work_group QuicksightDataSource#work_group}.'''
        result = self._values.get("work_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAthena(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAthenaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAthenaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02ee1f182c9d8c10d6baaca231c2f02a9d321b598ef94f18530e5d6139b72753)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWorkGroup")
    def reset_work_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkGroup", []))

    @builtins.property
    @jsii.member(jsii_name="workGroupInput")
    def work_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="workGroup")
    def work_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workGroup"))

    @work_group.setter
    def work_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbd5377c68192b23e5d9358c1466c7a7d87d355ab7d0ade4e520dace2e7b1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersAthena]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAthena], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAthena],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6729c268f4468b7d86733b23d0dbad625ccd22fa5a182a0a8175245f446c282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAurora",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersAurora:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e9e20a0a9f58b039eb7242d392da6a7776dfb4f4a0d7a6869c4367e918b2fe1)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAurora(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAuroraOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAuroraOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__995bbf66536266f33b9b456f7795aa0544abfc4f43294c37e0c81aff073c7ffc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacfdbbce04f1e610471812c398ae8e94b818ee866ec40e06ed855867d09d20d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6571dc4770c283124fb1dc8d7dff7782ec0f8982680e38ac1b9349271fe0d6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5680dbb418255fde49eaacc83a164244ae79882d09540663e0d7fb292035925d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersAurora]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAurora], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAurora],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771935f1a94fdb8785137f73f588edcc75ceaa013a3f4bdcdcc1f7f23e052ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAuroraPostgresql",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersAuroraPostgresql:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b4b587098f8296e1e6250d67c8768247564d9cf7b1a8a9972ec6de3348395a)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAuroraPostgresql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAuroraPostgresqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAuroraPostgresqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__002a214383ab5df6201f05622f9abd6c10838a5590b33e19840a66e8b5be3e9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785a04a76c09624ecc88dc88654b172a02fd995fa4829619f48e4dfa70bf3358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdeb82226d28c5692c71863abaab0c0372288b7c555ca1a4b0bc7cc9a470bec6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1cd9bbbedffbd5fc89e78c086bcccecdabb1c83b8ea0bd9c463ce0c9fa9a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAuroraPostgresql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAuroraPostgresql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAuroraPostgresql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02366467e54f1452c9ec93fd910a9caac65b2d1c5f5c7b32c4847e8af8fb8b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAwsIotAnalytics",
    jsii_struct_bases=[],
    name_mapping={"data_set_name": "dataSetName"},
)
class QuicksightDataSourceParametersAwsIotAnalytics:
    def __init__(self, *, data_set_name: builtins.str) -> None:
        '''
        :param data_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#data_set_name QuicksightDataSource#data_set_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43255c026201428a863309e7b49ea5cba708cdd358af2df67c972fa44d33ffa1)
            check_type(argname="argument data_set_name", value=data_set_name, expected_type=type_hints["data_set_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_set_name": data_set_name,
        }

    @builtins.property
    def data_set_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#data_set_name QuicksightDataSource#data_set_name}.'''
        result = self._values.get("data_set_name")
        assert result is not None, "Required property 'data_set_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersAwsIotAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersAwsIotAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersAwsIotAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fd0d9e5d773169b95a88e490caff092e31a7aa7a015b829c063408709c1846f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dataSetNameInput")
    def data_set_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetName")
    def data_set_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetName"))

    @data_set_name.setter
    def data_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f024112483727b88847aeb59595ff35629b590ae140f1776402898100127ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26621f3f83b7ea34cac13a08471c14c9459f5a3ddd4c437d8f71e63f42a741cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersDatabricks",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "port": "port",
        "sql_endpoint_path": "sqlEndpointPath",
    },
)
class QuicksightDataSourceParametersDatabricks:
    def __init__(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        sql_endpoint_path: builtins.str,
    ) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        :param sql_endpoint_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#sql_endpoint_path QuicksightDataSource#sql_endpoint_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be59de086d21a97d98cc6bda4d78d2065b04d86e3ba343caa44a56e5f83a5e19)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument sql_endpoint_path", value=sql_endpoint_path, expected_type=type_hints["sql_endpoint_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "port": port,
            "sql_endpoint_path": sql_endpoint_path,
        }

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def sql_endpoint_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#sql_endpoint_path QuicksightDataSource#sql_endpoint_path}.'''
        result = self._values.get("sql_endpoint_path")
        assert result is not None, "Required property 'sql_endpoint_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersDatabricks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersDatabricksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersDatabricksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d066f6fc4f07269a43c9daf982eb55699d7f507d639091aa2625d26774479fdd)
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
    @jsii.member(jsii_name="sqlEndpointPathInput")
    def sql_endpoint_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlEndpointPathInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635a2188ebc9bbbdedea26d68a4a10951df0b70f4ee84963fb01fb2964c9bba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c66b099c5538b0fc8a14bda3db00c28b2cd26b23830f9fdf6becde2115395f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlEndpointPath")
    def sql_endpoint_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlEndpointPath"))

    @sql_endpoint_path.setter
    def sql_endpoint_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1c8c4f3b8e58a79e5c318bd4ebf77d042a133cc218c2a5fa6c7c97ed4f8d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlEndpointPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersDatabricks]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersDatabricks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersDatabricks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833c142ad2bf49978906a3223cd33183359b54f9f0816a50ec5ee63f45946adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersJira",
    jsii_struct_bases=[],
    name_mapping={"site_base_url": "siteBaseUrl"},
)
class QuicksightDataSourceParametersJira:
    def __init__(self, *, site_base_url: builtins.str) -> None:
        '''
        :param site_base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c22096c6bc2976622761062db6c5a248dfed94c1364ae3f77e7a820b05958be)
            check_type(argname="argument site_base_url", value=site_base_url, expected_type=type_hints["site_base_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_base_url": site_base_url,
        }

    @builtins.property
    def site_base_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.'''
        result = self._values.get("site_base_url")
        assert result is not None, "Required property 'site_base_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersJira(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersJiraOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersJiraOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15771f60d0f5f5e8d328ab7ae7b3689cdf1562f62c8f5496ac003b21cf2eecb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="siteBaseUrlInput")
    def site_base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteBaseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="siteBaseUrl")
    def site_base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "siteBaseUrl"))

    @site_base_url.setter
    def site_base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2625fc0e368821460b5c1cfb0450d39b01622af462d23f59b5bb43a5dbf0b6f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteBaseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersJira]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersJira], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersJira],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d77218fa3157e7e486c3d3af558aa8bad27fd4c8a034d1328ccb01b3c87a8d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersMariaDb",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersMariaDb:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adf049f2a33ff28a01c76065c46ac5e7ef9aa9ff26134ddf442ee4d0bf833c37)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersMariaDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersMariaDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersMariaDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7af7b878b2a12dfe28e6a5a77bc93b56cc90c58a9e9e4d33f90aa3f015ef18b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fdf2753c28e019dee5481f54f99e6735d368b6f1fd023b6084e3f80b072df5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d7db8d1f3ce34340c0f695031a3ab345b3a4e1b12256cf5dc995703c1b01ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb16b7f9e988f91f01bd4e1b9ae94ed5b58c2d83b3ecd316d0fa59ff72568ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersMariaDb]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersMariaDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersMariaDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff0faf3be2d88aff9c90f009aa4a32df7f23ae7b8d92539d002d70fd682ab42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersMysql",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersMysql:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0479c145f28b151552baf9a6f9c914f210c685f21e1ed3daffc456a23c4036cc)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersMysql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersMysqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersMysqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c96ed01670592ccae0c6b3cde25b9ea56f382353b19bacf63582a844a5b52268)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5f25f8d074f5ff6ea24998b7c512cb399df55c623c01a06471270d5cdc9054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944d8e6c289e2a430f5b822592a88c84acc82870d4623f0514865584bf4f24b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2593ad7886704eca498c16362a24d6e1809387e9b3e84f149cf69c21750e72a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersMysql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersMysql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersMysql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b833205f972a2590077d813b72d304a50fc85c034f1c76137ee2cc207d696b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersOracle",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersOracle:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7726c7b82c7a3af38b50c900715fd4f7e5f35188cf1c921b42628241122152b)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersOracle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersOracleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersOracleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdd12c6b6229b443350bc373899f3eab321d3c87e51e161aba764a29dd6ea5b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e4f4d695e8ce1ac9c6c1db2146ed9f61936a61430444b98306003328143e81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c686baeb62c00942002a5a8483f4b1d74b20c7164b00b065867e4334b1612ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a679398d7d4e310aa28425200b0a8761af462ec329dc569b54383789415da88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersOracle]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersOracle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersOracle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67693dedadf787f37348906df29a6ff8cdbf95eb4ad0529093ceed1b8a12913b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSourceParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0be8cd4e5ec4aef36f65e7d89468c4225ba80fac8fd35187274517ee52a56f51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAmazonElasticsearch")
    def put_amazon_elasticsearch(self, *, domain: builtins.str) -> None:
        '''
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#domain QuicksightDataSource#domain}.
        '''
        value = QuicksightDataSourceParametersAmazonElasticsearch(domain=domain)

        return typing.cast(None, jsii.invoke(self, "putAmazonElasticsearch", [value]))

    @jsii.member(jsii_name="putAthena")
    def put_athena(self, *, work_group: typing.Optional[builtins.str] = None) -> None:
        '''
        :param work_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#work_group QuicksightDataSource#work_group}.
        '''
        value = QuicksightDataSourceParametersAthena(work_group=work_group)

        return typing.cast(None, jsii.invoke(self, "putAthena", [value]))

    @jsii.member(jsii_name="putAurora")
    def put_aurora(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersAurora(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putAurora", [value]))

    @jsii.member(jsii_name="putAuroraPostgresql")
    def put_aurora_postgresql(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersAuroraPostgresql(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putAuroraPostgresql", [value]))

    @jsii.member(jsii_name="putAwsIotAnalytics")
    def put_aws_iot_analytics(self, *, data_set_name: builtins.str) -> None:
        '''
        :param data_set_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#data_set_name QuicksightDataSource#data_set_name}.
        '''
        value = QuicksightDataSourceParametersAwsIotAnalytics(
            data_set_name=data_set_name
        )

        return typing.cast(None, jsii.invoke(self, "putAwsIotAnalytics", [value]))

    @jsii.member(jsii_name="putDatabricks")
    def put_databricks(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        sql_endpoint_path: builtins.str,
    ) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        :param sql_endpoint_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#sql_endpoint_path QuicksightDataSource#sql_endpoint_path}.
        '''
        value = QuicksightDataSourceParametersDatabricks(
            host=host, port=port, sql_endpoint_path=sql_endpoint_path
        )

        return typing.cast(None, jsii.invoke(self, "putDatabricks", [value]))

    @jsii.member(jsii_name="putJira")
    def put_jira(self, *, site_base_url: builtins.str) -> None:
        '''
        :param site_base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.
        '''
        value = QuicksightDataSourceParametersJira(site_base_url=site_base_url)

        return typing.cast(None, jsii.invoke(self, "putJira", [value]))

    @jsii.member(jsii_name="putMariaDb")
    def put_maria_db(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersMariaDb(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putMariaDb", [value]))

    @jsii.member(jsii_name="putMysql")
    def put_mysql(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersMysql(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putMysql", [value]))

    @jsii.member(jsii_name="putOracle")
    def put_oracle(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersOracle(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putOracle", [value]))

    @jsii.member(jsii_name="putPostgresql")
    def put_postgresql(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersPostgresql(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresql", [value]))

    @jsii.member(jsii_name="putPresto")
    def put_presto(
        self,
        *,
        catalog: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#catalog QuicksightDataSource#catalog}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersPresto(
            catalog=catalog, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putPresto", [value]))

    @jsii.member(jsii_name="putRds")
    def put_rds(self, *, database: builtins.str, instance_id: builtins.str) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#instance_id QuicksightDataSource#instance_id}.
        '''
        value = QuicksightDataSourceParametersRds(
            database=database, instance_id=instance_id
        )

        return typing.cast(None, jsii.invoke(self, "putRds", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        *,
        database: builtins.str,
        cluster_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#cluster_id QuicksightDataSource#cluster_id}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersRedshift(
            database=database, cluster_id=cluster_id, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        manifest_file_location: typing.Union["QuicksightDataSourceParametersS3ManifestFileLocation", typing.Dict[builtins.str, typing.Any]],
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manifest_file_location: manifest_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#manifest_file_location QuicksightDataSource#manifest_file_location}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#role_arn QuicksightDataSource#role_arn}.
        '''
        value = QuicksightDataSourceParametersS3(
            manifest_file_location=manifest_file_location, role_arn=role_arn
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putServiceNow")
    def put_service_now(self, *, site_base_url: builtins.str) -> None:
        '''
        :param site_base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.
        '''
        value = QuicksightDataSourceParametersServiceNow(site_base_url=site_base_url)

        return typing.cast(None, jsii.invoke(self, "putServiceNow", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        warehouse: builtins.str,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#warehouse QuicksightDataSource#warehouse}.
        '''
        value = QuicksightDataSourceParametersSnowflake(
            database=database, host=host, warehouse=warehouse
        )

        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="putSpark")
    def put_spark(self, *, host: builtins.str, port: jsii.Number) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersSpark(host=host, port=port)

        return typing.cast(None, jsii.invoke(self, "putSpark", [value]))

    @jsii.member(jsii_name="putSqlServer")
    def put_sql_server(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersSqlServer(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putSqlServer", [value]))

    @jsii.member(jsii_name="putTeradata")
    def put_teradata(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        value = QuicksightDataSourceParametersTeradata(
            database=database, host=host, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putTeradata", [value]))

    @jsii.member(jsii_name="putTwitter")
    def put_twitter(self, *, max_rows: jsii.Number, query: builtins.str) -> None:
        '''
        :param max_rows: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#max_rows QuicksightDataSource#max_rows}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#query QuicksightDataSource#query}.
        '''
        value = QuicksightDataSourceParametersTwitter(max_rows=max_rows, query=query)

        return typing.cast(None, jsii.invoke(self, "putTwitter", [value]))

    @jsii.member(jsii_name="resetAmazonElasticsearch")
    def reset_amazon_elasticsearch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonElasticsearch", []))

    @jsii.member(jsii_name="resetAthena")
    def reset_athena(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAthena", []))

    @jsii.member(jsii_name="resetAurora")
    def reset_aurora(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAurora", []))

    @jsii.member(jsii_name="resetAuroraPostgresql")
    def reset_aurora_postgresql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuroraPostgresql", []))

    @jsii.member(jsii_name="resetAwsIotAnalytics")
    def reset_aws_iot_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsIotAnalytics", []))

    @jsii.member(jsii_name="resetDatabricks")
    def reset_databricks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabricks", []))

    @jsii.member(jsii_name="resetJira")
    def reset_jira(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJira", []))

    @jsii.member(jsii_name="resetMariaDb")
    def reset_maria_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMariaDb", []))

    @jsii.member(jsii_name="resetMysql")
    def reset_mysql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysql", []))

    @jsii.member(jsii_name="resetOracle")
    def reset_oracle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracle", []))

    @jsii.member(jsii_name="resetPostgresql")
    def reset_postgresql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresql", []))

    @jsii.member(jsii_name="resetPresto")
    def reset_presto(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresto", []))

    @jsii.member(jsii_name="resetRds")
    def reset_rds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRds", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetServiceNow")
    def reset_service_now(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceNow", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="resetSpark")
    def reset_spark(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpark", []))

    @jsii.member(jsii_name="resetSqlServer")
    def reset_sql_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlServer", []))

    @jsii.member(jsii_name="resetTeradata")
    def reset_teradata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeradata", []))

    @jsii.member(jsii_name="resetTwitter")
    def reset_twitter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwitter", []))

    @builtins.property
    @jsii.member(jsii_name="amazonElasticsearch")
    def amazon_elasticsearch(
        self,
    ) -> QuicksightDataSourceParametersAmazonElasticsearchOutputReference:
        return typing.cast(QuicksightDataSourceParametersAmazonElasticsearchOutputReference, jsii.get(self, "amazonElasticsearch"))

    @builtins.property
    @jsii.member(jsii_name="athena")
    def athena(self) -> QuicksightDataSourceParametersAthenaOutputReference:
        return typing.cast(QuicksightDataSourceParametersAthenaOutputReference, jsii.get(self, "athena"))

    @builtins.property
    @jsii.member(jsii_name="aurora")
    def aurora(self) -> QuicksightDataSourceParametersAuroraOutputReference:
        return typing.cast(QuicksightDataSourceParametersAuroraOutputReference, jsii.get(self, "aurora"))

    @builtins.property
    @jsii.member(jsii_name="auroraPostgresql")
    def aurora_postgresql(
        self,
    ) -> QuicksightDataSourceParametersAuroraPostgresqlOutputReference:
        return typing.cast(QuicksightDataSourceParametersAuroraPostgresqlOutputReference, jsii.get(self, "auroraPostgresql"))

    @builtins.property
    @jsii.member(jsii_name="awsIotAnalytics")
    def aws_iot_analytics(
        self,
    ) -> QuicksightDataSourceParametersAwsIotAnalyticsOutputReference:
        return typing.cast(QuicksightDataSourceParametersAwsIotAnalyticsOutputReference, jsii.get(self, "awsIotAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="databricks")
    def databricks(self) -> QuicksightDataSourceParametersDatabricksOutputReference:
        return typing.cast(QuicksightDataSourceParametersDatabricksOutputReference, jsii.get(self, "databricks"))

    @builtins.property
    @jsii.member(jsii_name="jira")
    def jira(self) -> QuicksightDataSourceParametersJiraOutputReference:
        return typing.cast(QuicksightDataSourceParametersJiraOutputReference, jsii.get(self, "jira"))

    @builtins.property
    @jsii.member(jsii_name="mariaDb")
    def maria_db(self) -> QuicksightDataSourceParametersMariaDbOutputReference:
        return typing.cast(QuicksightDataSourceParametersMariaDbOutputReference, jsii.get(self, "mariaDb"))

    @builtins.property
    @jsii.member(jsii_name="mysql")
    def mysql(self) -> QuicksightDataSourceParametersMysqlOutputReference:
        return typing.cast(QuicksightDataSourceParametersMysqlOutputReference, jsii.get(self, "mysql"))

    @builtins.property
    @jsii.member(jsii_name="oracle")
    def oracle(self) -> QuicksightDataSourceParametersOracleOutputReference:
        return typing.cast(QuicksightDataSourceParametersOracleOutputReference, jsii.get(self, "oracle"))

    @builtins.property
    @jsii.member(jsii_name="postgresql")
    def postgresql(self) -> "QuicksightDataSourceParametersPostgresqlOutputReference":
        return typing.cast("QuicksightDataSourceParametersPostgresqlOutputReference", jsii.get(self, "postgresql"))

    @builtins.property
    @jsii.member(jsii_name="presto")
    def presto(self) -> "QuicksightDataSourceParametersPrestoOutputReference":
        return typing.cast("QuicksightDataSourceParametersPrestoOutputReference", jsii.get(self, "presto"))

    @builtins.property
    @jsii.member(jsii_name="rds")
    def rds(self) -> "QuicksightDataSourceParametersRdsOutputReference":
        return typing.cast("QuicksightDataSourceParametersRdsOutputReference", jsii.get(self, "rds"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(self) -> "QuicksightDataSourceParametersRedshiftOutputReference":
        return typing.cast("QuicksightDataSourceParametersRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "QuicksightDataSourceParametersS3OutputReference":
        return typing.cast("QuicksightDataSourceParametersS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="serviceNow")
    def service_now(self) -> "QuicksightDataSourceParametersServiceNowOutputReference":
        return typing.cast("QuicksightDataSourceParametersServiceNowOutputReference", jsii.get(self, "serviceNow"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(self) -> "QuicksightDataSourceParametersSnowflakeOutputReference":
        return typing.cast("QuicksightDataSourceParametersSnowflakeOutputReference", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="spark")
    def spark(self) -> "QuicksightDataSourceParametersSparkOutputReference":
        return typing.cast("QuicksightDataSourceParametersSparkOutputReference", jsii.get(self, "spark"))

    @builtins.property
    @jsii.member(jsii_name="sqlServer")
    def sql_server(self) -> "QuicksightDataSourceParametersSqlServerOutputReference":
        return typing.cast("QuicksightDataSourceParametersSqlServerOutputReference", jsii.get(self, "sqlServer"))

    @builtins.property
    @jsii.member(jsii_name="teradata")
    def teradata(self) -> "QuicksightDataSourceParametersTeradataOutputReference":
        return typing.cast("QuicksightDataSourceParametersTeradataOutputReference", jsii.get(self, "teradata"))

    @builtins.property
    @jsii.member(jsii_name="twitter")
    def twitter(self) -> "QuicksightDataSourceParametersTwitterOutputReference":
        return typing.cast("QuicksightDataSourceParametersTwitterOutputReference", jsii.get(self, "twitter"))

    @builtins.property
    @jsii.member(jsii_name="amazonElasticsearchInput")
    def amazon_elasticsearch_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch], jsii.get(self, "amazonElasticsearchInput"))

    @builtins.property
    @jsii.member(jsii_name="athenaInput")
    def athena_input(self) -> typing.Optional[QuicksightDataSourceParametersAthena]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAthena], jsii.get(self, "athenaInput"))

    @builtins.property
    @jsii.member(jsii_name="auroraInput")
    def aurora_input(self) -> typing.Optional[QuicksightDataSourceParametersAurora]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAurora], jsii.get(self, "auroraInput"))

    @builtins.property
    @jsii.member(jsii_name="auroraPostgresqlInput")
    def aurora_postgresql_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAuroraPostgresql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAuroraPostgresql], jsii.get(self, "auroraPostgresqlInput"))

    @builtins.property
    @jsii.member(jsii_name="awsIotAnalyticsInput")
    def aws_iot_analytics_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics], jsii.get(self, "awsIotAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="databricksInput")
    def databricks_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersDatabricks]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersDatabricks], jsii.get(self, "databricksInput"))

    @builtins.property
    @jsii.member(jsii_name="jiraInput")
    def jira_input(self) -> typing.Optional[QuicksightDataSourceParametersJira]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersJira], jsii.get(self, "jiraInput"))

    @builtins.property
    @jsii.member(jsii_name="mariaDbInput")
    def maria_db_input(self) -> typing.Optional[QuicksightDataSourceParametersMariaDb]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersMariaDb], jsii.get(self, "mariaDbInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlInput")
    def mysql_input(self) -> typing.Optional[QuicksightDataSourceParametersMysql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersMysql], jsii.get(self, "mysqlInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleInput")
    def oracle_input(self) -> typing.Optional[QuicksightDataSourceParametersOracle]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersOracle], jsii.get(self, "oracleInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlInput")
    def postgresql_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersPostgresql"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersPostgresql"], jsii.get(self, "postgresqlInput"))

    @builtins.property
    @jsii.member(jsii_name="prestoInput")
    def presto_input(self) -> typing.Optional["QuicksightDataSourceParametersPresto"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersPresto"], jsii.get(self, "prestoInput"))

    @builtins.property
    @jsii.member(jsii_name="rdsInput")
    def rds_input(self) -> typing.Optional["QuicksightDataSourceParametersRds"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersRds"], jsii.get(self, "rdsInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersRedshift"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional["QuicksightDataSourceParametersS3"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="serviceNowInput")
    def service_now_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersServiceNow"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersServiceNow"], jsii.get(self, "serviceNowInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersSnowflake"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSnowflake"], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkInput")
    def spark_input(self) -> typing.Optional["QuicksightDataSourceParametersSpark"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSpark"], jsii.get(self, "sparkInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlServerInput")
    def sql_server_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersSqlServer"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersSqlServer"], jsii.get(self, "sqlServerInput"))

    @builtins.property
    @jsii.member(jsii_name="teradataInput")
    def teradata_input(
        self,
    ) -> typing.Optional["QuicksightDataSourceParametersTeradata"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersTeradata"], jsii.get(self, "teradataInput"))

    @builtins.property
    @jsii.member(jsii_name="twitterInput")
    def twitter_input(self) -> typing.Optional["QuicksightDataSourceParametersTwitter"]:
        return typing.cast(typing.Optional["QuicksightDataSourceParametersTwitter"], jsii.get(self, "twitterInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParameters]:
        return typing.cast(typing.Optional[QuicksightDataSourceParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d8f42ad592c417b0d67d470130bf9018d185f5f756551f8caffbdc6cd095fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersPostgresql",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersPostgresql:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5fe278e6076b8fc0aa5dbc12b7c291f1891e0f25c57954801f96d3645562891)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersPostgresql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersPostgresqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersPostgresqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73de2786eec3649e0df663479e8f01da251138b6369e6b8a14fb345b216e79b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c1062f4b775ec970d1de90d2e65f56b0dceed92e447d7be47ba9eaa518fb50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e232096625cef2c2cd4a2d5b2e5efacc89175441277ddeebfb4980d4a543e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a748ccbe98acf100cddb0fa1091fe97602c4d090f32df88fe19b1db804400469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersPostgresql]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersPostgresql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersPostgresql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576c3f0836b18d993b45c0b1512f14338bfd175abad7ef9e3ab850b2f42ecf18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersPresto",
    jsii_struct_bases=[],
    name_mapping={"catalog": "catalog", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersPresto:
    def __init__(
        self,
        *,
        catalog: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#catalog QuicksightDataSource#catalog}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1999b008b32640a2bedd02bfcc29ac828a69dfdf5ddbd507d76d2f2ed5a098)
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "catalog": catalog,
            "host": host,
            "port": port,
        }

    @builtins.property
    def catalog(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#catalog QuicksightDataSource#catalog}.'''
        result = self._values.get("catalog")
        assert result is not None, "Required property 'catalog' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersPresto(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersPrestoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersPrestoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cc54ee9e933a387c82ad76420eec0952d1b0ac78a855b543bd74a712a51c97d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184dd3f9b7e7cedc80a1589a2bdce4267b0e98ae1a0f4e235033c0a7d2f65e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6aea2cbdcdbacf8f1ec83a73cfd7435f23dd00f59f0f647a4598de513dbb9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a70e65b6ed120ff095103589e1224188a40d1d6343795b33f84f95ca2f5708a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersPresto]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersPresto], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersPresto],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c227635381bca2ca9c090ca88a7472928919851d84edae9a82b61368674ffad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersRds",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "instance_id": "instanceId"},
)
class QuicksightDataSourceParametersRds:
    def __init__(self, *, database: builtins.str, instance_id: builtins.str) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#instance_id QuicksightDataSource#instance_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea6d4fe70a38653655d3ca94126a1b45fec63504237685896b4e64ca9dd7241)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "instance_id": instance_id,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#instance_id QuicksightDataSource#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersRds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersRdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersRdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95ff9591435afc2d4f10b6cc416b7897cd3a36af42da8e363877c7720d72c888)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853a325e5d638e71972682e7ae1059898638dc3a9b78b1858b47e17f936dd5c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab609fa14f8601643d76777985b3f6e9267b7db620677ea526b8df2a1c9771b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersRds]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersRds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersRds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1049b1b485a02d210eb334ddd2bb14d6f16099c1e8956f2fea4c2fd82d92f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersRedshift",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "cluster_id": "clusterId",
        "host": "host",
        "port": "port",
    },
)
class QuicksightDataSourceParametersRedshift:
    def __init__(
        self,
        *,
        database: builtins.str,
        cluster_id: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#cluster_id QuicksightDataSource#cluster_id}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd9cc108b60c0ef5aeb41fc268ffb62d44bd0e21606f8f979a87fb11f70c318)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
        }
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if host is not None:
            self._values["host"] = host
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#cluster_id QuicksightDataSource#cluster_id}.'''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__094ed789f7034a5570fce9330a2a968f15eb3a484a00b180ccc91d852547d724)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClusterId")
    def reset_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterId", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e1c6a7018bf77028270d66df6fa188510df82e1e13f6cd842f39c3883c41a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e8bb8d391fdee43642edf9a5e5d20d55de0945e93d715c36fb70675db07128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2528a34dec236e5407f213c4d676ce694ef5460b471a76a591d5ce0599d3c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61ca1ad4e2856f7a3ae763f9bb9ac7d83ae7f8d4c18b41063c314812644f031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersRedshift]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd25dc69f97ad8a6850349602d7ebf4b1a1cec48e14850675d58b627b7e8a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersS3",
    jsii_struct_bases=[],
    name_mapping={
        "manifest_file_location": "manifestFileLocation",
        "role_arn": "roleArn",
    },
)
class QuicksightDataSourceParametersS3:
    def __init__(
        self,
        *,
        manifest_file_location: typing.Union["QuicksightDataSourceParametersS3ManifestFileLocation", typing.Dict[builtins.str, typing.Any]],
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manifest_file_location: manifest_file_location block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#manifest_file_location QuicksightDataSource#manifest_file_location}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#role_arn QuicksightDataSource#role_arn}.
        '''
        if isinstance(manifest_file_location, dict):
            manifest_file_location = QuicksightDataSourceParametersS3ManifestFileLocation(**manifest_file_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0430ffbd2118ae78bfcf78f4e51aa72a78dde6700e3b8721ee0b3978f448039e)
            check_type(argname="argument manifest_file_location", value=manifest_file_location, expected_type=type_hints["manifest_file_location"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "manifest_file_location": manifest_file_location,
        }
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def manifest_file_location(
        self,
    ) -> "QuicksightDataSourceParametersS3ManifestFileLocation":
        '''manifest_file_location block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#manifest_file_location QuicksightDataSource#manifest_file_location}
        '''
        result = self._values.get("manifest_file_location")
        assert result is not None, "Required property 'manifest_file_location' is missing"
        return typing.cast("QuicksightDataSourceParametersS3ManifestFileLocation", result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#role_arn QuicksightDataSource#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersS3ManifestFileLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "key": "key"},
)
class QuicksightDataSourceParametersS3ManifestFileLocation:
    def __init__(self, *, bucket: builtins.str, key: builtins.str) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#bucket QuicksightDataSource#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#key QuicksightDataSource#key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7727425112c7dfe781657c10ae11ca29867c485a0ece801723695fcaf3d45b10)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "key": key,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#bucket QuicksightDataSource#bucket}.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#key QuicksightDataSource#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersS3ManifestFileLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersS3ManifestFileLocationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersS3ManifestFileLocationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52b86cec4821e8c5f87d314d6bbe1da5dd54325cccb5662cc523fb3f8ebeb329)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee889b78f0a06f463b7354bdeedce6295bf4fb24bcfdde810db7a0697ef4933f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690e0ac0bab6ef8e9c745d692bbfadb01e17cd8a2068a08fcc9fd83477826c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11152c247326d73216e0c1fc85ef26ca399cb9f417a67017e123ccbb533a7d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSourceParametersS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19f051b2723c193369b5b5f73f4fa5bbf50ec7df8ba0655ee18ae14e3c56e18b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putManifestFileLocation")
    def put_manifest_file_location(
        self,
        *,
        bucket: builtins.str,
        key: builtins.str,
    ) -> None:
        '''
        :param bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#bucket QuicksightDataSource#bucket}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#key QuicksightDataSource#key}.
        '''
        value = QuicksightDataSourceParametersS3ManifestFileLocation(
            bucket=bucket, key=key
        )

        return typing.cast(None, jsii.invoke(self, "putManifestFileLocation", [value]))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="manifestFileLocation")
    def manifest_file_location(
        self,
    ) -> QuicksightDataSourceParametersS3ManifestFileLocationOutputReference:
        return typing.cast(QuicksightDataSourceParametersS3ManifestFileLocationOutputReference, jsii.get(self, "manifestFileLocation"))

    @builtins.property
    @jsii.member(jsii_name="manifestFileLocationInput")
    def manifest_file_location_input(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation], jsii.get(self, "manifestFileLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2ab1ecf81354231d8ae2c67a86b7ae9b86e29541ba054c08c7c23a1a49847b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersS3]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e845b7d304e017d37b0e0c0a06cefd1a05ebe5866578e867b913e1d04725da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersServiceNow",
    jsii_struct_bases=[],
    name_mapping={"site_base_url": "siteBaseUrl"},
)
class QuicksightDataSourceParametersServiceNow:
    def __init__(self, *, site_base_url: builtins.str) -> None:
        '''
        :param site_base_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b81526d92f18fd878014fb2dd85e2f9034682d3c7b410a0557d46c0e1d0ff3)
            check_type(argname="argument site_base_url", value=site_base_url, expected_type=type_hints["site_base_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_base_url": site_base_url,
        }

    @builtins.property
    def site_base_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#site_base_url QuicksightDataSource#site_base_url}.'''
        result = self._values.get("site_base_url")
        assert result is not None, "Required property 'site_base_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersServiceNow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersServiceNowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersServiceNowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8deb9aabd5183427b1fa421a3a112447cf90e0cc28fd7742ef2c80d3935765e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="siteBaseUrlInput")
    def site_base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteBaseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="siteBaseUrl")
    def site_base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "siteBaseUrl"))

    @site_base_url.setter
    def site_base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b690eb18bb27e2243a16f83cd4120d4755390d8fada2399ab8e08a5437240624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteBaseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersServiceNow]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersServiceNow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersServiceNow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f368858104f10bc3791c51ddeb1b17deff82cb30849514e827c7f4e2a15a2ae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSnowflake",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "warehouse": "warehouse"},
)
class QuicksightDataSourceParametersSnowflake:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        warehouse: builtins.str,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param warehouse: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#warehouse QuicksightDataSource#warehouse}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9838118b8380ea240cc3c1690dbff0c1d1972c2483bf3481d57f4fbac08e2c)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument warehouse", value=warehouse, expected_type=type_hints["warehouse"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "warehouse": warehouse,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def warehouse(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#warehouse QuicksightDataSource#warehouse}.'''
        result = self._values.get("warehouse")
        assert result is not None, "Required property 'warehouse' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__031d6d56e64220696fefb34c4db1dcd9b62788a1030c30985dd671653878fe07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="warehouseInput")
    def warehouse_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__732382509eadf2a46d0c787734cca30ebbad87a008667348dfa7ee1eda5669a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d6f5b6e5054b338e044fe10124b16c9e4c82c8fd2c2b72599f6c14c5170239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="warehouse")
    def warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouse"))

    @warehouse.setter
    def warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c1413713897ac5321fa64eddb0179bff1a6b2ef6595e5be9bd3f2e719b12c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersSnowflake]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersSnowflake], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersSnowflake],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a535c4b032150bf1839b20cbf9220eef63756d3af57228fe30d73582325d27cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSpark",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port"},
)
class QuicksightDataSourceParametersSpark:
    def __init__(self, *, host: builtins.str, port: jsii.Number) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f4c3c86ac2a2094504bec475c860eb60f00bf2e569c5cadbdde4e7ae537635)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "port": port,
        }

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersSpark(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersSparkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSparkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6438a0e4367fcd90a572c7ded6bc278bf1b17657ba5eb44cedbe30d1c352d25f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc254876bd788bb40c3cb45ee0e90c3425efc5b3798f1fc02b15e6139d64a145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1c69036c4944921e9d7b77ebe1c1f4b1bfc647451aca7ef6da85238db27b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersSpark]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersSpark], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersSpark],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c459b0d08a87f9512f4277f1c7484a01aa4f4cedfb4c379d76815c85c8b6690b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSqlServer",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersSqlServer:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f438995ac4ee18828919d5e3c9e8da73495f7bcdd79e5a9e5109d2ccb47c6856)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersSqlServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersSqlServerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersSqlServerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9b2f70c784e6d2cb778b9e97e7b0bc8e359f485ec299a3c89ceea893968c2ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ce7da27ece5ff1188f4b5683112efb6b0c3ce52e36faff80807de1ecb0a27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a0fc8271cb5afcd92b3ba71243261bbe62564390424a078e48356514f10d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7cb7d44a040dc3cffa7b54682e49e2a88a03e324d7836e29f32f9d282cd6866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceParametersSqlServer]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersSqlServer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersSqlServer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4414771036c714ddb2c9bafeeb0871629271a8f58efb9da44b9740cb9ee36001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersTeradata",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "host": "host", "port": "port"},
)
class QuicksightDataSourceParametersTeradata:
    def __init__(
        self,
        *,
        database: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2878b47dae0b269a02aff20e8a9d7a04329feeb2deca1962cb2f14a5170e272)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "host": host,
            "port": port,
        }

    @builtins.property
    def database(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#database QuicksightDataSource#database}.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#host QuicksightDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#port QuicksightDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersTeradata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersTeradataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersTeradataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f83508b814f9349d49dfae821846420a0dc879dcf613e91a105db5f9c03165a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80195a5c45752f86546fc3dd4b53e564651b51f35d63923576ee0df44671102c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9773775bae37bd0961bb98d5efe796f542161d04b9b5b5ac0165901a7a6dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6ef3f30ddeefac596279b56fb8a740aee4a35ec4484d1bd497efebe472f4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersTeradata]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersTeradata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersTeradata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3383000239d07d30d04e771475a181e2ed2bd4900b07ac89706cd12f0cfbb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersTwitter",
    jsii_struct_bases=[],
    name_mapping={"max_rows": "maxRows", "query": "query"},
)
class QuicksightDataSourceParametersTwitter:
    def __init__(self, *, max_rows: jsii.Number, query: builtins.str) -> None:
        '''
        :param max_rows: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#max_rows QuicksightDataSource#max_rows}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#query QuicksightDataSource#query}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b05ea844c5f9abfabdcf525cc03ee07654a20ae1308a7f51717de2bcea8e9dd)
            check_type(argname="argument max_rows", value=max_rows, expected_type=type_hints["max_rows"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_rows": max_rows,
            "query": query,
        }

    @builtins.property
    def max_rows(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#max_rows QuicksightDataSource#max_rows}.'''
        result = self._values.get("max_rows")
        assert result is not None, "Required property 'max_rows' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#query QuicksightDataSource#query}.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceParametersTwitter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceParametersTwitterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceParametersTwitterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1ab5531568fb77656a45a2e728ef88674a28ef3fd47a39ce102b6ca82c5a904)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxRowsInput")
    def max_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRows")
    def max_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRows"))

    @max_rows.setter
    def max_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff04b913402df2a1eae452ada7f67a85eb2c4a0885921bcf5763f802788b4fb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90aaffb8d09e26768dcd62af47fb57f5d5fa00c32d309e0e2132f58cb49d32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceParametersTwitter]:
        return typing.cast(typing.Optional[QuicksightDataSourceParametersTwitter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceParametersTwitter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da63487c033215e7b3a8cb9198b917f406d2baf9418fc19eb52514ba9377c2b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourcePermission",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "principal": "principal"},
)
class QuicksightDataSourcePermission:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        principal: builtins.str,
    ) -> None:
        '''
        :param actions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#actions QuicksightDataSource#actions}.
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#principal QuicksightDataSource#principal}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e902d8df847d5d7a05eed76b016c638914ffdbf0bc1b433569ca21416b035d)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "principal": principal,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#actions QuicksightDataSource#actions}.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#principal QuicksightDataSource#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourcePermission(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourcePermissionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourcePermissionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__217db314c9b4e9e35ea07df2d685685e1f767a51e65540e69488dd3c8340289d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSourcePermissionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3882e0f9c87d652e282d87279e8b2f62d5201bb1292c8a07224aacee2659d7db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSourcePermissionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37ca6ffe0b5d926c8024c40d38734962f923af55393e2bbb9260b4f9f6beebc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eabd96703b0c5ed38b2ae48db2fbb9da4dcb2dae9b2545b1f5bb98fbdc82fbfc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d58b4d11aa6da1872b3db7500210379a8f0c9c30a3a46994691a71d5e20377a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSourcePermission]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSourcePermission]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSourcePermission]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7338e933e3c1b65d553c8b955e0da0a17d00a59f208b1c9dc1544682f3e081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSourcePermissionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourcePermissionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8292041a9702291577d24968701f1507447de6bc2c1057f2ee4a30e9e41d757f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb1653204a771df7d462ba03b91bba0a1a7c404d2003c8411a92c83fd58a980)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d050b653d1b6e5518919213463a39ce7ce8ef265642699d0a0f7bfddd6300da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSourcePermission]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSourcePermission]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSourcePermission]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520c6ec1b43cfea0a281a00f0720777aaf586f211e731ba802754055c42cd84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceSslProperties",
    jsii_struct_bases=[],
    name_mapping={"disable_ssl": "disableSsl"},
)
class QuicksightDataSourceSslProperties:
    def __init__(
        self,
        *,
        disable_ssl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param disable_ssl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#disable_ssl QuicksightDataSource#disable_ssl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3b1c93a579b71c958e6f5b7991900ac8b3eb2475b01bcdb2419f57509b9d01)
            check_type(argname="argument disable_ssl", value=disable_ssl, expected_type=type_hints["disable_ssl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disable_ssl": disable_ssl,
        }

    @builtins.property
    def disable_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#disable_ssl QuicksightDataSource#disable_ssl}.'''
        result = self._values.get("disable_ssl")
        assert result is not None, "Required property 'disable_ssl' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceSslProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceSslPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceSslPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__203d92fe35abe820f3c171b3a8e26af01173e4f8e832dd737b3f221144ecf3af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="disableSslInput")
    def disable_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableSslInput"))

    @builtins.property
    @jsii.member(jsii_name="disableSsl")
    def disable_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableSsl"))

    @disable_ssl.setter
    def disable_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0eaad512c22894a918a0ab25f12634dba60ea365c9bc0ffdb3b36e30f88786)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableSsl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSourceSslProperties]:
        return typing.cast(typing.Optional[QuicksightDataSourceSslProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceSslProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b329f97317a68eccae6d065ebc1d0bd3845d8be3c8726a7267e3b69cb1115d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceVpcConnectionProperties",
    jsii_struct_bases=[],
    name_mapping={"vpc_connection_arn": "vpcConnectionArn"},
)
class QuicksightDataSourceVpcConnectionProperties:
    def __init__(self, *, vpc_connection_arn: builtins.str) -> None:
        '''
        :param vpc_connection_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#vpc_connection_arn QuicksightDataSource#vpc_connection_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0944d0e0802e54fdb3531ba341d42c80843048c06deacdc65db2d31a774726d1)
            check_type(argname="argument vpc_connection_arn", value=vpc_connection_arn, expected_type=type_hints["vpc_connection_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_connection_arn": vpc_connection_arn,
        }

    @builtins.property
    def vpc_connection_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_source#vpc_connection_arn QuicksightDataSource#vpc_connection_arn}.'''
        result = self._values.get("vpc_connection_arn")
        assert result is not None, "Required property 'vpc_connection_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSourceVpcConnectionProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSourceVpcConnectionPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSource.QuicksightDataSourceVpcConnectionPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__528c9b168c606647a55601400b9f998b2d315cd5cf8d82ae86299b38d15fc6ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="vpcConnectionArnInput")
    def vpc_connection_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcConnectionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConnectionArn")
    def vpc_connection_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcConnectionArn"))

    @vpc_connection_arn.setter
    def vpc_connection_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd09e638cab26a93f6a1b9b1b514aca5d8fd7cec0809bbdd38dafa78634c659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConnectionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSourceVpcConnectionProperties]:
        return typing.cast(typing.Optional[QuicksightDataSourceVpcConnectionProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSourceVpcConnectionProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810220b3997457cf43e19afbe6402493df7860edbfffc9f73955b9e9d07a426f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QuicksightDataSource",
    "QuicksightDataSourceConfig",
    "QuicksightDataSourceCredentials",
    "QuicksightDataSourceCredentialsCredentialPair",
    "QuicksightDataSourceCredentialsCredentialPairOutputReference",
    "QuicksightDataSourceCredentialsOutputReference",
    "QuicksightDataSourceParameters",
    "QuicksightDataSourceParametersAmazonElasticsearch",
    "QuicksightDataSourceParametersAmazonElasticsearchOutputReference",
    "QuicksightDataSourceParametersAthena",
    "QuicksightDataSourceParametersAthenaOutputReference",
    "QuicksightDataSourceParametersAurora",
    "QuicksightDataSourceParametersAuroraOutputReference",
    "QuicksightDataSourceParametersAuroraPostgresql",
    "QuicksightDataSourceParametersAuroraPostgresqlOutputReference",
    "QuicksightDataSourceParametersAwsIotAnalytics",
    "QuicksightDataSourceParametersAwsIotAnalyticsOutputReference",
    "QuicksightDataSourceParametersDatabricks",
    "QuicksightDataSourceParametersDatabricksOutputReference",
    "QuicksightDataSourceParametersJira",
    "QuicksightDataSourceParametersJiraOutputReference",
    "QuicksightDataSourceParametersMariaDb",
    "QuicksightDataSourceParametersMariaDbOutputReference",
    "QuicksightDataSourceParametersMysql",
    "QuicksightDataSourceParametersMysqlOutputReference",
    "QuicksightDataSourceParametersOracle",
    "QuicksightDataSourceParametersOracleOutputReference",
    "QuicksightDataSourceParametersOutputReference",
    "QuicksightDataSourceParametersPostgresql",
    "QuicksightDataSourceParametersPostgresqlOutputReference",
    "QuicksightDataSourceParametersPresto",
    "QuicksightDataSourceParametersPrestoOutputReference",
    "QuicksightDataSourceParametersRds",
    "QuicksightDataSourceParametersRdsOutputReference",
    "QuicksightDataSourceParametersRedshift",
    "QuicksightDataSourceParametersRedshiftOutputReference",
    "QuicksightDataSourceParametersS3",
    "QuicksightDataSourceParametersS3ManifestFileLocation",
    "QuicksightDataSourceParametersS3ManifestFileLocationOutputReference",
    "QuicksightDataSourceParametersS3OutputReference",
    "QuicksightDataSourceParametersServiceNow",
    "QuicksightDataSourceParametersServiceNowOutputReference",
    "QuicksightDataSourceParametersSnowflake",
    "QuicksightDataSourceParametersSnowflakeOutputReference",
    "QuicksightDataSourceParametersSpark",
    "QuicksightDataSourceParametersSparkOutputReference",
    "QuicksightDataSourceParametersSqlServer",
    "QuicksightDataSourceParametersSqlServerOutputReference",
    "QuicksightDataSourceParametersTeradata",
    "QuicksightDataSourceParametersTeradataOutputReference",
    "QuicksightDataSourceParametersTwitter",
    "QuicksightDataSourceParametersTwitterOutputReference",
    "QuicksightDataSourcePermission",
    "QuicksightDataSourcePermissionList",
    "QuicksightDataSourcePermissionOutputReference",
    "QuicksightDataSourceSslProperties",
    "QuicksightDataSourceSslPropertiesOutputReference",
    "QuicksightDataSourceVpcConnectionProperties",
    "QuicksightDataSourceVpcConnectionPropertiesOutputReference",
]

publication.publish()

def _typecheckingstub__ed5fe7277a73407ec4dbd9499078245c5f6e63de15c139fd0a1611a48734ee96(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_source_id: builtins.str,
    name: builtins.str,
    parameters: typing.Union[QuicksightDataSourceParameters, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[QuicksightDataSourceCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSourcePermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssl_properties: typing.Optional[typing.Union[QuicksightDataSourceSslProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_connection_properties: typing.Optional[typing.Union[QuicksightDataSourceVpcConnectionProperties, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6a250ae2b4458d6bb2bba18ff5ae123cd018fe88f30cb882c6f8be21b70b64fc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38905942f7349aaa86ea38c3a9a28721ce04f9ff70a41b287205595773c369b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSourcePermission, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231d92da58bd56366dd194cfa88989be83bdd0318e729da2e21f86b02dbe7f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f9c5eb1a8fc19ff2c57348ba5ff59d770ef53f2337eb4244755694bff77795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bced0e57186cbe6824020d222e4da487a616d4a16686d385416c081bea835af4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3872557784bf849a99e80bc6e72f0ca23f36b6a7c2ab58623e812bd02baf218f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e27d42a148696eb245c3f02f4f817c7381d334e66c2c59e1d6c28af1118cbb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58c659e15cae5331df474dcc864160e04065bdc0e00231f295624700fb5b2a9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87de4bc32e45a07b0dd1896f863b53baf28737d1316aaa7e621889cb2b4f3dbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace59ef2c12ecb11cbb9da48181caa9765125bf00a740d57655355c04cc9d509(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_source_id: builtins.str,
    name: builtins.str,
    parameters: typing.Union[QuicksightDataSourceParameters, typing.Dict[builtins.str, typing.Any]],
    type: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[typing.Union[QuicksightDataSourceCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    permission: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSourcePermission, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssl_properties: typing.Optional[typing.Union[QuicksightDataSourceSslProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_connection_properties: typing.Optional[typing.Union[QuicksightDataSourceVpcConnectionProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcd7d18096e1a4599e7ade139321878a5e23b509830dd4e7bb5d700449b4eb9(
    *,
    copy_source_arn: typing.Optional[builtins.str] = None,
    credential_pair: typing.Optional[typing.Union[QuicksightDataSourceCredentialsCredentialPair, typing.Dict[builtins.str, typing.Any]]] = None,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1757a11c4883c42ef32dca254fca25071c4cc9a74465542166c5ccaf4bf97fa9(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a2fcdb914042f805321a524ee401c226cd8ce05ef9be17fca4208cfc5414bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75de464e7b3a93bc3173a5a394adfe4591fdc4348cdd1d6e2e81686c1ea9919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cfaeee11927cdd778498e732bac6262e6e89c58d078adf69deb3f5163d2670b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13ddd504b8e0beb5f32b2395e7e73e3fadc935a3f7d48a8e797754ffcbd8582(
    value: typing.Optional[QuicksightDataSourceCredentialsCredentialPair],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1baa26c34d191fc922ffc9dafb175f1e9988e45702c4fd0efcbb10efd796b445(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb80b38ec63cc32f9dfa35afd75eb393407aacfdba478c19eff871949b5e96c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55947bc272cc821aa6c5140dbbcb8c9a233d9cf85a179c218ad340b319717591(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__174cb92add5ec4cc9b05fd12dc78b3bd42b2f12fba09b6a47f3f7cce3da13cb7(
    value: typing.Optional[QuicksightDataSourceCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431a5f681cfa628f670dcb629107ec26712fa153ee5e0558429a6a6db49745ef(
    *,
    amazon_elasticsearch: typing.Optional[typing.Union[QuicksightDataSourceParametersAmazonElasticsearch, typing.Dict[builtins.str, typing.Any]]] = None,
    athena: typing.Optional[typing.Union[QuicksightDataSourceParametersAthena, typing.Dict[builtins.str, typing.Any]]] = None,
    aurora: typing.Optional[typing.Union[QuicksightDataSourceParametersAurora, typing.Dict[builtins.str, typing.Any]]] = None,
    aurora_postgresql: typing.Optional[typing.Union[QuicksightDataSourceParametersAuroraPostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_iot_analytics: typing.Optional[typing.Union[QuicksightDataSourceParametersAwsIotAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    databricks: typing.Optional[typing.Union[QuicksightDataSourceParametersDatabricks, typing.Dict[builtins.str, typing.Any]]] = None,
    jira: typing.Optional[typing.Union[QuicksightDataSourceParametersJira, typing.Dict[builtins.str, typing.Any]]] = None,
    maria_db: typing.Optional[typing.Union[QuicksightDataSourceParametersMariaDb, typing.Dict[builtins.str, typing.Any]]] = None,
    mysql: typing.Optional[typing.Union[QuicksightDataSourceParametersMysql, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle: typing.Optional[typing.Union[QuicksightDataSourceParametersOracle, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql: typing.Optional[typing.Union[QuicksightDataSourceParametersPostgresql, typing.Dict[builtins.str, typing.Any]]] = None,
    presto: typing.Optional[typing.Union[QuicksightDataSourceParametersPresto, typing.Dict[builtins.str, typing.Any]]] = None,
    rds: typing.Optional[typing.Union[QuicksightDataSourceParametersRds, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[QuicksightDataSourceParametersRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[QuicksightDataSourceParametersS3, typing.Dict[builtins.str, typing.Any]]] = None,
    service_now: typing.Optional[typing.Union[QuicksightDataSourceParametersServiceNow, typing.Dict[builtins.str, typing.Any]]] = None,
    snowflake: typing.Optional[typing.Union[QuicksightDataSourceParametersSnowflake, typing.Dict[builtins.str, typing.Any]]] = None,
    spark: typing.Optional[typing.Union[QuicksightDataSourceParametersSpark, typing.Dict[builtins.str, typing.Any]]] = None,
    sql_server: typing.Optional[typing.Union[QuicksightDataSourceParametersSqlServer, typing.Dict[builtins.str, typing.Any]]] = None,
    teradata: typing.Optional[typing.Union[QuicksightDataSourceParametersTeradata, typing.Dict[builtins.str, typing.Any]]] = None,
    twitter: typing.Optional[typing.Union[QuicksightDataSourceParametersTwitter, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482dcbb621ac863d7c60c3318c6307ab17613ebd14f228c5313361616f257721(
    *,
    domain: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4a8589d8734a004a2274e52a8b87d751f4f33a9755ef3cf064740a136cc303(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c21d0baad9fb3f249cfce4ff04628b6d5665acded4098531f87a26990085c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bafaf1c2adb10d2d1f55e9fb8aa224959e390e5ed9e7e9a6b8b2c71131082d9(
    value: typing.Optional[QuicksightDataSourceParametersAmazonElasticsearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331d741e9d006e66ec2cf88a16dd5b4fea4a9e02ce95b713af7f7acf22bd2b98(
    *,
    work_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ee1f182c9d8c10d6baaca231c2f02a9d321b598ef94f18530e5d6139b72753(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbd5377c68192b23e5d9358c1466c7a7d87d355ab7d0ade4e520dace2e7b1ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6729c268f4468b7d86733b23d0dbad625ccd22fa5a182a0a8175245f446c282(
    value: typing.Optional[QuicksightDataSourceParametersAthena],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9e20a0a9f58b039eb7242d392da6a7776dfb4f4a0d7a6869c4367e918b2fe1(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995bbf66536266f33b9b456f7795aa0544abfc4f43294c37e0c81aff073c7ffc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacfdbbce04f1e610471812c398ae8e94b818ee866ec40e06ed855867d09d20d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6571dc4770c283124fb1dc8d7dff7782ec0f8982680e38ac1b9349271fe0d6da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5680dbb418255fde49eaacc83a164244ae79882d09540663e0d7fb292035925d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771935f1a94fdb8785137f73f588edcc75ceaa013a3f4bdcdcc1f7f23e052ac9(
    value: typing.Optional[QuicksightDataSourceParametersAurora],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b4b587098f8296e1e6250d67c8768247564d9cf7b1a8a9972ec6de3348395a(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002a214383ab5df6201f05622f9abd6c10838a5590b33e19840a66e8b5be3e9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785a04a76c09624ecc88dc88654b172a02fd995fa4829619f48e4dfa70bf3358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdeb82226d28c5692c71863abaab0c0372288b7c555ca1a4b0bc7cc9a470bec6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1cd9bbbedffbd5fc89e78c086bcccecdabb1c83b8ea0bd9c463ce0c9fa9a14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02366467e54f1452c9ec93fd910a9caac65b2d1c5f5c7b32c4847e8af8fb8b0d(
    value: typing.Optional[QuicksightDataSourceParametersAuroraPostgresql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43255c026201428a863309e7b49ea5cba708cdd358af2df67c972fa44d33ffa1(
    *,
    data_set_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd0d9e5d773169b95a88e490caff092e31a7aa7a015b829c063408709c1846f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f024112483727b88847aeb59595ff35629b590ae140f1776402898100127ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26621f3f83b7ea34cac13a08471c14c9459f5a3ddd4c437d8f71e63f42a741cb(
    value: typing.Optional[QuicksightDataSourceParametersAwsIotAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be59de086d21a97d98cc6bda4d78d2065b04d86e3ba343caa44a56e5f83a5e19(
    *,
    host: builtins.str,
    port: jsii.Number,
    sql_endpoint_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d066f6fc4f07269a43c9daf982eb55699d7f507d639091aa2625d26774479fdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635a2188ebc9bbbdedea26d68a4a10951df0b70f4ee84963fb01fb2964c9bba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c66b099c5538b0fc8a14bda3db00c28b2cd26b23830f9fdf6becde2115395f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c8c4f3b8e58a79e5c318bd4ebf77d042a133cc218c2a5fa6c7c97ed4f8d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833c142ad2bf49978906a3223cd33183359b54f9f0816a50ec5ee63f45946adc(
    value: typing.Optional[QuicksightDataSourceParametersDatabricks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c22096c6bc2976622761062db6c5a248dfed94c1364ae3f77e7a820b05958be(
    *,
    site_base_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15771f60d0f5f5e8d328ab7ae7b3689cdf1562f62c8f5496ac003b21cf2eecb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2625fc0e368821460b5c1cfb0450d39b01622af462d23f59b5bb43a5dbf0b6f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d77218fa3157e7e486c3d3af558aa8bad27fd4c8a034d1328ccb01b3c87a8d7(
    value: typing.Optional[QuicksightDataSourceParametersJira],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf049f2a33ff28a01c76065c46ac5e7ef9aa9ff26134ddf442ee4d0bf833c37(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af7b878b2a12dfe28e6a5a77bc93b56cc90c58a9e9e4d33f90aa3f015ef18b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fdf2753c28e019dee5481f54f99e6735d368b6f1fd023b6084e3f80b072df5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d7db8d1f3ce34340c0f695031a3ab345b3a4e1b12256cf5dc995703c1b01ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb16b7f9e988f91f01bd4e1b9ae94ed5b58c2d83b3ecd316d0fa59ff72568ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff0faf3be2d88aff9c90f009aa4a32df7f23ae7b8d92539d002d70fd682ab42(
    value: typing.Optional[QuicksightDataSourceParametersMariaDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0479c145f28b151552baf9a6f9c914f210c685f21e1ed3daffc456a23c4036cc(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96ed01670592ccae0c6b3cde25b9ea56f382353b19bacf63582a844a5b52268(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5f25f8d074f5ff6ea24998b7c512cb399df55c623c01a06471270d5cdc9054(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944d8e6c289e2a430f5b822592a88c84acc82870d4623f0514865584bf4f24b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2593ad7886704eca498c16362a24d6e1809387e9b3e84f149cf69c21750e72a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b833205f972a2590077d813b72d304a50fc85c034f1c76137ee2cc207d696b(
    value: typing.Optional[QuicksightDataSourceParametersMysql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7726c7b82c7a3af38b50c900715fd4f7e5f35188cf1c921b42628241122152b(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd12c6b6229b443350bc373899f3eab321d3c87e51e161aba764a29dd6ea5b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e4f4d695e8ce1ac9c6c1db2146ed9f61936a61430444b98306003328143e81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c686baeb62c00942002a5a8483f4b1d74b20c7164b00b065867e4334b1612ea1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a679398d7d4e310aa28425200b0a8761af462ec329dc569b54383789415da88(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67693dedadf787f37348906df29a6ff8cdbf95eb4ad0529093ceed1b8a12913b(
    value: typing.Optional[QuicksightDataSourceParametersOracle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be8cd4e5ec4aef36f65e7d89468c4225ba80fac8fd35187274517ee52a56f51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8f42ad592c417b0d67d470130bf9018d185f5f756551f8caffbdc6cd095fdb(
    value: typing.Optional[QuicksightDataSourceParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5fe278e6076b8fc0aa5dbc12b7c291f1891e0f25c57954801f96d3645562891(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73de2786eec3649e0df663479e8f01da251138b6369e6b8a14fb345b216e79b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c1062f4b775ec970d1de90d2e65f56b0dceed92e447d7be47ba9eaa518fb50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e232096625cef2c2cd4a2d5b2e5efacc89175441277ddeebfb4980d4a543e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a748ccbe98acf100cddb0fa1091fe97602c4d090f32df88fe19b1db804400469(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576c3f0836b18d993b45c0b1512f14338bfd175abad7ef9e3ab850b2f42ecf18(
    value: typing.Optional[QuicksightDataSourceParametersPostgresql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1999b008b32640a2bedd02bfcc29ac828a69dfdf5ddbd507d76d2f2ed5a098(
    *,
    catalog: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc54ee9e933a387c82ad76420eec0952d1b0ac78a855b543bd74a712a51c97d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184dd3f9b7e7cedc80a1589a2bdce4267b0e98ae1a0f4e235033c0a7d2f65e71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6aea2cbdcdbacf8f1ec83a73cfd7435f23dd00f59f0f647a4598de513dbb9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a70e65b6ed120ff095103589e1224188a40d1d6343795b33f84f95ca2f5708a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c227635381bca2ca9c090ca88a7472928919851d84edae9a82b61368674ffad0(
    value: typing.Optional[QuicksightDataSourceParametersPresto],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea6d4fe70a38653655d3ca94126a1b45fec63504237685896b4e64ca9dd7241(
    *,
    database: builtins.str,
    instance_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ff9591435afc2d4f10b6cc416b7897cd3a36af42da8e363877c7720d72c888(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853a325e5d638e71972682e7ae1059898638dc3a9b78b1858b47e17f936dd5c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab609fa14f8601643d76777985b3f6e9267b7db620677ea526b8df2a1c9771b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1049b1b485a02d210eb334ddd2bb14d6f16099c1e8956f2fea4c2fd82d92f8(
    value: typing.Optional[QuicksightDataSourceParametersRds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd9cc108b60c0ef5aeb41fc268ffb62d44bd0e21606f8f979a87fb11f70c318(
    *,
    database: builtins.str,
    cluster_id: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094ed789f7034a5570fce9330a2a968f15eb3a484a00b180ccc91d852547d724(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e1c6a7018bf77028270d66df6fa188510df82e1e13f6cd842f39c3883c41a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e8bb8d391fdee43642edf9a5e5d20d55de0945e93d715c36fb70675db07128(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2528a34dec236e5407f213c4d676ce694ef5460b471a76a591d5ce0599d3c15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61ca1ad4e2856f7a3ae763f9bb9ac7d83ae7f8d4c18b41063c314812644f031(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd25dc69f97ad8a6850349602d7ebf4b1a1cec48e14850675d58b627b7e8a55(
    value: typing.Optional[QuicksightDataSourceParametersRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0430ffbd2118ae78bfcf78f4e51aa72a78dde6700e3b8721ee0b3978f448039e(
    *,
    manifest_file_location: typing.Union[QuicksightDataSourceParametersS3ManifestFileLocation, typing.Dict[builtins.str, typing.Any]],
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7727425112c7dfe781657c10ae11ca29867c485a0ece801723695fcaf3d45b10(
    *,
    bucket: builtins.str,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b86cec4821e8c5f87d314d6bbe1da5dd54325cccb5662cc523fb3f8ebeb329(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee889b78f0a06f463b7354bdeedce6295bf4fb24bcfdde810db7a0697ef4933f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690e0ac0bab6ef8e9c745d692bbfadb01e17cd8a2068a08fcc9fd83477826c49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11152c247326d73216e0c1fc85ef26ca399cb9f417a67017e123ccbb533a7d02(
    value: typing.Optional[QuicksightDataSourceParametersS3ManifestFileLocation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f051b2723c193369b5b5f73f4fa5bbf50ec7df8ba0655ee18ae14e3c56e18b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2ab1ecf81354231d8ae2c67a86b7ae9b86e29541ba054c08c7c23a1a49847b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e845b7d304e017d37b0e0c0a06cefd1a05ebe5866578e867b913e1d04725da(
    value: typing.Optional[QuicksightDataSourceParametersS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b81526d92f18fd878014fb2dd85e2f9034682d3c7b410a0557d46c0e1d0ff3(
    *,
    site_base_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8deb9aabd5183427b1fa421a3a112447cf90e0cc28fd7742ef2c80d3935765e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b690eb18bb27e2243a16f83cd4120d4755390d8fada2399ab8e08a5437240624(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f368858104f10bc3791c51ddeb1b17deff82cb30849514e827c7f4e2a15a2ae9(
    value: typing.Optional[QuicksightDataSourceParametersServiceNow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9838118b8380ea240cc3c1690dbff0c1d1972c2483bf3481d57f4fbac08e2c(
    *,
    database: builtins.str,
    host: builtins.str,
    warehouse: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031d6d56e64220696fefb34c4db1dcd9b62788a1030c30985dd671653878fe07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732382509eadf2a46d0c787734cca30ebbad87a008667348dfa7ee1eda5669a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d6f5b6e5054b338e044fe10124b16c9e4c82c8fd2c2b72599f6c14c5170239(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c1413713897ac5321fa64eddb0179bff1a6b2ef6595e5be9bd3f2e719b12c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a535c4b032150bf1839b20cbf9220eef63756d3af57228fe30d73582325d27cc(
    value: typing.Optional[QuicksightDataSourceParametersSnowflake],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f4c3c86ac2a2094504bec475c860eb60f00bf2e569c5cadbdde4e7ae537635(
    *,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6438a0e4367fcd90a572c7ded6bc278bf1b17657ba5eb44cedbe30d1c352d25f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc254876bd788bb40c3cb45ee0e90c3425efc5b3798f1fc02b15e6139d64a145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1c69036c4944921e9d7b77ebe1c1f4b1bfc647451aca7ef6da85238db27b8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c459b0d08a87f9512f4277f1c7484a01aa4f4cedfb4c379d76815c85c8b6690b(
    value: typing.Optional[QuicksightDataSourceParametersSpark],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f438995ac4ee18828919d5e3c9e8da73495f7bcdd79e5a9e5109d2ccb47c6856(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b2f70c784e6d2cb778b9e97e7b0bc8e359f485ec299a3c89ceea893968c2ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ce7da27ece5ff1188f4b5683112efb6b0c3ce52e36faff80807de1ecb0a27c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a0fc8271cb5afcd92b3ba71243261bbe62564390424a078e48356514f10d57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7cb7d44a040dc3cffa7b54682e49e2a88a03e324d7836e29f32f9d282cd6866(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4414771036c714ddb2c9bafeeb0871629271a8f58efb9da44b9740cb9ee36001(
    value: typing.Optional[QuicksightDataSourceParametersSqlServer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2878b47dae0b269a02aff20e8a9d7a04329feeb2deca1962cb2f14a5170e272(
    *,
    database: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f83508b814f9349d49dfae821846420a0dc879dcf613e91a105db5f9c03165a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80195a5c45752f86546fc3dd4b53e564651b51f35d63923576ee0df44671102c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9773775bae37bd0961bb98d5efe796f542161d04b9b5b5ac0165901a7a6dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6ef3f30ddeefac596279b56fb8a740aee4a35ec4484d1bd497efebe472f4db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3383000239d07d30d04e771475a181e2ed2bd4900b07ac89706cd12f0cfbb3(
    value: typing.Optional[QuicksightDataSourceParametersTeradata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b05ea844c5f9abfabdcf525cc03ee07654a20ae1308a7f51717de2bcea8e9dd(
    *,
    max_rows: jsii.Number,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ab5531568fb77656a45a2e728ef88674a28ef3fd47a39ce102b6ca82c5a904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff04b913402df2a1eae452ada7f67a85eb2c4a0885921bcf5763f802788b4fb7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90aaffb8d09e26768dcd62af47fb57f5d5fa00c32d309e0e2132f58cb49d32b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da63487c033215e7b3a8cb9198b917f406d2baf9418fc19eb52514ba9377c2b7(
    value: typing.Optional[QuicksightDataSourceParametersTwitter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e902d8df847d5d7a05eed76b016c638914ffdbf0bc1b433569ca21416b035d(
    *,
    actions: typing.Sequence[builtins.str],
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217db314c9b4e9e35ea07df2d685685e1f767a51e65540e69488dd3c8340289d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3882e0f9c87d652e282d87279e8b2f62d5201bb1292c8a07224aacee2659d7db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37ca6ffe0b5d926c8024c40d38734962f923af55393e2bbb9260b4f9f6beebc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabd96703b0c5ed38b2ae48db2fbb9da4dcb2dae9b2545b1f5bb98fbdc82fbfc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d58b4d11aa6da1872b3db7500210379a8f0c9c30a3a46994691a71d5e20377a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7338e933e3c1b65d553c8b955e0da0a17d00a59f208b1c9dc1544682f3e081(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSourcePermission]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8292041a9702291577d24968701f1507447de6bc2c1057f2ee4a30e9e41d757f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb1653204a771df7d462ba03b91bba0a1a7c404d2003c8411a92c83fd58a980(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d050b653d1b6e5518919213463a39ce7ce8ef265642699d0a0f7bfddd6300da5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520c6ec1b43cfea0a281a00f0720777aaf586f211e731ba802754055c42cd84c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSourcePermission]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3b1c93a579b71c958e6f5b7991900ac8b3eb2475b01bcdb2419f57509b9d01(
    *,
    disable_ssl: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203d92fe35abe820f3c171b3a8e26af01173e4f8e832dd737b3f221144ecf3af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c0eaad512c22894a918a0ab25f12634dba60ea365c9bc0ffdb3b36e30f88786(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b329f97317a68eccae6d065ebc1d0bd3845d8be3c8726a7267e3b69cb1115d(
    value: typing.Optional[QuicksightDataSourceSslProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0944d0e0802e54fdb3531ba341d42c80843048c06deacdc65db2d31a774726d1(
    *,
    vpc_connection_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528c9b168c606647a55601400b9f998b2d315cd5cf8d82ae86299b38d15fc6ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd09e638cab26a93f6a1b9b1b514aca5d8fd7cec0809bbdd38dafa78634c659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810220b3997457cf43e19afbe6402493df7860edbfffc9f73955b9e9d07a426f(
    value: typing.Optional[QuicksightDataSourceVpcConnectionProperties],
) -> None:
    """Type checking stubs"""
    pass
