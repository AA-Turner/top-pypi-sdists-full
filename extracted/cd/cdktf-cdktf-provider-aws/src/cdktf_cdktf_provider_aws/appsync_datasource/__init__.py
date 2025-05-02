r'''
# `aws_appsync_datasource`

Refer to the Terraform Registry for docs: [`aws_appsync_datasource`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource).
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


class AppsyncDatasource(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasource",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource aws_appsync_datasource}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dynamodb_config: typing.Optional[typing.Union["AppsyncDatasourceDynamodbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch_config: typing.Optional[typing.Union["AppsyncDatasourceElasticsearchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        event_bridge_config: typing.Optional[typing.Union["AppsyncDatasourceEventBridgeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        http_config: typing.Optional[typing.Union["AppsyncDatasourceHttpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        lambda_config: typing.Optional[typing.Union["AppsyncDatasourceLambdaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        opensearchservice_config: typing.Optional[typing.Union["AppsyncDatasourceOpensearchserviceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        relational_database_config: typing.Optional[typing.Union["AppsyncDatasourceRelationalDatabaseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource aws_appsync_datasource} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#api_id AppsyncDatasource#api_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#name AppsyncDatasource#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#type AppsyncDatasource#type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#description AppsyncDatasource#description}.
        :param dynamodb_config: dynamodb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#dynamodb_config AppsyncDatasource#dynamodb_config}
        :param elasticsearch_config: elasticsearch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#elasticsearch_config AppsyncDatasource#elasticsearch_config}
        :param event_bridge_config: event_bridge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#event_bridge_config AppsyncDatasource#event_bridge_config}
        :param http_config: http_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#http_config AppsyncDatasource#http_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#id AppsyncDatasource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lambda_config: lambda_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#lambda_config AppsyncDatasource#lambda_config}
        :param opensearchservice_config: opensearchservice_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#opensearchservice_config AppsyncDatasource#opensearchservice_config}
        :param relational_database_config: relational_database_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#relational_database_config AppsyncDatasource#relational_database_config}
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#service_role_arn AppsyncDatasource#service_role_arn}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0e3ba9433a03f5777389f2ac83f22977d1b7b4d00a0bfdd983275937f193d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AppsyncDatasourceConfig(
            api_id=api_id,
            name=name,
            type=type,
            description=description,
            dynamodb_config=dynamodb_config,
            elasticsearch_config=elasticsearch_config,
            event_bridge_config=event_bridge_config,
            http_config=http_config,
            id=id,
            lambda_config=lambda_config,
            opensearchservice_config=opensearchservice_config,
            relational_database_config=relational_database_config,
            service_role_arn=service_role_arn,
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
        '''Generates CDKTF code for importing a AppsyncDatasource resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppsyncDatasource to import.
        :param import_from_id: The id of the existing AppsyncDatasource that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppsyncDatasource to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f095d31deb30fe692c3247ca8610fb3c3aed0752198d6ab3199552e2a2f5881)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDynamodbConfig")
    def put_dynamodb_config(
        self,
        *,
        table_name: builtins.str,
        delta_sync_config: typing.Optional[typing.Union["AppsyncDatasourceDynamodbConfigDeltaSyncConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        use_caller_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        versioned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#table_name AppsyncDatasource#table_name}.
        :param delta_sync_config: delta_sync_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_config AppsyncDatasource#delta_sync_config}
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.
        :param use_caller_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#use_caller_credentials AppsyncDatasource#use_caller_credentials}.
        :param versioned: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#versioned AppsyncDatasource#versioned}.
        '''
        value = AppsyncDatasourceDynamodbConfig(
            table_name=table_name,
            delta_sync_config=delta_sync_config,
            region=region,
            use_caller_credentials=use_caller_credentials,
            versioned=versioned,
        )

        return typing.cast(None, jsii.invoke(self, "putDynamodbConfig", [value]))

    @jsii.member(jsii_name="putElasticsearchConfig")
    def put_elasticsearch_config(
        self,
        *,
        endpoint: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.
        '''
        value = AppsyncDatasourceElasticsearchConfig(endpoint=endpoint, region=region)

        return typing.cast(None, jsii.invoke(self, "putElasticsearchConfig", [value]))

    @jsii.member(jsii_name="putEventBridgeConfig")
    def put_event_bridge_config(self, *, event_bus_arn: builtins.str) -> None:
        '''
        :param event_bus_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#event_bus_arn AppsyncDatasource#event_bus_arn}.
        '''
        value = AppsyncDatasourceEventBridgeConfig(event_bus_arn=event_bus_arn)

        return typing.cast(None, jsii.invoke(self, "putEventBridgeConfig", [value]))

    @jsii.member(jsii_name="putHttpConfig")
    def put_http_config(
        self,
        *,
        endpoint: builtins.str,
        authorization_config: typing.Optional[typing.Union["AppsyncDatasourceHttpConfigAuthorizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.
        :param authorization_config: authorization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#authorization_config AppsyncDatasource#authorization_config}
        '''
        value = AppsyncDatasourceHttpConfig(
            endpoint=endpoint, authorization_config=authorization_config
        )

        return typing.cast(None, jsii.invoke(self, "putHttpConfig", [value]))

    @jsii.member(jsii_name="putLambdaConfig")
    def put_lambda_config(self, *, function_arn: builtins.str) -> None:
        '''
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#function_arn AppsyncDatasource#function_arn}.
        '''
        value = AppsyncDatasourceLambdaConfig(function_arn=function_arn)

        return typing.cast(None, jsii.invoke(self, "putLambdaConfig", [value]))

    @jsii.member(jsii_name="putOpensearchserviceConfig")
    def put_opensearchservice_config(
        self,
        *,
        endpoint: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.
        '''
        value = AppsyncDatasourceOpensearchserviceConfig(
            endpoint=endpoint, region=region
        )

        return typing.cast(None, jsii.invoke(self, "putOpensearchserviceConfig", [value]))

    @jsii.member(jsii_name="putRelationalDatabaseConfig")
    def put_relational_database_config(
        self,
        *,
        http_endpoint_config: typing.Optional[typing.Union["AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        source_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_endpoint_config: http_endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#http_endpoint_config AppsyncDatasource#http_endpoint_config}
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#source_type AppsyncDatasource#source_type}.
        '''
        value = AppsyncDatasourceRelationalDatabaseConfig(
            http_endpoint_config=http_endpoint_config, source_type=source_type
        )

        return typing.cast(None, jsii.invoke(self, "putRelationalDatabaseConfig", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamodbConfig")
    def reset_dynamodb_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbConfig", []))

    @jsii.member(jsii_name="resetElasticsearchConfig")
    def reset_elasticsearch_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearchConfig", []))

    @jsii.member(jsii_name="resetEventBridgeConfig")
    def reset_event_bridge_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventBridgeConfig", []))

    @jsii.member(jsii_name="resetHttpConfig")
    def reset_http_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLambdaConfig")
    def reset_lambda_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambdaConfig", []))

    @jsii.member(jsii_name="resetOpensearchserviceConfig")
    def reset_opensearchservice_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpensearchserviceConfig", []))

    @jsii.member(jsii_name="resetRelationalDatabaseConfig")
    def reset_relational_database_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelationalDatabaseConfig", []))

    @jsii.member(jsii_name="resetServiceRoleArn")
    def reset_service_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRoleArn", []))

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
    @jsii.member(jsii_name="dynamodbConfig")
    def dynamodb_config(self) -> "AppsyncDatasourceDynamodbConfigOutputReference":
        return typing.cast("AppsyncDatasourceDynamodbConfigOutputReference", jsii.get(self, "dynamodbConfig"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchConfig")
    def elasticsearch_config(
        self,
    ) -> "AppsyncDatasourceElasticsearchConfigOutputReference":
        return typing.cast("AppsyncDatasourceElasticsearchConfigOutputReference", jsii.get(self, "elasticsearchConfig"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeConfig")
    def event_bridge_config(
        self,
    ) -> "AppsyncDatasourceEventBridgeConfigOutputReference":
        return typing.cast("AppsyncDatasourceEventBridgeConfigOutputReference", jsii.get(self, "eventBridgeConfig"))

    @builtins.property
    @jsii.member(jsii_name="httpConfig")
    def http_config(self) -> "AppsyncDatasourceHttpConfigOutputReference":
        return typing.cast("AppsyncDatasourceHttpConfigOutputReference", jsii.get(self, "httpConfig"))

    @builtins.property
    @jsii.member(jsii_name="lambdaConfig")
    def lambda_config(self) -> "AppsyncDatasourceLambdaConfigOutputReference":
        return typing.cast("AppsyncDatasourceLambdaConfigOutputReference", jsii.get(self, "lambdaConfig"))

    @builtins.property
    @jsii.member(jsii_name="opensearchserviceConfig")
    def opensearchservice_config(
        self,
    ) -> "AppsyncDatasourceOpensearchserviceConfigOutputReference":
        return typing.cast("AppsyncDatasourceOpensearchserviceConfigOutputReference", jsii.get(self, "opensearchserviceConfig"))

    @builtins.property
    @jsii.member(jsii_name="relationalDatabaseConfig")
    def relational_database_config(
        self,
    ) -> "AppsyncDatasourceRelationalDatabaseConfigOutputReference":
        return typing.cast("AppsyncDatasourceRelationalDatabaseConfigOutputReference", jsii.get(self, "relationalDatabaseConfig"))

    @builtins.property
    @jsii.member(jsii_name="apiIdInput")
    def api_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbConfigInput")
    def dynamodb_config_input(
        self,
    ) -> typing.Optional["AppsyncDatasourceDynamodbConfig"]:
        return typing.cast(typing.Optional["AppsyncDatasourceDynamodbConfig"], jsii.get(self, "dynamodbConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchConfigInput")
    def elasticsearch_config_input(
        self,
    ) -> typing.Optional["AppsyncDatasourceElasticsearchConfig"]:
        return typing.cast(typing.Optional["AppsyncDatasourceElasticsearchConfig"], jsii.get(self, "elasticsearchConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBridgeConfigInput")
    def event_bridge_config_input(
        self,
    ) -> typing.Optional["AppsyncDatasourceEventBridgeConfig"]:
        return typing.cast(typing.Optional["AppsyncDatasourceEventBridgeConfig"], jsii.get(self, "eventBridgeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="httpConfigInput")
    def http_config_input(self) -> typing.Optional["AppsyncDatasourceHttpConfig"]:
        return typing.cast(typing.Optional["AppsyncDatasourceHttpConfig"], jsii.get(self, "httpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaConfigInput")
    def lambda_config_input(self) -> typing.Optional["AppsyncDatasourceLambdaConfig"]:
        return typing.cast(typing.Optional["AppsyncDatasourceLambdaConfig"], jsii.get(self, "lambdaConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="opensearchserviceConfigInput")
    def opensearchservice_config_input(
        self,
    ) -> typing.Optional["AppsyncDatasourceOpensearchserviceConfig"]:
        return typing.cast(typing.Optional["AppsyncDatasourceOpensearchserviceConfig"], jsii.get(self, "opensearchserviceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="relationalDatabaseConfigInput")
    def relational_database_config_input(
        self,
    ) -> typing.Optional["AppsyncDatasourceRelationalDatabaseConfig"]:
        return typing.cast(typing.Optional["AppsyncDatasourceRelationalDatabaseConfig"], jsii.get(self, "relationalDatabaseConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArnInput")
    def service_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiId"))

    @api_id.setter
    def api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b2a87497ab1789a2071f32120a91ad409823c35c2326a59221592efc855f2c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba247b620626d335906999b18eb2ba9297730db7a951cee57ab34024ac0ed5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac3a8dca914d989af223b96ba590517842a158fe27d7130316816b4f61c8658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7b043f214db5173fd13c8e2c66576d2bb8e59b87e3ea5622e2633494d59d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7b9220089cc177dfce7b3f0850c73fffc449583a7a29d33596d2da7f2bd09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd80e636a6a1693d26375ef23c33f20c66b9f45201a11b87ebd2f12a904cf6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_id": "apiId",
        "name": "name",
        "type": "type",
        "description": "description",
        "dynamodb_config": "dynamodbConfig",
        "elasticsearch_config": "elasticsearchConfig",
        "event_bridge_config": "eventBridgeConfig",
        "http_config": "httpConfig",
        "id": "id",
        "lambda_config": "lambdaConfig",
        "opensearchservice_config": "opensearchserviceConfig",
        "relational_database_config": "relationalDatabaseConfig",
        "service_role_arn": "serviceRoleArn",
    },
)
class AppsyncDatasourceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        dynamodb_config: typing.Optional[typing.Union["AppsyncDatasourceDynamodbConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch_config: typing.Optional[typing.Union["AppsyncDatasourceElasticsearchConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        event_bridge_config: typing.Optional[typing.Union["AppsyncDatasourceEventBridgeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        http_config: typing.Optional[typing.Union["AppsyncDatasourceHttpConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        lambda_config: typing.Optional[typing.Union["AppsyncDatasourceLambdaConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        opensearchservice_config: typing.Optional[typing.Union["AppsyncDatasourceOpensearchserviceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        relational_database_config: typing.Optional[typing.Union["AppsyncDatasourceRelationalDatabaseConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#api_id AppsyncDatasource#api_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#name AppsyncDatasource#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#type AppsyncDatasource#type}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#description AppsyncDatasource#description}.
        :param dynamodb_config: dynamodb_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#dynamodb_config AppsyncDatasource#dynamodb_config}
        :param elasticsearch_config: elasticsearch_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#elasticsearch_config AppsyncDatasource#elasticsearch_config}
        :param event_bridge_config: event_bridge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#event_bridge_config AppsyncDatasource#event_bridge_config}
        :param http_config: http_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#http_config AppsyncDatasource#http_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#id AppsyncDatasource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lambda_config: lambda_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#lambda_config AppsyncDatasource#lambda_config}
        :param opensearchservice_config: opensearchservice_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#opensearchservice_config AppsyncDatasource#opensearchservice_config}
        :param relational_database_config: relational_database_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#relational_database_config AppsyncDatasource#relational_database_config}
        :param service_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#service_role_arn AppsyncDatasource#service_role_arn}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dynamodb_config, dict):
            dynamodb_config = AppsyncDatasourceDynamodbConfig(**dynamodb_config)
        if isinstance(elasticsearch_config, dict):
            elasticsearch_config = AppsyncDatasourceElasticsearchConfig(**elasticsearch_config)
        if isinstance(event_bridge_config, dict):
            event_bridge_config = AppsyncDatasourceEventBridgeConfig(**event_bridge_config)
        if isinstance(http_config, dict):
            http_config = AppsyncDatasourceHttpConfig(**http_config)
        if isinstance(lambda_config, dict):
            lambda_config = AppsyncDatasourceLambdaConfig(**lambda_config)
        if isinstance(opensearchservice_config, dict):
            opensearchservice_config = AppsyncDatasourceOpensearchserviceConfig(**opensearchservice_config)
        if isinstance(relational_database_config, dict):
            relational_database_config = AppsyncDatasourceRelationalDatabaseConfig(**relational_database_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85072a5f3b388aa955362c74f3807ce118c6b00e26bb1e7ab37fdcfa74d59f31)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_id", value=api_id, expected_type=type_hints["api_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamodb_config", value=dynamodb_config, expected_type=type_hints["dynamodb_config"])
            check_type(argname="argument elasticsearch_config", value=elasticsearch_config, expected_type=type_hints["elasticsearch_config"])
            check_type(argname="argument event_bridge_config", value=event_bridge_config, expected_type=type_hints["event_bridge_config"])
            check_type(argname="argument http_config", value=http_config, expected_type=type_hints["http_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lambda_config", value=lambda_config, expected_type=type_hints["lambda_config"])
            check_type(argname="argument opensearchservice_config", value=opensearchservice_config, expected_type=type_hints["opensearchservice_config"])
            check_type(argname="argument relational_database_config", value=relational_database_config, expected_type=type_hints["relational_database_config"])
            check_type(argname="argument service_role_arn", value=service_role_arn, expected_type=type_hints["service_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_id": api_id,
            "name": name,
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
        if description is not None:
            self._values["description"] = description
        if dynamodb_config is not None:
            self._values["dynamodb_config"] = dynamodb_config
        if elasticsearch_config is not None:
            self._values["elasticsearch_config"] = elasticsearch_config
        if event_bridge_config is not None:
            self._values["event_bridge_config"] = event_bridge_config
        if http_config is not None:
            self._values["http_config"] = http_config
        if id is not None:
            self._values["id"] = id
        if lambda_config is not None:
            self._values["lambda_config"] = lambda_config
        if opensearchservice_config is not None:
            self._values["opensearchservice_config"] = opensearchservice_config
        if relational_database_config is not None:
            self._values["relational_database_config"] = relational_database_config
        if service_role_arn is not None:
            self._values["service_role_arn"] = service_role_arn

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
    def api_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#api_id AppsyncDatasource#api_id}.'''
        result = self._values.get("api_id")
        assert result is not None, "Required property 'api_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#name AppsyncDatasource#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#type AppsyncDatasource#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#description AppsyncDatasource#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb_config(self) -> typing.Optional["AppsyncDatasourceDynamodbConfig"]:
        '''dynamodb_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#dynamodb_config AppsyncDatasource#dynamodb_config}
        '''
        result = self._values.get("dynamodb_config")
        return typing.cast(typing.Optional["AppsyncDatasourceDynamodbConfig"], result)

    @builtins.property
    def elasticsearch_config(
        self,
    ) -> typing.Optional["AppsyncDatasourceElasticsearchConfig"]:
        '''elasticsearch_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#elasticsearch_config AppsyncDatasource#elasticsearch_config}
        '''
        result = self._values.get("elasticsearch_config")
        return typing.cast(typing.Optional["AppsyncDatasourceElasticsearchConfig"], result)

    @builtins.property
    def event_bridge_config(
        self,
    ) -> typing.Optional["AppsyncDatasourceEventBridgeConfig"]:
        '''event_bridge_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#event_bridge_config AppsyncDatasource#event_bridge_config}
        '''
        result = self._values.get("event_bridge_config")
        return typing.cast(typing.Optional["AppsyncDatasourceEventBridgeConfig"], result)

    @builtins.property
    def http_config(self) -> typing.Optional["AppsyncDatasourceHttpConfig"]:
        '''http_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#http_config AppsyncDatasource#http_config}
        '''
        result = self._values.get("http_config")
        return typing.cast(typing.Optional["AppsyncDatasourceHttpConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#id AppsyncDatasource#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_config(self) -> typing.Optional["AppsyncDatasourceLambdaConfig"]:
        '''lambda_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#lambda_config AppsyncDatasource#lambda_config}
        '''
        result = self._values.get("lambda_config")
        return typing.cast(typing.Optional["AppsyncDatasourceLambdaConfig"], result)

    @builtins.property
    def opensearchservice_config(
        self,
    ) -> typing.Optional["AppsyncDatasourceOpensearchserviceConfig"]:
        '''opensearchservice_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#opensearchservice_config AppsyncDatasource#opensearchservice_config}
        '''
        result = self._values.get("opensearchservice_config")
        return typing.cast(typing.Optional["AppsyncDatasourceOpensearchserviceConfig"], result)

    @builtins.property
    def relational_database_config(
        self,
    ) -> typing.Optional["AppsyncDatasourceRelationalDatabaseConfig"]:
        '''relational_database_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#relational_database_config AppsyncDatasource#relational_database_config}
        '''
        result = self._values.get("relational_database_config")
        return typing.cast(typing.Optional["AppsyncDatasourceRelationalDatabaseConfig"], result)

    @builtins.property
    def service_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#service_role_arn AppsyncDatasource#service_role_arn}.'''
        result = self._values.get("service_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceDynamodbConfig",
    jsii_struct_bases=[],
    name_mapping={
        "table_name": "tableName",
        "delta_sync_config": "deltaSyncConfig",
        "region": "region",
        "use_caller_credentials": "useCallerCredentials",
        "versioned": "versioned",
    },
)
class AppsyncDatasourceDynamodbConfig:
    def __init__(
        self,
        *,
        table_name: builtins.str,
        delta_sync_config: typing.Optional[typing.Union["AppsyncDatasourceDynamodbConfigDeltaSyncConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        use_caller_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        versioned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#table_name AppsyncDatasource#table_name}.
        :param delta_sync_config: delta_sync_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_config AppsyncDatasource#delta_sync_config}
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.
        :param use_caller_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#use_caller_credentials AppsyncDatasource#use_caller_credentials}.
        :param versioned: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#versioned AppsyncDatasource#versioned}.
        '''
        if isinstance(delta_sync_config, dict):
            delta_sync_config = AppsyncDatasourceDynamodbConfigDeltaSyncConfig(**delta_sync_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845663e4d45e64a575753b699c41449d1041070efd8a678c01fc7ab151b4422c)
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument delta_sync_config", value=delta_sync_config, expected_type=type_hints["delta_sync_config"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument use_caller_credentials", value=use_caller_credentials, expected_type=type_hints["use_caller_credentials"])
            check_type(argname="argument versioned", value=versioned, expected_type=type_hints["versioned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_name": table_name,
        }
        if delta_sync_config is not None:
            self._values["delta_sync_config"] = delta_sync_config
        if region is not None:
            self._values["region"] = region
        if use_caller_credentials is not None:
            self._values["use_caller_credentials"] = use_caller_credentials
        if versioned is not None:
            self._values["versioned"] = versioned

    @builtins.property
    def table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#table_name AppsyncDatasource#table_name}.'''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delta_sync_config(
        self,
    ) -> typing.Optional["AppsyncDatasourceDynamodbConfigDeltaSyncConfig"]:
        '''delta_sync_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_config AppsyncDatasource#delta_sync_config}
        '''
        result = self._values.get("delta_sync_config")
        return typing.cast(typing.Optional["AppsyncDatasourceDynamodbConfigDeltaSyncConfig"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_caller_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#use_caller_credentials AppsyncDatasource#use_caller_credentials}.'''
        result = self._values.get("use_caller_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def versioned(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#versioned AppsyncDatasource#versioned}.'''
        result = self._values.get("versioned")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceDynamodbConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceDynamodbConfigDeltaSyncConfig",
    jsii_struct_bases=[],
    name_mapping={
        "delta_sync_table_name": "deltaSyncTableName",
        "base_table_ttl": "baseTableTtl",
        "delta_sync_table_ttl": "deltaSyncTableTtl",
    },
)
class AppsyncDatasourceDynamodbConfigDeltaSyncConfig:
    def __init__(
        self,
        *,
        delta_sync_table_name: builtins.str,
        base_table_ttl: typing.Optional[jsii.Number] = None,
        delta_sync_table_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delta_sync_table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_table_name AppsyncDatasource#delta_sync_table_name}.
        :param base_table_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#base_table_ttl AppsyncDatasource#base_table_ttl}.
        :param delta_sync_table_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_table_ttl AppsyncDatasource#delta_sync_table_ttl}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1924bcc98de6fceee508d3d10c950b9fbcb52d2cc0512bff033eb1e9107b8479)
            check_type(argname="argument delta_sync_table_name", value=delta_sync_table_name, expected_type=type_hints["delta_sync_table_name"])
            check_type(argname="argument base_table_ttl", value=base_table_ttl, expected_type=type_hints["base_table_ttl"])
            check_type(argname="argument delta_sync_table_ttl", value=delta_sync_table_ttl, expected_type=type_hints["delta_sync_table_ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delta_sync_table_name": delta_sync_table_name,
        }
        if base_table_ttl is not None:
            self._values["base_table_ttl"] = base_table_ttl
        if delta_sync_table_ttl is not None:
            self._values["delta_sync_table_ttl"] = delta_sync_table_ttl

    @builtins.property
    def delta_sync_table_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_table_name AppsyncDatasource#delta_sync_table_name}.'''
        result = self._values.get("delta_sync_table_name")
        assert result is not None, "Required property 'delta_sync_table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base_table_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#base_table_ttl AppsyncDatasource#base_table_ttl}.'''
        result = self._values.get("base_table_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delta_sync_table_ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_table_ttl AppsyncDatasource#delta_sync_table_ttl}.'''
        result = self._values.get("delta_sync_table_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceDynamodbConfigDeltaSyncConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncDatasourceDynamodbConfigDeltaSyncConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceDynamodbConfigDeltaSyncConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94412613450241dc1f765632a4b3390a8ce4ca7eb2a3bff63857020193a3d2bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBaseTableTtl")
    def reset_base_table_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseTableTtl", []))

    @jsii.member(jsii_name="resetDeltaSyncTableTtl")
    def reset_delta_sync_table_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeltaSyncTableTtl", []))

    @builtins.property
    @jsii.member(jsii_name="baseTableTtlInput")
    def base_table_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "baseTableTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="deltaSyncTableNameInput")
    def delta_sync_table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deltaSyncTableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deltaSyncTableTtlInput")
    def delta_sync_table_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deltaSyncTableTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="baseTableTtl")
    def base_table_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "baseTableTtl"))

    @base_table_ttl.setter
    def base_table_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ff54fcd761c3fb7a9facf31bd2840a72d6c8ba55d0258415525851048afd93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseTableTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deltaSyncTableName")
    def delta_sync_table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deltaSyncTableName"))

    @delta_sync_table_name.setter
    def delta_sync_table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5597e28eafe95ffe9e83b4b9e44024725d32f56ac7b87f361c9054c19254fcb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deltaSyncTableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deltaSyncTableTtl")
    def delta_sync_table_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deltaSyncTableTtl"))

    @delta_sync_table_ttl.setter
    def delta_sync_table_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__043578821b0ffa102bde817b76963571bb82e9ef8875fdfdaa2d7b561521d8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deltaSyncTableTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncDatasourceDynamodbConfigDeltaSyncConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceDynamodbConfigDeltaSyncConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceDynamodbConfigDeltaSyncConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997f6a2091eddeaac3c7a5da6f50f9c124b27123216e419ac6cc19f221e466ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncDatasourceDynamodbConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceDynamodbConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81dfca5042d9cd6d07320d2f0636942e65e147dbf53c207e162db847186fc434)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDeltaSyncConfig")
    def put_delta_sync_config(
        self,
        *,
        delta_sync_table_name: builtins.str,
        base_table_ttl: typing.Optional[jsii.Number] = None,
        delta_sync_table_ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delta_sync_table_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_table_name AppsyncDatasource#delta_sync_table_name}.
        :param base_table_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#base_table_ttl AppsyncDatasource#base_table_ttl}.
        :param delta_sync_table_ttl: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#delta_sync_table_ttl AppsyncDatasource#delta_sync_table_ttl}.
        '''
        value = AppsyncDatasourceDynamodbConfigDeltaSyncConfig(
            delta_sync_table_name=delta_sync_table_name,
            base_table_ttl=base_table_ttl,
            delta_sync_table_ttl=delta_sync_table_ttl,
        )

        return typing.cast(None, jsii.invoke(self, "putDeltaSyncConfig", [value]))

    @jsii.member(jsii_name="resetDeltaSyncConfig")
    def reset_delta_sync_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeltaSyncConfig", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetUseCallerCredentials")
    def reset_use_caller_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCallerCredentials", []))

    @jsii.member(jsii_name="resetVersioned")
    def reset_versioned(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersioned", []))

    @builtins.property
    @jsii.member(jsii_name="deltaSyncConfig")
    def delta_sync_config(
        self,
    ) -> AppsyncDatasourceDynamodbConfigDeltaSyncConfigOutputReference:
        return typing.cast(AppsyncDatasourceDynamodbConfigDeltaSyncConfigOutputReference, jsii.get(self, "deltaSyncConfig"))

    @builtins.property
    @jsii.member(jsii_name="deltaSyncConfigInput")
    def delta_sync_config_input(
        self,
    ) -> typing.Optional[AppsyncDatasourceDynamodbConfigDeltaSyncConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceDynamodbConfigDeltaSyncConfig], jsii.get(self, "deltaSyncConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tableNameInput")
    def table_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="useCallerCredentialsInput")
    def use_caller_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCallerCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionedInput")
    def versioned_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "versionedInput"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b88aa6e84220e91bf455f47f4e3d9626f4c6043c7db369ce93d13b2e1b33edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a793747ad21b2d71c6959f626870080d968817cbf4e2d0b5e159aa6807e09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCallerCredentials")
    def use_caller_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCallerCredentials"))

    @use_caller_credentials.setter
    def use_caller_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e8c52dd2a00a5502e4928ddf8330ddd8b3d7127f7a96b0675b697539f4a5af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCallerCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versioned")
    def versioned(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "versioned"))

    @versioned.setter
    def versioned(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e399cc5c8d55aaeee6f7f93a0f95482b35eb4988d36b6f387e783288d78e02a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versioned", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncDatasourceDynamodbConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceDynamodbConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceDynamodbConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89af89d516f17fb903ca0ceb864a0b3fb798e1077e0a0d7dcf91c8432d46163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceElasticsearchConfig",
    jsii_struct_bases=[],
    name_mapping={"endpoint": "endpoint", "region": "region"},
)
class AppsyncDatasourceElasticsearchConfig:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1749087fe8a88236fcc687ab886b2af599e6efbf97f02a073072434b1170228c)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.'''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceElasticsearchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncDatasourceElasticsearchConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceElasticsearchConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ea4ede3fb150111d12526085a9cc83e8bef7c9758edc30fb109e7544dad45c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692fb6f82dc40800c72d198c652ad5bc728ca28bf9d1a1178bed08dab51c790f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296708711247623ca7cd7efee8340705fddf580ca39d5d58449d5674580dbedb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncDatasourceElasticsearchConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceElasticsearchConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceElasticsearchConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739d98ec8b1f35edaf7eb2fc8c6b379c663581a3a6994dbadef622b4b4a4658b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceEventBridgeConfig",
    jsii_struct_bases=[],
    name_mapping={"event_bus_arn": "eventBusArn"},
)
class AppsyncDatasourceEventBridgeConfig:
    def __init__(self, *, event_bus_arn: builtins.str) -> None:
        '''
        :param event_bus_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#event_bus_arn AppsyncDatasource#event_bus_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28360f76ae0351eaf03691885130f58b01d023989a7b76a442c3a255361cb604)
            check_type(argname="argument event_bus_arn", value=event_bus_arn, expected_type=type_hints["event_bus_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_bus_arn": event_bus_arn,
        }

    @builtins.property
    def event_bus_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#event_bus_arn AppsyncDatasource#event_bus_arn}.'''
        result = self._values.get("event_bus_arn")
        assert result is not None, "Required property 'event_bus_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceEventBridgeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncDatasourceEventBridgeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceEventBridgeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b9f580206f1c419534e750e5cdab64806e7c0a432db95e75928f1aa713fffcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="eventBusArnInput")
    def event_bus_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventBusArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBusArn")
    def event_bus_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventBusArn"))

    @event_bus_arn.setter
    def event_bus_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08c623f369f7bdba22770552395e51cfd154ccb6aa3211714f00a76d72d860f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBusArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncDatasourceEventBridgeConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceEventBridgeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceEventBridgeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb7ea6aaac6d4e4a65f7e4f409eafd006d792cf4b0e2b3234a4c5de0c6394e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceHttpConfig",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "authorization_config": "authorizationConfig",
    },
)
class AppsyncDatasourceHttpConfig:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        authorization_config: typing.Optional[typing.Union["AppsyncDatasourceHttpConfigAuthorizationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.
        :param authorization_config: authorization_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#authorization_config AppsyncDatasource#authorization_config}
        '''
        if isinstance(authorization_config, dict):
            authorization_config = AppsyncDatasourceHttpConfigAuthorizationConfig(**authorization_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f46d93d156528a693c8377bc8eea886f9b169779fae1ebe6f646a1448bc3ac2)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument authorization_config", value=authorization_config, expected_type=type_hints["authorization_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
        }
        if authorization_config is not None:
            self._values["authorization_config"] = authorization_config

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.'''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization_config(
        self,
    ) -> typing.Optional["AppsyncDatasourceHttpConfigAuthorizationConfig"]:
        '''authorization_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#authorization_config AppsyncDatasource#authorization_config}
        '''
        result = self._values.get("authorization_config")
        return typing.cast(typing.Optional["AppsyncDatasourceHttpConfigAuthorizationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceHttpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceHttpConfigAuthorizationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_type": "authorizationType",
        "aws_iam_config": "awsIamConfig",
    },
)
class AppsyncDatasourceHttpConfigAuthorizationConfig:
    def __init__(
        self,
        *,
        authorization_type: typing.Optional[builtins.str] = None,
        aws_iam_config: typing.Optional[typing.Union["AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#authorization_type AppsyncDatasource#authorization_type}.
        :param aws_iam_config: aws_iam_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#aws_iam_config AppsyncDatasource#aws_iam_config}
        '''
        if isinstance(aws_iam_config, dict):
            aws_iam_config = AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig(**aws_iam_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f11c7488258172e350cb7100191e9eda8fb177a732fa592ae05038cebf9da35)
            check_type(argname="argument authorization_type", value=authorization_type, expected_type=type_hints["authorization_type"])
            check_type(argname="argument aws_iam_config", value=aws_iam_config, expected_type=type_hints["aws_iam_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization_type is not None:
            self._values["authorization_type"] = authorization_type
        if aws_iam_config is not None:
            self._values["aws_iam_config"] = aws_iam_config

    @builtins.property
    def authorization_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#authorization_type AppsyncDatasource#authorization_type}.'''
        result = self._values.get("authorization_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_iam_config(
        self,
    ) -> typing.Optional["AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig"]:
        '''aws_iam_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#aws_iam_config AppsyncDatasource#aws_iam_config}
        '''
        result = self._values.get("aws_iam_config")
        return typing.cast(typing.Optional["AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceHttpConfigAuthorizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig",
    jsii_struct_bases=[],
    name_mapping={
        "signing_region": "signingRegion",
        "signing_service_name": "signingServiceName",
    },
)
class AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig:
    def __init__(
        self,
        *,
        signing_region: typing.Optional[builtins.str] = None,
        signing_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param signing_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#signing_region AppsyncDatasource#signing_region}.
        :param signing_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#signing_service_name AppsyncDatasource#signing_service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d885822cce22b57119de621793889f409416712ec87bad25f553ca3b1c14c38e)
            check_type(argname="argument signing_region", value=signing_region, expected_type=type_hints["signing_region"])
            check_type(argname="argument signing_service_name", value=signing_service_name, expected_type=type_hints["signing_service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if signing_region is not None:
            self._values["signing_region"] = signing_region
        if signing_service_name is not None:
            self._values["signing_service_name"] = signing_service_name

    @builtins.property
    def signing_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#signing_region AppsyncDatasource#signing_region}.'''
        result = self._values.get("signing_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signing_service_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#signing_service_name AppsyncDatasource#signing_service_name}.'''
        result = self._values.get("signing_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85cf37f379870fa9d1d3a63e8f568c02444e46efe9c53874f00e7fb2adb2e368)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSigningRegion")
    def reset_signing_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSigningRegion", []))

    @jsii.member(jsii_name="resetSigningServiceName")
    def reset_signing_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSigningServiceName", []))

    @builtins.property
    @jsii.member(jsii_name="signingRegionInput")
    def signing_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signingRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="signingServiceNameInput")
    def signing_service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "signingServiceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="signingRegion")
    def signing_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingRegion"))

    @signing_region.setter
    def signing_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d70e3356a1ce79eb873ecd2ca5ff407dca3b7da54e0294e918d380f3e1a3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingRegion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="signingServiceName")
    def signing_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signingServiceName"))

    @signing_service_name.setter
    def signing_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ad72a17e9b6319a396ddb2999c3674691987908716a5efd3da943dfe8e5b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signingServiceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b6963fdf967fc2761f1696218c0c77ba9d379da9ce55c1b93b7b30545bb0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncDatasourceHttpConfigAuthorizationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceHttpConfigAuthorizationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c6cb5bfa4cf9d9651b86ee7d0bd1f2521d90eb7f4b1ed542a0d82916556916a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAwsIamConfig")
    def put_aws_iam_config(
        self,
        *,
        signing_region: typing.Optional[builtins.str] = None,
        signing_service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param signing_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#signing_region AppsyncDatasource#signing_region}.
        :param signing_service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#signing_service_name AppsyncDatasource#signing_service_name}.
        '''
        value = AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig(
            signing_region=signing_region, signing_service_name=signing_service_name
        )

        return typing.cast(None, jsii.invoke(self, "putAwsIamConfig", [value]))

    @jsii.member(jsii_name="resetAuthorizationType")
    def reset_authorization_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationType", []))

    @jsii.member(jsii_name="resetAwsIamConfig")
    def reset_aws_iam_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsIamConfig", []))

    @builtins.property
    @jsii.member(jsii_name="awsIamConfig")
    def aws_iam_config(
        self,
    ) -> AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfigOutputReference:
        return typing.cast(AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfigOutputReference, jsii.get(self, "awsIamConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizationTypeInput")
    def authorization_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="awsIamConfigInput")
    def aws_iam_config_input(
        self,
    ) -> typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig], jsii.get(self, "awsIamConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationType"))

    @authorization_type.setter
    def authorization_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e4183b97ba9650bc93db898e0e2f6c444479c17c6726ca2ad22efb684cd7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd8237b72394a4bad4495dd1d91b7c23e9d91515dcbf5054abe5c5d2d4273a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncDatasourceHttpConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceHttpConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ac04a8f8ff8f036d1892a8189b57ae2c476b10f9c66ff32a5b8a4829c85cb05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorizationConfig")
    def put_authorization_config(
        self,
        *,
        authorization_type: typing.Optional[builtins.str] = None,
        aws_iam_config: typing.Optional[typing.Union[AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param authorization_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#authorization_type AppsyncDatasource#authorization_type}.
        :param aws_iam_config: aws_iam_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#aws_iam_config AppsyncDatasource#aws_iam_config}
        '''
        value = AppsyncDatasourceHttpConfigAuthorizationConfig(
            authorization_type=authorization_type, aws_iam_config=aws_iam_config
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorizationConfig", [value]))

    @jsii.member(jsii_name="resetAuthorizationConfig")
    def reset_authorization_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="authorizationConfig")
    def authorization_config(
        self,
    ) -> AppsyncDatasourceHttpConfigAuthorizationConfigOutputReference:
        return typing.cast(AppsyncDatasourceHttpConfigAuthorizationConfigOutputReference, jsii.get(self, "authorizationConfig"))

    @builtins.property
    @jsii.member(jsii_name="authorizationConfigInput")
    def authorization_config_input(
        self,
    ) -> typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfig], jsii.get(self, "authorizationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a14915cb61f6769eef0de5633fb198413f6aff29987c03b18cfbda93ac8873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncDatasourceHttpConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceHttpConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceHttpConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2def9e09b979e7c52ea53f8d3ba5059cace1f1e1f33c66ddd9a77c37071019)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceLambdaConfig",
    jsii_struct_bases=[],
    name_mapping={"function_arn": "functionArn"},
)
class AppsyncDatasourceLambdaConfig:
    def __init__(self, *, function_arn: builtins.str) -> None:
        '''
        :param function_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#function_arn AppsyncDatasource#function_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b91ecbca2d1d0b958271d6cc33de56cb6575e0d02ba3fc5ca28440d89edd85f)
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_arn": function_arn,
        }

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#function_arn AppsyncDatasource#function_arn}.'''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceLambdaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncDatasourceLambdaConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceLambdaConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__732040c6cd21f3ed0088934419bf930e7bee26037326d2a9d921a246eb6f4f93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="functionArnInput")
    def function_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @function_arn.setter
    def function_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d654183a91778566a6636571df48972b58a0c845cedb593f4984434dd2494c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AppsyncDatasourceLambdaConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceLambdaConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceLambdaConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898d70018df02028f1657890631db05e3e1accec3d27457225a2b5b7671d8332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceOpensearchserviceConfig",
    jsii_struct_bases=[],
    name_mapping={"endpoint": "endpoint", "region": "region"},
)
class AppsyncDatasourceOpensearchserviceConfig:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f15f149824ce18016b007f1a5e0c35f0e58a0ed487cd638fd6569cb8c2a2c71)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
        }
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#endpoint AppsyncDatasource#endpoint}.'''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceOpensearchserviceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncDatasourceOpensearchserviceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceOpensearchserviceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6949b424be857cd11c45b5a82a872727368e93e4e5ac9c5774973864855ad4d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317c9fd54150d4cd7f38b44356aa655f8db9ccf0fed7f251e5c91e574dbc8710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee1128b13de420e3d0ade82978d0dd5e819d519773dc17b74b76520306bde2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncDatasourceOpensearchserviceConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceOpensearchserviceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceOpensearchserviceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de25d28b86d86960cae77a770fe104d27c349442523152136198bc19ed73153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceRelationalDatabaseConfig",
    jsii_struct_bases=[],
    name_mapping={
        "http_endpoint_config": "httpEndpointConfig",
        "source_type": "sourceType",
    },
)
class AppsyncDatasourceRelationalDatabaseConfig:
    def __init__(
        self,
        *,
        http_endpoint_config: typing.Optional[typing.Union["AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        source_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_endpoint_config: http_endpoint_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#http_endpoint_config AppsyncDatasource#http_endpoint_config}
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#source_type AppsyncDatasource#source_type}.
        '''
        if isinstance(http_endpoint_config, dict):
            http_endpoint_config = AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig(**http_endpoint_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__366421674bb2d1dfd8ec5c275e20f8a0491116964e2d35b53f1dba57eb6f24c3)
            check_type(argname="argument http_endpoint_config", value=http_endpoint_config, expected_type=type_hints["http_endpoint_config"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_endpoint_config is not None:
            self._values["http_endpoint_config"] = http_endpoint_config
        if source_type is not None:
            self._values["source_type"] = source_type

    @builtins.property
    def http_endpoint_config(
        self,
    ) -> typing.Optional["AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig"]:
        '''http_endpoint_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#http_endpoint_config AppsyncDatasource#http_endpoint_config}
        '''
        result = self._values.get("http_endpoint_config")
        return typing.cast(typing.Optional["AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig"], result)

    @builtins.property
    def source_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#source_type AppsyncDatasource#source_type}.'''
        result = self._values.get("source_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceRelationalDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aws_secret_store_arn": "awsSecretStoreArn",
        "db_cluster_identifier": "dbClusterIdentifier",
        "database_name": "databaseName",
        "region": "region",
        "schema": "schema",
    },
)
class AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig:
    def __init__(
        self,
        *,
        aws_secret_store_arn: builtins.str,
        db_cluster_identifier: builtins.str,
        database_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_secret_store_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#aws_secret_store_arn AppsyncDatasource#aws_secret_store_arn}.
        :param db_cluster_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#db_cluster_identifier AppsyncDatasource#db_cluster_identifier}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#database_name AppsyncDatasource#database_name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#schema AppsyncDatasource#schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31cb65a8494c167d25f1816d0cf20dd8904265cbbb8fdbb0035e9e18532b5b9)
            check_type(argname="argument aws_secret_store_arn", value=aws_secret_store_arn, expected_type=type_hints["aws_secret_store_arn"])
            check_type(argname="argument db_cluster_identifier", value=db_cluster_identifier, expected_type=type_hints["db_cluster_identifier"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_secret_store_arn": aws_secret_store_arn,
            "db_cluster_identifier": db_cluster_identifier,
        }
        if database_name is not None:
            self._values["database_name"] = database_name
        if region is not None:
            self._values["region"] = region
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def aws_secret_store_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#aws_secret_store_arn AppsyncDatasource#aws_secret_store_arn}.'''
        result = self._values.get("aws_secret_store_arn")
        assert result is not None, "Required property 'aws_secret_store_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_cluster_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#db_cluster_identifier AppsyncDatasource#db_cluster_identifier}.'''
        result = self._values.get("db_cluster_identifier")
        assert result is not None, "Required property 'db_cluster_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#database_name AppsyncDatasource#database_name}.'''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#schema AppsyncDatasource#schema}.'''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79b38d74228d5ced8b05ac0f08c60d63bd7c780300c02668b187373f620af04a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatabaseName")
    def reset_database_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="awsSecretStoreArnInput")
    def aws_secret_store_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsSecretStoreArnInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifierInput")
    def db_cluster_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbClusterIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="awsSecretStoreArn")
    def aws_secret_store_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsSecretStoreArn"))

    @aws_secret_store_arn.setter
    def aws_secret_store_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e0b08b9171d2d86b6e56e1363cd25c68fb29ee6d75b1d014bafcecfb54654b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsSecretStoreArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ea0cc75721836d76f41e59c092808fb60456ea10b7310db0d03fb19ce21773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbClusterIdentifier"))

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856de77f22da8d8abd577d9a0faeb3564faa81c95d930981023c1cc42c5f42bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbClusterIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bf1029689bd5b1c8b9c86be71a42dca08fe45d23e0b812919a7ad22c65d28ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914031431105ec8fbe342d62b4a026e550c96d9990e3b767af8100879e74e429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8ce73548e84bb80c6f4cdf316bdb98fdc621cb59ef98a7fadd23252e63fce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsyncDatasourceRelationalDatabaseConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.appsyncDatasource.AppsyncDatasourceRelationalDatabaseConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9c618b6625b036e0b0910b8721abdfe44468f89ed1e30109c87ba6aa148cd20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpEndpointConfig")
    def put_http_endpoint_config(
        self,
        *,
        aws_secret_store_arn: builtins.str,
        db_cluster_identifier: builtins.str,
        database_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_secret_store_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#aws_secret_store_arn AppsyncDatasource#aws_secret_store_arn}.
        :param db_cluster_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#db_cluster_identifier AppsyncDatasource#db_cluster_identifier}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#database_name AppsyncDatasource#database_name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#region AppsyncDatasource#region}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/appsync_datasource#schema AppsyncDatasource#schema}.
        '''
        value = AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig(
            aws_secret_store_arn=aws_secret_store_arn,
            db_cluster_identifier=db_cluster_identifier,
            database_name=database_name,
            region=region,
            schema=schema,
        )

        return typing.cast(None, jsii.invoke(self, "putHttpEndpointConfig", [value]))

    @jsii.member(jsii_name="resetHttpEndpointConfig")
    def reset_http_endpoint_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpEndpointConfig", []))

    @jsii.member(jsii_name="resetSourceType")
    def reset_source_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceType", []))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointConfig")
    def http_endpoint_config(
        self,
    ) -> AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfigOutputReference:
        return typing.cast(AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfigOutputReference, jsii.get(self, "httpEndpointConfig"))

    @builtins.property
    @jsii.member(jsii_name="httpEndpointConfigInput")
    def http_endpoint_config_input(
        self,
    ) -> typing.Optional[AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig], jsii.get(self, "httpEndpointConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e9cbff7d2e591e1346feaeb88736cd55e7da54dc199775a2f78ab12218bf8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AppsyncDatasourceRelationalDatabaseConfig]:
        return typing.cast(typing.Optional[AppsyncDatasourceRelationalDatabaseConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AppsyncDatasourceRelationalDatabaseConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12765a33dd6f1a82cc1be7e6e2609f9e49884b5184a2d02b6b3d15813b293c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppsyncDatasource",
    "AppsyncDatasourceConfig",
    "AppsyncDatasourceDynamodbConfig",
    "AppsyncDatasourceDynamodbConfigDeltaSyncConfig",
    "AppsyncDatasourceDynamodbConfigDeltaSyncConfigOutputReference",
    "AppsyncDatasourceDynamodbConfigOutputReference",
    "AppsyncDatasourceElasticsearchConfig",
    "AppsyncDatasourceElasticsearchConfigOutputReference",
    "AppsyncDatasourceEventBridgeConfig",
    "AppsyncDatasourceEventBridgeConfigOutputReference",
    "AppsyncDatasourceHttpConfig",
    "AppsyncDatasourceHttpConfigAuthorizationConfig",
    "AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig",
    "AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfigOutputReference",
    "AppsyncDatasourceHttpConfigAuthorizationConfigOutputReference",
    "AppsyncDatasourceHttpConfigOutputReference",
    "AppsyncDatasourceLambdaConfig",
    "AppsyncDatasourceLambdaConfigOutputReference",
    "AppsyncDatasourceOpensearchserviceConfig",
    "AppsyncDatasourceOpensearchserviceConfigOutputReference",
    "AppsyncDatasourceRelationalDatabaseConfig",
    "AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig",
    "AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfigOutputReference",
    "AppsyncDatasourceRelationalDatabaseConfigOutputReference",
]

publication.publish()

def _typecheckingstub__0d0e3ba9433a03f5777389f2ac83f22977d1b7b4d00a0bfdd983275937f193d3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dynamodb_config: typing.Optional[typing.Union[AppsyncDatasourceDynamodbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticsearch_config: typing.Optional[typing.Union[AppsyncDatasourceElasticsearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    event_bridge_config: typing.Optional[typing.Union[AppsyncDatasourceEventBridgeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    http_config: typing.Optional[typing.Union[AppsyncDatasourceHttpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    lambda_config: typing.Optional[typing.Union[AppsyncDatasourceLambdaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    opensearchservice_config: typing.Optional[typing.Union[AppsyncDatasourceOpensearchserviceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    relational_database_config: typing.Optional[typing.Union[AppsyncDatasourceRelationalDatabaseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__2f095d31deb30fe692c3247ca8610fb3c3aed0752198d6ab3199552e2a2f5881(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b2a87497ab1789a2071f32120a91ad409823c35c2326a59221592efc855f2c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba247b620626d335906999b18eb2ba9297730db7a951cee57ab34024ac0ed5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac3a8dca914d989af223b96ba590517842a158fe27d7130316816b4f61c8658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7b043f214db5173fd13c8e2c66576d2bb8e59b87e3ea5622e2633494d59d89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7b9220089cc177dfce7b3f0850c73fffc449583a7a29d33596d2da7f2bd09c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd80e636a6a1693d26375ef23c33f20c66b9f45201a11b87ebd2f12a904cf6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85072a5f3b388aa955362c74f3807ce118c6b00e26bb1e7ab37fdcfa74d59f31(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    dynamodb_config: typing.Optional[typing.Union[AppsyncDatasourceDynamodbConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticsearch_config: typing.Optional[typing.Union[AppsyncDatasourceElasticsearchConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    event_bridge_config: typing.Optional[typing.Union[AppsyncDatasourceEventBridgeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    http_config: typing.Optional[typing.Union[AppsyncDatasourceHttpConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    lambda_config: typing.Optional[typing.Union[AppsyncDatasourceLambdaConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    opensearchservice_config: typing.Optional[typing.Union[AppsyncDatasourceOpensearchserviceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    relational_database_config: typing.Optional[typing.Union[AppsyncDatasourceRelationalDatabaseConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845663e4d45e64a575753b699c41449d1041070efd8a678c01fc7ab151b4422c(
    *,
    table_name: builtins.str,
    delta_sync_config: typing.Optional[typing.Union[AppsyncDatasourceDynamodbConfigDeltaSyncConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    use_caller_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    versioned: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1924bcc98de6fceee508d3d10c950b9fbcb52d2cc0512bff033eb1e9107b8479(
    *,
    delta_sync_table_name: builtins.str,
    base_table_ttl: typing.Optional[jsii.Number] = None,
    delta_sync_table_ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94412613450241dc1f765632a4b3390a8ce4ca7eb2a3bff63857020193a3d2bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ff54fcd761c3fb7a9facf31bd2840a72d6c8ba55d0258415525851048afd93(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5597e28eafe95ffe9e83b4b9e44024725d32f56ac7b87f361c9054c19254fcb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043578821b0ffa102bde817b76963571bb82e9ef8875fdfdaa2d7b561521d8bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997f6a2091eddeaac3c7a5da6f50f9c124b27123216e419ac6cc19f221e466ff(
    value: typing.Optional[AppsyncDatasourceDynamodbConfigDeltaSyncConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81dfca5042d9cd6d07320d2f0636942e65e147dbf53c207e162db847186fc434(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b88aa6e84220e91bf455f47f4e3d9626f4c6043c7db369ce93d13b2e1b33edb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a793747ad21b2d71c6959f626870080d968817cbf4e2d0b5e159aa6807e09c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e8c52dd2a00a5502e4928ddf8330ddd8b3d7127f7a96b0675b697539f4a5af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e399cc5c8d55aaeee6f7f93a0f95482b35eb4988d36b6f387e783288d78e02a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89af89d516f17fb903ca0ceb864a0b3fb798e1077e0a0d7dcf91c8432d46163(
    value: typing.Optional[AppsyncDatasourceDynamodbConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1749087fe8a88236fcc687ab886b2af599e6efbf97f02a073072434b1170228c(
    *,
    endpoint: builtins.str,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea4ede3fb150111d12526085a9cc83e8bef7c9758edc30fb109e7544dad45c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692fb6f82dc40800c72d198c652ad5bc728ca28bf9d1a1178bed08dab51c790f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296708711247623ca7cd7efee8340705fddf580ca39d5d58449d5674580dbedb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739d98ec8b1f35edaf7eb2fc8c6b379c663581a3a6994dbadef622b4b4a4658b(
    value: typing.Optional[AppsyncDatasourceElasticsearchConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28360f76ae0351eaf03691885130f58b01d023989a7b76a442c3a255361cb604(
    *,
    event_bus_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9f580206f1c419534e750e5cdab64806e7c0a432db95e75928f1aa713fffcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08c623f369f7bdba22770552395e51cfd154ccb6aa3211714f00a76d72d860f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb7ea6aaac6d4e4a65f7e4f409eafd006d792cf4b0e2b3234a4c5de0c6394e8(
    value: typing.Optional[AppsyncDatasourceEventBridgeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f46d93d156528a693c8377bc8eea886f9b169779fae1ebe6f646a1448bc3ac2(
    *,
    endpoint: builtins.str,
    authorization_config: typing.Optional[typing.Union[AppsyncDatasourceHttpConfigAuthorizationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f11c7488258172e350cb7100191e9eda8fb177a732fa592ae05038cebf9da35(
    *,
    authorization_type: typing.Optional[builtins.str] = None,
    aws_iam_config: typing.Optional[typing.Union[AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d885822cce22b57119de621793889f409416712ec87bad25f553ca3b1c14c38e(
    *,
    signing_region: typing.Optional[builtins.str] = None,
    signing_service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cf37f379870fa9d1d3a63e8f568c02444e46efe9c53874f00e7fb2adb2e368(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d70e3356a1ce79eb873ecd2ca5ff407dca3b7da54e0294e918d380f3e1a3f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ad72a17e9b6319a396ddb2999c3674691987908716a5efd3da943dfe8e5b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b6963fdf967fc2761f1696218c0c77ba9d379da9ce55c1b93b7b30545bb0af(
    value: typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfigAwsIamConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6cb5bfa4cf9d9651b86ee7d0bd1f2521d90eb7f4b1ed542a0d82916556916a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e4183b97ba9650bc93db898e0e2f6c444479c17c6726ca2ad22efb684cd7b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd8237b72394a4bad4495dd1d91b7c23e9d91515dcbf5054abe5c5d2d4273a6(
    value: typing.Optional[AppsyncDatasourceHttpConfigAuthorizationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac04a8f8ff8f036d1892a8189b57ae2c476b10f9c66ff32a5b8a4829c85cb05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a14915cb61f6769eef0de5633fb198413f6aff29987c03b18cfbda93ac8873(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2def9e09b979e7c52ea53f8d3ba5059cace1f1e1f33c66ddd9a77c37071019(
    value: typing.Optional[AppsyncDatasourceHttpConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b91ecbca2d1d0b958271d6cc33de56cb6575e0d02ba3fc5ca28440d89edd85f(
    *,
    function_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732040c6cd21f3ed0088934419bf930e7bee26037326d2a9d921a246eb6f4f93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d654183a91778566a6636571df48972b58a0c845cedb593f4984434dd2494c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898d70018df02028f1657890631db05e3e1accec3d27457225a2b5b7671d8332(
    value: typing.Optional[AppsyncDatasourceLambdaConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f15f149824ce18016b007f1a5e0c35f0e58a0ed487cd638fd6569cb8c2a2c71(
    *,
    endpoint: builtins.str,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6949b424be857cd11c45b5a82a872727368e93e4e5ac9c5774973864855ad4d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317c9fd54150d4cd7f38b44356aa655f8db9ccf0fed7f251e5c91e574dbc8710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee1128b13de420e3d0ade82978d0dd5e819d519773dc17b74b76520306bde2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de25d28b86d86960cae77a770fe104d27c349442523152136198bc19ed73153(
    value: typing.Optional[AppsyncDatasourceOpensearchserviceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366421674bb2d1dfd8ec5c275e20f8a0491116964e2d35b53f1dba57eb6f24c3(
    *,
    http_endpoint_config: typing.Optional[typing.Union[AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31cb65a8494c167d25f1816d0cf20dd8904265cbbb8fdbb0035e9e18532b5b9(
    *,
    aws_secret_store_arn: builtins.str,
    db_cluster_identifier: builtins.str,
    database_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b38d74228d5ced8b05ac0f08c60d63bd7c780300c02668b187373f620af04a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e0b08b9171d2d86b6e56e1363cd25c68fb29ee6d75b1d014bafcecfb54654b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ea0cc75721836d76f41e59c092808fb60456ea10b7310db0d03fb19ce21773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856de77f22da8d8abd577d9a0faeb3564faa81c95d930981023c1cc42c5f42bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bf1029689bd5b1c8b9c86be71a42dca08fe45d23e0b812919a7ad22c65d28ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914031431105ec8fbe342d62b4a026e550c96d9990e3b767af8100879e74e429(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8ce73548e84bb80c6f4cdf316bdb98fdc621cb59ef98a7fadd23252e63fce7(
    value: typing.Optional[AppsyncDatasourceRelationalDatabaseConfigHttpEndpointConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c618b6625b036e0b0910b8721abdfe44468f89ed1e30109c87ba6aa148cd20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e9cbff7d2e591e1346feaeb88736cd55e7da54dc199775a2f78ab12218bf8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12765a33dd6f1a82cc1be7e6e2609f9e49884b5184a2d02b6b3d15813b293c6c(
    value: typing.Optional[AppsyncDatasourceRelationalDatabaseConfig],
) -> None:
    """Type checking stubs"""
    pass
