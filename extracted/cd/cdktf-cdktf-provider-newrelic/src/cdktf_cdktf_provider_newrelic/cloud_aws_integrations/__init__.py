r'''
# `newrelic_cloud_aws_integrations`

Refer to the Terraform Registry for docs: [`newrelic_cloud_aws_integrations`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations).
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


class CloudAwsIntegrations(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrations",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations newrelic_cloud_aws_integrations}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        alb: typing.Optional[typing.Union["CloudAwsIntegrationsAlb", typing.Dict[builtins.str, typing.Any]]] = None,
        api_gateway: typing.Optional[typing.Union["CloudAwsIntegrationsApiGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scaling: typing.Optional[typing.Union["CloudAwsIntegrationsAutoScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_app_sync: typing.Optional[typing.Union["CloudAwsIntegrationsAwsAppSync", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_athena: typing.Optional[typing.Union["CloudAwsIntegrationsAwsAthena", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_auto_discovery: typing.Optional[typing.Union["CloudAwsIntegrationsAwsAutoDiscovery", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_cognito: typing.Optional[typing.Union["CloudAwsIntegrationsAwsCognito", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_connect: typing.Optional[typing.Union["CloudAwsIntegrationsAwsConnect", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_direct_connect: typing.Optional[typing.Union["CloudAwsIntegrationsAwsDirectConnect", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_fsx: typing.Optional[typing.Union["CloudAwsIntegrationsAwsFsx", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_glue: typing.Optional[typing.Union["CloudAwsIntegrationsAwsGlue", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_kinesis_analytics: typing.Optional[typing.Union["CloudAwsIntegrationsAwsKinesisAnalytics", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_media_convert: typing.Optional[typing.Union["CloudAwsIntegrationsAwsMediaConvert", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_media_package_vod: typing.Optional[typing.Union["CloudAwsIntegrationsAwsMediaPackageVod", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_mq: typing.Optional[typing.Union["CloudAwsIntegrationsAwsMq", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_msk: typing.Optional[typing.Union["CloudAwsIntegrationsAwsMsk", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_neptune: typing.Optional[typing.Union["CloudAwsIntegrationsAwsNeptune", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_qldb: typing.Optional[typing.Union["CloudAwsIntegrationsAwsQldb", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_route53_resolver: typing.Optional[typing.Union["CloudAwsIntegrationsAwsRoute53Resolver", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_states: typing.Optional[typing.Union["CloudAwsIntegrationsAwsStates", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_transit_gateway: typing.Optional[typing.Union["CloudAwsIntegrationsAwsTransitGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_waf: typing.Optional[typing.Union["CloudAwsIntegrationsAwsWaf", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_wafv2: typing.Optional[typing.Union["CloudAwsIntegrationsAwsWafv2", typing.Dict[builtins.str, typing.Any]]] = None,
        billing: typing.Optional[typing.Union["CloudAwsIntegrationsBilling", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudfront: typing.Optional[typing.Union["CloudAwsIntegrationsCloudfront", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudtrail: typing.Optional[typing.Union["CloudAwsIntegrationsCloudtrail", typing.Dict[builtins.str, typing.Any]]] = None,
        doc_db: typing.Optional[typing.Union["CloudAwsIntegrationsDocDb", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb: typing.Optional[typing.Union["CloudAwsIntegrationsDynamodb", typing.Dict[builtins.str, typing.Any]]] = None,
        ebs: typing.Optional[typing.Union["CloudAwsIntegrationsEbs", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2: typing.Optional[typing.Union["CloudAwsIntegrationsEc2", typing.Dict[builtins.str, typing.Any]]] = None,
        ecs: typing.Optional[typing.Union["CloudAwsIntegrationsEcs", typing.Dict[builtins.str, typing.Any]]] = None,
        efs: typing.Optional[typing.Union["CloudAwsIntegrationsEfs", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticache: typing.Optional[typing.Union["CloudAwsIntegrationsElasticache", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticbeanstalk: typing.Optional[typing.Union["CloudAwsIntegrationsElasticbeanstalk", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch: typing.Optional[typing.Union["CloudAwsIntegrationsElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        elb: typing.Optional[typing.Union["CloudAwsIntegrationsElb", typing.Dict[builtins.str, typing.Any]]] = None,
        emr: typing.Optional[typing.Union["CloudAwsIntegrationsEmr", typing.Dict[builtins.str, typing.Any]]] = None,
        health: typing.Optional[typing.Union["CloudAwsIntegrationsHealth", typing.Dict[builtins.str, typing.Any]]] = None,
        iam: typing.Optional[typing.Union["CloudAwsIntegrationsIam", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        iot: typing.Optional[typing.Union["CloudAwsIntegrationsIot", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis: typing.Optional[typing.Union["CloudAwsIntegrationsKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_firehose: typing.Optional[typing.Union["CloudAwsIntegrationsKinesisFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_: typing.Optional[typing.Union["CloudAwsIntegrationsLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        rds: typing.Optional[typing.Union["CloudAwsIntegrationsRds", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["CloudAwsIntegrationsRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        route53: typing.Optional[typing.Union["CloudAwsIntegrationsRoute53", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["CloudAwsIntegrationsS3", typing.Dict[builtins.str, typing.Any]]] = None,
        ses: typing.Optional[typing.Union["CloudAwsIntegrationsSes", typing.Dict[builtins.str, typing.Any]]] = None,
        sns: typing.Optional[typing.Union["CloudAwsIntegrationsSns", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs: typing.Optional[typing.Union["CloudAwsIntegrationsSqs", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_advisor: typing.Optional[typing.Union["CloudAwsIntegrationsTrustedAdvisor", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[typing.Union["CloudAwsIntegrationsVpc", typing.Dict[builtins.str, typing.Any]]] = None,
        x_ray: typing.Optional[typing.Union["CloudAwsIntegrationsXRay", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations newrelic_cloud_aws_integrations} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param linked_account_id: The ID of the linked AWS account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#linked_account_id CloudAwsIntegrations#linked_account_id}
        :param account_id: The ID of the account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#account_id CloudAwsIntegrations#account_id}
        :param alb: alb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#alb CloudAwsIntegrations#alb}
        :param api_gateway: api_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#api_gateway CloudAwsIntegrations#api_gateway}
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#auto_scaling CloudAwsIntegrations#auto_scaling}
        :param aws_app_sync: aws_app_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_app_sync CloudAwsIntegrations#aws_app_sync}
        :param aws_athena: aws_athena block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_athena CloudAwsIntegrations#aws_athena}
        :param aws_auto_discovery: aws_auto_discovery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_auto_discovery CloudAwsIntegrations#aws_auto_discovery}
        :param aws_cognito: aws_cognito block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_cognito CloudAwsIntegrations#aws_cognito}
        :param aws_connect: aws_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_connect CloudAwsIntegrations#aws_connect}
        :param aws_direct_connect: aws_direct_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_direct_connect CloudAwsIntegrations#aws_direct_connect}
        :param aws_fsx: aws_fsx block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_fsx CloudAwsIntegrations#aws_fsx}
        :param aws_glue: aws_glue block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_glue CloudAwsIntegrations#aws_glue}
        :param aws_kinesis_analytics: aws_kinesis_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_kinesis_analytics CloudAwsIntegrations#aws_kinesis_analytics}
        :param aws_media_convert: aws_media_convert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_media_convert CloudAwsIntegrations#aws_media_convert}
        :param aws_media_package_vod: aws_media_package_vod block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_media_package_vod CloudAwsIntegrations#aws_media_package_vod}
        :param aws_mq: aws_mq block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_mq CloudAwsIntegrations#aws_mq}
        :param aws_msk: aws_msk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_msk CloudAwsIntegrations#aws_msk}
        :param aws_neptune: aws_neptune block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_neptune CloudAwsIntegrations#aws_neptune}
        :param aws_qldb: aws_qldb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_qldb CloudAwsIntegrations#aws_qldb}
        :param aws_route53_resolver: aws_route53resolver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_route53resolver CloudAwsIntegrations#aws_route53resolver}
        :param aws_states: aws_states block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_states CloudAwsIntegrations#aws_states}
        :param aws_transit_gateway: aws_transit_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_transit_gateway CloudAwsIntegrations#aws_transit_gateway}
        :param aws_waf: aws_waf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_waf CloudAwsIntegrations#aws_waf}
        :param aws_wafv2: aws_wafv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_wafv2 CloudAwsIntegrations#aws_wafv2}
        :param billing: billing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#billing CloudAwsIntegrations#billing}
        :param cloudfront: cloudfront block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#cloudfront CloudAwsIntegrations#cloudfront}
        :param cloudtrail: cloudtrail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#cloudtrail CloudAwsIntegrations#cloudtrail}
        :param doc_db: doc_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#doc_db CloudAwsIntegrations#doc_db}
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#dynamodb CloudAwsIntegrations#dynamodb}
        :param ebs: ebs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ebs CloudAwsIntegrations#ebs}
        :param ec2: ec2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ec2 CloudAwsIntegrations#ec2}
        :param ecs: ecs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ecs CloudAwsIntegrations#ecs}
        :param efs: efs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#efs CloudAwsIntegrations#efs}
        :param elasticache: elasticache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticache CloudAwsIntegrations#elasticache}
        :param elasticbeanstalk: elasticbeanstalk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticbeanstalk CloudAwsIntegrations#elasticbeanstalk}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticsearch CloudAwsIntegrations#elasticsearch}
        :param elb: elb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elb CloudAwsIntegrations#elb}
        :param emr: emr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#emr CloudAwsIntegrations#emr}
        :param health: health block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#health CloudAwsIntegrations#health}
        :param iam: iam block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#iam CloudAwsIntegrations#iam}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#id CloudAwsIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iot: iot block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#iot CloudAwsIntegrations#iot}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#kinesis CloudAwsIntegrations#kinesis}
        :param kinesis_firehose: kinesis_firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#kinesis_firehose CloudAwsIntegrations#kinesis_firehose}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#lambda CloudAwsIntegrations#lambda}
        :param rds: rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#rds CloudAwsIntegrations#rds}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#redshift CloudAwsIntegrations#redshift}
        :param route53: route53 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#route53 CloudAwsIntegrations#route53}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#s3 CloudAwsIntegrations#s3}
        :param ses: ses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ses CloudAwsIntegrations#ses}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#sns CloudAwsIntegrations#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#sqs CloudAwsIntegrations#sqs}
        :param trusted_advisor: trusted_advisor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#trusted_advisor CloudAwsIntegrations#trusted_advisor}
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#vpc CloudAwsIntegrations#vpc}
        :param x_ray: x_ray block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#x_ray CloudAwsIntegrations#x_ray}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218636da2f5c84b07b8f11f887c728956d546cee837b90d553762da5832a9fd8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudAwsIntegrationsConfig(
            linked_account_id=linked_account_id,
            account_id=account_id,
            alb=alb,
            api_gateway=api_gateway,
            auto_scaling=auto_scaling,
            aws_app_sync=aws_app_sync,
            aws_athena=aws_athena,
            aws_auto_discovery=aws_auto_discovery,
            aws_cognito=aws_cognito,
            aws_connect=aws_connect,
            aws_direct_connect=aws_direct_connect,
            aws_fsx=aws_fsx,
            aws_glue=aws_glue,
            aws_kinesis_analytics=aws_kinesis_analytics,
            aws_media_convert=aws_media_convert,
            aws_media_package_vod=aws_media_package_vod,
            aws_mq=aws_mq,
            aws_msk=aws_msk,
            aws_neptune=aws_neptune,
            aws_qldb=aws_qldb,
            aws_route53_resolver=aws_route53_resolver,
            aws_states=aws_states,
            aws_transit_gateway=aws_transit_gateway,
            aws_waf=aws_waf,
            aws_wafv2=aws_wafv2,
            billing=billing,
            cloudfront=cloudfront,
            cloudtrail=cloudtrail,
            doc_db=doc_db,
            dynamodb=dynamodb,
            ebs=ebs,
            ec2=ec2,
            ecs=ecs,
            efs=efs,
            elasticache=elasticache,
            elasticbeanstalk=elasticbeanstalk,
            elasticsearch=elasticsearch,
            elb=elb,
            emr=emr,
            health=health,
            iam=iam,
            id=id,
            iot=iot,
            kinesis=kinesis,
            kinesis_firehose=kinesis_firehose,
            lambda_=lambda_,
            rds=rds,
            redshift=redshift,
            route53=route53,
            s3=s3,
            ses=ses,
            sns=sns,
            sqs=sqs,
            trusted_advisor=trusted_advisor,
            vpc=vpc,
            x_ray=x_ray,
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
        '''Generates CDKTF code for importing a CloudAwsIntegrations resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudAwsIntegrations to import.
        :param import_from_id: The id of the existing CloudAwsIntegrations that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudAwsIntegrations to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c748f9b66efa26a1d6b8f71f9197de4e1828f69db8b7c07ee5aa6a94f2a0e77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlb")
    def put_alb(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        load_balancer_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param load_balancer_prefixes: Specify each name or prefix for the LBs that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#load_balancer_prefixes CloudAwsIntegrations#load_balancer_prefixes}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsAlb(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            load_balancer_prefixes=load_balancer_prefixes,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putAlb", [value]))

    @jsii.member(jsii_name="putApiGateway")
    def put_api_gateway(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        stage_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param stage_prefixes: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#stage_prefixes CloudAwsIntegrations#stage_prefixes}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsApiGateway(
            aws_regions=aws_regions,
            metrics_polling_interval=metrics_polling_interval,
            stage_prefixes=stage_prefixes,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putApiGateway", [value]))

    @jsii.member(jsii_name="putAutoScaling")
    def put_auto_scaling(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAutoScaling(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScaling", [value]))

    @jsii.member(jsii_name="putAwsAppSync")
    def put_aws_app_sync(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsAppSync(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAppSync", [value]))

    @jsii.member(jsii_name="putAwsAthena")
    def put_aws_athena(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsAthena(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAthena", [value]))

    @jsii.member(jsii_name="putAwsAutoDiscovery")
    def put_aws_auto_discovery(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsAutoDiscovery(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsAutoDiscovery", [value]))

    @jsii.member(jsii_name="putAwsCognito")
    def put_aws_cognito(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsCognito(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsCognito", [value]))

    @jsii.member(jsii_name="putAwsConnect")
    def put_aws_connect(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsConnect(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsConnect", [value]))

    @jsii.member(jsii_name="putAwsDirectConnect")
    def put_aws_direct_connect(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsDirectConnect(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsDirectConnect", [value]))

    @jsii.member(jsii_name="putAwsFsx")
    def put_aws_fsx(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsFsx(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsFsx", [value]))

    @jsii.member(jsii_name="putAwsGlue")
    def put_aws_glue(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsGlue(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsGlue", [value]))

    @jsii.member(jsii_name="putAwsKinesisAnalytics")
    def put_aws_kinesis_analytics(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsKinesisAnalytics(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsKinesisAnalytics", [value]))

    @jsii.member(jsii_name="putAwsMediaConvert")
    def put_aws_media_convert(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsMediaConvert(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsMediaConvert", [value]))

    @jsii.member(jsii_name="putAwsMediaPackageVod")
    def put_aws_media_package_vod(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsMediaPackageVod(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsMediaPackageVod", [value]))

    @jsii.member(jsii_name="putAwsMq")
    def put_aws_mq(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsMq(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsMq", [value]))

    @jsii.member(jsii_name="putAwsMsk")
    def put_aws_msk(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsMsk(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsMsk", [value]))

    @jsii.member(jsii_name="putAwsNeptune")
    def put_aws_neptune(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsNeptune(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsNeptune", [value]))

    @jsii.member(jsii_name="putAwsQldb")
    def put_aws_qldb(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsQldb(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsQldb", [value]))

    @jsii.member(jsii_name="putAwsRoute53Resolver")
    def put_aws_route53_resolver(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsRoute53Resolver(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsRoute53Resolver", [value]))

    @jsii.member(jsii_name="putAwsStates")
    def put_aws_states(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsStates(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsStates", [value]))

    @jsii.member(jsii_name="putAwsTransitGateway")
    def put_aws_transit_gateway(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsTransitGateway(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsTransitGateway", [value]))

    @jsii.member(jsii_name="putAwsWaf")
    def put_aws_waf(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsWaf(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsWaf", [value]))

    @jsii.member(jsii_name="putAwsWafv2")
    def put_aws_wafv2(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsAwsWafv2(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsWafv2", [value]))

    @jsii.member(jsii_name="putBilling")
    def put_billing(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsBilling(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putBilling", [value]))

    @jsii.member(jsii_name="putCloudfront")
    def put_cloudfront(
        self,
        *,
        fetch_lambdas_at_edge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fetch_lambdas_at_edge: Specify if Lambdas@Edge should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_lambdas_at_edge CloudAwsIntegrations#fetch_lambdas_at_edge}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsCloudfront(
            fetch_lambdas_at_edge=fetch_lambdas_at_edge,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putCloudfront", [value]))

    @jsii.member(jsii_name="putCloudtrail")
    def put_cloudtrail(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsCloudtrail(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putCloudtrail", [value]))

    @jsii.member(jsii_name="putDocDb")
    def put_doc_db(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsDocDb(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putDocDb", [value]))

    @jsii.member(jsii_name="putDynamodb")
    def put_dynamodb(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsDynamodb(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putDynamodb", [value]))

    @jsii.member(jsii_name="putEbs")
    def put_ebs(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsEbs(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putEbs", [value]))

    @jsii.member(jsii_name="putEc2")
    def put_ec2(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        duplicate_ec2_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param duplicate_ec2_tags: Specify if the old legacy metadata and tag names have to be kept, it will consume more ingest data size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#duplicate_ec2_tags CloudAwsIntegrations#duplicate_ec2_tags}
        :param fetch_ip_addresses: Specify if IP addresses of ec2 instance should be collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_ip_addresses CloudAwsIntegrations#fetch_ip_addresses}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsEc2(
            aws_regions=aws_regions,
            duplicate_ec2_tags=duplicate_ec2_tags,
            fetch_ip_addresses=fetch_ip_addresses,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putEc2", [value]))

    @jsii.member(jsii_name="putEcs")
    def put_ecs(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsEcs(
            aws_regions=aws_regions,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putEcs", [value]))

    @jsii.member(jsii_name="putEfs")
    def put_efs(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsEfs(
            aws_regions=aws_regions,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putEfs", [value]))

    @jsii.member(jsii_name="putElasticache")
    def put_elasticache(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsElasticache(
            aws_regions=aws_regions,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putElasticache", [value]))

    @jsii.member(jsii_name="putElasticbeanstalk")
    def put_elasticbeanstalk(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsElasticbeanstalk(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putElasticbeanstalk", [value]))

    @jsii.member(jsii_name="putElasticsearch")
    def put_elasticsearch(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_nodes: Specify if metrics should be collected for nodes. Turning it on will increase the number of API calls made to CloudWatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_nodes CloudAwsIntegrations#fetch_nodes}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsElasticsearch(
            aws_regions=aws_regions,
            fetch_nodes=fetch_nodes,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putElasticsearch", [value]))

    @jsii.member(jsii_name="putElb")
    def put_elb(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsElb(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
        )

        return typing.cast(None, jsii.invoke(self, "putElb", [value]))

    @jsii.member(jsii_name="putEmr")
    def put_emr(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsEmr(
            aws_regions=aws_regions,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putEmr", [value]))

    @jsii.member(jsii_name="putHealth")
    def put_health(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsHealth(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putHealth", [value]))

    @jsii.member(jsii_name="putIam")
    def put_iam(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsIam(
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putIam", [value]))

    @jsii.member(jsii_name="putIot")
    def put_iot(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsIot(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putIot", [value]))

    @jsii.member(jsii_name="putKinesis")
    def put_kinesis(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_shards: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_shards: Specify if Shards should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_shards CloudAwsIntegrations#fetch_shards}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsKinesis(
            aws_regions=aws_regions,
            fetch_shards=fetch_shards,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putKinesis", [value]))

    @jsii.member(jsii_name="putKinesisFirehose")
    def put_kinesis_firehose(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsKinesisFirehose(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putKinesisFirehose", [value]))

    @jsii.member(jsii_name="putLambda")
    def put_lambda(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsLambda(
            aws_regions=aws_regions,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putLambda", [value]))

    @jsii.member(jsii_name="putRds")
    def put_rds(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsRds(
            aws_regions=aws_regions,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putRds", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsRedshift(
            aws_regions=aws_regions,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putRoute53")
    def put_route53(
        self,
        *,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsRoute53(
            fetch_extended_inventory=fetch_extended_inventory,
            metrics_polling_interval=metrics_polling_interval,
        )

        return typing.cast(None, jsii.invoke(self, "putRoute53", [value]))

    @jsii.member(jsii_name="putS3")
    def put_s3(
        self,
        *,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsS3(
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSes")
    def put_ses(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsSes(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putSes", [value]))

    @jsii.member(jsii_name="putSns")
    def put_sns(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsSns(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            metrics_polling_interval=metrics_polling_interval,
        )

        return typing.cast(None, jsii.invoke(self, "putSns", [value]))

    @jsii.member(jsii_name="putSqs")
    def put_sqs(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        queue_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param queue_prefixes: Specify each name or prefix for the Queues that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#queue_prefixes CloudAwsIntegrations#queue_prefixes}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsSqs(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            queue_prefixes=queue_prefixes,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putSqs", [value]))

    @jsii.member(jsii_name="putTrustedAdvisor")
    def put_trusted_advisor(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsTrustedAdvisor(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putTrustedAdvisor", [value]))

    @jsii.member(jsii_name="putVpc")
    def put_vpc(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_nat_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_vpn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_nat_gateway: Specify if NAT gateway should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_nat_gateway CloudAwsIntegrations#fetch_nat_gateway}
        :param fetch_vpn: Specify if VPN should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_vpn CloudAwsIntegrations#fetch_vpn}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        value = CloudAwsIntegrationsVpc(
            aws_regions=aws_regions,
            fetch_nat_gateway=fetch_nat_gateway,
            fetch_vpn=fetch_vpn,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putVpc", [value]))

    @jsii.member(jsii_name="putXRay")
    def put_x_ray(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsIntegrationsXRay(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putXRay", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAlb")
    def reset_alb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlb", []))

    @jsii.member(jsii_name="resetApiGateway")
    def reset_api_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiGateway", []))

    @jsii.member(jsii_name="resetAutoScaling")
    def reset_auto_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScaling", []))

    @jsii.member(jsii_name="resetAwsAppSync")
    def reset_aws_app_sync(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAppSync", []))

    @jsii.member(jsii_name="resetAwsAthena")
    def reset_aws_athena(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAthena", []))

    @jsii.member(jsii_name="resetAwsAutoDiscovery")
    def reset_aws_auto_discovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAutoDiscovery", []))

    @jsii.member(jsii_name="resetAwsCognito")
    def reset_aws_cognito(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsCognito", []))

    @jsii.member(jsii_name="resetAwsConnect")
    def reset_aws_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsConnect", []))

    @jsii.member(jsii_name="resetAwsDirectConnect")
    def reset_aws_direct_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsDirectConnect", []))

    @jsii.member(jsii_name="resetAwsFsx")
    def reset_aws_fsx(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsFsx", []))

    @jsii.member(jsii_name="resetAwsGlue")
    def reset_aws_glue(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsGlue", []))

    @jsii.member(jsii_name="resetAwsKinesisAnalytics")
    def reset_aws_kinesis_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsKinesisAnalytics", []))

    @jsii.member(jsii_name="resetAwsMediaConvert")
    def reset_aws_media_convert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsMediaConvert", []))

    @jsii.member(jsii_name="resetAwsMediaPackageVod")
    def reset_aws_media_package_vod(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsMediaPackageVod", []))

    @jsii.member(jsii_name="resetAwsMq")
    def reset_aws_mq(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsMq", []))

    @jsii.member(jsii_name="resetAwsMsk")
    def reset_aws_msk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsMsk", []))

    @jsii.member(jsii_name="resetAwsNeptune")
    def reset_aws_neptune(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsNeptune", []))

    @jsii.member(jsii_name="resetAwsQldb")
    def reset_aws_qldb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsQldb", []))

    @jsii.member(jsii_name="resetAwsRoute53Resolver")
    def reset_aws_route53_resolver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRoute53Resolver", []))

    @jsii.member(jsii_name="resetAwsStates")
    def reset_aws_states(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsStates", []))

    @jsii.member(jsii_name="resetAwsTransitGateway")
    def reset_aws_transit_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsTransitGateway", []))

    @jsii.member(jsii_name="resetAwsWaf")
    def reset_aws_waf(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsWaf", []))

    @jsii.member(jsii_name="resetAwsWafv2")
    def reset_aws_wafv2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsWafv2", []))

    @jsii.member(jsii_name="resetBilling")
    def reset_billing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBilling", []))

    @jsii.member(jsii_name="resetCloudfront")
    def reset_cloudfront(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudfront", []))

    @jsii.member(jsii_name="resetCloudtrail")
    def reset_cloudtrail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudtrail", []))

    @jsii.member(jsii_name="resetDocDb")
    def reset_doc_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocDb", []))

    @jsii.member(jsii_name="resetDynamodb")
    def reset_dynamodb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamodb", []))

    @jsii.member(jsii_name="resetEbs")
    def reset_ebs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbs", []))

    @jsii.member(jsii_name="resetEc2")
    def reset_ec2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2", []))

    @jsii.member(jsii_name="resetEcs")
    def reset_ecs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcs", []))

    @jsii.member(jsii_name="resetEfs")
    def reset_efs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEfs", []))

    @jsii.member(jsii_name="resetElasticache")
    def reset_elasticache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticache", []))

    @jsii.member(jsii_name="resetElasticbeanstalk")
    def reset_elasticbeanstalk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticbeanstalk", []))

    @jsii.member(jsii_name="resetElasticsearch")
    def reset_elasticsearch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearch", []))

    @jsii.member(jsii_name="resetElb")
    def reset_elb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElb", []))

    @jsii.member(jsii_name="resetEmr")
    def reset_emr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmr", []))

    @jsii.member(jsii_name="resetHealth")
    def reset_health(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealth", []))

    @jsii.member(jsii_name="resetIam")
    def reset_iam(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIam", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIot")
    def reset_iot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIot", []))

    @jsii.member(jsii_name="resetKinesis")
    def reset_kinesis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesis", []))

    @jsii.member(jsii_name="resetKinesisFirehose")
    def reset_kinesis_firehose(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKinesisFirehose", []))

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @jsii.member(jsii_name="resetRds")
    def reset_rds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRds", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetRoute53")
    def reset_route53(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoute53", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSes")
    def reset_ses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSes", []))

    @jsii.member(jsii_name="resetSns")
    def reset_sns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSns", []))

    @jsii.member(jsii_name="resetSqs")
    def reset_sqs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqs", []))

    @jsii.member(jsii_name="resetTrustedAdvisor")
    def reset_trusted_advisor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedAdvisor", []))

    @jsii.member(jsii_name="resetVpc")
    def reset_vpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpc", []))

    @jsii.member(jsii_name="resetXRay")
    def reset_x_ray(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXRay", []))

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
    @jsii.member(jsii_name="alb")
    def alb(self) -> "CloudAwsIntegrationsAlbOutputReference":
        return typing.cast("CloudAwsIntegrationsAlbOutputReference", jsii.get(self, "alb"))

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(self) -> "CloudAwsIntegrationsApiGatewayOutputReference":
        return typing.cast("CloudAwsIntegrationsApiGatewayOutputReference", jsii.get(self, "apiGateway"))

    @builtins.property
    @jsii.member(jsii_name="autoScaling")
    def auto_scaling(self) -> "CloudAwsIntegrationsAutoScalingOutputReference":
        return typing.cast("CloudAwsIntegrationsAutoScalingOutputReference", jsii.get(self, "autoScaling"))

    @builtins.property
    @jsii.member(jsii_name="awsAppSync")
    def aws_app_sync(self) -> "CloudAwsIntegrationsAwsAppSyncOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsAppSyncOutputReference", jsii.get(self, "awsAppSync"))

    @builtins.property
    @jsii.member(jsii_name="awsAthena")
    def aws_athena(self) -> "CloudAwsIntegrationsAwsAthenaOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsAthenaOutputReference", jsii.get(self, "awsAthena"))

    @builtins.property
    @jsii.member(jsii_name="awsAutoDiscovery")
    def aws_auto_discovery(
        self,
    ) -> "CloudAwsIntegrationsAwsAutoDiscoveryOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsAutoDiscoveryOutputReference", jsii.get(self, "awsAutoDiscovery"))

    @builtins.property
    @jsii.member(jsii_name="awsCognito")
    def aws_cognito(self) -> "CloudAwsIntegrationsAwsCognitoOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsCognitoOutputReference", jsii.get(self, "awsCognito"))

    @builtins.property
    @jsii.member(jsii_name="awsConnect")
    def aws_connect(self) -> "CloudAwsIntegrationsAwsConnectOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsConnectOutputReference", jsii.get(self, "awsConnect"))

    @builtins.property
    @jsii.member(jsii_name="awsDirectConnect")
    def aws_direct_connect(
        self,
    ) -> "CloudAwsIntegrationsAwsDirectConnectOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsDirectConnectOutputReference", jsii.get(self, "awsDirectConnect"))

    @builtins.property
    @jsii.member(jsii_name="awsFsx")
    def aws_fsx(self) -> "CloudAwsIntegrationsAwsFsxOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsFsxOutputReference", jsii.get(self, "awsFsx"))

    @builtins.property
    @jsii.member(jsii_name="awsGlue")
    def aws_glue(self) -> "CloudAwsIntegrationsAwsGlueOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsGlueOutputReference", jsii.get(self, "awsGlue"))

    @builtins.property
    @jsii.member(jsii_name="awsKinesisAnalytics")
    def aws_kinesis_analytics(
        self,
    ) -> "CloudAwsIntegrationsAwsKinesisAnalyticsOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsKinesisAnalyticsOutputReference", jsii.get(self, "awsKinesisAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="awsMediaConvert")
    def aws_media_convert(self) -> "CloudAwsIntegrationsAwsMediaConvertOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsMediaConvertOutputReference", jsii.get(self, "awsMediaConvert"))

    @builtins.property
    @jsii.member(jsii_name="awsMediaPackageVod")
    def aws_media_package_vod(
        self,
    ) -> "CloudAwsIntegrationsAwsMediaPackageVodOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsMediaPackageVodOutputReference", jsii.get(self, "awsMediaPackageVod"))

    @builtins.property
    @jsii.member(jsii_name="awsMq")
    def aws_mq(self) -> "CloudAwsIntegrationsAwsMqOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsMqOutputReference", jsii.get(self, "awsMq"))

    @builtins.property
    @jsii.member(jsii_name="awsMsk")
    def aws_msk(self) -> "CloudAwsIntegrationsAwsMskOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsMskOutputReference", jsii.get(self, "awsMsk"))

    @builtins.property
    @jsii.member(jsii_name="awsNeptune")
    def aws_neptune(self) -> "CloudAwsIntegrationsAwsNeptuneOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsNeptuneOutputReference", jsii.get(self, "awsNeptune"))

    @builtins.property
    @jsii.member(jsii_name="awsQldb")
    def aws_qldb(self) -> "CloudAwsIntegrationsAwsQldbOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsQldbOutputReference", jsii.get(self, "awsQldb"))

    @builtins.property
    @jsii.member(jsii_name="awsRoute53Resolver")
    def aws_route53_resolver(
        self,
    ) -> "CloudAwsIntegrationsAwsRoute53ResolverOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsRoute53ResolverOutputReference", jsii.get(self, "awsRoute53Resolver"))

    @builtins.property
    @jsii.member(jsii_name="awsStates")
    def aws_states(self) -> "CloudAwsIntegrationsAwsStatesOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsStatesOutputReference", jsii.get(self, "awsStates"))

    @builtins.property
    @jsii.member(jsii_name="awsTransitGateway")
    def aws_transit_gateway(
        self,
    ) -> "CloudAwsIntegrationsAwsTransitGatewayOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsTransitGatewayOutputReference", jsii.get(self, "awsTransitGateway"))

    @builtins.property
    @jsii.member(jsii_name="awsWaf")
    def aws_waf(self) -> "CloudAwsIntegrationsAwsWafOutputReference":
        return typing.cast("CloudAwsIntegrationsAwsWafOutputReference", jsii.get(self, "awsWaf"))

    @builtins.property
    @jsii.member(jsii_name="awsWafv2")
    def aws_wafv2(self) -> "CloudAwsIntegrationsAwsWafv2OutputReference":
        return typing.cast("CloudAwsIntegrationsAwsWafv2OutputReference", jsii.get(self, "awsWafv2"))

    @builtins.property
    @jsii.member(jsii_name="billing")
    def billing(self) -> "CloudAwsIntegrationsBillingOutputReference":
        return typing.cast("CloudAwsIntegrationsBillingOutputReference", jsii.get(self, "billing"))

    @builtins.property
    @jsii.member(jsii_name="cloudfront")
    def cloudfront(self) -> "CloudAwsIntegrationsCloudfrontOutputReference":
        return typing.cast("CloudAwsIntegrationsCloudfrontOutputReference", jsii.get(self, "cloudfront"))

    @builtins.property
    @jsii.member(jsii_name="cloudtrail")
    def cloudtrail(self) -> "CloudAwsIntegrationsCloudtrailOutputReference":
        return typing.cast("CloudAwsIntegrationsCloudtrailOutputReference", jsii.get(self, "cloudtrail"))

    @builtins.property
    @jsii.member(jsii_name="docDb")
    def doc_db(self) -> "CloudAwsIntegrationsDocDbOutputReference":
        return typing.cast("CloudAwsIntegrationsDocDbOutputReference", jsii.get(self, "docDb"))

    @builtins.property
    @jsii.member(jsii_name="dynamodb")
    def dynamodb(self) -> "CloudAwsIntegrationsDynamodbOutputReference":
        return typing.cast("CloudAwsIntegrationsDynamodbOutputReference", jsii.get(self, "dynamodb"))

    @builtins.property
    @jsii.member(jsii_name="ebs")
    def ebs(self) -> "CloudAwsIntegrationsEbsOutputReference":
        return typing.cast("CloudAwsIntegrationsEbsOutputReference", jsii.get(self, "ebs"))

    @builtins.property
    @jsii.member(jsii_name="ec2")
    def ec2(self) -> "CloudAwsIntegrationsEc2OutputReference":
        return typing.cast("CloudAwsIntegrationsEc2OutputReference", jsii.get(self, "ec2"))

    @builtins.property
    @jsii.member(jsii_name="ecs")
    def ecs(self) -> "CloudAwsIntegrationsEcsOutputReference":
        return typing.cast("CloudAwsIntegrationsEcsOutputReference", jsii.get(self, "ecs"))

    @builtins.property
    @jsii.member(jsii_name="efs")
    def efs(self) -> "CloudAwsIntegrationsEfsOutputReference":
        return typing.cast("CloudAwsIntegrationsEfsOutputReference", jsii.get(self, "efs"))

    @builtins.property
    @jsii.member(jsii_name="elasticache")
    def elasticache(self) -> "CloudAwsIntegrationsElasticacheOutputReference":
        return typing.cast("CloudAwsIntegrationsElasticacheOutputReference", jsii.get(self, "elasticache"))

    @builtins.property
    @jsii.member(jsii_name="elasticbeanstalk")
    def elasticbeanstalk(self) -> "CloudAwsIntegrationsElasticbeanstalkOutputReference":
        return typing.cast("CloudAwsIntegrationsElasticbeanstalkOutputReference", jsii.get(self, "elasticbeanstalk"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearch")
    def elasticsearch(self) -> "CloudAwsIntegrationsElasticsearchOutputReference":
        return typing.cast("CloudAwsIntegrationsElasticsearchOutputReference", jsii.get(self, "elasticsearch"))

    @builtins.property
    @jsii.member(jsii_name="elb")
    def elb(self) -> "CloudAwsIntegrationsElbOutputReference":
        return typing.cast("CloudAwsIntegrationsElbOutputReference", jsii.get(self, "elb"))

    @builtins.property
    @jsii.member(jsii_name="emr")
    def emr(self) -> "CloudAwsIntegrationsEmrOutputReference":
        return typing.cast("CloudAwsIntegrationsEmrOutputReference", jsii.get(self, "emr"))

    @builtins.property
    @jsii.member(jsii_name="health")
    def health(self) -> "CloudAwsIntegrationsHealthOutputReference":
        return typing.cast("CloudAwsIntegrationsHealthOutputReference", jsii.get(self, "health"))

    @builtins.property
    @jsii.member(jsii_name="iam")
    def iam(self) -> "CloudAwsIntegrationsIamOutputReference":
        return typing.cast("CloudAwsIntegrationsIamOutputReference", jsii.get(self, "iam"))

    @builtins.property
    @jsii.member(jsii_name="iot")
    def iot(self) -> "CloudAwsIntegrationsIotOutputReference":
        return typing.cast("CloudAwsIntegrationsIotOutputReference", jsii.get(self, "iot"))

    @builtins.property
    @jsii.member(jsii_name="kinesis")
    def kinesis(self) -> "CloudAwsIntegrationsKinesisOutputReference":
        return typing.cast("CloudAwsIntegrationsKinesisOutputReference", jsii.get(self, "kinesis"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehose")
    def kinesis_firehose(self) -> "CloudAwsIntegrationsKinesisFirehoseOutputReference":
        return typing.cast("CloudAwsIntegrationsKinesisFirehoseOutputReference", jsii.get(self, "kinesisFirehose"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "CloudAwsIntegrationsLambdaOutputReference":
        return typing.cast("CloudAwsIntegrationsLambdaOutputReference", jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="rds")
    def rds(self) -> "CloudAwsIntegrationsRdsOutputReference":
        return typing.cast("CloudAwsIntegrationsRdsOutputReference", jsii.get(self, "rds"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(self) -> "CloudAwsIntegrationsRedshiftOutputReference":
        return typing.cast("CloudAwsIntegrationsRedshiftOutputReference", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="route53")
    def route53(self) -> "CloudAwsIntegrationsRoute53OutputReference":
        return typing.cast("CloudAwsIntegrationsRoute53OutputReference", jsii.get(self, "route53"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "CloudAwsIntegrationsS3OutputReference":
        return typing.cast("CloudAwsIntegrationsS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="ses")
    def ses(self) -> "CloudAwsIntegrationsSesOutputReference":
        return typing.cast("CloudAwsIntegrationsSesOutputReference", jsii.get(self, "ses"))

    @builtins.property
    @jsii.member(jsii_name="sns")
    def sns(self) -> "CloudAwsIntegrationsSnsOutputReference":
        return typing.cast("CloudAwsIntegrationsSnsOutputReference", jsii.get(self, "sns"))

    @builtins.property
    @jsii.member(jsii_name="sqs")
    def sqs(self) -> "CloudAwsIntegrationsSqsOutputReference":
        return typing.cast("CloudAwsIntegrationsSqsOutputReference", jsii.get(self, "sqs"))

    @builtins.property
    @jsii.member(jsii_name="trustedAdvisor")
    def trusted_advisor(self) -> "CloudAwsIntegrationsTrustedAdvisorOutputReference":
        return typing.cast("CloudAwsIntegrationsTrustedAdvisorOutputReference", jsii.get(self, "trustedAdvisor"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> "CloudAwsIntegrationsVpcOutputReference":
        return typing.cast("CloudAwsIntegrationsVpcOutputReference", jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="xRay")
    def x_ray(self) -> "CloudAwsIntegrationsXRayOutputReference":
        return typing.cast("CloudAwsIntegrationsXRayOutputReference", jsii.get(self, "xRay"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="albInput")
    def alb_input(self) -> typing.Optional["CloudAwsIntegrationsAlb"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAlb"], jsii.get(self, "albInput"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayInput")
    def api_gateway_input(self) -> typing.Optional["CloudAwsIntegrationsApiGateway"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsApiGateway"], jsii.get(self, "apiGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingInput")
    def auto_scaling_input(self) -> typing.Optional["CloudAwsIntegrationsAutoScaling"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAutoScaling"], jsii.get(self, "autoScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAppSyncInput")
    def aws_app_sync_input(self) -> typing.Optional["CloudAwsIntegrationsAwsAppSync"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsAppSync"], jsii.get(self, "awsAppSyncInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAthenaInput")
    def aws_athena_input(self) -> typing.Optional["CloudAwsIntegrationsAwsAthena"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsAthena"], jsii.get(self, "awsAthenaInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAutoDiscoveryInput")
    def aws_auto_discovery_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsAwsAutoDiscovery"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsAutoDiscovery"], jsii.get(self, "awsAutoDiscoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="awsCognitoInput")
    def aws_cognito_input(self) -> typing.Optional["CloudAwsIntegrationsAwsCognito"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsCognito"], jsii.get(self, "awsCognitoInput"))

    @builtins.property
    @jsii.member(jsii_name="awsConnectInput")
    def aws_connect_input(self) -> typing.Optional["CloudAwsIntegrationsAwsConnect"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsConnect"], jsii.get(self, "awsConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="awsDirectConnectInput")
    def aws_direct_connect_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsAwsDirectConnect"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsDirectConnect"], jsii.get(self, "awsDirectConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="awsFsxInput")
    def aws_fsx_input(self) -> typing.Optional["CloudAwsIntegrationsAwsFsx"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsFsx"], jsii.get(self, "awsFsxInput"))

    @builtins.property
    @jsii.member(jsii_name="awsGlueInput")
    def aws_glue_input(self) -> typing.Optional["CloudAwsIntegrationsAwsGlue"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsGlue"], jsii.get(self, "awsGlueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsKinesisAnalyticsInput")
    def aws_kinesis_analytics_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsAwsKinesisAnalytics"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsKinesisAnalytics"], jsii.get(self, "awsKinesisAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="awsMediaConvertInput")
    def aws_media_convert_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsAwsMediaConvert"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsMediaConvert"], jsii.get(self, "awsMediaConvertInput"))

    @builtins.property
    @jsii.member(jsii_name="awsMediaPackageVodInput")
    def aws_media_package_vod_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsAwsMediaPackageVod"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsMediaPackageVod"], jsii.get(self, "awsMediaPackageVodInput"))

    @builtins.property
    @jsii.member(jsii_name="awsMqInput")
    def aws_mq_input(self) -> typing.Optional["CloudAwsIntegrationsAwsMq"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsMq"], jsii.get(self, "awsMqInput"))

    @builtins.property
    @jsii.member(jsii_name="awsMskInput")
    def aws_msk_input(self) -> typing.Optional["CloudAwsIntegrationsAwsMsk"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsMsk"], jsii.get(self, "awsMskInput"))

    @builtins.property
    @jsii.member(jsii_name="awsNeptuneInput")
    def aws_neptune_input(self) -> typing.Optional["CloudAwsIntegrationsAwsNeptune"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsNeptune"], jsii.get(self, "awsNeptuneInput"))

    @builtins.property
    @jsii.member(jsii_name="awsQldbInput")
    def aws_qldb_input(self) -> typing.Optional["CloudAwsIntegrationsAwsQldb"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsQldb"], jsii.get(self, "awsQldbInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRoute53ResolverInput")
    def aws_route53_resolver_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsAwsRoute53Resolver"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsRoute53Resolver"], jsii.get(self, "awsRoute53ResolverInput"))

    @builtins.property
    @jsii.member(jsii_name="awsStatesInput")
    def aws_states_input(self) -> typing.Optional["CloudAwsIntegrationsAwsStates"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsStates"], jsii.get(self, "awsStatesInput"))

    @builtins.property
    @jsii.member(jsii_name="awsTransitGatewayInput")
    def aws_transit_gateway_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsAwsTransitGateway"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsTransitGateway"], jsii.get(self, "awsTransitGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="awsWafInput")
    def aws_waf_input(self) -> typing.Optional["CloudAwsIntegrationsAwsWaf"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsWaf"], jsii.get(self, "awsWafInput"))

    @builtins.property
    @jsii.member(jsii_name="awsWafv2Input")
    def aws_wafv2_input(self) -> typing.Optional["CloudAwsIntegrationsAwsWafv2"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsAwsWafv2"], jsii.get(self, "awsWafv2Input"))

    @builtins.property
    @jsii.member(jsii_name="billingInput")
    def billing_input(self) -> typing.Optional["CloudAwsIntegrationsBilling"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsBilling"], jsii.get(self, "billingInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudfrontInput")
    def cloudfront_input(self) -> typing.Optional["CloudAwsIntegrationsCloudfront"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsCloudfront"], jsii.get(self, "cloudfrontInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudtrailInput")
    def cloudtrail_input(self) -> typing.Optional["CloudAwsIntegrationsCloudtrail"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsCloudtrail"], jsii.get(self, "cloudtrailInput"))

    @builtins.property
    @jsii.member(jsii_name="docDbInput")
    def doc_db_input(self) -> typing.Optional["CloudAwsIntegrationsDocDb"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsDocDb"], jsii.get(self, "docDbInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamodbInput")
    def dynamodb_input(self) -> typing.Optional["CloudAwsIntegrationsDynamodb"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsDynamodb"], jsii.get(self, "dynamodbInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsInput")
    def ebs_input(self) -> typing.Optional["CloudAwsIntegrationsEbs"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsEbs"], jsii.get(self, "ebsInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2Input")
    def ec2_input(self) -> typing.Optional["CloudAwsIntegrationsEc2"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsEc2"], jsii.get(self, "ec2Input"))

    @builtins.property
    @jsii.member(jsii_name="ecsInput")
    def ecs_input(self) -> typing.Optional["CloudAwsIntegrationsEcs"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsEcs"], jsii.get(self, "ecsInput"))

    @builtins.property
    @jsii.member(jsii_name="efsInput")
    def efs_input(self) -> typing.Optional["CloudAwsIntegrationsEfs"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsEfs"], jsii.get(self, "efsInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticacheInput")
    def elasticache_input(self) -> typing.Optional["CloudAwsIntegrationsElasticache"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsElasticache"], jsii.get(self, "elasticacheInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticbeanstalkInput")
    def elasticbeanstalk_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsElasticbeanstalk"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsElasticbeanstalk"], jsii.get(self, "elasticbeanstalkInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchInput")
    def elasticsearch_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsElasticsearch"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsElasticsearch"], jsii.get(self, "elasticsearchInput"))

    @builtins.property
    @jsii.member(jsii_name="elbInput")
    def elb_input(self) -> typing.Optional["CloudAwsIntegrationsElb"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsElb"], jsii.get(self, "elbInput"))

    @builtins.property
    @jsii.member(jsii_name="emrInput")
    def emr_input(self) -> typing.Optional["CloudAwsIntegrationsEmr"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsEmr"], jsii.get(self, "emrInput"))

    @builtins.property
    @jsii.member(jsii_name="healthInput")
    def health_input(self) -> typing.Optional["CloudAwsIntegrationsHealth"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsHealth"], jsii.get(self, "healthInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInput")
    def iam_input(self) -> typing.Optional["CloudAwsIntegrationsIam"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsIam"], jsii.get(self, "iamInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iotInput")
    def iot_input(self) -> typing.Optional["CloudAwsIntegrationsIot"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsIot"], jsii.get(self, "iotInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseInput")
    def kinesis_firehose_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsKinesisFirehose"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsKinesisFirehose"], jsii.get(self, "kinesisFirehoseInput"))

    @builtins.property
    @jsii.member(jsii_name="kinesisInput")
    def kinesis_input(self) -> typing.Optional["CloudAwsIntegrationsKinesis"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsKinesis"], jsii.get(self, "kinesisInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(self) -> typing.Optional["CloudAwsIntegrationsLambda"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsLambda"], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedAccountIdInput")
    def linked_account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "linkedAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="rdsInput")
    def rds_input(self) -> typing.Optional["CloudAwsIntegrationsRds"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsRds"], jsii.get(self, "rdsInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(self) -> typing.Optional["CloudAwsIntegrationsRedshift"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsRedshift"], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="route53Input")
    def route53_input(self) -> typing.Optional["CloudAwsIntegrationsRoute53"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsRoute53"], jsii.get(self, "route53Input"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional["CloudAwsIntegrationsS3"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="sesInput")
    def ses_input(self) -> typing.Optional["CloudAwsIntegrationsSes"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsSes"], jsii.get(self, "sesInput"))

    @builtins.property
    @jsii.member(jsii_name="snsInput")
    def sns_input(self) -> typing.Optional["CloudAwsIntegrationsSns"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsSns"], jsii.get(self, "snsInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsInput")
    def sqs_input(self) -> typing.Optional["CloudAwsIntegrationsSqs"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsSqs"], jsii.get(self, "sqsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedAdvisorInput")
    def trusted_advisor_input(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsTrustedAdvisor"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsTrustedAdvisor"], jsii.get(self, "trustedAdvisorInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcInput")
    def vpc_input(self) -> typing.Optional["CloudAwsIntegrationsVpc"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsVpc"], jsii.get(self, "vpcInput"))

    @builtins.property
    @jsii.member(jsii_name="xRayInput")
    def x_ray_input(self) -> typing.Optional["CloudAwsIntegrationsXRay"]:
        return typing.cast(typing.Optional["CloudAwsIntegrationsXRay"], jsii.get(self, "xRayInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5219cec395e62e4e80020a1434f822e106636205b1c60eb208915ae3fb2ebcc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bc997685d6f8091c1aeb3bc838d3517467f180193964c59a5ff4dec857a6d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkedAccountId")
    def linked_account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "linkedAccountId"))

    @linked_account_id.setter
    def linked_account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947ffbc6d56f727b440fd8f8118b85c3b51c796e2061df9d54dc4f7e8a8ac873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedAccountId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAlb",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "fetch_tags": "fetchTags",
        "load_balancer_prefixes": "loadBalancerPrefixes",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsAlb:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        load_balancer_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param load_balancer_prefixes: Specify each name or prefix for the LBs that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#load_balancer_prefixes CloudAwsIntegrations#load_balancer_prefixes}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e40c59dd4d07db8036db912b3d55367876e9d77f5205cf22f9f483431901d19)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument load_balancer_prefixes", value=load_balancer_prefixes, expected_type=type_hints["load_balancer_prefixes"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if load_balancer_prefixes is not None:
            self._values["load_balancer_prefixes"] = load_balancer_prefixes
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def load_balancer_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each name or prefix for the LBs that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#load_balancer_prefixes CloudAwsIntegrations#load_balancer_prefixes}
        '''
        result = self._values.get("load_balancer_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAlb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAlbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAlbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__572217df744846f2766d2affe294d69726b61e9680270a7bd923e0111b104af3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetLoadBalancerPrefixes")
    def reset_load_balancer_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancerPrefixes", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerPrefixesInput")
    def load_balancer_prefixes_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loadBalancerPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9706cd7ff89e53664ab1cfd3c3035cda1a0cc1be501a30f0e5746e2d3e7e2e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b3ce8feaeaf2af84265f7259427c238e3cfbc42f4c9461ffded1079005d95c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe6f052ff4d591211660ad507830c4891a9367c1347f6cc8366c041461ed5ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerPrefixes")
    def load_balancer_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loadBalancerPrefixes"))

    @load_balancer_prefixes.setter
    def load_balancer_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff379d8c86d86ed60ea79ebb3c74b0994dd7ad6522c150d4ef706818a5ab0df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e3734ab02a24e893e41f78ff92468a606167dbc8be3283b85012bd7b191f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62ed7ae7c08e77ed7e50f49e4c5c6888c8927d4b0a8ccb50aaca10edebdc4867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767b2668e3f3efc893160d37ed3ccd4a4903950da2102758a3ecd77ffc8bde44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAlb]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAlb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsAlb]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecba4987951050f636453107e5a4b0740c989f21f1391c41ed3a15bc4b2e080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsApiGateway",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
        "stage_prefixes": "stagePrefixes",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsApiGateway:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        stage_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param stage_prefixes: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#stage_prefixes CloudAwsIntegrations#stage_prefixes}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c455c691d322c0e9b961d79d5bde588c516e04970357f51f4751bf5c9ca651)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument stage_prefixes", value=stage_prefixes, expected_type=type_hints["stage_prefixes"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if stage_prefixes is not None:
            self._values["stage_prefixes"] = stage_prefixes
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stage_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#stage_prefixes CloudAwsIntegrations#stage_prefixes}
        '''
        result = self._values.get("stage_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsApiGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsApiGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsApiGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c0794f271d38a04aa555de1b5ec64fb2d72c06537815188b1ffc3b74b2017ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetStagePrefixes")
    def reset_stage_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagePrefixes", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="stagePrefixesInput")
    def stage_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stagePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b07b9ac4b3c1c86fe1fe990ff471e943866bf78f624acacaf9956ea9190927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e79ee75f76044b8ae48438ec73f10c6e0ad857ed30e8ed7347e647d247a2885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagePrefixes")
    def stage_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stagePrefixes"))

    @stage_prefixes.setter
    def stage_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df396b0c5b30777f8bb53d69cdfc9dd1db0ea822aaad2bb7f6579b47c47c97da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2f50b2e93d3ce05e2b3e16b68de6ce8a31bb57531f62cbec8b253c53036527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520d3a4fe43e7a445173c8f404fe784d1f92ba90fb3425a01e48013b1061ad26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsApiGateway]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsApiGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsApiGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53085079a55deb7ff8923b44e6ad6676461678ad21ab2c684a7df120f716881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAutoScaling",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAutoScaling:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1a637079b6721ef1936e2e172260f07f1596ffa6ce5b0859040f8ee31604d3)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAutoScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAutoScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAutoScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__492d1f319956f75f675cf675053fd025d349bbe0b2f861cdb21a76b8b9e78b91)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f8bc1aa7ae647c694a1b75d3d84458de85506dff10366afee1adae3bccd62c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b792f26dc3907e199974d6a32f887bb94d57eb57ac2c2d1f827e677efb439cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAutoScaling]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAutoScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAutoScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7c50d259f2a569292112597fd78316ca372be95904b02ac682fd5cceb0cc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsAppSync",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsAppSync:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb27c211c2553d9a3ac20e3e8ec713612f8887916f61164f4ba610706ce5dbe)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsAppSync(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsAppSyncOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsAppSyncOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1732a8916426229bff1f258e1e0fbfb9551d43457e7900815ad67cbf8c935cf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d8eca29f363bbc313a464a8bf96b7e90acc97acac5f970ea1ae98c47a11982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0990aaa0fc31abe1c9722fc8f90787dbab338f39159db03369c844db077ca4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsAppSync]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsAppSync], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsAppSync],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65da110080261e9965faa937acfeea8959eb5723430ddd78f97fbe5f9fedd3ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsAthena",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsAthena:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6d4a1c59279a1b5b4d108de10deb8322e29b7c26b6647a0b9f8abd0e9ab2da)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsAthena(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsAthenaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsAthenaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a18b1f9bde7a5f8e4e5c85d35cdb72852d1ba915a27d65f1cdefce2e653d21c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1123ec36abb5a0ec0eeb13c02226108192b20c1c8835e822d9b1e2d37bd0c67f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a29993735352695316ee5dc5d3d302b286552c3017ab6912fd42790badc43b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsAthena]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsAthena], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsAthena],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa9c8cd8ab12498062d6f65aca27198e443a2d07624451850b73388e451c720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsAutoDiscovery",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsAutoDiscovery:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2696be9c1d02d3937eea9c46e9e600bd5fa5943114bc0466cd8cbbbff37e6d7a)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsAutoDiscovery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsAutoDiscoveryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsAutoDiscoveryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b82a6a1c1566d58f509511ba01e2a74047aa63bfa567f8e1c30f072083f502f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48af961ff5adca680177384658fa500ec6c61ac3abde2a1436118e58b6fc4bb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ef994b8c3bc9882b5a1a3502578614783166ad71401529859bab5aa1fa21d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsAutoDiscovery]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsAutoDiscovery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsAutoDiscovery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12111b8516b2c9db5715d10c2bf508410fded980890b0e34105b29a159c0ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsCognito",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsCognito:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979a8717df7247972c094e198570b76c0254c4c58f9a386dc643ed39180b3f55)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsCognito(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsCognitoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsCognitoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5af7b76d436e5475bd65f3d69efe50a2c796953a6b6fea6c1fb6a217d7fa882)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876abea8542cd18043634adb5243217e00b06937cc0d36feb9860f0a5c094535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e057352b0abd3f42323ec536db2de4e697c734502a5a764a3ca91d3c72022aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsCognito]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsCognito], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsCognito],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147e934fc44d3874acf250647d9d5452681a389af25271c4bb0d7fdbee12abe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsConnect",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsConnect:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56418f9ce152dc44aaafd1c86907ac25ed16ce9e2b1af0e7aa4ff2b9ae0ad461)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsConnect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsConnectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsConnectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74e95f82b6a8032ffd4ce668bf74d0f930ab97e94db5d61118551692b1821b11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811019247b441fa37f3114612ff411542ea28e5ca9eb8abcf855edfb24893241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70607156bf068687595e89c93a129d0180b2621363451b7ef3d9398a43e0f8b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsConnect]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsConnect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsConnect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429cabf9d7bc9bbc306dba7a297f0da310c52e115ff57dbfb8dc1243f62d13c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsDirectConnect",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsDirectConnect:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb9a828a1b41fc81696e6197a0e9f57784438b53b7fbbca98e825c9e881814c)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsDirectConnect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsDirectConnectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsDirectConnectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39b26c7d199640199b08ac7444e459222e1018629846ed750b38efd053816aa1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd6d86bf944bdfdf1c78bb03ac45a047292ac29ff698a125bcb02d2c9bbe7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2efed19c1353098726510c48d3e02da2bf407f124af77475dbcec60c7a22c2f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsDirectConnect]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsDirectConnect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsDirectConnect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04033f504cd978f051b4328e6a4f723239bb791237f9682cce0416aebdc4e1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsFsx",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsFsx:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd4834378e05043d61d8c41067b08f3a3f361dc6810f60afd63d529c07d5df0)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsFsx(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsFsxOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsFsxOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__222209fdfbdad356c50e8013e190aef00e6ef4c39b648b826d384e636cffebb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2657143f79e2d78e94c658d14e0bc3216a9954a3d51f9826bc1317a85e4263d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e6f896545fa35a91199254e2690d4bc3be4b83626340921d0d25fb5ee699d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsFsx]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsFsx], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsFsx],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079d3b1543ee28287c873d94e6d45dc9aaf619f2a6fac2a424494379dc645ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsGlue",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsGlue:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13be6d1e289887a9278c10174d6446805dc6eeabd824fb8860f8b1a69f32c647)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsGlue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsGlueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsGlueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22384cd45e950c0be0beecf4d8f11ea18093dd317b55921dbf6a78b79aed3789)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8a1a1fe69cc1c0f4ff619415ef15eeb6ad829b164ecb681e2023e630ec659a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21b3d806045359287c61d4dee5fc3cbc7c3821fe6f7a1cd70cb9733924062f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsGlue]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsGlue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsGlue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edba3644a475c9306bca931ac7eb661a197b6bec5017d58fe0632182c935db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsKinesisAnalytics",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsKinesisAnalytics:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__929efc01f0eb14cbb469863a0673f2c86b8996f93f9c174be4e0ee76b81ea554)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsKinesisAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsKinesisAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsKinesisAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41b2772ec0e809bf1613d575ca445f201d5622045400617a581f49530e4e2a5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0396e6b059a84d235e4298bd4bb94335d62823d8fc7e43159be80cf70e54f19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31234072496c501eb0be8cb8dca29b26b94aebb0a02da535a64d8bf3f5d6c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudAwsIntegrationsAwsKinesisAnalytics]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsKinesisAnalytics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsKinesisAnalytics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6825c259162df555b2a7f4c4124ec2837f2bdabac708db9204d84f2efa50776c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsMediaConvert",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsMediaConvert:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7215dec7cb085c0a02e39a1406839de741fa58a2af9bddc4313ceb049b528cfd)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsMediaConvert(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsMediaConvertOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsMediaConvertOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9985b664e688d2ad517eb682b1a2d3ecd1ad21de651d33145cdb945adbcd80dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41e034de553b9742add856d7242d9a0c05e8727267e4a32bc93ba7e14eab653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0afb8bbeada0d12306f4e82045aab9ccebd3f98a001c28f3d7b520f11f67a4a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsMediaConvert]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsMediaConvert], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsMediaConvert],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3134fd44a7c90f8daccd0da879765cd1f50a29a1245c78269210b66757dac27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsMediaPackageVod",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsMediaPackageVod:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56895def110fcf5f07690cddb3bb6220a710c9eae098fc702d32b03587a0f88a)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsMediaPackageVod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsMediaPackageVodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsMediaPackageVodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d6c078300b0f054679e623ebfff563f1bd655b68f7548f9effb98d0bb30577)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf79231cbcd1b3367f31a2f5e85c086a4a7babdba9e91857c850971c85e73b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9ad8b88ef081e20845d475343fe1bc3422db36ddb54a624ff976764698d39e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsMediaPackageVod]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsMediaPackageVod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsMediaPackageVod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d191f349a8910587d2080b976ed452fa4469aabeb37676eca5d807badef7739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsMq",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsMq:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__023766cb8a0bf6393fca99b9a6c33a64059f9e044f562bdbb6231fe4bbd18379)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsMq(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsMqOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsMqOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9054c66fa1fd5267fc9ea2d6dd72573f098426719ea3315faadbd2cb45cbf51f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e33551d35dcf5c948db6ce2e8837fc68dd8fea95b21d820a5f1784ff5e5b001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca395bd03831e1d9a69bbe259352a48569940ddfec703163f3298b0614f6195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsMq]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsMq], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsAwsMq]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab114092f8588c14a63f489b0f20977085e8656df5e8238aedd79a002aa17a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsMsk",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsMsk:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a3e4c89d63cfee2a701c7d13eeea996cec77dfa04e231f0ad76f55f15be2a7)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsMsk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsMskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsMskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e59916632c4947a6e555de0503c4b8aa40fa94b2a38cc178812b1c461bbd047a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03fcf21e4012d08770b4e30824bebc7a492b8fde84a703579b339c8dff622368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b707de6fec18b038a8c219dc7d605e252c0099a72dbc192512593442c7de3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsMsk]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsMsk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsMsk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed742e5fad962b97df17fad73bd8caa0bb2db027489a5c2886d6e117542954e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsNeptune",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsNeptune:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d5d6fc2cb030dce0f96498079a27b14770ef125a713605ba769ca9856be22a)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsNeptune(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsNeptuneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsNeptuneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2da33d0297d2ff75c5926660706b29cc8e7e4d9c6b6e1922497ac026dc1f04a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__303b13d8461b72e611fefb6ebff644c44dbbb5044c7142f2973cad106197795c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba22c03539ce9b82fec840284339ad6fba81f4d91fd53f07e80ce701bb285e65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsNeptune]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsNeptune], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsNeptune],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05bc0338045b275e428d27902786fd0a6c59bf287c69f09636de85a4ed6f7d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsQldb",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsQldb:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e40ab013e4b71051afa2a6e3a9477fdebf6398813ac7b56556183160ae6f41c)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsQldb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsQldbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsQldbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2e0fda50c5558bddbad3f24a710a5cd0c8c7e8e864f254832657015d5ff9df6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45383924abdd9351e051d565811a69f05fc1531182c5c16a6a6daad99dff506)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de9eeeb7c7d98fe164eb4ec11b2847a10519cc6aa734f6f5ca80a92ffadc78c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsQldb]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsQldb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsQldb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c33d4d8f497905b7eab0a56376427d79455fbe7d5065dcb55c85a5e5ebe983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsRoute53Resolver",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsRoute53Resolver:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d996c041ee32148d6b98aba4921359109f18a55ebc49355547cf1f803fbd62e)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsRoute53Resolver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsRoute53ResolverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsRoute53ResolverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c2b194291d9ed0e477679251e878709ac658ca4423d2a599dc8f382dea2f230)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161b9a151142c84126131ab8cfe3376df22cbae9a681d73519b77958ae91edbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f622b1d4c376052dffa8e2a474b54bf105839c1fd4cee63886b8c267fd9e414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsRoute53Resolver]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsRoute53Resolver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsRoute53Resolver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54429e7fb6b7811156396606fa3b33fa78e43d7bb4d28b59c7fdab57e587cded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsStates",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsStates:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991333ab1ecdb2219b97dbaca765d788c80e79f1a1245319d452bd2a3dd66405)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsStates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsStatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsStatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__789018829d62b4743b85475385f4f6581462e2c7652f17f1c29100a43c19c294)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983a6f406043af64912a5ba05bbd3e0409d9980c36eac69867554850daa4bb85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8c1665abdd1e1578b96e75870f7566e34cf2429aca335285fdb9b2ab1a1cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsStates]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsStates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsStates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa49c73e7f8a5b126334d7b7f67026a917646f47903416c46388d033780d1238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsTransitGateway",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsTransitGateway:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643e89acdb5932bd7d59be268065180494a868d5b53015a8fa3018521a827f8f)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsTransitGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsTransitGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsTransitGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__215dd8c1eacc8e547770d87f9703c8c84de18b67fefe39be50ddf909077532cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6d3496ac958c5471ceefab26ecb2891a134ab4ac03209271e8a5059bc0c788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf6298d5adcbb0cfbf2c03740b22670f1d6da3b661bec9d84364f5e5fbede21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsTransitGateway]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsTransitGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsTransitGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3989a15499f56076f6c81944d4c258a34a79724ca8c56cf1cef0ab9eb6674bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsWaf",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsWaf:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f854a435a68b01769b18046a82ee738aeae217f89ecfe5cfe5909a9b8ab4941b)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsWaf(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsWafOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsWafOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6fa8e423cfcb04bf7b465151857fbaed542fc38da05cb937d97fcfb848db24b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88de4a5e06561acdb23619d393d7582a7775b3ef9efa2eb16d3548bf3f2bbf73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f39a6895d183ead48f2fce0420a9ead287b1cea09888b913ae0e9c4a205d9bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsWaf]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsWaf], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsWaf],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd84577c4a9548848eff9e94f9798ae3f88b476d21ff5eca82801c81cfeb8713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsWafv2",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsAwsWafv2:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0aa03acb5e2ef6c930e1717137b507913393a6d9225bad081cb7ea06878e999)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsAwsWafv2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsAwsWafv2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsAwsWafv2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab1c86b69c91d89215faa65a2c7d66963d1793bfea89fd0c1eb713e7b936426f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fb1314403eddc9d853878d299ec1cb8ae2b598e32d0b6496c073d2804093c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979e9561f20a5d1da0a87f2073af6a7a8fa8e054e230aa0131d7f6cc4209380a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsAwsWafv2]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsWafv2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsAwsWafv2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8112051486758f03735e07486d35dba68ebc2579f90abdc4cb961da1f767cf93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsBilling",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudAwsIntegrationsBilling:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9ccb32fc89d2507f407cef214d9b76981c4a2617faf94bdbaa95a6ca60f3d7)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsBilling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsBillingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsBillingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a62b82999bd05c07ebf66e82fc1cd50209c887f3e8d6dc616b8642f2880f4679)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5dcbb93b5a3ec7ecb2b967fb94b1d9617184e309d8b240bc3497a0639781d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsBilling]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsBilling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsBilling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9b69b3eb4d71e529ac6b4536b8ceaaf0ec2e61eb0d3064868b86777f85484d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsCloudfront",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_lambdas_at_edge": "fetchLambdasAtEdge",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsCloudfront:
    def __init__(
        self,
        *,
        fetch_lambdas_at_edge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fetch_lambdas_at_edge: Specify if Lambdas@Edge should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_lambdas_at_edge CloudAwsIntegrations#fetch_lambdas_at_edge}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2266f63c7b7630abc91377c0b73f98ea11cdfc99572d6efd5d1717467b93268d)
            check_type(argname="argument fetch_lambdas_at_edge", value=fetch_lambdas_at_edge, expected_type=type_hints["fetch_lambdas_at_edge"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fetch_lambdas_at_edge is not None:
            self._values["fetch_lambdas_at_edge"] = fetch_lambdas_at_edge
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def fetch_lambdas_at_edge(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if Lambdas@Edge should be monitored.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_lambdas_at_edge CloudAwsIntegrations#fetch_lambdas_at_edge}
        '''
        result = self._values.get("fetch_lambdas_at_edge")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsCloudfront(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsCloudfrontOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsCloudfrontOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__132ed19a0f2762a2a6b1cee8263296884e7041980d1dca9a15fc28b94373f34e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFetchLambdasAtEdge")
    def reset_fetch_lambdas_at_edge(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchLambdasAtEdge", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="fetchLambdasAtEdgeInput")
    def fetch_lambdas_at_edge_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchLambdasAtEdgeInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchLambdasAtEdge")
    def fetch_lambdas_at_edge(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchLambdasAtEdge"))

    @fetch_lambdas_at_edge.setter
    def fetch_lambdas_at_edge(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce7268e8743febf91ec2c4b5fcca1df4cbe74f6a61c7bd59ca11276a934c88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchLambdasAtEdge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f1c94f60b7b6df1ef2f1c0585228308b55c572831bb596b27a7cb34e80f8a9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b86a8e638086bd572176d84fa6b53a13ac9c68ab9a354830d723baaa8b3a913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bac78be632b9df054c9395ac5b0eb2a280088708e1d302d19fa0a84e85b1113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1c4636ed02d9193a01ed51d804de2b184b4ed807b5ea50e3c04b5580e8a789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsCloudfront]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsCloudfront], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsCloudfront],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106fd6f9e62b93c8232fd1c042c4db950ff6af06b96d423f9df293d774c8e072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsCloudtrail",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsCloudtrail:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9133ba564bcdd8e4779348d80ab1c85ac796b37f55e670dd76c7e2d6c8aa73fb)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsCloudtrail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsCloudtrailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsCloudtrailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b6ddf9f2bfcf0c0e767bae6f5221261f7773891ee8bb2cb0935bb827b27f74a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a8e5ffa65cec1a9d99267d29a7d0df8763911839b2c7fc3ec6b822357589d34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac2025d900c573c9470c10047d81f45e617e5ba44b85dab88d0e5f8141da6b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsCloudtrail]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsCloudtrail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsCloudtrail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2520ae8e39751ad9964fa5eb5ebc623daec32d6e9e54c03ba08593b5e99b0f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "linked_account_id": "linkedAccountId",
        "account_id": "accountId",
        "alb": "alb",
        "api_gateway": "apiGateway",
        "auto_scaling": "autoScaling",
        "aws_app_sync": "awsAppSync",
        "aws_athena": "awsAthena",
        "aws_auto_discovery": "awsAutoDiscovery",
        "aws_cognito": "awsCognito",
        "aws_connect": "awsConnect",
        "aws_direct_connect": "awsDirectConnect",
        "aws_fsx": "awsFsx",
        "aws_glue": "awsGlue",
        "aws_kinesis_analytics": "awsKinesisAnalytics",
        "aws_media_convert": "awsMediaConvert",
        "aws_media_package_vod": "awsMediaPackageVod",
        "aws_mq": "awsMq",
        "aws_msk": "awsMsk",
        "aws_neptune": "awsNeptune",
        "aws_qldb": "awsQldb",
        "aws_route53_resolver": "awsRoute53Resolver",
        "aws_states": "awsStates",
        "aws_transit_gateway": "awsTransitGateway",
        "aws_waf": "awsWaf",
        "aws_wafv2": "awsWafv2",
        "billing": "billing",
        "cloudfront": "cloudfront",
        "cloudtrail": "cloudtrail",
        "doc_db": "docDb",
        "dynamodb": "dynamodb",
        "ebs": "ebs",
        "ec2": "ec2",
        "ecs": "ecs",
        "efs": "efs",
        "elasticache": "elasticache",
        "elasticbeanstalk": "elasticbeanstalk",
        "elasticsearch": "elasticsearch",
        "elb": "elb",
        "emr": "emr",
        "health": "health",
        "iam": "iam",
        "id": "id",
        "iot": "iot",
        "kinesis": "kinesis",
        "kinesis_firehose": "kinesisFirehose",
        "lambda_": "lambda",
        "rds": "rds",
        "redshift": "redshift",
        "route53": "route53",
        "s3": "s3",
        "ses": "ses",
        "sns": "sns",
        "sqs": "sqs",
        "trusted_advisor": "trustedAdvisor",
        "vpc": "vpc",
        "x_ray": "xRay",
    },
)
class CloudAwsIntegrationsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        alb: typing.Optional[typing.Union[CloudAwsIntegrationsAlb, typing.Dict[builtins.str, typing.Any]]] = None,
        api_gateway: typing.Optional[typing.Union[CloudAwsIntegrationsApiGateway, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scaling: typing.Optional[typing.Union[CloudAwsIntegrationsAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_app_sync: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAppSync, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_athena: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAthena, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_auto_discovery: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAutoDiscovery, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_cognito: typing.Optional[typing.Union[CloudAwsIntegrationsAwsCognito, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_connect: typing.Optional[typing.Union[CloudAwsIntegrationsAwsConnect, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_direct_connect: typing.Optional[typing.Union[CloudAwsIntegrationsAwsDirectConnect, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_fsx: typing.Optional[typing.Union[CloudAwsIntegrationsAwsFsx, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_glue: typing.Optional[typing.Union[CloudAwsIntegrationsAwsGlue, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_kinesis_analytics: typing.Optional[typing.Union[CloudAwsIntegrationsAwsKinesisAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_media_convert: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMediaConvert, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_media_package_vod: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMediaPackageVod, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_mq: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMq, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_msk: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMsk, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_neptune: typing.Optional[typing.Union[CloudAwsIntegrationsAwsNeptune, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_qldb: typing.Optional[typing.Union[CloudAwsIntegrationsAwsQldb, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_route53_resolver: typing.Optional[typing.Union[CloudAwsIntegrationsAwsRoute53Resolver, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_states: typing.Optional[typing.Union[CloudAwsIntegrationsAwsStates, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_transit_gateway: typing.Optional[typing.Union[CloudAwsIntegrationsAwsTransitGateway, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_waf: typing.Optional[typing.Union[CloudAwsIntegrationsAwsWaf, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_wafv2: typing.Optional[typing.Union[CloudAwsIntegrationsAwsWafv2, typing.Dict[builtins.str, typing.Any]]] = None,
        billing: typing.Optional[typing.Union[CloudAwsIntegrationsBilling, typing.Dict[builtins.str, typing.Any]]] = None,
        cloudfront: typing.Optional[typing.Union[CloudAwsIntegrationsCloudfront, typing.Dict[builtins.str, typing.Any]]] = None,
        cloudtrail: typing.Optional[typing.Union[CloudAwsIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
        doc_db: typing.Optional[typing.Union["CloudAwsIntegrationsDocDb", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamodb: typing.Optional[typing.Union["CloudAwsIntegrationsDynamodb", typing.Dict[builtins.str, typing.Any]]] = None,
        ebs: typing.Optional[typing.Union["CloudAwsIntegrationsEbs", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2: typing.Optional[typing.Union["CloudAwsIntegrationsEc2", typing.Dict[builtins.str, typing.Any]]] = None,
        ecs: typing.Optional[typing.Union["CloudAwsIntegrationsEcs", typing.Dict[builtins.str, typing.Any]]] = None,
        efs: typing.Optional[typing.Union["CloudAwsIntegrationsEfs", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticache: typing.Optional[typing.Union["CloudAwsIntegrationsElasticache", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticbeanstalk: typing.Optional[typing.Union["CloudAwsIntegrationsElasticbeanstalk", typing.Dict[builtins.str, typing.Any]]] = None,
        elasticsearch: typing.Optional[typing.Union["CloudAwsIntegrationsElasticsearch", typing.Dict[builtins.str, typing.Any]]] = None,
        elb: typing.Optional[typing.Union["CloudAwsIntegrationsElb", typing.Dict[builtins.str, typing.Any]]] = None,
        emr: typing.Optional[typing.Union["CloudAwsIntegrationsEmr", typing.Dict[builtins.str, typing.Any]]] = None,
        health: typing.Optional[typing.Union["CloudAwsIntegrationsHealth", typing.Dict[builtins.str, typing.Any]]] = None,
        iam: typing.Optional[typing.Union["CloudAwsIntegrationsIam", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        iot: typing.Optional[typing.Union["CloudAwsIntegrationsIot", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis: typing.Optional[typing.Union["CloudAwsIntegrationsKinesis", typing.Dict[builtins.str, typing.Any]]] = None,
        kinesis_firehose: typing.Optional[typing.Union["CloudAwsIntegrationsKinesisFirehose", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_: typing.Optional[typing.Union["CloudAwsIntegrationsLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        rds: typing.Optional[typing.Union["CloudAwsIntegrationsRds", typing.Dict[builtins.str, typing.Any]]] = None,
        redshift: typing.Optional[typing.Union["CloudAwsIntegrationsRedshift", typing.Dict[builtins.str, typing.Any]]] = None,
        route53: typing.Optional[typing.Union["CloudAwsIntegrationsRoute53", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["CloudAwsIntegrationsS3", typing.Dict[builtins.str, typing.Any]]] = None,
        ses: typing.Optional[typing.Union["CloudAwsIntegrationsSes", typing.Dict[builtins.str, typing.Any]]] = None,
        sns: typing.Optional[typing.Union["CloudAwsIntegrationsSns", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs: typing.Optional[typing.Union["CloudAwsIntegrationsSqs", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_advisor: typing.Optional[typing.Union["CloudAwsIntegrationsTrustedAdvisor", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[typing.Union["CloudAwsIntegrationsVpc", typing.Dict[builtins.str, typing.Any]]] = None,
        x_ray: typing.Optional[typing.Union["CloudAwsIntegrationsXRay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param linked_account_id: The ID of the linked AWS account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#linked_account_id CloudAwsIntegrations#linked_account_id}
        :param account_id: The ID of the account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#account_id CloudAwsIntegrations#account_id}
        :param alb: alb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#alb CloudAwsIntegrations#alb}
        :param api_gateway: api_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#api_gateway CloudAwsIntegrations#api_gateway}
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#auto_scaling CloudAwsIntegrations#auto_scaling}
        :param aws_app_sync: aws_app_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_app_sync CloudAwsIntegrations#aws_app_sync}
        :param aws_athena: aws_athena block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_athena CloudAwsIntegrations#aws_athena}
        :param aws_auto_discovery: aws_auto_discovery block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_auto_discovery CloudAwsIntegrations#aws_auto_discovery}
        :param aws_cognito: aws_cognito block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_cognito CloudAwsIntegrations#aws_cognito}
        :param aws_connect: aws_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_connect CloudAwsIntegrations#aws_connect}
        :param aws_direct_connect: aws_direct_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_direct_connect CloudAwsIntegrations#aws_direct_connect}
        :param aws_fsx: aws_fsx block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_fsx CloudAwsIntegrations#aws_fsx}
        :param aws_glue: aws_glue block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_glue CloudAwsIntegrations#aws_glue}
        :param aws_kinesis_analytics: aws_kinesis_analytics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_kinesis_analytics CloudAwsIntegrations#aws_kinesis_analytics}
        :param aws_media_convert: aws_media_convert block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_media_convert CloudAwsIntegrations#aws_media_convert}
        :param aws_media_package_vod: aws_media_package_vod block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_media_package_vod CloudAwsIntegrations#aws_media_package_vod}
        :param aws_mq: aws_mq block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_mq CloudAwsIntegrations#aws_mq}
        :param aws_msk: aws_msk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_msk CloudAwsIntegrations#aws_msk}
        :param aws_neptune: aws_neptune block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_neptune CloudAwsIntegrations#aws_neptune}
        :param aws_qldb: aws_qldb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_qldb CloudAwsIntegrations#aws_qldb}
        :param aws_route53_resolver: aws_route53resolver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_route53resolver CloudAwsIntegrations#aws_route53resolver}
        :param aws_states: aws_states block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_states CloudAwsIntegrations#aws_states}
        :param aws_transit_gateway: aws_transit_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_transit_gateway CloudAwsIntegrations#aws_transit_gateway}
        :param aws_waf: aws_waf block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_waf CloudAwsIntegrations#aws_waf}
        :param aws_wafv2: aws_wafv2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_wafv2 CloudAwsIntegrations#aws_wafv2}
        :param billing: billing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#billing CloudAwsIntegrations#billing}
        :param cloudfront: cloudfront block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#cloudfront CloudAwsIntegrations#cloudfront}
        :param cloudtrail: cloudtrail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#cloudtrail CloudAwsIntegrations#cloudtrail}
        :param doc_db: doc_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#doc_db CloudAwsIntegrations#doc_db}
        :param dynamodb: dynamodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#dynamodb CloudAwsIntegrations#dynamodb}
        :param ebs: ebs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ebs CloudAwsIntegrations#ebs}
        :param ec2: ec2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ec2 CloudAwsIntegrations#ec2}
        :param ecs: ecs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ecs CloudAwsIntegrations#ecs}
        :param efs: efs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#efs CloudAwsIntegrations#efs}
        :param elasticache: elasticache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticache CloudAwsIntegrations#elasticache}
        :param elasticbeanstalk: elasticbeanstalk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticbeanstalk CloudAwsIntegrations#elasticbeanstalk}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticsearch CloudAwsIntegrations#elasticsearch}
        :param elb: elb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elb CloudAwsIntegrations#elb}
        :param emr: emr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#emr CloudAwsIntegrations#emr}
        :param health: health block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#health CloudAwsIntegrations#health}
        :param iam: iam block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#iam CloudAwsIntegrations#iam}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#id CloudAwsIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iot: iot block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#iot CloudAwsIntegrations#iot}
        :param kinesis: kinesis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#kinesis CloudAwsIntegrations#kinesis}
        :param kinesis_firehose: kinesis_firehose block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#kinesis_firehose CloudAwsIntegrations#kinesis_firehose}
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#lambda CloudAwsIntegrations#lambda}
        :param rds: rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#rds CloudAwsIntegrations#rds}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#redshift CloudAwsIntegrations#redshift}
        :param route53: route53 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#route53 CloudAwsIntegrations#route53}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#s3 CloudAwsIntegrations#s3}
        :param ses: ses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ses CloudAwsIntegrations#ses}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#sns CloudAwsIntegrations#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#sqs CloudAwsIntegrations#sqs}
        :param trusted_advisor: trusted_advisor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#trusted_advisor CloudAwsIntegrations#trusted_advisor}
        :param vpc: vpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#vpc CloudAwsIntegrations#vpc}
        :param x_ray: x_ray block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#x_ray CloudAwsIntegrations#x_ray}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alb, dict):
            alb = CloudAwsIntegrationsAlb(**alb)
        if isinstance(api_gateway, dict):
            api_gateway = CloudAwsIntegrationsApiGateway(**api_gateway)
        if isinstance(auto_scaling, dict):
            auto_scaling = CloudAwsIntegrationsAutoScaling(**auto_scaling)
        if isinstance(aws_app_sync, dict):
            aws_app_sync = CloudAwsIntegrationsAwsAppSync(**aws_app_sync)
        if isinstance(aws_athena, dict):
            aws_athena = CloudAwsIntegrationsAwsAthena(**aws_athena)
        if isinstance(aws_auto_discovery, dict):
            aws_auto_discovery = CloudAwsIntegrationsAwsAutoDiscovery(**aws_auto_discovery)
        if isinstance(aws_cognito, dict):
            aws_cognito = CloudAwsIntegrationsAwsCognito(**aws_cognito)
        if isinstance(aws_connect, dict):
            aws_connect = CloudAwsIntegrationsAwsConnect(**aws_connect)
        if isinstance(aws_direct_connect, dict):
            aws_direct_connect = CloudAwsIntegrationsAwsDirectConnect(**aws_direct_connect)
        if isinstance(aws_fsx, dict):
            aws_fsx = CloudAwsIntegrationsAwsFsx(**aws_fsx)
        if isinstance(aws_glue, dict):
            aws_glue = CloudAwsIntegrationsAwsGlue(**aws_glue)
        if isinstance(aws_kinesis_analytics, dict):
            aws_kinesis_analytics = CloudAwsIntegrationsAwsKinesisAnalytics(**aws_kinesis_analytics)
        if isinstance(aws_media_convert, dict):
            aws_media_convert = CloudAwsIntegrationsAwsMediaConvert(**aws_media_convert)
        if isinstance(aws_media_package_vod, dict):
            aws_media_package_vod = CloudAwsIntegrationsAwsMediaPackageVod(**aws_media_package_vod)
        if isinstance(aws_mq, dict):
            aws_mq = CloudAwsIntegrationsAwsMq(**aws_mq)
        if isinstance(aws_msk, dict):
            aws_msk = CloudAwsIntegrationsAwsMsk(**aws_msk)
        if isinstance(aws_neptune, dict):
            aws_neptune = CloudAwsIntegrationsAwsNeptune(**aws_neptune)
        if isinstance(aws_qldb, dict):
            aws_qldb = CloudAwsIntegrationsAwsQldb(**aws_qldb)
        if isinstance(aws_route53_resolver, dict):
            aws_route53_resolver = CloudAwsIntegrationsAwsRoute53Resolver(**aws_route53_resolver)
        if isinstance(aws_states, dict):
            aws_states = CloudAwsIntegrationsAwsStates(**aws_states)
        if isinstance(aws_transit_gateway, dict):
            aws_transit_gateway = CloudAwsIntegrationsAwsTransitGateway(**aws_transit_gateway)
        if isinstance(aws_waf, dict):
            aws_waf = CloudAwsIntegrationsAwsWaf(**aws_waf)
        if isinstance(aws_wafv2, dict):
            aws_wafv2 = CloudAwsIntegrationsAwsWafv2(**aws_wafv2)
        if isinstance(billing, dict):
            billing = CloudAwsIntegrationsBilling(**billing)
        if isinstance(cloudfront, dict):
            cloudfront = CloudAwsIntegrationsCloudfront(**cloudfront)
        if isinstance(cloudtrail, dict):
            cloudtrail = CloudAwsIntegrationsCloudtrail(**cloudtrail)
        if isinstance(doc_db, dict):
            doc_db = CloudAwsIntegrationsDocDb(**doc_db)
        if isinstance(dynamodb, dict):
            dynamodb = CloudAwsIntegrationsDynamodb(**dynamodb)
        if isinstance(ebs, dict):
            ebs = CloudAwsIntegrationsEbs(**ebs)
        if isinstance(ec2, dict):
            ec2 = CloudAwsIntegrationsEc2(**ec2)
        if isinstance(ecs, dict):
            ecs = CloudAwsIntegrationsEcs(**ecs)
        if isinstance(efs, dict):
            efs = CloudAwsIntegrationsEfs(**efs)
        if isinstance(elasticache, dict):
            elasticache = CloudAwsIntegrationsElasticache(**elasticache)
        if isinstance(elasticbeanstalk, dict):
            elasticbeanstalk = CloudAwsIntegrationsElasticbeanstalk(**elasticbeanstalk)
        if isinstance(elasticsearch, dict):
            elasticsearch = CloudAwsIntegrationsElasticsearch(**elasticsearch)
        if isinstance(elb, dict):
            elb = CloudAwsIntegrationsElb(**elb)
        if isinstance(emr, dict):
            emr = CloudAwsIntegrationsEmr(**emr)
        if isinstance(health, dict):
            health = CloudAwsIntegrationsHealth(**health)
        if isinstance(iam, dict):
            iam = CloudAwsIntegrationsIam(**iam)
        if isinstance(iot, dict):
            iot = CloudAwsIntegrationsIot(**iot)
        if isinstance(kinesis, dict):
            kinesis = CloudAwsIntegrationsKinesis(**kinesis)
        if isinstance(kinesis_firehose, dict):
            kinesis_firehose = CloudAwsIntegrationsKinesisFirehose(**kinesis_firehose)
        if isinstance(lambda_, dict):
            lambda_ = CloudAwsIntegrationsLambda(**lambda_)
        if isinstance(rds, dict):
            rds = CloudAwsIntegrationsRds(**rds)
        if isinstance(redshift, dict):
            redshift = CloudAwsIntegrationsRedshift(**redshift)
        if isinstance(route53, dict):
            route53 = CloudAwsIntegrationsRoute53(**route53)
        if isinstance(s3, dict):
            s3 = CloudAwsIntegrationsS3(**s3)
        if isinstance(ses, dict):
            ses = CloudAwsIntegrationsSes(**ses)
        if isinstance(sns, dict):
            sns = CloudAwsIntegrationsSns(**sns)
        if isinstance(sqs, dict):
            sqs = CloudAwsIntegrationsSqs(**sqs)
        if isinstance(trusted_advisor, dict):
            trusted_advisor = CloudAwsIntegrationsTrustedAdvisor(**trusted_advisor)
        if isinstance(vpc, dict):
            vpc = CloudAwsIntegrationsVpc(**vpc)
        if isinstance(x_ray, dict):
            x_ray = CloudAwsIntegrationsXRay(**x_ray)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3ac5886f8796b4cd2e377d13a118f9277a15b3d6884b09bb067e13e9f18b87)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument linked_account_id", value=linked_account_id, expected_type=type_hints["linked_account_id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument alb", value=alb, expected_type=type_hints["alb"])
            check_type(argname="argument api_gateway", value=api_gateway, expected_type=type_hints["api_gateway"])
            check_type(argname="argument auto_scaling", value=auto_scaling, expected_type=type_hints["auto_scaling"])
            check_type(argname="argument aws_app_sync", value=aws_app_sync, expected_type=type_hints["aws_app_sync"])
            check_type(argname="argument aws_athena", value=aws_athena, expected_type=type_hints["aws_athena"])
            check_type(argname="argument aws_auto_discovery", value=aws_auto_discovery, expected_type=type_hints["aws_auto_discovery"])
            check_type(argname="argument aws_cognito", value=aws_cognito, expected_type=type_hints["aws_cognito"])
            check_type(argname="argument aws_connect", value=aws_connect, expected_type=type_hints["aws_connect"])
            check_type(argname="argument aws_direct_connect", value=aws_direct_connect, expected_type=type_hints["aws_direct_connect"])
            check_type(argname="argument aws_fsx", value=aws_fsx, expected_type=type_hints["aws_fsx"])
            check_type(argname="argument aws_glue", value=aws_glue, expected_type=type_hints["aws_glue"])
            check_type(argname="argument aws_kinesis_analytics", value=aws_kinesis_analytics, expected_type=type_hints["aws_kinesis_analytics"])
            check_type(argname="argument aws_media_convert", value=aws_media_convert, expected_type=type_hints["aws_media_convert"])
            check_type(argname="argument aws_media_package_vod", value=aws_media_package_vod, expected_type=type_hints["aws_media_package_vod"])
            check_type(argname="argument aws_mq", value=aws_mq, expected_type=type_hints["aws_mq"])
            check_type(argname="argument aws_msk", value=aws_msk, expected_type=type_hints["aws_msk"])
            check_type(argname="argument aws_neptune", value=aws_neptune, expected_type=type_hints["aws_neptune"])
            check_type(argname="argument aws_qldb", value=aws_qldb, expected_type=type_hints["aws_qldb"])
            check_type(argname="argument aws_route53_resolver", value=aws_route53_resolver, expected_type=type_hints["aws_route53_resolver"])
            check_type(argname="argument aws_states", value=aws_states, expected_type=type_hints["aws_states"])
            check_type(argname="argument aws_transit_gateway", value=aws_transit_gateway, expected_type=type_hints["aws_transit_gateway"])
            check_type(argname="argument aws_waf", value=aws_waf, expected_type=type_hints["aws_waf"])
            check_type(argname="argument aws_wafv2", value=aws_wafv2, expected_type=type_hints["aws_wafv2"])
            check_type(argname="argument billing", value=billing, expected_type=type_hints["billing"])
            check_type(argname="argument cloudfront", value=cloudfront, expected_type=type_hints["cloudfront"])
            check_type(argname="argument cloudtrail", value=cloudtrail, expected_type=type_hints["cloudtrail"])
            check_type(argname="argument doc_db", value=doc_db, expected_type=type_hints["doc_db"])
            check_type(argname="argument dynamodb", value=dynamodb, expected_type=type_hints["dynamodb"])
            check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
            check_type(argname="argument ec2", value=ec2, expected_type=type_hints["ec2"])
            check_type(argname="argument ecs", value=ecs, expected_type=type_hints["ecs"])
            check_type(argname="argument efs", value=efs, expected_type=type_hints["efs"])
            check_type(argname="argument elasticache", value=elasticache, expected_type=type_hints["elasticache"])
            check_type(argname="argument elasticbeanstalk", value=elasticbeanstalk, expected_type=type_hints["elasticbeanstalk"])
            check_type(argname="argument elasticsearch", value=elasticsearch, expected_type=type_hints["elasticsearch"])
            check_type(argname="argument elb", value=elb, expected_type=type_hints["elb"])
            check_type(argname="argument emr", value=emr, expected_type=type_hints["emr"])
            check_type(argname="argument health", value=health, expected_type=type_hints["health"])
            check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iot", value=iot, expected_type=type_hints["iot"])
            check_type(argname="argument kinesis", value=kinesis, expected_type=type_hints["kinesis"])
            check_type(argname="argument kinesis_firehose", value=kinesis_firehose, expected_type=type_hints["kinesis_firehose"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument rds", value=rds, expected_type=type_hints["rds"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument ses", value=ses, expected_type=type_hints["ses"])
            check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            check_type(argname="argument trusted_advisor", value=trusted_advisor, expected_type=type_hints["trusted_advisor"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument x_ray", value=x_ray, expected_type=type_hints["x_ray"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_account_id": linked_account_id,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if alb is not None:
            self._values["alb"] = alb
        if api_gateway is not None:
            self._values["api_gateway"] = api_gateway
        if auto_scaling is not None:
            self._values["auto_scaling"] = auto_scaling
        if aws_app_sync is not None:
            self._values["aws_app_sync"] = aws_app_sync
        if aws_athena is not None:
            self._values["aws_athena"] = aws_athena
        if aws_auto_discovery is not None:
            self._values["aws_auto_discovery"] = aws_auto_discovery
        if aws_cognito is not None:
            self._values["aws_cognito"] = aws_cognito
        if aws_connect is not None:
            self._values["aws_connect"] = aws_connect
        if aws_direct_connect is not None:
            self._values["aws_direct_connect"] = aws_direct_connect
        if aws_fsx is not None:
            self._values["aws_fsx"] = aws_fsx
        if aws_glue is not None:
            self._values["aws_glue"] = aws_glue
        if aws_kinesis_analytics is not None:
            self._values["aws_kinesis_analytics"] = aws_kinesis_analytics
        if aws_media_convert is not None:
            self._values["aws_media_convert"] = aws_media_convert
        if aws_media_package_vod is not None:
            self._values["aws_media_package_vod"] = aws_media_package_vod
        if aws_mq is not None:
            self._values["aws_mq"] = aws_mq
        if aws_msk is not None:
            self._values["aws_msk"] = aws_msk
        if aws_neptune is not None:
            self._values["aws_neptune"] = aws_neptune
        if aws_qldb is not None:
            self._values["aws_qldb"] = aws_qldb
        if aws_route53_resolver is not None:
            self._values["aws_route53_resolver"] = aws_route53_resolver
        if aws_states is not None:
            self._values["aws_states"] = aws_states
        if aws_transit_gateway is not None:
            self._values["aws_transit_gateway"] = aws_transit_gateway
        if aws_waf is not None:
            self._values["aws_waf"] = aws_waf
        if aws_wafv2 is not None:
            self._values["aws_wafv2"] = aws_wafv2
        if billing is not None:
            self._values["billing"] = billing
        if cloudfront is not None:
            self._values["cloudfront"] = cloudfront
        if cloudtrail is not None:
            self._values["cloudtrail"] = cloudtrail
        if doc_db is not None:
            self._values["doc_db"] = doc_db
        if dynamodb is not None:
            self._values["dynamodb"] = dynamodb
        if ebs is not None:
            self._values["ebs"] = ebs
        if ec2 is not None:
            self._values["ec2"] = ec2
        if ecs is not None:
            self._values["ecs"] = ecs
        if efs is not None:
            self._values["efs"] = efs
        if elasticache is not None:
            self._values["elasticache"] = elasticache
        if elasticbeanstalk is not None:
            self._values["elasticbeanstalk"] = elasticbeanstalk
        if elasticsearch is not None:
            self._values["elasticsearch"] = elasticsearch
        if elb is not None:
            self._values["elb"] = elb
        if emr is not None:
            self._values["emr"] = emr
        if health is not None:
            self._values["health"] = health
        if iam is not None:
            self._values["iam"] = iam
        if id is not None:
            self._values["id"] = id
        if iot is not None:
            self._values["iot"] = iot
        if kinesis is not None:
            self._values["kinesis"] = kinesis
        if kinesis_firehose is not None:
            self._values["kinesis_firehose"] = kinesis_firehose
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if rds is not None:
            self._values["rds"] = rds
        if redshift is not None:
            self._values["redshift"] = redshift
        if route53 is not None:
            self._values["route53"] = route53
        if s3 is not None:
            self._values["s3"] = s3
        if ses is not None:
            self._values["ses"] = ses
        if sns is not None:
            self._values["sns"] = sns
        if sqs is not None:
            self._values["sqs"] = sqs
        if trusted_advisor is not None:
            self._values["trusted_advisor"] = trusted_advisor
        if vpc is not None:
            self._values["vpc"] = vpc
        if x_ray is not None:
            self._values["x_ray"] = x_ray

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
    def linked_account_id(self) -> jsii.Number:
        '''The ID of the linked AWS account in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#linked_account_id CloudAwsIntegrations#linked_account_id}
        '''
        result = self._values.get("linked_account_id")
        assert result is not None, "Required property 'linked_account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the account in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#account_id CloudAwsIntegrations#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alb(self) -> typing.Optional[CloudAwsIntegrationsAlb]:
        '''alb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#alb CloudAwsIntegrations#alb}
        '''
        result = self._values.get("alb")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAlb], result)

    @builtins.property
    def api_gateway(self) -> typing.Optional[CloudAwsIntegrationsApiGateway]:
        '''api_gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#api_gateway CloudAwsIntegrations#api_gateway}
        '''
        result = self._values.get("api_gateway")
        return typing.cast(typing.Optional[CloudAwsIntegrationsApiGateway], result)

    @builtins.property
    def auto_scaling(self) -> typing.Optional[CloudAwsIntegrationsAutoScaling]:
        '''auto_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#auto_scaling CloudAwsIntegrations#auto_scaling}
        '''
        result = self._values.get("auto_scaling")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAutoScaling], result)

    @builtins.property
    def aws_app_sync(self) -> typing.Optional[CloudAwsIntegrationsAwsAppSync]:
        '''aws_app_sync block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_app_sync CloudAwsIntegrations#aws_app_sync}
        '''
        result = self._values.get("aws_app_sync")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsAppSync], result)

    @builtins.property
    def aws_athena(self) -> typing.Optional[CloudAwsIntegrationsAwsAthena]:
        '''aws_athena block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_athena CloudAwsIntegrations#aws_athena}
        '''
        result = self._values.get("aws_athena")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsAthena], result)

    @builtins.property
    def aws_auto_discovery(
        self,
    ) -> typing.Optional[CloudAwsIntegrationsAwsAutoDiscovery]:
        '''aws_auto_discovery block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_auto_discovery CloudAwsIntegrations#aws_auto_discovery}
        '''
        result = self._values.get("aws_auto_discovery")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsAutoDiscovery], result)

    @builtins.property
    def aws_cognito(self) -> typing.Optional[CloudAwsIntegrationsAwsCognito]:
        '''aws_cognito block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_cognito CloudAwsIntegrations#aws_cognito}
        '''
        result = self._values.get("aws_cognito")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsCognito], result)

    @builtins.property
    def aws_connect(self) -> typing.Optional[CloudAwsIntegrationsAwsConnect]:
        '''aws_connect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_connect CloudAwsIntegrations#aws_connect}
        '''
        result = self._values.get("aws_connect")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsConnect], result)

    @builtins.property
    def aws_direct_connect(
        self,
    ) -> typing.Optional[CloudAwsIntegrationsAwsDirectConnect]:
        '''aws_direct_connect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_direct_connect CloudAwsIntegrations#aws_direct_connect}
        '''
        result = self._values.get("aws_direct_connect")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsDirectConnect], result)

    @builtins.property
    def aws_fsx(self) -> typing.Optional[CloudAwsIntegrationsAwsFsx]:
        '''aws_fsx block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_fsx CloudAwsIntegrations#aws_fsx}
        '''
        result = self._values.get("aws_fsx")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsFsx], result)

    @builtins.property
    def aws_glue(self) -> typing.Optional[CloudAwsIntegrationsAwsGlue]:
        '''aws_glue block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_glue CloudAwsIntegrations#aws_glue}
        '''
        result = self._values.get("aws_glue")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsGlue], result)

    @builtins.property
    def aws_kinesis_analytics(
        self,
    ) -> typing.Optional[CloudAwsIntegrationsAwsKinesisAnalytics]:
        '''aws_kinesis_analytics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_kinesis_analytics CloudAwsIntegrations#aws_kinesis_analytics}
        '''
        result = self._values.get("aws_kinesis_analytics")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsKinesisAnalytics], result)

    @builtins.property
    def aws_media_convert(self) -> typing.Optional[CloudAwsIntegrationsAwsMediaConvert]:
        '''aws_media_convert block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_media_convert CloudAwsIntegrations#aws_media_convert}
        '''
        result = self._values.get("aws_media_convert")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsMediaConvert], result)

    @builtins.property
    def aws_media_package_vod(
        self,
    ) -> typing.Optional[CloudAwsIntegrationsAwsMediaPackageVod]:
        '''aws_media_package_vod block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_media_package_vod CloudAwsIntegrations#aws_media_package_vod}
        '''
        result = self._values.get("aws_media_package_vod")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsMediaPackageVod], result)

    @builtins.property
    def aws_mq(self) -> typing.Optional[CloudAwsIntegrationsAwsMq]:
        '''aws_mq block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_mq CloudAwsIntegrations#aws_mq}
        '''
        result = self._values.get("aws_mq")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsMq], result)

    @builtins.property
    def aws_msk(self) -> typing.Optional[CloudAwsIntegrationsAwsMsk]:
        '''aws_msk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_msk CloudAwsIntegrations#aws_msk}
        '''
        result = self._values.get("aws_msk")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsMsk], result)

    @builtins.property
    def aws_neptune(self) -> typing.Optional[CloudAwsIntegrationsAwsNeptune]:
        '''aws_neptune block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_neptune CloudAwsIntegrations#aws_neptune}
        '''
        result = self._values.get("aws_neptune")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsNeptune], result)

    @builtins.property
    def aws_qldb(self) -> typing.Optional[CloudAwsIntegrationsAwsQldb]:
        '''aws_qldb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_qldb CloudAwsIntegrations#aws_qldb}
        '''
        result = self._values.get("aws_qldb")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsQldb], result)

    @builtins.property
    def aws_route53_resolver(
        self,
    ) -> typing.Optional[CloudAwsIntegrationsAwsRoute53Resolver]:
        '''aws_route53resolver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_route53resolver CloudAwsIntegrations#aws_route53resolver}
        '''
        result = self._values.get("aws_route53_resolver")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsRoute53Resolver], result)

    @builtins.property
    def aws_states(self) -> typing.Optional[CloudAwsIntegrationsAwsStates]:
        '''aws_states block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_states CloudAwsIntegrations#aws_states}
        '''
        result = self._values.get("aws_states")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsStates], result)

    @builtins.property
    def aws_transit_gateway(
        self,
    ) -> typing.Optional[CloudAwsIntegrationsAwsTransitGateway]:
        '''aws_transit_gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_transit_gateway CloudAwsIntegrations#aws_transit_gateway}
        '''
        result = self._values.get("aws_transit_gateway")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsTransitGateway], result)

    @builtins.property
    def aws_waf(self) -> typing.Optional[CloudAwsIntegrationsAwsWaf]:
        '''aws_waf block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_waf CloudAwsIntegrations#aws_waf}
        '''
        result = self._values.get("aws_waf")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsWaf], result)

    @builtins.property
    def aws_wafv2(self) -> typing.Optional[CloudAwsIntegrationsAwsWafv2]:
        '''aws_wafv2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_wafv2 CloudAwsIntegrations#aws_wafv2}
        '''
        result = self._values.get("aws_wafv2")
        return typing.cast(typing.Optional[CloudAwsIntegrationsAwsWafv2], result)

    @builtins.property
    def billing(self) -> typing.Optional[CloudAwsIntegrationsBilling]:
        '''billing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#billing CloudAwsIntegrations#billing}
        '''
        result = self._values.get("billing")
        return typing.cast(typing.Optional[CloudAwsIntegrationsBilling], result)

    @builtins.property
    def cloudfront(self) -> typing.Optional[CloudAwsIntegrationsCloudfront]:
        '''cloudfront block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#cloudfront CloudAwsIntegrations#cloudfront}
        '''
        result = self._values.get("cloudfront")
        return typing.cast(typing.Optional[CloudAwsIntegrationsCloudfront], result)

    @builtins.property
    def cloudtrail(self) -> typing.Optional[CloudAwsIntegrationsCloudtrail]:
        '''cloudtrail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#cloudtrail CloudAwsIntegrations#cloudtrail}
        '''
        result = self._values.get("cloudtrail")
        return typing.cast(typing.Optional[CloudAwsIntegrationsCloudtrail], result)

    @builtins.property
    def doc_db(self) -> typing.Optional["CloudAwsIntegrationsDocDb"]:
        '''doc_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#doc_db CloudAwsIntegrations#doc_db}
        '''
        result = self._values.get("doc_db")
        return typing.cast(typing.Optional["CloudAwsIntegrationsDocDb"], result)

    @builtins.property
    def dynamodb(self) -> typing.Optional["CloudAwsIntegrationsDynamodb"]:
        '''dynamodb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#dynamodb CloudAwsIntegrations#dynamodb}
        '''
        result = self._values.get("dynamodb")
        return typing.cast(typing.Optional["CloudAwsIntegrationsDynamodb"], result)

    @builtins.property
    def ebs(self) -> typing.Optional["CloudAwsIntegrationsEbs"]:
        '''ebs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ebs CloudAwsIntegrations#ebs}
        '''
        result = self._values.get("ebs")
        return typing.cast(typing.Optional["CloudAwsIntegrationsEbs"], result)

    @builtins.property
    def ec2(self) -> typing.Optional["CloudAwsIntegrationsEc2"]:
        '''ec2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ec2 CloudAwsIntegrations#ec2}
        '''
        result = self._values.get("ec2")
        return typing.cast(typing.Optional["CloudAwsIntegrationsEc2"], result)

    @builtins.property
    def ecs(self) -> typing.Optional["CloudAwsIntegrationsEcs"]:
        '''ecs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ecs CloudAwsIntegrations#ecs}
        '''
        result = self._values.get("ecs")
        return typing.cast(typing.Optional["CloudAwsIntegrationsEcs"], result)

    @builtins.property
    def efs(self) -> typing.Optional["CloudAwsIntegrationsEfs"]:
        '''efs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#efs CloudAwsIntegrations#efs}
        '''
        result = self._values.get("efs")
        return typing.cast(typing.Optional["CloudAwsIntegrationsEfs"], result)

    @builtins.property
    def elasticache(self) -> typing.Optional["CloudAwsIntegrationsElasticache"]:
        '''elasticache block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticache CloudAwsIntegrations#elasticache}
        '''
        result = self._values.get("elasticache")
        return typing.cast(typing.Optional["CloudAwsIntegrationsElasticache"], result)

    @builtins.property
    def elasticbeanstalk(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsElasticbeanstalk"]:
        '''elasticbeanstalk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticbeanstalk CloudAwsIntegrations#elasticbeanstalk}
        '''
        result = self._values.get("elasticbeanstalk")
        return typing.cast(typing.Optional["CloudAwsIntegrationsElasticbeanstalk"], result)

    @builtins.property
    def elasticsearch(self) -> typing.Optional["CloudAwsIntegrationsElasticsearch"]:
        '''elasticsearch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elasticsearch CloudAwsIntegrations#elasticsearch}
        '''
        result = self._values.get("elasticsearch")
        return typing.cast(typing.Optional["CloudAwsIntegrationsElasticsearch"], result)

    @builtins.property
    def elb(self) -> typing.Optional["CloudAwsIntegrationsElb"]:
        '''elb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#elb CloudAwsIntegrations#elb}
        '''
        result = self._values.get("elb")
        return typing.cast(typing.Optional["CloudAwsIntegrationsElb"], result)

    @builtins.property
    def emr(self) -> typing.Optional["CloudAwsIntegrationsEmr"]:
        '''emr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#emr CloudAwsIntegrations#emr}
        '''
        result = self._values.get("emr")
        return typing.cast(typing.Optional["CloudAwsIntegrationsEmr"], result)

    @builtins.property
    def health(self) -> typing.Optional["CloudAwsIntegrationsHealth"]:
        '''health block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#health CloudAwsIntegrations#health}
        '''
        result = self._values.get("health")
        return typing.cast(typing.Optional["CloudAwsIntegrationsHealth"], result)

    @builtins.property
    def iam(self) -> typing.Optional["CloudAwsIntegrationsIam"]:
        '''iam block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#iam CloudAwsIntegrations#iam}
        '''
        result = self._values.get("iam")
        return typing.cast(typing.Optional["CloudAwsIntegrationsIam"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#id CloudAwsIntegrations#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iot(self) -> typing.Optional["CloudAwsIntegrationsIot"]:
        '''iot block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#iot CloudAwsIntegrations#iot}
        '''
        result = self._values.get("iot")
        return typing.cast(typing.Optional["CloudAwsIntegrationsIot"], result)

    @builtins.property
    def kinesis(self) -> typing.Optional["CloudAwsIntegrationsKinesis"]:
        '''kinesis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#kinesis CloudAwsIntegrations#kinesis}
        '''
        result = self._values.get("kinesis")
        return typing.cast(typing.Optional["CloudAwsIntegrationsKinesis"], result)

    @builtins.property
    def kinesis_firehose(
        self,
    ) -> typing.Optional["CloudAwsIntegrationsKinesisFirehose"]:
        '''kinesis_firehose block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#kinesis_firehose CloudAwsIntegrations#kinesis_firehose}
        '''
        result = self._values.get("kinesis_firehose")
        return typing.cast(typing.Optional["CloudAwsIntegrationsKinesisFirehose"], result)

    @builtins.property
    def lambda_(self) -> typing.Optional["CloudAwsIntegrationsLambda"]:
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#lambda CloudAwsIntegrations#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional["CloudAwsIntegrationsLambda"], result)

    @builtins.property
    def rds(self) -> typing.Optional["CloudAwsIntegrationsRds"]:
        '''rds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#rds CloudAwsIntegrations#rds}
        '''
        result = self._values.get("rds")
        return typing.cast(typing.Optional["CloudAwsIntegrationsRds"], result)

    @builtins.property
    def redshift(self) -> typing.Optional["CloudAwsIntegrationsRedshift"]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#redshift CloudAwsIntegrations#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional["CloudAwsIntegrationsRedshift"], result)

    @builtins.property
    def route53(self) -> typing.Optional["CloudAwsIntegrationsRoute53"]:
        '''route53 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#route53 CloudAwsIntegrations#route53}
        '''
        result = self._values.get("route53")
        return typing.cast(typing.Optional["CloudAwsIntegrationsRoute53"], result)

    @builtins.property
    def s3(self) -> typing.Optional["CloudAwsIntegrationsS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#s3 CloudAwsIntegrations#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["CloudAwsIntegrationsS3"], result)

    @builtins.property
    def ses(self) -> typing.Optional["CloudAwsIntegrationsSes"]:
        '''ses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#ses CloudAwsIntegrations#ses}
        '''
        result = self._values.get("ses")
        return typing.cast(typing.Optional["CloudAwsIntegrationsSes"], result)

    @builtins.property
    def sns(self) -> typing.Optional["CloudAwsIntegrationsSns"]:
        '''sns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#sns CloudAwsIntegrations#sns}
        '''
        result = self._values.get("sns")
        return typing.cast(typing.Optional["CloudAwsIntegrationsSns"], result)

    @builtins.property
    def sqs(self) -> typing.Optional["CloudAwsIntegrationsSqs"]:
        '''sqs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#sqs CloudAwsIntegrations#sqs}
        '''
        result = self._values.get("sqs")
        return typing.cast(typing.Optional["CloudAwsIntegrationsSqs"], result)

    @builtins.property
    def trusted_advisor(self) -> typing.Optional["CloudAwsIntegrationsTrustedAdvisor"]:
        '''trusted_advisor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#trusted_advisor CloudAwsIntegrations#trusted_advisor}
        '''
        result = self._values.get("trusted_advisor")
        return typing.cast(typing.Optional["CloudAwsIntegrationsTrustedAdvisor"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["CloudAwsIntegrationsVpc"]:
        '''vpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#vpc CloudAwsIntegrations#vpc}
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["CloudAwsIntegrationsVpc"], result)

    @builtins.property
    def x_ray(self) -> typing.Optional["CloudAwsIntegrationsXRay"]:
        '''x_ray block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#x_ray CloudAwsIntegrations#x_ray}
        '''
        result = self._values.get("x_ray")
        return typing.cast(typing.Optional["CloudAwsIntegrationsXRay"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsDocDb",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsDocDb:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b58ef8635db36e48a559b28b40b82ec4dd41bcbf964598d8e8c2610059fab98)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsDocDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsDocDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsDocDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1ceccfccb2c01b0f9212f0432a797550e67fbdd0276877c6b924299041c1031)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ebc6521dc6dbb79edfa912af0c774c5085a0c22a1fddfcb7136dfa7d1b116b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0251404e38849d33ade8e61fb4a4f375b9f0abdad07106312e45c3d4b21750a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsDocDb]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsDocDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsDocDb]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc4f66bc4ff0d503483eee5301c5ff5f022809adb60e47f7984abedc805bb6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsDynamodb",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsDynamodb:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5578f1d84d4136281045d42ad8cd804a13cc5131e1178f2fccd5b32eb19d5c5)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags and the extended inventory should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsDynamodb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsDynamodbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsDynamodbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d63de01db4ae0b0c1bb57e122b9de70208908339a87fea7db52de6be41399f47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8967537590fd407ef87b17cdb3e8e14573bcc6eb2783e6aeaf26921ad387a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6eef481b4e6030a18404931159f971595bdbc8c35991b41abffa6f42d1de1d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e31eb274e4bee47ad7d113887cdd0dd1949d31f810f808ed9fd4ec41ba112f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4148f25094ab70de41d3490c6f56d99a8a90ce1a2338b03739e4589f51264ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8896f374709a77e40838e0baf47c1b340d607a26eea31360e4a78f8a025585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214da2ecdf3995075af216f69b0f82ce4e4cfb3ca0c190d27f819d6c091e20ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsDynamodb]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsDynamodb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsDynamodb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d074c5d8cf91a2b0c05e3fc8b374afcd939f649d899d2c7eb064d257556d6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEbs",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsEbs:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__909f355c4271f6dcaecbb07f9ada237cc94ab8c821a91e5bafe9fa11b0eaa605)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsEbs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsEbsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEbsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad2f8518ae0401dc8f55b50b3c4f7351d29e2e022e1474c44c76b6f83aa9f58e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f4efed1910cb6ed6c2b896da5a388a514dc242df2299bec08795f96bdd0486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36730bf112da13b303a8cd641ce619002c519eb7ac18cb5dd167683f9cdb69c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a615ef6c4966b9a26cc111d73aea7d15f816d304d60e6737c402a3722f5d7e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95154e577bf4ae3b0391027960e94449016f015171fd62ae84f5db2dbe8f54de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bc95bebc9d91ac422ba41d510ba209286dd5faa95a22078d42ec2d106b948d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsEbs]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsEbs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsEbs]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef261a2f59459427265681ecb47f61448eeba8cef04471586c8e9342b09dab59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEc2",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "duplicate_ec2_tags": "duplicateEc2Tags",
        "fetch_ip_addresses": "fetchIpAddresses",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsEc2:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        duplicate_ec2_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param duplicate_ec2_tags: Specify if the old legacy metadata and tag names have to be kept, it will consume more ingest data size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#duplicate_ec2_tags CloudAwsIntegrations#duplicate_ec2_tags}
        :param fetch_ip_addresses: Specify if IP addresses of ec2 instance should be collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_ip_addresses CloudAwsIntegrations#fetch_ip_addresses}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f43c746d4c560876d4d23b2e3ac9f26d25f5d2e33dc79ae443a705b90e24b71)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument duplicate_ec2_tags", value=duplicate_ec2_tags, expected_type=type_hints["duplicate_ec2_tags"])
            check_type(argname="argument fetch_ip_addresses", value=fetch_ip_addresses, expected_type=type_hints["fetch_ip_addresses"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if duplicate_ec2_tags is not None:
            self._values["duplicate_ec2_tags"] = duplicate_ec2_tags
        if fetch_ip_addresses is not None:
            self._values["fetch_ip_addresses"] = fetch_ip_addresses
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def duplicate_ec2_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if the old legacy metadata and tag names have to be kept, it will consume more ingest data size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#duplicate_ec2_tags CloudAwsIntegrations#duplicate_ec2_tags}
        '''
        result = self._values.get("duplicate_ec2_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_ip_addresses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if IP addresses of ec2 instance should be collected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_ip_addresses CloudAwsIntegrations#fetch_ip_addresses}
        '''
        result = self._values.get("fetch_ip_addresses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsEc2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsEc2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEc2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8d0e44efc7af60ebfa03a5a86beab29b50854db698b9add74de4af7511dc208)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetDuplicateEc2Tags")
    def reset_duplicate_ec2_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuplicateEc2Tags", []))

    @jsii.member(jsii_name="resetFetchIpAddresses")
    def reset_fetch_ip_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchIpAddresses", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="duplicateEc2TagsInput")
    def duplicate_ec2_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "duplicateEc2TagsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchIpAddressesInput")
    def fetch_ip_addresses_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchIpAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f70e897d6e07ca582f442aa67a4238fc441d7ed6d2101aca280de768d00022)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="duplicateEc2Tags")
    def duplicate_ec2_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "duplicateEc2Tags"))

    @duplicate_ec2_tags.setter
    def duplicate_ec2_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1319c85e3996edbda499bf468ecf07a57c6ff4faad9c62aa3f872d0cd3e876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duplicateEc2Tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchIpAddresses")
    def fetch_ip_addresses(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchIpAddresses"))

    @fetch_ip_addresses.setter
    def fetch_ip_addresses(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5001c87823109b828438df45d3fbf09c57161ad5dce1335088101874e688d976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchIpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92016a3e32fb89496b7009b1a4164d395271a410864f684d523e7350505b1110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fcd8bb774b145606b7e8ca4a0cfbfc7f02e1a7d34405156e0d9c4a011c46994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323a8830d16f0df2a0373e5b3f11abe645251534cc308610384f5658f4422410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsEc2]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsEc2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsEc2]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e0a2272f9f3d13c8b605d90c2976aa911d6152fa5df7c11ec718c9ee153985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEcs",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsEcs:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83f796e181d26247d104c9fe70d8764649915e7028d5c62c4a7e5aae71137df)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags and the extended inventory should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsEcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsEcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e7f35a8ea2e54751e87118bd9b91f7f50aa5231cb42be6721315b2aeaf0853f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ae09cdaef0014ca4e52a20b13d2ca4130f94eaaf1ef2573f5b17d4fc094966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe554c4db75816ff439117503f934bf5cffd8179eed2fdc392e5e8e809c7876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cda46e7545cb6438ad8794452725911a86b109d1c713ad678e1b48f2127e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed42d7f1f910630dff244b510469d2406c7a09dfe1189f929830d720093e4d25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d00e3a4e413092a1199b3eeff85440058c95324889086a9d38fdaf6a78c67c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsEcs]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsEcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsEcs]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04ab7b63047bd06debb3888a68adb0c8d569b5653fc26cdd56673eb08cc656f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEfs",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsEfs:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51591c32b4d16705f46eafcbda67feaad34a0e245798a8aca05542df9e22bb4f)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags and the extended inventory should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsEfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsEfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb68c778c42f4a39a9cb09b0001cc862f8cfd2c428b4765f548f2a9285fbc285)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4e7da1fdba58ca9f9235d58ae728836b6997a4c23c350265e2207787288bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca6f02f52c7706c8bae670add60262e80cca377f2ee7b74895d71e639b8da87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d26e7592d9ee7867e96025243cd89109dea2730dc9a8ce1036ab5a531b10278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b60ecc72e4c238fed0e9b5cb57860a8842693a125917dee4e365523246e6c5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d87edd35880b88d4f04aadab968ed216ac39e7ff1b65887bc81eb418c3df66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsEfs]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsEfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsEfs]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d8497c781988fc405051efea0c0a299b2ef0158f81e1b017b49cf49b6a2827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsElasticache",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsElasticache:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a265d833358b069d2e6598bcd48148ee03e786160cd47ea8e1515310681517)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsElasticache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsElasticacheOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsElasticacheOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__982457a0f6895e0cc9e1f80aac5819a710b35fe5e69e1ad37a8566845b24346f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f099daa9bd9e534c0a0e2779af92e057c7aee6d6f0750ca8e3273d49f44509c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c301267e8f5404c845359347350c0719602845136378747ad9233a1c1ec9bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a74d1d6c880c68a800086be7ded5465334eb72d5d1427ee5568066ad8673059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d0a572643e1fb4e4492e03f8e8fe7f19bd6dcd5a0cfdf59ba556fc0b47d6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__905e8b6e7e65d5ad8d98505c01e090be4e9b9a38eea9bbf29a9c8ff00b48ba92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsElasticache]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsElasticache], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsElasticache],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8994f3840bdf7c9bc56e11e083f5a7cc92c467fc900aa90d6e93c38ad2578349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsElasticbeanstalk",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsElasticbeanstalk:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f1ab201b42323e7a38236319998e1fd03d900f7c3f1dc464357c54b3f73f19)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags and the extended inventory should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsElasticbeanstalk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsElasticbeanstalkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsElasticbeanstalkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2095c6e31c5df5691a2caec253ebecb0ad4d69eede26c171b338804c1eb2d59c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d415eb8246fba884efdfbc5b23e202cb470d149d485023f40255151a70163c47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bfa72c0e5e1f6bae095d8cf592ac0bc8dc2a8cc8a551ef99532da4dd16e8cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b665bcaa8758e845578c2711d3fcd1f633ed09312baa00de505a39734ff8d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0d51f66e7cd5e881f79f1275935dd80bf5d65610599f71b153542ed53a9b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e78a38e92d32a750149df2e09b652169e17f584297a8d3afece2d98e5816ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b14840bc60eb2113f8b5ce031dc5d96b2eed7b0b9eb3b50dfd5414df78bf54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsElasticbeanstalk]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsElasticbeanstalk], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsElasticbeanstalk],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14643cb6d24f18eab2712e31c07817044c9a9f99cd7f0a7639fa7b00151343e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsElasticsearch",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_nodes": "fetchNodes",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsElasticsearch:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_nodes: Specify if metrics should be collected for nodes. Turning it on will increase the number of API calls made to CloudWatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_nodes CloudAwsIntegrations#fetch_nodes}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7727f9fe6b3572b1bb784fe6ea29840ccd3473caefa3749c6e0d683041068f34)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_nodes", value=fetch_nodes, expected_type=type_hints["fetch_nodes"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_nodes is not None:
            self._values["fetch_nodes"] = fetch_nodes
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_nodes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if metrics should be collected for nodes.

        Turning it on will increase the number of API calls made to CloudWatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_nodes CloudAwsIntegrations#fetch_nodes}
        '''
        result = self._values.get("fetch_nodes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsElasticsearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsElasticsearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsElasticsearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94ce0bcd96b43b1a66a79cd12005994824450ab6811f480d8efbd9d835e66d05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchNodes")
    def reset_fetch_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchNodes", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchNodesInput")
    def fetch_nodes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchNodesInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d785760cff6d1ab0700dcc823e4942dff3886b2d1ce53e87f7773c0cc461d0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchNodes")
    def fetch_nodes(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchNodes"))

    @fetch_nodes.setter
    def fetch_nodes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036153fad20e50dba10f4423848c9e081d324b1c20ec20543f09cd494ae3320d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06ddc1ca114209c58bc8b9e5f6fbd635dd8ba5fb926b0e7425896d3a2504d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a726fd17918d907da54c6711491bbf2716e17dcdd9fca2a5f4e65842095846c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2dde2ce82e59bbbac227b29ea13d4629295d80ef1ac7523c1753279bd03176d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsElasticsearch]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsElasticsearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsElasticsearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec34d47c44aeb8721aaa4b1644fb4debb947f313c9c7a58ebac0f68610ccc860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsElb",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsElb:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2884a4a766bd7a950c15bbaeecf493edfc5cb79afb317f70265d74e003c296)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsElb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsElbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsElbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5895c6677f231b40721945fcb94cbef8a4374063716946e207a239150d1d17c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c94e0ea139f50608fccc2d99fbac64efe829bf3305593d8bd6c98745ea240f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eaa3c9aa758d81bbb6051837b083195073d8641f8cdd7f85373c9b05f048726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46fb9bf72ca113b8f996bd73cbc0059e6ca9c6bba7fb1a50915390ef88fe896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae06a2128cfd7dc64cbf85aea0beb8545fdfad115d96e1ad6650266b711ed8b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsElb]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsElb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsElb]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0183c4d7d2ff4cb238a1f572d5e79aadcf87fd2f8d2bc990a3db357acce6d2f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEmr",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsEmr:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26424bc22971717dd05375c498d7154172ef8af8956ed4347d56c5fc88f96173)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags and the extended inventory should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsEmr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsEmrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsEmrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98ecb2084e37056ef2a9e636b08581101d2fcc569251282425077868da06b727)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ffd7840ccbbe14c7361193ca4eef19b80b15709cda70dc2d63d4f6f8f50443e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81dc3b402d8dee82d9bcee8a29d57794dcc754389be2797d7b306f9bee07ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87d1ed6f2c4bbb860b0fe1e87358517f7b617b05b5dd593d135b5268cb40fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060759d3e500820bb87484ba7179952be74065ddd6bee5136e2cea16f64a7068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1f40cf13861dd22b8b31d463052c5a5071215c6b441983627e85cb43bc1919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsEmr]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsEmr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsEmr]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c25496e28caf4731da733215eda27ca0b7448e7eba45e56e5c9c5cdcbb32a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsHealth",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudAwsIntegrationsHealth:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c219d859d9fa6c3f00149ad1692a19b0b2ab9eec6f51eacdd9731529b70b36)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsHealth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsHealthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsHealthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f86711bd01ca429e5db58f084e73315a1b7be773c21e46bb74a94ed2a1845097)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2e7878d24eba1730c9b8637f82d3912d9cab70e21be12e9c6003a465cd62f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsHealth]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsHealth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsHealth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24de463ea31715daafca9d6f499d395e152ac71f03aea5f4055fc70ff230ee33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsIam",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsIam:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddd5b2e484f42f6a258f352d60e9c154ddecad6865b19d33507415e7615f3aa)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsIam(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsIamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsIamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__975af37a114bab9caf68b37237f818cd58b2038586da80bee38aa76d1a23f5e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2022803284284011eea6b96b3851fcd5e214cd91decc5e1ea2c8bb981e5394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d4edd11da59bab88501a1108fec16dfcf1b2fd70e2f2453fa204c8e4510f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a6826a1a1d121276a53c7e1a9033bdb3ac4b8598c74b560e27665552f8cbf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsIam]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsIam], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsIam]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a1e3879db7bd116fec0510ab0155fade4c87d9538232861f78a757e59985986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsIot",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsIot:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e422a5bafafa06f150ece395f191b38536bad3a325ba06e69ef2172248cf18)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsIot(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsIotOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsIotOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b975bd5ee64a3398f35f93dda18d97926846853e9117a546746369c0e2dee5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d7b00aae200011394b3a781e56a9e5c36ee44625b1c9f490a1b6dda7ddec6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638664ab206dd8a34e714ea341a9452ca69f8e6e2cb01ef5fd223f1d79d75b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsIot]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsIot], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsIot]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238a3bd0007e0b65b928487ed913e9466ebfcb425ababa5f2e9f00dfa806cd78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsKinesis",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_shards": "fetchShards",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsKinesis:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_shards: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_shards: Specify if Shards should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_shards CloudAwsIntegrations#fetch_shards}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02b7ae6ba6effe218d73983d6bbbf1499f4a53b761609aaaf14c2a192347ddc)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_shards", value=fetch_shards, expected_type=type_hints["fetch_shards"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_shards is not None:
            self._values["fetch_shards"] = fetch_shards
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_shards(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if Shards should be monitored.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_shards CloudAwsIntegrations#fetch_shards}
        '''
        result = self._values.get("fetch_shards")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags and the extended inventory should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsKinesis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsKinesisFirehose",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsKinesisFirehose:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4899ace1e2f15c8d36df53aaf02c5d848c6f4f665ca6bd9f9291be2b72307e8)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsKinesisFirehose(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsKinesisFirehoseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsKinesisFirehoseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__567c934e4890cf64113f332cf8f5342f2afbc4d1fb09df722122c4877d894423)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf56f83953c751aec57b8b9abe86565aac99c6268dd780028cd9b12da77dead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa20b97c7d6d7d4c339494f3a9d366e1c277b99df5a84a325b0dc0fcb1f95a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsKinesisFirehose]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsKinesisFirehose], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsKinesisFirehose],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61559454c09978765371771b1fd1ab2290086f29a9fd5f3bb97b16d8c30566b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudAwsIntegrationsKinesisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsKinesisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ed4ccaa26a04852d9fd0956491b1c64fa39d680202a5a48b521bdbc8098bfeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchShards")
    def reset_fetch_shards(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchShards", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchShardsInput")
    def fetch_shards_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchShardsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd92d157459e4939262ea4eef0128a6a45609be2cc36da168273a1f0a2599d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchShards")
    def fetch_shards(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchShards"))

    @fetch_shards.setter
    def fetch_shards(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acac1dbe8d77913ed3dafa701d5c111cf1a1ecb545cdc6974784732fb1804920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchShards", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12742bb43ca145ef11839ff33e40ad14ebd9b1e18881ed256af5019810e6e2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01be2a0db3ea93319ec480199be0e36353acedb9e7a4f58352349b9ca7d789e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca50e97fa059f69150815ec8554a6f7f4f0d8c8fc70f0f178421f8cd052f6a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb8ddaf3b2d51b928c21dae0e823ca3c59a290af1b1c15155314841c6962f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsKinesis]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsKinesis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsKinesis],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__557e49ef7aafa388d0df54a88624f7e4545513b0b471a78afefd15ec28f5c852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsLambda",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsLambda:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fba1fd24d6485c6c8669f4032c7de0e5dc1ffd3075fb6700e0e54d2d733054)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags and the extended inventory should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2ed4d124d33d1ede24dd3d816514f5d3518fe50463134e643c4f465da4acefc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9eb86ad5628bf8d0874822e3cd6f73902e2240255f276237aef59c39c965a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190a5d35532ff0378c13a9dad64441953d7748f65862a8dc9b9c6b394de3abba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b954e7c3ab2bdbb9f0fdcb637b515eb84bdbf11abe7112c0a8c2a6707a23f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd67422d83ee5dc793c39329e97ba424d1069f1aab368b0b3a54f14241a2721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58410683cb48c383f855b2d0a3d9d1fa6c7f7061e8c796b16e6bff5f85ed089e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsLambda]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e07dcdd6995ab0bdccd67889f84d2fde3d326aa2eb69374e879cdd368977a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsRds",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsRds:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_tags: Specify if tags and the extended inventory should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ef19ee1e94be8c030bd83921992a50012ed15c64f72f499c43c3548a3bb2cb)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags and the extended inventory should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsRds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsRdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsRdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d813f5dcfa34c8661e768bce268dba574e35a8f967824c890a7d651403f5c40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49716e4525aee23aed0f5eb394164ceda817c695a0353b3f96bfca8cf8b9d290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1906b6693db813cbb489fbadf53a0945a2607714764a35db4b3785c139bc4168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad99a2aed013fa8bfdcdf74614bc5f4c49bb7f0aaf741d71a2ac62a061edf1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75aaf9f5873b62aad30175bac772f1d58a46011f2e9de335b4738c2474755d2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87229a59051b84c9d20eef39261b5aac6fa86e3b6e747effd5d510115ab222ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsRds]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsRds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsRds]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9779cc6678a175b67f95fc604708e546c1364644f89021b3da1bf6cbe7b26265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsRedshift",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsRedshift:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb9070ec2cc7313454135aa1f8ec3cf5a87c394b68065dbf5fd48c24b3d28bd)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6b9e86f7a3694b922b37b54da7da2bce3ccb49106cd9cc71debda1866d6c7c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e202bd2b41551e861d3ac4ff6d65f9a1f5635b05a3e6dddf3b883d8f97433c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc9ac273ecefd2d5cefb10cba10ab80cb279c5cd28b3e85f1f0f40c08b06a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2585a70b4720da2f0ca24c6898f3e6300a3e32a37a39350719c99fe52222379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac02361522846cbb12a65eb96b317096693941efb1a0227fd7a6b037f057967f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsRedshift]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsRedshift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsRedshift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fe674c3feffb17fa94e644af690b2b46e4a587f070654bd9df5ef742b3de57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsRoute53",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_extended_inventory": "fetchExtendedInventory",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsRoute53:
    def __init__(
        self,
        *,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a20df314f69caa152daeaaf9e1a79af6c02eb767f1c2a074b312a9abf0d8614)
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsRoute53(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsRoute53OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsRoute53OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__582cb9615aef9256e0cb8a64f1e3a05a3d279bf27c10c89c7c3165824bf70e15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8298eb105a1aa7686e524467104aa217a512a4ff838edda1ad718f95e2bc5df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907aaac838f438ff2f0bd7b05b81e09bcde13205f265a75df4b622fbaaac5e05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsRoute53]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsRoute53], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsRoute53],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7942a524b027d2a916c59459d0b75e534d75383070c2c2eebeb5360873dda36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsS3",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_extended_inventory": "fetchExtendedInventory",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsS3:
    def __init__(
        self,
        *,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ab9b96b00818e6013fe2103e98626b3ebfb0e15dda0b7f25488ae4ca0a47e8)
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9e785c94925ae01e650b7ed9f3f0da5e0411ad1fc02448a3cc694243e0db6dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5d5070716ec7a9d7a7071ca97c377020954879feea0af0375d8219a691771cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__112668b464fb2439d9a502835f3f499c65e2e47667bdb66bbe1ed47e850aac1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6039bca92dc66d6f16736123bcf25b9ff1cdd5a6c24ea16785e120d7afc838d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4920669dd0f46f8cea694a877d684f673679b85d71afb15f111b4adbeadffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d80585b215775cad0e9a2ab99cc85bfb96a397ae1c1c2f67522c88666f5de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsS3]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsS3]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__683ccb60ceff40081ecf5543bc48e2f1fe43c3201e15763be3993daa3aa831cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsSes",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsSes:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8446d723a2e6fb35098bcc49ad88c7494fe6212adf9ae9016a6102d7d8b4f74f)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsSes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsSesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsSesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__162538ca923fd38f4e1f2a10bd365045e325767656835e3dfac92c265a5c4342)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6d49c6981a736f07ee60fb99fce538a337ae74c6ce8c12bc4db411e3a17518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb70314f3e76b5a965216f95665cecd39d55e65bfc29aa41f576224f05379b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsSes]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsSes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsSes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff3890c76b22def229164440f3a955a2c10de38c443fd60a46f5d925fade923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsSns",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsSns:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ba4c3bcc7ec9bee1908f2e1b40b72d011c01b2a0a8bdfa635d54e0c6471ae0)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsSns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsSnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsSnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd3b1801b8139fa0f8353d82d6752e173d8436180b8543875d793457a443a36c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab287791e88ede87e0c3b800bd1a28da1588c7fac7f89f9e000c782cae2b9b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9852e5a73b67961581aa6c4a75b0c28257e73a5e3f536717471f973b7b836488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0b495c4e73eab14489b2fffe4f1c9c513e0f3c5af48ce612cad9162175319a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsSns]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsSns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsSns]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b574dfde649bcffb8d5240d25810f8bc0ec8008250082a1c7d08b4c3cda82832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsSqs",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "queue_prefixes": "queuePrefixes",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsSqs:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        queue_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param queue_prefixes: Specify each name or prefix for the Queues that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#queue_prefixes CloudAwsIntegrations#queue_prefixes}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff0fdb38a11ddff4ce2122194281474d0b4eb857f20967f959c0b6ff482274d2)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_extended_inventory", value=fetch_extended_inventory, expected_type=type_hints["fetch_extended_inventory"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument queue_prefixes", value=queue_prefixes, expected_type=type_hints["queue_prefixes"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_extended_inventory is not None:
            self._values["fetch_extended_inventory"] = fetch_extended_inventory
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if queue_prefixes is not None:
            self._values["queue_prefixes"] = queue_prefixes
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_extended_inventory CloudAwsIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_tags CloudAwsIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each name or prefix for the Queues that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#queue_prefixes CloudAwsIntegrations#queue_prefixes}
        '''
        result = self._values.get("queue_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsSqs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsSqsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsSqsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50c82c17993cd532f044fa9bbb76080639102a1097dd3bbd258b6a057e578a21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchExtendedInventory")
    def reset_fetch_extended_inventory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchExtendedInventory", []))

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetQueuePrefixes")
    def reset_queue_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueuePrefixes", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventoryInput")
    def fetch_extended_inventory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchExtendedInventoryInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="queuePrefixesInput")
    def queue_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queuePrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0219280ccbb7365033672650f0457d19210eec5eb655bc3d0e7d22327b3ff7c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchExtendedInventory")
    def fetch_extended_inventory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchExtendedInventory"))

    @fetch_extended_inventory.setter
    def fetch_extended_inventory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9eb6b104fa1f8dfc59ea1bc3b7db356606c2c4cba4ff623b18a868fd653197)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a8db6cb6573eae10a24accf4282134c50441a61865fed1f40eb25a7548ee70f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f811bea2416e9ddc5496c341d349847fef56cf5073d15b0acb04b3bd5f512d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queuePrefixes")
    def queue_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queuePrefixes"))

    @queue_prefixes.setter
    def queue_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012ec307c9820febb8e3c2880f114b2fe239b4f9ad935334baf578c9dc5dc3ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queuePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1303753e6b8fc4ca48d1c07abb7cbc0e77ff84cacf809634f6d69c038a004983)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5513d7d34b1d0443eabe5a593433bec77bf17b074d5dafc6871bfedb766913c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsSqs]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsSqs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsSqs]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1dba19905ae3a482b0cf802cca6aaa7cdd3ef5f4ed826c6e6fc4fcb3d9bc2e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsTrustedAdvisor",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudAwsIntegrationsTrustedAdvisor:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668858f73919a08f504c8a90bb65ffb65bc1d01d05572ddba939811087652a14)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsTrustedAdvisor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsTrustedAdvisorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsTrustedAdvisorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a147261cc3bf496a0e170a5e441607f620af5f12ed60056d946be7f8b8c0f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4f346a457cb1508ddb025b8d144de7b4840241fc61fa8191b69cf6be3c6e85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsTrustedAdvisor]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsTrustedAdvisor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsIntegrationsTrustedAdvisor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4bc63cefa256d5b5346d16c3750a584927d393bdf9459dbab1f2801aa2c8f36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsVpc",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_nat_gateway": "fetchNatGateway",
        "fetch_vpn": "fetchVpn",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsIntegrationsVpc:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_nat_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_vpn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param fetch_nat_gateway: Specify if NAT gateway should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_nat_gateway CloudAwsIntegrations#fetch_nat_gateway}
        :param fetch_vpn: Specify if VPN should be monitored. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_vpn CloudAwsIntegrations#fetch_vpn}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a05e1712a6079eebfb1cebb9021117640ecdb1735fc94235af901ee1bb64db)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_nat_gateway", value=fetch_nat_gateway, expected_type=type_hints["fetch_nat_gateway"])
            check_type(argname="argument fetch_vpn", value=fetch_vpn, expected_type=type_hints["fetch_vpn"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if fetch_nat_gateway is not None:
            self._values["fetch_nat_gateway"] = fetch_nat_gateway
        if fetch_vpn is not None:
            self._values["fetch_vpn"] = fetch_vpn
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_value is not None:
            self._values["tag_value"] = tag_value

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_nat_gateway(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if NAT gateway should be monitored.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_nat_gateway CloudAwsIntegrations#fetch_nat_gateway}
        '''
        result = self._values.get("fetch_nat_gateway")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_vpn(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if VPN should be monitored.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#fetch_vpn CloudAwsIntegrations#fetch_vpn}
        '''
        result = self._values.get("fetch_vpn")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_key CloudAwsIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#tag_value CloudAwsIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsVpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsVpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc03184763dca962a4a8ab314c5c148983b1f331637301224bdc278d238f3491)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetFetchNatGateway")
    def reset_fetch_nat_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchNatGateway", []))

    @jsii.member(jsii_name="resetFetchVpn")
    def reset_fetch_vpn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchVpn", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @jsii.member(jsii_name="resetTagKey")
    def reset_tag_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagKey", []))

    @jsii.member(jsii_name="resetTagValue")
    def reset_tag_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagValue", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchNatGatewayInput")
    def fetch_nat_gateway_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchNatGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchVpnInput")
    def fetch_vpn_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchVpnInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagValueInput")
    def tag_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagValueInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__555e7d85f2e58ac7b541bacd19f13077a47af6954e80f4b40ac339755b9b7896)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchNatGateway")
    def fetch_nat_gateway(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchNatGateway"))

    @fetch_nat_gateway.setter
    def fetch_nat_gateway(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b2657609fdf500a4e737b95dd4cc4b3d5550f0c3ef0c867e038437ea0e58637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchNatGateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fetchVpn")
    def fetch_vpn(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchVpn"))

    @fetch_vpn.setter
    def fetch_vpn(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da72c88928d008dd41e6355c8234df0e259a01b0abb531818bb0b36c7caf2c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchVpn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9579bf68121b247cafa084f153862e870a9191414d93835d82fabaa96a992f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac7fa1649a4d226ab4fb2c00a338e4d9911e66ca678b5bcc71bd5245e0bb120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ea2f558eb8f44587d62e70414f9e1cafca3e2ec1df4590a34f1a3d47499183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsVpc]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsVpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsVpc]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ac68e78d33565f199421a44fdec8c9985ca38d90c14b0a0d05bbf25fe5b8d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsXRay",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsIntegrationsXRay:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df10b2612d85d90190d8350575e635e7b3cef8ab626c415ebe5664e6ba53fa3)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def aws_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#aws_regions CloudAwsIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_integrations#metrics_polling_interval CloudAwsIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsIntegrationsXRay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsIntegrationsXRayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsIntegrations.CloudAwsIntegrationsXRayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a6346257c8ea2f1ec9b3140050ddcbf2de3e49b2b5a0d947981b6092478178a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="awsRegionsInput")
    def aws_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "awsRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="awsRegions")
    def aws_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79083a4b7f98cacdf2df9c5b1d5b897d17ff97f9019b6f6c3ae30bb3bebc0d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4546e51c704af084ceb7556b0b73a76c7e2723052e3525aec1976082b7e3d1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsIntegrationsXRay]:
        return typing.cast(typing.Optional[CloudAwsIntegrationsXRay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudAwsIntegrationsXRay]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89f8a3bae21c57127494ed28f6b8aaadeb03b9affab91c6a763edc84787e128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudAwsIntegrations",
    "CloudAwsIntegrationsAlb",
    "CloudAwsIntegrationsAlbOutputReference",
    "CloudAwsIntegrationsApiGateway",
    "CloudAwsIntegrationsApiGatewayOutputReference",
    "CloudAwsIntegrationsAutoScaling",
    "CloudAwsIntegrationsAutoScalingOutputReference",
    "CloudAwsIntegrationsAwsAppSync",
    "CloudAwsIntegrationsAwsAppSyncOutputReference",
    "CloudAwsIntegrationsAwsAthena",
    "CloudAwsIntegrationsAwsAthenaOutputReference",
    "CloudAwsIntegrationsAwsAutoDiscovery",
    "CloudAwsIntegrationsAwsAutoDiscoveryOutputReference",
    "CloudAwsIntegrationsAwsCognito",
    "CloudAwsIntegrationsAwsCognitoOutputReference",
    "CloudAwsIntegrationsAwsConnect",
    "CloudAwsIntegrationsAwsConnectOutputReference",
    "CloudAwsIntegrationsAwsDirectConnect",
    "CloudAwsIntegrationsAwsDirectConnectOutputReference",
    "CloudAwsIntegrationsAwsFsx",
    "CloudAwsIntegrationsAwsFsxOutputReference",
    "CloudAwsIntegrationsAwsGlue",
    "CloudAwsIntegrationsAwsGlueOutputReference",
    "CloudAwsIntegrationsAwsKinesisAnalytics",
    "CloudAwsIntegrationsAwsKinesisAnalyticsOutputReference",
    "CloudAwsIntegrationsAwsMediaConvert",
    "CloudAwsIntegrationsAwsMediaConvertOutputReference",
    "CloudAwsIntegrationsAwsMediaPackageVod",
    "CloudAwsIntegrationsAwsMediaPackageVodOutputReference",
    "CloudAwsIntegrationsAwsMq",
    "CloudAwsIntegrationsAwsMqOutputReference",
    "CloudAwsIntegrationsAwsMsk",
    "CloudAwsIntegrationsAwsMskOutputReference",
    "CloudAwsIntegrationsAwsNeptune",
    "CloudAwsIntegrationsAwsNeptuneOutputReference",
    "CloudAwsIntegrationsAwsQldb",
    "CloudAwsIntegrationsAwsQldbOutputReference",
    "CloudAwsIntegrationsAwsRoute53Resolver",
    "CloudAwsIntegrationsAwsRoute53ResolverOutputReference",
    "CloudAwsIntegrationsAwsStates",
    "CloudAwsIntegrationsAwsStatesOutputReference",
    "CloudAwsIntegrationsAwsTransitGateway",
    "CloudAwsIntegrationsAwsTransitGatewayOutputReference",
    "CloudAwsIntegrationsAwsWaf",
    "CloudAwsIntegrationsAwsWafOutputReference",
    "CloudAwsIntegrationsAwsWafv2",
    "CloudAwsIntegrationsAwsWafv2OutputReference",
    "CloudAwsIntegrationsBilling",
    "CloudAwsIntegrationsBillingOutputReference",
    "CloudAwsIntegrationsCloudfront",
    "CloudAwsIntegrationsCloudfrontOutputReference",
    "CloudAwsIntegrationsCloudtrail",
    "CloudAwsIntegrationsCloudtrailOutputReference",
    "CloudAwsIntegrationsConfig",
    "CloudAwsIntegrationsDocDb",
    "CloudAwsIntegrationsDocDbOutputReference",
    "CloudAwsIntegrationsDynamodb",
    "CloudAwsIntegrationsDynamodbOutputReference",
    "CloudAwsIntegrationsEbs",
    "CloudAwsIntegrationsEbsOutputReference",
    "CloudAwsIntegrationsEc2",
    "CloudAwsIntegrationsEc2OutputReference",
    "CloudAwsIntegrationsEcs",
    "CloudAwsIntegrationsEcsOutputReference",
    "CloudAwsIntegrationsEfs",
    "CloudAwsIntegrationsEfsOutputReference",
    "CloudAwsIntegrationsElasticache",
    "CloudAwsIntegrationsElasticacheOutputReference",
    "CloudAwsIntegrationsElasticbeanstalk",
    "CloudAwsIntegrationsElasticbeanstalkOutputReference",
    "CloudAwsIntegrationsElasticsearch",
    "CloudAwsIntegrationsElasticsearchOutputReference",
    "CloudAwsIntegrationsElb",
    "CloudAwsIntegrationsElbOutputReference",
    "CloudAwsIntegrationsEmr",
    "CloudAwsIntegrationsEmrOutputReference",
    "CloudAwsIntegrationsHealth",
    "CloudAwsIntegrationsHealthOutputReference",
    "CloudAwsIntegrationsIam",
    "CloudAwsIntegrationsIamOutputReference",
    "CloudAwsIntegrationsIot",
    "CloudAwsIntegrationsIotOutputReference",
    "CloudAwsIntegrationsKinesis",
    "CloudAwsIntegrationsKinesisFirehose",
    "CloudAwsIntegrationsKinesisFirehoseOutputReference",
    "CloudAwsIntegrationsKinesisOutputReference",
    "CloudAwsIntegrationsLambda",
    "CloudAwsIntegrationsLambdaOutputReference",
    "CloudAwsIntegrationsRds",
    "CloudAwsIntegrationsRdsOutputReference",
    "CloudAwsIntegrationsRedshift",
    "CloudAwsIntegrationsRedshiftOutputReference",
    "CloudAwsIntegrationsRoute53",
    "CloudAwsIntegrationsRoute53OutputReference",
    "CloudAwsIntegrationsS3",
    "CloudAwsIntegrationsS3OutputReference",
    "CloudAwsIntegrationsSes",
    "CloudAwsIntegrationsSesOutputReference",
    "CloudAwsIntegrationsSns",
    "CloudAwsIntegrationsSnsOutputReference",
    "CloudAwsIntegrationsSqs",
    "CloudAwsIntegrationsSqsOutputReference",
    "CloudAwsIntegrationsTrustedAdvisor",
    "CloudAwsIntegrationsTrustedAdvisorOutputReference",
    "CloudAwsIntegrationsVpc",
    "CloudAwsIntegrationsVpcOutputReference",
    "CloudAwsIntegrationsXRay",
    "CloudAwsIntegrationsXRayOutputReference",
]

publication.publish()

def _typecheckingstub__218636da2f5c84b07b8f11f887c728956d546cee837b90d553762da5832a9fd8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    alb: typing.Optional[typing.Union[CloudAwsIntegrationsAlb, typing.Dict[builtins.str, typing.Any]]] = None,
    api_gateway: typing.Optional[typing.Union[CloudAwsIntegrationsApiGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scaling: typing.Optional[typing.Union[CloudAwsIntegrationsAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_app_sync: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAppSync, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_athena: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAthena, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_auto_discovery: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAutoDiscovery, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_cognito: typing.Optional[typing.Union[CloudAwsIntegrationsAwsCognito, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_connect: typing.Optional[typing.Union[CloudAwsIntegrationsAwsConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_direct_connect: typing.Optional[typing.Union[CloudAwsIntegrationsAwsDirectConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_fsx: typing.Optional[typing.Union[CloudAwsIntegrationsAwsFsx, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_glue: typing.Optional[typing.Union[CloudAwsIntegrationsAwsGlue, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_kinesis_analytics: typing.Optional[typing.Union[CloudAwsIntegrationsAwsKinesisAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_media_convert: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMediaConvert, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_media_package_vod: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMediaPackageVod, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_mq: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMq, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_msk: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMsk, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_neptune: typing.Optional[typing.Union[CloudAwsIntegrationsAwsNeptune, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_qldb: typing.Optional[typing.Union[CloudAwsIntegrationsAwsQldb, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_route53_resolver: typing.Optional[typing.Union[CloudAwsIntegrationsAwsRoute53Resolver, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_states: typing.Optional[typing.Union[CloudAwsIntegrationsAwsStates, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_transit_gateway: typing.Optional[typing.Union[CloudAwsIntegrationsAwsTransitGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_waf: typing.Optional[typing.Union[CloudAwsIntegrationsAwsWaf, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_wafv2: typing.Optional[typing.Union[CloudAwsIntegrationsAwsWafv2, typing.Dict[builtins.str, typing.Any]]] = None,
    billing: typing.Optional[typing.Union[CloudAwsIntegrationsBilling, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudfront: typing.Optional[typing.Union[CloudAwsIntegrationsCloudfront, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudtrail: typing.Optional[typing.Union[CloudAwsIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
    doc_db: typing.Optional[typing.Union[CloudAwsIntegrationsDocDb, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamodb: typing.Optional[typing.Union[CloudAwsIntegrationsDynamodb, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs: typing.Optional[typing.Union[CloudAwsIntegrationsEbs, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2: typing.Optional[typing.Union[CloudAwsIntegrationsEc2, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs: typing.Optional[typing.Union[CloudAwsIntegrationsEcs, typing.Dict[builtins.str, typing.Any]]] = None,
    efs: typing.Optional[typing.Union[CloudAwsIntegrationsEfs, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticache: typing.Optional[typing.Union[CloudAwsIntegrationsElasticache, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticbeanstalk: typing.Optional[typing.Union[CloudAwsIntegrationsElasticbeanstalk, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticsearch: typing.Optional[typing.Union[CloudAwsIntegrationsElasticsearch, typing.Dict[builtins.str, typing.Any]]] = None,
    elb: typing.Optional[typing.Union[CloudAwsIntegrationsElb, typing.Dict[builtins.str, typing.Any]]] = None,
    emr: typing.Optional[typing.Union[CloudAwsIntegrationsEmr, typing.Dict[builtins.str, typing.Any]]] = None,
    health: typing.Optional[typing.Union[CloudAwsIntegrationsHealth, typing.Dict[builtins.str, typing.Any]]] = None,
    iam: typing.Optional[typing.Union[CloudAwsIntegrationsIam, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    iot: typing.Optional[typing.Union[CloudAwsIntegrationsIot, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis: typing.Optional[typing.Union[CloudAwsIntegrationsKinesis, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_firehose: typing.Optional[typing.Union[CloudAwsIntegrationsKinesisFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_: typing.Optional[typing.Union[CloudAwsIntegrationsLambda, typing.Dict[builtins.str, typing.Any]]] = None,
    rds: typing.Optional[typing.Union[CloudAwsIntegrationsRds, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[CloudAwsIntegrationsRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    route53: typing.Optional[typing.Union[CloudAwsIntegrationsRoute53, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[CloudAwsIntegrationsS3, typing.Dict[builtins.str, typing.Any]]] = None,
    ses: typing.Optional[typing.Union[CloudAwsIntegrationsSes, typing.Dict[builtins.str, typing.Any]]] = None,
    sns: typing.Optional[typing.Union[CloudAwsIntegrationsSns, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs: typing.Optional[typing.Union[CloudAwsIntegrationsSqs, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_advisor: typing.Optional[typing.Union[CloudAwsIntegrationsTrustedAdvisor, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[typing.Union[CloudAwsIntegrationsVpc, typing.Dict[builtins.str, typing.Any]]] = None,
    x_ray: typing.Optional[typing.Union[CloudAwsIntegrationsXRay, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4c748f9b66efa26a1d6b8f71f9197de4e1828f69db8b7c07ee5aa6a94f2a0e77(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5219cec395e62e4e80020a1434f822e106636205b1c60eb208915ae3fb2ebcc2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bc997685d6f8091c1aeb3bc838d3517467f180193964c59a5ff4dec857a6d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947ffbc6d56f727b440fd8f8118b85c3b51c796e2061df9d54dc4f7e8a8ac873(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e40c59dd4d07db8036db912b3d55367876e9d77f5205cf22f9f483431901d19(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    load_balancer_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572217df744846f2766d2affe294d69726b61e9680270a7bd923e0111b104af3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9706cd7ff89e53664ab1cfd3c3035cda1a0cc1be501a30f0e5746e2d3e7e2e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b3ce8feaeaf2af84265f7259427c238e3cfbc42f4c9461ffded1079005d95c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe6f052ff4d591211660ad507830c4891a9367c1347f6cc8366c041461ed5ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff379d8c86d86ed60ea79ebb3c74b0994dd7ad6522c150d4ef706818a5ab0df(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e3734ab02a24e893e41f78ff92468a606167dbc8be3283b85012bd7b191f99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ed7ae7c08e77ed7e50f49e4c5c6888c8927d4b0a8ccb50aaca10edebdc4867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767b2668e3f3efc893160d37ed3ccd4a4903950da2102758a3ecd77ffc8bde44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecba4987951050f636453107e5a4b0740c989f21f1391c41ed3a15bc4b2e080(
    value: typing.Optional[CloudAwsIntegrationsAlb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c455c691d322c0e9b961d79d5bde588c516e04970357f51f4751bf5c9ca651(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    stage_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0794f271d38a04aa555de1b5ec64fb2d72c06537815188b1ffc3b74b2017ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b07b9ac4b3c1c86fe1fe990ff471e943866bf78f624acacaf9956ea9190927(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e79ee75f76044b8ae48438ec73f10c6e0ad857ed30e8ed7347e647d247a2885(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df396b0c5b30777f8bb53d69cdfc9dd1db0ea822aaad2bb7f6579b47c47c97da(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2f50b2e93d3ce05e2b3e16b68de6ce8a31bb57531f62cbec8b253c53036527(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520d3a4fe43e7a445173c8f404fe784d1f92ba90fb3425a01e48013b1061ad26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53085079a55deb7ff8923b44e6ad6676461678ad21ab2c684a7df120f716881(
    value: typing.Optional[CloudAwsIntegrationsApiGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1a637079b6721ef1936e2e172260f07f1596ffa6ce5b0859040f8ee31604d3(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492d1f319956f75f675cf675053fd025d349bbe0b2f861cdb21a76b8b9e78b91(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f8bc1aa7ae647c694a1b75d3d84458de85506dff10366afee1adae3bccd62c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b792f26dc3907e199974d6a32f887bb94d57eb57ac2c2d1f827e677efb439cbd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7c50d259f2a569292112597fd78316ca372be95904b02ac682fd5cceb0cc5a(
    value: typing.Optional[CloudAwsIntegrationsAutoScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb27c211c2553d9a3ac20e3e8ec713612f8887916f61164f4ba610706ce5dbe(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1732a8916426229bff1f258e1e0fbfb9551d43457e7900815ad67cbf8c935cf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d8eca29f363bbc313a464a8bf96b7e90acc97acac5f970ea1ae98c47a11982(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0990aaa0fc31abe1c9722fc8f90787dbab338f39159db03369c844db077ca4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65da110080261e9965faa937acfeea8959eb5723430ddd78f97fbe5f9fedd3ce(
    value: typing.Optional[CloudAwsIntegrationsAwsAppSync],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6d4a1c59279a1b5b4d108de10deb8322e29b7c26b6647a0b9f8abd0e9ab2da(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a18b1f9bde7a5f8e4e5c85d35cdb72852d1ba915a27d65f1cdefce2e653d21c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1123ec36abb5a0ec0eeb13c02226108192b20c1c8835e822d9b1e2d37bd0c67f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a29993735352695316ee5dc5d3d302b286552c3017ab6912fd42790badc43b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa9c8cd8ab12498062d6f65aca27198e443a2d07624451850b73388e451c720(
    value: typing.Optional[CloudAwsIntegrationsAwsAthena],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2696be9c1d02d3937eea9c46e9e600bd5fa5943114bc0466cd8cbbbff37e6d7a(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82a6a1c1566d58f509511ba01e2a74047aa63bfa567f8e1c30f072083f502f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48af961ff5adca680177384658fa500ec6c61ac3abde2a1436118e58b6fc4bb6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ef994b8c3bc9882b5a1a3502578614783166ad71401529859bab5aa1fa21d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12111b8516b2c9db5715d10c2bf508410fded980890b0e34105b29a159c0ea7(
    value: typing.Optional[CloudAwsIntegrationsAwsAutoDiscovery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979a8717df7247972c094e198570b76c0254c4c58f9a386dc643ed39180b3f55(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5af7b76d436e5475bd65f3d69efe50a2c796953a6b6fea6c1fb6a217d7fa882(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876abea8542cd18043634adb5243217e00b06937cc0d36feb9860f0a5c094535(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e057352b0abd3f42323ec536db2de4e697c734502a5a764a3ca91d3c72022aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147e934fc44d3874acf250647d9d5452681a389af25271c4bb0d7fdbee12abe2(
    value: typing.Optional[CloudAwsIntegrationsAwsCognito],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56418f9ce152dc44aaafd1c86907ac25ed16ce9e2b1af0e7aa4ff2b9ae0ad461(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e95f82b6a8032ffd4ce668bf74d0f930ab97e94db5d61118551692b1821b11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811019247b441fa37f3114612ff411542ea28e5ca9eb8abcf855edfb24893241(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70607156bf068687595e89c93a129d0180b2621363451b7ef3d9398a43e0f8b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429cabf9d7bc9bbc306dba7a297f0da310c52e115ff57dbfb8dc1243f62d13c4(
    value: typing.Optional[CloudAwsIntegrationsAwsConnect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb9a828a1b41fc81696e6197a0e9f57784438b53b7fbbca98e825c9e881814c(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b26c7d199640199b08ac7444e459222e1018629846ed750b38efd053816aa1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd6d86bf944bdfdf1c78bb03ac45a047292ac29ff698a125bcb02d2c9bbe7cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2efed19c1353098726510c48d3e02da2bf407f124af77475dbcec60c7a22c2f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04033f504cd978f051b4328e6a4f723239bb791237f9682cce0416aebdc4e1a5(
    value: typing.Optional[CloudAwsIntegrationsAwsDirectConnect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd4834378e05043d61d8c41067b08f3a3f361dc6810f60afd63d529c07d5df0(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222209fdfbdad356c50e8013e190aef00e6ef4c39b648b826d384e636cffebb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2657143f79e2d78e94c658d14e0bc3216a9954a3d51f9826bc1317a85e4263d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6f896545fa35a91199254e2690d4bc3be4b83626340921d0d25fb5ee699d6e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079d3b1543ee28287c873d94e6d45dc9aaf619f2a6fac2a424494379dc645ab9(
    value: typing.Optional[CloudAwsIntegrationsAwsFsx],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13be6d1e289887a9278c10174d6446805dc6eeabd824fb8860f8b1a69f32c647(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22384cd45e950c0be0beecf4d8f11ea18093dd317b55921dbf6a78b79aed3789(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e8a1a1fe69cc1c0f4ff619415ef15eeb6ad829b164ecb681e2023e630ec659a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21b3d806045359287c61d4dee5fc3cbc7c3821fe6f7a1cd70cb9733924062f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edba3644a475c9306bca931ac7eb661a197b6bec5017d58fe0632182c935db8(
    value: typing.Optional[CloudAwsIntegrationsAwsGlue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929efc01f0eb14cbb469863a0673f2c86b8996f93f9c174be4e0ee76b81ea554(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b2772ec0e809bf1613d575ca445f201d5622045400617a581f49530e4e2a5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0396e6b059a84d235e4298bd4bb94335d62823d8fc7e43159be80cf70e54f19f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31234072496c501eb0be8cb8dca29b26b94aebb0a02da535a64d8bf3f5d6c2c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6825c259162df555b2a7f4c4124ec2837f2bdabac708db9204d84f2efa50776c(
    value: typing.Optional[CloudAwsIntegrationsAwsKinesisAnalytics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7215dec7cb085c0a02e39a1406839de741fa58a2af9bddc4313ceb049b528cfd(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9985b664e688d2ad517eb682b1a2d3ecd1ad21de651d33145cdb945adbcd80dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41e034de553b9742add856d7242d9a0c05e8727267e4a32bc93ba7e14eab653(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0afb8bbeada0d12306f4e82045aab9ccebd3f98a001c28f3d7b520f11f67a4a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3134fd44a7c90f8daccd0da879765cd1f50a29a1245c78269210b66757dac27a(
    value: typing.Optional[CloudAwsIntegrationsAwsMediaConvert],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56895def110fcf5f07690cddb3bb6220a710c9eae098fc702d32b03587a0f88a(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d6c078300b0f054679e623ebfff563f1bd655b68f7548f9effb98d0bb30577(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf79231cbcd1b3367f31a2f5e85c086a4a7babdba9e91857c850971c85e73b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9ad8b88ef081e20845d475343fe1bc3422db36ddb54a624ff976764698d39e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d191f349a8910587d2080b976ed452fa4469aabeb37676eca5d807badef7739(
    value: typing.Optional[CloudAwsIntegrationsAwsMediaPackageVod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023766cb8a0bf6393fca99b9a6c33a64059f9e044f562bdbb6231fe4bbd18379(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9054c66fa1fd5267fc9ea2d6dd72573f098426719ea3315faadbd2cb45cbf51f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e33551d35dcf5c948db6ce2e8837fc68dd8fea95b21d820a5f1784ff5e5b001(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca395bd03831e1d9a69bbe259352a48569940ddfec703163f3298b0614f6195(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab114092f8588c14a63f489b0f20977085e8656df5e8238aedd79a002aa17a3(
    value: typing.Optional[CloudAwsIntegrationsAwsMq],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a3e4c89d63cfee2a701c7d13eeea996cec77dfa04e231f0ad76f55f15be2a7(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59916632c4947a6e555de0503c4b8aa40fa94b2a38cc178812b1c461bbd047a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03fcf21e4012d08770b4e30824bebc7a492b8fde84a703579b339c8dff622368(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b707de6fec18b038a8c219dc7d605e252c0099a72dbc192512593442c7de3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed742e5fad962b97df17fad73bd8caa0bb2db027489a5c2886d6e117542954e3(
    value: typing.Optional[CloudAwsIntegrationsAwsMsk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d5d6fc2cb030dce0f96498079a27b14770ef125a713605ba769ca9856be22a(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2da33d0297d2ff75c5926660706b29cc8e7e4d9c6b6e1922497ac026dc1f04a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303b13d8461b72e611fefb6ebff644c44dbbb5044c7142f2973cad106197795c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba22c03539ce9b82fec840284339ad6fba81f4d91fd53f07e80ce701bb285e65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05bc0338045b275e428d27902786fd0a6c59bf287c69f09636de85a4ed6f7d62(
    value: typing.Optional[CloudAwsIntegrationsAwsNeptune],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e40ab013e4b71051afa2a6e3a9477fdebf6398813ac7b56556183160ae6f41c(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e0fda50c5558bddbad3f24a710a5cd0c8c7e8e864f254832657015d5ff9df6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45383924abdd9351e051d565811a69f05fc1531182c5c16a6a6daad99dff506(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de9eeeb7c7d98fe164eb4ec11b2847a10519cc6aa734f6f5ca80a92ffadc78c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c33d4d8f497905b7eab0a56376427d79455fbe7d5065dcb55c85a5e5ebe983(
    value: typing.Optional[CloudAwsIntegrationsAwsQldb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d996c041ee32148d6b98aba4921359109f18a55ebc49355547cf1f803fbd62e(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2b194291d9ed0e477679251e878709ac658ca4423d2a599dc8f382dea2f230(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161b9a151142c84126131ab8cfe3376df22cbae9a681d73519b77958ae91edbb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f622b1d4c376052dffa8e2a474b54bf105839c1fd4cee63886b8c267fd9e414(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54429e7fb6b7811156396606fa3b33fa78e43d7bb4d28b59c7fdab57e587cded(
    value: typing.Optional[CloudAwsIntegrationsAwsRoute53Resolver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991333ab1ecdb2219b97dbaca765d788c80e79f1a1245319d452bd2a3dd66405(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__789018829d62b4743b85475385f4f6581462e2c7652f17f1c29100a43c19c294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983a6f406043af64912a5ba05bbd3e0409d9980c36eac69867554850daa4bb85(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8c1665abdd1e1578b96e75870f7566e34cf2429aca335285fdb9b2ab1a1cd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa49c73e7f8a5b126334d7b7f67026a917646f47903416c46388d033780d1238(
    value: typing.Optional[CloudAwsIntegrationsAwsStates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643e89acdb5932bd7d59be268065180494a868d5b53015a8fa3018521a827f8f(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215dd8c1eacc8e547770d87f9703c8c84de18b67fefe39be50ddf909077532cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6d3496ac958c5471ceefab26ecb2891a134ab4ac03209271e8a5059bc0c788(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf6298d5adcbb0cfbf2c03740b22670f1d6da3b661bec9d84364f5e5fbede21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3989a15499f56076f6c81944d4c258a34a79724ca8c56cf1cef0ab9eb6674bff(
    value: typing.Optional[CloudAwsIntegrationsAwsTransitGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f854a435a68b01769b18046a82ee738aeae217f89ecfe5cfe5909a9b8ab4941b(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fa8e423cfcb04bf7b465151857fbaed542fc38da05cb937d97fcfb848db24b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88de4a5e06561acdb23619d393d7582a7775b3ef9efa2eb16d3548bf3f2bbf73(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f39a6895d183ead48f2fce0420a9ead287b1cea09888b913ae0e9c4a205d9bd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd84577c4a9548848eff9e94f9798ae3f88b476d21ff5eca82801c81cfeb8713(
    value: typing.Optional[CloudAwsIntegrationsAwsWaf],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0aa03acb5e2ef6c930e1717137b507913393a6d9225bad081cb7ea06878e999(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1c86b69c91d89215faa65a2c7d66963d1793bfea89fd0c1eb713e7b936426f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fb1314403eddc9d853878d299ec1cb8ae2b598e32d0b6496c073d2804093c3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979e9561f20a5d1da0a87f2073af6a7a8fa8e054e230aa0131d7f6cc4209380a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8112051486758f03735e07486d35dba68ebc2579f90abdc4cb961da1f767cf93(
    value: typing.Optional[CloudAwsIntegrationsAwsWafv2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9ccb32fc89d2507f407cef214d9b76981c4a2617faf94bdbaa95a6ca60f3d7(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62b82999bd05c07ebf66e82fc1cd50209c887f3e8d6dc616b8642f2880f4679(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5dcbb93b5a3ec7ecb2b967fb94b1d9617184e309d8b240bc3497a0639781d84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9b69b3eb4d71e529ac6b4536b8ceaaf0ec2e61eb0d3064868b86777f85484d(
    value: typing.Optional[CloudAwsIntegrationsBilling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2266f63c7b7630abc91377c0b73f98ea11cdfc99572d6efd5d1717467b93268d(
    *,
    fetch_lambdas_at_edge: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132ed19a0f2762a2a6b1cee8263296884e7041980d1dca9a15fc28b94373f34e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce7268e8743febf91ec2c4b5fcca1df4cbe74f6a61c7bd59ca11276a934c88e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1c94f60b7b6df1ef2f1c0585228308b55c572831bb596b27a7cb34e80f8a9b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b86a8e638086bd572176d84fa6b53a13ac9c68ab9a354830d723baaa8b3a913(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bac78be632b9df054c9395ac5b0eb2a280088708e1d302d19fa0a84e85b1113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1c4636ed02d9193a01ed51d804de2b184b4ed807b5ea50e3c04b5580e8a789(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106fd6f9e62b93c8232fd1c042c4db950ff6af06b96d423f9df293d774c8e072(
    value: typing.Optional[CloudAwsIntegrationsCloudfront],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9133ba564bcdd8e4779348d80ab1c85ac796b37f55e670dd76c7e2d6c8aa73fb(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6ddf9f2bfcf0c0e767bae6f5221261f7773891ee8bb2cb0935bb827b27f74a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8e5ffa65cec1a9d99267d29a7d0df8763911839b2c7fc3ec6b822357589d34(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac2025d900c573c9470c10047d81f45e617e5ba44b85dab88d0e5f8141da6b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2520ae8e39751ad9964fa5eb5ebc623daec32d6e9e54c03ba08593b5e99b0f82(
    value: typing.Optional[CloudAwsIntegrationsCloudtrail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3ac5886f8796b4cd2e377d13a118f9277a15b3d6884b09bb067e13e9f18b87(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    alb: typing.Optional[typing.Union[CloudAwsIntegrationsAlb, typing.Dict[builtins.str, typing.Any]]] = None,
    api_gateway: typing.Optional[typing.Union[CloudAwsIntegrationsApiGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scaling: typing.Optional[typing.Union[CloudAwsIntegrationsAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_app_sync: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAppSync, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_athena: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAthena, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_auto_discovery: typing.Optional[typing.Union[CloudAwsIntegrationsAwsAutoDiscovery, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_cognito: typing.Optional[typing.Union[CloudAwsIntegrationsAwsCognito, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_connect: typing.Optional[typing.Union[CloudAwsIntegrationsAwsConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_direct_connect: typing.Optional[typing.Union[CloudAwsIntegrationsAwsDirectConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_fsx: typing.Optional[typing.Union[CloudAwsIntegrationsAwsFsx, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_glue: typing.Optional[typing.Union[CloudAwsIntegrationsAwsGlue, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_kinesis_analytics: typing.Optional[typing.Union[CloudAwsIntegrationsAwsKinesisAnalytics, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_media_convert: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMediaConvert, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_media_package_vod: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMediaPackageVod, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_mq: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMq, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_msk: typing.Optional[typing.Union[CloudAwsIntegrationsAwsMsk, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_neptune: typing.Optional[typing.Union[CloudAwsIntegrationsAwsNeptune, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_qldb: typing.Optional[typing.Union[CloudAwsIntegrationsAwsQldb, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_route53_resolver: typing.Optional[typing.Union[CloudAwsIntegrationsAwsRoute53Resolver, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_states: typing.Optional[typing.Union[CloudAwsIntegrationsAwsStates, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_transit_gateway: typing.Optional[typing.Union[CloudAwsIntegrationsAwsTransitGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_waf: typing.Optional[typing.Union[CloudAwsIntegrationsAwsWaf, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_wafv2: typing.Optional[typing.Union[CloudAwsIntegrationsAwsWafv2, typing.Dict[builtins.str, typing.Any]]] = None,
    billing: typing.Optional[typing.Union[CloudAwsIntegrationsBilling, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudfront: typing.Optional[typing.Union[CloudAwsIntegrationsCloudfront, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudtrail: typing.Optional[typing.Union[CloudAwsIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
    doc_db: typing.Optional[typing.Union[CloudAwsIntegrationsDocDb, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamodb: typing.Optional[typing.Union[CloudAwsIntegrationsDynamodb, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs: typing.Optional[typing.Union[CloudAwsIntegrationsEbs, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2: typing.Optional[typing.Union[CloudAwsIntegrationsEc2, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs: typing.Optional[typing.Union[CloudAwsIntegrationsEcs, typing.Dict[builtins.str, typing.Any]]] = None,
    efs: typing.Optional[typing.Union[CloudAwsIntegrationsEfs, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticache: typing.Optional[typing.Union[CloudAwsIntegrationsElasticache, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticbeanstalk: typing.Optional[typing.Union[CloudAwsIntegrationsElasticbeanstalk, typing.Dict[builtins.str, typing.Any]]] = None,
    elasticsearch: typing.Optional[typing.Union[CloudAwsIntegrationsElasticsearch, typing.Dict[builtins.str, typing.Any]]] = None,
    elb: typing.Optional[typing.Union[CloudAwsIntegrationsElb, typing.Dict[builtins.str, typing.Any]]] = None,
    emr: typing.Optional[typing.Union[CloudAwsIntegrationsEmr, typing.Dict[builtins.str, typing.Any]]] = None,
    health: typing.Optional[typing.Union[CloudAwsIntegrationsHealth, typing.Dict[builtins.str, typing.Any]]] = None,
    iam: typing.Optional[typing.Union[CloudAwsIntegrationsIam, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    iot: typing.Optional[typing.Union[CloudAwsIntegrationsIot, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis: typing.Optional[typing.Union[CloudAwsIntegrationsKinesis, typing.Dict[builtins.str, typing.Any]]] = None,
    kinesis_firehose: typing.Optional[typing.Union[CloudAwsIntegrationsKinesisFirehose, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_: typing.Optional[typing.Union[CloudAwsIntegrationsLambda, typing.Dict[builtins.str, typing.Any]]] = None,
    rds: typing.Optional[typing.Union[CloudAwsIntegrationsRds, typing.Dict[builtins.str, typing.Any]]] = None,
    redshift: typing.Optional[typing.Union[CloudAwsIntegrationsRedshift, typing.Dict[builtins.str, typing.Any]]] = None,
    route53: typing.Optional[typing.Union[CloudAwsIntegrationsRoute53, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[CloudAwsIntegrationsS3, typing.Dict[builtins.str, typing.Any]]] = None,
    ses: typing.Optional[typing.Union[CloudAwsIntegrationsSes, typing.Dict[builtins.str, typing.Any]]] = None,
    sns: typing.Optional[typing.Union[CloudAwsIntegrationsSns, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs: typing.Optional[typing.Union[CloudAwsIntegrationsSqs, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_advisor: typing.Optional[typing.Union[CloudAwsIntegrationsTrustedAdvisor, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[typing.Union[CloudAwsIntegrationsVpc, typing.Dict[builtins.str, typing.Any]]] = None,
    x_ray: typing.Optional[typing.Union[CloudAwsIntegrationsXRay, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b58ef8635db36e48a559b28b40b82ec4dd41bcbf964598d8e8c2610059fab98(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ceccfccb2c01b0f9212f0432a797550e67fbdd0276877c6b924299041c1031(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebc6521dc6dbb79edfa912af0c774c5085a0c22a1fddfcb7136dfa7d1b116b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0251404e38849d33ade8e61fb4a4f375b9f0abdad07106312e45c3d4b21750a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc4f66bc4ff0d503483eee5301c5ff5f022809adb60e47f7984abedc805bb6e(
    value: typing.Optional[CloudAwsIntegrationsDocDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5578f1d84d4136281045d42ad8cd804a13cc5131e1178f2fccd5b32eb19d5c5(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63de01db4ae0b0c1bb57e122b9de70208908339a87fea7db52de6be41399f47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8967537590fd407ef87b17cdb3e8e14573bcc6eb2783e6aeaf26921ad387a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6eef481b4e6030a18404931159f971595bdbc8c35991b41abffa6f42d1de1d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e31eb274e4bee47ad7d113887cdd0dd1949d31f810f808ed9fd4ec41ba112f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4148f25094ab70de41d3490c6f56d99a8a90ce1a2338b03739e4589f51264ba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8896f374709a77e40838e0baf47c1b340d607a26eea31360e4a78f8a025585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214da2ecdf3995075af216f69b0f82ce4e4cfb3ca0c190d27f819d6c091e20ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d074c5d8cf91a2b0c05e3fc8b374afcd939f649d899d2c7eb064d257556d6b5(
    value: typing.Optional[CloudAwsIntegrationsDynamodb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909f355c4271f6dcaecbb07f9ada237cc94ab8c821a91e5bafe9fa11b0eaa605(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2f8518ae0401dc8f55b50b3c4f7351d29e2e022e1474c44c76b6f83aa9f58e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f4efed1910cb6ed6c2b896da5a388a514dc242df2299bec08795f96bdd0486(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36730bf112da13b303a8cd641ce619002c519eb7ac18cb5dd167683f9cdb69c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a615ef6c4966b9a26cc111d73aea7d15f816d304d60e6737c402a3722f5d7e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95154e577bf4ae3b0391027960e94449016f015171fd62ae84f5db2dbe8f54de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bc95bebc9d91ac422ba41d510ba209286dd5faa95a22078d42ec2d106b948d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef261a2f59459427265681ecb47f61448eeba8cef04471586c8e9342b09dab59(
    value: typing.Optional[CloudAwsIntegrationsEbs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f43c746d4c560876d4d23b2e3ac9f26d25f5d2e33dc79ae443a705b90e24b71(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    duplicate_ec2_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d0e44efc7af60ebfa03a5a86beab29b50854db698b9add74de4af7511dc208(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f70e897d6e07ca582f442aa67a4238fc441d7ed6d2101aca280de768d00022(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1319c85e3996edbda499bf468ecf07a57c6ff4faad9c62aa3f872d0cd3e876(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5001c87823109b828438df45d3fbf09c57161ad5dce1335088101874e688d976(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92016a3e32fb89496b7009b1a4164d395271a410864f684d523e7350505b1110(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fcd8bb774b145606b7e8ca4a0cfbfc7f02e1a7d34405156e0d9c4a011c46994(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323a8830d16f0df2a0373e5b3f11abe645251534cc308610384f5658f4422410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e0a2272f9f3d13c8b605d90c2976aa911d6152fa5df7c11ec718c9ee153985(
    value: typing.Optional[CloudAwsIntegrationsEc2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83f796e181d26247d104c9fe70d8764649915e7028d5c62c4a7e5aae71137df(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7f35a8ea2e54751e87118bd9b91f7f50aa5231cb42be6721315b2aeaf0853f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ae09cdaef0014ca4e52a20b13d2ca4130f94eaaf1ef2573f5b17d4fc094966(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe554c4db75816ff439117503f934bf5cffd8179eed2fdc392e5e8e809c7876(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cda46e7545cb6438ad8794452725911a86b109d1c713ad678e1b48f2127e59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed42d7f1f910630dff244b510469d2406c7a09dfe1189f929830d720093e4d25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d00e3a4e413092a1199b3eeff85440058c95324889086a9d38fdaf6a78c67c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04ab7b63047bd06debb3888a68adb0c8d569b5653fc26cdd56673eb08cc656f2(
    value: typing.Optional[CloudAwsIntegrationsEcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51591c32b4d16705f46eafcbda67feaad34a0e245798a8aca05542df9e22bb4f(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb68c778c42f4a39a9cb09b0001cc862f8cfd2c428b4765f548f2a9285fbc285(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4e7da1fdba58ca9f9235d58ae728836b6997a4c23c350265e2207787288bcc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca6f02f52c7706c8bae670add60262e80cca377f2ee7b74895d71e639b8da87(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d26e7592d9ee7867e96025243cd89109dea2730dc9a8ce1036ab5a531b10278(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60ecc72e4c238fed0e9b5cb57860a8842693a125917dee4e365523246e6c5eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d87edd35880b88d4f04aadab968ed216ac39e7ff1b65887bc81eb418c3df66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d8497c781988fc405051efea0c0a299b2ef0158f81e1b017b49cf49b6a2827(
    value: typing.Optional[CloudAwsIntegrationsEfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a265d833358b069d2e6598bcd48148ee03e786160cd47ea8e1515310681517(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982457a0f6895e0cc9e1f80aac5819a710b35fe5e69e1ad37a8566845b24346f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f099daa9bd9e534c0a0e2779af92e057c7aee6d6f0750ca8e3273d49f44509c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c301267e8f5404c845359347350c0719602845136378747ad9233a1c1ec9bf4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a74d1d6c880c68a800086be7ded5465334eb72d5d1427ee5568066ad8673059(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d0a572643e1fb4e4492e03f8e8fe7f19bd6dcd5a0cfdf59ba556fc0b47d6e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905e8b6e7e65d5ad8d98505c01e090be4e9b9a38eea9bbf29a9c8ff00b48ba92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8994f3840bdf7c9bc56e11e083f5a7cc92c467fc900aa90d6e93c38ad2578349(
    value: typing.Optional[CloudAwsIntegrationsElasticache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f1ab201b42323e7a38236319998e1fd03d900f7c3f1dc464357c54b3f73f19(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2095c6e31c5df5691a2caec253ebecb0ad4d69eede26c171b338804c1eb2d59c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d415eb8246fba884efdfbc5b23e202cb470d149d485023f40255151a70163c47(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bfa72c0e5e1f6bae095d8cf592ac0bc8dc2a8cc8a551ef99532da4dd16e8cb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b665bcaa8758e845578c2711d3fcd1f633ed09312baa00de505a39734ff8d33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0d51f66e7cd5e881f79f1275935dd80bf5d65610599f71b153542ed53a9b44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e78a38e92d32a750149df2e09b652169e17f584297a8d3afece2d98e5816ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b14840bc60eb2113f8b5ce031dc5d96b2eed7b0b9eb3b50dfd5414df78bf54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14643cb6d24f18eab2712e31c07817044c9a9f99cd7f0a7639fa7b00151343e4(
    value: typing.Optional[CloudAwsIntegrationsElasticbeanstalk],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7727f9fe6b3572b1bb784fe6ea29840ccd3473caefa3749c6e0d683041068f34(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ce0bcd96b43b1a66a79cd12005994824450ab6811f480d8efbd9d835e66d05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d785760cff6d1ab0700dcc823e4942dff3886b2d1ce53e87f7773c0cc461d0c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036153fad20e50dba10f4423848c9e081d324b1c20ec20543f09cd494ae3320d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06ddc1ca114209c58bc8b9e5f6fbd635dd8ba5fb926b0e7425896d3a2504d7c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a726fd17918d907da54c6711491bbf2716e17dcdd9fca2a5f4e65842095846c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dde2ce82e59bbbac227b29ea13d4629295d80ef1ac7523c1753279bd03176d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec34d47c44aeb8721aaa4b1644fb4debb947f313c9c7a58ebac0f68610ccc860(
    value: typing.Optional[CloudAwsIntegrationsElasticsearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2884a4a766bd7a950c15bbaeecf493edfc5cb79afb317f70265d74e003c296(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5895c6677f231b40721945fcb94cbef8a4374063716946e207a239150d1d17c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94e0ea139f50608fccc2d99fbac64efe829bf3305593d8bd6c98745ea240f1c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eaa3c9aa758d81bbb6051837b083195073d8641f8cdd7f85373c9b05f048726(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46fb9bf72ca113b8f996bd73cbc0059e6ca9c6bba7fb1a50915390ef88fe896(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae06a2128cfd7dc64cbf85aea0beb8545fdfad115d96e1ad6650266b711ed8b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0183c4d7d2ff4cb238a1f572d5e79aadcf87fd2f8d2bc990a3db357acce6d2f1(
    value: typing.Optional[CloudAwsIntegrationsElb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26424bc22971717dd05375c498d7154172ef8af8956ed4347d56c5fc88f96173(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ecb2084e37056ef2a9e636b08581101d2fcc569251282425077868da06b727(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ffd7840ccbbe14c7361193ca4eef19b80b15709cda70dc2d63d4f6f8f50443e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81dc3b402d8dee82d9bcee8a29d57794dcc754389be2797d7b306f9bee07ea6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87d1ed6f2c4bbb860b0fe1e87358517f7b617b05b5dd593d135b5268cb40fed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060759d3e500820bb87484ba7179952be74065ddd6bee5136e2cea16f64a7068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1f40cf13861dd22b8b31d463052c5a5071215c6b441983627e85cb43bc1919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c25496e28caf4731da733215eda27ca0b7448e7eba45e56e5c9c5cdcbb32a9f(
    value: typing.Optional[CloudAwsIntegrationsEmr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c219d859d9fa6c3f00149ad1692a19b0b2ab9eec6f51eacdd9731529b70b36(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86711bd01ca429e5db58f084e73315a1b7be773c21e46bb74a94ed2a1845097(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2e7878d24eba1730c9b8637f82d3912d9cab70e21be12e9c6003a465cd62f3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24de463ea31715daafca9d6f499d395e152ac71f03aea5f4055fc70ff230ee33(
    value: typing.Optional[CloudAwsIntegrationsHealth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddd5b2e484f42f6a258f352d60e9c154ddecad6865b19d33507415e7615f3aa(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975af37a114bab9caf68b37237f818cd58b2038586da80bee38aa76d1a23f5e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2022803284284011eea6b96b3851fcd5e214cd91decc5e1ea2c8bb981e5394(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d4edd11da59bab88501a1108fec16dfcf1b2fd70e2f2453fa204c8e4510f90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a6826a1a1d121276a53c7e1a9033bdb3ac4b8598c74b560e27665552f8cbf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1e3879db7bd116fec0510ab0155fade4c87d9538232861f78a757e59985986(
    value: typing.Optional[CloudAwsIntegrationsIam],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e422a5bafafa06f150ece395f191b38536bad3a325ba06e69ef2172248cf18(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b975bd5ee64a3398f35f93dda18d97926846853e9117a546746369c0e2dee5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d7b00aae200011394b3a781e56a9e5c36ee44625b1c9f490a1b6dda7ddec6f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638664ab206dd8a34e714ea341a9452ca69f8e6e2cb01ef5fd223f1d79d75b02(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238a3bd0007e0b65b928487ed913e9466ebfcb425ababa5f2e9f00dfa806cd78(
    value: typing.Optional[CloudAwsIntegrationsIot],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02b7ae6ba6effe218d73983d6bbbf1499f4a53b761609aaaf14c2a192347ddc(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_shards: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4899ace1e2f15c8d36df53aaf02c5d848c6f4f665ca6bd9f9291be2b72307e8(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567c934e4890cf64113f332cf8f5342f2afbc4d1fb09df722122c4877d894423(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf56f83953c751aec57b8b9abe86565aac99c6268dd780028cd9b12da77dead(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa20b97c7d6d7d4c339494f3a9d366e1c277b99df5a84a325b0dc0fcb1f95a6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61559454c09978765371771b1fd1ab2290086f29a9fd5f3bb97b16d8c30566b4(
    value: typing.Optional[CloudAwsIntegrationsKinesisFirehose],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed4ccaa26a04852d9fd0956491b1c64fa39d680202a5a48b521bdbc8098bfeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd92d157459e4939262ea4eef0128a6a45609be2cc36da168273a1f0a2599d12(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acac1dbe8d77913ed3dafa701d5c111cf1a1ecb545cdc6974784732fb1804920(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12742bb43ca145ef11839ff33e40ad14ebd9b1e18881ed256af5019810e6e2eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01be2a0db3ea93319ec480199be0e36353acedb9e7a4f58352349b9ca7d789e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca50e97fa059f69150815ec8554a6f7f4f0d8c8fc70f0f178421f8cd052f6a1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb8ddaf3b2d51b928c21dae0e823ca3c59a290af1b1c15155314841c6962f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557e49ef7aafa388d0df54a88624f7e4545513b0b471a78afefd15ec28f5c852(
    value: typing.Optional[CloudAwsIntegrationsKinesis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fba1fd24d6485c6c8669f4032c7de0e5dc1ffd3075fb6700e0e54d2d733054(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ed4d124d33d1ede24dd3d816514f5d3518fe50463134e643c4f465da4acefc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9eb86ad5628bf8d0874822e3cd6f73902e2240255f276237aef59c39c965a3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190a5d35532ff0378c13a9dad64441953d7748f65862a8dc9b9c6b394de3abba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b954e7c3ab2bdbb9f0fdcb637b515eb84bdbf11abe7112c0a8c2a6707a23f6c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd67422d83ee5dc793c39329e97ba424d1069f1aab368b0b3a54f14241a2721(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58410683cb48c383f855b2d0a3d9d1fa6c7f7061e8c796b16e6bff5f85ed089e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e07dcdd6995ab0bdccd67889f84d2fde3d326aa2eb69374e879cdd368977a68(
    value: typing.Optional[CloudAwsIntegrationsLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ef19ee1e94be8c030bd83921992a50012ed15c64f72f499c43c3548a3bb2cb(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d813f5dcfa34c8661e768bce268dba574e35a8f967824c890a7d651403f5c40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49716e4525aee23aed0f5eb394164ceda817c695a0353b3f96bfca8cf8b9d290(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1906b6693db813cbb489fbadf53a0945a2607714764a35db4b3785c139bc4168(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad99a2aed013fa8bfdcdf74614bc5f4c49bb7f0aaf741d71a2ac62a061edf1e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75aaf9f5873b62aad30175bac772f1d58a46011f2e9de335b4738c2474755d2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87229a59051b84c9d20eef39261b5aac6fa86e3b6e747effd5d510115ab222ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9779cc6678a175b67f95fc604708e546c1364644f89021b3da1bf6cbe7b26265(
    value: typing.Optional[CloudAwsIntegrationsRds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bb9070ec2cc7313454135aa1f8ec3cf5a87c394b68065dbf5fd48c24b3d28bd(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b9e86f7a3694b922b37b54da7da2bce3ccb49106cd9cc71debda1866d6c7c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e202bd2b41551e861d3ac4ff6d65f9a1f5635b05a3e6dddf3b883d8f97433c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc9ac273ecefd2d5cefb10cba10ab80cb279c5cd28b3e85f1f0f40c08b06a6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2585a70b4720da2f0ca24c6898f3e6300a3e32a37a39350719c99fe52222379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac02361522846cbb12a65eb96b317096693941efb1a0227fd7a6b037f057967f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fe674c3feffb17fa94e644af690b2b46e4a587f070654bd9df5ef742b3de57(
    value: typing.Optional[CloudAwsIntegrationsRedshift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a20df314f69caa152daeaaf9e1a79af6c02eb767f1c2a074b312a9abf0d8614(
    *,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582cb9615aef9256e0cb8a64f1e3a05a3d279bf27c10c89c7c3165824bf70e15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8298eb105a1aa7686e524467104aa217a512a4ff838edda1ad718f95e2bc5df2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907aaac838f438ff2f0bd7b05b81e09bcde13205f265a75df4b622fbaaac5e05(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7942a524b027d2a916c59459d0b75e534d75383070c2c2eebeb5360873dda36(
    value: typing.Optional[CloudAwsIntegrationsRoute53],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ab9b96b00818e6013fe2103e98626b3ebfb0e15dda0b7f25488ae4ca0a47e8(
    *,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e785c94925ae01e650b7ed9f3f0da5e0411ad1fc02448a3cc694243e0db6dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5d5070716ec7a9d7a7071ca97c377020954879feea0af0375d8219a691771cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__112668b464fb2439d9a502835f3f499c65e2e47667bdb66bbe1ed47e850aac1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6039bca92dc66d6f16736123bcf25b9ff1cdd5a6c24ea16785e120d7afc838d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4920669dd0f46f8cea694a877d684f673679b85d71afb15f111b4adbeadffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d80585b215775cad0e9a2ab99cc85bfb96a397ae1c1c2f67522c88666f5de5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683ccb60ceff40081ecf5543bc48e2f1fe43c3201e15763be3993daa3aa831cc(
    value: typing.Optional[CloudAwsIntegrationsS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8446d723a2e6fb35098bcc49ad88c7494fe6212adf9ae9016a6102d7d8b4f74f(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162538ca923fd38f4e1f2a10bd365045e325767656835e3dfac92c265a5c4342(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6d49c6981a736f07ee60fb99fce538a337ae74c6ce8c12bc4db411e3a17518(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb70314f3e76b5a965216f95665cecd39d55e65bfc29aa41f576224f05379b8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff3890c76b22def229164440f3a955a2c10de38c443fd60a46f5d925fade923(
    value: typing.Optional[CloudAwsIntegrationsSes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ba4c3bcc7ec9bee1908f2e1b40b72d011c01b2a0a8bdfa635d54e0c6471ae0(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3b1801b8139fa0f8353d82d6752e173d8436180b8543875d793457a443a36c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab287791e88ede87e0c3b800bd1a28da1588c7fac7f89f9e000c782cae2b9b88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9852e5a73b67961581aa6c4a75b0c28257e73a5e3f536717471f973b7b836488(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0b495c4e73eab14489b2fffe4f1c9c513e0f3c5af48ce612cad9162175319a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b574dfde649bcffb8d5240d25810f8bc0ec8008250082a1c7d08b4c3cda82832(
    value: typing.Optional[CloudAwsIntegrationsSns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0fdb38a11ddff4ce2122194281474d0b4eb857f20967f959c0b6ff482274d2(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    queue_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c82c17993cd532f044fa9bbb76080639102a1097dd3bbd258b6a057e578a21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0219280ccbb7365033672650f0457d19210eec5eb655bc3d0e7d22327b3ff7c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9eb6b104fa1f8dfc59ea1bc3b7db356606c2c4cba4ff623b18a868fd653197(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a8db6cb6573eae10a24accf4282134c50441a61865fed1f40eb25a7548ee70f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f811bea2416e9ddc5496c341d349847fef56cf5073d15b0acb04b3bd5f512d63(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012ec307c9820febb8e3c2880f114b2fe239b4f9ad935334baf578c9dc5dc3ed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1303753e6b8fc4ca48d1c07abb7cbc0e77ff84cacf809634f6d69c038a004983(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5513d7d34b1d0443eabe5a593433bec77bf17b074d5dafc6871bfedb766913c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dba19905ae3a482b0cf802cca6aaa7cdd3ef5f4ed826c6e6fc4fcb3d9bc2e4(
    value: typing.Optional[CloudAwsIntegrationsSqs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668858f73919a08f504c8a90bb65ffb65bc1d01d05572ddba939811087652a14(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a147261cc3bf496a0e170a5e441607f620af5f12ed60056d946be7f8b8c0f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4f346a457cb1508ddb025b8d144de7b4840241fc61fa8191b69cf6be3c6e85(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bc63cefa256d5b5346d16c3750a584927d393bdf9459dbab1f2801aa2c8f36(
    value: typing.Optional[CloudAwsIntegrationsTrustedAdvisor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a05e1712a6079eebfb1cebb9021117640ecdb1735fc94235af901ee1bb64db(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_nat_gateway: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_vpn: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc03184763dca962a4a8ab314c5c148983b1f331637301224bdc278d238f3491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__555e7d85f2e58ac7b541bacd19f13077a47af6954e80f4b40ac339755b9b7896(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2657609fdf500a4e737b95dd4cc4b3d5550f0c3ef0c867e038437ea0e58637(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da72c88928d008dd41e6355c8234df0e259a01b0abb531818bb0b36c7caf2c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9579bf68121b247cafa084f153862e870a9191414d93835d82fabaa96a992f14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac7fa1649a4d226ab4fb2c00a338e4d9911e66ca678b5bcc71bd5245e0bb120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ea2f558eb8f44587d62e70414f9e1cafca3e2ec1df4590a34f1a3d47499183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ac68e78d33565f199421a44fdec8c9985ca38d90c14b0a0d05bbf25fe5b8d7(
    value: typing.Optional[CloudAwsIntegrationsVpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df10b2612d85d90190d8350575e635e7b3cef8ab626c415ebe5664e6ba53fa3(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a6346257c8ea2f1ec9b3140050ddcbf2de3e49b2b5a0d947981b6092478178a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79083a4b7f98cacdf2df9c5b1d5b897d17ff97f9019b6f6c3ae30bb3bebc0d61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4546e51c704af084ceb7556b0b73a76c7e2723052e3525aec1976082b7e3d1a3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89f8a3bae21c57127494ed28f6b8aaadeb03b9affab91c6a763edc84787e128(
    value: typing.Optional[CloudAwsIntegrationsXRay],
) -> None:
    """Type checking stubs"""
    pass
