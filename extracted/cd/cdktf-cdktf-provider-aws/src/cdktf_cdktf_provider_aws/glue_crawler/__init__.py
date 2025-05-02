r'''
# `aws_glue_crawler`

Refer to the Terraform Registry for docs: [`aws_glue_crawler`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler).
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


class GlueCrawler(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawler",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler aws_glue_crawler}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database_name: builtins.str,
        name: builtins.str,
        role: builtins.str,
        catalog_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerCatalogTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[builtins.str] = None,
        delta_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDeltaTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDynamodbTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hudi_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerHudiTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iceberg_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerIcebergTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerJdbcTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lake_formation_configuration: typing.Optional[typing.Union["GlueCrawlerLakeFormationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        lineage_configuration: typing.Optional[typing.Union["GlueCrawlerLineageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        mongodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerMongodbTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        recrawl_policy: typing.Optional[typing.Union["GlueCrawlerRecrawlPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerS3Target", typing.Dict[builtins.str, typing.Any]]]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        schema_change_policy: typing.Optional[typing.Union["GlueCrawlerSchemaChangePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler aws_glue_crawler} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#name GlueCrawler#name}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#role GlueCrawler#role}.
        :param catalog_target: catalog_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#catalog_target GlueCrawler#catalog_target}
        :param classifiers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#classifiers GlueCrawler#classifiers}.
        :param configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#configuration GlueCrawler#configuration}.
        :param delta_target: delta_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#delta_target GlueCrawler#delta_target}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#description GlueCrawler#description}.
        :param dynamodb_target: dynamodb_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#dynamodb_target GlueCrawler#dynamodb_target}
        :param hudi_target: hudi_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#hudi_target GlueCrawler#hudi_target}
        :param iceberg_target: iceberg_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#iceberg_target GlueCrawler#iceberg_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#id GlueCrawler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_target: jdbc_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#jdbc_target GlueCrawler#jdbc_target}
        :param lake_formation_configuration: lake_formation_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#lake_formation_configuration GlueCrawler#lake_formation_configuration}
        :param lineage_configuration: lineage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#lineage_configuration GlueCrawler#lineage_configuration}
        :param mongodb_target: mongodb_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#mongodb_target GlueCrawler#mongodb_target}
        :param recrawl_policy: recrawl_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#recrawl_policy GlueCrawler#recrawl_policy}
        :param s3_target: s3_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#s3_target GlueCrawler#s3_target}
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#schedule GlueCrawler#schedule}.
        :param schema_change_policy: schema_change_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#schema_change_policy GlueCrawler#schema_change_policy}
        :param security_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#security_configuration GlueCrawler#security_configuration}.
        :param table_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#table_prefix GlueCrawler#table_prefix}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#tags GlueCrawler#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#tags_all GlueCrawler#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4c65516ffdc5c97487ac31110b7c4525d049d77903d7a06b88e348de6b8c12)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GlueCrawlerConfig(
            database_name=database_name,
            name=name,
            role=role,
            catalog_target=catalog_target,
            classifiers=classifiers,
            configuration=configuration,
            delta_target=delta_target,
            description=description,
            dynamodb_target=dynamodb_target,
            hudi_target=hudi_target,
            iceberg_target=iceberg_target,
            id=id,
            jdbc_target=jdbc_target,
            lake_formation_configuration=lake_formation_configuration,
            lineage_configuration=lineage_configuration,
            mongodb_target=mongodb_target,
            recrawl_policy=recrawl_policy,
            s3_target=s3_target,
            schedule=schedule,
            schema_change_policy=schema_change_policy,
            security_configuration=security_configuration,
            table_prefix=table_prefix,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a GlueCrawler resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GlueCrawler to import.
        :param import_from_id: The id of the existing GlueCrawler that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GlueCrawler to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c232dadb53a6328de083f0e910b75bc70976fa9799debf2e9003ca9a606ea1c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCatalogTarget")
    def put_catalog_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerCatalogTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01247cd1643d642f5c04cb3361ea0af393745714337ee375b3e42d94448f91da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCatalogTarget", [value]))

    @jsii.member(jsii_name="putDeltaTarget")
    def put_delta_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDeltaTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912d3cd66530321712b6bd9a19cccebc436fa04763a144e6d829ff9f0351fb3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDeltaTarget", [value]))

    @jsii.member(jsii_name="putDynamodbTarget")
    def put_dynamodb_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDynamodbTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b64061c517f0535dad3a626445b29d5a6698b6fe33f57e64f338b6e5ae5833a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDynamodbTarget", [value]))

    @jsii.member(jsii_name="putHudiTarget")
    def put_hudi_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerHudiTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25592c1ebbbdcb60c04d49667d62ec3444dde01117f8ccb051b4e78de85dd79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHudiTarget", [value]))

    @jsii.member(jsii_name="putIcebergTarget")
    def put_iceberg_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerIcebergTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7e40e52417b691b77e5666c4551de06d69e33c6de64eafc092f8eb15e09604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIcebergTarget", [value]))

    @jsii.member(jsii_name="putJdbcTarget")
    def put_jdbc_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerJdbcTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fa5d3e8e992fdf8b5e5cf9889e90c183c323e6b409be5e0c5e6174bcb4615f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putJdbcTarget", [value]))

    @jsii.member(jsii_name="putLakeFormationConfiguration")
    def put_lake_formation_configuration(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        use_lake_formation_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#account_id GlueCrawler#account_id}.
        :param use_lake_formation_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#use_lake_formation_credentials GlueCrawler#use_lake_formation_credentials}.
        '''
        value = GlueCrawlerLakeFormationConfiguration(
            account_id=account_id,
            use_lake_formation_credentials=use_lake_formation_credentials,
        )

        return typing.cast(None, jsii.invoke(self, "putLakeFormationConfiguration", [value]))

    @jsii.member(jsii_name="putLineageConfiguration")
    def put_lineage_configuration(
        self,
        *,
        crawler_lineage_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param crawler_lineage_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#crawler_lineage_settings GlueCrawler#crawler_lineage_settings}.
        '''
        value = GlueCrawlerLineageConfiguration(
            crawler_lineage_settings=crawler_lineage_settings
        )

        return typing.cast(None, jsii.invoke(self, "putLineageConfiguration", [value]))

    @jsii.member(jsii_name="putMongodbTarget")
    def put_mongodb_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerMongodbTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45bfbaec671f67f29b90e95bcfece0bb33fdb425fca839c5685cfc29b092ae61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMongodbTarget", [value]))

    @jsii.member(jsii_name="putRecrawlPolicy")
    def put_recrawl_policy(
        self,
        *,
        recrawl_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recrawl_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#recrawl_behavior GlueCrawler#recrawl_behavior}.
        '''
        value = GlueCrawlerRecrawlPolicy(recrawl_behavior=recrawl_behavior)

        return typing.cast(None, jsii.invoke(self, "putRecrawlPolicy", [value]))

    @jsii.member(jsii_name="putS3Target")
    def put_s3_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerS3Target", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba686db54bf400e9f82b25b7751b28815fe8447191112e9fe0408f7489dece7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3Target", [value]))

    @jsii.member(jsii_name="putSchemaChangePolicy")
    def put_schema_change_policy(
        self,
        *,
        delete_behavior: typing.Optional[builtins.str] = None,
        update_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#delete_behavior GlueCrawler#delete_behavior}.
        :param update_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#update_behavior GlueCrawler#update_behavior}.
        '''
        value = GlueCrawlerSchemaChangePolicy(
            delete_behavior=delete_behavior, update_behavior=update_behavior
        )

        return typing.cast(None, jsii.invoke(self, "putSchemaChangePolicy", [value]))

    @jsii.member(jsii_name="resetCatalogTarget")
    def reset_catalog_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalogTarget", []))

    @jsii.member(jsii_name="resetClassifiers")
    def reset_classifiers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassifiers", []))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetDeltaTarget")
    def reset_delta_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeltaTarget", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamodbTarget")
    def reset_dynamodb_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodbTarget", []))

    @jsii.member(jsii_name="resetHudiTarget")
    def reset_hudi_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHudiTarget", []))

    @jsii.member(jsii_name="resetIcebergTarget")
    def reset_iceberg_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcebergTarget", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJdbcTarget")
    def reset_jdbc_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJdbcTarget", []))

    @jsii.member(jsii_name="resetLakeFormationConfiguration")
    def reset_lake_formation_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLakeFormationConfiguration", []))

    @jsii.member(jsii_name="resetLineageConfiguration")
    def reset_lineage_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLineageConfiguration", []))

    @jsii.member(jsii_name="resetMongodbTarget")
    def reset_mongodb_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongodbTarget", []))

    @jsii.member(jsii_name="resetRecrawlPolicy")
    def reset_recrawl_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecrawlPolicy", []))

    @jsii.member(jsii_name="resetS3Target")
    def reset_s3_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Target", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetSchemaChangePolicy")
    def reset_schema_change_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaChangePolicy", []))

    @jsii.member(jsii_name="resetSecurityConfiguration")
    def reset_security_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityConfiguration", []))

    @jsii.member(jsii_name="resetTablePrefix")
    def reset_table_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTablePrefix", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="catalogTarget")
    def catalog_target(self) -> "GlueCrawlerCatalogTargetList":
        return typing.cast("GlueCrawlerCatalogTargetList", jsii.get(self, "catalogTarget"))

    @builtins.property
    @jsii.member(jsii_name="deltaTarget")
    def delta_target(self) -> "GlueCrawlerDeltaTargetList":
        return typing.cast("GlueCrawlerDeltaTargetList", jsii.get(self, "deltaTarget"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbTarget")
    def dynamodb_target(self) -> "GlueCrawlerDynamodbTargetList":
        return typing.cast("GlueCrawlerDynamodbTargetList", jsii.get(self, "dynamodbTarget"))

    @builtins.property
    @jsii.member(jsii_name="hudiTarget")
    def hudi_target(self) -> "GlueCrawlerHudiTargetList":
        return typing.cast("GlueCrawlerHudiTargetList", jsii.get(self, "hudiTarget"))

    @builtins.property
    @jsii.member(jsii_name="icebergTarget")
    def iceberg_target(self) -> "GlueCrawlerIcebergTargetList":
        return typing.cast("GlueCrawlerIcebergTargetList", jsii.get(self, "icebergTarget"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTarget")
    def jdbc_target(self) -> "GlueCrawlerJdbcTargetList":
        return typing.cast("GlueCrawlerJdbcTargetList", jsii.get(self, "jdbcTarget"))

    @builtins.property
    @jsii.member(jsii_name="lakeFormationConfiguration")
    def lake_formation_configuration(
        self,
    ) -> "GlueCrawlerLakeFormationConfigurationOutputReference":
        return typing.cast("GlueCrawlerLakeFormationConfigurationOutputReference", jsii.get(self, "lakeFormationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="lineageConfiguration")
    def lineage_configuration(self) -> "GlueCrawlerLineageConfigurationOutputReference":
        return typing.cast("GlueCrawlerLineageConfigurationOutputReference", jsii.get(self, "lineageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="mongodbTarget")
    def mongodb_target(self) -> "GlueCrawlerMongodbTargetList":
        return typing.cast("GlueCrawlerMongodbTargetList", jsii.get(self, "mongodbTarget"))

    @builtins.property
    @jsii.member(jsii_name="recrawlPolicy")
    def recrawl_policy(self) -> "GlueCrawlerRecrawlPolicyOutputReference":
        return typing.cast("GlueCrawlerRecrawlPolicyOutputReference", jsii.get(self, "recrawlPolicy"))

    @builtins.property
    @jsii.member(jsii_name="s3Target")
    def s3_target(self) -> "GlueCrawlerS3TargetList":
        return typing.cast("GlueCrawlerS3TargetList", jsii.get(self, "s3Target"))

    @builtins.property
    @jsii.member(jsii_name="schemaChangePolicy")
    def schema_change_policy(self) -> "GlueCrawlerSchemaChangePolicyOutputReference":
        return typing.cast("GlueCrawlerSchemaChangePolicyOutputReference", jsii.get(self, "schemaChangePolicy"))

    @builtins.property
    @jsii.member(jsii_name="catalogTargetInput")
    def catalog_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerCatalogTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerCatalogTarget"]]], jsii.get(self, "catalogTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="classifiersInput")
    def classifiers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "classifiersInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deltaTargetInput")
    def delta_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDeltaTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDeltaTarget"]]], jsii.get(self, "deltaTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbTargetInput")
    def dynamodb_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDynamodbTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDynamodbTarget"]]], jsii.get(self, "dynamodbTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="hudiTargetInput")
    def hudi_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerHudiTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerHudiTarget"]]], jsii.get(self, "hudiTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="icebergTargetInput")
    def iceberg_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerIcebergTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerIcebergTarget"]]], jsii.get(self, "icebergTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jdbcTargetInput")
    def jdbc_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerJdbcTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerJdbcTarget"]]], jsii.get(self, "jdbcTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="lakeFormationConfigurationInput")
    def lake_formation_configuration_input(
        self,
    ) -> typing.Optional["GlueCrawlerLakeFormationConfiguration"]:
        return typing.cast(typing.Optional["GlueCrawlerLakeFormationConfiguration"], jsii.get(self, "lakeFormationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="lineageConfigurationInput")
    def lineage_configuration_input(
        self,
    ) -> typing.Optional["GlueCrawlerLineageConfiguration"]:
        return typing.cast(typing.Optional["GlueCrawlerLineageConfiguration"], jsii.get(self, "lineageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="mongodbTargetInput")
    def mongodb_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerMongodbTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerMongodbTarget"]]], jsii.get(self, "mongodbTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="recrawlPolicyInput")
    def recrawl_policy_input(self) -> typing.Optional["GlueCrawlerRecrawlPolicy"]:
        return typing.cast(typing.Optional["GlueCrawlerRecrawlPolicy"], jsii.get(self, "recrawlPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="s3TargetInput")
    def s3_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerS3Target"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerS3Target"]]], jsii.get(self, "s3TargetInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaChangePolicyInput")
    def schema_change_policy_input(
        self,
    ) -> typing.Optional["GlueCrawlerSchemaChangePolicy"]:
        return typing.cast(typing.Optional["GlueCrawlerSchemaChangePolicy"], jsii.get(self, "schemaChangePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="securityConfigurationInput")
    def security_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefixInput")
    def table_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tablePrefixInput"))

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
    @jsii.member(jsii_name="classifiers")
    def classifiers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "classifiers"))

    @classifiers.setter
    def classifiers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e584f9ae52ef56c0ae0cd226cd421f19a5bc8a7936cee0646bb0fd6780a4f0fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classifiers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973dfc8b8574af4a0abd0ec6be229d9db660bb6f4ed2a2deb45546806c401560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860d5bafa378fe75f2bfe4f2f6dfcb35c19d2318a6946bf7e4501f131080da42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd0ed47844462ff012f1a932cf8108c1e425ff67a2accbef85bd9cee8986e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc47d2abe4b5d2a8815ab3eee25bf56784b10da31fc343134a0d19e76c1749b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb70e6ec91748f678074ff5c83dd3c6651398e3210e8a2961e273e3bffbe547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c997ffc3551344a35cab96f3d3ed77fcb63d2e7bdd725dffb72f0e70d31e13f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ce870459bbffbdd9c7c9f394d96db142e4b36e92865b3cd43735526e67f3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityConfiguration")
    def security_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityConfiguration"))

    @security_configuration.setter
    def security_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b067cb0c1fb730878cf9e3b445b09490354dffcad681f83ed160f9580d48e290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePrefix"))

    @table_prefix.setter
    def table_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df06198ceade2405bae6b568713c32cefa23f3c07ae12edd690850287c1783d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablePrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd137d7ad61d863ab66f66d2c446e697b9c28275426d89b6146021bd9b3ca8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1af8e2ea3d47ebd92b0fa3234038ce1f773c9fdf26dc7c70702c896ae3669e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerCatalogTarget",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "tables": "tables",
        "connection_name": "connectionName",
        "dlq_event_queue_arn": "dlqEventQueueArn",
        "event_queue_arn": "eventQueueArn",
    },
)
class GlueCrawlerCatalogTarget:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        tables: typing.Sequence[builtins.str],
        connection_name: typing.Optional[builtins.str] = None,
        dlq_event_queue_arn: typing.Optional[builtins.str] = None,
        event_queue_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.
        :param tables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#tables GlueCrawler#tables}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param dlq_event_queue_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#dlq_event_queue_arn GlueCrawler#dlq_event_queue_arn}.
        :param event_queue_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#event_queue_arn GlueCrawler#event_queue_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5a3c6ad3aa8e0b625d2a87b05df251418e59496dcf56b73c199e05b38bde77)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument tables", value=tables, expected_type=type_hints["tables"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument dlq_event_queue_arn", value=dlq_event_queue_arn, expected_type=type_hints["dlq_event_queue_arn"])
            check_type(argname="argument event_queue_arn", value=event_queue_arn, expected_type=type_hints["event_queue_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "tables": tables,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if dlq_event_queue_arn is not None:
            self._values["dlq_event_queue_arn"] = dlq_event_queue_arn
        if event_queue_arn is not None:
            self._values["event_queue_arn"] = event_queue_arn

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tables(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#tables GlueCrawler#tables}.'''
        result = self._values.get("tables")
        assert result is not None, "Required property 'tables' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dlq_event_queue_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#dlq_event_queue_arn GlueCrawler#dlq_event_queue_arn}.'''
        result = self._values.get("dlq_event_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_queue_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#event_queue_arn GlueCrawler#event_queue_arn}.'''
        result = self._values.get("event_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerCatalogTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerCatalogTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerCatalogTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c963ab98113c234d7865ae295c4c0daf3da0858727e68a486daf53ddca89b5c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerCatalogTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881f46f92fbec060ee94689a91656688378a5bd3bd29056b67db532749f786d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerCatalogTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ffe51bec2236c27931d870e4a4b7d0bc424c063aed6c14d539a92fe8c951d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2365102d07208c93159d18c53ba2155f2311816df8bcc19c821f7a32c3c0281b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf1d3035adbe27fcaf7ffc59f070bcad22165b210cbe31149d7813be873ee04b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e515f41d9075e58415356e3f4106e1ef3b1099d8f22e3505940bb8f569a4fa43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerCatalogTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerCatalogTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25f400655704386773cc09ffdd489f52c0e80b28f99e73ea894198d3f05cfd2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetDlqEventQueueArn")
    def reset_dlq_event_queue_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDlqEventQueueArn", []))

    @jsii.member(jsii_name="resetEventQueueArn")
    def reset_event_queue_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventQueueArn", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dlqEventQueueArnInput")
    def dlq_event_queue_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dlqEventQueueArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventQueueArnInput")
    def event_queue_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventQueueArnInput"))

    @builtins.property
    @jsii.member(jsii_name="tablesInput")
    def tables_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tablesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0043a5400b19467313db56e0273fe86f573e8a642de0a0f0cbe10a461eb5a83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047e2247f0b058cdfe4aef46f7a3c9e84847e9c11f02cbe9f72a3997f27fc060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dlqEventQueueArn")
    def dlq_event_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dlqEventQueueArn"))

    @dlq_event_queue_arn.setter
    def dlq_event_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a1f94402b2ffa06002e574a2ba7a4dfcd134c12c9e41b612ca7875faaa2b4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dlqEventQueueArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventQueueArn")
    def event_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventQueueArn"))

    @event_queue_arn.setter
    def event_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37af715e5b76ac53965b2d18452ade1a7242231c851258ac7f4abda0f9bb68e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventQueueArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tables")
    def tables(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tables"))

    @tables.setter
    def tables(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e5d9bc5a4bd9f206706033b290b79457f7178ce38f2e2600ce8e9184a5bb3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerCatalogTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerCatalogTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerCatalogTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d1782aacbf4c05f47d673cb65bd98c84540f3f302910705150731c5fd54e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database_name": "databaseName",
        "name": "name",
        "role": "role",
        "catalog_target": "catalogTarget",
        "classifiers": "classifiers",
        "configuration": "configuration",
        "delta_target": "deltaTarget",
        "description": "description",
        "dynamodb_target": "dynamodbTarget",
        "hudi_target": "hudiTarget",
        "iceberg_target": "icebergTarget",
        "id": "id",
        "jdbc_target": "jdbcTarget",
        "lake_formation_configuration": "lakeFormationConfiguration",
        "lineage_configuration": "lineageConfiguration",
        "mongodb_target": "mongodbTarget",
        "recrawl_policy": "recrawlPolicy",
        "s3_target": "s3Target",
        "schedule": "schedule",
        "schema_change_policy": "schemaChangePolicy",
        "security_configuration": "securityConfiguration",
        "table_prefix": "tablePrefix",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class GlueCrawlerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database_name: builtins.str,
        name: builtins.str,
        role: builtins.str,
        catalog_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerCatalogTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[builtins.str] = None,
        delta_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDeltaTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerDynamodbTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hudi_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerHudiTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        iceberg_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerIcebergTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        jdbc_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerJdbcTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        lake_formation_configuration: typing.Optional[typing.Union["GlueCrawlerLakeFormationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        lineage_configuration: typing.Optional[typing.Union["GlueCrawlerLineageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        mongodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerMongodbTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        recrawl_policy: typing.Optional[typing.Union["GlueCrawlerRecrawlPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GlueCrawlerS3Target", typing.Dict[builtins.str, typing.Any]]]]] = None,
        schedule: typing.Optional[builtins.str] = None,
        schema_change_policy: typing.Optional[typing.Union["GlueCrawlerSchemaChangePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#name GlueCrawler#name}.
        :param role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#role GlueCrawler#role}.
        :param catalog_target: catalog_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#catalog_target GlueCrawler#catalog_target}
        :param classifiers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#classifiers GlueCrawler#classifiers}.
        :param configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#configuration GlueCrawler#configuration}.
        :param delta_target: delta_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#delta_target GlueCrawler#delta_target}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#description GlueCrawler#description}.
        :param dynamodb_target: dynamodb_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#dynamodb_target GlueCrawler#dynamodb_target}
        :param hudi_target: hudi_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#hudi_target GlueCrawler#hudi_target}
        :param iceberg_target: iceberg_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#iceberg_target GlueCrawler#iceberg_target}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#id GlueCrawler#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jdbc_target: jdbc_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#jdbc_target GlueCrawler#jdbc_target}
        :param lake_formation_configuration: lake_formation_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#lake_formation_configuration GlueCrawler#lake_formation_configuration}
        :param lineage_configuration: lineage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#lineage_configuration GlueCrawler#lineage_configuration}
        :param mongodb_target: mongodb_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#mongodb_target GlueCrawler#mongodb_target}
        :param recrawl_policy: recrawl_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#recrawl_policy GlueCrawler#recrawl_policy}
        :param s3_target: s3_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#s3_target GlueCrawler#s3_target}
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#schedule GlueCrawler#schedule}.
        :param schema_change_policy: schema_change_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#schema_change_policy GlueCrawler#schema_change_policy}
        :param security_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#security_configuration GlueCrawler#security_configuration}.
        :param table_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#table_prefix GlueCrawler#table_prefix}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#tags GlueCrawler#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#tags_all GlueCrawler#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(lake_formation_configuration, dict):
            lake_formation_configuration = GlueCrawlerLakeFormationConfiguration(**lake_formation_configuration)
        if isinstance(lineage_configuration, dict):
            lineage_configuration = GlueCrawlerLineageConfiguration(**lineage_configuration)
        if isinstance(recrawl_policy, dict):
            recrawl_policy = GlueCrawlerRecrawlPolicy(**recrawl_policy)
        if isinstance(schema_change_policy, dict):
            schema_change_policy = GlueCrawlerSchemaChangePolicy(**schema_change_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70be716cf9fd8495efcfe58a5112ee47ab881fc2603bf65028ec1ae23a6c35a4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument catalog_target", value=catalog_target, expected_type=type_hints["catalog_target"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument delta_target", value=delta_target, expected_type=type_hints["delta_target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamodb_target", value=dynamodb_target, expected_type=type_hints["dynamodb_target"])
            check_type(argname="argument hudi_target", value=hudi_target, expected_type=type_hints["hudi_target"])
            check_type(argname="argument iceberg_target", value=iceberg_target, expected_type=type_hints["iceberg_target"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jdbc_target", value=jdbc_target, expected_type=type_hints["jdbc_target"])
            check_type(argname="argument lake_formation_configuration", value=lake_formation_configuration, expected_type=type_hints["lake_formation_configuration"])
            check_type(argname="argument lineage_configuration", value=lineage_configuration, expected_type=type_hints["lineage_configuration"])
            check_type(argname="argument mongodb_target", value=mongodb_target, expected_type=type_hints["mongodb_target"])
            check_type(argname="argument recrawl_policy", value=recrawl_policy, expected_type=type_hints["recrawl_policy"])
            check_type(argname="argument s3_target", value=s3_target, expected_type=type_hints["s3_target"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument schema_change_policy", value=schema_change_policy, expected_type=type_hints["schema_change_policy"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
            "name": name,
            "role": role,
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
        if catalog_target is not None:
            self._values["catalog_target"] = catalog_target
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if configuration is not None:
            self._values["configuration"] = configuration
        if delta_target is not None:
            self._values["delta_target"] = delta_target
        if description is not None:
            self._values["description"] = description
        if dynamodb_target is not None:
            self._values["dynamodb_target"] = dynamodb_target
        if hudi_target is not None:
            self._values["hudi_target"] = hudi_target
        if iceberg_target is not None:
            self._values["iceberg_target"] = iceberg_target
        if id is not None:
            self._values["id"] = id
        if jdbc_target is not None:
            self._values["jdbc_target"] = jdbc_target
        if lake_formation_configuration is not None:
            self._values["lake_formation_configuration"] = lake_formation_configuration
        if lineage_configuration is not None:
            self._values["lineage_configuration"] = lineage_configuration
        if mongodb_target is not None:
            self._values["mongodb_target"] = mongodb_target
        if recrawl_policy is not None:
            self._values["recrawl_policy"] = recrawl_policy
        if s3_target is not None:
            self._values["s3_target"] = s3_target
        if schedule is not None:
            self._values["schedule"] = schedule
        if schema_change_policy is not None:
            self._values["schema_change_policy"] = schema_change_policy
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if table_prefix is not None:
            self._values["table_prefix"] = table_prefix
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#database_name GlueCrawler#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#name GlueCrawler#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#role GlueCrawler#role}.'''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]]:
        '''catalog_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#catalog_target GlueCrawler#catalog_target}
        '''
        result = self._values.get("catalog_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]], result)

    @builtins.property
    def classifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#classifiers GlueCrawler#classifiers}.'''
        result = self._values.get("classifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#configuration GlueCrawler#configuration}.'''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delta_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDeltaTarget"]]]:
        '''delta_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#delta_target GlueCrawler#delta_target}
        '''
        result = self._values.get("delta_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDeltaTarget"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#description GlueCrawler#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamodb_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDynamodbTarget"]]]:
        '''dynamodb_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#dynamodb_target GlueCrawler#dynamodb_target}
        '''
        result = self._values.get("dynamodb_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerDynamodbTarget"]]], result)

    @builtins.property
    def hudi_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerHudiTarget"]]]:
        '''hudi_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#hudi_target GlueCrawler#hudi_target}
        '''
        result = self._values.get("hudi_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerHudiTarget"]]], result)

    @builtins.property
    def iceberg_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerIcebergTarget"]]]:
        '''iceberg_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#iceberg_target GlueCrawler#iceberg_target}
        '''
        result = self._values.get("iceberg_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerIcebergTarget"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#id GlueCrawler#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jdbc_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerJdbcTarget"]]]:
        '''jdbc_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#jdbc_target GlueCrawler#jdbc_target}
        '''
        result = self._values.get("jdbc_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerJdbcTarget"]]], result)

    @builtins.property
    def lake_formation_configuration(
        self,
    ) -> typing.Optional["GlueCrawlerLakeFormationConfiguration"]:
        '''lake_formation_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#lake_formation_configuration GlueCrawler#lake_formation_configuration}
        '''
        result = self._values.get("lake_formation_configuration")
        return typing.cast(typing.Optional["GlueCrawlerLakeFormationConfiguration"], result)

    @builtins.property
    def lineage_configuration(
        self,
    ) -> typing.Optional["GlueCrawlerLineageConfiguration"]:
        '''lineage_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#lineage_configuration GlueCrawler#lineage_configuration}
        '''
        result = self._values.get("lineage_configuration")
        return typing.cast(typing.Optional["GlueCrawlerLineageConfiguration"], result)

    @builtins.property
    def mongodb_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerMongodbTarget"]]]:
        '''mongodb_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#mongodb_target GlueCrawler#mongodb_target}
        '''
        result = self._values.get("mongodb_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerMongodbTarget"]]], result)

    @builtins.property
    def recrawl_policy(self) -> typing.Optional["GlueCrawlerRecrawlPolicy"]:
        '''recrawl_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#recrawl_policy GlueCrawler#recrawl_policy}
        '''
        result = self._values.get("recrawl_policy")
        return typing.cast(typing.Optional["GlueCrawlerRecrawlPolicy"], result)

    @builtins.property
    def s3_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerS3Target"]]]:
        '''s3_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#s3_target GlueCrawler#s3_target}
        '''
        result = self._values.get("s3_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GlueCrawlerS3Target"]]], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#schedule GlueCrawler#schedule}.'''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_change_policy(self) -> typing.Optional["GlueCrawlerSchemaChangePolicy"]:
        '''schema_change_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#schema_change_policy GlueCrawler#schema_change_policy}
        '''
        result = self._values.get("schema_change_policy")
        return typing.cast(typing.Optional["GlueCrawlerSchemaChangePolicy"], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#security_configuration GlueCrawler#security_configuration}.'''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#table_prefix GlueCrawler#table_prefix}.'''
        result = self._values.get("table_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#tags GlueCrawler#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#tags_all GlueCrawler#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerDeltaTarget",
    jsii_struct_bases=[],
    name_mapping={
        "delta_tables": "deltaTables",
        "write_manifest": "writeManifest",
        "connection_name": "connectionName",
        "create_native_delta_table": "createNativeDeltaTable",
    },
)
class GlueCrawlerDeltaTarget:
    def __init__(
        self,
        *,
        delta_tables: typing.Sequence[builtins.str],
        write_manifest: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        connection_name: typing.Optional[builtins.str] = None,
        create_native_delta_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param delta_tables: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#delta_tables GlueCrawler#delta_tables}.
        :param write_manifest: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#write_manifest GlueCrawler#write_manifest}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param create_native_delta_table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#create_native_delta_table GlueCrawler#create_native_delta_table}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ed98b8be4f732e000212784a03756b4296bf66ae2780f62783f33ea462438e)
            check_type(argname="argument delta_tables", value=delta_tables, expected_type=type_hints["delta_tables"])
            check_type(argname="argument write_manifest", value=write_manifest, expected_type=type_hints["write_manifest"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument create_native_delta_table", value=create_native_delta_table, expected_type=type_hints["create_native_delta_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delta_tables": delta_tables,
            "write_manifest": write_manifest,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if create_native_delta_table is not None:
            self._values["create_native_delta_table"] = create_native_delta_table

    @builtins.property
    def delta_tables(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#delta_tables GlueCrawler#delta_tables}.'''
        result = self._values.get("delta_tables")
        assert result is not None, "Required property 'delta_tables' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def write_manifest(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#write_manifest GlueCrawler#write_manifest}.'''
        result = self._values.get("write_manifest")
        assert result is not None, "Required property 'write_manifest' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_native_delta_table(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#create_native_delta_table GlueCrawler#create_native_delta_table}.'''
        result = self._values.get("create_native_delta_table")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerDeltaTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerDeltaTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerDeltaTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__607a53e23e9f9d9465c5ac39aa1c6f9155e3565076ab7d838883ef44fdf281b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerDeltaTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9c4d35061247d5d87f06af80e2a400b3678f0acb78a07a73eb2886cdd186418)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerDeltaTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6df37594b034a62085c16006b47fb155184fd6dc81c69cf4a72a90ee176258)
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
            type_hints = typing.get_type_hints(_typecheckingstub__200c45fed2ed2b771c616f3fb5797d569124648fe2041e02d564d7062d36e468)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b01296bcee7baca8b2f9c8b0bb453f700d118f9c5c747901a08dc1a6b01c5566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDeltaTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDeltaTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDeltaTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aab1e5b95303388984b0ee1e2b2f3dc76e6e1d97a39029dd611318a177e2ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerDeltaTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerDeltaTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d8ba6e99234d78fdc41a34f0be8a8b1d880762f5b09ce4f1fe9b181de2a5d0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetCreateNativeDeltaTable")
    def reset_create_native_delta_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateNativeDeltaTable", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="createNativeDeltaTableInput")
    def create_native_delta_table_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createNativeDeltaTableInput"))

    @builtins.property
    @jsii.member(jsii_name="deltaTablesInput")
    def delta_tables_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "deltaTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="writeManifestInput")
    def write_manifest_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeManifestInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c277d9503eb195d0dc04b592d593158a363c153c3da44b75161432d7cbd8f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createNativeDeltaTable")
    def create_native_delta_table(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createNativeDeltaTable"))

    @create_native_delta_table.setter
    def create_native_delta_table(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9c12bae98879b12680838fa6f48c6ab2e3bf0184c08ae64fd48be3cc549ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createNativeDeltaTable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deltaTables")
    def delta_tables(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deltaTables"))

    @delta_tables.setter
    def delta_tables(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c68c35523584d2f06c35d7555a2d325ab23725427cfdaf1f632756cf93074a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deltaTables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="writeManifest")
    def write_manifest(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "writeManifest"))

    @write_manifest.setter
    def write_manifest(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1910ce883e709de44e96dfc4b6e16fa5e062c01f169b80a0abb49629ef83fa8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeManifest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDeltaTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDeltaTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDeltaTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2aad4650d8a07a487da2d01a9039763272bd53ee1cfa4f4358ebf9795b09120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerDynamodbTarget",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "scan_all": "scanAll", "scan_rate": "scanRate"},
)
class GlueCrawlerDynamodbTarget:
    def __init__(
        self,
        *,
        path: builtins.str,
        scan_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scan_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#path GlueCrawler#path}.
        :param scan_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#scan_all GlueCrawler#scan_all}.
        :param scan_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#scan_rate GlueCrawler#scan_rate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4a3f9ae5a62dcf48f95b95ae4cfb17eec77a8a937bec64d924b129aff37140)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument scan_all", value=scan_all, expected_type=type_hints["scan_all"])
            check_type(argname="argument scan_rate", value=scan_rate, expected_type=type_hints["scan_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if scan_all is not None:
            self._values["scan_all"] = scan_all
        if scan_rate is not None:
            self._values["scan_rate"] = scan_rate

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#path GlueCrawler#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scan_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#scan_all GlueCrawler#scan_all}.'''
        result = self._values.get("scan_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scan_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#scan_rate GlueCrawler#scan_rate}.'''
        result = self._values.get("scan_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerDynamodbTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerDynamodbTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerDynamodbTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__332f4cb840975c65b44f25deecb73d20b5ac9c1257629856f0eff6ffc92a28b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerDynamodbTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a0cefbc4b86253290246904b5321246b466422522b84cabb943b64f95d8ab3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerDynamodbTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0973f5b98721085b86ae96b6546aa84283905fafe141dda41d7685c317e4f97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cec4d86ad2e0b93fd651b158196304ee96dd47deca09861185bd3f28a09d3050)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da90b5ca6369bd2cbeb55f787c2f1c1cfbe7d471cb9911fa47ceebba86c10182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDynamodbTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDynamodbTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDynamodbTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e02558b564e1c03622210cbb4c90a9558f5d766f700cf19cd8b337d8ee35678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerDynamodbTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerDynamodbTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e642bbc08e1ffb36584f3414362e61e8d36667ea7588339feca83f6231d353fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetScanAll")
    def reset_scan_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanAll", []))

    @jsii.member(jsii_name="resetScanRate")
    def reset_scan_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanRate", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="scanAllInput")
    def scan_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scanAllInput"))

    @builtins.property
    @jsii.member(jsii_name="scanRateInput")
    def scan_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scanRateInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7af26dcc3cdacc1d02fed166eedfe88b32be1dcbd4b22871ff3749d263292e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanAll")
    def scan_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scanAll"))

    @scan_all.setter
    def scan_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78da00f17249e51add1c9f3bfad74712c3601ac4848dd21b9514eef9a65a9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanRate")
    def scan_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scanRate"))

    @scan_rate.setter
    def scan_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649dee3d6f76c0d7aeff52085948384148057a2d6fd41afb083abefa0e673cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDynamodbTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDynamodbTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDynamodbTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011d851fb0e8529633716501cb72028e9c1e598b069bde7ed1f783e272ec87e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerHudiTarget",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_traversal_depth": "maximumTraversalDepth",
        "paths": "paths",
        "connection_name": "connectionName",
        "exclusions": "exclusions",
    },
)
class GlueCrawlerHudiTarget:
    def __init__(
        self,
        *,
        maximum_traversal_depth: jsii.Number,
        paths: typing.Sequence[builtins.str],
        connection_name: typing.Optional[builtins.str] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param maximum_traversal_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#maximum_traversal_depth GlueCrawler#maximum_traversal_depth}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#paths GlueCrawler#paths}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param exclusions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b59d4c21a8c34b546f5734f88b4475d75154bc9c3df24c4b6a270bd99dead4)
            check_type(argname="argument maximum_traversal_depth", value=maximum_traversal_depth, expected_type=type_hints["maximum_traversal_depth"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_traversal_depth": maximum_traversal_depth,
            "paths": paths,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if exclusions is not None:
            self._values["exclusions"] = exclusions

    @builtins.property
    def maximum_traversal_depth(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#maximum_traversal_depth GlueCrawler#maximum_traversal_depth}.'''
        result = self._values.get("maximum_traversal_depth")
        assert result is not None, "Required property 'maximum_traversal_depth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#paths GlueCrawler#paths}.'''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.'''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerHudiTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerHudiTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerHudiTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca47e1175924bc859361c82e08c173d3324f4182f0d6800c20e91227d7ac0c73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerHudiTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733286d54cb3f0dcb3f38bbf4e6173436641e6e4c3bbf4b621bfada3e0991a0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerHudiTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b71bbd38ceda6fa15388466debbfcaad78006e0f28a8f3659470e3990ec204)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae8d87e37be3f5e6ef626def560eced2c550faa9719858c4e4bdbffa81970923)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc9bce204ad7de78194e168774df6abd14a95b2ed1c95f14b94f6b8dd47f371c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerHudiTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerHudiTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerHudiTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d5718653a4bee230a1fe904ea0d19abb2b42d06acb727b3ef2f95f125d987e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerHudiTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerHudiTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a76c4b42d96c78e8061edd4c9434a2dd90e75dd76b855045d8c9a1eccfadb8e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumTraversalDepthInput")
    def maximum_traversal_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumTraversalDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f566821962a0b85275f6615817c8ab59698c6985a48241090257c72d469484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusions"))

    @exclusions.setter
    def exclusions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148e2eb5e5cba11f6a2d3d87f20c6291035122d61847416caa0fb2a9268e19f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumTraversalDepth")
    def maximum_traversal_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumTraversalDepth"))

    @maximum_traversal_depth.setter
    def maximum_traversal_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39fd6dad300fbe2cb03bff9ebb29ba74e2c65e01b2e27e134660001f8c22813c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumTraversalDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdad4a149e67579f5bc863a6d20e80767264c99197c2cc7efdf4264cb22ade21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerHudiTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerHudiTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerHudiTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4764551d2e925a363f2dd8bd5c4d44d7261bea506e13f95ce2524f06fa657fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerIcebergTarget",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_traversal_depth": "maximumTraversalDepth",
        "paths": "paths",
        "connection_name": "connectionName",
        "exclusions": "exclusions",
    },
)
class GlueCrawlerIcebergTarget:
    def __init__(
        self,
        *,
        maximum_traversal_depth: jsii.Number,
        paths: typing.Sequence[builtins.str],
        connection_name: typing.Optional[builtins.str] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param maximum_traversal_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#maximum_traversal_depth GlueCrawler#maximum_traversal_depth}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#paths GlueCrawler#paths}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param exclusions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6595cc4d44306f256fb9c29efa49c4da2ea22430d66c48d0d599f8d18ff34ae)
            check_type(argname="argument maximum_traversal_depth", value=maximum_traversal_depth, expected_type=type_hints["maximum_traversal_depth"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_traversal_depth": maximum_traversal_depth,
            "paths": paths,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if exclusions is not None:
            self._values["exclusions"] = exclusions

    @builtins.property
    def maximum_traversal_depth(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#maximum_traversal_depth GlueCrawler#maximum_traversal_depth}.'''
        result = self._values.get("maximum_traversal_depth")
        assert result is not None, "Required property 'maximum_traversal_depth' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def paths(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#paths GlueCrawler#paths}.'''
        result = self._values.get("paths")
        assert result is not None, "Required property 'paths' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.'''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerIcebergTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerIcebergTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerIcebergTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2f960b027e290fdfa42daab7aceaf2b443bc9ddd2ff03af5486c2ea7bc5652a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerIcebergTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8a26763b25715a67f240daeb9dba096f7ba00052b15e49d124423d9409d971)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerIcebergTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c72c8a28d74d3056a42ec4ca1541a074b35e72cc9eeba6811fc1cb9bc6b0fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b24f240114faf40db256b49399bcac1137ed03dc4f0d52e6af1f2840b58b4761)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eabbc8ccb5aa769695cd4a6b597e7fb08b04ea484b75394e4cf703e7bcdc390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerIcebergTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerIcebergTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerIcebergTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fe46c7a5eda5a5995cfe04ccd4f21036915d3a2a5d282819f04e37dcffb14a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerIcebergTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerIcebergTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12e5481eecad3db65f3651a28c6c1da8be16d82790ff60fba12e5bba1440dd74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumTraversalDepthInput")
    def maximum_traversal_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumTraversalDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f2a1aa6b52828b3d6d000b6f7a572b6c0f3546c6b884b4b5a14f105c22f893)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusions"))

    @exclusions.setter
    def exclusions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c38dfa797252c5a2af1a9cb3e8131460d20008c1a2b1303d310586c236f7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumTraversalDepth")
    def maximum_traversal_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumTraversalDepth"))

    @maximum_traversal_depth.setter
    def maximum_traversal_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197d70afc23e5f5b95934b88a5f80eca1bd53aea791e2cb147388fc90334061a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumTraversalDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888d804ac7d48e6643bb1f2492e88f865dd6c23b359bb4328dcb91cbff16639b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerIcebergTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerIcebergTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerIcebergTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168f33a5363df9b342d86ba44ce81f5cf81fdfc921883b451164aee9f2cd63f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerJdbcTarget",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "path": "path",
        "enable_additional_metadata": "enableAdditionalMetadata",
        "exclusions": "exclusions",
    },
)
class GlueCrawlerJdbcTarget:
    def __init__(
        self,
        *,
        connection_name: builtins.str,
        path: builtins.str,
        enable_additional_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#path GlueCrawler#path}.
        :param enable_additional_metadata: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#enable_additional_metadata GlueCrawler#enable_additional_metadata}.
        :param exclusions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0b8ca35ae61e40fe2419e036b15295e1b709d068551322d2b7790a382637bc)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument enable_additional_metadata", value=enable_additional_metadata, expected_type=type_hints["enable_additional_metadata"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_name": connection_name,
            "path": path,
        }
        if enable_additional_metadata is not None:
            self._values["enable_additional_metadata"] = enable_additional_metadata
        if exclusions is not None:
            self._values["exclusions"] = exclusions

    @builtins.property
    def connection_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        assert result is not None, "Required property 'connection_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#path GlueCrawler#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_additional_metadata(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#enable_additional_metadata GlueCrawler#enable_additional_metadata}.'''
        result = self._values.get("enable_additional_metadata")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.'''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerJdbcTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerJdbcTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerJdbcTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51d1fb9ffd52414ab9521db0d99a9e4d3664f0e1d5f1b4d899a636b61a7dc018)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerJdbcTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904a715d97a047288a58d5fd88fa49dda77a9c334aa3bdd4ab3168d1f4122fb1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerJdbcTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20a204827fb99f47cbc90f3ebe6ff1e74ed3876852ab69837bdc75e8c3bf3ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82c99379deb0d5129c8aa248a455f0cf503567c2271a5776e64b35c9dc9236ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c390d3709dd488c2be32a084c73c3703d67f18199b9a75e77269351b80406b6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerJdbcTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerJdbcTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerJdbcTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ba6d128ded4c284e2ca10862813e05afeea3e1022f89175f57b38f848b94bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerJdbcTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerJdbcTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdbe039e5147743f174d50d3ce6486aa931cdd5038b988099abb8382f2422956)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnableAdditionalMetadata")
    def reset_enable_additional_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAdditionalMetadata", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAdditionalMetadataInput")
    def enable_additional_metadata_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enableAdditionalMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05e0acf1b764dd5f487ab58846ff59298bb558ff9dbcd3883c2845014135fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAdditionalMetadata")
    def enable_additional_metadata(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "enableAdditionalMetadata"))

    @enable_additional_metadata.setter
    def enable_additional_metadata(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4357d6fd6f5e14053e8557bdfdd935677f2c98b3bce44b55a3ecfebbf59bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAdditionalMetadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusions"))

    @exclusions.setter
    def exclusions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1973c7014e553b6e233bef92aeb5601a03e2a5231e03dbaa11b19f474e683e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4861b6859b3b5b44a1c8c3a5ee1210588035619b94fd0a65e3996eb0884e93ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerJdbcTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerJdbcTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerJdbcTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f872978356c83674adfa7b73077f1f3e4265fa28e5237648b514b593fe2140e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerLakeFormationConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "use_lake_formation_credentials": "useLakeFormationCredentials",
    },
)
class GlueCrawlerLakeFormationConfiguration:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        use_lake_formation_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#account_id GlueCrawler#account_id}.
        :param use_lake_formation_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#use_lake_formation_credentials GlueCrawler#use_lake_formation_credentials}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e49750b032f075036e4cb1870abcf9354615920dda4bafdcf65507f92b09a6df)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument use_lake_formation_credentials", value=use_lake_formation_credentials, expected_type=type_hints["use_lake_formation_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if use_lake_formation_credentials is not None:
            self._values["use_lake_formation_credentials"] = use_lake_formation_credentials

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#account_id GlueCrawler#account_id}.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_lake_formation_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#use_lake_formation_credentials GlueCrawler#use_lake_formation_credentials}.'''
        result = self._values.get("use_lake_formation_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerLakeFormationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerLakeFormationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerLakeFormationConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b71e993e3d968fffc40fd4c46f697239c828cc4d807d0032648d62a2ac0cbe4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetUseLakeFormationCredentials")
    def reset_use_lake_formation_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseLakeFormationCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="useLakeFormationCredentialsInput")
    def use_lake_formation_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useLakeFormationCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f032077010ab1f117d72bbf674ca594c1e494573aa21d9602b7ea25356bc00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useLakeFormationCredentials")
    def use_lake_formation_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useLakeFormationCredentials"))

    @use_lake_formation_credentials.setter
    def use_lake_formation_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aead4a0401aeed761649f783bc3e4927c7583e0f93caae69dffee3e0efc792c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLakeFormationCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueCrawlerLakeFormationConfiguration]:
        return typing.cast(typing.Optional[GlueCrawlerLakeFormationConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueCrawlerLakeFormationConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84918d978ee85f79f924f1e80eaaef3be1d11a8a68da3aeb7e00b01837705546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerLineageConfiguration",
    jsii_struct_bases=[],
    name_mapping={"crawler_lineage_settings": "crawlerLineageSettings"},
)
class GlueCrawlerLineageConfiguration:
    def __init__(
        self,
        *,
        crawler_lineage_settings: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param crawler_lineage_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#crawler_lineage_settings GlueCrawler#crawler_lineage_settings}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab316959ad80c77b0f3d5648271572772b7d32698e581a1fd5a584aadc1b3140)
            check_type(argname="argument crawler_lineage_settings", value=crawler_lineage_settings, expected_type=type_hints["crawler_lineage_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if crawler_lineage_settings is not None:
            self._values["crawler_lineage_settings"] = crawler_lineage_settings

    @builtins.property
    def crawler_lineage_settings(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#crawler_lineage_settings GlueCrawler#crawler_lineage_settings}.'''
        result = self._values.get("crawler_lineage_settings")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerLineageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerLineageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerLineageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afb5c9377c139e0503834b6cf2dbc2a0a70fe818972f8fd2eb93f7c83d16ccf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCrawlerLineageSettings")
    def reset_crawler_lineage_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlerLineageSettings", []))

    @builtins.property
    @jsii.member(jsii_name="crawlerLineageSettingsInput")
    def crawler_lineage_settings_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "crawlerLineageSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlerLineageSettings")
    def crawler_lineage_settings(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "crawlerLineageSettings"))

    @crawler_lineage_settings.setter
    def crawler_lineage_settings(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a8ebad655302f578df47e11654d2601dd8be03ce52e76832564f5322629467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlerLineageSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueCrawlerLineageConfiguration]:
        return typing.cast(typing.Optional[GlueCrawlerLineageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueCrawlerLineageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13346889e5296420b2003090b2d7b7671dd257873bbb439a911973aac724c89d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerMongodbTarget",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "path": "path",
        "scan_all": "scanAll",
    },
)
class GlueCrawlerMongodbTarget:
    def __init__(
        self,
        *,
        connection_name: builtins.str,
        path: builtins.str,
        scan_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#path GlueCrawler#path}.
        :param scan_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#scan_all GlueCrawler#scan_all}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25f9a719a955db4fe04c0aa1fb1e2a64978d46f5c22c517d99534b2bb75dd39)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument scan_all", value=scan_all, expected_type=type_hints["scan_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_name": connection_name,
            "path": path,
        }
        if scan_all is not None:
            self._values["scan_all"] = scan_all

    @builtins.property
    def connection_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        assert result is not None, "Required property 'connection_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#path GlueCrawler#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scan_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#scan_all GlueCrawler#scan_all}.'''
        result = self._values.get("scan_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerMongodbTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerMongodbTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerMongodbTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0532ab563ea17dc6ac7afd7d63a5bca04fee1c8919b5289bc14f30573a69b1af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerMongodbTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d25cd7535eda40581b558a0732c31101e9ff645f8c4ff9ed7f770dc1ff4945)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerMongodbTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78dc79d541254caf3af1e75ba2c4731af0c9df5f5118e23dcb58931d9b2b409)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9bed9d61c91682193f9ea7da6aff492a258a64dd60ba62fb0937a4a76407278)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fb6a0e0792768c81fd33a4b336b5277869dfff83cc1a526431431d4997679a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerMongodbTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerMongodbTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerMongodbTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc2f32cd9ddefcdfdf51eab04a7bbf59fc11ab1802a22690047d397aa9d621d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerMongodbTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerMongodbTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d66096ef0db6de342a39ed6572b527106e91c632cce137adc3cfcc808f64c9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetScanAll")
    def reset_scan_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScanAll", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="scanAllInput")
    def scan_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scanAllInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e675d6b1089ccbcf8f199a76297df15fa225f04039adfd96c0c5771c1076290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7670f19760b1eb506a6a56f399ea0d100c10803e9bf3cfd1ccc8d0f97e975542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scanAll")
    def scan_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scanAll"))

    @scan_all.setter
    def scan_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda86e4841b088bb6c0d4dc1d2de7cbaf664ee41576edbac3ccf751992fec570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scanAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerMongodbTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerMongodbTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerMongodbTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5743671231d696e9c7049e487b871321a8300ed3dcd0e769b159e7e6c83dbf78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerRecrawlPolicy",
    jsii_struct_bases=[],
    name_mapping={"recrawl_behavior": "recrawlBehavior"},
)
class GlueCrawlerRecrawlPolicy:
    def __init__(
        self,
        *,
        recrawl_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recrawl_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#recrawl_behavior GlueCrawler#recrawl_behavior}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5905d83bf20d4a60d912f7ad07b73c539718f183b9e84f3efe95d79adf79e439)
            check_type(argname="argument recrawl_behavior", value=recrawl_behavior, expected_type=type_hints["recrawl_behavior"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recrawl_behavior is not None:
            self._values["recrawl_behavior"] = recrawl_behavior

    @builtins.property
    def recrawl_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#recrawl_behavior GlueCrawler#recrawl_behavior}.'''
        result = self._values.get("recrawl_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerRecrawlPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerRecrawlPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerRecrawlPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5926ac874651895380a800f7b30949c030898f54df9af4abfef45cfe284c1b58)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRecrawlBehavior")
    def reset_recrawl_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecrawlBehavior", []))

    @builtins.property
    @jsii.member(jsii_name="recrawlBehaviorInput")
    def recrawl_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recrawlBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="recrawlBehavior")
    def recrawl_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recrawlBehavior"))

    @recrawl_behavior.setter
    def recrawl_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6fe2bde03cce5707f9623d63d2578ec402928078844985141a004d5c16bac18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recrawlBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueCrawlerRecrawlPolicy]:
        return typing.cast(typing.Optional[GlueCrawlerRecrawlPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GlueCrawlerRecrawlPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2dc17b27ceeceb4def47d997803f6925c9ea1e4f139fd80b22d72e937c5ceef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerS3Target",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "connection_name": "connectionName",
        "dlq_event_queue_arn": "dlqEventQueueArn",
        "event_queue_arn": "eventQueueArn",
        "exclusions": "exclusions",
        "sample_size": "sampleSize",
    },
)
class GlueCrawlerS3Target:
    def __init__(
        self,
        *,
        path: builtins.str,
        connection_name: typing.Optional[builtins.str] = None,
        dlq_event_queue_arn: typing.Optional[builtins.str] = None,
        event_queue_arn: typing.Optional[builtins.str] = None,
        exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sample_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#path GlueCrawler#path}.
        :param connection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.
        :param dlq_event_queue_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#dlq_event_queue_arn GlueCrawler#dlq_event_queue_arn}.
        :param event_queue_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#event_queue_arn GlueCrawler#event_queue_arn}.
        :param exclusions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.
        :param sample_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#sample_size GlueCrawler#sample_size}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c5ac45a1fcaffd80f31c027d77a2cb5d4504087c3c075518d3543d14737d02)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument dlq_event_queue_arn", value=dlq_event_queue_arn, expected_type=type_hints["dlq_event_queue_arn"])
            check_type(argname="argument event_queue_arn", value=event_queue_arn, expected_type=type_hints["event_queue_arn"])
            check_type(argname="argument exclusions", value=exclusions, expected_type=type_hints["exclusions"])
            check_type(argname="argument sample_size", value=sample_size, expected_type=type_hints["sample_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if dlq_event_queue_arn is not None:
            self._values["dlq_event_queue_arn"] = dlq_event_queue_arn
        if event_queue_arn is not None:
            self._values["event_queue_arn"] = event_queue_arn
        if exclusions is not None:
            self._values["exclusions"] = exclusions
        if sample_size is not None:
            self._values["sample_size"] = sample_size

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#path GlueCrawler#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#connection_name GlueCrawler#connection_name}.'''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dlq_event_queue_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#dlq_event_queue_arn GlueCrawler#dlq_event_queue_arn}.'''
        result = self._values.get("dlq_event_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_queue_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#event_queue_arn GlueCrawler#event_queue_arn}.'''
        result = self._values.get("event_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#exclusions GlueCrawler#exclusions}.'''
        result = self._values.get("exclusions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sample_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#sample_size GlueCrawler#sample_size}.'''
        result = self._values.get("sample_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerS3Target(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerS3TargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerS3TargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__697552c178167fcb4eef170212b5baa7071b6616d5b0cc7566d964886484a366)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GlueCrawlerS3TargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc35815fb8eaf63191e38264b591692ad56e9fed777de1486cb9efe78f2c017)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GlueCrawlerS3TargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d405d143424eadd1c8792b45ae6f1787b141fb12b2b458951c14abddab0af086)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2203b335b10d644ff3d4ce43fa48df43fa02ad5a668a4a6667f9aeb59c37b144)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7902841d4a3fa51d5b8eeb826169cf96fc672616956ffc72e9dd5ae2417c571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerS3Target]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerS3Target]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerS3Target]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4b7b6ebece744d19beec3be94f455c9efd3d34f8a251ac856eced1a6782820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GlueCrawlerS3TargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerS3TargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__995d8373dda0a06c5e94200c2cf2185173d7bbea002245861a52668f4469d50a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConnectionName")
    def reset_connection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionName", []))

    @jsii.member(jsii_name="resetDlqEventQueueArn")
    def reset_dlq_event_queue_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDlqEventQueueArn", []))

    @jsii.member(jsii_name="resetEventQueueArn")
    def reset_event_queue_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventQueueArn", []))

    @jsii.member(jsii_name="resetExclusions")
    def reset_exclusions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusions", []))

    @jsii.member(jsii_name="resetSampleSize")
    def reset_sample_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleSize", []))

    @builtins.property
    @jsii.member(jsii_name="connectionNameInput")
    def connection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dlqEventQueueArnInput")
    def dlq_event_queue_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dlqEventQueueArnInput"))

    @builtins.property
    @jsii.member(jsii_name="eventQueueArnInput")
    def event_queue_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventQueueArnInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionsInput")
    def exclusions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleSizeInput")
    def sample_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

    @connection_name.setter
    def connection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57629122f25b3470d6cda3dd8069182e837bccc105c78c0f6ce83d21843ef606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dlqEventQueueArn")
    def dlq_event_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dlqEventQueueArn"))

    @dlq_event_queue_arn.setter
    def dlq_event_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f669f53370127645744431fe7ce84119fd3aa12c2b2bffd7daa198498bf81c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dlqEventQueueArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventQueueArn")
    def event_queue_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventQueueArn"))

    @event_queue_arn.setter
    def event_queue_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6c8c8ac1bd4a504dd11271c1a5db36297d15f13f7bcfba0d4710b50dde3d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventQueueArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusions")
    def exclusions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusions"))

    @exclusions.setter
    def exclusions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8c295070c47040487d5d853c24f540321de1a2bdd99402bbe43c73b3005e76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adc5fdfe296b6c58609fafad8594fcdbc57aded588644ca18dc259e225363f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleSize")
    def sample_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleSize"))

    @sample_size.setter
    def sample_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43711d29881348ee3e3a28d6ada50c2825ce99faf29069d7b233dba424649ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerS3Target]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerS3Target]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerS3Target]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b94db6d56b50a5021cd44f1b25cfce42b4c1d346de47f88c72040c1fe75255)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerSchemaChangePolicy",
    jsii_struct_bases=[],
    name_mapping={
        "delete_behavior": "deleteBehavior",
        "update_behavior": "updateBehavior",
    },
)
class GlueCrawlerSchemaChangePolicy:
    def __init__(
        self,
        *,
        delete_behavior: typing.Optional[builtins.str] = None,
        update_behavior: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delete_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#delete_behavior GlueCrawler#delete_behavior}.
        :param update_behavior: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#update_behavior GlueCrawler#update_behavior}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b168a4a105f3bdf826db49d7e4fc7f9d36174a9c0b54f9935e32b65ce6f1548)
            check_type(argname="argument delete_behavior", value=delete_behavior, expected_type=type_hints["delete_behavior"])
            check_type(argname="argument update_behavior", value=update_behavior, expected_type=type_hints["update_behavior"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_behavior is not None:
            self._values["delete_behavior"] = delete_behavior
        if update_behavior is not None:
            self._values["update_behavior"] = update_behavior

    @builtins.property
    def delete_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#delete_behavior GlueCrawler#delete_behavior}.'''
        result = self._values.get("delete_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/glue_crawler#update_behavior GlueCrawler#update_behavior}.'''
        result = self._values.get("update_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueCrawlerSchemaChangePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueCrawlerSchemaChangePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.glueCrawler.GlueCrawlerSchemaChangePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f71c8d06d6fbd96fd70ef02429ecb4ec3ce40186c6ae0bbf6b4977ed8c0714)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDeleteBehavior")
    def reset_delete_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteBehavior", []))

    @jsii.member(jsii_name="resetUpdateBehavior")
    def reset_update_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateBehavior", []))

    @builtins.property
    @jsii.member(jsii_name="deleteBehaviorInput")
    def delete_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="updateBehaviorInput")
    def update_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteBehavior")
    def delete_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteBehavior"))

    @delete_behavior.setter
    def delete_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76bf5842f067c80a2f8b68de469228013684c7f562deaa643c25ebcaa72e414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="updateBehavior")
    def update_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateBehavior"))

    @update_behavior.setter
    def update_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b49b0ddc274d8633b8e09737079d5fec1e0acb5a38b79ce55833e554a79a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GlueCrawlerSchemaChangePolicy]:
        return typing.cast(typing.Optional[GlueCrawlerSchemaChangePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GlueCrawlerSchemaChangePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79022f13929eefee1e455531eafd94332fcc7b5f081cdc50805b0e9d871ddf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GlueCrawler",
    "GlueCrawlerCatalogTarget",
    "GlueCrawlerCatalogTargetList",
    "GlueCrawlerCatalogTargetOutputReference",
    "GlueCrawlerConfig",
    "GlueCrawlerDeltaTarget",
    "GlueCrawlerDeltaTargetList",
    "GlueCrawlerDeltaTargetOutputReference",
    "GlueCrawlerDynamodbTarget",
    "GlueCrawlerDynamodbTargetList",
    "GlueCrawlerDynamodbTargetOutputReference",
    "GlueCrawlerHudiTarget",
    "GlueCrawlerHudiTargetList",
    "GlueCrawlerHudiTargetOutputReference",
    "GlueCrawlerIcebergTarget",
    "GlueCrawlerIcebergTargetList",
    "GlueCrawlerIcebergTargetOutputReference",
    "GlueCrawlerJdbcTarget",
    "GlueCrawlerJdbcTargetList",
    "GlueCrawlerJdbcTargetOutputReference",
    "GlueCrawlerLakeFormationConfiguration",
    "GlueCrawlerLakeFormationConfigurationOutputReference",
    "GlueCrawlerLineageConfiguration",
    "GlueCrawlerLineageConfigurationOutputReference",
    "GlueCrawlerMongodbTarget",
    "GlueCrawlerMongodbTargetList",
    "GlueCrawlerMongodbTargetOutputReference",
    "GlueCrawlerRecrawlPolicy",
    "GlueCrawlerRecrawlPolicyOutputReference",
    "GlueCrawlerS3Target",
    "GlueCrawlerS3TargetList",
    "GlueCrawlerS3TargetOutputReference",
    "GlueCrawlerSchemaChangePolicy",
    "GlueCrawlerSchemaChangePolicyOutputReference",
]

publication.publish()

def _typecheckingstub__2d4c65516ffdc5c97487ac31110b7c4525d049d77903d7a06b88e348de6b8c12(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database_name: builtins.str,
    name: builtins.str,
    role: builtins.str,
    catalog_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerCatalogTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[builtins.str] = None,
    delta_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDeltaTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDynamodbTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hudi_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerHudiTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iceberg_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerIcebergTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerJdbcTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lake_formation_configuration: typing.Optional[typing.Union[GlueCrawlerLakeFormationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    lineage_configuration: typing.Optional[typing.Union[GlueCrawlerLineageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    mongodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerMongodbTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    recrawl_policy: typing.Optional[typing.Union[GlueCrawlerRecrawlPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerS3Target, typing.Dict[builtins.str, typing.Any]]]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    schema_change_policy: typing.Optional[typing.Union[GlueCrawlerSchemaChangePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    table_prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__4c232dadb53a6328de083f0e910b75bc70976fa9799debf2e9003ca9a606ea1c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01247cd1643d642f5c04cb3361ea0af393745714337ee375b3e42d94448f91da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerCatalogTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912d3cd66530321712b6bd9a19cccebc436fa04763a144e6d829ff9f0351fb3a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDeltaTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b64061c517f0535dad3a626445b29d5a6698b6fe33f57e64f338b6e5ae5833a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDynamodbTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25592c1ebbbdcb60c04d49667d62ec3444dde01117f8ccb051b4e78de85dd79(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerHudiTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7e40e52417b691b77e5666c4551de06d69e33c6de64eafc092f8eb15e09604(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerIcebergTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fa5d3e8e992fdf8b5e5cf9889e90c183c323e6b409be5e0c5e6174bcb4615f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerJdbcTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45bfbaec671f67f29b90e95bcfece0bb33fdb425fca839c5685cfc29b092ae61(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerMongodbTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba686db54bf400e9f82b25b7751b28815fe8447191112e9fe0408f7489dece7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerS3Target, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e584f9ae52ef56c0ae0cd226cd421f19a5bc8a7936cee0646bb0fd6780a4f0fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973dfc8b8574af4a0abd0ec6be229d9db660bb6f4ed2a2deb45546806c401560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860d5bafa378fe75f2bfe4f2f6dfcb35c19d2318a6946bf7e4501f131080da42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd0ed47844462ff012f1a932cf8108c1e425ff67a2accbef85bd9cee8986e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc47d2abe4b5d2a8815ab3eee25bf56784b10da31fc343134a0d19e76c1749b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb70e6ec91748f678074ff5c83dd3c6651398e3210e8a2961e273e3bffbe547(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c997ffc3551344a35cab96f3d3ed77fcb63d2e7bdd725dffb72f0e70d31e13f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ce870459bbffbdd9c7c9f394d96db142e4b36e92865b3cd43735526e67f3b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b067cb0c1fb730878cf9e3b445b09490354dffcad681f83ed160f9580d48e290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df06198ceade2405bae6b568713c32cefa23f3c07ae12edd690850287c1783d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd137d7ad61d863ab66f66d2c446e697b9c28275426d89b6146021bd9b3ca8e3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1af8e2ea3d47ebd92b0fa3234038ce1f773c9fdf26dc7c70702c896ae3669e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5a3c6ad3aa8e0b625d2a87b05df251418e59496dcf56b73c199e05b38bde77(
    *,
    database_name: builtins.str,
    tables: typing.Sequence[builtins.str],
    connection_name: typing.Optional[builtins.str] = None,
    dlq_event_queue_arn: typing.Optional[builtins.str] = None,
    event_queue_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c963ab98113c234d7865ae295c4c0daf3da0858727e68a486daf53ddca89b5c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881f46f92fbec060ee94689a91656688378a5bd3bd29056b67db532749f786d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ffe51bec2236c27931d870e4a4b7d0bc424c063aed6c14d539a92fe8c951d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2365102d07208c93159d18c53ba2155f2311816df8bcc19c821f7a32c3c0281b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1d3035adbe27fcaf7ffc59f070bcad22165b210cbe31149d7813be873ee04b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e515f41d9075e58415356e3f4106e1ef3b1099d8f22e3505940bb8f569a4fa43(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerCatalogTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f400655704386773cc09ffdd489f52c0e80b28f99e73ea894198d3f05cfd2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0043a5400b19467313db56e0273fe86f573e8a642de0a0f0cbe10a461eb5a83c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047e2247f0b058cdfe4aef46f7a3c9e84847e9c11f02cbe9f72a3997f27fc060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a1f94402b2ffa06002e574a2ba7a4dfcd134c12c9e41b612ca7875faaa2b4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37af715e5b76ac53965b2d18452ade1a7242231c851258ac7f4abda0f9bb68e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e5d9bc5a4bd9f206706033b290b79457f7178ce38f2e2600ce8e9184a5bb3f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d1782aacbf4c05f47d673cb65bd98c84540f3f302910705150731c5fd54e38(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerCatalogTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70be716cf9fd8495efcfe58a5112ee47ab881fc2603bf65028ec1ae23a6c35a4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database_name: builtins.str,
    name: builtins.str,
    role: builtins.str,
    catalog_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerCatalogTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[builtins.str] = None,
    delta_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDeltaTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerDynamodbTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hudi_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerHudiTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    iceberg_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerIcebergTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    jdbc_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerJdbcTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    lake_formation_configuration: typing.Optional[typing.Union[GlueCrawlerLakeFormationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    lineage_configuration: typing.Optional[typing.Union[GlueCrawlerLineageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    mongodb_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerMongodbTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    recrawl_policy: typing.Optional[typing.Union[GlueCrawlerRecrawlPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GlueCrawlerS3Target, typing.Dict[builtins.str, typing.Any]]]]] = None,
    schedule: typing.Optional[builtins.str] = None,
    schema_change_policy: typing.Optional[typing.Union[GlueCrawlerSchemaChangePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    security_configuration: typing.Optional[builtins.str] = None,
    table_prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ed98b8be4f732e000212784a03756b4296bf66ae2780f62783f33ea462438e(
    *,
    delta_tables: typing.Sequence[builtins.str],
    write_manifest: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    connection_name: typing.Optional[builtins.str] = None,
    create_native_delta_table: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607a53e23e9f9d9465c5ac39aa1c6f9155e3565076ab7d838883ef44fdf281b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c4d35061247d5d87f06af80e2a400b3678f0acb78a07a73eb2886cdd186418(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6df37594b034a62085c16006b47fb155184fd6dc81c69cf4a72a90ee176258(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200c45fed2ed2b771c616f3fb5797d569124648fe2041e02d564d7062d36e468(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01296bcee7baca8b2f9c8b0bb453f700d118f9c5c747901a08dc1a6b01c5566(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aab1e5b95303388984b0ee1e2b2f3dc76e6e1d97a39029dd611318a177e2ce8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDeltaTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8ba6e99234d78fdc41a34f0be8a8b1d880762f5b09ce4f1fe9b181de2a5d0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c277d9503eb195d0dc04b592d593158a363c153c3da44b75161432d7cbd8f47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9c12bae98879b12680838fa6f48c6ab2e3bf0184c08ae64fd48be3cc549ba3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c68c35523584d2f06c35d7555a2d325ab23725427cfdaf1f632756cf93074a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1910ce883e709de44e96dfc4b6e16fa5e062c01f169b80a0abb49629ef83fa8e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2aad4650d8a07a487da2d01a9039763272bd53ee1cfa4f4358ebf9795b09120(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDeltaTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4a3f9ae5a62dcf48f95b95ae4cfb17eec77a8a937bec64d924b129aff37140(
    *,
    path: builtins.str,
    scan_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scan_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332f4cb840975c65b44f25deecb73d20b5ac9c1257629856f0eff6ffc92a28b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a0cefbc4b86253290246904b5321246b466422522b84cabb943b64f95d8ab3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0973f5b98721085b86ae96b6546aa84283905fafe141dda41d7685c317e4f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec4d86ad2e0b93fd651b158196304ee96dd47deca09861185bd3f28a09d3050(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da90b5ca6369bd2cbeb55f787c2f1c1cfbe7d471cb9911fa47ceebba86c10182(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e02558b564e1c03622210cbb4c90a9558f5d766f700cf19cd8b337d8ee35678(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerDynamodbTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e642bbc08e1ffb36584f3414362e61e8d36667ea7588339feca83f6231d353fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af26dcc3cdacc1d02fed166eedfe88b32be1dcbd4b22871ff3749d263292e95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78da00f17249e51add1c9f3bfad74712c3601ac4848dd21b9514eef9a65a9ec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649dee3d6f76c0d7aeff52085948384148057a2d6fd41afb083abefa0e673cfa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011d851fb0e8529633716501cb72028e9c1e598b069bde7ed1f783e272ec87e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerDynamodbTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b59d4c21a8c34b546f5734f88b4475d75154bc9c3df24c4b6a270bd99dead4(
    *,
    maximum_traversal_depth: jsii.Number,
    paths: typing.Sequence[builtins.str],
    connection_name: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca47e1175924bc859361c82e08c173d3324f4182f0d6800c20e91227d7ac0c73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733286d54cb3f0dcb3f38bbf4e6173436641e6e4c3bbf4b621bfada3e0991a0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b71bbd38ceda6fa15388466debbfcaad78006e0f28a8f3659470e3990ec204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8d87e37be3f5e6ef626def560eced2c550faa9719858c4e4bdbffa81970923(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9bce204ad7de78194e168774df6abd14a95b2ed1c95f14b94f6b8dd47f371c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d5718653a4bee230a1fe904ea0d19abb2b42d06acb727b3ef2f95f125d987e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerHudiTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a76c4b42d96c78e8061edd4c9434a2dd90e75dd76b855045d8c9a1eccfadb8e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f566821962a0b85275f6615817c8ab59698c6985a48241090257c72d469484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148e2eb5e5cba11f6a2d3d87f20c6291035122d61847416caa0fb2a9268e19f2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fd6dad300fbe2cb03bff9ebb29ba74e2c65e01b2e27e134660001f8c22813c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdad4a149e67579f5bc863a6d20e80767264c99197c2cc7efdf4264cb22ade21(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4764551d2e925a363f2dd8bd5c4d44d7261bea506e13f95ce2524f06fa657fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerHudiTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6595cc4d44306f256fb9c29efa49c4da2ea22430d66c48d0d599f8d18ff34ae(
    *,
    maximum_traversal_depth: jsii.Number,
    paths: typing.Sequence[builtins.str],
    connection_name: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f960b027e290fdfa42daab7aceaf2b443bc9ddd2ff03af5486c2ea7bc5652a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8a26763b25715a67f240daeb9dba096f7ba00052b15e49d124423d9409d971(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c72c8a28d74d3056a42ec4ca1541a074b35e72cc9eeba6811fc1cb9bc6b0fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24f240114faf40db256b49399bcac1137ed03dc4f0d52e6af1f2840b58b4761(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eabbc8ccb5aa769695cd4a6b597e7fb08b04ea484b75394e4cf703e7bcdc390(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fe46c7a5eda5a5995cfe04ccd4f21036915d3a2a5d282819f04e37dcffb14a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerIcebergTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e5481eecad3db65f3651a28c6c1da8be16d82790ff60fba12e5bba1440dd74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f2a1aa6b52828b3d6d000b6f7a572b6c0f3546c6b884b4b5a14f105c22f893(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c38dfa797252c5a2af1a9cb3e8131460d20008c1a2b1303d310586c236f7a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197d70afc23e5f5b95934b88a5f80eca1bd53aea791e2cb147388fc90334061a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888d804ac7d48e6643bb1f2492e88f865dd6c23b359bb4328dcb91cbff16639b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168f33a5363df9b342d86ba44ce81f5cf81fdfc921883b451164aee9f2cd63f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerIcebergTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0b8ca35ae61e40fe2419e036b15295e1b709d068551322d2b7790a382637bc(
    *,
    connection_name: builtins.str,
    path: builtins.str,
    enable_additional_metadata: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d1fb9ffd52414ab9521db0d99a9e4d3664f0e1d5f1b4d899a636b61a7dc018(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904a715d97a047288a58d5fd88fa49dda77a9c334aa3bdd4ab3168d1f4122fb1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20a204827fb99f47cbc90f3ebe6ff1e74ed3876852ab69837bdc75e8c3bf3ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c99379deb0d5129c8aa248a455f0cf503567c2271a5776e64b35c9dc9236ad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c390d3709dd488c2be32a084c73c3703d67f18199b9a75e77269351b80406b6c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ba6d128ded4c284e2ca10862813e05afeea3e1022f89175f57b38f848b94bc5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerJdbcTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbe039e5147743f174d50d3ce6486aa931cdd5038b988099abb8382f2422956(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05e0acf1b764dd5f487ab58846ff59298bb558ff9dbcd3883c2845014135fe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4357d6fd6f5e14053e8557bdfdd935677f2c98b3bce44b55a3ecfebbf59bf4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1973c7014e553b6e233bef92aeb5601a03e2a5231e03dbaa11b19f474e683e94(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4861b6859b3b5b44a1c8c3a5ee1210588035619b94fd0a65e3996eb0884e93ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f872978356c83674adfa7b73077f1f3e4265fa28e5237648b514b593fe2140e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerJdbcTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49750b032f075036e4cb1870abcf9354615920dda4bafdcf65507f92b09a6df(
    *,
    account_id: typing.Optional[builtins.str] = None,
    use_lake_formation_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b71e993e3d968fffc40fd4c46f697239c828cc4d807d0032648d62a2ac0cbe4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f032077010ab1f117d72bbf674ca594c1e494573aa21d9602b7ea25356bc00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aead4a0401aeed761649f783bc3e4927c7583e0f93caae69dffee3e0efc792c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84918d978ee85f79f924f1e80eaaef3be1d11a8a68da3aeb7e00b01837705546(
    value: typing.Optional[GlueCrawlerLakeFormationConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab316959ad80c77b0f3d5648271572772b7d32698e581a1fd5a584aadc1b3140(
    *,
    crawler_lineage_settings: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb5c9377c139e0503834b6cf2dbc2a0a70fe818972f8fd2eb93f7c83d16ccf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a8ebad655302f578df47e11654d2601dd8be03ce52e76832564f5322629467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13346889e5296420b2003090b2d7b7671dd257873bbb439a911973aac724c89d(
    value: typing.Optional[GlueCrawlerLineageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25f9a719a955db4fe04c0aa1fb1e2a64978d46f5c22c517d99534b2bb75dd39(
    *,
    connection_name: builtins.str,
    path: builtins.str,
    scan_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0532ab563ea17dc6ac7afd7d63a5bca04fee1c8919b5289bc14f30573a69b1af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d25cd7535eda40581b558a0732c31101e9ff645f8c4ff9ed7f770dc1ff4945(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78dc79d541254caf3af1e75ba2c4731af0c9df5f5118e23dcb58931d9b2b409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bed9d61c91682193f9ea7da6aff492a258a64dd60ba62fb0937a4a76407278(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb6a0e0792768c81fd33a4b336b5277869dfff83cc1a526431431d4997679a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc2f32cd9ddefcdfdf51eab04a7bbf59fc11ab1802a22690047d397aa9d621d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerMongodbTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d66096ef0db6de342a39ed6572b527106e91c632cce137adc3cfcc808f64c9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e675d6b1089ccbcf8f199a76297df15fa225f04039adfd96c0c5771c1076290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7670f19760b1eb506a6a56f399ea0d100c10803e9bf3cfd1ccc8d0f97e975542(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda86e4841b088bb6c0d4dc1d2de7cbaf664ee41576edbac3ccf751992fec570(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5743671231d696e9c7049e487b871321a8300ed3dcd0e769b159e7e6c83dbf78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerMongodbTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5905d83bf20d4a60d912f7ad07b73c539718f183b9e84f3efe95d79adf79e439(
    *,
    recrawl_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5926ac874651895380a800f7b30949c030898f54df9af4abfef45cfe284c1b58(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fe2bde03cce5707f9623d63d2578ec402928078844985141a004d5c16bac18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2dc17b27ceeceb4def47d997803f6925c9ea1e4f139fd80b22d72e937c5ceef(
    value: typing.Optional[GlueCrawlerRecrawlPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c5ac45a1fcaffd80f31c027d77a2cb5d4504087c3c075518d3543d14737d02(
    *,
    path: builtins.str,
    connection_name: typing.Optional[builtins.str] = None,
    dlq_event_queue_arn: typing.Optional[builtins.str] = None,
    event_queue_arn: typing.Optional[builtins.str] = None,
    exclusions: typing.Optional[typing.Sequence[builtins.str]] = None,
    sample_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697552c178167fcb4eef170212b5baa7071b6616d5b0cc7566d964886484a366(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc35815fb8eaf63191e38264b591692ad56e9fed777de1486cb9efe78f2c017(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d405d143424eadd1c8792b45ae6f1787b141fb12b2b458951c14abddab0af086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2203b335b10d644ff3d4ce43fa48df43fa02ad5a668a4a6667f9aeb59c37b144(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7902841d4a3fa51d5b8eeb826169cf96fc672616956ffc72e9dd5ae2417c571(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4b7b6ebece744d19beec3be94f455c9efd3d34f8a251ac856eced1a6782820(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GlueCrawlerS3Target]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995d8373dda0a06c5e94200c2cf2185173d7bbea002245861a52668f4469d50a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57629122f25b3470d6cda3dd8069182e837bccc105c78c0f6ce83d21843ef606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f669f53370127645744431fe7ce84119fd3aa12c2b2bffd7daa198498bf81c74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6c8c8ac1bd4a504dd11271c1a5db36297d15f13f7bcfba0d4710b50dde3d11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8c295070c47040487d5d853c24f540321de1a2bdd99402bbe43c73b3005e76(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adc5fdfe296b6c58609fafad8594fcdbc57aded588644ca18dc259e225363f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43711d29881348ee3e3a28d6ada50c2825ce99faf29069d7b233dba424649ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b94db6d56b50a5021cd44f1b25cfce42b4c1d346de47f88c72040c1fe75255(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GlueCrawlerS3Target]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b168a4a105f3bdf826db49d7e4fc7f9d36174a9c0b54f9935e32b65ce6f1548(
    *,
    delete_behavior: typing.Optional[builtins.str] = None,
    update_behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f71c8d06d6fbd96fd70ef02429ecb4ec3ce40186c6ae0bbf6b4977ed8c0714(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76bf5842f067c80a2f8b68de469228013684c7f562deaa643c25ebcaa72e414(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b49b0ddc274d8633b8e09737079d5fec1e0acb5a38b79ce55833e554a79a1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79022f13929eefee1e455531eafd94332fcc7b5f081cdc50805b0e9d871ddf0(
    value: typing.Optional[GlueCrawlerSchemaChangePolicy],
) -> None:
    """Type checking stubs"""
    pass
