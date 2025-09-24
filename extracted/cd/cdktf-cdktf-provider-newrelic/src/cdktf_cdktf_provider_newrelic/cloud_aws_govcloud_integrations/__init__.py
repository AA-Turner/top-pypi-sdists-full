r'''
# `newrelic_cloud_aws_govcloud_integrations`

Refer to the Terraform Registry for docs: [`newrelic_cloud_aws_govcloud_integrations`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations).
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


class CloudAwsGovcloudIntegrations(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrations",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations newrelic_cloud_aws_govcloud_integrations}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        alb: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsAlb", typing.Dict[builtins.str, typing.Any]]] = None,
        api_gateway: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsApiGateway", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scaling: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsAutoScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_direct_connect: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsAwsDirectConnect", typing.Dict[builtins.str, typing.Any]]] = None,
        aws_states: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsAwsStates", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudtrail: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsCloudtrail", typing.Dict[builtins.str, typing.Any]]] = None,
        dynamo_db: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsDynamoDb", typing.Dict[builtins.str, typing.Any]]] = None,
        ebs: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsEbs", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsEc2", typing.Dict[builtins.str, typing.Any]]] = None,
        elastic_search: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsElasticSearch", typing.Dict[builtins.str, typing.Any]]] = None,
        elb: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsElb", typing.Dict[builtins.str, typing.Any]]] = None,
        emr: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsEmr", typing.Dict[builtins.str, typing.Any]]] = None,
        iam: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsIam", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        lambda_: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        rds: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsRds", typing.Dict[builtins.str, typing.Any]]] = None,
        red_shift: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsRedShift", typing.Dict[builtins.str, typing.Any]]] = None,
        route53: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsRoute53", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsS3", typing.Dict[builtins.str, typing.Any]]] = None,
        sns: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsSns", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsSqs", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations newrelic_cloud_aws_govcloud_integrations} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param linked_account_id: The ID of the linked AwsGovCloud account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#linked_account_id CloudAwsGovcloudIntegrations#linked_account_id}
        :param account_id: The ID of the account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#account_id CloudAwsGovcloudIntegrations#account_id}
        :param alb: alb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#alb CloudAwsGovcloudIntegrations#alb}
        :param api_gateway: api_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#api_gateway CloudAwsGovcloudIntegrations#api_gateway}
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#auto_scaling CloudAwsGovcloudIntegrations#auto_scaling}
        :param aws_direct_connect: aws_direct_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_direct_connect CloudAwsGovcloudIntegrations#aws_direct_connect}
        :param aws_states: aws_states block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_states CloudAwsGovcloudIntegrations#aws_states}
        :param cloudtrail: cloudtrail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#cloudtrail CloudAwsGovcloudIntegrations#cloudtrail}
        :param dynamo_db: dynamo_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#dynamo_db CloudAwsGovcloudIntegrations#dynamo_db}
        :param ebs: ebs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#ebs CloudAwsGovcloudIntegrations#ebs}
        :param ec2: ec2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#ec2 CloudAwsGovcloudIntegrations#ec2}
        :param elastic_search: elastic_search block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#elastic_search CloudAwsGovcloudIntegrations#elastic_search}
        :param elb: elb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#elb CloudAwsGovcloudIntegrations#elb}
        :param emr: emr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#emr CloudAwsGovcloudIntegrations#emr}
        :param iam: iam block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#iam CloudAwsGovcloudIntegrations#iam}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#id CloudAwsGovcloudIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#lambda CloudAwsGovcloudIntegrations#lambda}
        :param rds: rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#rds CloudAwsGovcloudIntegrations#rds}
        :param red_shift: red_shift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#red_shift CloudAwsGovcloudIntegrations#red_shift}
        :param route53: route53 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#route53 CloudAwsGovcloudIntegrations#route53}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#s3 CloudAwsGovcloudIntegrations#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#sns CloudAwsGovcloudIntegrations#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#sqs CloudAwsGovcloudIntegrations#sqs}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eda26c6e8d12f000daa81f1c91cf2d134419b2071a38fb8ffa48d2a7e882c6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudAwsGovcloudIntegrationsConfig(
            linked_account_id=linked_account_id,
            account_id=account_id,
            alb=alb,
            api_gateway=api_gateway,
            auto_scaling=auto_scaling,
            aws_direct_connect=aws_direct_connect,
            aws_states=aws_states,
            cloudtrail=cloudtrail,
            dynamo_db=dynamo_db,
            ebs=ebs,
            ec2=ec2,
            elastic_search=elastic_search,
            elb=elb,
            emr=emr,
            iam=iam,
            id=id,
            lambda_=lambda_,
            rds=rds,
            red_shift=red_shift,
            route53=route53,
            s3=s3,
            sns=sns,
            sqs=sqs,
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
        '''Generates CDKTF code for importing a CloudAwsGovcloudIntegrations resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudAwsGovcloudIntegrations to import.
        :param import_from_id: The id of the existing CloudAwsGovcloudIntegrations that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudAwsGovcloudIntegrations to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5f7cb2c053c4b87e652aeb3b80b4d2cde5f869d6876c17f9e5d510ed139f48)
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param load_balancer_prefixes: Specify each name or prefix for the LBs that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#load_balancer_prefixes CloudAwsGovcloudIntegrations#load_balancer_prefixes}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsAlb(
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param stage_prefixes: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#stage_prefixes CloudAwsGovcloudIntegrations#stage_prefixes}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsApiGateway(
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsGovcloudIntegrationsAutoScaling(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScaling", [value]))

    @jsii.member(jsii_name="putAwsDirectConnect")
    def put_aws_direct_connect(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsGovcloudIntegrationsAwsDirectConnect(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsDirectConnect", [value]))

    @jsii.member(jsii_name="putAwsStates")
    def put_aws_states(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsGovcloudIntegrationsAwsStates(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAwsStates", [value]))

    @jsii.member(jsii_name="putCloudtrail")
    def put_cloudtrail(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsGovcloudIntegrationsCloudtrail(
            aws_regions=aws_regions, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putCloudtrail", [value]))

    @jsii.member(jsii_name="putDynamoDb")
    def put_dynamo_db(
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsDynamoDb(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putDynamoDb", [value]))

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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsEbs(
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
        fetch_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_ip_addresses: Specify if IP addresses of ec2 instance should be collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_ip_addresses CloudAwsGovcloudIntegrations#fetch_ip_addresses}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsEc2(
            aws_regions=aws_regions,
            fetch_ip_addresses=fetch_ip_addresses,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putEc2", [value]))

    @jsii.member(jsii_name="putElasticSearch")
    def put_elastic_search(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_nodes: Specify if IP addresses of ec2 instance should be collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_nodes CloudAwsGovcloudIntegrations#fetch_nodes}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsElasticSearch(
            aws_regions=aws_regions,
            fetch_nodes=fetch_nodes,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putElasticSearch", [value]))

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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsGovcloudIntegrationsElb(
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
        aws_regions: typing.Optional[builtins.str] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsEmr(
            aws_regions=aws_regions,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putEmr", [value]))

    @jsii.member(jsii_name="putIam")
    def put_iam(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsIam(
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putIam", [value]))

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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsLambda(
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsRds(
            aws_regions=aws_regions,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putRds", [value]))

    @jsii.member(jsii_name="putRedShift")
    def put_red_shift(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsRedShift(
            aws_regions=aws_regions,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putRedShift", [value]))

    @jsii.member(jsii_name="putRoute53")
    def put_route53(
        self,
        *,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsGovcloudIntegrationsRoute53(
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
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsS3(
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putS3", [value]))

    @jsii.member(jsii_name="putSns")
    def put_sns(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        value = CloudAwsGovcloudIntegrationsSns(
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param queue_prefixes: Specify each name or prefix for the Queues that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#queue_prefixes CloudAwsGovcloudIntegrations#queue_prefixes}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        value = CloudAwsGovcloudIntegrationsSqs(
            aws_regions=aws_regions,
            fetch_extended_inventory=fetch_extended_inventory,
            fetch_tags=fetch_tags,
            metrics_polling_interval=metrics_polling_interval,
            queue_prefixes=queue_prefixes,
            tag_key=tag_key,
            tag_value=tag_value,
        )

        return typing.cast(None, jsii.invoke(self, "putSqs", [value]))

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

    @jsii.member(jsii_name="resetAwsDirectConnect")
    def reset_aws_direct_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsDirectConnect", []))

    @jsii.member(jsii_name="resetAwsStates")
    def reset_aws_states(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsStates", []))

    @jsii.member(jsii_name="resetCloudtrail")
    def reset_cloudtrail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudtrail", []))

    @jsii.member(jsii_name="resetDynamoDb")
    def reset_dynamo_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamoDb", []))

    @jsii.member(jsii_name="resetEbs")
    def reset_ebs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbs", []))

    @jsii.member(jsii_name="resetEc2")
    def reset_ec2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEc2", []))

    @jsii.member(jsii_name="resetElasticSearch")
    def reset_elastic_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticSearch", []))

    @jsii.member(jsii_name="resetElb")
    def reset_elb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElb", []))

    @jsii.member(jsii_name="resetEmr")
    def reset_emr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmr", []))

    @jsii.member(jsii_name="resetIam")
    def reset_iam(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIam", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLambda")
    def reset_lambda(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLambda", []))

    @jsii.member(jsii_name="resetRds")
    def reset_rds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRds", []))

    @jsii.member(jsii_name="resetRedShift")
    def reset_red_shift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedShift", []))

    @jsii.member(jsii_name="resetRoute53")
    def reset_route53(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoute53", []))

    @jsii.member(jsii_name="resetS3")
    def reset_s3(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3", []))

    @jsii.member(jsii_name="resetSns")
    def reset_sns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSns", []))

    @jsii.member(jsii_name="resetSqs")
    def reset_sqs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqs", []))

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
    def alb(self) -> "CloudAwsGovcloudIntegrationsAlbOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsAlbOutputReference", jsii.get(self, "alb"))

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(self) -> "CloudAwsGovcloudIntegrationsApiGatewayOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsApiGatewayOutputReference", jsii.get(self, "apiGateway"))

    @builtins.property
    @jsii.member(jsii_name="autoScaling")
    def auto_scaling(self) -> "CloudAwsGovcloudIntegrationsAutoScalingOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsAutoScalingOutputReference", jsii.get(self, "autoScaling"))

    @builtins.property
    @jsii.member(jsii_name="awsDirectConnect")
    def aws_direct_connect(
        self,
    ) -> "CloudAwsGovcloudIntegrationsAwsDirectConnectOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsAwsDirectConnectOutputReference", jsii.get(self, "awsDirectConnect"))

    @builtins.property
    @jsii.member(jsii_name="awsStates")
    def aws_states(self) -> "CloudAwsGovcloudIntegrationsAwsStatesOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsAwsStatesOutputReference", jsii.get(self, "awsStates"))

    @builtins.property
    @jsii.member(jsii_name="cloudtrail")
    def cloudtrail(self) -> "CloudAwsGovcloudIntegrationsCloudtrailOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsCloudtrailOutputReference", jsii.get(self, "cloudtrail"))

    @builtins.property
    @jsii.member(jsii_name="dynamoDb")
    def dynamo_db(self) -> "CloudAwsGovcloudIntegrationsDynamoDbOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsDynamoDbOutputReference", jsii.get(self, "dynamoDb"))

    @builtins.property
    @jsii.member(jsii_name="ebs")
    def ebs(self) -> "CloudAwsGovcloudIntegrationsEbsOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsEbsOutputReference", jsii.get(self, "ebs"))

    @builtins.property
    @jsii.member(jsii_name="ec2")
    def ec2(self) -> "CloudAwsGovcloudIntegrationsEc2OutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsEc2OutputReference", jsii.get(self, "ec2"))

    @builtins.property
    @jsii.member(jsii_name="elasticSearch")
    def elastic_search(
        self,
    ) -> "CloudAwsGovcloudIntegrationsElasticSearchOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsElasticSearchOutputReference", jsii.get(self, "elasticSearch"))

    @builtins.property
    @jsii.member(jsii_name="elb")
    def elb(self) -> "CloudAwsGovcloudIntegrationsElbOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsElbOutputReference", jsii.get(self, "elb"))

    @builtins.property
    @jsii.member(jsii_name="emr")
    def emr(self) -> "CloudAwsGovcloudIntegrationsEmrOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsEmrOutputReference", jsii.get(self, "emr"))

    @builtins.property
    @jsii.member(jsii_name="iam")
    def iam(self) -> "CloudAwsGovcloudIntegrationsIamOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsIamOutputReference", jsii.get(self, "iam"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "CloudAwsGovcloudIntegrationsLambdaOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsLambdaOutputReference", jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="rds")
    def rds(self) -> "CloudAwsGovcloudIntegrationsRdsOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsRdsOutputReference", jsii.get(self, "rds"))

    @builtins.property
    @jsii.member(jsii_name="redShift")
    def red_shift(self) -> "CloudAwsGovcloudIntegrationsRedShiftOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsRedShiftOutputReference", jsii.get(self, "redShift"))

    @builtins.property
    @jsii.member(jsii_name="route53")
    def route53(self) -> "CloudAwsGovcloudIntegrationsRoute53OutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsRoute53OutputReference", jsii.get(self, "route53"))

    @builtins.property
    @jsii.member(jsii_name="s3")
    def s3(self) -> "CloudAwsGovcloudIntegrationsS3OutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsS3OutputReference", jsii.get(self, "s3"))

    @builtins.property
    @jsii.member(jsii_name="sns")
    def sns(self) -> "CloudAwsGovcloudIntegrationsSnsOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsSnsOutputReference", jsii.get(self, "sns"))

    @builtins.property
    @jsii.member(jsii_name="sqs")
    def sqs(self) -> "CloudAwsGovcloudIntegrationsSqsOutputReference":
        return typing.cast("CloudAwsGovcloudIntegrationsSqsOutputReference", jsii.get(self, "sqs"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="albInput")
    def alb_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsAlb"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsAlb"], jsii.get(self, "albInput"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayInput")
    def api_gateway_input(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsApiGateway"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsApiGateway"], jsii.get(self, "apiGatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingInput")
    def auto_scaling_input(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsAutoScaling"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsAutoScaling"], jsii.get(self, "autoScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="awsDirectConnectInput")
    def aws_direct_connect_input(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsAwsDirectConnect"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsAwsDirectConnect"], jsii.get(self, "awsDirectConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="awsStatesInput")
    def aws_states_input(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsAwsStates"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsAwsStates"], jsii.get(self, "awsStatesInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudtrailInput")
    def cloudtrail_input(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsCloudtrail"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsCloudtrail"], jsii.get(self, "cloudtrailInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamoDbInput")
    def dynamo_db_input(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsDynamoDb"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsDynamoDb"], jsii.get(self, "dynamoDbInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsInput")
    def ebs_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsEbs"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsEbs"], jsii.get(self, "ebsInput"))

    @builtins.property
    @jsii.member(jsii_name="ec2Input")
    def ec2_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsEc2"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsEc2"], jsii.get(self, "ec2Input"))

    @builtins.property
    @jsii.member(jsii_name="elasticSearchInput")
    def elastic_search_input(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsElasticSearch"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsElasticSearch"], jsii.get(self, "elasticSearchInput"))

    @builtins.property
    @jsii.member(jsii_name="elbInput")
    def elb_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsElb"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsElb"], jsii.get(self, "elbInput"))

    @builtins.property
    @jsii.member(jsii_name="emrInput")
    def emr_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsEmr"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsEmr"], jsii.get(self, "emrInput"))

    @builtins.property
    @jsii.member(jsii_name="iamInput")
    def iam_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsIam"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsIam"], jsii.get(self, "iamInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaInput")
    def lambda_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsLambda"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsLambda"], jsii.get(self, "lambdaInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedAccountIdInput")
    def linked_account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "linkedAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="rdsInput")
    def rds_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsRds"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsRds"], jsii.get(self, "rdsInput"))

    @builtins.property
    @jsii.member(jsii_name="redShiftInput")
    def red_shift_input(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsRedShift"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsRedShift"], jsii.get(self, "redShiftInput"))

    @builtins.property
    @jsii.member(jsii_name="route53Input")
    def route53_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsRoute53"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsRoute53"], jsii.get(self, "route53Input"))

    @builtins.property
    @jsii.member(jsii_name="s3Input")
    def s3_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsS3"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsS3"], jsii.get(self, "s3Input"))

    @builtins.property
    @jsii.member(jsii_name="snsInput")
    def sns_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsSns"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsSns"], jsii.get(self, "snsInput"))

    @builtins.property
    @jsii.member(jsii_name="sqsInput")
    def sqs_input(self) -> typing.Optional["CloudAwsGovcloudIntegrationsSqs"]:
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsSqs"], jsii.get(self, "sqsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deb5b6b7a7e0dbe35ffbff76a033a31cc0ed113e1df3a3337249c72947c88f3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd43ecae9ec7fe4d0c563d645913ebc2c4ccf130ebc7e799d59003b038d040ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkedAccountId")
    def linked_account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "linkedAccountId"))

    @linked_account_id.setter
    def linked_account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3aae4015cf6aaf18321e44eef9f8ea8e022df7c9855d6f3527582a57c20e8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedAccountId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsAlb",
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
class CloudAwsGovcloudIntegrationsAlb:
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param load_balancer_prefixes: Specify each name or prefix for the LBs that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#load_balancer_prefixes CloudAwsGovcloudIntegrations#load_balancer_prefixes}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f817a10c04aa2753bc7f77eaa74ea595843e24933e62cde50adea5788d742e97)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def load_balancer_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each name or prefix for the LBs that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#load_balancer_prefixes CloudAwsGovcloudIntegrations#load_balancer_prefixes}
        '''
        result = self._values.get("load_balancer_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsAlb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsAlbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsAlbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cac73cc333055956d85e0b04c9b7de4ab9f3f2e175e9bcd78715c22eac19f468)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0effd0e1b72e171ffc13b950c404e0399680f5535b8c06f5c244a36fd6537e63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a5f6de8716707e764a1b25fb91d58942bc9c2aae422b32886d9d59d01478821)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d50b20006b4fb44495527251f0931a96d955ffd14eea20689958b1429d3e42e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancerPrefixes")
    def load_balancer_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loadBalancerPrefixes"))

    @load_balancer_prefixes.setter
    def load_balancer_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43577ada1e37b683cf3c249ab84f85499a430140dfeddd4659718a4bfd66f6c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancerPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e0abb8a760d80336d085b9ffe0068cb5dff4c21bf24d043e469bb45f7c5fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1758ec9435bb110258d3e1c8e0e4510b5bdf91e5ac86abb8658ad4048fce33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d30c974418cb43d2095ffa97229a880fe9a8c31a82b1e4d0db6b201d558871d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsAlb]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsAlb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsAlb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee44d09715c8e2a9dc190f56be46e8e3e28b152ef6c1fc284e765c8398dbedf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsApiGateway",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
        "stage_prefixes": "stagePrefixes",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsApiGateway:
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param stage_prefixes: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#stage_prefixes CloudAwsGovcloudIntegrations#stage_prefixes}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e087ac35c9cde27979a52f35bb5d73969a36c289a16f4c4fc4875c1578696d3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stage_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#stage_prefixes CloudAwsGovcloudIntegrations#stage_prefixes}
        '''
        result = self._values.get("stage_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsApiGateway(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsApiGatewayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsApiGatewayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25a0e3e7519b24e0665351dca7b6bfcd8dbd5730527be45db8b8a032c6e6dba1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4655ec9ff38c699e1555730715f55c98dd7243a05083fd9ad5df985a5c82844a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f3f3f97827fe2225476110f6e71c5eca23a637815585816c253acbba37048a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagePrefixes")
    def stage_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stagePrefixes"))

    @stage_prefixes.setter
    def stage_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5814335507d0aa3af3a9a30650dd7b3a78e06899ab03f21d52b842a39516e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93245e7217134e5521c8be1eb4ad86b48f0bf37920f698e3c56f979a3fb00b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae211c650bd4ecfe1a7b3b0251d50263d08565a9dc1a0c8d4648dd3288894fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsApiGateway]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsApiGateway], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsApiGateway],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613feb6d84d4e67db676ccbf352272d55b9fc92734af393fd4b80bd72f397400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsAutoScaling",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsGovcloudIntegrationsAutoScaling:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b353a4a956ffb3b1c9ca6779b0b23820e9371a84a16e766d2a4c3daefe9a24d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsAutoScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsAutoScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsAutoScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__549b9dfe0968c3555c9803a6ced8a645164a1ff92a2b1a23ad005a14c03421af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81347b6d30c719016710c7f5ff46c56c8dc2de368a69d52aab28d34c952406fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44b9eb2d2ceb88739ca44c9c9638ccb3d48f99b25e75a1d61decff4095485cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudAwsGovcloudIntegrationsAutoScaling]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsAutoScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsAutoScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523f7c932c45dc3807480e4c71f933217f9a7009760d0460c378f2a070aa0029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsAwsDirectConnect",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsGovcloudIntegrationsAwsDirectConnect:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fac89efd6ee5edc022634453eebeb5ca18400bd17743f0ea008079992859d569)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsAwsDirectConnect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsAwsDirectConnectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsAwsDirectConnectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b59f21cac198f9539573233c8ce44985cd7af94cd24c195b2960e515fc5da9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e9e77f3f012b14247278b4e9e2981aba5eece1d6fdfadb8c76fe10d1b0eb25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f93137c77e7ea80e3e2fa58f2a23ebac4e062c586e1315a0c3ae175a170f327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudAwsGovcloudIntegrationsAwsDirectConnect]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsAwsDirectConnect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsAwsDirectConnect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e027cfd2833307fc3f81f52bfe2b6a88baf4d7dc7807d84433b23866a9aac25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsAwsStates",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsGovcloudIntegrationsAwsStates:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224d17aa02faae1e233081920e641702c92b651090d2ca5b99da27ba1305df29)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsAwsStates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsAwsStatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsAwsStatesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edac122d4db8f9e9ac95c3a2080ffb27a6f30d723a0e9a1bf280bccfad8fa4c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9ca416da9c9bf6ec9984591de1c7454d0fbae47672242d566fd0187558a87eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6652cad744558b7bd7d8352c178fbe826e83b762586304a97d0f01334ec3d669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsAwsStates]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsAwsStates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsAwsStates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caff62f9215c0696cd79e5d182be5363849beaba36f668ada275ef38fd79c5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsCloudtrail",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsGovcloudIntegrationsCloudtrail:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a41ac5be0c1e45cd597be879712bba6f252632e8e6a9bdc519c79bb33cb40b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsCloudtrail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsCloudtrailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsCloudtrailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e23c25c529bfe420e260acf18e8b5b3fb722c2d2718914a897df7e6de142fce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee04b53a4cc7909fbe582098b261fd7ab2c6a5ca0795b781dcaf46a9716e5a19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8e65709f5e4b8e602c43679233df50aaaf3dec7615a8176b94fbbdc98e9f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsCloudtrail]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsCloudtrail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsCloudtrail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6b8d44d1e8cec42cd44fc6bcf2728d9fbbd87ac18169a249d84db4284aec8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsConfig",
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
        "aws_direct_connect": "awsDirectConnect",
        "aws_states": "awsStates",
        "cloudtrail": "cloudtrail",
        "dynamo_db": "dynamoDb",
        "ebs": "ebs",
        "ec2": "ec2",
        "elastic_search": "elasticSearch",
        "elb": "elb",
        "emr": "emr",
        "iam": "iam",
        "id": "id",
        "lambda_": "lambda",
        "rds": "rds",
        "red_shift": "redShift",
        "route53": "route53",
        "s3": "s3",
        "sns": "sns",
        "sqs": "sqs",
    },
)
class CloudAwsGovcloudIntegrationsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        alb: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAlb, typing.Dict[builtins.str, typing.Any]]] = None,
        api_gateway: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsApiGateway, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scaling: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_direct_connect: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAwsDirectConnect, typing.Dict[builtins.str, typing.Any]]] = None,
        aws_states: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAwsStates, typing.Dict[builtins.str, typing.Any]]] = None,
        cloudtrail: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
        dynamo_db: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsDynamoDb", typing.Dict[builtins.str, typing.Any]]] = None,
        ebs: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsEbs", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsEc2", typing.Dict[builtins.str, typing.Any]]] = None,
        elastic_search: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsElasticSearch", typing.Dict[builtins.str, typing.Any]]] = None,
        elb: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsElb", typing.Dict[builtins.str, typing.Any]]] = None,
        emr: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsEmr", typing.Dict[builtins.str, typing.Any]]] = None,
        iam: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsIam", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        lambda_: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        rds: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsRds", typing.Dict[builtins.str, typing.Any]]] = None,
        red_shift: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsRedShift", typing.Dict[builtins.str, typing.Any]]] = None,
        route53: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsRoute53", typing.Dict[builtins.str, typing.Any]]] = None,
        s3: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsS3", typing.Dict[builtins.str, typing.Any]]] = None,
        sns: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsSns", typing.Dict[builtins.str, typing.Any]]] = None,
        sqs: typing.Optional[typing.Union["CloudAwsGovcloudIntegrationsSqs", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param linked_account_id: The ID of the linked AwsGovCloud account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#linked_account_id CloudAwsGovcloudIntegrations#linked_account_id}
        :param account_id: The ID of the account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#account_id CloudAwsGovcloudIntegrations#account_id}
        :param alb: alb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#alb CloudAwsGovcloudIntegrations#alb}
        :param api_gateway: api_gateway block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#api_gateway CloudAwsGovcloudIntegrations#api_gateway}
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#auto_scaling CloudAwsGovcloudIntegrations#auto_scaling}
        :param aws_direct_connect: aws_direct_connect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_direct_connect CloudAwsGovcloudIntegrations#aws_direct_connect}
        :param aws_states: aws_states block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_states CloudAwsGovcloudIntegrations#aws_states}
        :param cloudtrail: cloudtrail block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#cloudtrail CloudAwsGovcloudIntegrations#cloudtrail}
        :param dynamo_db: dynamo_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#dynamo_db CloudAwsGovcloudIntegrations#dynamo_db}
        :param ebs: ebs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#ebs CloudAwsGovcloudIntegrations#ebs}
        :param ec2: ec2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#ec2 CloudAwsGovcloudIntegrations#ec2}
        :param elastic_search: elastic_search block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#elastic_search CloudAwsGovcloudIntegrations#elastic_search}
        :param elb: elb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#elb CloudAwsGovcloudIntegrations#elb}
        :param emr: emr block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#emr CloudAwsGovcloudIntegrations#emr}
        :param iam: iam block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#iam CloudAwsGovcloudIntegrations#iam}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#id CloudAwsGovcloudIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param lambda_: lambda block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#lambda CloudAwsGovcloudIntegrations#lambda}
        :param rds: rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#rds CloudAwsGovcloudIntegrations#rds}
        :param red_shift: red_shift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#red_shift CloudAwsGovcloudIntegrations#red_shift}
        :param route53: route53 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#route53 CloudAwsGovcloudIntegrations#route53}
        :param s3: s3 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#s3 CloudAwsGovcloudIntegrations#s3}
        :param sns: sns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#sns CloudAwsGovcloudIntegrations#sns}
        :param sqs: sqs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#sqs CloudAwsGovcloudIntegrations#sqs}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alb, dict):
            alb = CloudAwsGovcloudIntegrationsAlb(**alb)
        if isinstance(api_gateway, dict):
            api_gateway = CloudAwsGovcloudIntegrationsApiGateway(**api_gateway)
        if isinstance(auto_scaling, dict):
            auto_scaling = CloudAwsGovcloudIntegrationsAutoScaling(**auto_scaling)
        if isinstance(aws_direct_connect, dict):
            aws_direct_connect = CloudAwsGovcloudIntegrationsAwsDirectConnect(**aws_direct_connect)
        if isinstance(aws_states, dict):
            aws_states = CloudAwsGovcloudIntegrationsAwsStates(**aws_states)
        if isinstance(cloudtrail, dict):
            cloudtrail = CloudAwsGovcloudIntegrationsCloudtrail(**cloudtrail)
        if isinstance(dynamo_db, dict):
            dynamo_db = CloudAwsGovcloudIntegrationsDynamoDb(**dynamo_db)
        if isinstance(ebs, dict):
            ebs = CloudAwsGovcloudIntegrationsEbs(**ebs)
        if isinstance(ec2, dict):
            ec2 = CloudAwsGovcloudIntegrationsEc2(**ec2)
        if isinstance(elastic_search, dict):
            elastic_search = CloudAwsGovcloudIntegrationsElasticSearch(**elastic_search)
        if isinstance(elb, dict):
            elb = CloudAwsGovcloudIntegrationsElb(**elb)
        if isinstance(emr, dict):
            emr = CloudAwsGovcloudIntegrationsEmr(**emr)
        if isinstance(iam, dict):
            iam = CloudAwsGovcloudIntegrationsIam(**iam)
        if isinstance(lambda_, dict):
            lambda_ = CloudAwsGovcloudIntegrationsLambda(**lambda_)
        if isinstance(rds, dict):
            rds = CloudAwsGovcloudIntegrationsRds(**rds)
        if isinstance(red_shift, dict):
            red_shift = CloudAwsGovcloudIntegrationsRedShift(**red_shift)
        if isinstance(route53, dict):
            route53 = CloudAwsGovcloudIntegrationsRoute53(**route53)
        if isinstance(s3, dict):
            s3 = CloudAwsGovcloudIntegrationsS3(**s3)
        if isinstance(sns, dict):
            sns = CloudAwsGovcloudIntegrationsSns(**sns)
        if isinstance(sqs, dict):
            sqs = CloudAwsGovcloudIntegrationsSqs(**sqs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf74a61cf454afee559b8e407490ed8866ff45b36e54ef4ba28dd57d4d1b780a)
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
            check_type(argname="argument aws_direct_connect", value=aws_direct_connect, expected_type=type_hints["aws_direct_connect"])
            check_type(argname="argument aws_states", value=aws_states, expected_type=type_hints["aws_states"])
            check_type(argname="argument cloudtrail", value=cloudtrail, expected_type=type_hints["cloudtrail"])
            check_type(argname="argument dynamo_db", value=dynamo_db, expected_type=type_hints["dynamo_db"])
            check_type(argname="argument ebs", value=ebs, expected_type=type_hints["ebs"])
            check_type(argname="argument ec2", value=ec2, expected_type=type_hints["ec2"])
            check_type(argname="argument elastic_search", value=elastic_search, expected_type=type_hints["elastic_search"])
            check_type(argname="argument elb", value=elb, expected_type=type_hints["elb"])
            check_type(argname="argument emr", value=emr, expected_type=type_hints["emr"])
            check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument rds", value=rds, expected_type=type_hints["rds"])
            check_type(argname="argument red_shift", value=red_shift, expected_type=type_hints["red_shift"])
            check_type(argname="argument route53", value=route53, expected_type=type_hints["route53"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
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
        if aws_direct_connect is not None:
            self._values["aws_direct_connect"] = aws_direct_connect
        if aws_states is not None:
            self._values["aws_states"] = aws_states
        if cloudtrail is not None:
            self._values["cloudtrail"] = cloudtrail
        if dynamo_db is not None:
            self._values["dynamo_db"] = dynamo_db
        if ebs is not None:
            self._values["ebs"] = ebs
        if ec2 is not None:
            self._values["ec2"] = ec2
        if elastic_search is not None:
            self._values["elastic_search"] = elastic_search
        if elb is not None:
            self._values["elb"] = elb
        if emr is not None:
            self._values["emr"] = emr
        if iam is not None:
            self._values["iam"] = iam
        if id is not None:
            self._values["id"] = id
        if lambda_ is not None:
            self._values["lambda_"] = lambda_
        if rds is not None:
            self._values["rds"] = rds
        if red_shift is not None:
            self._values["red_shift"] = red_shift
        if route53 is not None:
            self._values["route53"] = route53
        if s3 is not None:
            self._values["s3"] = s3
        if sns is not None:
            self._values["sns"] = sns
        if sqs is not None:
            self._values["sqs"] = sqs

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
        '''The ID of the linked AwsGovCloud account in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#linked_account_id CloudAwsGovcloudIntegrations#linked_account_id}
        '''
        result = self._values.get("linked_account_id")
        assert result is not None, "Required property 'linked_account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the account in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#account_id CloudAwsGovcloudIntegrations#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alb(self) -> typing.Optional[CloudAwsGovcloudIntegrationsAlb]:
        '''alb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#alb CloudAwsGovcloudIntegrations#alb}
        '''
        result = self._values.get("alb")
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsAlb], result)

    @builtins.property
    def api_gateway(self) -> typing.Optional[CloudAwsGovcloudIntegrationsApiGateway]:
        '''api_gateway block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#api_gateway CloudAwsGovcloudIntegrations#api_gateway}
        '''
        result = self._values.get("api_gateway")
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsApiGateway], result)

    @builtins.property
    def auto_scaling(self) -> typing.Optional[CloudAwsGovcloudIntegrationsAutoScaling]:
        '''auto_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#auto_scaling CloudAwsGovcloudIntegrations#auto_scaling}
        '''
        result = self._values.get("auto_scaling")
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsAutoScaling], result)

    @builtins.property
    def aws_direct_connect(
        self,
    ) -> typing.Optional[CloudAwsGovcloudIntegrationsAwsDirectConnect]:
        '''aws_direct_connect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_direct_connect CloudAwsGovcloudIntegrations#aws_direct_connect}
        '''
        result = self._values.get("aws_direct_connect")
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsAwsDirectConnect], result)

    @builtins.property
    def aws_states(self) -> typing.Optional[CloudAwsGovcloudIntegrationsAwsStates]:
        '''aws_states block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_states CloudAwsGovcloudIntegrations#aws_states}
        '''
        result = self._values.get("aws_states")
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsAwsStates], result)

    @builtins.property
    def cloudtrail(self) -> typing.Optional[CloudAwsGovcloudIntegrationsCloudtrail]:
        '''cloudtrail block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#cloudtrail CloudAwsGovcloudIntegrations#cloudtrail}
        '''
        result = self._values.get("cloudtrail")
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsCloudtrail], result)

    @builtins.property
    def dynamo_db(self) -> typing.Optional["CloudAwsGovcloudIntegrationsDynamoDb"]:
        '''dynamo_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#dynamo_db CloudAwsGovcloudIntegrations#dynamo_db}
        '''
        result = self._values.get("dynamo_db")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsDynamoDb"], result)

    @builtins.property
    def ebs(self) -> typing.Optional["CloudAwsGovcloudIntegrationsEbs"]:
        '''ebs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#ebs CloudAwsGovcloudIntegrations#ebs}
        '''
        result = self._values.get("ebs")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsEbs"], result)

    @builtins.property
    def ec2(self) -> typing.Optional["CloudAwsGovcloudIntegrationsEc2"]:
        '''ec2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#ec2 CloudAwsGovcloudIntegrations#ec2}
        '''
        result = self._values.get("ec2")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsEc2"], result)

    @builtins.property
    def elastic_search(
        self,
    ) -> typing.Optional["CloudAwsGovcloudIntegrationsElasticSearch"]:
        '''elastic_search block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#elastic_search CloudAwsGovcloudIntegrations#elastic_search}
        '''
        result = self._values.get("elastic_search")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsElasticSearch"], result)

    @builtins.property
    def elb(self) -> typing.Optional["CloudAwsGovcloudIntegrationsElb"]:
        '''elb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#elb CloudAwsGovcloudIntegrations#elb}
        '''
        result = self._values.get("elb")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsElb"], result)

    @builtins.property
    def emr(self) -> typing.Optional["CloudAwsGovcloudIntegrationsEmr"]:
        '''emr block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#emr CloudAwsGovcloudIntegrations#emr}
        '''
        result = self._values.get("emr")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsEmr"], result)

    @builtins.property
    def iam(self) -> typing.Optional["CloudAwsGovcloudIntegrationsIam"]:
        '''iam block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#iam CloudAwsGovcloudIntegrations#iam}
        '''
        result = self._values.get("iam")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsIam"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#id CloudAwsGovcloudIntegrations#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_(self) -> typing.Optional["CloudAwsGovcloudIntegrationsLambda"]:
        '''lambda block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#lambda CloudAwsGovcloudIntegrations#lambda}
        '''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsLambda"], result)

    @builtins.property
    def rds(self) -> typing.Optional["CloudAwsGovcloudIntegrationsRds"]:
        '''rds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#rds CloudAwsGovcloudIntegrations#rds}
        '''
        result = self._values.get("rds")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsRds"], result)

    @builtins.property
    def red_shift(self) -> typing.Optional["CloudAwsGovcloudIntegrationsRedShift"]:
        '''red_shift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#red_shift CloudAwsGovcloudIntegrations#red_shift}
        '''
        result = self._values.get("red_shift")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsRedShift"], result)

    @builtins.property
    def route53(self) -> typing.Optional["CloudAwsGovcloudIntegrationsRoute53"]:
        '''route53 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#route53 CloudAwsGovcloudIntegrations#route53}
        '''
        result = self._values.get("route53")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsRoute53"], result)

    @builtins.property
    def s3(self) -> typing.Optional["CloudAwsGovcloudIntegrationsS3"]:
        '''s3 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#s3 CloudAwsGovcloudIntegrations#s3}
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsS3"], result)

    @builtins.property
    def sns(self) -> typing.Optional["CloudAwsGovcloudIntegrationsSns"]:
        '''sns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#sns CloudAwsGovcloudIntegrations#sns}
        '''
        result = self._values.get("sns")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsSns"], result)

    @builtins.property
    def sqs(self) -> typing.Optional["CloudAwsGovcloudIntegrationsSqs"]:
        '''sqs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#sqs CloudAwsGovcloudIntegrations#sqs}
        '''
        result = self._values.get("sqs")
        return typing.cast(typing.Optional["CloudAwsGovcloudIntegrationsSqs"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsDynamoDb",
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
class CloudAwsGovcloudIntegrationsDynamoDb:
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369da735db1dbe7da07401c2ef9a44b702b14988bbaaa41d38961f9159bcd7d0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsDynamoDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsDynamoDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsDynamoDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebeb6a06bfaaaf339662f351390d0a7baa739fd08d8054eb7259e2b6897720ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9a51ce489783d51a00a0a48f7d5068e5ec3f3b3177447b43a60888c1916e3a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__caa47b40a9d75414e1134bc3b479c173977d6ad705b2f3b27426329709495734)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fda5a4af916e7ea706cee5c036a5a9ca3fce46a9626650f9c680a3277c1ec11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648c8eaf57c61e6f81580f6fe90acbb027dbca1e110b94ecc0862e2997a86a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a121f11801354943cec60e300c663a742ee2bd9b91fa7a864353d84b3f3faeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63df2f8ef54ebb62af7fee06b26dce71427463530c505e567a1a942ab8cb210a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsDynamoDb]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsDynamoDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsDynamoDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e713173ca419f130e7fff84ad5664ce48ffe46ddaae4135be2ada83de53f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsEbs",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsEbs:
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af26a76ff2dc7a309bae0cd55c2609a3c7c894089d59784fb2c392bdfdb2c62)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsEbs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsEbsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsEbsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2584a027838a469a5faac9aa888e6fde197ab3e68b951d80563539d14c414f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c80d8b4725ed20aef72a948a58e63bd11ee357ca2891b3f25427c4de906be8b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9179780e6a554d661325cfd2b17413a163a9cbfd8f9041baf9a8c3ebc620ff84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6eab784ca9cd30470e73c6dc77214e67e79166485b82dd989a6b9281ec3bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f6c072eca90dfdd735ee0cf3ded4955883871b50dc95ea8c2d93fc0a262f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee68308111386cf21c18b7dc8beb665bc52cc651eef121d02dc42f625cbacb22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsEbs]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsEbs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsEbs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb0b50e778ec5ce00b0dcab61e40301c1f90217fa42bd05136d0832a25f7b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsEc2",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_ip_addresses": "fetchIpAddresses",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsEc2:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_ip_addresses: Specify if IP addresses of ec2 instance should be collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_ip_addresses CloudAwsGovcloudIntegrations#fetch_ip_addresses}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b30e14714e99d72581f3ba4dd21d11d27e87dfc1a26ee67b87f014f6ed39ae3)
            check_type(argname="argument aws_regions", value=aws_regions, expected_type=type_hints["aws_regions"])
            check_type(argname="argument fetch_ip_addresses", value=fetch_ip_addresses, expected_type=type_hints["fetch_ip_addresses"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_value", value=tag_value, expected_type=type_hints["tag_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_regions is not None:
            self._values["aws_regions"] = aws_regions
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_ip_addresses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if IP addresses of ec2 instance should be collected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_ip_addresses CloudAwsGovcloudIntegrations#fetch_ip_addresses}
        '''
        result = self._values.get("fetch_ip_addresses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsEc2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsEc2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsEc2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6495b6f29742b9e983d7245e0a605b274c9c16373831a4d74a2c1dffb9030afa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAwsRegions")
    def reset_aws_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsRegions", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e96bfaa86141ef72fbcd26f79c703b163e360b17d54b995edf90b8efc08685b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__e652ced5390408b11e5df4c8da4671c3d46bfafc61ce88bc8f4d914e462f1240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchIpAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f06b59f97607f9da0ccc66a531f3105659ddd24388ff0485183d1b1b542e7aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03e69fdebf442ac6db80b1e8a25a4ab70da2851efbc129de3d33a7ae88eb3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0fc29b089e11377fc22b412dd1bd4de23bba90597288a5222f10d849a39e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsEc2]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsEc2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsEc2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f191cec0ffc27af5e367ddba1e6af335cafc2a93f06da5c7de8f1af88ed200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsElasticSearch",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_nodes": "fetchNodes",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsElasticSearch:
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_nodes: Specify if IP addresses of ec2 instance should be collected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_nodes CloudAwsGovcloudIntegrations#fetch_nodes}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976a55d3e8593ec8ff86a393cf3d4c0c9ccd67968b991e917cbb1f4afae0475c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_nodes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if IP addresses of ec2 instance should be collected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_nodes CloudAwsGovcloudIntegrations#fetch_nodes}
        '''
        result = self._values.get("fetch_nodes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsElasticSearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsElasticSearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsElasticSearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f497c3971da263a0f045086c819a96f4c4c3b257c7f12541968c24d60d857ee3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18bd4032357bfb28b9e6ac09417630d88425fcbaeed74f25e38f95b7d586ae37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e67832fc3e3d0016cff07f596fab63adb2631facee0756e949cfee82ba299ac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchNodes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5144f42471d6a91645879b3c661b77dfbe1d15695a3b99b4589a89ef67f53445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75422338f59e1499b29bd833cd2fc071f27aa0f33e031fee01f120be8c414090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6416608d4c7d658381187e138f8db3f13ebaeca035dfc39d28f85604724aa91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudAwsGovcloudIntegrationsElasticSearch]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsElasticSearch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsElasticSearch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de08e3fbe38575c18cc23d4d0b5ee0f0fcef4a6c09759489628cd339adfc4351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsElb",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsGovcloudIntegrationsElb:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eda53f4a4b30871629329a7a13ebccee2521f4905abd3ab08fe947c296b131a9)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsElb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsElbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsElbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e31d0039670e097919b16a9f0afc12e90e2a8bd51b03451e7e4e3c8bf6361a9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69d68b1cf47a043d008fd11dd51ce2224cc1aa43fe376bdfabdf5615716eeeb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c0d43b0e80ea9001f5d6d748033671adc15a2c9930ff05f705d1690d4ccf4f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8026413017183e8c4040be55fe5faa53986fea1b38a2c9be467c34c5ae7b0a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d331402c638cadef7d31af3486923dd4b545225a2c0900b6b3fe185905b878fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsElb]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsElb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsElb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f47ab07315d85b757b148e97924e9fef732c38afdef756af663ce600247b03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsEmr",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsEmr:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[builtins.str] = None,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffd346cdb60df198343c865413dad68c2009fd5095cae18f677c44b87a68479)
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
    def aws_regions(self) -> typing.Optional[builtins.str]:
        '''Specify each AWS region that includes the resources that you want to monitor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsEmr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsEmrOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsEmrOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5627e3578fd75e771a99c29c7519549b019f0d1c5ee4ac2f4aab5c6dbeef1c45)
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
    def aws_regions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsRegionsInput"))

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
    def aws_regions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsRegions"))

    @aws_regions.setter
    def aws_regions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fdfc2434bdf7757474a8a8c641769d71f8af0409262721eb93b54472a61d80e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7f85bbae79a914aa9e4efd89246a848b06b28e3241b7496a17f2cef97e3decf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61216f28b0c927651c5343201d9e88e2fe4580beef3f5ccc10d93a2261bae8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31592ade29adf39fbedd7d6786580235f1b426968374ef0c0aab01b52d67aae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a6bb8c4559f757c4c8bc5a2aed04df809ed79bd7b85c90945a946b6d8c6435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsEmr]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsEmr], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsEmr],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d412035c23b43536ec42236de7bd5fca395bfff001ab6ede23c6b00624465b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsIam",
    jsii_struct_bases=[],
    name_mapping={
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsIam:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1d2078bbe54373546cd05ac14a3780f82eac9c224ff4aaeec0232debf38e5d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsIam(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsIamOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsIamOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45d531a26a4e2e5ce408996e7e21b4d4af75f9d3d63f19b49cb799e2597487c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52a96077dd72c394dc33d5cde9e34cf9d278562edd64b757cdd9a0089de53356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147b08e2cbfc7e8d637b00a627197e1af12a7ad2e753a73237692d6cb64f10d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca056f8ed880b67e2c0795ab321260589c1568589d5a90cae6d5a513ba0da9c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsIam]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsIam], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsIam],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b35540f22414a4052bf152066b36152e1c0039c56dbeadf784d668e7439dca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsLambda",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsLambda:
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd820aef904432036e66947e64324d505eecbc2aaad422a5aa200c65c304b587)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsLambdaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsLambdaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea0e13d3f50a4e36c6c1342686f6bcc3add3229439436bc905cb3a08c1623633)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a21e645d64a2ff102adb887cb213b654f79993f0a3ae595394a942a1d9e7fea9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88219676566ed0a97343350bb098ceab56b7c966ba102171df744712673e0738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af46152d644d2e430d4650bbb4998046c1cae62b127057c386ca10bcdd030a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6517f197559660c4a774e571bccbb12a1e306e570d00186decc9e39ec03dbd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5835f11b7f5d3cf963c6e2499bb1f3fd170f3f464ffc83af5da864e12d9d711a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsLambda]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsLambda], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsLambda],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4967b129dc84d269958273f36cea9e1de2dc40c067eae6004bc4eecf403988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsRds",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsRds:
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b467006cde7fbb5c56b9532fd2884a0c9aabfb94d3818b23d9d20af2d2c889c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsRds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsRdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsRdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7e2bdc76fe35684624886a74ee0fb53d06066132f3d1ab3040488e957e087ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4baf6fd707c0dd51a63a5d62392fb784d819d9bbbcecd93d2d1f6e38ff67ea60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cea821f06470870d28497e0f4fd291fa87a1d4f3d6938b515df865c17d98381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e828607ef160b4f27c81fb9e3776cafac72c08472e43710cc4d381257f85c1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704436daed79ffc232792ce367de3ddfa0b1a746d5799132ea4f7177c02d0c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab1fa25118a929890518bfb6849ab2051731bcebc98e958a7ed831578ee730bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsRds]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsRds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsRds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2471c28b1fb1f56cfb287e6cc2b559419c09ffbbf4168feb891a7d744f4b4c8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsRedShift",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsRedShift:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa2b6446a47775bf06d1ab2e3297d98c0b74f935b010b9514b584fde9915417)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsRedShift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsRedShiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsRedShiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30052ea8e0aa4ce770ec67d05ed97c9f7e9135fc2e747a2539b5cbb4ec64b0c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__678d0ce030f8e388c20405a5151513a52d8a7353d20fd49378d16ac803d13473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsRegions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96642c1b38786135054a595c465a051dbdd5267685ab67983181242e1f3252b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348731a53875cabe3fc23e251483183dd17003f6d42471ae1271d14ce7e246f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7edfe4d83c16ab69a8f94c0fe9779a89407db53698e85f46916f8beafcd3c764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsRedShift]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsRedShift], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsRedShift],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc8bf1d4dc66257e683aa11f017fae9f0ceef8ff1c0ea4e5767a09629798338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsRoute53",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_extended_inventory": "fetchExtendedInventory",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsGovcloudIntegrationsRoute53:
    def __init__(
        self,
        *,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc423df6bc44af0ccea6175c05059961391289e8484072d7c12b6e18f4dd4686)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsRoute53(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsRoute53OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsRoute53OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47f6eb6867adb72e687741c0b04b41fd7aa6049489ecb4a13910879be7b216f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4279c30d6255b53a194b6cfa722deec9ee94ff84f64db0123f839549c2c805b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef15d635ade457ead4f5070ce01ac80caeb153c9cf962728686db9b028b79a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsRoute53]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsRoute53], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsRoute53],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da10936b1fbf34d8637633e1ea44c87ed03f4f78d55cf88b8b1be253e774f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsS3",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_extended_inventory": "fetchExtendedInventory",
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
        "tag_key": "tagKey",
        "tag_value": "tagValue",
    },
)
class CloudAwsGovcloudIntegrationsS3:
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
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46eeaedf0b60d122318da800106206618796d5633405d6fa32948d46adf77df3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsS3(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsS3OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsS3OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72411924004368c43d1afe1843f56cac2baf5e108fd1aa315361b535544edc59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7baee762c815a1cbc216d98d190c4ab63169ed1724f53623de51ae19dad672e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0707748e83342ad189e44c79cf7f42b158f4bdaf49a17877cf86a009b90f48bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6cf65c7c785b459084bdca660853e2823b3e99cfe279d77f400babdb6a57cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85bedd4e5fbaf17fa1fe71d43eaba1392b8892110876f84f065eb0bededc6473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f659157dfa39b36003f49576d69c31caa7e58dba545db945f41c6fa588e442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsS3]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsS3], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsS3],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ba623284c81f8e81ebe3ac1ced7444006bc39560606027b09570992fe8f6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsSns",
    jsii_struct_bases=[],
    name_mapping={
        "aws_regions": "awsRegions",
        "fetch_extended_inventory": "fetchExtendedInventory",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudAwsGovcloudIntegrationsSns:
    def __init__(
        self,
        *,
        aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0a8d81b32ee67703acdff645ba65cdd045ffa23fa1bfe2739a995e728ee1ba)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsSns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsSnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsSnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__844febf0bac41b3e47156c99bc68bb295d583c372b250aa851645b7814f17e9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc4c7e7e6c8e586f5ce339a2d2cee32e124eb478b074a886574f6a9f92a6e732)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aa8d4c2c65d8f09022ecb662b36738d55fca321ce11f30a23e7c2bcafb29a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchExtendedInventory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4882e8f091b655bf6b7de5ebed71c77f014a1d638042e22a750d8ea4a3a37b50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsSns]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsSns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsSns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d9144c0d72826b52abac0982099a403a81b898d2733ea7fc675a7706a89764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsSqs",
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
class CloudAwsGovcloudIntegrationsSqs:
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
        :param aws_regions: Specify each AWS region that includes the resources that you want to monitor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        :param fetch_extended_inventory: Determine if extra inventory data be collected or not. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        :param fetch_tags: Specify if tags should be collected. May affect total data collection time and contribute to the Cloud provider API rate limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        :param metrics_polling_interval: The data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        :param queue_prefixes: Specify each name or prefix for the Queues that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#queue_prefixes CloudAwsGovcloudIntegrations#queue_prefixes}
        :param tag_key: Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        :param tag_value: Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68cae4d216a7702a7cbdc5367425e888b8454c9db2a0f47cf1aaa33c08380bf8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#aws_regions CloudAwsGovcloudIntegrations#aws_regions}
        '''
        result = self._values.get("aws_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def fetch_extended_inventory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determine if extra inventory data be collected or not.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_extended_inventory CloudAwsGovcloudIntegrations#fetch_extended_inventory}
        '''
        result = self._values.get("fetch_extended_inventory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specify if tags should be collected.

        May affect total data collection time and contribute to the Cloud provider API rate limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#fetch_tags CloudAwsGovcloudIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''The data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#metrics_polling_interval CloudAwsGovcloudIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify each name or prefix for the Queues that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#queue_prefixes CloudAwsGovcloudIntegrations#queue_prefixes}
        '''
        result = self._values.get("queue_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag key associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_key CloudAwsGovcloudIntegrations#tag_key}
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_value(self) -> typing.Optional[builtins.str]:
        '''Specify a Tag value associated with the resources that you want to monitor. Filter values are case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_aws_govcloud_integrations#tag_value CloudAwsGovcloudIntegrations#tag_value}
        '''
        result = self._values.get("tag_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudAwsGovcloudIntegrationsSqs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudAwsGovcloudIntegrationsSqsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudAwsGovcloudIntegrations.CloudAwsGovcloudIntegrationsSqsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf90dfc825b01e346b77e39984160b288e690317a0a7893c5aa8fac80bfa4ad0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea99ebe1553bd30cf0351fd7874442c7d708c5b214114285d0ef82af7cc58d39)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c9b677c4fe053ebc7a800e5505df89900ae676de1b0cda1247ffeb7652431d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e90d71d8fd2a8bf9c2d6aa14ba45b5b77b92c27aa33d38b574b34ca40982273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818c9e6b7d471539328b96bb9fbe8641a7bd763e9fc076bf7310c9558e5a3e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queuePrefixes")
    def queue_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queuePrefixes"))

    @queue_prefixes.setter
    def queue_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6044511a0eeb759003a1f86a17da51e2740c7388fc94d04bfe859f029f0ed8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queuePrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860bc61c08d69419017d02ace269d2f790a5c5af209282a9ab35ef4094ef47fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagValue")
    def tag_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagValue"))

    @tag_value.setter
    def tag_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92269292809b26431010a46e4f186735ed48a1cfb15a16092c0722aed8c42ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudAwsGovcloudIntegrationsSqs]:
        return typing.cast(typing.Optional[CloudAwsGovcloudIntegrationsSqs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudAwsGovcloudIntegrationsSqs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72a7c57c2dae935fa4a3192a7c91af5b6d96087ecede5c2e3a7cacf879987ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudAwsGovcloudIntegrations",
    "CloudAwsGovcloudIntegrationsAlb",
    "CloudAwsGovcloudIntegrationsAlbOutputReference",
    "CloudAwsGovcloudIntegrationsApiGateway",
    "CloudAwsGovcloudIntegrationsApiGatewayOutputReference",
    "CloudAwsGovcloudIntegrationsAutoScaling",
    "CloudAwsGovcloudIntegrationsAutoScalingOutputReference",
    "CloudAwsGovcloudIntegrationsAwsDirectConnect",
    "CloudAwsGovcloudIntegrationsAwsDirectConnectOutputReference",
    "CloudAwsGovcloudIntegrationsAwsStates",
    "CloudAwsGovcloudIntegrationsAwsStatesOutputReference",
    "CloudAwsGovcloudIntegrationsCloudtrail",
    "CloudAwsGovcloudIntegrationsCloudtrailOutputReference",
    "CloudAwsGovcloudIntegrationsConfig",
    "CloudAwsGovcloudIntegrationsDynamoDb",
    "CloudAwsGovcloudIntegrationsDynamoDbOutputReference",
    "CloudAwsGovcloudIntegrationsEbs",
    "CloudAwsGovcloudIntegrationsEbsOutputReference",
    "CloudAwsGovcloudIntegrationsEc2",
    "CloudAwsGovcloudIntegrationsEc2OutputReference",
    "CloudAwsGovcloudIntegrationsElasticSearch",
    "CloudAwsGovcloudIntegrationsElasticSearchOutputReference",
    "CloudAwsGovcloudIntegrationsElb",
    "CloudAwsGovcloudIntegrationsElbOutputReference",
    "CloudAwsGovcloudIntegrationsEmr",
    "CloudAwsGovcloudIntegrationsEmrOutputReference",
    "CloudAwsGovcloudIntegrationsIam",
    "CloudAwsGovcloudIntegrationsIamOutputReference",
    "CloudAwsGovcloudIntegrationsLambda",
    "CloudAwsGovcloudIntegrationsLambdaOutputReference",
    "CloudAwsGovcloudIntegrationsRds",
    "CloudAwsGovcloudIntegrationsRdsOutputReference",
    "CloudAwsGovcloudIntegrationsRedShift",
    "CloudAwsGovcloudIntegrationsRedShiftOutputReference",
    "CloudAwsGovcloudIntegrationsRoute53",
    "CloudAwsGovcloudIntegrationsRoute53OutputReference",
    "CloudAwsGovcloudIntegrationsS3",
    "CloudAwsGovcloudIntegrationsS3OutputReference",
    "CloudAwsGovcloudIntegrationsSns",
    "CloudAwsGovcloudIntegrationsSnsOutputReference",
    "CloudAwsGovcloudIntegrationsSqs",
    "CloudAwsGovcloudIntegrationsSqsOutputReference",
]

publication.publish()

def _typecheckingstub__7eda26c6e8d12f000daa81f1c91cf2d134419b2071a38fb8ffa48d2a7e882c6c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    alb: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAlb, typing.Dict[builtins.str, typing.Any]]] = None,
    api_gateway: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsApiGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scaling: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_direct_connect: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAwsDirectConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_states: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAwsStates, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudtrail: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamo_db: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsDynamoDb, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsEbs, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsEc2, typing.Dict[builtins.str, typing.Any]]] = None,
    elastic_search: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsElasticSearch, typing.Dict[builtins.str, typing.Any]]] = None,
    elb: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsElb, typing.Dict[builtins.str, typing.Any]]] = None,
    emr: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsEmr, typing.Dict[builtins.str, typing.Any]]] = None,
    iam: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsIam, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    lambda_: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsLambda, typing.Dict[builtins.str, typing.Any]]] = None,
    rds: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsRds, typing.Dict[builtins.str, typing.Any]]] = None,
    red_shift: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsRedShift, typing.Dict[builtins.str, typing.Any]]] = None,
    route53: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsRoute53, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsS3, typing.Dict[builtins.str, typing.Any]]] = None,
    sns: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsSns, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsSqs, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8f5f7cb2c053c4b87e652aeb3b80b4d2cde5f869d6876c17f9e5d510ed139f48(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb5b6b7a7e0dbe35ffbff76a033a31cc0ed113e1df3a3337249c72947c88f3b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd43ecae9ec7fe4d0c563d645913ebc2c4ccf130ebc7e799d59003b038d040ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3aae4015cf6aaf18321e44eef9f8ea8e022df7c9855d6f3527582a57c20e8bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f817a10c04aa2753bc7f77eaa74ea595843e24933e62cde50adea5788d742e97(
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

def _typecheckingstub__cac73cc333055956d85e0b04c9b7de4ab9f3f2e175e9bcd78715c22eac19f468(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0effd0e1b72e171ffc13b950c404e0399680f5535b8c06f5c244a36fd6537e63(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5f6de8716707e764a1b25fb91d58942bc9c2aae422b32886d9d59d01478821(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50b20006b4fb44495527251f0931a96d955ffd14eea20689958b1429d3e42e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43577ada1e37b683cf3c249ab84f85499a430140dfeddd4659718a4bfd66f6c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e0abb8a760d80336d085b9ffe0068cb5dff4c21bf24d043e469bb45f7c5fde(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1758ec9435bb110258d3e1c8e0e4510b5bdf91e5ac86abb8658ad4048fce33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d30c974418cb43d2095ffa97229a880fe9a8c31a82b1e4d0db6b201d558871d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee44d09715c8e2a9dc190f56be46e8e3e28b152ef6c1fc284e765c8398dbedf1(
    value: typing.Optional[CloudAwsGovcloudIntegrationsAlb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e087ac35c9cde27979a52f35bb5d73969a36c289a16f4c4fc4875c1578696d3(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    stage_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a0e3e7519b24e0665351dca7b6bfcd8dbd5730527be45db8b8a032c6e6dba1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4655ec9ff38c699e1555730715f55c98dd7243a05083fd9ad5df985a5c82844a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f3f3f97827fe2225476110f6e71c5eca23a637815585816c253acbba37048a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae5814335507d0aa3af3a9a30650dd7b3a78e06899ab03f21d52b842a39516e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93245e7217134e5521c8be1eb4ad86b48f0bf37920f698e3c56f979a3fb00b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae211c650bd4ecfe1a7b3b0251d50263d08565a9dc1a0c8d4648dd3288894fd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613feb6d84d4e67db676ccbf352272d55b9fc92734af393fd4b80bd72f397400(
    value: typing.Optional[CloudAwsGovcloudIntegrationsApiGateway],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b353a4a956ffb3b1c9ca6779b0b23820e9371a84a16e766d2a4c3daefe9a24d(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549b9dfe0968c3555c9803a6ced8a645164a1ff92a2b1a23ad005a14c03421af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81347b6d30c719016710c7f5ff46c56c8dc2de368a69d52aab28d34c952406fe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44b9eb2d2ceb88739ca44c9c9638ccb3d48f99b25e75a1d61decff4095485cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523f7c932c45dc3807480e4c71f933217f9a7009760d0460c378f2a070aa0029(
    value: typing.Optional[CloudAwsGovcloudIntegrationsAutoScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac89efd6ee5edc022634453eebeb5ca18400bd17743f0ea008079992859d569(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b59f21cac198f9539573233c8ce44985cd7af94cd24c195b2960e515fc5da9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9e77f3f012b14247278b4e9e2981aba5eece1d6fdfadb8c76fe10d1b0eb25c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f93137c77e7ea80e3e2fa58f2a23ebac4e062c586e1315a0c3ae175a170f327(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e027cfd2833307fc3f81f52bfe2b6a88baf4d7dc7807d84433b23866a9aac25(
    value: typing.Optional[CloudAwsGovcloudIntegrationsAwsDirectConnect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224d17aa02faae1e233081920e641702c92b651090d2ca5b99da27ba1305df29(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edac122d4db8f9e9ac95c3a2080ffb27a6f30d723a0e9a1bf280bccfad8fa4c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ca416da9c9bf6ec9984591de1c7454d0fbae47672242d566fd0187558a87eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6652cad744558b7bd7d8352c178fbe826e83b762586304a97d0f01334ec3d669(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caff62f9215c0696cd79e5d182be5363849beaba36f668ada275ef38fd79c5d3(
    value: typing.Optional[CloudAwsGovcloudIntegrationsAwsStates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a41ac5be0c1e45cd597be879712bba6f252632e8e6a9bdc519c79bb33cb40b(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e23c25c529bfe420e260acf18e8b5b3fb722c2d2718914a897df7e6de142fce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee04b53a4cc7909fbe582098b261fd7ab2c6a5ca0795b781dcaf46a9716e5a19(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8e65709f5e4b8e602c43679233df50aaaf3dec7615a8176b94fbbdc98e9f12(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6b8d44d1e8cec42cd44fc6bcf2728d9fbbd87ac18169a249d84db4284aec8d(
    value: typing.Optional[CloudAwsGovcloudIntegrationsCloudtrail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf74a61cf454afee559b8e407490ed8866ff45b36e54ef4ba28dd57d4d1b780a(
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
    alb: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAlb, typing.Dict[builtins.str, typing.Any]]] = None,
    api_gateway: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsApiGateway, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scaling: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_direct_connect: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAwsDirectConnect, typing.Dict[builtins.str, typing.Any]]] = None,
    aws_states: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsAwsStates, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudtrail: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsCloudtrail, typing.Dict[builtins.str, typing.Any]]] = None,
    dynamo_db: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsDynamoDb, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsEbs, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsEc2, typing.Dict[builtins.str, typing.Any]]] = None,
    elastic_search: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsElasticSearch, typing.Dict[builtins.str, typing.Any]]] = None,
    elb: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsElb, typing.Dict[builtins.str, typing.Any]]] = None,
    emr: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsEmr, typing.Dict[builtins.str, typing.Any]]] = None,
    iam: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsIam, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    lambda_: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsLambda, typing.Dict[builtins.str, typing.Any]]] = None,
    rds: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsRds, typing.Dict[builtins.str, typing.Any]]] = None,
    red_shift: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsRedShift, typing.Dict[builtins.str, typing.Any]]] = None,
    route53: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsRoute53, typing.Dict[builtins.str, typing.Any]]] = None,
    s3: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsS3, typing.Dict[builtins.str, typing.Any]]] = None,
    sns: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsSns, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs: typing.Optional[typing.Union[CloudAwsGovcloudIntegrationsSqs, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369da735db1dbe7da07401c2ef9a44b702b14988bbaaa41d38961f9159bcd7d0(
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

def _typecheckingstub__ebeb6a06bfaaaf339662f351390d0a7baa739fd08d8054eb7259e2b6897720ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a51ce489783d51a00a0a48f7d5068e5ec3f3b3177447b43a60888c1916e3a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa47b40a9d75414e1134bc3b479c173977d6ad705b2f3b27426329709495734(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fda5a4af916e7ea706cee5c036a5a9ca3fce46a9626650f9c680a3277c1ec11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648c8eaf57c61e6f81580f6fe90acbb027dbca1e110b94ecc0862e2997a86a59(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a121f11801354943cec60e300c663a742ee2bd9b91fa7a864353d84b3f3faeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63df2f8ef54ebb62af7fee06b26dce71427463530c505e567a1a942ab8cb210a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e713173ca419f130e7fff84ad5664ce48ffe46ddaae4135be2ada83de53f41(
    value: typing.Optional[CloudAwsGovcloudIntegrationsDynamoDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af26a76ff2dc7a309bae0cd55c2609a3c7c894089d59784fb2c392bdfdb2c62(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2584a027838a469a5faac9aa888e6fde197ab3e68b951d80563539d14c414f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80d8b4725ed20aef72a948a58e63bd11ee357ca2891b3f25427c4de906be8b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9179780e6a554d661325cfd2b17413a163a9cbfd8f9041baf9a8c3ebc620ff84(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6eab784ca9cd30470e73c6dc77214e67e79166485b82dd989a6b9281ec3bd2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f6c072eca90dfdd735ee0cf3ded4955883871b50dc95ea8c2d93fc0a262f5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee68308111386cf21c18b7dc8beb665bc52cc651eef121d02dc42f625cbacb22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb0b50e778ec5ce00b0dcab61e40301c1f90217fa42bd05136d0832a25f7b4f(
    value: typing.Optional[CloudAwsGovcloudIntegrationsEbs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b30e14714e99d72581f3ba4dd21d11d27e87dfc1a26ee67b87f014f6ed39ae3(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_ip_addresses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6495b6f29742b9e983d7245e0a605b274c9c16373831a4d74a2c1dffb9030afa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96bfaa86141ef72fbcd26f79c703b163e360b17d54b995edf90b8efc08685b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e652ced5390408b11e5df4c8da4671c3d46bfafc61ce88bc8f4d914e462f1240(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f06b59f97607f9da0ccc66a531f3105659ddd24388ff0485183d1b1b542e7aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03e69fdebf442ac6db80b1e8a25a4ab70da2851efbc129de3d33a7ae88eb3c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0fc29b089e11377fc22b412dd1bd4de23bba90597288a5222f10d849a39e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f191cec0ffc27af5e367ddba1e6af335cafc2a93f06da5c7de8f1af88ed200(
    value: typing.Optional[CloudAwsGovcloudIntegrationsEc2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976a55d3e8593ec8ff86a393cf3d4c0c9ccd67968b991e917cbb1f4afae0475c(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_nodes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f497c3971da263a0f045086c819a96f4c4c3b257c7f12541968c24d60d857ee3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bd4032357bfb28b9e6ac09417630d88425fcbaeed74f25e38f95b7d586ae37(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67832fc3e3d0016cff07f596fab63adb2631facee0756e949cfee82ba299ac2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5144f42471d6a91645879b3c661b77dfbe1d15695a3b99b4589a89ef67f53445(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75422338f59e1499b29bd833cd2fc071f27aa0f33e031fee01f120be8c414090(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6416608d4c7d658381187e138f8db3f13ebaeca035dfc39d28f85604724aa91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de08e3fbe38575c18cc23d4d0b5ee0f0fcef4a6c09759489628cd339adfc4351(
    value: typing.Optional[CloudAwsGovcloudIntegrationsElasticSearch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda53f4a4b30871629329a7a13ebccee2521f4905abd3ab08fe947c296b131a9(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31d0039670e097919b16a9f0afc12e90e2a8bd51b03451e7e4e3c8bf6361a9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d68b1cf47a043d008fd11dd51ce2224cc1aa43fe376bdfabdf5615716eeeb5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0d43b0e80ea9001f5d6d748033671adc15a2c9930ff05f705d1690d4ccf4f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8026413017183e8c4040be55fe5faa53986fea1b38a2c9be467c34c5ae7b0a27(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d331402c638cadef7d31af3486923dd4b545225a2c0900b6b3fe185905b878fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f47ab07315d85b757b148e97924e9fef732c38afdef756af663ce600247b03(
    value: typing.Optional[CloudAwsGovcloudIntegrationsElb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffd346cdb60df198343c865413dad68c2009fd5095cae18f677c44b87a68479(
    *,
    aws_regions: typing.Optional[builtins.str] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5627e3578fd75e771a99c29c7519549b019f0d1c5ee4ac2f4aab5c6dbeef1c45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdfc2434bdf7757474a8a8c641769d71f8af0409262721eb93b54472a61d80e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f85bbae79a914aa9e4efd89246a848b06b28e3241b7496a17f2cef97e3decf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61216f28b0c927651c5343201d9e88e2fe4580beef3f5ccc10d93a2261bae8f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31592ade29adf39fbedd7d6786580235f1b426968374ef0c0aab01b52d67aae7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a6bb8c4559f757c4c8bc5a2aed04df809ed79bd7b85c90945a946b6d8c6435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d412035c23b43536ec42236de7bd5fca395bfff001ab6ede23c6b00624465b0(
    value: typing.Optional[CloudAwsGovcloudIntegrationsEmr],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1d2078bbe54373546cd05ac14a3780f82eac9c224ff4aaeec0232debf38e5d(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d531a26a4e2e5ce408996e7e21b4d4af75f9d3d63f19b49cb799e2597487c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a96077dd72c394dc33d5cde9e34cf9d278562edd64b757cdd9a0089de53356(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147b08e2cbfc7e8d637b00a627197e1af12a7ad2e753a73237692d6cb64f10d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca056f8ed880b67e2c0795ab321260589c1568589d5a90cae6d5a513ba0da9c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b35540f22414a4052bf152066b36152e1c0039c56dbeadf784d668e7439dca5(
    value: typing.Optional[CloudAwsGovcloudIntegrationsIam],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd820aef904432036e66947e64324d505eecbc2aaad422a5aa200c65c304b587(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0e13d3f50a4e36c6c1342686f6bcc3add3229439436bc905cb3a08c1623633(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21e645d64a2ff102adb887cb213b654f79993f0a3ae595394a942a1d9e7fea9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88219676566ed0a97343350bb098ceab56b7c966ba102171df744712673e0738(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af46152d644d2e430d4650bbb4998046c1cae62b127057c386ca10bcdd030a25(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6517f197559660c4a774e571bccbb12a1e306e570d00186decc9e39ec03dbd16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5835f11b7f5d3cf963c6e2499bb1f3fd170f3f464ffc83af5da864e12d9d711a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4967b129dc84d269958273f36cea9e1de2dc40c067eae6004bc4eecf403988(
    value: typing.Optional[CloudAwsGovcloudIntegrationsLambda],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b467006cde7fbb5c56b9532fd2884a0c9aabfb94d3818b23d9d20af2d2c889c(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e2bdc76fe35684624886a74ee0fb53d06066132f3d1ab3040488e957e087ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4baf6fd707c0dd51a63a5d62392fb784d819d9bbbcecd93d2d1f6e38ff67ea60(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cea821f06470870d28497e0f4fd291fa87a1d4f3d6938b515df865c17d98381(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e828607ef160b4f27c81fb9e3776cafac72c08472e43710cc4d381257f85c1dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704436daed79ffc232792ce367de3ddfa0b1a746d5799132ea4f7177c02d0c15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1fa25118a929890518bfb6849ab2051731bcebc98e958a7ed831578ee730bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2471c28b1fb1f56cfb287e6cc2b559419c09ffbbf4168feb891a7d744f4b4c8b(
    value: typing.Optional[CloudAwsGovcloudIntegrationsRds],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa2b6446a47775bf06d1ab2e3297d98c0b74f935b010b9514b584fde9915417(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30052ea8e0aa4ce770ec67d05ed97c9f7e9135fc2e747a2539b5cbb4ec64b0c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678d0ce030f8e388c20405a5151513a52d8a7353d20fd49378d16ac803d13473(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96642c1b38786135054a595c465a051dbdd5267685ab67983181242e1f3252b1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348731a53875cabe3fc23e251483183dd17003f6d42471ae1271d14ce7e246f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7edfe4d83c16ab69a8f94c0fe9779a89407db53698e85f46916f8beafcd3c764(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc8bf1d4dc66257e683aa11f017fae9f0ceef8ff1c0ea4e5767a09629798338(
    value: typing.Optional[CloudAwsGovcloudIntegrationsRedShift],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc423df6bc44af0ccea6175c05059961391289e8484072d7c12b6e18f4dd4686(
    *,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f6eb6867adb72e687741c0b04b41fd7aa6049489ecb4a13910879be7b216f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4279c30d6255b53a194b6cfa722deec9ee94ff84f64db0123f839549c2c805b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef15d635ade457ead4f5070ce01ac80caeb153c9cf962728686db9b028b79a57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da10936b1fbf34d8637633e1ea44c87ed03f4f78d55cf88b8b1be253e774f88(
    value: typing.Optional[CloudAwsGovcloudIntegrationsRoute53],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46eeaedf0b60d122318da800106206618796d5633405d6fa32948d46adf77df3(
    *,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72411924004368c43d1afe1843f56cac2baf5e108fd1aa315361b535544edc59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7baee762c815a1cbc216d98d190c4ab63169ed1724f53623de51ae19dad672e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0707748e83342ad189e44c79cf7f42b158f4bdaf49a17877cf86a009b90f48bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6cf65c7c785b459084bdca660853e2823b3e99cfe279d77f400babdb6a57cd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85bedd4e5fbaf17fa1fe71d43eaba1392b8892110876f84f065eb0bededc6473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f659157dfa39b36003f49576d69c31caa7e58dba545db945f41c6fa588e442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ba623284c81f8e81ebe3ac1ced7444006bc39560606027b09570992fe8f6b5(
    value: typing.Optional[CloudAwsGovcloudIntegrationsS3],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0a8d81b32ee67703acdff645ba65cdd045ffa23fa1bfe2739a995e728ee1ba(
    *,
    aws_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    fetch_extended_inventory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844febf0bac41b3e47156c99bc68bb295d583c372b250aa851645b7814f17e9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4c7e7e6c8e586f5ce339a2d2cee32e124eb478b074a886574f6a9f92a6e732(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa8d4c2c65d8f09022ecb662b36738d55fca321ce11f30a23e7c2bcafb29a33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4882e8f091b655bf6b7de5ebed71c77f014a1d638042e22a750d8ea4a3a37b50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d9144c0d72826b52abac0982099a403a81b898d2733ea7fc675a7706a89764(
    value: typing.Optional[CloudAwsGovcloudIntegrationsSns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68cae4d216a7702a7cbdc5367425e888b8454c9db2a0f47cf1aaa33c08380bf8(
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

def _typecheckingstub__cf90dfc825b01e346b77e39984160b288e690317a0a7893c5aa8fac80bfa4ad0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea99ebe1553bd30cf0351fd7874442c7d708c5b214114285d0ef82af7cc58d39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9b677c4fe053ebc7a800e5505df89900ae676de1b0cda1247ffeb7652431d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e90d71d8fd2a8bf9c2d6aa14ba45b5b77b92c27aa33d38b574b34ca40982273(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818c9e6b7d471539328b96bb9fbe8641a7bd763e9fc076bf7310c9558e5a3e45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6044511a0eeb759003a1f86a17da51e2740c7388fc94d04bfe859f029f0ed8b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860bc61c08d69419017d02ace269d2f790a5c5af209282a9ab35ef4094ef47fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92269292809b26431010a46e4f186735ed48a1cfb15a16092c0722aed8c42ef0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72a7c57c2dae935fa4a3192a7c91af5b6d96087ecede5c2e3a7cacf879987ad(
    value: typing.Optional[CloudAwsGovcloudIntegrationsSqs],
) -> None:
    """Type checking stubs"""
    pass
