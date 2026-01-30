r'''
[![NPM version](https://badge.fury.io/js/cdk-common.svg)](https://badge.fury.io/js/cdk-common)
[![PyPI version](https://badge.fury.io/py/cdk-common.svg)](https://badge.fury.io/py/cdk-common)
[![release](https://github.com/neilkuan/cdk-common/actions/workflows/release.yml/badge.svg)](https://github.com/neilkuan/cdk-common/actions/workflows/release.yml)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-common?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-common?label=pypi&color=blue)

# Welcome to `cdk-common`

This Constructs Library will collection of useful `function` and `class` for AWS CDK.

## Install

```bash
Use the npm dist tag to opt in CDKv1 or CDKv2:

// for CDKv2
npm install cdk-common
```

### AWS Managed Policies `enum`

```python
import * as cdk from 'aws-cdk-lib';
import { AWSManagedPolicies } from 'cdk-common';
import { Construct } from 'constructs';
const app = new cdk.App();

const stack = new cdk.Stack(app, 'integ-default', { env });

export class IntegDefault extends Construct {
  constructor(scope: Construct, id: string ) {
    super(scope, id);

    const role = new iam.Role(this, 'iamrole', {
      assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com'),
    });
    // Use this way.
    role.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName(AWSManagedPolicies.AMAZON_SSM_MANAGED_INSTANCE_CORE));

    // Not this way.
    role.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'));
  }
}
```
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_codeguruprofiler as _aws_cdk_aws_codeguruprofiler_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="cdk-common.AWSManagedPolicies")
class AWSManagedPolicies(enum.Enum):
    '''
    :stability: experimental
    '''

    ADMINISTRATOR_ACCESS = "ADMINISTRATOR_ACCESS"
    '''
    :stability: experimental
    '''
    POWER_USER_ACCESS = "POWER_USER_ACCESS"
    '''
    :stability: experimental
    '''
    READ_ONLY_ACCESS = "READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLOUD_FORMATION_READ_ONLY_ACCESS = "AWSCLOUD_FORMATION_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_FRONT_FULL_ACCESS = "CLOUD_FRONT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLOUD_HSM_FULL_ACCESS = "AWSCLOUD_HSM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLOUD_HSM_READ_ONLY_ACCESS = "AWSCLOUD_HSM_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    RESOURCE_GROUPSAND_TAG_EDITOR_FULL_ACCESS = "RESOURCE_GROUPSAND_TAG_EDITOR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    RESOURCE_GROUPSAND_TAG_EDITOR_READ_ONLY_ACCESS = "RESOURCE_GROUPSAND_TAG_EDITOR_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_FRONT_READ_ONLY_ACCESS = "CLOUD_FRONT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_SEARCH_FULL_ACCESS = "CLOUD_SEARCH_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_SEARCH_READ_ONLY_ACCESS = "CLOUD_SEARCH_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_FULL_ACCESS = "CLOUD_WATCH_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_READ_ONLY_ACCESS = "CLOUD_WATCH_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_LOGS_FULL_ACCESS = "CLOUD_WATCH_LOGS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_LOGS_READ_ONLY_ACCESS = "CLOUD_WATCH_LOGS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDIRECT_CONNECT_FULL_ACCESS = "AWSDIRECT_CONNECT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDIRECT_CONNECT_READ_ONLY_ACCESS = "AWSDIRECT_CONNECT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_APP_STREAM_FULL_ACCESS = "AMAZON_APP_STREAM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_APP_STREAM_READ_ONLY_ACCESS = "AMAZON_APP_STREAM_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DYNAMO_DB_FULL_ACCESS = "AMAZON_DYNAMO_DB_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DYNAMO_DB_READ_ONLY_ACCESS = "AMAZON_DYNAMO_DB_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DYNAMO_DB_FULL_ACCESSWITH_DATA_PIPELINE = "AMAZON_DYNAMO_DB_FULL_ACCESSWITH_DATA_PIPELINE"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_FULL_ACCESS = "AMAZON_E_C2_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_READ_ONLY_ACCESS = "AMAZON_E_C2_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTI_CACHE_FULL_ACCESS = "AMAZON_ELASTI_CACHE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTI_CACHE_READ_ONLY_ACCESS = "AMAZON_ELASTI_CACHE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_MAP_REDUCE_FULL_ACCESS = "AMAZON_ELASTIC_MAP_REDUCE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_MAP_REDUCE_READ_ONLY_ACCESS = "AMAZON_ELASTIC_MAP_REDUCE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_GLACIER_READ_ONLY_ACCESS = "AMAZON_GLACIER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_GLACIER_FULL_ACCESS = "AMAZON_GLACIER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_KINESIS_FULL_ACCESS = "AMAZON_KINESIS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_KINESIS_READ_ONLY_ACCESS = "AMAZON_KINESIS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACEREAD_ONLY = "AWSMARKETPLACEREAD_ONLY"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_MANAGE_SUBSCRIPTIONS = "AWSMARKETPLACE_MANAGE_SUBSCRIPTIONS"
    '''
    :stability: experimental
    '''
    AMAZON_MOBILE_ANALYTICS_FULL_ACCESS = "AMAZON_MOBILE_ANALYTICS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MOBILE_ANALYTICS_FINANCIAL_REPORT_ACCESS = "AMAZON_MOBILE_ANALYTICS_FINANCIAL_REPORT_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZONMOBILEANALYTICSNON_FINANCIALREPORTACCESS = "AMAZONMOBILEANALYTICSNON_FINANCIALREPORTACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MOBILE_ANALYTICS_WRITE_ONLY_ACCESS = "AMAZON_MOBILE_ANALYTICS_WRITE_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    IAMFULL_ACCESS = "IAMFULL_ACCESS"
    '''
    :stability: experimental
    '''
    IAMREAD_ONLY_ACCESS = "IAMREAD_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSKEY_MANAGEMENT_SERVICE_POWER_USER = "AWSKEY_MANAGEMENT_SERVICE_POWER_USER"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_MAIL_FULL_ACCESS = "AMAZON_WORK_MAIL_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_MAIL_READ_ONLY_ACCESS = "AMAZON_WORK_MAIL_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIMPORT_EXPORT_READ_ONLY_ACCESS = "AWSIMPORT_EXPORT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIMPORT_EXPORT_FULL_ACCESS = "AWSIMPORT_EXPORT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_EXECUTE = "AWSLAMBDA_EXECUTE"
    '''
    :stability: experimental
    '''
    AWSLAMBDAINVOCATION_DYNAMODB = "AWSLAMBDAINVOCATION_DYNAMODB"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_FULL_ACCESS = "AMAZON_REDSHIFT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_READ_ONLY_ACCESS = "AMAZON_REDSHIFT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_FULL_ACCESS = "AMAZON_RDS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_READ_ONLY_ACCESS = "AMAZON_RDS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_FULL_ACCESS = "AMAZON_ROUTE53_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_READ_ONLY_ACCESS = "AMAZON_ROUTE53_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_DOMAINS_FULL_ACCESS = "AMAZON_ROUTE53_DOMAINS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_DOMAINS_READ_ONLY_ACCESS = "AMAZON_ROUTE53_DOMAINS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_S3_FULL_ACCESS = "AMAZON_S3_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_S3_READ_ONLY_ACCESS = "AMAZON_S3_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    SECURITY_AUDIT = "SECURITY_AUDIT"
    '''
    :stability: experimental
    '''
    AMAZON_SES_FULL_ACCESS = "AMAZON_SES_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SES_READ_ONLY_ACCESS = "AMAZON_SES_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    SIMPLE_WORKFLOW_FULL_ACCESS = "SIMPLE_WORKFLOW_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SNS_FULL_ACCESS = "AMAZON_SNS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SNS_READ_ONLY_ACCESS = "AMAZON_SNS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SQS_FULL_ACCESS = "AMAZON_SQS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SQS_READ_ONLY_ACCESS = "AMAZON_SQS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSTORAGE_GATEWAY_FULL_ACCESS = "AWSSTORAGE_GATEWAY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSTORAGE_GATEWAY_READ_ONLY_ACCESS = "AWSSTORAGE_GATEWAY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSUPPORT_ACCESS = "AWSSUPPORT_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDIRECTORY_SERVICE_FULL_ACCESS = "AWSDIRECTORY_SERVICE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDIRECTORY_SERVICE_READ_ONLY_ACCESS = "AWSDIRECTORY_SERVICE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ZOCALO_FULL_ACCESS = "AMAZON_ZOCALO_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ZOCALO_READ_ONLY_ACCESS = "AMAZON_ZOCALO_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_VPC_FULL_ACCESS = "AMAZON_VPC_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_VPC_READ_ONLY_ACCESS = "AMAZON_VPC_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSACCOUNT_ACTIVITY_ACCESS = "AWSACCOUNT_ACTIVITY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSACCOUNT_USAGE_REPORT_ACCESS = "AWSACCOUNT_USAGE_REPORT_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_MAP_REDUCE_ROLE = "AMAZON_ELASTIC_MAP_REDUCE_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_MAP_REDUCEFOR_E_C2_ROLE = "AMAZON_ELASTIC_MAP_REDUCEFOR_E_C2_ROLE"
    '''
    :stability: experimental
    '''
    AUTO_SCALING_NOTIFICATION_ACCESS_ROLE = "AUTO_SCALING_NOTIFICATION_ACCESS_ROLE"
    '''
    :stability: experimental
    '''
    AWSCLOUD_HSM_ROLE = "AWSCLOUD_HSM_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_ROLEFOR_DATA_PIPELINE_ROLE = "AMAZON_E_C2_ROLEFOR_DATA_PIPELINE_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_TRANSCODER_ROLE = "AMAZON_ELASTIC_TRANSCODER_ROLE"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_ROLE = "AWSLAMBDA_ROLE"
    '''
    :stability: experimental
    '''
    RDSCLOUD_HSM_AUTHORIZATION_ROLE = "RDSCLOUD_HSM_AUTHORIZATION_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_SNS_ROLE = "AMAZON_SNS_ROLE"
    '''
    :stability: experimental
    '''
    AWSCONNECTOR = "AWSCONNECTOR"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_FULL_ACCESS = "AWSMARKETPLACE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCONFIG_USER_ACCESS = "AWSCONFIG_USER_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_CONTAINER_SERVICEFOR_E_C2_ROLE = "AMAZON_E_C2_CONTAINER_SERVICEFOR_E_C2_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_COGNITO_READ_ONLY = "AMAZON_COGNITO_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_COGNITO_POWER_USER = "AMAZON_COGNITO_POWER_USER"
    '''
    :stability: experimental
    '''
    AMAZON_COGNITO_DEVELOPER_AUTHENTICATED_IDENTITIES = "AMAZON_COGNITO_DEVELOPER_AUTHENTICATED_IDENTITIES"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_APPLICATION_MANAGER_ADMIN_ACCESS = "AMAZON_WORK_SPACES_APPLICATION_MANAGER_ADMIN_ACCESS"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_BASIC_EXECUTION_ROLE = "AWSLAMBDA_BASIC_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_DYNAMO_DB_EXECUTION_ROLE = "AWSLAMBDA_DYNAMO_DB_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_KINESIS_EXECUTION_ROLE = "AWSLAMBDA_KINESIS_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_CONTAINER_SERVICE_ROLE = "AMAZON_E_C2_CONTAINER_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_MACHINE_LEARNING_BATCH_PREDICTIONS_ACCESS = "AMAZON_MACHINE_LEARNING_BATCH_PREDICTIONS_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MACHINE_LEARNING_CREATE_ONLY_ACCESS = "AMAZON_MACHINE_LEARNING_CREATE_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MACHINE_LEARNING_FULL_ACCESS = "AMAZON_MACHINE_LEARNING_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MACHINE_LEARNING_MANAGE_REAL_TIME_ENDPOINT_ONLY_ACCESS = "AMAZON_MACHINE_LEARNING_MANAGE_REAL_TIME_ENDPOINT_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MACHINE_LEARNING_READ_ONLY_ACCESS = "AMAZON_MACHINE_LEARNING_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MACHINE_LEARNING_REAL_TIME_PREDICTION_ONLY_ACCESS = "AMAZON_MACHINE_LEARNING_REAL_TIME_PREDICTION_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_ROLE = "AWSCODE_DEPLOY_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_ROLEFOR_AWS_CODE_DEPLOY = "AMAZON_E_C2_ROLEFOR_AWS_CODE_DEPLOY"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_FULL_ACCESS = "AWSCODE_DEPLOY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_DEPLOYER_ACCESS = "AWSCODE_DEPLOY_DEPLOYER_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_READ_ONLY_ACCESS = "AWSCODE_DEPLOY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_FILE_SYSTEM_FULL_ACCESS = "AMAZON_ELASTIC_FILE_SYSTEM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_FILE_SYSTEM_READ_ONLY_ACCESS = "AMAZON_ELASTIC_FILE_SYSTEM_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_FULL_ACCESS = "AMAZON_SSM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_READ_ONLY_ACCESS = "AMAZON_SSM_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_ROLEFOR_SS_M = "AMAZON_E_C2_ROLEFOR_SS_M"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_ACTIONS_E_C2_ACCESS = "CLOUD_WATCH_ACTIONS_E_C2_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_PIPELINE_CUSTOM_ACTION_ACCESS = "AWSCODE_PIPELINE_CUSTOM_ACTION_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_COMMIT_FULL_ACCESS = "AWSCODE_COMMIT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_COMMIT_READ_ONLY = "AWSCODE_COMMIT_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSCODE_COMMIT_POWER_USER = "AWSCODE_COMMIT_POWER_USER"
    '''
    :stability: experimental
    '''
    IAMUSER_SSH_KEYS = "IAMUSER_SSH_KEYS"
    '''
    :stability: experimental
    '''
    AMAZON_API_GATEWAY_ADMINISTRATOR = "AMAZON_API_GATEWAY_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    AMAZON_API_GATEWAY_INVOKE_FULL_ACCESS = "AMAZON_API_GATEWAY_INVOKE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDEVICE_FARM_FULL_ACCESS = "AWSDEVICE_FARM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DRSVPC_MANAGEMENT = "AMAZON_DRSVPC_MANAGEMENT"
    '''
    :stability: experimental
    '''
    VMIMPORT_EXPORT_ROLE_FOR_AWS_CONNECTOR = "VMIMPORT_EXPORT_ROLE_FOR_AWS_CONNECTOR"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_ADMIN = "AMAZON_WORK_SPACES_ADMIN"
    '''
    :stability: experimental
    '''
    AMAZON_ES_FULL_ACCESS = "AMAZON_ES_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ES_READ_ONLY_ACCESS = "AMAZON_ES_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSWAFREAD_ONLY_ACCESS = "AWSWAFREAD_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSWAFFULL_ACCESS = "AWSWAFFULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_INSPECTOR_READ_ONLY_ACCESS = "AMAZON_INSPECTOR_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_INSPECTOR_FULL_ACCESS = "AMAZON_INSPECTOR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_KINESIS_FIREHOSE_READ_ONLY_ACCESS = "AMAZON_KINESIS_FIREHOSE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_KINESIS_FIREHOSE_FULL_ACCESS = "AMAZON_KINESIS_FIREHOSE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_RULE_ACTIONS = "AWSIO_T_RULE_ACTIONS"
    '''
    :stability: experimental
    '''
    AWSIO_T_LOGGING = "AWSIO_T_LOGGING"
    '''
    :stability: experimental
    '''
    AWSIO_T_FULL_ACCESS = "AWSIO_T_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_DATA_ACCESS = "AWSIO_T_DATA_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_CONFIG_ACCESS = "AWSIO_T_CONFIG_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_CONFIG_READ_ONLY_ACCESS = "AWSIO_T_CONFIG_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_DESCRIBE_RD_S = "AWSQUICK_SIGHT_DESCRIBE_RD_S"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_DESCRIBE_REDSHIFT = "AWSQUICK_SIGHT_DESCRIBE_REDSHIFT"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_LIST_IA_M = "AWSQUICK_SIGHT_LIST_IA_M"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_ENHANCED_MONITORING_ROLE = "AMAZON_RDS_ENHANCED_MONITORING_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_API_GATEWAY_PUSH_TO_CLOUD_WATCH_LOGS = "AMAZON_API_GATEWAY_PUSH_TO_CLOUD_WATCH_LOGS"
    '''
    :stability: experimental
    '''
    AMAZON_DMSVPC_MANAGEMENT_ROLE = "AMAZON_DMSVPC_MANAGEMENT_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_MECHANICAL_TURK_FULL_ACCESS = "AMAZON_MECHANICAL_TURK_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MECHANICAL_TURK_READ_ONLY = "AMAZON_MECHANICAL_TURK_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_CONTAINER_REGISTRY_READ_ONLY = "AMAZON_E_C2_CONTAINER_REGISTRY_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_CONTAINER_REGISTRY_POWER_USER = "AMAZON_E_C2_CONTAINER_REGISTRY_POWER_USER"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_CONTAINER_REGISTRY_FULL_ACCESS = "AMAZON_E_C2_CONTAINER_REGISTRY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DMS_CLOUD_WATCH_LOGS_ROLE = "AMAZON_DMS_CLOUD_WATCH_LOGS_ROLE"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_EVENTS_READ_ONLY_ACCESS = "CLOUD_WATCH_EVENTS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_EVENTS_BUILT_IN_TARGET_EXECUTION_ACCESS = "CLOUD_WATCH_EVENTS_BUILT_IN_TARGET_EXECUTION_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_EVENTS_INVOCATION_ACCESS = "CLOUD_WATCH_EVENTS_INVOCATION_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_EVENTS_FULL_ACCESS = "CLOUD_WATCH_EVENTS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCERTIFICATE_MANAGER_FULL_ACCESS = "AWSCERTIFICATE_MANAGER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCERTIFICATE_MANAGER_READ_ONLY = "AWSCERTIFICATE_MANAGER_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_WEB_TIER = "AWSELASTIC_BEANSTALK_WEB_TIER"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_WORKER_TIER = "AWSELASTIC_BEANSTALK_WORKER_TIER"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_MULTICONTAINER_DOCKER = "AWSELASTIC_BEANSTALK_MULTICONTAINER_DOCKER"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_ENHANCED_HEALTH = "AWSELASTIC_BEANSTALK_ENHANCED_HEALTH"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_VPC_ACCESS_EXECUTION_ROLE = "AWSLAMBDA_VPC_ACCESS_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_DIRECTORY_SERVICE_ACCESS = "AMAZON_RDS_DIRECTORY_SERVICE_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_METERING_FULL_ACCESS = "AWSMARKETPLACE_METERING_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCONFIG_RULES_EXECUTION_ROLE = "AWSCONFIG_RULES_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_SERVICE = "AWSELASTIC_BEANSTALK_SERVICE"
    '''
    :stability: experimental
    '''
    AMAZON_DMS_REDSHIFT_S3_ROLE = "AMAZON_DMS_REDSHIFT_S3_ROLE"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_DISCOVERY_SERVICE_FULL_ACCESS = "AWSAPPLICATION_DISCOVERY_SERVICE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_DISCOVERY_AGENT_ACCESS = "AWSAPPLICATION_DISCOVERY_AGENT_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_CONTAINER_SERVICE_AUTOSCALE_ROLE = "AMAZON_E_C2_CONTAINER_SERVICE_AUTOSCALE_ROLE"
    '''
    :stability: experimental
    '''
    AWSCODE_PIPELINE_APPROVER_ACCESS = "AWSCODE_PIPELINE_APPROVER_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAGENTLESS_DISCOVERY_SERVICE = "AWSAGENTLESS_DISCOVERY_SERVICE"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_SPOT_FLEET_AUTOSCALE_ROLE = "AMAZON_E_C2_SPOT_FLEET_AUTOSCALE_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_KINESIS_ANALYTICS_READ_ONLY = "AMAZON_KINESIS_ANALYTICS_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_KINESIS_ANALYTICS_FULL_ACCESS = "AMAZON_KINESIS_ANALYTICS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    SERVER_MIGRATION_CONNECTOR = "SERVER_MIGRATION_CONNECTOR"
    '''
    :stability: experimental
    '''
    VIEW_ONLY_ACCESS = "VIEW_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    SUPPORT_USER = "SUPPORT_USER"
    '''
    :stability: experimental
    '''
    SYSTEM_ADMINISTRATOR = "SYSTEM_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    DATABASE_ADMINISTRATOR = "DATABASE_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    DATA_SCIENTIST = "DATA_SCIENTIST"
    '''
    :stability: experimental
    '''
    NETWORK_ADMINISTRATOR = "NETWORK_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    BILLING = "BILLING"
    '''
    :stability: experimental
    '''
    IAMUSER_CHANGE_PASSWORD = "IAMUSER_CHANGE_PASSWORD"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_MAP_REDUCEFOR_AUTO_SCALING_ROLE = "AMAZON_ELASTIC_MAP_REDUCEFOR_AUTO_SCALING_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_APP_STREAM_SERVICE_ACCESS = "AMAZON_APP_STREAM_SERVICE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_REKOGNITION_FULL_ACCESS = "AMAZON_REKOGNITION_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_REKOGNITION_READ_ONLY_ACCESS = "AMAZON_REKOGNITION_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ATHENA_FULL_ACCESS = "AMAZON_ATHENA_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_POLLY_FULL_ACCESS = "AMAZON_POLLY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_POLLY_READ_ONLY_ACCESS = "AMAZON_POLLY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_MAINTENANCE_WINDOW_ROLE = "AMAZON_SSM_MAINTENANCE_WINDOW_ROLE"
    '''
    :stability: experimental
    '''
    AWSXRAY_WRITE_ONLY_ACCESS = "AWSXRAY_WRITE_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSXRAY_READ_ONLY_ACCESS = "AWSXRAY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSXRAY_FULL_ACCESS = "AWSXRAY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_BUILD_DEVELOPER_ACCESS = "AWSCODE_BUILD_DEVELOPER_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_BUILD_READ_ONLY_ACCESS = "AWSCODE_BUILD_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_BUILD_ADMIN_ACCESS = "AWSCODE_BUILD_ADMIN_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_AUTOMATION_ROLE = "AMAZON_SSM_AUTOMATION_ROLE"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_ENI_MANAGEMENT_ACCESS = "AWSLAMBDA_ENI_MANAGEMENT_ACCESS"
    '''
    :stability: experimental
    '''
    AWSHEALTH_FULL_ACCESS = "AWSHEALTH_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBATCH_FULL_ACCESS = "AWSBATCH_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBATCH_SERVICE_ROLE = "AWSBATCH_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AWSQUICKSIGHT_ATHENA_ACCESS = "AWSQUICKSIGHT_ATHENA_ACCESS"
    '''
    :stability: experimental
    '''
    IAMSELF_MANAGE_SERVICE_SPECIFIC_CREDENTIALS = "IAMSELF_MANAGE_SERVICE_SPECIFIC_CREDENTIALS"
    '''
    :stability: experimental
    '''
    AWSSTEP_FUNCTIONS_READ_ONLY_ACCESS = "AWSSTEP_FUNCTIONS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSTEP_FUNCTIONS_FULL_ACCESS = "AWSSTEP_FUNCTIONS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSTEP_FUNCTIONS_CONSOLE_FULL_ACCESS = "AWSSTEP_FUNCTIONS_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AUTO_SCALING_FULL_ACCESS = "AUTO_SCALING_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AUTO_SCALING_READ_ONLY_ACCESS = "AUTO_SCALING_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AUTO_SCALING_CONSOLE_FULL_ACCESS = "AUTO_SCALING_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AUTO_SCALING_CONSOLE_READ_ONLY_ACCESS = "AUTO_SCALING_CONSOLE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATAPIPELINE_FULLACCESS = "AWSDATAPIPELINE_FULLACCESS"
    '''
    :stability: experimental
    '''
    AWSDATAPIPELINE_POWERUSER = "AWSDATAPIPELINE_POWERUSER"
    '''
    :stability: experimental
    '''
    APPLICATION_AUTO_SCALING_FOR_AMAZON_APP_STREAM_ACCESS = "APPLICATION_AUTO_SCALING_FOR_AMAZON_APP_STREAM_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGREENGRASS_RESOURCE_ACCESS_ROLE_POLICY = "AWSGREENGRASS_RESOURCE_ACCESS_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_CUSTOM_PLATFORMFOR_E_C2_ROLE = "AWSELASTIC_BEANSTALK_CUSTOM_PLATFORMFOR_E_C2_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_CLOUD_DIRECTORY_FULL_ACCESS = "AMAZON_CLOUD_DIRECTORY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CLOUD_DIRECTORY_READ_ONLY_ACCESS = "AMAZON_CLOUD_DIRECTORY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_GET_ENTITLEMENTS = "AWSMARKETPLACE_GET_ENTITLEMENTS"
    '''
    :stability: experimental
    '''
    AMAZON_LEX_RUN_BOTS_ONLY = "AMAZON_LEX_RUN_BOTS_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_LEX_READ_ONLY = "AMAZON_LEX_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_LEX_FULL_ACCESS = "AMAZON_LEX_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_STAR_SERVICE_ROLE = "AWSCODE_STAR_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AWSCODE_STAR_FULL_ACCESS = "AWSCODE_STAR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGREENGRASS_FULL_ACCESS = "AWSGREENGRASS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_CONTAINER_SERVICE_EVENTS_ROLE = "AMAZON_E_C2_CONTAINER_SERVICE_EVENTS_ROLE"
    '''
    :stability: experimental
    '''
    QUICK_SIGHT_ACCESS_FOR_S3_STORAGE_MANAGEMENT_ANALYTICS_READ_ONLY = "QUICK_SIGHT_ACCESS_FOR_S3_STORAGE_MANAGEMENT_ANALYTICS_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_SPOT_FLEET_TAGGING_ROLE = "AMAZON_E_C2_SPOT_FLEET_TAGGING_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTICSEARCH_SERVICE_ROLE_POLICY = "AMAZON_ELASTICSEARCH_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_VPC_CROSS_ACCOUNT_NETWORK_INTERFACE_OPERATIONS = "AMAZON_VPC_CROSS_ACCOUNT_NETWORK_INTERFACE_OPERATIONS"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_AUTOMATION_APPROVER_ACCESS = "AMAZON_SSM_AUTOMATION_APPROVER_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_DISCOVERY_ACCESS = "AWSMIGRATION_HUB_DISCOVERY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGLUE_SERVICE_ROLE = "AWSGLUE_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AWSGLUE_CONSOLE_FULL_ACCESS = "AWSGLUE_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGLUE_SERVICE_NOTEBOOK_ROLE = "AWSGLUE_SERVICE_NOTEBOOK_ROLE"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_SMS_ACCESS = "AWSMIGRATION_HUB_SMS_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_DMS_ACCESS = "AWSMIGRATION_HUB_DMS_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_FULL_ACCESS = "AWSMIGRATION_HUB_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MACIE_SERVICE_ROLE = "AMAZON_MACIE_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_MACIE_FULL_ACCESS = "AMAZON_MACIE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_SERVICE_ROLE_POLICY = "AWSELASTIC_BEANSTALK_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSEC2_SPOT_SERVICE_ROLE_POLICY = "AWSEC2_SPOT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_SERVICE_LINKED_ROLE_POLICY = "AMAZON_REDSHIFT_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_LOAD_BALANCING_SERVICE_ROLE_POLICY = "AWSELASTIC_LOAD_BALANCING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_LOAD_BALANCING_CLASSIC_SERVICE_ROLE_POLICY = "AWSELASTIC_LOAD_BALANCING_CLASSIC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSENHANCED_CLASSIC_NETWORKING_MANGEMENT_POLICY = "AWSENHANCED_CLASSIC_NETWORKING_MANGEMENT_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EMR_CLEANUP_POLICY = "AMAZON_EMR_CLEANUP_POLICY"
    '''
    :stability: experimental
    '''
    LEX_CHANNEL_POLICY = "LEX_CHANNEL_POLICY"
    '''
    :stability: experimental
    '''
    LEX_BOT_POLICY = "LEX_BOT_POLICY"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_REPLICATOR = "AWSLAMBDA_REPLICATOR"
    '''
    :stability: experimental
    '''
    AWSORGANIZATIONS_SERVICE_TRUST_POLICY = "AWSORGANIZATIONS_SERVICE_TRUST_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_E_C2_SCHEDULED_INSTANCES = "AWSSERVICE_ROLE_FOR_E_C2_SCHEDULED_INSTANCES"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_SERVICE_ROLE_POLICY = "AMAZON_ECS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_RDS_CLUSTER_POLICY = "AWSAPPLICATION_AUTOSCALING_RDS_CLUSTER_POLICY"
    '''
    :stability: experimental
    '''
    APIGATEWAY_SERVICE_ROLE_POLICY = "APIGATEWAY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_APP_STREAM_FLEET_POLICY = "AWSAPPLICATION_AUTOSCALING_APP_STREAM_FLEET_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_DYNAMO_DB_TABLE_POLICY = "AWSAPPLICATION_AUTOSCALING_DYNAMO_DB_TABLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSEC2_SPOT_FLEET_SERVICE_ROLE_POLICY = "AWSEC2_SPOT_FLEET_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_E_C2_SPOT_FLEET_REQUEST_POLICY = "AWSAPPLICATION_AUTOSCALING_E_C2_SPOT_FLEET_REQUEST_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_ECS_SERVICE_POLICY = "AWSAPPLICATION_AUTOSCALING_ECS_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_EMR_INSTANCE_GROUP_POLICY = "AWSAPPLICATION_AUTOSCALING_EMR_INSTANCE_GROUP_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_READ_ONLY = "AMAZON_CHIME_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_FULL_ACCESS = "AMAZON_CHIME_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_USER_MANAGEMENT = "AMAZON_CHIME_USER_MANAGEMENT"
    '''
    :stability: experimental
    '''
    CLOUD_HSM_SERVICE_ROLE_POLICY = "CLOUD_HSM_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZONECS_FULLACCESS = "AMAZONECS_FULLACCESS"
    '''
    :stability: experimental
    '''
    DYNAMO_DB_REPLICATION_SERVICE_ROLE_POLICY = "DYNAMO_DB_REPLICATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_SERVICE_ROLE_POLICY = "AMAZON_SSM_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_TASK_EXECUTION_ROLE_POLICY = "AMAZON_ECS_TASK_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_EVENTS_SERVICE_ROLE_POLICY = "CLOUD_WATCH_EVENTS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_INSPECTOR_SERVICE_ROLE_POLICY = "AMAZON_INSPECTOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPRICE_LIST_SERVICE_FULL_ACCESS = "AWSPRICE_LIST_SERVICE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_ROLE_FOR_LAMBDA = "AWSCODE_DEPLOY_ROLE_FOR_LAMBDA"
    '''
    :stability: experimental
    '''
    AMAZON_MQ_FULL_ACCESS = "AMAZON_MQ_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MQ_READ_ONLY_ACCESS = "AMAZON_MQ_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_GUARD_DUTY_SERVICE_ROLE_POLICY = "AMAZON_GUARD_DUTY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_GUARD_DUTY_READ_ONLY_ACCESS = "AMAZON_GUARD_DUTY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_GUARD_DUTY_FULL_ACCESS = "AMAZON_GUARD_DUTY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_READ_ONLY = "AMAZON_SAGE_MAKER_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_FULL_ACCESS = "AMAZON_SAGE_MAKER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_FREE_RTOS_FULL_ACCESS = "AMAZON_FREE_RTOS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDEEP_LENS_SERVICE_ROLE_POLICY = "AWSDEEP_LENS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDEEP_LENS_LAMBDA_FUNCTION_ACCESS_POLICY = "AWSDEEP_LENS_LAMBDA_FUNCTION_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_REKOGNITION_SERVICE_ROLE = "AMAZON_REKOGNITION_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_IO_T_ANALYTICS_ACCESS = "AWSQUICK_SIGHT_IO_T_ANALYTICS_ACCESS"
    '''
    :stability: experimental
    '''
    COMPREHEND_FULL_ACCESS = "COMPREHEND_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    COMPREHEND_READ_ONLY = "COMPREHEND_READ_ONLY"
    '''
    :stability: experimental
    '''
    GREENGRASS_OTA_UPDATE_ARTIFACT_ACCESS = "GREENGRASS_OTA_UPDATE_ARTIFACT_ACCESS"
    '''
    :stability: experimental
    '''
    TRANSLATE_READ_ONLY = "TRANSLATE_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSCLOUD9_SERVICE_ROLE_POLICY = "AWSCLOUD9_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCLOUD9_USER = "AWSCLOUD9_USER"
    '''
    :stability: experimental
    '''
    AWSCLOUD9_ADMINISTRATOR = "AWSCLOUD9_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    AWSCLOUD9_ENVIRONMENT_MEMBER = "AWSCLOUD9_ENVIRONMENT_MEMBER"
    '''
    :stability: experimental
    '''
    ALEXA_FOR_BUSINESS_FULL_ACCESS = "ALEXA_FOR_BUSINESS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    ALEXA_FOR_BUSINESS_READ_ONLY_ACCESS = "ALEXA_FOR_BUSINESS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    ALEXA_FOR_BUSINESS_DEVICE_SETUP = "ALEXA_FOR_BUSINESS_DEVICE_SETUP"
    '''
    :stability: experimental
    '''
    ALEXA_FOR_BUSINESS_GATEWAY_EXECUTION = "ALEXA_FOR_BUSINESS_GATEWAY_EXECUTION"
    '''
    :stability: experimental
    '''
    AWSIO_T_THINGS_REGISTRATION = "AWSIO_T_THINGS_REGISTRATION"
    '''
    :stability: experimental
    '''
    AMAZON_KINESIS_VIDEO_STREAMS_READ_ONLY_ACCESS = "AMAZON_KINESIS_VIDEO_STREAMS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_KINESIS_VIDEO_STREAMS_FULL_ACCESS = "AMAZON_KINESIS_VIDEO_STREAMS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSSOSERVICE_ROLE_POLICY = "AWSSSOSERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    ELASTI_CACHE_SERVICE_ROLE_POLICY = "ELASTI_CACHE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSIO_TOTA_UPDATE = "AWSIO_TOTA_UPDATE"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_PACKAGE_FULL_ACCESS = "AWSELEMENTAL_MEDIA_PACKAGE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_PACKAGE_READ_ONLY = "AWSELEMENTAL_MEDIA_PACKAGE_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_SERVICE_ROLE_POLICY = "AMAZON_RDS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AUTO_SCALING_SERVICE_ROLE_POLICY = "AUTO_SCALING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_AUTO_NAMING_READ_ONLY_ACCESS = "AMAZON_ROUTE53_AUTO_NAMING_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_AUTO_NAMING_FULL_ACCESS = "AMAZON_ROUTE53_AUTO_NAMING_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_SAGE_MAKER_ENDPOINT_POLICY = "AWSAPPLICATION_AUTOSCALING_SAGE_MAKER_ENDPOINT_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_ADMIN_FULL_ACCESS = "AWSSERVICE_CATALOG_ADMIN_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_END_USER_FULL_ACCESS = "AWSSERVICE_CATALOG_END_USER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSTRUSTED_ADVISOR_SERVICE_ROLE_POLICY = "AWSTRUSTED_ADVISOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ES_COGNITO_ACCESS = "AMAZON_ES_COGNITO_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBATCH_SERVICE_EVENT_TARGET_ROLE = "AWSBATCH_SERVICE_EVENT_TARGET_ROLE"
    '''
    :stability: experimental
    '''
    DAXSERVICE_ROLE_POLICY = "DAXSERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_STORE_FULL_ACCESS = "AWSELEMENTAL_MEDIA_STORE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_AGENT_ADMIN_POLICY = "CLOUD_WATCH_AGENT_ADMIN_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_AGENT_SERVER_POLICY = "CLOUD_WATCH_AGENT_SERVER_POLICY"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_GROUPS_READ_ONLY_ACCESS = "AWSRESOURCE_GROUPS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_STORE_READ_ONLY = "AWSELEMENTAL_MEDIA_STORE_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_AUTO_NAMING_REGISTRANT_ACCESS = "AMAZON_ROUTE53_AUTO_NAMING_REGISTRANT_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCONFIG_ROLE_FOR_ORGANIZATIONS = "AWSCONFIG_ROLE_FOR_ORGANIZATIONS"
    '''
    :stability: experimental
    '''
    AWSAPP_SYNC_ADMINISTRATOR = "AWSAPP_SYNC_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    AWSAPP_SYNC_SCHEMA_AUTHOR = "AWSAPP_SYNC_SCHEMA_AUTHOR"
    '''
    :stability: experimental
    '''
    AWSAPP_SYNC_INVOKE_FULL_ACCESS = "AWSAPP_SYNC_INVOKE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSEC2_FLEET_SERVICE_ROLE_POLICY = "AWSEC2_FLEET_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    FMSSERVICE_ROLE_POLICY = "FMSSERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_TRANSCRIBE_READ_ONLY_ACCESS = "AMAZON_TRANSCRIBE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_TRANSCRIBE_FULL_ACCESS = "AMAZON_TRANSCRIBE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    SECRETS_MANAGER_READ_WRITE = "SECRETS_MANAGER_READ_WRITE"
    '''
    :stability: experimental
    '''
    AWSAPP_SYNC_PUSH_TO_CLOUD_WATCH_LOGS = "AWSAPP_SYNC_PUSH_TO_CLOUD_WATCH_LOGS"
    '''
    :stability: experimental
    '''
    AWSARTIFACT_ACCOUNT_SYNC = "AWSARTIFACT_ACCOUNT_SYNC"
    '''
    :stability: experimental
    '''
    AMAZONELASTICTRANSCODER_FULLACCESS = "AMAZONELASTICTRANSCODER_FULLACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_BETA_SERVICE_ROLE_POLICY = "AMAZON_RDS_BETA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSFMADMIN_FULL_ACCESS = "AWSFMADMIN_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSFMADMIN_READ_ONLY_ACCESS = "AWSFMADMIN_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSFMMEMBER_READ_ONLY_ACCESS = "AWSFMMEMBER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_CLUSTER_POLICY = "AMAZON_EKS_CLUSTER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZONEKS_CNI_POLICY = "AMAZONEKS_CNI_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_SERVICE_POLICY = "AMAZON_EKS_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_WORKER_NODE_POLICY = "AMAZON_EKS_WORKER_NODE_POLICY"
    '''
    :stability: experimental
    '''
    NEPTUNE_READ_ONLY_ACCESS = "NEPTUNE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    NEPTUNE_FULL_ACCESS = "NEPTUNE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCONFIG_SERVICE_ROLE_POLICY = "AWSCONFIG_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_PREVIEW_SERVICE_ROLE_POLICY = "AMAZON_RDS_PREVIEW_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTO_SCALING_CUSTOM_RESOURCE_POLICY = "AWSAPPLICATION_AUTO_SCALING_CUSTOM_RESOURCE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSHIELD_DRT_ACCESS_POLICY = "AWSSHIELD_DRT_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    AMAZONELASTICTRANSCODER_READONLYACCESS = "AMAZONELASTICTRANSCODER_READONLYACCESS"
    '''
    :stability: experimental
    '''
    AMAZONELASTICTRANSCODER_JOBSSUBMITTER = "AMAZONELASTICTRANSCODER_JOBSSUBMITTER"
    '''
    :stability: experimental
    '''
    AWSCLOUD_FRONT_LOGGER = "AWSCLOUD_FRONT_LOGGER"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_SQS_QUEUE_EXECUTION_ROLE = "AWSLAMBDA_SQS_QUEUE_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AWSIO_T_ANALYTICS_READ_ONLY_ACCESS = "AWSIO_T_ANALYTICS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_ANALYTICS_FULL_ACCESS = "AWSIO_T_ANALYTICS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    NEPTUNE_CONSOLE_FULL_ACCESS = "NEPTUNE_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MACIE_SERVICE_ROLE_POLICY = "AMAZON_MACIE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_CONVERT_READ_ONLY = "AWSELEMENTAL_MEDIA_CONVERT_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_CONVERT_FULL_ACCESS = "AWSELEMENTAL_MEDIA_CONVERT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSSOREAD_ONLY = "AWSSSOREAD_ONLY"
    '''
    :stability: experimental
    '''
    AWSSSOMASTER_ACCOUNT_ADMINISTRATOR = "AWSSSOMASTER_ACCOUNT_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    AWSSSOMEMBER_ACCOUNT_ADMINISTRATOR = "AWSSSOMEMBER_ACCOUNT_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    AMAZON_MACIE_HANDSHAKE_ROLE = "AMAZON_MACIE_HANDSHAKE_ROLE"
    '''
    :stability: experimental
    '''
    AWSDATA_LIFECYCLE_MANAGER_SERVICE_ROLE = "AWSDATA_LIFECYCLE_MANAGER_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_DEFENDER_AUDIT = "AWSIO_T_DEVICE_DEFENDER_AUDIT"
    '''
    :stability: experimental
    '''
    AWSDISCOVERY_CONTINUOUS_EXPORT_FIREHOSE_POLICY = "AWSDISCOVERY_CONTINUOUS_EXPORT_FIREHOSE_POLICY"
    '''
    :stability: experimental
    '''
    APPLICATION_DISCOVERY_SERVICE_CONTINUOUS_EXPORT_SERVICE_ROLE_POLICY = "APPLICATION_DISCOVERY_SERVICE_CONTINUOUS_EXPORT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAUTO_SCALING_PLANS_E_C2_AUTO_SCALING_POLICY = "AWSAUTO_SCALING_PLANS_E_C2_AUTO_SCALING_POLICY"
    '''
    :stability: experimental
    '''
    WAFREGIONAL_LOGGING_SERVICE_ROLE_POLICY = "WAFREGIONAL_LOGGING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    WAFLOGGING_SERVICE_ROLE_POLICY = "WAFLOGGING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_FREE_RTOSOTA_UPDATE = "AMAZON_FREE_RTOSOTA_UPDATE"
    '''
    :stability: experimental
    '''
    AWSXRAY_DAEMON_WRITE_ACCESS = "AWSXRAY_DAEMON_WRITE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CONNECT_SERVICE_LINKED_ROLE_POLICY = "AMAZON_CONNECT_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    ELASTIC_LOAD_BALANCING_READ_ONLY = "ELASTIC_LOAD_BALANCING_READ_ONLY"
    '''
    :stability: experimental
    '''
    ELASTIC_LOAD_BALANCING_FULL_ACCESS = "ELASTIC_LOAD_BALANCING_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    LIGHTSAIL_EXPORT_ACCESS = "LIGHTSAIL_EXPORT_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_QUERY_EDITOR = "AMAZON_REDSHIFT_QUERY_EDITOR"
    '''
    :stability: experimental
    '''
    AWSGLUE_CONSOLE_SAGE_MAKER_NOTEBOOK_FULL_ACCESS = "AWSGLUE_CONSOLE_SAGE_MAKER_NOTEBOOK_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CONNECT_READ_ONLY_ACCESS = "AMAZON_CONNECT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCERTIFICATE_MANAGER_PRIVATE_CA_AUDITOR = "AWSCERTIFICATE_MANAGER_PRIVATE_CA_AUDITOR"
    '''
    :stability: experimental
    '''
    AWSCERTIFICATE_MANAGER_PRIVATE_CA_USER = "AWSCERTIFICATE_MANAGER_PRIVATE_CA_USER"
    '''
    :stability: experimental
    '''
    AWSCERTIFICATE_MANAGER_PRIVATE_CA_FULL_ACCESS = "AWSCERTIFICATE_MANAGER_PRIVATE_CA_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCERTIFICATE_MANAGER_PRIVATE_CA_READ_ONLY = "AWSCERTIFICATE_MANAGER_PRIVATE_CA_READ_ONLY"
    '''
    :stability: experimental
    '''
    CLOUD_TRAIL_SERVICE_ROLE_POLICY = "CLOUD_TRAIL_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSGREENGRASS_READ_ONLY_ACCESS = "AWSGREENGRASS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSSODIRECTORY_READ_ONLY = "AWSSSODIRECTORY_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSSSODIRECTORY_ADMINISTRATOR = "AWSSSODIRECTORY_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    AWSORGANIZATIONS_FULL_ACCESS = "AWSORGANIZATIONS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSORGANIZATIONS_READ_ONLY_ACCESS = "AWSORGANIZATIONS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_IO_T_SITE_WISE = "AWSSERVICE_ROLE_FOR_IO_T_SITE_WISE"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_ACCESS_MANAGER_SERVICE_ROLE_POLICY = "AWSRESOURCE_ACCESS_MANAGER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSKEY_MANAGEMENT_SERVICE_CUSTOM_KEY_STORES_SERVICE_ROLE_POLICY = "AWSKEY_MANAGEMENT_SERVICE_CUSTOM_KEY_STORES_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    KAFKA_SERVICE_ROLE_POLICY = "KAFKA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_MAP_REDUCE_EDITORS_ROLE = "AMAZON_ELASTIC_MAP_REDUCE_EDITORS_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_DATA_FULL_ACCESS = "AMAZON_RDS_DATA_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSROBO_MAKER_READ_ONLY_ACCESS = "AWSROBO_MAKER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSROBO_MAKER_SERVICE_ROLE_POLICY = "AWSROBO_MAKER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSROBO_MAKER_SERVICE_POLICY = "AWSROBO_MAKER_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSVPCTRANSIT_GATEWAY_SERVICE_ROLE_POLICY = "AWSVPCTRANSIT_GATEWAY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSLICENSE_MANAGER_SERVICE_ROLE_POLICY = "AWSLICENSE_MANAGER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSLICENSE_MANAGER_MASTER_ACCOUNT_ROLE_POLICY = "AWSLICENSE_MANAGER_MASTER_ACCOUNT_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSLICENSE_MANAGER_MEMBER_ACCOUNT_ROLE_POLICY = "AWSLICENSE_MANAGER_MEMBER_ACCOUNT_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SERVER_MIGRATION_SERVICE_LAUNCH_ROLE = "SERVER_MIGRATION_SERVICE_LAUNCH_ROLE"
    '''
    :stability: experimental
    '''
    GLOBAL_ACCELERATOR_READ_ONLY_ACCESS = "GLOBAL_ACCELERATOR_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    GLOBAL_ACCELERATOR_FULL_ACCESS = "GLOBAL_ACCELERATOR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_MARKETPLACE_ADMIN_FULL_ACCESS = "AWSPRIVATE_MARKETPLACE_ADMIN_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    COMPREHEND_MEDICAL_FULL_ACCESS = "COMPREHEND_MEDICAL_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_ROLE_FOR_EC_S = "AWSCODE_DEPLOY_ROLE_FOR_EC_S"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_ROLE_FOR_ECS_LIMITED = "AWSCODE_DEPLOY_ROLE_FOR_ECS_LIMITED"
    '''
    :stability: experimental
    '''
    TRANSLATE_FULL_ACCESS = "TRANSLATE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSECURITY_HUB_SERVICE_ROLE_POLICY = "AWSSECURITY_HUB_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSECURITY_HUB_FULL_ACCESS = "AWSSECURITY_HUB_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSECURITY_HUB_READ_ONLY_ACCESS = "AWSSECURITY_HUB_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_F_SX_SERVICE_ROLE_POLICY = "AMAZON_F_SX_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    FSX_DELETE_SERVICE_LINKED_ROLE_ACCESS = "FSX_DELETE_SERVICE_LINKED_ROLE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_F_SX_READ_ONLY_ACCESS = "AMAZON_F_SX_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_F_SX_FULL_ACCESS = "AMAZON_F_SX_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_F_SX_CONSOLE_READ_ONLY_ACCESS = "AMAZON_F_SX_CONSOLE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_F_SX_CONSOLE_FULL_ACCESS = "AMAZON_F_SX_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_TEXTRACT_FULL_ACCESS = "AMAZON_TEXTRACT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_TEXTRACT_SERVICE_ROLE = "AMAZON_TEXTRACT_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AWSCLOUD_MAP_READ_ONLY_ACCESS = "AWSCLOUD_MAP_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLOUD_MAP_FULL_ACCESS = "AWSCLOUD_MAP_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLOUD_MAP_DISCOVER_INSTANCE_ACCESS = "AWSCLOUD_MAP_DISCOVER_INSTANCE_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLOUD_MAP_REGISTER_INSTANCE_ACCESS = "AWSCLOUD_MAP_REGISTER_INSTANCE_ACCESS"
    '''
    :stability: experimental
    '''
    WELL_ARCHITECTED_CONSOLE_FULL_ACCESS = "WELL_ARCHITECTED_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    WELL_ARCHITECTED_CONSOLE_READ_ONLY_ACCESS = "WELL_ARCHITECTED_CONSOLE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUDWATCH_APPLICATION_INSIGHTS_SERVICE_LINKED_ROLE_POLICY = "CLOUDWATCH_APPLICATION_INSIGHTS_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSIO_T_SITE_WISE_FULL_ACCESS = "AWSIO_T_SITE_WISE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_SITE_WISE_READ_ONLY_ACCESS = "AWSIO_T_SITE_WISE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_PERSONALIZE_FULL_ACCESS = "AMAZON_PERSONALIZE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLIENT_VPN_SERVICE_ROLE_POLICY = "CLIENT_VPN_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_MQ_API_READ_ONLY_ACCESS = "AMAZON_MQ_API_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MQ_API_FULL_ACCESS = "AMAZON_MQ_API_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DOC_DB_FULL_ACCESS = "AMAZON_DOC_DB_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DOC_DB_READ_ONLY_ACCESS = "AMAZON_DOC_DB_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DOC_DB_CONSOLE_FULL_ACCESS = "AMAZON_DOC_DB_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_ROLE_POLICY_FOR_BACKUP = "AWSBACKUP_SERVICE_ROLE_POLICY_FOR_BACKUP"
    '''
    :stability: experimental
    '''
    AWSIO_T_EVENTS_READ_ONLY_ACCESS = "AWSIO_T_EVENTS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_EVENTS_FULL_ACCESS = "AWSIO_T_EVENTS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_MAINTENANCE = "AWSELASTIC_BEANSTALK_MAINTENANCE"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_ROLE_POLICY_FOR_RESTORES = "AWSBACKUP_SERVICE_ROLE_POLICY_FOR_RESTORES"
    '''
    :stability: experimental
    '''
    AWSTRANSFER_LOGGING_ACCESS = "AWSTRANSFER_LOGGING_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MSK_FULL_ACCESS = "AMAZON_MSK_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MSK_READ_ONLY_ACCESS = "AMAZON_MSK_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_FORECAST_FULL_ACCESS = "AMAZON_FORECAST_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATA_SYNC_READ_ONLY_ACCESS = "AWSDATA_SYNC_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATA_SYNC_FULL_ACCESS = "AWSDATA_SYNC_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    WORK_LINK_SERVICE_ROLE_POLICY = "WORK_LINK_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDEEP_RACER_SERVICE_ROLE_POLICY = "AWSDEEP_RACER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDEEP_RACER_CLOUD_FORMATION_ACCESS_POLICY = "AWSDEEP_RACER_CLOUD_FORMATION_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    AWSDEEP_RACER_ROBO_MAKER_ACCESS_POLICY = "AWSDEEP_RACER_ROBO_MAKER_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    COMPREHEND_DATA_ACCESS_ROLE_POLICY = "COMPREHEND_DATA_ACCESS_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    ALEXA_FOR_BUSINESS_NETWORK_PROFILE_SERVICE_POLICY = "ALEXA_FOR_BUSINESS_NETWORK_PROFILE_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_MANAGED_INSTANCE_CORE = "AMAZON_SSM_MANAGED_INSTANCE_CORE"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_DIRECTORY_SERVICE_ACCESS = "AMAZON_SSM_DIRECTORY_SERVICE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_COGNITO_IDP_EMAIL_SERVICE_ROLE_POLICY = "AMAZON_COGNITO_IDP_EMAIL_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSIQFULL_ACCESS = "AWSIQFULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGLOBAL_ACCELERATOR_SLR_POLICY = "AWSGLOBAL_ACCELERATOR_SLR_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_MAIL_EVENTS_SERVICE_ROLE_POLICY = "AMAZON_WORK_MAIL_EVENTS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPP_MESH_FULL_ACCESS = "AWSAPP_MESH_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPP_MESH_READ_ONLY = "AWSAPP_MESH_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_MANAGED_BLOCKCHAIN_CONSOLE_FULL_ACCESS = "AMAZON_MANAGED_BLOCKCHAIN_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MANAGED_BLOCKCHAIN_FULL_ACCESS = "AMAZON_MANAGED_BLOCKCHAIN_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MANAGED_BLOCKCHAIN_READ_ONLY_ACCESS = "AMAZON_MANAGED_BLOCKCHAIN_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDENY_ALL = "AWSDENY_ALL"
    '''
    :stability: experimental
    '''
    AWSCONTROL_TOWER_SERVICE_ROLE_POLICY = "AWSCONTROL_TOWER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_RESOLVER_FULL_ACCESS = "AMAZON_ROUTE53_RESOLVER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_RESOLVER_READ_ONLY_ACCESS = "AMAZON_ROUTE53_RESOLVER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_SITE_WISE_CONSOLE_FULL_ACCESS = "AWSIO_T_SITE_WISE_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPP_MESH_SERVICE_ROLE_POLICY = "AWSAPP_MESH_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_ACCESS_MANAGER_FULL_ACCESS = "AWSRESOURCE_ACCESS_MANAGER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    MIGRATION_HUB_SERVICE_ROLE_POLICY = "MIGRATION_HUB_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    MIGRATION_HUB_DMS_ACCESS_SERVICE_ROLE_POLICY = "MIGRATION_HUB_DMS_ACCESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    MIGRATION_HUB_SMS_ACCESS_SERVICE_ROLE_POLICY = "MIGRATION_HUB_SMS_ACCESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCONFIG_MULTI_ACCOUNT_SETUP_POLICY = "AWSCONFIG_MULTI_ACCOUNT_SETUP_POLICY"
    '''
    :stability: experimental
    '''
    AWSCONFIG_REMEDIATION_SERVICE_ROLE_POLICY = "AWSCONFIG_REMEDIATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPP_MESH_PREVIEW_SERVICE_ROLE_POLICY = "AWSAPP_MESH_PREVIEW_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCERTIFICATE_MANAGER_PRIVATE_CA_PRIVILEGED_USER = "AWSCERTIFICATE_MANAGER_PRIVATE_CA_PRIVILEGED_USER"
    '''
    :stability: experimental
    '''
    LAKE_FORMATION_DATA_ACCESS_SERVICE_ROLE_POLICY = "LAKE_FORMATION_DATA_ACCESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    IAMACCESS_ADVISOR_READ_ONLY = "IAMACCESS_ADVISOR_READ_ONLY"
    '''
    :stability: experimental
    '''
    SERVICE_QUOTAS_SERVICE_ROLE_POLICY = "SERVICE_QUOTAS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SERVICE_QUOTAS_READ_ONLY_ACCESS = "SERVICE_QUOTAS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    SERVICE_QUOTAS_FULL_ACCESS = "SERVICE_QUOTAS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_PROCUREMENT_SYSTEM_ADMIN_FULL_ACCESS = "AWSMARKETPLACE_PROCUREMENT_SYSTEM_ADMIN_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    EC2_INSTANCE_CONNECT = "EC2_INSTANCE_CONNECT"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_SERVICE_ACCESS = "AMAZON_WORK_SPACES_SERVICE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_SELF_SERVICE_ACCESS = "AMAZON_WORK_SPACES_SELF_SERVICE_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_SELLER_FULL_ACCESS = "AWSMARKETPLACE_SELLER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_SELLER_PRODUCTS_FULL_ACCESS = "AWSMARKETPLACE_SELLER_PRODUCTS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_SELLER_PRODUCTS_READ_ONLY = "AWSMARKETPLACE_SELLER_PRODUCTS_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSAPP_MESH_ENVOY_ACCESS = "AWSAPP_MESH_ENVOY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_READ_ONLY_ACCESS = "AMAZON_EVENT_BRIDGE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_FULL_ACCESS = "AMAZON_EVENT_BRIDGE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUDWATCH_CROSSACCOUNTACCESS = "CLOUDWATCH_CROSSACCOUNTACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_AUTOMATIC_DASHBOARDS_ACCESS = "CLOUD_WATCH_AUTOMATIC_DASHBOARDS_ACCESS"
    '''
    :stability: experimental
    '''
    CONFIG_CONFORMS_SERVICE_ROLE_POLICY = "CONFIG_CONFORMS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCLOUD_FORMATION_FULL_ACCESS = "AWSCLOUD_FORMATION_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    ELEMENTAL_APPLIANCES_SOFTWARE_FULL_ACCESS = "ELEMENTAL_APPLIANCES_SOFTWARE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPP_MESH_PREVIEW_ENVOY_ACCESS = "AWSAPP_MESH_PREVIEW_ENVOY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSVPCS2_S_VPN_SERVICE_ROLE_POLICY = "AWSVPCS2_S_VPN_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_SM_S = "AWSSERVICE_ROLE_FOR_SM_S"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_DEFENDER_ENABLE_IO_T_LOGGING_MITIGATION_ACTION = "AWSIO_T_DEVICE_DEFENDER_ENABLE_IO_T_LOGGING_MITIGATION_ACTION"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_DEFENDER_PUBLISH_FINDINGS_TO_SNS_MITIGATION_ACTION = "AWSIO_T_DEVICE_DEFENDER_PUBLISH_FINDINGS_TO_SNS_MITIGATION_ACTION"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_DEFENDER_REPLACE_DEFAULT_POLICY_MITIGATION_ACTION = "AWSIO_T_DEVICE_DEFENDER_REPLACE_DEFAULT_POLICY_MITIGATION_ACTION"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_DEFENDER_UPDATE_CA_CERT_MITIGATION_ACTION = "AWSIO_T_DEVICE_DEFENDER_UPDATE_CA_CERT_MITIGATION_ACTION"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_DEFENDER_UPDATE_DEVICE_CERT_MITIGATION_ACTION = "AWSIO_T_DEVICE_DEFENDER_UPDATE_DEVICE_CERT_MITIGATION_ACTION"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_DEFENDER_ADD_THINGS_TO_THING_GROUP_MITIGATION_ACTION = "AWSIO_T_DEVICE_DEFENDER_ADD_THINGS_TO_THING_GROUP_MITIGATION_ACTION"
    '''
    :stability: experimental
    '''
    AWSLAKE_FORMATION_DATA_ADMIN = "AWSLAKE_FORMATION_DATA_ADMIN"
    '''
    :stability: experimental
    '''
    AWSIQCONTRACT_SERVICE_ROLE_POLICY = "AWSIQCONTRACT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSIQPERMISSION_SERVICE_ROLE_POLICY = "AWSIQPERMISSION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_QLDB_READ_ONLY = "AMAZON_QLDB_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_QLDB_FULL_ACCESS = "AMAZON_QLDB_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_QLDB_CONSOLE_FULL_ACCESS = "AMAZON_QLDB_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_VOICE_CONNECTOR_SERVICE_LINKED_ROLE_POLICY = "AMAZON_CHIME_VOICE_CONNECTOR_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_SERVICE_ROLE_POLICY = "AMAZON_CHIME_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_LOG_DELIVERY_POLICY = "AWSSERVICE_ROLE_FOR_LOG_DELIVERY_POLICY"
    '''
    :stability: experimental
    '''
    ALEXA_FOR_BUSINESS_POLY_DELEGATED_ACCESS_POLICY = "ALEXA_FOR_BUSINESS_POLY_DELEGATED_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_NOTEBOOKS_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_NOTEBOOKS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_LAMBDA_CONCURRENCY_POLICY = "AWSAPPLICATION_AUTOSCALING_LAMBDA_CONCURRENCY_POLICY"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_ACCOUNT_DISCOVERY_SERVICE_POLICY = "AWSSYSTEMS_MANAGER_ACCOUNT_DISCOVERY_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_END_USER_READ_ONLY_ACCESS = "AWSSERVICE_CATALOG_END_USER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_ADMIN_READ_ONLY_ACCESS = "AWSSERVICE_CATALOG_ADMIN_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_MARKETPLACE_REQUESTS = "AWSPRIVATE_MARKETPLACE_REQUESTS"
    '''
    :stability: experimental
    '''
    AWSFOR_WORD_PRESS_PLUGIN_POLICY = "AWSFOR_WORD_PRESS_PLUGIN_POLICY"
    '''
    :stability: experimental
    '''
    AWSCODE_STAR_NOTIFICATIONS_SERVICE_ROLE_POLICY = "AWSCODE_STAR_NOTIFICATIONS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_FILE_SYSTEM_SERVICE_ROLE_POLICY = "AMAZON_ELASTIC_FILE_SYSTEM_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSAVINGS_PLANS_READ_ONLY_ACCESS = "AWSSAVINGS_PLANS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSAVINGS_PLANS_FULL_ACCESS = "AWSSAVINGS_PLANS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    WAFV2_LOGGING_SERVICE_ROLE_POLICY = "WAFV2_LOGGING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_AMAZON_EKS_NODEGROUP = "AWSSERVICE_ROLE_FOR_AMAZON_EKS_NODEGROUP"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_ROLE_POLICY_FOR_LAUNCH_WIZARD = "AMAZON_E_C2_ROLE_POLICY_FOR_LAUNCH_WIZARD"
    '''
    :stability: experimental
    '''
    AWSDATA_EXCHANGE_READ_ONLY = "AWSDATA_EXCHANGE_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSDATA_EXCHANGE_SUBSCRIBER_FULL_ACCESS = "AWSDATA_EXCHANGE_SUBSCRIBER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATA_EXCHANGE_PROVIDER_FULL_ACCESS = "AWSDATA_EXCHANGE_PROVIDER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATA_EXCHANGE_FULL_ACCESS = "AWSDATA_EXCHANGE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_SITE_WISE_MONITOR_SERVICE_ROLE_POLICY = "AWSIO_T_SITE_WISE_MONITOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_COMPREHEND_ENDPOINT_POLICY = "AWSAPPLICATION_AUTOSCALING_COMPREHEND_ENDPOINT_POLICY"
    '''
    :stability: experimental
    '''
    DYNAMO_DB_CLOUD_WATCH_CONTRIBUTOR_INSIGHTS_SERVICE_ROLE_POLICY = "DYNAMO_DB_CLOUD_WATCH_CONTRIBUTOR_INSIGHTS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCHATBOT_SERVICE_LINKED_ROLE_POLICY = "AWSCHATBOT_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSBACKUP_FULL_ACCESS = "AWSBACKUP_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_OPERATOR_ACCESS = "AWSBACKUP_OPERATOR_ACCESS"
    '''
    :stability: experimental
    '''
    AWSTRUSTED_ADVISOR_REPORTING_SERVICE_ROLE_POLICY = "AWSTRUSTED_ADVISOR_REPORTING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_METERING_REGISTER_USAGE = "AWSMARKETPLACE_METERING_REGISTER_USAGE"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_MANAGED_UPDATES_SERVICE_ROLE_POLICY = "AWSELASTIC_BEANSTALK_MANAGED_UPDATES_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_FARGATE_POD_EXECUTION_ROLE_POLICY = "AMAZON_EKS_FARGATE_POD_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_FOR_FARGATE_SERVICE_ROLE_POLICY = "AMAZON_EKS_FOR_FARGATE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_SYNTHETICS_FULL_ACCESS = "CLOUD_WATCH_SYNTHETICS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_SYNTHETICS_READ_ONLY_ACCESS = "CLOUD_WATCH_SYNTHETICS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_SCHEMAS_SERVICE_ROLE_POLICY = "AMAZON_EVENT_BRIDGE_SCHEMAS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_SCHEMAS_READ_ONLY_ACCESS = "AMAZON_EVENT_BRIDGE_SCHEMAS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_SCHEMAS_FULL_ACCESS = "AMAZON_EVENT_BRIDGE_SCHEMAS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_IMAGE_BUILDER = "AWSSERVICE_ROLE_FOR_IMAGE_BUILDER"
    '''
    :stability: experimental
    '''
    EC2_INSTANCE_PROFILE_FOR_IMAGE_BUILDER = "EC2_INSTANCE_PROFILE_FOR_IMAGE_BUILDER"
    '''
    :stability: experimental
    '''
    IAMACCESS_ANALYZER_FULL_ACCESS = "IAMACCESS_ANALYZER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    IAMACCESS_ANALYZER_READ_ONLY_ACCESS = "IAMACCESS_ANALYZER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    ACCESS_ANALYZER_SERVICE_ROLE_POLICY = "ACCESS_ANALYZER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_GURU_REVIEWER_SERVICE_ROLE_POLICY = "AMAZON_CODE_GURU_REVIEWER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_GURU_REVIEWER_FULL_ACCESS = "AMAZON_CODE_GURU_REVIEWER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    COMPUTE_OPTIMIZER_SERVICE_ROLE_POLICY = "COMPUTE_OPTIMIZER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_GURU_REVIEWER_READ_ONLY_ACCESS = "AMAZON_CODE_GURU_REVIEWER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_GURU_PROFILER_FULL_ACCESS = "AMAZON_CODE_GURU_PROFILER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_GURU_PROFILER_READ_ONLY_ACCESS = "AMAZON_CODE_GURU_PROFILER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MCS_FULL_ACCESS = "AMAZON_MCS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MCS_READ_ONLY_ACCESS = "AMAZON_MCS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSNETWORK_MANAGER_SERVICE_ROLE_POLICY = "AWSNETWORK_MANAGER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_KENDRA_READ_ONLY_ACCESS = "AMAZON_KENDRA_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_KENDRA_FULL_ACCESS = "AMAZON_KENDRA_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_MECHANICAL_TURK_ACCESS = "AMAZON_SAGE_MAKER_MECHANICAL_TURK_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_AUGMENTED_AI_HUMAN_LOOP_FULL_ACCESS = "AMAZON_AUGMENTED_AI_HUMAN_LOOP_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_AUGMENTED_AI_FULL_ACCESS = "AMAZON_AUGMENTED_AI_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSNETWORK_MANAGER_READ_ONLY_ACCESS = "AWSNETWORK_MANAGER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSNETWORK_MANAGER_FULL_ACCESS = "AWSNETWORK_MANAGER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_FRAUD_DETECTOR_FULL_ACCESS_POLICY = "AMAZON_FRAUD_DETECTOR_FULL_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_ACCESS_MANAGER_RESOURCE_SHARE_PARTICIPANT_ACCESS = "AWSRESOURCE_ACCESS_MANAGER_RESOURCE_SHARE_PARTICIPANT_ACCESS"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_ACCESS_MANAGER_READ_ONLY_ACCESS = "AWSRESOURCE_ACCESS_MANAGER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_FORMATION_STACK_SETS_ORG_MEMBER_SERVICE_ROLE_POLICY = "CLOUD_FORMATION_STACK_SETS_ORG_MEMBER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_FORMATION_STACK_SETS_ORG_ADMIN_SERVICE_ROLE_POLICY = "CLOUD_FORMATION_STACK_SETS_ORG_ADMIN_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    HEALTH_ORGANIZATIONSSERVICEROLEPOLICY = "HEALTH_ORGANIZATIONSSERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWSIMAGE_BUILDER_READ_ONLY_ACCESS = "AWSIMAGE_BUILDER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIMAGE_BUILDER_FULL_ACCESS = "AWSIMAGE_BUILDER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    EC2_FLEET_TIME_SHIFTABLE_SERVICE_ROLE_POLICY = "EC2_FLEET_TIME_SHIFTABLE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_REKOGNITION_CUSTOM_LABELS_FULL_ACCESS = "AMAZON_REKOGNITION_CUSTOM_LABELS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_DOCS_READ_ONLY_ACCESS = "AMAZON_WORK_DOCS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_FILE_SYSTEM_CLIENT_READ_WRITE_ACCESS = "AMAZON_ELASTIC_FILE_SYSTEM_CLIENT_READ_WRITE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_FILE_SYSTEM_CLIENT_READ_ONLY_ACCESS = "AMAZON_ELASTIC_FILE_SYSTEM_CLIENT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_FILE_SYSTEM_CLIENT_FULL_ACCESS = "AMAZON_ELASTIC_FILE_SYSTEM_CLIENT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_SAGE_MAKER_POLICY = "AWSQUICK_SIGHT_SAGE_MAKER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_MANAGED_BLOCKCHAIN_SERVICE_ROLE_POLICY = "AMAZON_MANAGED_BLOCKCHAIN_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPP_SYNC_SERVICE_ROLE_POLICY = "AWSAPP_SYNC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_SD_K = "AMAZON_CHIME_SD_K"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_TESTER_FOR_FREE_RTOS_FULL_ACCESS = "AWSIO_T_DEVICE_TESTER_FOR_FREE_RTOS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_DEVICE_TESTER_FOR_GREENGRASS_FULL_ACCESS = "AWSIO_T_DEVICE_TESTER_FOR_GREENGRASS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_SERVICE_ROLE_POLICY = "AMAZON_EKS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    COMPUTE_OPTIMIZER_READ_ONLY_ACCESS = "COMPUTE_OPTIMIZER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_CASSANDRA_TABLE_POLICY = "AWSAPPLICATION_AUTOSCALING_CASSANDRA_TABLE_POLICY"
    '''
    :stability: experimental
    '''
    ELEMENTAL_APPLIANCES_SOFTWARE_READ_ONLY_ACCESS = "ELEMENTAL_APPLIANCES_SOFTWARE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    GAME_LIFT_GAME_SERVER_GROUP_POLICY = "GAME_LIFT_GAME_SERVER_GROUP_POLICY"
    '''
    :stability: experimental
    '''
    AWSWAFCONSOLE_FULL_ACCESS = "AWSWAFCONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSWAFCONSOLE_READ_ONLY_ACCESS = "AWSWAFCONSOLE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_DOCS_FULL_ACCESS = "AMAZON_WORK_DOCS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_AUGMENTED_AI_INTEGRATED_API_ACCESS = "AMAZON_AUGMENTED_AI_INTEGRATED_API_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_KEYSPACES_FULL_ACCESS = "AMAZON_KEYSPACES_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_KEYSPACES_READ_ONLY_ACCESS = "AMAZON_KEYSPACES_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DETECTIVE_FULL_ACCESS = "AMAZON_DETECTIVE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPURCHASE_ORDERS_SERVICE_ROLE_POLICY = "AWSPURCHASE_ORDERS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SERVER_MIGRATION_SERVICE_CONSOLE_FULL_ACCESS = "SERVER_MIGRATION_SERVICE_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_LINKED_ROLE_POLICY_FOR_BACKUP_TEST = "AWSBACKUP_SERVICE_LINKED_ROLE_POLICY_FOR_BACKUP_TEST"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_PATCH_ASSOCIATION = "AMAZON_SSM_PATCH_ASSOCIATION"
    '''
    :stability: experimental
    '''
    AWSCLOUD9_SSM_INSTANCE_PROFILE = "AWSCLOUD9_SSM_INSTANCE_PROFILE"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_ROLE_FOR_CLOUD_FORMATION = "AWSCODE_DEPLOY_ROLE_FOR_CLOUD_FORMATION"
    '''
    :stability: experimental
    '''
    AWSIO_T_SITE_WISE_MONITOR_PORTAL_ACCESS = "AWSIO_T_SITE_WISE_MONITOR_PORTAL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSTHINKBOX_AWS_PORTAL_GATEWAY_POLICY = "AWSTHINKBOX_AWS_PORTAL_GATEWAY_POLICY"
    '''
    :stability: experimental
    '''
    AWSTHINKBOX_AWS_PORTAL_WORKER_POLICY = "AWSTHINKBOX_AWS_PORTAL_WORKER_POLICY"
    '''
    :stability: experimental
    '''
    AWSTHINKBOX_ASSET_SERVER_POLICY = "AWSTHINKBOX_ASSET_SERVER_POLICY"
    '''
    :stability: experimental
    '''
    AWSTHINKBOX_DEADLINE_RESOURCE_TRACKER_ACCESS_POLICY = "AWSTHINKBOX_DEADLINE_RESOURCE_TRACKER_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    AWSTHINKBOX_DEADLINE_RESOURCE_TRACKER_ADMIN_POLICY = "AWSTHINKBOX_DEADLINE_RESOURCE_TRACKER_ADMIN_POLICY"
    '''
    :stability: experimental
    '''
    AWSTHINKBOX_DEADLINE_SPOT_EVENT_PLUGIN_WORKER_POLICY = "AWSTHINKBOX_DEADLINE_SPOT_EVENT_PLUGIN_WORKER_POLICY"
    '''
    :stability: experimental
    '''
    AWSTHINKBOX_DEADLINE_SPOT_EVENT_PLUGIN_ADMIN_POLICY = "AWSTHINKBOX_DEADLINE_SPOT_EVENT_PLUGIN_ADMIN_POLICY"
    '''
    :stability: experimental
    '''
    AWSTHINKBOX_AWS_PORTAL_ADMIN_POLICY = "AWSTHINKBOX_AWS_PORTAL_ADMIN_POLICY"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_LINKED_ROLE_POLICY_FOR_BACKUP = "AWSBACKUP_SERVICE_LINKED_ROLE_POLICY_FOR_BACKUP"
    '''
    :stability: experimental
    '''
    AMAZON_APP_FLOW_READ_ONLY_ACCESS = "AMAZON_APP_FLOW_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_APP_FLOW_FULL_ACCESS = "AMAZON_APP_FLOW_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    ALEXA_FOR_BUSINESS_LIFESIZE_DELEGATED_ACCESS_POLICY = "ALEXA_FOR_BUSINESS_LIFESIZE_DELEGATED_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    ELEMENTAL_ACTIVATIONS_FULL_ACCESS = "ELEMENTAL_ACTIVATIONS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_ROLE_WORKER_TIER = "AWSELASTIC_BEANSTALK_ROLE_WORKER_TIER"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_ROLE_SN_S = "AWSELASTIC_BEANSTALK_ROLE_SN_S"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_ROLE_RD_S = "AWSELASTIC_BEANSTALK_ROLE_RD_S"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_ROLE_EC_S = "AWSELASTIC_BEANSTALK_ROLE_EC_S"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_ROLE_CORE = "AWSELASTIC_BEANSTALK_ROLE_CORE"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_ROLE_CW_L = "AWSELASTIC_BEANSTALK_ROLE_CW_L"
    '''
    :stability: experimental
    '''
    AWSCODE_ARTIFACT_ADMIN_ACCESS = "AWSCODE_ARTIFACT_ADMIN_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_ORGANIZATION_ADMIN_ACCESS = "AWSBACKUP_ORGANIZATION_ADMIN_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MACHINE_LEARNING_ROLEFOR_REDSHIFT_DATA_SOURCE_V3 = "AMAZON_MACHINE_LEARNING_ROLEFOR_REDSHIFT_DATA_SOURCE_V3"
    '''
    :stability: experimental
    '''
    AMAZON_HONEYCODE_TEAM_ASSOCIATION_READ_ONLY_ACCESS = "AMAZON_HONEYCODE_TEAM_ASSOCIATION_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_HONEYCODE_WORKBOOK_READ_ONLY_ACCESS = "AMAZON_HONEYCODE_WORKBOOK_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_HONEYCODE_FULL_ACCESS = "AMAZON_HONEYCODE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_HONEYCODE_READ_ONLY_ACCESS = "AMAZON_HONEYCODE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_HONEYCODE_TEAM_ASSOCIATION_FULL_ACCESS = "AMAZON_HONEYCODE_TEAM_ASSOCIATION_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_HONEYCODE_WORKBOOK_FULL_ACCESS = "AMAZON_HONEYCODE_WORKBOOK_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CERTIFICATE_MANAGER_SERVICE_ROLE_POLICY = "CERTIFICATE_MANAGER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCODE_ARTIFACT_READ_ONLY_ACCESS = "AWSCODE_ARTIFACT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICEROLEFORCODEGURU_PROFILER = "AWSSERVICEROLEFORCODEGURU_PROFILER"
    '''
    :stability: experimental
    '''
    AMAZON_COGNITO_IDP_SERVICE_ROLE_POLICY = "AMAZON_COGNITO_IDP_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_LIVE_READ_ONLY = "AWSELEMENTAL_MEDIA_LIVE_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_LIVE_FULL_ACCESS = "AWSELEMENTAL_MEDIA_LIVE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_GROUND_TRUTH_EXECUTION = "AMAZON_SAGE_MAKER_GROUND_TRUTH_EXECUTION"
    '''
    :stability: experimental
    '''
    SERVER_MIGRATION_SERVICE_ROLE_FOR_INSTANCE_VALIDATION = "SERVER_MIGRATION_SERVICE_ROLE_FOR_INSTANCE_VALIDATION"
    '''
    :stability: experimental
    '''
    AWSCODEPIPELINE_READONLYACCESS = "AWSCODEPIPELINE_READONLYACCESS"
    '''
    :stability: experimental
    '''
    AWSCODEPIPELINE_FULLACCESS = "AWSCODEPIPELINE_FULLACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_BRAKET_SERVICE_ROLE_POLICY = "AMAZON_BRAKET_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSLAKE_FORMATION_CROSS_ACCOUNT_MANAGER = "AWSLAKE_FORMATION_CROSS_ACCOUNT_MANAGER"
    '''
    :stability: experimental
    '''
    AMAZON_BRAKET_FULL_ACCESS = "AMAZON_BRAKET_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_MSK_EXECUTION_ROLE = "AWSLAMBDA_MSK_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AWSCOMPROMISED_KEY_QUARANTINE = "AWSCOMPROMISED_KEY_QUARANTINE"
    '''
    :stability: experimental
    '''
    AMAZON_EKSVPC_RESOURCE_CONTROLLER = "AMAZON_EKSVPC_RESOURCE_CONTROLLER"
    '''
    :stability: experimental
    '''
    ROUTE53_RESOLVER_SERVICE_ROLE_POLICY = "ROUTE53_RESOLVER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLIENT_VPN_SERVICE_CONNECTIONS_ROLE_POLICY = "CLIENT_VPN_SERVICE_CONNECTIONS_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCODE_DEPLOY_ROLE_FOR_LAMBDA_LIMITED = "AWSCODE_DEPLOY_ROLE_FOR_LAMBDA_LIMITED"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_ROLEFOR_AWS_CODE_DEPLOY_LIMITED = "AMAZON_E_C2_ROLEFOR_AWS_CODE_DEPLOY_LIMITED"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_KAFKA_CLUSTER_POLICY = "AWSAPPLICATION_AUTOSCALING_KAFKA_CLUSTER_POLICY"
    '''
    :stability: experimental
    '''
    AWSTRANSFER_READ_ONLY_ACCESS = "AWSTRANSFER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBILLING_READ_ONLY_ACCESS = "AWSBILLING_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    ELEMENTAL_ACTIVATIONS_READ_ONLY_ACCESS = "ELEMENTAL_ACTIVATIONS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    ELEMENTAL_ACTIVATIONS_GENERATE_LICENSES = "ELEMENTAL_ACTIVATIONS_GENERATE_LICENSES"
    '''
    :stability: experimental
    '''
    ELEMENTAL_ACTIVATIONS_DOWNLOAD_SOFTWARE_ACCESS = "ELEMENTAL_ACTIVATIONS_DOWNLOAD_SOFTWARE_ACCESS"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_ELASTICSEARCH_POLICY = "AWSQUICK_SIGHT_ELASTICSEARCH_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_DATA_FULL_ACCESS = "AMAZON_REDSHIFT_DATA_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSROBOMAKER_FULLACCESS = "AWSROBOMAKER_FULLACCESS"
    '''
    :stability: experimental
    '''
    AWS_CONFIGROLE = "AWS_CONFIGROLE"
    '''
    :stability: experimental
    '''
    MEDIA_PACKAGE_SERVICE_ROLE_POLICY = "MEDIA_PACKAGE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_AMI_INGESTION = "AWSMARKETPLACE_AMI_INGESTION"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_MAP_REDUCE_PLACEMENT_GROUP_POLICY = "AMAZON_ELASTIC_MAP_REDUCE_PLACEMENT_GROUP_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_FILE_SYSTEMS_UTILS = "AMAZON_ELASTIC_FILE_SYSTEMS_UTILS"
    '''
    :stability: experimental
    '''
    EC2_IMAGE_BUILDER_CROSS_ACCOUNT_DISTRIBUTION_ACCESS = "EC2_IMAGE_BUILDER_CROSS_ACCOUNT_DISTRIBUTION_ACCESS"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_TIMESTREAM_POLICY = "AWSQUICK_SIGHT_TIMESTREAM_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_TIMESTREAM_READ_ONLY_ACCESS = "AMAZON_TIMESTREAM_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_TIMESTREAM_FULL_ACCESS = "AMAZON_TIMESTREAM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_TIMESTREAM_CONSOLE_FULL_ACCESS = "AMAZON_TIMESTREAM_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_CLOUD_WATCH_ALARMS_ACTION_SSM_SERVICE_ROLE_POLICY = "AWSSERVICE_ROLE_FOR_CLOUD_WATCH_ALARMS_ACTION_SSM_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_S3_OUTPOSTS_FULL_ACCESS = "AMAZON_S3_OUTPOSTS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_S3_OUTPOSTS_READ_ONLY_ACCESS = "AMAZON_S3_OUTPOSTS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDEEP_RACER_FULL_ACCESS = "AWSDEEP_RACER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_LAMBDA_INSIGHTS_EXECUTION_ROLE_POLICY = "CLOUD_WATCH_LAMBDA_INSIGHTS_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCLOUDTRAIL_FULLACCESS = "AWSCLOUDTRAIL_FULLACCESS"
    '''
    :stability: experimental
    '''
    AWSSUPPORT_SERVICE_ROLE_POLICY = "AWSSUPPORT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSBUDGETS_READ_ONLY_ACCESS = "AWSBUDGETS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBUDGETS_ACTIONS_WITH_AWS_RESOURCE_CONTROL_ACCESS = "AWSBUDGETS_ACTIONS_WITH_AWS_RESOURCE_CONTROL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATA_LIFECYCLE_MANAGER_SERVICE_ROLE_FOR_AMI_MANAGEMENT = "AWSDATA_LIFECYCLE_MANAGER_SERVICE_ROLE_FOR_AMI_MANAGEMENT"
    '''
    :stability: experimental
    '''
    AMAZON_MQ_SERVICE_ROLE_POLICY = "AMAZON_MQ_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSOUTPOSTS_SERVICE_ROLE_POLICY = "AWSOUTPOSTS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWS_GLUE_DATA_BREW_FULL_ACCESS_POLICY = "AWS_GLUE_DATA_BREW_FULL_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    DYNAMO_DB_KINESIS_REPLICATION_SERVICE_ROLE_POLICY = "DYNAMO_DB_KINESIS_REPLICATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_APP_REGISTRY_FULL_ACCESS = "AWSSERVICE_CATALOG_APP_REGISTRY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_APP_REGISTRY_READ_ONLY_ACCESS = "AWSSERVICE_CATALOG_APP_REGISTRY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSNETWORK_FIREWALL_SERVICE_ROLE_POLICY = "AWSNETWORK_FIREWALL_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_READONLYACCESS = "AWSLAMBDA_READONLYACCESS"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_FULLACCESS = "AWSLAMBDA_FULLACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_HONEYCODE_SERVICE_ROLE_POLICY = "AMAZON_HONEYCODE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    S3_STORAGE_LENS_SERVICE_ROLE_POLICY = "S3_STORAGE_LENS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSGLUE_SCHEMA_REGISTRY_FULL_ACCESS = "AWSGLUE_SCHEMA_REGISTRY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGLUE_SCHEMA_REGISTRY_READONLY_ACCESS = "AWSGLUE_SCHEMA_REGISTRY_READONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZONCONNECT_FULLACCESS = "AMAZONCONNECT_FULLACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MWAA_SERVICE_ROLE_POLICY = "AMAZON_MWAA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_APPLICATION_INSIGHTS_FULL_ACCESS = "CLOUD_WATCH_APPLICATION_INSIGHTS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_APPLICATION_INSIGHTS_READ_ONLY_ACCESS = "CLOUD_WATCH_APPLICATION_INSIGHTS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    ELEMENTAL_SUPPORT_CENTER_FULL_ACCESS = "ELEMENTAL_SUPPORT_CENTER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZONSAGEMAKERADMIN_SERVICECATALOGPRODUCTSSERVICEROLEPOLICY = "AMAZONSAGEMAKERADMIN_SERVICECATALOGPRODUCTSSERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DEV_OPS_GURU_SERVICE_ROLE_POLICY = "AMAZON_DEV_OPS_GURU_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPANORAMA_GREENGRASS_GROUP_ROLE_POLICY = "AWSPANORAMA_GREENGRASS_GROUP_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPANORAMA_FULL_ACCESS = "AWSPANORAMA_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPANORAMA_APPLIANCE_ROLE_POLICY = "AWSPANORAMA_APPLIANCE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPANORAMA_SAGE_MAKER_ROLE_POLICY = "AWSPANORAMA_SAGE_MAKER_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPANORAMA_SERVICE_ROLE_POLICY = "AWSPANORAMA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_CONTAINER_REGISTRY_PUBLIC_POWER_USER = "AMAZON_ELASTIC_CONTAINER_REGISTRY_PUBLIC_POWER_USER"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_FEATURE_STORE_ACCESS = "AMAZON_SAGE_MAKER_FEATURE_STORE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DEV_OPS_GURU_READ_ONLY_ACCESS = "AMAZON_DEV_OPS_GURU_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DEV_OPS_GURU_FULL_ACCESS = "AMAZON_DEV_OPS_GURU_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_CONTAINER_REGISTRY_PUBLIC_FULL_ACCESS = "AMAZON_ELASTIC_CONTAINER_REGISTRY_PUBLIC_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ELASTIC_CONTAINER_REGISTRY_PUBLIC_READ_ONLY = "AMAZON_ELASTIC_CONTAINER_REGISTRY_PUBLIC_READ_ONLY"
    '''
    :stability: experimental
    '''
    ADMINISTRATORACCESS_AMPLIFY = "ADMINISTRATORACCESS_AMPLIFY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_MONITRON_POLICY = "AWSSERVICE_ROLE_FOR_MONITRON_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_MONITRON_FULL_ACCESS = "AMAZON_MONITRON_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_LICENSE_MANAGEMENT_SERVICE_ROLE_POLICY = "AWSMARKETPLACE_LICENSE_MANAGEMENT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSGLUE_DATA_BREW_SERVICE_ROLE = "AWSGLUE_DATA_BREW_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    ECRREPLICATION_SERVICE_ROLE_POLICY = "ECRREPLICATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    IVSRECORD_TO_S3 = "IVSRECORD_TO_S3"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_CHANGE_MANAGEMENT_SERVICE_POLICY = "AWSSYSTEMS_MANAGER_CHANGE_MANAGEMENT_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAUDIT_MANAGER_SERVICE_ROLE_POLICY = "AWSAUDIT_MANAGER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_EDGE_DEVICE_FLEET_POLICY = "AMAZON_SAGE_MAKER_EDGE_DEVICE_FLEET_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EMR_CONTAINERS_SERVICE_ROLE_POLICY = "AMAZON_EMR_CONTAINERS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    EC2_INSTANCE_PROFILE_FOR_IMAGE_BUILDER_ECR_CONTAINER_BUILDS = "EC2_INSTANCE_PROFILE_FOR_IMAGE_BUILDER_ECR_CONTAINER_BUILDS"
    '''
    :stability: experimental
    '''
    AWSAUDIT_MANAGER_ADMINISTRATOR_ACCESS = "AWSAUDIT_MANAGER_ADMINISTRATOR_ACCESS"
    '''
    :stability: experimental
    '''
    AWSTRANSFER_CONSOLE_FULL_ACCESS = "AWSTRANSFER_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSTRANSFER_FULL_ACCESS = "AWSTRANSFER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_FLEET_HUB_FEDERATION_ACCESS = "AWSIO_T_FLEET_HUB_FEDERATION_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_WIRELESS_FULL_ACCESS = "AWSIO_T_WIRELESS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_WIRELESS_READ_ONLY_ACCESS = "AWSIO_T_WIRELESS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_WIRELESS_FULL_PUBLISH_ACCESS = "AWSIO_T_WIRELESS_FULL_PUBLISH_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_WIRELESS_GATEWAY_CERT_MANAGER = "AWSIO_T_WIRELESS_GATEWAY_CERT_MANAGER"
    '''
    :stability: experimental
    '''
    AWSIO_T_WIRELESS_DATA_ACCESS = "AWSIO_T_WIRELESS_DATA_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_WIRELESS_LOGGING = "AWSIO_T_WIRELESS_LOGGING"
    '''
    :stability: experimental
    '''
    AWSCLOUD_SHELL_FULL_ACCESS = "AWSCLOUD_SHELL_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_PROMETHEUS_FULL_ACCESS = "AMAZON_PROMETHEUS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_PROMETHEUS_CONSOLE_FULL_ACCESS = "AMAZON_PROMETHEUS_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_PROMETHEUS_QUERY_ACCESS = "AMAZON_PROMETHEUS_QUERY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_PROMETHEUS_REMOTE_WRITE_ACCESS = "AMAZON_PROMETHEUS_REMOTE_WRITE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_FIS_SERVICE_ROLE_POLICY = "AMAZON_FIS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CORE_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_CORE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_LEX_V2_BOT_POLICY = "AMAZON_LEX_V2_BOT_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_LEX_CHANNELS_ACCESS = "AMAZON_LEX_CHANNELS_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDIRECT_CONNECT_SERVICE_ROLE_POLICY = "AWSDIRECT_CONNECT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_READ_ONLY = "AWSELASTIC_BEANSTALK_READ_ONLY"
    '''
    :stability: experimental
    '''
    ADMINISTRATORACCESS_AWSELASTICBEANSTALK = "ADMINISTRATORACCESS_AWSELASTICBEANSTALK"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_MAIL_MESSAGE_FLOW_READ_ONLY_ACCESS = "AMAZON_WORK_MAIL_MESSAGE_FLOW_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_GURU_PROFILER_AGENT_ACCESS = "AMAZON_CODE_GURU_PROFILER_AGENT_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_MAIL_MESSAGE_FLOW_FULL_ACCESS = "AMAZON_WORK_MAIL_MESSAGE_FLOW_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_API_DESTINATIONS_SERVICE_ROLE_POLICY = "AMAZON_EVENT_BRIDGE_API_DESTINATIONS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_HEALTH_LAKE_FULL_ACCESS = "AMAZON_HEALTH_LAKE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_HEALTH_LAKE_READ_ONLY_ACCESS = "AMAZON_HEALTH_LAKE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPROTON_DEVELOPER_ACCESS = "AWSPROTON_DEVELOPER_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSTORAGE_GATEWAY_SERVICE_ROLE_POLICY = "AWSSTORAGE_GATEWAY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPROTON_FULL_ACCESS = "AWSPROTON_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPROTON_READ_ONLY_ACCESS = "AWSPROTON_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGRAFANA_CONSOLE_READ_ONLY_ACCESS = "AWSGRAFANA_CONSOLE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGRAFANA_WORKSPACE_PERMISSION_MANAGEMENT = "AWSGRAFANA_WORKSPACE_PERMISSION_MANAGEMENT"
    '''
    :stability: experimental
    '''
    AWSGRAFANA_ACCOUNT_ADMINISTRATOR = "AWSGRAFANA_ACCOUNT_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    AWSELASTIC_BEANSTALK_MANAGED_UPDATES_CUSTOMER_ROLE_POLICY = "AWSELASTIC_BEANSTALK_MANAGED_UPDATES_CUSTOMER_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    BATCH_SERVICE_ROLE_POLICY = "BATCH_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZONEMRSERVICEPOLICY_V2 = "AMAZONEMRSERVICEPOLICY_V2"
    '''
    :stability: experimental
    '''
    AMAZONEMRREADONLYACCESSPOLICY_V2 = "AMAZONEMRREADONLYACCESSPOLICY_V2"
    '''
    :stability: experimental
    '''
    AMAZONEMRFULLACCESSPOLICY_V2 = "AMAZONEMRFULLACCESSPOLICY_V2"
    '''
    :stability: experimental
    '''
    AWSSECURITY_HUB_ORGANIZATIONS_ACCESS = "AWSSECURITY_HUB_ORGANIZATIONS_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_SERVICE_ROLE_POLICY = "AWSAPPLICATION_MIGRATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_CONVERSION_SERVER_POLICY = "AWSAPPLICATION_MIGRATION_CONVERSION_SERVER_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_FULL_ACCESS = "AWSAPPLICATION_MIGRATION_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_AGENT_POLICY = "AWSAPPLICATION_MIGRATION_AGENT_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_E_C2_ACCESS = "AWSAPPLICATION_MIGRATION_E_C2_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_MGH_ACCESS = "AWSAPPLICATION_MIGRATION_MGH_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_READ_ONLY_ACCESS = "AWSAPPLICATION_MIGRATION_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_REPLICATION_SERVER_POLICY = "AWSAPPLICATION_MIGRATION_REPLICATION_SERVER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_LOOKOUT_EQUIPMENT_FULL_ACCESS = "AMAZON_LOOKOUT_EQUIPMENT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCOMPROMISED_KEY_QUARANTINE_V2 = "AWSCOMPROMISED_KEY_QUARANTINE_V2"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_OPS_DATA_SYNC_SERVICE_ROLE_POLICY = "AWSSYSTEMS_MANAGER_OPS_DATA_SYNC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCLOUDWATCHALARMS_ACTIONSSMINCIDENTSSERVICEROLEPOLICY = "AWSCLOUDWATCHALARMS_ACTIONSSMINCIDENTSSERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AMAZONNIMBLESTUDIO_LAUNCHPROFILEWORKER = "AMAZONNIMBLESTUDIO_LAUNCHPROFILEWORKER"
    '''
    :stability: experimental
    '''
    AMAZONNIMBLESTUDIO_STUDIOADMIN = "AMAZONNIMBLESTUDIO_STUDIOADMIN"
    '''
    :stability: experimental
    '''
    AMAZONNIMBLESTUDIO_STUDIOUSER = "AMAZONNIMBLESTUDIO_STUDIOUSER"
    '''
    :stability: experimental
    '''
    AMAZON_LOOKOUT_EQUIPMENT_READ_ONLY_ACCESS = "AMAZON_LOOKOUT_EQUIPMENT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_LOOKOUT_METRICS_READ_ONLY_ACCESS = "AMAZON_LOOKOUT_METRICS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_LOOKOUT_METRICS_FULL_ACCESS = "AMAZON_LOOKOUT_METRICS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSINCIDENT_MANAGER_SERVICE_ROLE_POLICY = "AWSINCIDENT_MANAGER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSINCIDENT_MANAGER_RESOLVER_ACCESS = "AWSINCIDENT_MANAGER_RESOLVER_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_LOOKOUT_VISION_READ_ONLY_ACCESS = "AMAZON_LOOKOUT_VISION_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_LOOKOUT_VISION_FULL_ACCESS = "AMAZON_LOOKOUT_VISION_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_LOOKOUT_VISION_CONSOLE_READ_ONLY_ACCESS = "AMAZON_LOOKOUT_VISION_CONSOLE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_LOOKOUT_VISION_CONSOLE_FULL_ACCESS = "AMAZON_LOOKOUT_VISION_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    APP_RUNNER_SERVICE_ROLE_POLICY = "APP_RUNNER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPP_RUNNER_SERVICE_POLICY_FOR_ECR_ACCESS = "AWSAPP_RUNNER_SERVICE_POLICY_FOR_ECR_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_APP_REGISTRY_SERVICE_ROLE_POLICY = "AWSSERVICE_CATALOG_APP_REGISTRY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDEVICE_FARM_TEST_GRID_SERVICE_ROLE_POLICY = "AWSDEVICE_FARM_TEST_GRID_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSKEY_MANAGEMENT_SERVICE_MULTI_REGION_KEYS_SERVICE_ROLE_POLICY = "AWSKEY_MANAGEMENT_SERVICE_MULTI_REGION_KEYS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSSMOPS_INSIGHTS_SERVICE_ROLE_POLICY = "AWSSSMOPS_INSIGHTS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSBUG_BUST_SERVICE_ROLE_POLICY = "AWSBUG_BUST_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSBUG_BUST_FULL_ACCESS = "AWSBUG_BUST_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBUG_BUST_PLAYER_ACCESS = "AWSBUG_BUST_PLAYER_ACCESS"
    '''
    :stability: experimental
    '''
    ROUTE53_RECOVERY_READINESS_SERVICE_ROLE_POLICY = "ROUTE53_RECOVERY_READINESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_PIPELINES_INTEGRATIONS = "AMAZON_SAGE_MAKER_PIPELINES_INTEGRATIONS"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_TRANSCRIPTION_SERVICE_LINKED_ROLE_POLICY = "AMAZON_CHIME_TRANSCRIPTION_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSLICENSE_MANAGER_CONSUMPTION_POLICY = "AWSLICENSE_MANAGER_CONSUMPTION_POLICY"
    '''
    :stability: experimental
    '''
    MEMORY_DB_SERVICE_ROLE_POLICY = "MEMORY_DB_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_ELASTI_CACHE_RG_POLICY = "AWSAPPLICATION_AUTOSCALING_ELASTI_CACHE_RG_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_S3_OBJECT_LAMBDA_EXECUTION_ROLE_POLICY = "AMAZON_S3_OBJECT_LAMBDA_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_RECOVERY_READINESS_FULL_ACCESS = "AMAZON_ROUTE53_RECOVERY_READINESS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_RECOVERY_CLUSTER_READ_ONLY_ACCESS = "AMAZON_ROUTE53_RECOVERY_CLUSTER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_RECOVERY_CONTROL_CONFIG_FULL_ACCESS = "AMAZON_ROUTE53_RECOVERY_CONTROL_CONFIG_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_RECOVERY_CONTROL_CONFIG_READ_ONLY_ACCESS = "AMAZON_ROUTE53_RECOVERY_CONTROL_CONFIG_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_RECOVERY_READINESS_READ_ONLY_ACCESS = "AMAZON_ROUTE53_RECOVERY_READINESS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_RECOVERY_CLUSTER_FULL_ACCESS = "AMAZON_ROUTE53_RECOVERY_CLUSTER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_POLICY_FOR_BACKUP_REPORTS = "AWSSERVICE_ROLE_POLICY_FOR_BACKUP_REPORTS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_AUDIT_ACCESS = "AWSBACKUP_AUDIT_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_SERVICE_ROLE_POLICY = "AMAZON_OPEN_SEARCH_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_SERVICE_COGNITO_ACCESS = "AMAZON_OPEN_SEARCH_SERVICE_COGNITO_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_NEPTUNE_CLUSTER_POLICY = "AWSAPPLICATION_AUTOSCALING_NEPTUNE_CLUSTER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_CONNECTOR_SERVICE_ROLE_POLICY = "AMAZON_EKS_CONNECTOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    KAFKA_CONNECT_SERVICE_ROLE_POLICY = "KAFKA_CONNECT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICKSIGHT_OPEN_SEARCH_POLICY = "AWSQUICKSIGHT_OPEN_SEARCH_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_SERVICE_FULL_ACCESS = "AMAZON_OPEN_SEARCH_SERVICE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_SERVICE_READ_ONLY_ACCESS = "AMAZON_OPEN_SEARCH_SERVICE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMEDIA_TAILOR_SERVICE_ROLE_POLICY = "AWSMEDIA_TAILOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_MSK_CONNECT_READ_ONLY_ACCESS = "AMAZON_MSK_CONNECT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CONNECT_CAMPAIGNS_SERVICE_LINKED_ROLE_POLICY = "AMAZON_CONNECT_CAMPAIGNS_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_QUERY_EDITOR_V2_FULL_ACCESS = "AMAZON_REDSHIFT_QUERY_EDITOR_V2_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_QUERY_EDITOR_V2_NO_SHARING = "AMAZON_REDSHIFT_QUERY_EDITOR_V2_NO_SHARING"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_QUERY_EDITOR_V2_READ_SHARING = "AMAZON_REDSHIFT_QUERY_EDITOR_V2_READ_SHARING"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_QUERY_EDITOR_V2_READ_WRITE_SHARING = "AMAZON_REDSHIFT_QUERY_EDITOR_V2_READ_WRITE_SHARING"
    '''
    :stability: experimental
    '''
    AMAZON_CONNECT_VOICE_ID_FULL_ACCESS = "AMAZON_CONNECT_VOICE_ID_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSEC2_CAPACITY_RESERVATION_FLEET_ROLE_POLICY = "AWSEC2_CAPACITY_RESERVATION_FLEET_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSACCOUNT_MANAGEMENT_FULL_ACCESS = "AWSACCOUNT_MANAGEMENT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSACCOUNT_MANAGEMENT_READ_ONLY_ACCESS = "AWSACCOUNT_MANAGEMENT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MEMORY_DB_FULL_ACCESS = "AMAZON_MEMORY_DB_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_MEMORY_DB_READ_ONLY_ACCESS = "AMAZON_MEMORY_DB_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_CUSTOM_SERVICE_ROLE_POLICY = "AMAZON_RDS_CUSTOM_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_CUSTOM_PREVIEW_SERVICE_ROLE_POLICY = "AMAZON_RDS_CUSTOM_PREVIEW_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_STRATEGY_SERVICE_ROLE_POLICY = "AWSMIGRATION_HUB_STRATEGY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_STRATEGY_CONSOLE_FULL_ACCESS = "AWSMIGRATION_HUB_STRATEGY_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_STRATEGY_COLLECTOR = "AWSMIGRATION_HUB_STRATEGY_COLLECTOR"
    '''
    :stability: experimental
    '''
    AWSPANORAMA_SERVICE_LINKED_ROLE_POLICY = "AWSPANORAMA_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPANORAMA_APPLIANCE_SERVICE_ROLE_POLICY = "AWSPANORAMA_APPLIANCE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_PURCHASE_ORDERS_SERVICE_ROLE_POLICY = "AWSMARKETPLACE_PURCHASE_ORDERS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDEEP_RACER_ACCOUNT_ADMIN_ACCESS = "AWSDEEP_RACER_ACCOUNT_ADMIN_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDEEP_RACER_DEFAULT_MULTI_USER_ACCESS = "AWSDEEP_RACER_DEFAULT_MULTI_USER_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCOST_AND_USAGE_REPORT_AUTOMATION_POLICY = "AWSCOST_AND_USAGE_REPORT_AUTOMATION_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_ALL_COMMANDS_FULL_ACCESS = "AMAZON_REDSHIFT_ALL_COMMANDS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_V_CENTER_CLIENT_POLICY = "AWSAPPLICATION_MIGRATION_V_CENTER_CLIENT_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DEV_OPS_GURU_ORGANIZATIONS_ACCESS = "AMAZON_DEV_OPS_GURU_ORGANIZATIONS_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_INSPECTOR2_SERVICE_ROLE_POLICY = "AMAZON_INSPECTOR2_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_RECOVERY_INSTANCE_POLICY = "AWSELASTIC_DISASTER_RECOVERY_RECOVERY_INSTANCE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_AGENT_POLICY = "AWSELASTIC_DISASTER_RECOVERY_AGENT_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_AGENT_INSTALLATION_POLICY = "AWSELASTIC_DISASTER_RECOVERY_AGENT_INSTALLATION_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_FAILBACK_POLICY = "AWSELASTIC_DISASTER_RECOVERY_FAILBACK_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_CONSOLE_FULL_ACCESS = "AWSELASTIC_DISASTER_RECOVERY_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_READ_ONLY_ACCESS = "AWSELASTIC_DISASTER_RECOVERY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_SERVICE_ROLE_POLICY = "AWSELASTIC_DISASTER_RECOVERY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_FAILBACK_INSTALLATION_POLICY = "AWSELASTIC_DISASTER_RECOVERY_FAILBACK_INSTALLATION_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_REPLICATION_SERVER_POLICY = "AWSELASTIC_DISASTER_RECOVERY_REPLICATION_SERVER_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_CONVERSION_SERVER_POLICY = "AWSELASTIC_DISASTER_RECOVERY_CONVERSION_SERVER_POLICY"
    '''
    :stability: experimental
    '''
    AWSSHIELD_SERVICE_ROLE_POLICY = "AWSSHIELD_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CLOUD_WATCH_RUM_SERVICE_ROLE_POLICY = "AMAZON_CLOUD_WATCH_RUM_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DETECTIVE_SERVICE_LINKED_ROLE_POLICY = "AMAZON_DETECTIVE_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_GRAFANA_ATHENA_ACCESS = "AMAZON_GRAFANA_ATHENA_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_TAILOR_FULL_ACCESS = "AWSELEMENTAL_MEDIA_TAILOR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_TAILOR_READ_ONLY = "AWSELEMENTAL_MEDIA_TAILOR_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSPROTON_SYNC_SERVICE_ROLE_POLICY = "AWSPROTON_SYNC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_BRAKET_JOBS_EXECUTION_POLICY = "AMAZON_BRAKET_JOBS_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSECRPULLTHROUGHCACHE_SERVICEROLEPOLICY = "AWSECRPULLTHROUGHCACHE_SERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AMAZON_GRAFANA_REDSHIFT_ACCESS = "AMAZON_GRAFANA_REDSHIFT_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_REFACTOR_SPACES_SERVICE_ROLE_POLICY = "AWSMIGRATION_HUB_REFACTOR_SPACES_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_REFACTOR_SPACES_FULL_ACCESS = "AWSMIGRATION_HUB_REFACTOR_SPACES_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CLOUD_WATCH_EVIDENTLY_READ_ONLY_ACCESS = "AMAZON_CLOUD_WATCH_EVIDENTLY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CLOUD_WATCH_EVIDENTLY_FULL_ACCESS = "AMAZON_CLOUD_WATCH_EVIDENTLY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CLOUD_WATCH_RUM_READ_ONLY_ACCESS = "AMAZON_CLOUD_WATCH_RUM_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CLOUD_WATCH_RUM_FULL_ACCESS = "AMAZON_CLOUD_WATCH_RUM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_INSPECTOR2_FULL_ACCESS = "AMAZON_INSPECTOR2_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_WEB_SERVICE_ROLE_POLICY = "AMAZON_WORK_SPACES_WEB_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_WEB_READ_ONLY = "AMAZON_WORK_SPACES_WEB_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSIPAMSERVICE_ROLE_POLICY = "AWSIPAMSERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_NETWORKS_SERVICE_ROLE_POLICY = "AWSPRIVATE_NETWORKS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DEV_OPS_GURU_CONSOLE_FULL_ACCESS = "AMAZON_DEV_OPS_GURU_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    EC2_FAST_LAUNCH_SERVICE_ROLE_POLICY = "EC2_FAST_LAUNCH_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPP_RUNNER_FULL_ACCESS = "AWSAPP_RUNNER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    APP_RUNNER_NETWORKING_SERVICE_ROLE_POLICY = "APP_RUNNER_NETWORKING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_INSPECTOR2_READ_ONLY_ACCESS = "AMAZON_INSPECTOR2_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_ROLE_POLICY_FOR_S3_RESTORE = "AWSBACKUP_SERVICE_ROLE_POLICY_FOR_S3_RESTORE"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_ROLE_POLICY_FOR_S3_BACKUP = "AWSBACKUP_SERVICE_ROLE_POLICY_FOR_S3_BACKUP"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_GLUE_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_GLUE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_CODE_PIPELINE_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_CODE_PIPELINE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_EVENTS_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_EVENTS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_FIREHOSE_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_FIREHOSE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPP_RUNNER_READ_ONLY_ACCESS = "AWSAPP_RUNNER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIDENTITY_SYNC_FULL_ACCESS = "AWSIDENTITY_SYNC_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIDENTITY_SYNC_READ_ONLY_ACCESS = "AWSIDENTITY_SYNC_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_API_GATEWAY_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_API_GATEWAY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_CLOUDFORMATION_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_CLOUDFORMATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_CODE_BUILD_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_CODE_BUILD_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_LAMBDA_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_SERVICE_CATALOG_PRODUCTS_LAMBDA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EBSCSI_DRIVER_POLICY = "AMAZON_EBSCSI_DRIVER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_SDK_MEDIA_PIPELINES_SERVICE_LINKED_ROLE_POLICY = "AMAZON_CHIME_SDK_MEDIA_PIPELINES_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_PERFORMANCE_INSIGHTS_READ_ONLY = "AMAZON_RDS_PERFORMANCE_INSIGHTS_READ_ONLY"
    '''
    :stability: experimental
    '''
    ROSAMANAGE_SUBSCRIPTION = "ROSAMANAGE_SUBSCRIPTION"
    '''
    :stability: experimental
    '''
    AWSBILLING_CONDUCTOR_FULL_ACCESS = "AWSBILLING_CONDUCTOR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBILLING_CONDUCTOR_READ_ONLY_ACCESS = "AWSBILLING_CONDUCTOR_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWS_GLUE_SESSION_USER_RESTRICTED_SERVICE_ROLE = "AWS_GLUE_SESSION_USER_RESTRICTED_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AWS_GLUE_SESSION_USER_RESTRICTED_POLICY = "AWS_GLUE_SESSION_USER_RESTRICTED_POLICY"
    '''
    :stability: experimental
    '''
    AWS_GLUE_SESSION_USER_RESTRICTED_NOTEBOOK_POLICY = "AWS_GLUE_SESSION_USER_RESTRICTED_NOTEBOOK_POLICY"
    '''
    :stability: experimental
    '''
    AWS_GLUE_SESSION_USER_RESTRICTED_NOTEBOOK_SERVICE_ROLE = "AWS_GLUE_SESSION_USER_RESTRICTED_NOTEBOOK_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_ORCHESTRATOR_SERVICE_ROLE_POLICY = "AWSMIGRATION_HUB_ORCHESTRATOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_ORCHESTRATOR_PLUGIN = "AWSMIGRATION_HUB_ORCHESTRATOR_PLUGIN"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_ORCHESTRATOR_CONSOLE_FULL_ACCESS = "AWSMIGRATION_HUB_ORCHESTRATOR_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMIGRATION_HUB_ORCHESTRATOR_INSTANCE_ROLE_POLICY = "AWSMIGRATION_HUB_ORCHESTRATOR_INSTANCE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    MONITRON_SERVICE_ROLE_POLICY = "MONITRON_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EMR_SERVERLESS_SERVICE_ROLE_POLICY = "AMAZON_EMR_SERVERLESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSBUDGETSACTIONS_ROLEPOLICYFORRESOURCEADMINISTRATIONWITHSSM = "AWSBUDGETSACTIONS_ROLEPOLICYFORRESOURCEADMINISTRATIONWITHSSM"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_STAGING_ACCOUNT_POLICY = "AWSELASTIC_DISASTER_RECOVERY_STAGING_ACCOUNT_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_EC2_INSTANCE_POLICY = "AWSELASTIC_DISASTER_RECOVERY_EC2_INSTANCE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATIONMIGRATIONAGENTPOLICY_V2 = "AWSAPPLICATIONMIGRATIONAGENTPOLICY_V2"
    '''
    :stability: experimental
    '''
    AWSM2_SERVICE_POLICY = "AWSM2_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMANAGED_SERVICES_DEPLOYMENT_TOOLKIT_POLICY = "AWSMANAGED_SERVICES_DEPLOYMENT_TOOLKIT_POLICY"
    '''
    :stability: experimental
    '''
    AWSCLOUDTRAIL_READONLYACCESS = "AWSCLOUDTRAIL_READONLYACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_AGENT_INSTALLATION_POLICY = "AWSAPPLICATION_MIGRATION_AGENT_INSTALLATION_POLICY"
    '''
    :stability: experimental
    '''
    AWSWELL_ARCHITECTED_ORGANIZATIONS_SERVICE_ROLE_POLICY = "AWSWELL_ARCHITECTED_ORGANIZATIONS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSROLES_ANYWHERE_SERVICE_POLICY = "AWSROLES_ANYWHERE_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSNETWORK_MANAGER_CLOUD_WAN_SERVICE_ROLE_POLICY = "AWSNETWORK_MANAGER_CLOUD_WAN_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_GUARD_DUTY_MALWARE_PROTECTION_SERVICE_ROLE_POLICY = "AMAZON_GUARD_DUTY_MALWARE_PROTECTION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSVENDOR_INSIGHTS_VENDOR_FULL_ACCESS = "AWSVENDOR_INSIGHTS_VENDOR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSVENDOR_INSIGHTS_VENDOR_READ_ONLY = "AWSVENDOR_INSIGHTS_VENDOR_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSVENDOR_INSIGHTS_ASSESSOR_FULL_ACCESS = "AWSVENDOR_INSIGHTS_ASSESSOR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSVENDOR_INSIGHTS_ASSESSOR_READ_ONLY = "AWSVENDOR_INSIGHTS_ASSESSOR_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSLICENSE_MANAGER_USER_SUBSCRIPTIONS_SERVICE_ROLE_POLICY = "AWSLICENSE_MANAGER_USER_SUBSCRIPTIONS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSTRUSTED_ADVISOR_PRIORITY_FULL_ACCESS = "AWSTRUSTED_ADVISOR_PRIORITY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSTRUSTED_ADVISOR_PRIORITY_READ_ONLY_ACCESS = "AWSTRUSTED_ADVISOR_PRIORITY_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_DISCOVERY_AGENTLESS_COLLECTOR_ACCESS = "AWSAPPLICATION_DISCOVERY_AGENTLESS_COLLECTOR_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSUPPORT_APP_FULL_ACCESS = "AWSSUPPORT_APP_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSUPPORT_APP_READ_ONLY_ACCESS = "AWSSUPPORT_APP_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_LOCAL_OUTPOST_SERVICE_ROLE_POLICY = "AMAZON_EKS_LOCAL_OUTPOST_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CANVAS_FORECAST_ACCESS = "AMAZON_SAGE_MAKER_CANVAS_FORECAST_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_LOCAL_OUTPOST_CLUSTER_POLICY = "AMAZON_EKS_LOCAL_OUTPOST_CLUSTER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SSM_MANAGED_E_C2_INSTANCE_DEFAULT_POLICY = "AMAZON_SSM_MANAGED_E_C2_INSTANCE_DEFAULT_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CANVAS_FULL_ACCESS = "AMAZON_SAGE_MAKER_CANVAS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CLOUD_WATCH_EVIDENTLY_SERVICE_ROLE_POLICY = "AMAZON_CLOUD_WATCH_EVIDENTLY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDEVICE_FARM_SERVICE_ROLE_POLICY = "AWSDEVICE_FARM_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSIO_T_FLEETWISE_SERVICE_ROLE_POLICY = "AWSIO_T_FLEETWISE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSUPPORT_PLANS_READ_ONLY_ACCESS = "AWSSUPPORT_PLANS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSUPPORT_PLANS_FULL_ACCESS = "AWSSUPPORT_PLANS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    APP_INTEGRATIONS_SERVICE_LINKED_ROLE_POLICY = "APP_INTEGRATIONS_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_APP_STREAM_PCA_ACCESS = "AMAZON_APP_STREAM_PCA_ACCESS"
    '''
    :stability: experimental
    '''
    AWSREFACTORING_TOOLKIT_SIDECAR_POLICY = "AWSREFACTORING_TOOLKIT_SIDECAR_POLICY"
    '''
    :stability: experimental
    '''
    AWSREFACTORING_TOOLKIT_FULL_ACCESS = "AWSREFACTORING_TOOLKIT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_EXPLORER_SERVICE_ROLE_POLICY = "AWSRESOURCE_EXPLORER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSFAULT_INJECTION_SIMULATOR_SSM_ACCESS = "AWSFAULT_INJECTION_SIMULATOR_SSM_ACCESS"
    '''
    :stability: experimental
    '''
    AWSFAULT_INJECTION_SIMULATOR_RDS_ACCESS = "AWSFAULT_INJECTION_SIMULATOR_RDS_ACCESS"
    '''
    :stability: experimental
    '''
    AWSFAULT_INJECTION_SIMULATOR_NETWORK_ACCESS = "AWSFAULT_INJECTION_SIMULATOR_NETWORK_ACCESS"
    '''
    :stability: experimental
    '''
    AWSFAULT_INJECTION_SIMULATOR_EKS_ACCESS = "AWSFAULT_INJECTION_SIMULATOR_EKS_ACCESS"
    '''
    :stability: experimental
    '''
    AWSFAULT_INJECTION_SIMULATOR_ECS_ACCESS = "AWSFAULT_INJECTION_SIMULATOR_ECS_ACCESS"
    '''
    :stability: experimental
    '''
    AWSFAULT_INJECTION_SIMULATOR_E_C2_ACCESS = "AWSFAULT_INJECTION_SIMULATOR_E_C2_ACCESS"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_EXPLORER_READ_ONLY_ACCESS = "AWSRESOURCE_EXPLORER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_EXPLORER_FULL_ACCESS = "AWSRESOURCE_EXPLORER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_WORKSPACES_PCA_ACCESS = "AMAZON_WORKSPACES_PCA_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_GRAFANA_SERVICE_LINKED_ROLE_POLICY = "AMAZON_GRAFANA_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPROTON_CODE_BUILD_PROVISIONING_BASIC_ACCESS = "AWSPROTON_CODE_BUILD_PROVISIONING_BASIC_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPROTON_CODE_BUILD_PROVISIONING_SERVICE_ROLE_POLICY = "AWSPROTON_CODE_BUILD_PROVISIONING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_SCHEDULER_FULL_ACCESS = "AMAZON_EVENT_BRIDGE_SCHEDULER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_SCHEDULER_READ_ONLY_ACCESS = "AMAZON_EVENT_BRIDGE_SCHEDULER_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_RESTORE_ACCESS_FOR_SAPHAN_A = "AWSBACKUP_RESTORE_ACCESS_FOR_SAPHAN_A"
    '''
    :stability: experimental
    '''
    AWSBACKUP_DATA_TRANSFER_ACCESS = "AWSBACKUP_DATA_TRANSFER_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_SYNC_SERVICE_ROLE_POLICY = "AWSSERVICE_CATALOG_SYNC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSSMFOR_SAP_SERVICE_LINKED_ROLE_POLICY = "AWSSSMFOR_SAP_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_FOR_SAP_FULL_ACCESS = "AWSSYSTEMS_MANAGER_FOR_SAP_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_FOR_SAP_READ_ONLY_ACCESS = "AWSSYSTEMS_MANAGER_FOR_SAP_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_INGESTION_SERVICE_ROLE_POLICY = "AMAZON_OPEN_SEARCH_INGESTION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSREACHABILITY_ANALYZER_SERVICE_ROLE_POLICY = "AWSREACHABILITY_ANALYZER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_SERVERLESS_SERVICE_ROLE_POLICY = "AMAZON_OPEN_SEARCH_SERVERLESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_SSM_ACCESS = "AWSAPPLICATION_MIGRATION_SSM_ACCESS"
    '''
    :stability: experimental
    '''
    OAMREAD_ONLY_ACCESS = "OAMREAD_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    OAMFULL_ACCESS = "OAMFULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSXRAY_CROSS_ACCOUNT_SHARING_CONFIGURATION = "AWSXRAY_CROSS_ACCOUNT_SHARING_CONFIGURATION"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_LOGS_CROSS_ACCOUNT_SHARING_CONFIGURATION = "CLOUD_WATCH_LOGS_CROSS_ACCOUNT_SHARING_CONFIGURATION"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_CROSS_ACCOUNT_SHARING_CONFIGURATION = "CLOUD_WATCH_CROSS_ACCOUNT_SHARING_CONFIGURATION"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_INTERNET_MONITOR_SERVICE_ROLE_POLICY = "CLOUD_WATCH_INTERNET_MONITOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSWICKR_FULL_ACCESS = "AWSWICKR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSVPCVERIFIED_ACCESS_SERVICE_ROLE_POLICY = "AWSVPCVERIFIED_ACCESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_OMICS_READ_ONLY_ACCESS = "AMAZON_OMICS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    SECURITY_LAKE_SERVICE_LINKED_ROLE = "SECURITY_LAKE_SERVICE_LINKED_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_SECURITY_LAKE_PERMISSIONS_BOUNDARY = "AMAZON_SECURITY_LAKE_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_MODEL_GOVERNANCE_USE_ACCESS = "AMAZON_SAGE_MAKER_MODEL_GOVERNANCE_USE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_GEOSPATIAL_FULL_ACCESS = "AMAZON_SAGE_MAKER_GEOSPATIAL_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_GEOSPATIAL_EXECUTION_ROLE = "AMAZON_SAGE_MAKER_GEOSPATIAL_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AMAZONDOCDB_ELASTICSERVICEROLEPOLICY = "AMAZONDOCDB_ELASTICSERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWSVPC_LATTICE_SERVICE_ROLE_POLICY = "AWSVPC_LATTICE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_PIPES_FULL_ACCESS = "AMAZON_EVENT_BRIDGE_PIPES_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_PIPES_READ_ONLY_ACCESS = "AMAZON_EVENT_BRIDGE_PIPES_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EVENT_BRIDGE_PIPES_OPERATOR_ACCESS = "AMAZON_EVENT_BRIDGE_PIPES_OPERATOR_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_GROUND_STATION_DATAFLOW_ENDPOINT_GROUP_POLICY = "AWSSERVICE_ROLE_FOR_GROUND_STATION_DATAFLOW_ENDPOINT_GROUP_POLICY"
    '''
    :stability: experimental
    '''
    AWSBACKUP_GATEWAY_SERVICE_ROLE_POLICY_FOR_VIRTUAL_MACHINE_METADATA_SYNC = "AWSBACKUP_GATEWAY_SERVICE_ROLE_POLICY_FOR_VIRTUAL_MACHINE_METADATA_SYNC"
    '''
    :stability: experimental
    '''
    AWSMANAGEDSERVICES_DETECTIVECONTROLSCONFIG_SERVICEROLEPOLICY = "AWSMANAGEDSERVICES_DETECTIVECONTROLSCONFIG_SERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWSLICENSE_MANAGER_LINUX_SUBSCRIPTIONS_SERVICE_ROLE_POLICY = "AWSLICENSE_MANAGER_LINUX_SUBSCRIPTIONS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSOUTPOSTS_AUTHORIZE_SERVER_POLICY = "AWSOUTPOSTS_AUTHORIZE_SERVER_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTICDISASTERRECOVERYSTAGINGACCOUNTPOLICY_V2 = "AWSELASTICDISASTERRECOVERYSTAGINGACCOUNTPOLICY_V2"
    '''
    :stability: experimental
    '''
    RESOURCE_GROUPS_SERVICE_ROLE_POLICY = "RESOURCE_GROUPS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSCLEAN_ROOMS_READ_ONLY_ACCESS = "AWSCLEAN_ROOMS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLEAN_ROOMS_FULL_ACCESS = "AWSCLEAN_ROOMS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLEAN_ROOMS_FULL_ACCESS_NO_QUERYING = "AWSCLEAN_ROOMS_FULL_ACCESS_NO_QUERYING"
    '''
    :stability: experimental
    '''
    AWSHEALTH_EVENTPROCESSORSERVICEROLEPOLICY = "AWSHEALTH_EVENTPROCESSORSERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DETECTIVE_MEMBER_ACCESS = "AMAZON_DETECTIVE_MEMBER_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DETECTIVE_INVESTIGATOR_ACCESS = "AMAZON_DETECTIVE_INVESTIGATOR_ACCESS"
    '''
    :stability: experimental
    '''
    EC2_INSTANCE_CONNECT_ENDPOINT = "EC2_INSTANCE_CONNECT_ENDPOINT"
    '''
    :stability: experimental
    '''
    AMAZON_COGNITO_UNAUTHENTICATED_IDENTITIES = "AMAZON_COGNITO_UNAUTHENTICATED_IDENTITIES"
    '''
    :stability: experimental
    '''
    AWSMANAGEDSERVICES_EVENTSSERVICEROLEPOLICY = "AWSMANAGEDSERVICES_EVENTSSERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_CA_USER = "AWSPRIVATE_CA_USER"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_CA_FULL_ACCESS = "AWSPRIVATE_CA_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_CA_PRIVILEGED_USER = "AWSPRIVATE_CA_PRIVILEGED_USER"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_CA_READ_ONLY = "AWSPRIVATE_CA_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_CA_AUDITOR = "AWSPRIVATE_CA_AUDITOR"
    '''
    :stability: experimental
    '''
    AMAZON_OMICS_FULL_ACCESS = "AMAZON_OMICS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSUPPLY_CHAIN_FEDERATION_ADMIN_ACCESS = "AWSSUPPLY_CHAIN_FEDERATION_ADMIN_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DETECTIVE_ORGANIZATIONS_ACCESS = "AMAZON_DETECTIVE_ORGANIZATIONS_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CHIME_SDK_MESSAGING_SERVICE_ROLE_POLICY = "AMAZON_CHIME_SDK_MESSAGING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDMSFLEET_ADVISOR_SERVICE_ROLE_POLICY = "AWSDMSFLEET_ADVISOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CUSTOMER_PROFILES_SERVICE_LINKED_ROLE_POLICY = "CUSTOMER_PROFILES_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDATA_SYNC_DISCOVERY_SERVICE_ROLE_POLICY = "AWSDATA_SYNC_DISCOVERY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    MEDIA_CONNECT_GATEWAY_INSTANCE_ROLE_POLICY = "MEDIA_CONNECT_GATEWAY_INSTANCE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMANAGEDSERVICES_CONTACTSSERVICEROLEPOLICY = "AWSMANAGEDSERVICES_CONTACTSSERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CANVAS_AI_SERVICES_ACCESS = "AMAZON_SAGE_MAKER_CANVAS_AI_SERVICES_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_CODE_WHISPERER_POLICY = "AWSSERVICE_ROLE_FOR_CODE_WHISPERER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_GRAFANA_CLOUD_WATCH_ACCESS = "AMAZON_GRAFANA_CLOUD_WATCH_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGROUND_STATION_AGENT_INSTANCE_POLICY = "AWSGROUND_STATION_AGENT_INSTANCE_POLICY"
    '''
    :stability: experimental
    '''
    VPCLATTICE_SERVICES_INVOKE_ACCESS = "VPCLATTICE_SERVICES_INVOKE_ACCESS"
    '''
    :stability: experimental
    '''
    VPCLATTICE_READ_ONLY_ACCESS = "VPCLATTICE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    VPCLATTICE_FULL_ACCESS = "VPCLATTICE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMIGRATIONHUBREFACTORSPACES_ENVIRONMENTSWITHOUTBRIDGESFULLACCESS = "AWSMIGRATIONHUBREFACTORSPACES_ENVIRONMENTSWITHOUTBRIDGESFULLACCESS"
    '''
    :stability: experimental
    '''
    AWSMEDIA_CONNECT_SERVICE_POLICY = "AWSMEDIA_CONNECT_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPROTON_SERVICE_GIT_SYNC_SERVICE_ROLE_POLICY = "AWSPROTON_SERVICE_GIT_SYNC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_CATALOG_ORGS_DATA_SYNC_SERVICE_ROLE_POLICY = "AWSSERVICE_CATALOG_ORGS_DATA_SYNC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_MODEL_REGISTRY_FULL_ACCESS = "AMAZON_SAGE_MAKER_MODEL_REGISTRY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSUSER_NOTIFICATIONS_SERVICE_LINKED_ROLE_POLICY = "AWSUSER_NOTIFICATIONS_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_CATALYST_SUPPORT_ACCESS = "AMAZON_CODE_CATALYST_SUPPORT_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_CATALYST_READ_ONLY_ACCESS = "AMAZON_CODE_CATALYST_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_CATALYST_FULL_ACCESS = "AMAZON_CODE_CATALYST_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    ROSACLOUD_NETWORK_CONFIG_OPERATOR_POLICY = "ROSACLOUD_NETWORK_CONFIG_OPERATOR_POLICY"
    '''
    :stability: experimental
    '''
    ROSAWORKER_INSTANCE_POLICY = "ROSAWORKER_INSTANCE_POLICY"
    '''
    :stability: experimental
    '''
    ROSAAMAZON_EBSCSI_DRIVER_OPERATOR_POLICY = "ROSAAMAZON_EBSCSI_DRIVER_OPERATOR_POLICY"
    '''
    :stability: experimental
    '''
    ROSAINGRESS_OPERATOR_POLICY = "ROSAINGRESS_OPERATOR_POLICY"
    '''
    :stability: experimental
    '''
    ROSACONTROL_PLANE_OPERATOR_POLICY = "ROSACONTROL_PLANE_OPERATOR_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_INGESTION_READ_ONLY_ACCESS = "AMAZON_OPEN_SEARCH_INGESTION_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_INGESTION_FULL_ACCESS = "AMAZON_OPEN_SEARCH_INGESTION_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSWELL_ARCHITECTED_DISCOVERY_SERVICE_ROLE_POLICY = "AWSWELL_ARCHITECTED_DISCOVERY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    ROSAKUBE_CONTROLLER_POLICY = "ROSAKUBE_CONTROLLER_POLICY"
    '''
    :stability: experimental
    '''
    ROSAKMSPROVIDER_POLICY = "ROSAKMSPROVIDER_POLICY"
    '''
    :stability: experimental
    '''
    ROSAIMAGE_REGISTRY_OPERATOR_POLICY = "ROSAIMAGE_REGISTRY_OPERATOR_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_VPC_REACHABILITY_ANALYZER_PATH_COMPONENT_READ_POLICY = "AMAZON_VPC_REACHABILITY_ANALYZER_PATH_COMPONENT_READ_POLICY"
    '''
    :stability: experimental
    '''
    KEYSPACES_REPLICATION_SERVICE_ROLE_POLICY = "KEYSPACES_REPLICATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_GURU_SECURITY_SCAN_ACCESS = "AMAZON_CODE_GURU_SECURITY_SCAN_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CODE_GURU_SECURITY_FULL_ACCESS = "AMAZON_CODE_GURU_SECURITY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSFIN_SPACE_SERVICE_ROLE_POLICY = "AWSFIN_SPACE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_CROSS_ACCOUNT_REPLICATION_POLICY = "AWSELASTIC_DISASTER_RECOVERY_CROSS_ACCOUNT_REPLICATION_POLICY"
    '''
    :stability: experimental
    '''
    AWSDMSSERVERLESS_SERVICE_ROLE_POLICY = "AWSDMSSERVERLESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SECURITY_LAKE_ADMINISTRATOR = "AMAZON_SECURITY_LAKE_ADMINISTRATOR"
    '''
    :stability: experimental
    '''
    ROSASRESUPPORT_POLICY = "ROSASRESUPPORT_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DOC_DB_ELASTIC_FULL_ACCESS = "AMAZON_DOC_DB_ELASTIC_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCONTROL_TOWER_ACCOUNT_SERVICE_ROLE_POLICY = "AWSCONTROL_TOWER_ACCOUNT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    ROSAINSTALLER_POLICY = "ROSAINSTALLER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DOC_DB_ELASTIC_READ_ONLY_ACCESS = "AMAZON_DOC_DB_ELASTIC_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    ROSANODE_POOL_MANAGEMENT_POLICY = "ROSANODE_POOL_MANAGEMENT_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_NETWORK_REPLICATION_POLICY = "AWSELASTIC_DISASTER_RECOVERY_NETWORK_REPLICATION_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_VPC_REACHABILITY_ANALYZER_FULL_ACCESS_POLICY = "AMAZON_VPC_REACHABILITY_ANALYZER_FULL_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_MACIE_READ_ONLY_ACCESS = "AMAZON_MACIE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_VPC_NETWORK_ACCESS_ANALYZER_FULL_ACCESS_POLICY = "AMAZON_VPC_NETWORK_ACCESS_ANALYZER_FULL_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    EMRDESCRIBE_CLUSTER_POLICY_FOR_EMRWA_L = "EMRDESCRIBE_CLUSTER_POLICY_FOR_EMRWA_L"
    '''
    :stability: experimental
    '''
    AWSAPP_FABRIC_SERVICE_ROLE_POLICY = "AWSAPP_FABRIC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSRESILIENCE_HUB_ASSSESSMENT_EXECUTION_POLICY = "AWSRESILIENCE_HUB_ASSSESSMENT_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPP_FABRIC_FULL_ACCESS = "AWSAPP_FABRIC_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSAPP_FABRIC_READ_ONLY_ACCESS = "AWSAPP_FABRIC_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_COGNITO_UN_AUTHED_IDENTITIES_SESSION_POLICY = "AMAZON_COGNITO_UN_AUTHED_IDENTITIES_SESSION_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EFSCSI_DRIVER_POLICY = "AMAZON_EFSCSI_DRIVER_POLICY"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_PACKAGE_V2_FULL_ACCESS = "AWSELEMENTAL_MEDIA_PACKAGE_V2_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_PACKAGE_V2_READ_ONLY = "AWSELEMENTAL_MEDIA_PACKAGE_V2_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSHEALTH_IMAGING_FULL_ACCESS = "AWSHEALTH_IMAGING_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSHEALTH_IMAGING_READ_ONLY_ACCESS = "AWSHEALTH_IMAGING_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_FULL_ACCESS_V2 = "CLOUD_WATCH_FULL_ACCESS_V2"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_PARTNER_SERVICE_CATALOG_PRODUCTS_LAMBDA_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_PARTNER_SERVICE_CATALOG_PRODUCTS_LAMBDA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_PARTNER_SERVICE_CATALOG_PRODUCTS_API_GATEWAY_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_PARTNER_SERVICE_CATALOG_PRODUCTS_API_GATEWAY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_PARTNER_SERVICE_CATALOG_PRODUCTS_CLOUD_FORMATION_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_PARTNER_SERVICE_CATALOG_PRODUCTS_CLOUD_FORMATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMIGRATIONHUBREFACTORSPACES_SSMAUTOMATIONPOLICY = "AWSMIGRATIONHUBREFACTORSPACES_SSMAUTOMATIONPOLICY"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_PERFORMANCE_INSIGHTS_FULL_ACCESS = "AMAZON_RDS_PERFORMANCE_INSIGHTS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSENTITY_RESOLUTION_CONSOLE_FULL_ACCESS = "AWSENTITY_RESOLUTION_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSENTITY_RESOLUTION_CONSOLE_READ_ONLY_ACCESS = "AWSENTITY_RESOLUTION_CONSOLE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSARTIFACT_SERVICE_ROLE_POLICY = "AWSARTIFACT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_SERVICE_EC2_INSTANCE_POLICY = "AWSAPPLICATION_MIGRATION_SERVICE_EC2_INSTANCE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_LAUNCH_WIZARD_FULL_ACCESS_V2 = "AMAZON_LAUNCH_WIZARD_FULL_ACCESS_V2"
    '''
    :stability: experimental
    '''
    AWSSERVICEROLEFORCLOUDWATCHMETRICS_DBPERFINSIGHTSSERVICEROLEPOLICY = "AWSSERVICEROLEFORCLOUDWATCHMETRICS_DBPERFINSIGHTSSERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_ENVIRONMENT_ROLE_PERMISSIONS_BOUNDARY = "AMAZON_DATA_ZONE_ENVIRONMENT_ROLE_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AMAZONKEYSPACESREADONLYACCESS_V2 = "AMAZONKEYSPACESREADONLYACCESS_V2"
    '''
    :stability: experimental
    '''
    AWSELASTIC_DISASTER_RECOVERY_LAUNCH_ACTIONS_POLICY = "AWSELASTIC_DISASTER_RECOVERY_LAUNCH_ACTIONS_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_FULL_ACCESS = "AMAZON_DATA_ZONE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_REDSHIFT_MANAGE_ACCESS_ROLE_POLICY = "AMAZON_DATA_ZONE_REDSHIFT_MANAGE_ACCESS_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_REDSHIFT_GLUE_PROVISIONING_POLICY = "AMAZON_DATA_ZONE_REDSHIFT_GLUE_PROVISIONING_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_GLUE_MANAGE_ACCESS_ROLE_POLICY = "AMAZON_DATA_ZONE_GLUE_MANAGE_ACCESS_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_FULL_USER_ACCESS = "AMAZON_DATA_ZONE_FULL_USER_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_DOMAIN_EXECUTION_ROLE_POLICY = "AMAZON_DATA_ZONE_DOMAIN_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSS3_ON_OUTPOSTS_SERVICE_ROLE_POLICY = "AWSS3_ON_OUTPOSTS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CANVAS_DIRECT_DEPLOY_ACCESS = "AMAZON_SAGE_MAKER_CANVAS_DIRECT_DEPLOY_ACCESS"
    '''
    :stability: experimental
    '''
    AMPLIFY_BACKEND_DEPLOY_FULL_ACCESS = "AMPLIFY_BACKEND_DEPLOY_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_CONNECT_SYNCHRONIZATION_SERVICE_ROLE_POLICY = "AMAZON_CONNECT_SYNCHRONIZATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CANVAS_DATA_PREP_FULL_ACCESS = "AMAZON_SAGE_MAKER_CANVAS_DATA_PREP_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATA_LIFECYCLE_MANAGER_SSM_FULL_ACCESS = "AWSDATA_LIFECYCLE_MANAGER_SSM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIAMIDENTITY_CENTER_ALLOW_LIST_FOR_IDENTITY_CONTEXT = "AWSIAMIDENTITY_CENTER_ALLOW_LIST_FOR_IDENTITY_CONTEXT"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_APPLICATION_SIGNALS_SERVICE_ROLE_POLICY = "CLOUD_WATCH_APPLICATION_SIGNALS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    PARTNER_CENTRAL_ACCOUNT_MANAGEMENT_USER_ROLE_ASSOCIATION = "PARTNER_CENTRAL_ACCOUNT_MANAGEMENT_USER_ROLE_ASSOCIATION"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_POLICY_FOR_BACKUP_RESTORE_TESTING = "AWSSERVICE_ROLE_POLICY_FOR_BACKUP_RESTORE_TESTING"
    '''
    :stability: experimental
    '''
    AWSINCIDENT_MANAGER_INCIDENT_ACCESS_SERVICE_ROLE_POLICY = "AWSINCIDENT_MANAGER_INCIDENT_ACCESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSIO_T_TWIN_MAKER_SERVICE_ROLE_POLICY = "AWSIO_T_TWIN_MAKER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSRESOURCE_EXPLORER_ORGANIZATIONS_ACCESS = "AWSRESOURCE_EXPLORER_ORGANIZATIONS_ACCESS"
    '''
    :stability: experimental
    '''
    AWSRE_POST_PRIVATE_CLOUD_WATCH_ACCESS = "AWSRE_POST_PRIVATE_CLOUD_WATCH_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_DEPLOYMENT_SERVICE_ROLE_POLICY = "AWSMARKETPLACE_DEPLOYMENT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSGIT_SYNC_SERVICE_ROLE_POLICY = "AWSGIT_SYNC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    EC2_IMAGE_BUILDER_LIFECYCLE_EXECUTION_POLICY = "EC2_IMAGE_BUILDER_LIFECYCLE_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_INSPECTOR2_AGENTLESS_SERVICE_ROLE_POLICY = "AMAZON_INSPECTOR2_AGENTLESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    COST_OPTIMIZATION_HUB_SERVICE_ROLE_POLICY = "COST_OPTIMIZATION_HUB_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_PROMETHEUS_SCRAPER_SERVICE_ROLE_POLICY = "AMAZON_PROMETHEUS_SCRAPER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSREPOST_SPACE_SUPPORT_OPERATIONS_POLICY = "AWSREPOST_SPACE_SUPPORT_OPERATIONS_POLICY"
    '''
    :stability: experimental
    '''
    AWSELASTICDISASTERRECOVERYCONSOLEFULLACCESS_V2 = "AWSELASTICDISASTERRECOVERYCONSOLEFULLACCESS_V2"
    '''
    :stability: experimental
    '''
    AMAZON_ONE_ENTERPRISE_FULL_ACCESS = "AMAZON_ONE_ENTERPRISE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ONE_ENTERPRISE_READ_ONLY_ACCESS = "AMAZON_ONE_ENTERPRISE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ONE_ENTERPRISE_INSTALLER_ACCESS = "AMAZON_ONE_ENTERPRISE_INSTALLER_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_Q_FULL_ACCESS = "AMAZON_Q_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_NEPTUNE_GRAPH_POLICY = "AWSSERVICE_ROLE_FOR_NEPTUNE_GRAPH_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CLUSTER_INSTANCE_ROLE_POLICY = "AMAZON_SAGE_MAKER_CLUSTER_INSTANCE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSZONAL_AUTOSHIFT_PRACTICE_RUN_SLR_POLICY = "AWSZONAL_AUTOSHIFT_PRACTICE_RUN_SLR_POLICY"
    '''
    :stability: experimental
    '''
    AWSCLEAN_ROOMS_ML_READ_ONLY_ACCESS = "AWSCLEAN_ROOMS_ML_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLEAN_ROOMS_ML_FULL_ACCESS = "AWSCLEAN_ROOMS_ML_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    NEPTUNE_GRAPH_READ_ONLY_ACCESS = "NEPTUNE_GRAPH_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    IVSREAD_ONLY_ACCESS = "IVSREAD_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMSKREPLICATOR_EXECUTION_ROLE = "AWSMSKREPLICATOR_EXECUTION_ROLE"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_FULL_ACCESS = "AMAZON_BEDROCK_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_READ_ONLY = "AMAZON_BEDROCK_READ_ONLY"
    '''
    :stability: experimental
    '''
    COST_OPTIMIZATION_HUB_READ_ONLY_ACCESS = "COST_OPTIMIZATION_HUB_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    IVSFULL_ACCESS = "IVSFULL_ACCESS"
    '''
    :stability: experimental
    '''
    COST_OPTIMIZATION_HUB_ADMIN_ACCESS = "COST_OPTIMIZATION_HUB_ADMIN_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_NETWORK_MONITOR_SERVICE_ROLE_POLICY = "CLOUD_WATCH_NETWORK_MONITOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_DASHBOARDS_SERVICE_ROLE_POLICY = "AMAZON_OPEN_SEARCH_DASHBOARDS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSARTIFACT_REPORTS_READ_ONLY_ACCESS = "AWSARTIFACT_REPORTS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSGRAFANA_WORKSPACE_PERMISSION_MANAGEMENT_V2 = "AWSGRAFANA_WORKSPACE_PERMISSION_MANAGEMENT_V2"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_VOLUMES = "AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_VOLUMES"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_SERVICE_CONNECT_TRANSPORT_LAYER_SECURITY = "AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_SERVICE_CONNECT_TRANSPORT_LAYER_SECURITY"
    '''
    :stability: experimental
    '''
    AMAZON_SECURITY_LAKE_METASTORE_MANAGER = "AMAZON_SECURITY_LAKE_METASTORE_MANAGER"
    '''
    :stability: experimental
    '''
    AMAZON_INSPECTOR2_MANAGED_CIS_POLICY = "AMAZON_INSPECTOR2_MANAGED_CIS_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_LEX_REPLICATION_POLICY = "AMAZON_LEX_REPLICATION_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CANVAS_BEDROCK_ACCESS = "AMAZON_SAGE_MAKER_CANVAS_BEDROCK_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_PRIVATE_MARKETPLACE_ADMIN_POLICY = "AWSSERVICE_ROLE_FOR_PRIVATE_MARKETPLACE_ADMIN_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_RDS_CUSTOM_INSTANCE_PROFILE_ROLE_POLICY = "AMAZON_RDS_CUSTOM_INSTANCE_PROFILE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_RESALE_AUTHORIZATION_SERVICE_ROLE_POLICY = "AWSMARKETPLACE_RESALE_AUTHORIZATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_TIMESTREAM_INFLUX_DB_SERVICE_ROLE_POLICY = "AMAZON_TIMESTREAM_INFLUX_DB_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_TIMESTREAM_INFLUX_DB_FULL_ACCESS = "AMAZON_TIMESTREAM_INFLUX_DB_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSEC2_VSS_SNAPSHOT_POLICY = "AWSEC2_VSS_SNAPSHOT_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_ASSET_BUNDLE_EXPORT_POLICY = "AWSQUICK_SIGHT_ASSET_BUNDLE_EXPORT_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_ASSET_BUNDLE_IMPORT_POLICY = "AWSQUICK_SIGHT_ASSET_BUNDLE_IMPORT_POLICY"
    '''
    :stability: experimental
    '''
    AWSDEADLINECLOUD_USERACCESSFARMS = "AWSDEADLINECLOUD_USERACCESSFARMS"
    '''
    :stability: experimental
    '''
    AWSDEADLINECLOUD_USERACCESSFLEETS = "AWSDEADLINECLOUD_USERACCESSFLEETS"
    '''
    :stability: experimental
    '''
    AWSDEADLINECLOUD_USERACCESSJOBS = "AWSDEADLINECLOUD_USERACCESSJOBS"
    '''
    :stability: experimental
    '''
    AWSDEADLINECLOUD_USERACCESSQUEUES = "AWSDEADLINECLOUD_USERACCESSQUEUES"
    '''
    :stability: experimental
    '''
    AWSDEADLINECLOUD_FLEETWORKER = "AWSDEADLINECLOUD_FLEETWORKER"
    '''
    :stability: experimental
    '''
    AWSDEADLINECLOUD_WORKERHOST = "AWSDEADLINECLOUD_WORKERHOST"
    '''
    :stability: experimental
    '''
    SPLIT_COST_ALLOCATION_DATA_SERVICE_ROLE_POLICY = "SPLIT_COST_ALLOCATION_DATA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_SAGE_MAKER_ENVIRONMENT_ROLE_PERMISSIONS_BOUNDARY = "AMAZON_DATA_ZONE_SAGE_MAKER_ENVIRONMENT_ROLE_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_SAGE_MAKER_PROVISIONING_ROLE_POLICY = "AMAZON_DATA_ZONE_SAGE_MAKER_PROVISIONING_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_SAGE_MAKER_MANAGE_ACCESS_ROLE_POLICY = "AMAZON_DATA_ZONE_SAGE_MAKER_MANAGE_ACCESS_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_AMAZON_Q_DEVELOPER = "AWSSERVICE_ROLE_FOR_AMAZON_Q_DEVELOPER"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_USER_SUBSCRIPTIONS = "AWSSERVICE_ROLE_FOR_USER_SUBSCRIPTIONS"
    '''
    :stability: experimental
    '''
    QBUSINESS_SERVICE_ROLE_POLICY = "QBUSINESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_PROFILES_READ_ONLY_ACCESS = "AMAZON_ROUTE53_PROFILES_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ROUTE53_PROFILES_FULL_ACCESS = "AMAZON_ROUTE53_PROFILES_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_OPEN_SEARCH_DIRECT_QUERY_GLUE_CREATE_ACCESS = "AMAZON_OPEN_SEARCH_DIRECT_QUERY_GLUE_CREATE_ACCESS"
    '''
    :stability: experimental
    '''
    EC2_FAST_LAUNCH_FULL_ACCESS = "EC2_FAST_LAUNCH_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SES_SERVICE_ROLE_POLICY = "AMAZON_SES_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_APPLICATION_SIGNALS_READ_ONLY_ACCESS = "CLOUD_WATCH_APPLICATION_SIGNALS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_APPLICATION_SIGNALS_FULL_ACCESS = "CLOUD_WATCH_APPLICATION_SIGNALS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBCMDATA_EXPORTS_SERVICE_ROLE_POLICY = "AWSBCMDATA_EXPORTS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    OPENSEARCH_INGESTION_SELF_MANAGED_VPCE_POLICY = "OPENSEARCH_INGESTION_SELF_MANAGED_VPCE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_AUTOSCALING_WORK_SPACES_POOL_POLICY = "AWSAPPLICATION_AUTOSCALING_WORK_SPACES_POOL_POLICY"
    '''
    :stability: experimental
    '''
    ECRTEMPLATE_SERVICE_ROLE_POLICY = "ECRTEMPLATE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_SECURE_BROWSER_READ_ONLY = "AMAZON_WORK_SPACES_SECURE_BROWSER_READ_ONLY"
    '''
    :stability: experimental
    '''
    SSMQUICK_SETUP_ROLE_POLICY = "SSMQUICK_SETUP_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_PATCH_POLICY_BASELINE_ACCESS = "AWSQUICK_SETUP_PATCH_POLICY_BASELINE_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_ENABLE_CONFIG_RECORDING_EXECUTION_POLICY = "AWSSYSTEMS_MANAGER_ENABLE_CONFIG_RECORDING_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_ENABLE_EXPLORER_EXECUTION_POLICY = "AWSSYSTEMS_MANAGER_ENABLE_EXPLORER_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_DEV_OPS_GURU_PERMISSIONS_BOUNDARY = "AWSQUICK_SETUP_DEV_OPS_GURU_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_PATCH_POLICY_PERMISSIONS_BOUNDARY = "AWSQUICK_SETUP_PATCH_POLICY_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_SSM_HOST_MGMT_PERMISSIONS_BOUNDARY = "AWSQUICK_SETUP_SSM_HOST_MGMT_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_DISTRIBUTOR_PERMISSIONS_BOUNDARY = "AWSQUICK_SETUP_DISTRIBUTOR_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_CFGC_PACKS_PERMISSIONS_BOUNDARY = "AWSQUICK_SETUP_CFGC_PACKS_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_SCHEDULER_PERMISSIONS_BOUNDARY = "AWSQUICK_SETUP_SCHEDULER_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_DEPLOYMENT_ROLE_POLICY = "AWSQUICK_SETUP_DEPLOYMENT_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_PATCH_POLICY_DEPLOYMENT_ROLE_POLICY = "AWSQUICK_SETUP_PATCH_POLICY_DEPLOYMENT_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_POOL_SERVICE_ACCESS = "AMAZON_WORK_SPACES_POOL_SERVICE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_Q_DEVELOPER_ACCESS = "AMAZON_Q_DEVELOPER_ACCESS"
    '''
    :stability: experimental
    '''
    APP_STUDIO_SERVICE_ROLE_POLICY = "APP_STUDIO_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_THIN_CLIENT_READ_ONLY_ACCESS = "AMAZON_WORK_SPACES_THIN_CLIENT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CANVAS_EMR_SERVERLESS_EXECUTION_ROLE_POLICY = "AMAZON_SAGE_MAKER_CANVAS_EMR_SERVERLESS_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_STUDIO_PERMISSIONS_BOUNDARY = "AMAZON_BEDROCK_STUDIO_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_THIN_CLIENT_FULL_ACCESS = "AMAZON_WORK_SPACES_THIN_CLIENT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCOMPROMISED_KEY_QUARANTINE_V3 = "AWSCOMPROMISED_KEY_QUARANTINE_V3"
    '''
    :stability: experimental
    '''
    AWSPCSSERVICE_ROLE_POLICY = "AWSPCSSERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_HYPER_POD_SERVICE_ROLE_POLICY = "AMAZON_SAGE_MAKER_HYPER_POD_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDIRECTORY_SERVICE_DATA_FULL_ACCESS = "AWSDIRECTORY_SERVICE_DATA_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDIRECTORY_SERVICE_DATA_READ_ONLY_ACCESS = "AWSDIRECTORY_SERVICE_DATA_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    QAPPS_SERVICE_ROLE_POLICY = "QAPPS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_WORKER_NODE_MINIMAL_POLICY = "AMAZON_EKS_WORKER_NODE_MINIMAL_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_PROCUREMENT_INSIGHTS_POLICY = "AWSSERVICE_ROLE_FOR_PROCUREMENT_INSIGHTS_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_CONTAINER_REGISTRY_PULL_ONLY = "AMAZON_E_C2_CONTAINER_REGISTRY_PULL_ONLY"
    '''
    :stability: experimental
    '''
    AWSDATA_SYNC_SERVICE_ROLE_POLICY = "AWSDATA_SYNC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSDATA_EXCHANGE_SERVICE_ROLE_POLICY_FOR_ORGANIZATION_DISCOVERY = "AWSDATA_EXCHANGE_SERVICE_ROLE_POLICY_FOR_ORGANIZATION_DISCOVERY"
    '''
    :stability: experimental
    '''
    AWSDATA_EXCHANGE_SERVICE_ROLE_POLICY_FOR_LICENSE_MANAGEMENT = "AWSDATA_EXCHANGE_SERVICE_ROLE_POLICY_FOR_LICENSE_MANAGEMENT"
    '''
    :stability: experimental
    '''
    AWSSOCIAL_MESSAGING_SERVICE_ROLE_POLICY = "AWSSOCIAL_MESSAGING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    RESOURCE_GROUPS_TAGGING_API_TAG_UNTAG_SUPPORTED_RESOURCES = "RESOURCE_GROUPS_TAGGING_API_TAG_UNTAG_SUPPORTED_RESOURCES"
    '''
    :stability: experimental
    '''
    AMAZON_VERIFIED_PERMISSIONS_FULL_ACCESS = "AMAZON_VERIFIED_PERMISSIONS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_VERIFIED_PERMISSIONS_READ_ONLY_ACCESS = "AMAZON_VERIFIED_PERMISSIONS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_LAMBDA_APPLICATION_SIGNALS_EXECUTION_ROLE_POLICY = "CLOUD_WATCH_LAMBDA_APPLICATION_SIGNALS_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_INTERNET_MONITOR_FULL_ACCESS = "CLOUD_WATCH_INTERNET_MONITOR_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATA_EXCHANGE_DATA_GRANT_OWNER_FULL_ACCESS = "AWSDATA_EXCHANGE_DATA_GRANT_OWNER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDATA_EXCHANGE_DATA_GRANT_RECEIVER_FULL_ACCESS = "AWSDATA_EXCHANGE_DATA_GRANT_RECEIVER_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCLOUD_FRONT_VPC_ORIGIN_SERVICE_ROLE_POLICY = "AWSCLOUD_FRONT_VPC_ORIGIN_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_NETWORKING_POLICY = "AMAZON_EKS_NETWORKING_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_LOAD_BALANCING_POLICY = "AMAZON_EKS_LOAD_BALANCING_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_BLOCK_STORAGE_POLICY = "AMAZON_EKS_BLOCK_STORAGE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_COMPUTE_POLICY = "AMAZON_EKS_COMPUTE_POLICY"
    '''
    :stability: experimental
    '''
    GAME_LIFT_CONTAINER_FLEET_POLICY = "GAME_LIFT_CONTAINER_FLEET_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_BEDROCK_MODEL_MANAGEMENT_POLICY = "AMAZON_DATA_ZONE_BEDROCK_MODEL_MANAGEMENT_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_DATA_ZONE_BEDROCK_MODEL_CONSUMPTION_POLICY = "AMAZON_DATA_ZONE_BEDROCK_MODEL_CONSUMPTION_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_INTERNET_MONITOR_READ_ONLY_ACCESS = "CLOUD_WATCH_INTERNET_MONITOR_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_ODB_SERVICE_ROLE_POLICY = "AMAZON_ODB_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SMSVOICE_SERVICE_ROLE_POLICY = "SMSVOICE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPARTNER_CENTRAL_OPPORTUNITY_MANAGEMENT = "AWSPARTNER_CENTRAL_OPPORTUNITY_MANAGEMENT"
    '''
    :stability: experimental
    '''
    AWSPARTNER_CENTRAL_SANDBOX_FULL_ACCESS = "AWSPARTNER_CENTRAL_SANDBOX_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    SECURITY_LAKE_RESOURCE_MANAGEMENT_SERVICE_ROLE_POLICY = "SECURITY_LAKE_RESOURCE_MANAGEMENT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SQSUNLOCK_QUEUE_POLICY = "SQSUNLOCK_QUEUE_POLICY"
    '''
    :stability: experimental
    '''
    S3_UNLOCK_BUCKET_POLICY = "S3_UNLOCK_BUCKET_POLICY"
    '''
    :stability: experimental
    '''
    IAMAUDIT_ROOT_USER_CREDENTIALS = "IAMAUDIT_ROOT_USER_CREDENTIALS"
    '''
    :stability: experimental
    '''
    IAMCREATE_ROOT_USER_PASSWORD = "IAMCREATE_ROOT_USER_PASSWORD"
    '''
    :stability: experimental
    '''
    IAMDELETE_ROOT_USER_CREDENTIALS = "IAMDELETE_ROOT_USER_CREDENTIALS"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_VPC_LATTICE = "AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_VPC_LATTICE"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_ENABLE_DHMC_EXECUTION_POLICY = "AWSQUICK_SETUP_ENABLE_DHMC_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_MANAGED_INSTANCE_PROFILE_EXECUTION_POLICY = "AWSQUICK_SETUP_MANAGED_INSTANCE_PROFILE_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_SSM_LIFECYCLE_MANAGEMENT_EXECUTION_POLICY = "AWSQUICK_SETUP_SSM_LIFECYCLE_MANAGEMENT_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_SSM_DEPLOYMENT_S3_BUCKET_ROLE_POLICY = "AWSQUICK_SETUP_SSM_DEPLOYMENT_S3_BUCKET_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_ENABLE_AREX_EXECUTION_POLICY = "AWSQUICK_SETUP_ENABLE_AREX_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_SSM_MANAGE_RESOURCES_EXECUTION_POLICY = "AWSQUICK_SETUP_SSM_MANAGE_RESOURCES_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_SSM_DEPLOYMENT_ROLE_POLICY = "AWSQUICK_SETUP_SSM_DEPLOYMENT_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWS_SSM_AUTOMATION_DIAGNOSISBUCKETPOLICY = "AWS_SSM_AUTOMATION_DIAGNOSISBUCKETPOLICY"
    '''
    :stability: experimental
    '''
    AWS_SSM_DIAGNOSISAUTOMATION_ADMINISTRATIONROLEPOLICY = "AWS_SSM_DIAGNOSISAUTOMATION_ADMINISTRATIONROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWS_SSM_DIAGNOSISAUTOMATION_EXECUTIONROLEPOLICY = "AWS_SSM_DIAGNOSISAUTOMATION_EXECUTIONROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWS_SSM_DIAGNOSISAUTOMATION_OPERATIONALACCOUNTADMINISTRATIONROLEPOLICY = "AWS_SSM_DIAGNOSISAUTOMATION_OPERATIONALACCOUNTADMINISTRATIONROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWS_SSM_REMEDIATIONAUTOMATION_ADMINISTRATIONROLEPOLICY = "AWS_SSM_REMEDIATIONAUTOMATION_ADMINISTRATIONROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWS_SSM_REMEDIATIONAUTOMATION_EXECUTIONROLEPOLICY = "AWS_SSM_REMEDIATIONAUTOMATION_EXECUTIONROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWS_SSM_REMEDIATIONAUTOMATION_OPERATIONALACCOUNTADMINISTRATIONROLEPOLICY = "AWS_SSM_REMEDIATIONAUTOMATION_OPERATIONALACCOUNTADMINISTRATIONROLEPOLICY"
    '''
    :stability: experimental
    '''
    AWSPARTNER_CENTRAL_FULL_ACCESS = "AWSPARTNER_CENTRAL_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMARKETPLACE_SELLER_OFFER_MANAGEMENT = "AWSMARKETPLACE_SELLER_OFFER_MANAGEMENT"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_PROJECT_ROLE_MACHINE_LEARNING_POLICY = "SAGE_MAKER_STUDIO_PROJECT_ROLE_MACHINE_LEARNING_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_DOMAIN_SERVICE_ROLE_POLICY = "SAGE_MAKER_STUDIO_DOMAIN_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_DOMAIN_EXECUTION_ROLE_POLICY = "SAGE_MAKER_STUDIO_DOMAIN_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_PROJECT_USER_ROLE_PERMISSIONS_BOUNDARY = "SAGE_MAKER_STUDIO_PROJECT_USER_ROLE_PERMISSIONS_BOUNDARY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_PROJECT_PROVISIONING_ROLE_POLICY = "SAGE_MAKER_STUDIO_PROJECT_PROVISIONING_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_PROJECT_USER_ROLE_POLICY = "SAGE_MAKER_STUDIO_PROJECT_USER_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSARTIFACT_AGREEMENTS_FULL_ACCESS = "AWSARTIFACT_AGREEMENTS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSARTIFACT_AGREEMENTS_READ_ONLY_ACCESS = "AWSARTIFACT_AGREEMENTS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPARTNER_LED_SUPPORT_READ_ONLY_ACCESS = "AWSPARTNER_LED_SUPPORT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSOBSERVABILITY_ADMIN_SERVICE_ROLE_POLICY = "AWSOBSERVABILITY_ADMIN_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_FULL_ACCESS = "SAGE_MAKER_STUDIO_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    DECLARATIVE_POLICIES_E_C2_REPORT = "DECLARATIVE_POLICIES_E_C2_REPORT"
    '''
    :stability: experimental
    '''
    AWSSECURITY_INCIDENT_RESPONSE_SERVICE_ROLE_POLICY = "AWSSECURITY_INCIDENT_RESPONSE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSECURITY_INCIDENT_RESPONSE_TRIAGE_SERVICE_ROLE_POLICY = "AWSSECURITY_INCIDENT_RESPONSE_TRIAGE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_OPEN_SEARCH_DASHBOARDS_FULL_ACCESS = "CLOUD_WATCH_OPEN_SEARCH_DASHBOARDS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_OPEN_SEARCH_DASHBOARD_ACCESS = "CLOUD_WATCH_OPEN_SEARCH_DASHBOARD_ACCESS"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_NETWORK_FLOW_MONITOR_SERVICE_ROLE_POLICY = "CLOUD_WATCH_NETWORK_FLOW_MONITOR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_NETWORK_FLOW_MONITOR_AGENT_PUBLISH_POLICY = "CLOUD_WATCH_NETWORK_FLOW_MONITOR_AGENT_PUBLISH_POLICY"
    '''
    :stability: experimental
    '''
    CLOUD_WATCH_NETWORK_FLOW_MONITOR_TOPOLOGY_SERVICE_ROLE_POLICY = "CLOUD_WATCH_NETWORK_FLOW_MONITOR_TOPOLOGY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSECURITY_INCIDENT_RESPONSE_READ_ONLY_ACCESS = "AWSSECURITY_INCIDENT_RESPONSE_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSECURITY_INCIDENT_RESPONSE_CASE_FULL_ACCESS = "AWSSECURITY_INCIDENT_RESPONSE_CASE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSECURITY_INCIDENT_RESPONSE_FULL_ACCESS = "AWSSECURITY_INCIDENT_RESPONSE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AIOPS_ASSISTANT_POLICY = "AIOPS_ASSISTANT_POLICY"
    '''
    :stability: experimental
    '''
    AIOPS_CONSOLE_ADMIN_POLICY = "AIOPS_CONSOLE_ADMIN_POLICY"
    '''
    :stability: experimental
    '''
    AIOPS_READ_ONLY_ACCESS = "AIOPS_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AIOPS_OPERATOR_ACCESS = "AIOPS_OPERATOR_ACCESS"
    '''
    :stability: experimental
    '''
    AURORA_DSQL_SERVICE_LINKED_ROLE_POLICY = "AURORA_DSQL_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_S3_TABLES_READ_ONLY_ACCESS = "AMAZON_S3_TABLES_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_AURORA_DSQL_READ_ONLY_ACCESS = "AMAZON_AURORA_DSQL_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_S3_TABLES_FULL_ACCESS = "AMAZON_S3_TABLES_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    QBUSINESS_QUICKSIGHT_PLUGIN_POLICY = "QBUSINESS_QUICKSIGHT_PLUGIN_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_AURORA_DSQL_CONSOLE_FULL_ACCESS = "AMAZON_AURORA_DSQL_CONSOLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_AURORA_DSQL_FULL_ACCESS = "AMAZON_AURORA_DSQL_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_TRAINING_PLAN_CREATE_ACCESS = "AMAZON_SAGE_MAKER_TRAINING_PLAN_CREATE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_CANVAS_SM_DATA_SCIENCE_ASSISTANT_ACCESS = "AMAZON_SAGE_MAKER_CANVAS_SM_DATA_SCIENCE_ASSISTANT_ACCESS"
    '''
    :stability: experimental
    '''
    AWSPARTNER_CENTRAL_SELLING_RESOURCE_SNAPSHOT_JOB_EXECUTION_ROLE_POLICY = "AWSPARTNER_CENTRAL_SELLING_RESOURCE_SNAPSHOT_JOB_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_ROLE_POLICY_FOR_INDEXING = "AWSBACKUP_SERVICE_ROLE_POLICY_FOR_INDEXING"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_ROLE_POLICY_FOR_ITEM_RESTORES = "AWSBACKUP_SERVICE_ROLE_POLICY_FOR_ITEM_RESTORES"
    '''
    :stability: experimental
    '''
    AWSMANAGEDSERVICES_SELFSERVICEREPORTING_SERVICEROLEPOLICY = "AWSMANAGEDSERVICES_SELFSERVICEREPORTING_SERVICEROLEPOLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_PARTNER_APPS_FULL_ACCESS = "AMAZON_SAGE_MAKER_PARTNER_APPS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_QUERY_EXECUTION_ROLE_POLICY = "SAGE_MAKER_STUDIO_QUERY_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_EMR_SERVICE_ROLE_POLICY = "SAGE_MAKER_STUDIO_EMR_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_CONNECT_READ_ONLY_ACCESS = "AWSELEMENTAL_MEDIA_CONNECT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSELEMENTAL_MEDIA_CONNECT_FULL_ACCESS = "AWSELEMENTAL_MEDIA_CONNECT_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_BEDROCK_AGENT_SERVICE_ROLE_POLICY = "SAGE_MAKER_STUDIO_BEDROCK_AGENT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_BEDROCK_CHAT_AGENT_USER_ROLE_POLICY = "SAGE_MAKER_STUDIO_BEDROCK_CHAT_AGENT_USER_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_BEDROCK_FLOW_SERVICE_ROLE_POLICY = "SAGE_MAKER_STUDIO_BEDROCK_FLOW_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_BEDROCK_PROMPT_USER_ROLE_POLICY = "SAGE_MAKER_STUDIO_BEDROCK_PROMPT_USER_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_BEDROCK_EVALUATION_JOB_SERVICE_ROLE_POLICY = "SAGE_MAKER_STUDIO_BEDROCK_EVALUATION_JOB_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_BEDROCK_KNOWLEDGE_BASE_SERVICE_ROLE_POLICY = "SAGE_MAKER_STUDIO_BEDROCK_KNOWLEDGE_BASE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_BEDROCK_KNOWLEDGE_BASE_CUSTOM_RESOURCE_POLICY = "SAGE_MAKER_STUDIO_BEDROCK_KNOWLEDGE_BASE_CUSTOM_RESOURCE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_BEDROCK_FUNCTION_EXECUTION_ROLE_POLICY = "SAGE_MAKER_STUDIO_BEDROCK_FUNCTION_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_EMR_INSTANCE_ROLE_POLICY = "SAGE_MAKER_STUDIO_EMR_INSTANCE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SEARCH_OPERATOR_ACCESS = "AWSBACKUP_SEARCH_OPERATOR_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_MANAGED_INTEGRATIONS_FULL_ACCESS = "AWSIO_T_MANAGED_INTEGRATIONS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSIO_T_MANAGED_INTEGRATIONS_ROLE_POLICY = "AWSIO_T_MANAGED_INTEGRATIONS_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_COMPUTE_SERVICE_ROLE_POLICY = "AMAZON_ECS_COMPUTE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSMEDIA_LIVE_ANYWHERE_SERVICE_ROLE_POLICY = "AWSMEDIA_LIVE_ANYWHERE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    GIT_LAB_DUO_WITH_AMAZON_Q_PERMISSIONS_POLICY = "GIT_LAB_DUO_WITH_AMAZON_Q_PERMISSIONS_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_JITNA_DEPLOYMENT_ROLE_POLICY = "AWSQUICK_SETUP_JITNA_DEPLOYMENT_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_TIMESTREAM_INFLUX_DB_FULL_ACCESS_WITHOUT_MARKETPLACE_ACCESS = "AMAZON_TIMESTREAM_INFLUX_DB_FULL_ACCESS_WITHOUT_MARKETPLACE_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_NOTIFICATIONS_SERVICE_POLICY = "AWSSYSTEMS_MANAGER_NOTIFICATIONS_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_JUST_IN_TIME_ACCESS_TOKEN_SESSION_POLICY = "AWSSYSTEMS_MANAGER_JUST_IN_TIME_ACCESS_TOKEN_SESSION_POLICY"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_JUST_IN_TIME_ACCESS_TOKEN_POLICY = "AWSSYSTEMS_MANAGER_JUST_IN_TIME_ACCESS_TOKEN_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_MANAGE_JITNA_RESOURCES_EXECUTION_POLICY = "AWSQUICK_SETUP_MANAGE_JITNA_RESOURCES_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_JUST_IN_TIME_ACCESS_SERVICE_POLICY = "AWSSYSTEMS_MANAGER_JUST_IN_TIME_ACCESS_SERVICE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSYSTEMS_MANAGER_JUST_IN_TIME_NODE_ACCESS_ROLE_PROPAGATION_POLICY = "AWSSYSTEMS_MANAGER_JUST_IN_TIME_NODE_ACCESS_ROLE_PROPAGATION_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_DASHBOARD_SERVICE_ROLE_POLICY = "AMAZON_EKS_DASHBOARD_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_SECRETS_MANAGER_WRITE_POLICY = "AWSQUICK_SIGHT_SECRETS_MANAGER_WRITE_POLICY"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_FOR_AWS_TRANSFORM = "AWSSERVICE_ROLE_FOR_AWS_TRANSFORM"
    '''
    :stability: experimental
    '''
    CLOUD_TRAIL_EVENT_CONTEXT = "CLOUD_TRAIL_EVENT_CONTEXT"
    '''
    :stability: experimental
    '''
    AMAZON_EVS_SERVICE_ROLE_POLICY = "AMAZON_EVS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPRIVATE_CA_CONNECTOR_FOR_KUBERNETES_POLICY = "AWSPRIVATE_CA_CONNECTOR_FOR_KUBERNETES_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SIGHT_SECRETS_MANAGER_WRITE_ACCESS = "AWSQUICK_SIGHT_SECRETS_MANAGER_WRITE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZONDYNAMODBFULLACCESS_V2 = "AMAZONDYNAMODBFULLACCESS_V2"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_QUICK_SIGHT_VPC_POLICY = "AMAZON_SAGE_MAKER_QUICK_SIGHT_VPC_POLICY"
    '''
    :stability: experimental
    '''
    AMAZONGUARDDUTYFULLACCESS_V2 = "AMAZONGUARDDUTYFULLACCESS_V2"
    '''
    :stability: experimental
    '''
    AWSSECURITY_HUB_V2_SERVICE_ROLE_POLICY = "AWSSECURITY_HUB_V2_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSNETWORK_FIREWALL_READ_ONLY_ACCESS = "AWSNETWORK_FIREWALL_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSNETWORK_FIREWALL_FULL_ACCESS = "AWSNETWORK_FIREWALL_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSSERVICE_ROLE_POLICY_FOR_WORKSPACES_INSTANCES = "AWSSERVICE_ROLE_POLICY_FOR_WORKSPACES_INSTANCES"
    '''
    :stability: experimental
    '''
    AMAZON_WORK_SPACES_THIN_CLIENT_MONITORING_SERVICE_ROLE_POLICY = "AMAZON_WORK_SPACES_THIN_CLIENT_MONITORING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    NETWORK_SECURITY_DIRECTOR_SERVICE_LINKED_ROLE_POLICY = "NETWORK_SECURITY_DIRECTOR_SERVICE_LINKED_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    MULTI_PARTY_APPROVAL_READ_ONLY_ACCESS = "MULTI_PARTY_APPROVAL_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    MULTI_PARTY_APPROVAL_FULL_ACCESS = "MULTI_PARTY_APPROVAL_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_EKS_DASHBOARD_CONSOLE_READ_ONLY = "AMAZON_EKS_DASHBOARD_CONSOLE_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_S3_TABLES_LAKE_FORMATION_SERVICE_ROLE = "AMAZON_S3_TABLES_LAKE_FORMATION_SERVICE_ROLE"
    '''
    :stability: experimental
    '''
    KEYSPACES_CDC_SERVICE_ROLE_POLICY = "KEYSPACES_CDC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSPCSCOMPUTE_NODE_POLICY = "AWSPCSCOMPUTE_NODE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_LIMITED_ACCESS = "AMAZON_BEDROCK_LIMITED_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_MARKETPLACE_ACCESS = "AMAZON_BEDROCK_MARKETPLACE_ACCESS"
    '''
    :stability: experimental
    '''
    AWSZONE_GROUP_ACCESS_MANAGEMENT_SERVICE_ROLE_POLICY = "AWSZONE_GROUP_ACCESS_MANAGEMENT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZONINSPECTOR2FULLACCESS_V2 = "AMAZONINSPECTOR2FULLACCESS_V2"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_ADMIN_PROJECT_USER_ROLE_POLICY = "SAGE_MAKER_STUDIO_ADMIN_PROJECT_USER_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_HYPER_POD_OBSERVABILITY_ADMIN_ACCESS = "AMAZON_SAGE_MAKER_HYPER_POD_OBSERVABILITY_ADMIN_ACCESS"
    '''
    :stability: experimental
    '''
    AWSDIRECTORY_SERVICE_SERVICE_ROLE_POLICY = "AWSDIRECTORY_SERVICE_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSBATCH_SERVICE_ROLE_POLICY_FOR_SAGE_MAKER = "AWSBATCH_SERVICE_ROLE_POLICY_FOR_SAGE_MAKER"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_AGENT_CORE_MEMORY_BEDROCK_MODEL_INFERENCE_EXECUTION_ROLE_POLICY = "AMAZON_BEDROCK_AGENT_CORE_MEMORY_BEDROCK_MODEL_INFERENCE_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    BEDROCK_AGENT_CORE_FULL_ACCESS = "BEDROCK_AGENT_CORE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSROLES_ANYWHERE_FULL_ACCESS = "AWSROLES_ANYWHERE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSROLES_ANYWHERE_READ_ONLY = "AWSROLES_ANYWHERE_READ_ONLY"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_LOAD_BALANCERS = "AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_LOAD_BALANCERS"
    '''
    :stability: experimental
    '''
    BUDGETS_SERVICE_ROLE_POLICY = "BUDGETS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSOBSERVABILITY_ADMIN_TELEMETRY_ENABLEMENT_SERVICE_ROLE_POLICY = "AWSOBSERVABILITY_ADMIN_TELEMETRY_ENABLEMENT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_START_STOP_INSTANCES_EXECUTION_POLICY = "AWSQUICK_SETUP_START_STOP_INSTANCES_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSQUICK_SETUP_START_SSM_ASSOCIATIONS_EXECUTION_POLICY = "AWSQUICK_SETUP_START_SSM_ASSOCIATIONS_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    ROSASHARED_VPC_ROUTE53_POLICY = "ROSASHARED_VPC_ROUTE53_POLICY"
    '''
    :stability: experimental
    '''
    ROSASHARED_VPC_ENDPOINT_POLICY = "ROSASHARED_VPC_ENDPOINT_POLICY"
    '''
    :stability: experimental
    '''
    AWSMANAGEMENT_CONSOLE_BASIC_USER_ACCESS = "AWSMANAGEMENT_CONSOLE_BASIC_USER_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMANAGEMENT_CONSOLE_ADMINISTRATOR_ACCESS = "AWSMANAGEMENT_CONSOLE_ADMINISTRATOR_ACCESS"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_USER_IAM_DEFAULT_EXECUTION_POLICY = "SAGE_MAKER_STUDIO_USER_IAM_DEFAULT_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_ADMIN_IAM_PERMISSIVE_EXECUTION_POLICY = "SAGE_MAKER_STUDIO_ADMIN_IAM_PERMISSIVE_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_ADMIN_IAM_DEFAULT_EXECUTION_POLICY = "SAGE_MAKER_STUDIO_ADMIN_IAM_DEFAULT_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_USER_IAM_PERMISSIVE_EXECUTION_POLICY = "SAGE_MAKER_STUDIO_USER_IAM_PERMISSIVE_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_USER_IAM_CONSOLE_POLICY = "SAGE_MAKER_STUDIO_USER_IAM_CONSOLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_ADMIN_IAM_CONSOLE_POLICY = "SAGE_MAKER_STUDIO_ADMIN_IAM_CONSOLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_HYPER_POD_TRAINING_OPERATOR_ACCESS = "AMAZON_SAGE_MAKER_HYPER_POD_TRAINING_OPERATOR_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_E_C2_IMAGE_REFERENCES_ACCESS_POLICY = "AMAZON_E_C2_IMAGE_REFERENCES_ACCESS_POLICY"
    '''
    :stability: experimental
    '''
    AWSTRANSFORM_APPLICATION_DEPLOYMENT_POLICY = "AWSTRANSFORM_APPLICATION_DEPLOYMENT_POLICY"
    '''
    :stability: experimental
    '''
    AWSBILLING_SERVICE_ROLE_POLICY = "AWSBILLING_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSOBSERVABILITY_ADMIN_LOGS_CENTRALIZATION_SERVICE_ROLE_POLICY = "AWSOBSERVABILITY_ADMIN_LOGS_CENTRALIZATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    BEDROCK_AGENT_CORE_NETWORK_SERVICE_ROLE_POLICY = "BEDROCK_AGENT_CORE_NETWORK_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_MANAGED_INSTANCES = "AMAZON_ECS_INFRASTRUCTURE_ROLE_POLICY_FOR_MANAGED_INSTANCES"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_INSTANCE_ROLE_POLICY_FOR_MANAGED_INSTANCES = "AMAZON_ECS_INSTANCE_ROLE_POLICY_FOR_MANAGED_INSTANCES"
    '''
    :stability: experimental
    '''
    AWSTRANSFORM_APPLICATION_ECS_DEPLOYMENT_POLICY = "AWSTRANSFORM_APPLICATION_ECS_DEPLOYMENT_POLICY"
    '''
    :stability: experimental
    '''
    AWSCONTROL_TOWER_IDENTITY_CENTER_MANAGEMENT_POLICY = "AWSCONTROL_TOWER_IDENTITY_CENTER_MANAGEMENT_POLICY"
    '''
    :stability: experimental
    '''
    AWSEC2_CAPACITY_MANAGER_SERVICE_ROLE_POLICY = "AWSEC2_CAPACITY_MANAGER_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AIOPS_ASSISTANT_INCIDENT_REPORT_POLICY = "AIOPS_ASSISTANT_INCIDENT_REPORT_POLICY"
    '''
    :stability: experimental
    '''
    BEDROCK_AGENT_CORE_RUNTIME_IDENTITY_SERVICE_ROLE_POLICY = "BEDROCK_AGENT_CORE_RUNTIME_IDENTITY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    DYNAMO_DB_GLOBAL_TABLE_SETTINGS_MANAGEMENT_SERVICE_ROLE_POLICY = "DYNAMO_DB_GLOBAL_TABLE_SETTINGS_MANAGEMENT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    RTBFABRIC_SERVICE_ROLE_POLICY = "RTBFABRIC_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    SAGE_MAKER_STUDIO_EMR_CONTAINERS_SYSTEM_NAMESPACE_ROLE_POLICY = "SAGE_MAKER_STUDIO_EMR_CONTAINERS_SYSTEM_NAMESPACE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_APPLICATION_RECOVERY_CONTROLLER_REGION_SWITCH_PLAN_EXECUTION_POLICY = "AMAZON_APPLICATION_RECOVERY_CONTROLLER_REGION_SWITCH_PLAN_EXECUTION_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_NETWORK_MIGRATION_CUSTOM_RESOURCE = "AWSAPPLICATION_MIGRATION_NETWORK_MIGRATION_CUSTOM_RESOURCE"
    '''
    :stability: experimental
    '''
    AWSSECRETS_MANAGER_CLIENT_READ_ONLY_ACCESS = "AWSSECRETS_MANAGER_CLIENT_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSCONTROL_TOWER_CLOUD_TRAIL_ROLE_POLICY = "AWSCONTROL_TOWER_CLOUD_TRAIL_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSAPPLICATION_MIGRATION_NETWORK_MIGRATION_MULTI_ACCOUNT = "AWSAPPLICATION_MIGRATION_NETWORK_MIGRATION_MULTI_ACCOUNT"
    '''
    :stability: experimental
    '''
    AMAZON_ECS_INFRASTRUCTURE_ROLEFOR_EXPRESS_GATEWAY_SERVICES = "AMAZON_ECS_INFRASTRUCTURE_ROLEFOR_EXPRESS_GATEWAY_SERVICES"
    '''
    :stability: experimental
    '''
    AWSEC2_SQL_HA_SERVICE_ROLE_POLICY = "AWSEC2_SQL_HA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSEC2_SQL_HA_INSTANCE_POLICY = "AWSEC2_SQL_HA_INSTANCE_POLICY"
    '''
    :stability: experimental
    '''
    AWSNATGATEWAY_SERVICE_ROLE_POLICY = "AWSNATGATEWAY_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_ATHENA_SERVICE_ROLE_POLICY = "AMAZON_ATHENA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    COMPUTE_OPTIMIZER_AUTOMATION_SERVICE_ROLE_POLICY = "COMPUTE_OPTIMIZER_AUTOMATION_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_MWAA_SERVERLESS_SERVICE_ROLE_POLICY = "AMAZON_MWAA_SERVERLESS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SPACES_ROUTER_POLICY = "AMAZON_SAGE_MAKER_SPACES_ROUTER_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_SPACES_CONTROLLER_POLICY = "AMAZON_SAGE_MAKER_SPACES_CONTROLLER_POLICY"
    '''
    :stability: experimental
    '''
    AWSPARTNER_CENTRAL_CHANNEL_HANDSHAKE_APPROVAL_MANAGEMENT = "AWSPARTNER_CENTRAL_CHANNEL_HANDSHAKE_APPROVAL_MANAGEMENT"
    '''
    :stability: experimental
    '''
    AWSPARTNER_CENTRAL_CHANNEL_MANAGEMENT = "AWSPARTNER_CENTRAL_CHANNEL_MANAGEMENT"
    '''
    :stability: experimental
    '''
    SIGN_IN_LOCAL_DEVELOPMENT_ACCESS = "SIGN_IN_LOCAL_DEVELOPMENT_ACCESS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_SERVICE_ROLE_POLICY_FOR_SCANS = "AWSBACKUP_SERVICE_ROLE_POLICY_FOR_SCANS"
    '''
    :stability: experimental
    '''
    AWSBACKUP_GUARD_DUTY_ROLE_POLICY_FOR_SCANS = "AWSBACKUP_GUARD_DUTY_ROLE_POLICY_FOR_SCANS"
    '''
    :stability: experimental
    '''
    AMAZON_EKSMCP_READ_ONLY_ACCESS = "AMAZON_EKSMCP_READ_ONLY_ACCESS"
    '''
    :stability: experimental
    '''
    AWSMCP_SERVICE_ACTIONS_FULL_ACCESS = "AWSMCP_SERVICE_ACTIONS_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_REDSHIFT_FEDERATED_AUTHORIZATION = "AMAZON_REDSHIFT_FEDERATED_AUTHORIZATION"
    '''
    :stability: experimental
    '''
    AWSIDENTITY_CENTER_EXTERNAL_MANAGEMENT_POLICY = "AWSIDENTITY_CENTER_EXTERNAL_MANAGEMENT_POLICY"
    '''
    :stability: experimental
    '''
    NOVA_ACT_SERVICE_ROLE_POLICY = "NOVA_ACT_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_SERVICE_ROLE_POLICY = "AWSLAMBDA_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_MANAGED_E_C2_RESOURCE_OPERATOR = "AWSLAMBDA_MANAGED_E_C2_RESOURCE_OPERATOR"
    '''
    :stability: experimental
    '''
    AWSPARTNER_CENTRAL_MARKETING_MANAGEMENT = "AWSPARTNER_CENTRAL_MARKETING_MANAGEMENT"
    '''
    :stability: experimental
    '''
    SECURITY_AGENT_WEB_APP_API_POLICY = "SECURITY_AGENT_WEB_APP_API_POLICY"
    '''
    :stability: experimental
    '''
    AWSLAMBDA_BASIC_DURABLE_EXECUTION_ROLE_POLICY = "AWSLAMBDA_BASIC_DURABLE_EXECUTION_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_MANTLE_INFERENCE_ACCESS = "AMAZON_BEDROCK_MANTLE_INFERENCE_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_MANTLE_FULL_ACCESS = "AMAZON_BEDROCK_MANTLE_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_BEDROCK_MANTLE_READ_ONLY = "AMAZON_BEDROCK_MANTLE_READ_ONLY"
    '''
    :stability: experimental
    '''
    AWSTRANSFORM_CUSTOM_FULL_ACCESS = "AWSTRANSFORM_CUSTOM_FULL_ACCESS"
    '''
    :stability: experimental
    '''
    AWSTRANSFORM_CUSTOM_EXECUTE_TRANSFORMATIONS = "AWSTRANSFORM_CUSTOM_EXECUTE_TRANSFORMATIONS"
    '''
    :stability: experimental
    '''
    AWSTRANSFORM_CUSTOM_MANAGE_TRANSFORMATIONS = "AWSTRANSFORM_CUSTOM_MANAGE_TRANSFORMATIONS"
    '''
    :stability: experimental
    '''
    ACCOUNT_MANAGEMENT_FROM_VERCEL = "ACCOUNT_MANAGEMENT_FROM_VERCEL"
    '''
    :stability: experimental
    '''
    CONSOLE_FULL_ACCESS_FROM_VERCEL = "CONSOLE_FULL_ACCESS_FROM_VERCEL"
    '''
    :stability: experimental
    '''
    CONSOLE_VIEW_ONLY_ACCESS_FROM_VERCEL = "CONSOLE_VIEW_ONLY_ACCESS_FROM_VERCEL"
    '''
    :stability: experimental
    '''
    AWSACCOUNT_SETTINGS_MANAGEMENT_ROLE = "AWSACCOUNT_SETTINGS_MANAGEMENT_ROLE"
    '''
    :stability: experimental
    '''
    AWSUSER_ATTRIBUTE_COST_ALLOCATION_POLICY = "AWSUSER_ATTRIBUTE_COST_ALLOCATION_POLICY"
    '''
    :stability: experimental
    '''
    AWSCLEAN_ROOMS_SERVICE_ROLE_POLICY = "AWSCLEAN_ROOMS_SERVICE_ROLE_POLICY"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_HYPER_POD_GATED_MODEL_ACCESS = "AMAZON_SAGE_MAKER_HYPER_POD_GATED_MODEL_ACCESS"
    '''
    :stability: experimental
    '''
    AMAZON_SAGE_MAKER_HYPER_POD_INFERENCE_ACCESS = "AMAZON_SAGE_MAKER_HYPER_POD_INFERENCE_ACCESS"
    '''
    :stability: experimental
    '''


class LambdaArmFunction(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-common.LambdaArmFunction",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        code: "_aws_cdk_aws_lambda_ceddda9d.Code",
        handler: builtins.str,
        runtime: "_aws_cdk_aws_lambda_ceddda9d.Runtime",
        adot_instrumentation: typing.Optional[typing.Union["_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        application_log_level: typing.Optional[builtins.str] = None,
        application_log_level_v2: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel"] = None,
        architecture: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Architecture"] = None,
        code_signing_config: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig"] = None,
        current_version_options: typing.Optional[typing.Union["_aws_cdk_aws_lambda_ceddda9d.VersionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional["_aws_cdk_aws_sqs_ceddda9d.IQueue"] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"] = None,
        ephemeral_storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        events: typing.Optional[typing.Sequence["_aws_cdk_aws_lambda_ceddda9d.IEventSource"]] = None,
        filesystem: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.FileSystem"] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence["_aws_cdk_aws_iam_ceddda9d.PolicyStatement"]] = None,
        insights_version: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion"] = None,
        ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
        layers: typing.Optional[typing.Sequence["_aws_cdk_aws_lambda_ceddda9d.ILayerVersion"]] = None,
        log_format: typing.Optional[builtins.str] = None,
        logging_format: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LoggingFormat"] = None,
        log_group: typing.Optional["_aws_cdk_aws_logs_ceddda9d.ILogGroup"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        log_retention_retry_options: typing.Optional[typing.Union["_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        params_and_secrets: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion"] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional["_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup"] = None,
        recursive_loop: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop"] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
        runtime_management_mode: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        snap_start: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.SnapStartConf"] = None,
        system_log_level: typing.Optional[builtins.str] = None,
        system_log_level_v2: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel"] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        tracing: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Tracing"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        vpc_subnets: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        max_event_age: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        on_failure: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IDestination"] = None,
        on_success: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IDestination"] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param code: The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/foundation-progmodel.html. Use ``Handler.FROM_IMAGE`` when defining a function from a Docker image. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide. Use ``Runtime.FROM_IMAGE`` when defining a function from a Docker image.
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_ipv6_outbound: Whether to allow the Lambda to send all ipv6 network traffic. If set to true, there will only be a single egress rule which allows all outbound ipv6 traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets using ipv6. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllIpv6Outbound`` directly on the security group. Default: false
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic (except ipv6). If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllOutbound`` directly on the security group. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param application_log_level: (deprecated) Sets the application log level for the function. Default: "INFO"
        :param application_log_level_v2: Sets the application log level for the function. Default: ApplicationLogLevel.INFO
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param ipv6_allowed_for_dual_stack: Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets. Only used if 'vpc' is supplied. Default: false
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_format: (deprecated) Sets the logFormat for the function. Default: "Text"
        :param logging_format: Sets the loggingFormat for the function. Default: LoggingFormat.TEXT
        :param log_group: The log group the function sends logs to. By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/<function name>. However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention. Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it. Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16. If you are deploying to another type of region, please check regional availability first. Default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. This is a legacy API and we strongly recommend you move away from it if you can. Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property to instruct the Lambda function to send logs to it. Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change. Users and code and referencing the name verbatim will have to adjust. In AWS CDK code, you can access the log group name directly from the LogGroup construct:: import * as logs from 'aws-cdk-lib/aws-logs'; declare const myLogGroup: logs.LogGroup; myLogGroup.logGroupName; Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param params_and_secrets: Specify the configuration of Parameters and Secrets Extension. Default: - No Parameters and Secrets Extension
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param recursive_loop: Sets the Recursive Loop Protection for Lambda Function. It lets Lambda detect and terminate unintended recursive loops. Default: RecursiveLoop.Terminate
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param snap_start: Enable SnapStart for Lambda Function. SnapStart is currently supported for Java 11, Java 17, Python 3.12, Python 3.13, and .NET 8 runtime Default: - No snapstart
        :param system_log_level: (deprecated) Sets the system log level for the function. Default: "INFO"
        :param system_log_level_v2: Sets the system log level for the function. Default: SystemLogLevel.INFO
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e3bf296f8f93487cf70874ee83259ced40125114b74561132f89f028cf123d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaArmFunctionProps(
            code=code,
            handler=handler,
            runtime=runtime,
            adot_instrumentation=adot_instrumentation,
            allow_all_ipv6_outbound=allow_all_ipv6_outbound,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            application_log_level=application_log_level,
            application_log_level_v2=application_log_level_v2,
            architecture=architecture,
            code_signing_config=code_signing_config,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            dead_letter_topic=dead_letter_topic,
            description=description,
            environment=environment,
            environment_encryption=environment_encryption,
            ephemeral_storage_size=ephemeral_storage_size,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            insights_version=insights_version,
            ipv6_allowed_for_dual_stack=ipv6_allowed_for_dual_stack,
            layers=layers,
            log_format=log_format,
            logging_format=logging_format,
            log_group=log_group,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            params_and_secrets=params_and_secrets,
            profiling=profiling,
            profiling_group=profiling_group,
            recursive_loop=recursive_loop,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            runtime_management_mode=runtime_management_mode,
            security_groups=security_groups,
            snap_start=snap_start,
            system_log_level=system_log_level,
            system_log_level_v2=system_log_level_v2,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> "_aws_cdk_aws_lambda_ceddda9d.Function":
        '''
        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_lambda_ceddda9d.Function", jsii.get(self, "lambdaFunction"))


@jsii.data_type(
    jsii_type="cdk-common.LambdaArmFunctionProps",
    jsii_struct_bases=[_aws_cdk_aws_lambda_ceddda9d.FunctionProps],
    name_mapping={
        "max_event_age": "maxEventAge",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
        "retry_attempts": "retryAttempts",
        "adot_instrumentation": "adotInstrumentation",
        "allow_all_ipv6_outbound": "allowAllIpv6Outbound",
        "allow_all_outbound": "allowAllOutbound",
        "allow_public_subnet": "allowPublicSubnet",
        "application_log_level": "applicationLogLevel",
        "application_log_level_v2": "applicationLogLevelV2",
        "architecture": "architecture",
        "code_signing_config": "codeSigningConfig",
        "current_version_options": "currentVersionOptions",
        "dead_letter_queue": "deadLetterQueue",
        "dead_letter_queue_enabled": "deadLetterQueueEnabled",
        "dead_letter_topic": "deadLetterTopic",
        "description": "description",
        "environment": "environment",
        "environment_encryption": "environmentEncryption",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "events": "events",
        "filesystem": "filesystem",
        "function_name": "functionName",
        "initial_policy": "initialPolicy",
        "insights_version": "insightsVersion",
        "ipv6_allowed_for_dual_stack": "ipv6AllowedForDualStack",
        "layers": "layers",
        "log_format": "logFormat",
        "logging_format": "loggingFormat",
        "log_group": "logGroup",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "memory_size": "memorySize",
        "params_and_secrets": "paramsAndSecrets",
        "profiling": "profiling",
        "profiling_group": "profilingGroup",
        "recursive_loop": "recursiveLoop",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "runtime_management_mode": "runtimeManagementMode",
        "security_groups": "securityGroups",
        "snap_start": "snapStart",
        "system_log_level": "systemLogLevel",
        "system_log_level_v2": "systemLogLevelV2",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "code": "code",
        "handler": "handler",
        "runtime": "runtime",
    },
)
class LambdaArmFunctionProps(_aws_cdk_aws_lambda_ceddda9d.FunctionProps):
    def __init__(
        self,
        *,
        max_event_age: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        on_failure: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IDestination"] = None,
        on_success: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IDestination"] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        adot_instrumentation: typing.Optional[typing.Union["_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        application_log_level: typing.Optional[builtins.str] = None,
        application_log_level_v2: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel"] = None,
        architecture: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Architecture"] = None,
        code_signing_config: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig"] = None,
        current_version_options: typing.Optional[typing.Union["_aws_cdk_aws_lambda_ceddda9d.VersionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional["_aws_cdk_aws_sqs_ceddda9d.IQueue"] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"] = None,
        ephemeral_storage_size: typing.Optional["_aws_cdk_ceddda9d.Size"] = None,
        events: typing.Optional[typing.Sequence["_aws_cdk_aws_lambda_ceddda9d.IEventSource"]] = None,
        filesystem: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.FileSystem"] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence["_aws_cdk_aws_iam_ceddda9d.PolicyStatement"]] = None,
        insights_version: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion"] = None,
        ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
        layers: typing.Optional[typing.Sequence["_aws_cdk_aws_lambda_ceddda9d.ILayerVersion"]] = None,
        log_format: typing.Optional[builtins.str] = None,
        logging_format: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LoggingFormat"] = None,
        log_group: typing.Optional["_aws_cdk_aws_logs_ceddda9d.ILogGroup"] = None,
        log_retention: typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"] = None,
        log_retention_retry_options: typing.Optional[typing.Union["_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        params_and_secrets: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion"] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional["_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup"] = None,
        recursive_loop: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop"] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"] = None,
        runtime_management_mode: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode"] = None,
        security_groups: typing.Optional[typing.Sequence["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]] = None,
        snap_start: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.SnapStartConf"] = None,
        system_log_level: typing.Optional[builtins.str] = None,
        system_log_level_v2: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel"] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        tracing: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Tracing"] = None,
        vpc: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"] = None,
        vpc_subnets: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
        code: "_aws_cdk_aws_lambda_ceddda9d.Code",
        handler: builtins.str,
        runtime: "_aws_cdk_aws_lambda_ceddda9d.Runtime",
    ) -> None:
        '''
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_ipv6_outbound: Whether to allow the Lambda to send all ipv6 network traffic. If set to true, there will only be a single egress rule which allows all outbound ipv6 traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets using ipv6. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllIpv6Outbound`` directly on the security group. Default: false
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic (except ipv6). If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllOutbound`` directly on the security group. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param application_log_level: (deprecated) Sets the application log level for the function. Default: "INFO"
        :param application_log_level_v2: Sets the application log level for the function. Default: ApplicationLogLevel.INFO
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param ipv6_allowed_for_dual_stack: Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets. Only used if 'vpc' is supplied. Default: false
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_format: (deprecated) Sets the logFormat for the function. Default: "Text"
        :param logging_format: Sets the loggingFormat for the function. Default: LoggingFormat.TEXT
        :param log_group: The log group the function sends logs to. By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/<function name>. However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention. Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it. Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16. If you are deploying to another type of region, please check regional availability first. Default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. This is a legacy API and we strongly recommend you move away from it if you can. Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property to instruct the Lambda function to send logs to it. Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change. Users and code and referencing the name verbatim will have to adjust. In AWS CDK code, you can access the log group name directly from the LogGroup construct:: import * as logs from 'aws-cdk-lib/aws-logs'; declare const myLogGroup: logs.LogGroup; myLogGroup.logGroupName; Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param params_and_secrets: Specify the configuration of Parameters and Secrets Extension. Default: - No Parameters and Secrets Extension
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param recursive_loop: Sets the Recursive Loop Protection for Lambda Function. It lets Lambda detect and terminate unintended recursive loops. Default: RecursiveLoop.Terminate
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param snap_start: Enable SnapStart for Lambda Function. SnapStart is currently supported for Java 11, Java 17, Python 3.12, Python 3.13, and .NET 8 runtime Default: - No snapstart
        :param system_log_level: (deprecated) Sets the system log level for the function. Default: "INFO"
        :param system_log_level_v2: Sets the system log level for the function. Default: SystemLogLevel.INFO
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param code: The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/foundation-progmodel.html. Use ``Handler.FROM_IMAGE`` when defining a function from a Docker image. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide. Use ``Runtime.FROM_IMAGE`` when defining a function from a Docker image.

        :stability: experimental
        '''
        if isinstance(adot_instrumentation, dict):
            adot_instrumentation = _aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig(**adot_instrumentation)
        if isinstance(current_version_options, dict):
            current_version_options = _aws_cdk_aws_lambda_ceddda9d.VersionOptions(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40eefcd7535af0a73fd2cbf4f236c945325c5f550487a9083a190243b2b72ae2)
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument adot_instrumentation", value=adot_instrumentation, expected_type=type_hints["adot_instrumentation"])
            check_type(argname="argument allow_all_ipv6_outbound", value=allow_all_ipv6_outbound, expected_type=type_hints["allow_all_ipv6_outbound"])
            check_type(argname="argument allow_all_outbound", value=allow_all_outbound, expected_type=type_hints["allow_all_outbound"])
            check_type(argname="argument allow_public_subnet", value=allow_public_subnet, expected_type=type_hints["allow_public_subnet"])
            check_type(argname="argument application_log_level", value=application_log_level, expected_type=type_hints["application_log_level"])
            check_type(argname="argument application_log_level_v2", value=application_log_level_v2, expected_type=type_hints["application_log_level_v2"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument code_signing_config", value=code_signing_config, expected_type=type_hints["code_signing_config"])
            check_type(argname="argument current_version_options", value=current_version_options, expected_type=type_hints["current_version_options"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument dead_letter_queue_enabled", value=dead_letter_queue_enabled, expected_type=type_hints["dead_letter_queue_enabled"])
            check_type(argname="argument dead_letter_topic", value=dead_letter_topic, expected_type=type_hints["dead_letter_topic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_encryption", value=environment_encryption, expected_type=type_hints["environment_encryption"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument initial_policy", value=initial_policy, expected_type=type_hints["initial_policy"])
            check_type(argname="argument insights_version", value=insights_version, expected_type=type_hints["insights_version"])
            check_type(argname="argument ipv6_allowed_for_dual_stack", value=ipv6_allowed_for_dual_stack, expected_type=type_hints["ipv6_allowed_for_dual_stack"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument logging_format", value=logging_format, expected_type=type_hints["logging_format"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument log_retention_role", value=log_retention_role, expected_type=type_hints["log_retention_role"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument params_and_secrets", value=params_and_secrets, expected_type=type_hints["params_and_secrets"])
            check_type(argname="argument profiling", value=profiling, expected_type=type_hints["profiling"])
            check_type(argname="argument profiling_group", value=profiling_group, expected_type=type_hints["profiling_group"])
            check_type(argname="argument recursive_loop", value=recursive_loop, expected_type=type_hints["recursive_loop"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument runtime_management_mode", value=runtime_management_mode, expected_type=type_hints["runtime_management_mode"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument snap_start", value=snap_start, expected_type=type_hints["snap_start"])
            check_type(argname="argument system_log_level", value=system_log_level, expected_type=type_hints["system_log_level"])
            check_type(argname="argument system_log_level_v2", value=system_log_level_v2, expected_type=type_hints["system_log_level_v2"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code": code,
            "handler": handler,
            "runtime": runtime,
        }
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if adot_instrumentation is not None:
            self._values["adot_instrumentation"] = adot_instrumentation
        if allow_all_ipv6_outbound is not None:
            self._values["allow_all_ipv6_outbound"] = allow_all_ipv6_outbound
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if application_log_level is not None:
            self._values["application_log_level"] = application_log_level
        if application_log_level_v2 is not None:
            self._values["application_log_level_v2"] = application_log_level_v2
        if architecture is not None:
            self._values["architecture"] = architecture
        if code_signing_config is not None:
            self._values["code_signing_config"] = code_signing_config
        if current_version_options is not None:
            self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None:
            self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if dead_letter_topic is not None:
            self._values["dead_letter_topic"] = dead_letter_topic
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if environment_encryption is not None:
            self._values["environment_encryption"] = environment_encryption
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if events is not None:
            self._values["events"] = events
        if filesystem is not None:
            self._values["filesystem"] = filesystem
        if function_name is not None:
            self._values["function_name"] = function_name
        if initial_policy is not None:
            self._values["initial_policy"] = initial_policy
        if insights_version is not None:
            self._values["insights_version"] = insights_version
        if ipv6_allowed_for_dual_stack is not None:
            self._values["ipv6_allowed_for_dual_stack"] = ipv6_allowed_for_dual_stack
        if layers is not None:
            self._values["layers"] = layers
        if log_format is not None:
            self._values["log_format"] = log_format
        if logging_format is not None:
            self._values["logging_format"] = logging_format
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if params_and_secrets is not None:
            self._values["params_and_secrets"] = params_and_secrets
        if profiling is not None:
            self._values["profiling"] = profiling
        if profiling_group is not None:
            self._values["profiling_group"] = profiling_group
        if recursive_loop is not None:
            self._values["recursive_loop"] = recursive_loop
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if runtime_management_mode is not None:
            self._values["runtime_management_mode"] = runtime_management_mode
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if snap_start is not None:
            self._values["snap_start"] = snap_start
        if system_log_level is not None:
            self._values["system_log_level"] = system_log_level
        if system_log_level_v2 is not None:
            self._values["system_log_level_v2"] = system_log_level_v2
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def max_event_age(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        :default: Duration.hours(6)
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def on_failure(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IDestination"]:
        '''The destination for failed invocations.

        :default: - no destination
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IDestination"], result)

    @builtins.property
    def on_success(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IDestination"]:
        '''The destination for successful invocations.

        :default: - no destination
        '''
        result = self._values.get("on_success")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.IDestination"], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        :default: 2
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def adot_instrumentation(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig"]:
        '''Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation.

        :default: - No ADOT instrumentation

        :see: https://aws-otel.github.io/docs/getting-started/lambda
        '''
        result = self._values.get("adot_instrumentation")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig"], result)

    @builtins.property
    def allow_all_ipv6_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow the Lambda to send all ipv6 network traffic.

        If set to true, there will only be a single egress rule which allows all
        outbound ipv6 traffic. If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets using ipv6.

        Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set.
        Instead, configure ``allowAllIpv6Outbound`` directly on the security group.

        :default: false
        '''
        result = self._values.get("allow_all_ipv6_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow the Lambda to send all network traffic (except ipv6).

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set.
        Instead, configure ``allowAllOutbound`` directly on the security group.

        :default: true
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        '''Lambda Functions in a public subnet can NOT access the internet.

        Use this property to acknowledge this limitation and still place the function in a public subnet.

        :default: false

        :see: https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841
        '''
        result = self._values.get("allow_public_subnet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def application_log_level(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Sets the application log level for the function.

        :default: "INFO"

        :deprecated: Use ``applicationLogLevelV2`` as a property instead.

        :stability: deprecated
        '''
        result = self._values.get("application_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_log_level_v2(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel"]:
        '''Sets the application log level for the function.

        :default: ApplicationLogLevel.INFO
        '''
        result = self._values.get("application_log_level_v2")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel"], result)

    @builtins.property
    def architecture(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Architecture"]:
        '''The system architectures compatible with this lambda function.

        :default: Architecture.X86_64
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Architecture"], result)

    @builtins.property
    def code_signing_config(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig"]:
        '''Code signing config associated with this function.

        :default: - Not Sign the Code
        '''
        result = self._values.get("code_signing_config")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig"], result)

    @builtins.property
    def current_version_options(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.VersionOptions"]:
        '''Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        :default: - default options as described in ``VersionOptions``
        '''
        result = self._values.get("current_version_options")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.VersionOptions"], result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional["_aws_cdk_aws_sqs_ceddda9d.IQueue"]:
        '''The SQS queue to use if DLQ is enabled.

        If SNS topic is desired, specify ``deadLetterTopic`` property instead.

        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional["_aws_cdk_aws_sqs_ceddda9d.IQueue"], result)

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[builtins.bool]:
        '''Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        '''
        result = self._values.get("dead_letter_queue_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dead_letter_topic(self) -> typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"]:
        '''The SNS topic to use as a DLQ.

        Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created
        rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly.

        :default: - no SNS topic
        '''
        result = self._values.get("dead_letter_topic")
        return typing.cast(typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the function.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_encryption(
        self,
    ) -> typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"]:
        '''The AWS KMS key that's used to encrypt your function's environment variables.

        :default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        '''
        result = self._values.get("environment_encryption")
        return typing.cast(typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional["_aws_cdk_ceddda9d.Size"]:
        '''The size of the function’s /tmp directory in MiB.

        :default: 512 MiB
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Size"], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_lambda_ceddda9d.IEventSource"]]:
        '''Event sources for this function.

        You can also add event sources using ``addEventSource``.

        :default: - No event sources.
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_lambda_ceddda9d.IEventSource"]], result)

    @builtins.property
    def filesystem(self) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.FileSystem"]:
        '''The filesystem configuration for the lambda function.

        :default: - will not mount any filesystem
        '''
        result = self._values.get("filesystem")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.FileSystem"], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''A name for the function.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_policy(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_iam_ceddda9d.PolicyStatement"]]:
        '''Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        :default: - No policy statements are added to the created Lambda role.
        '''
        result = self._values.get("initial_policy")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_iam_ceddda9d.PolicyStatement"]], result)

    @builtins.property
    def insights_version(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion"]:
        '''Specify the version of CloudWatch Lambda insights to use for monitoring.

        :default: - No Lambda Insights

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-Getting-Started-docker.html
        '''
        result = self._values.get("insights_version")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion"], result)

    @builtins.property
    def ipv6_allowed_for_dual_stack(self) -> typing.Optional[builtins.bool]:
        '''Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets.

        Only used if 'vpc' is supplied.

        :default: false
        '''
        result = self._values.get("ipv6_allowed_for_dual_stack")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def layers(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_lambda_ceddda9d.ILayerVersion"]]:
        '''A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by multiple functions.

        :default: - No layers.
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_lambda_ceddda9d.ILayerVersion"]], result)

    @builtins.property
    def log_format(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Sets the logFormat for the function.

        :default: "Text"

        :deprecated: Use ``loggingFormat`` as a property instead.

        :stability: deprecated
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_format(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LoggingFormat"]:
        '''Sets the loggingFormat for the function.

        :default: LoggingFormat.TEXT
        '''
        result = self._values.get("logging_format")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LoggingFormat"], result)

    @builtins.property
    def log_group(self) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.ILogGroup"]:
        '''The log group the function sends logs to.

        By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/.
        However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention.

        Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it.

        Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16.
        If you are deploying to another type of region, please check regional availability first.

        :default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.ILogGroup"], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"]:
        '''The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        This is a legacy API and we strongly recommend you move away from it if you can.
        Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property
        to instruct the Lambda function to send logs to it.
        Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change.
        Users and code and referencing the name verbatim will have to adjust.

        In AWS CDK code, you can access the log group name directly from the LogGroup construct::

           import * as logs from 'aws-cdk-lib/aws-logs';

           declare const myLogGroup: logs.LogGroup;
           myLogGroup.logGroupName;

        :default: logs.RetentionDays.INFINITE
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional["_aws_cdk_aws_logs_ceddda9d.RetentionDays"], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions"]:
        '''When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can.
        ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it.

        :default: - Default AWS SDK retry options.
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions"], result)

    @builtins.property
    def log_retention_role(self) -> typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"]:
        '''The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can.
        ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it.

        :default: - A new role is created.
        '''
        result = self._values.get("log_retention_role")
        return typing.cast(typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 128
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def params_and_secrets(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion"]:
        '''Specify the configuration of Parameters and Secrets Extension.

        :default: - No Parameters and Secrets Extension

        :see: https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html
        '''
        result = self._values.get("params_and_secrets")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion"], result)

    @builtins.property
    def profiling(self) -> typing.Optional[builtins.bool]:
        '''Enable profiling.

        :default: - No profiling.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        '''
        result = self._values.get("profiling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profiling_group(
        self,
    ) -> typing.Optional["_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup"]:
        '''Profiling Group.

        :default: - A new profiling group will be created if ``profiling`` is set.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        '''
        result = self._values.get("profiling_group")
        return typing.cast(typing.Optional["_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup"], result)

    @builtins.property
    def recursive_loop(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop"]:
        '''Sets the Recursive Loop Protection for Lambda Function.

        It lets Lambda detect and terminate unintended recursive loops.

        :default: RecursiveLoop.Terminate
        '''
        result = self._values.get("recursive_loop")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop"], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''The maximum of concurrent executions you want to reserve for the function.

        :default: - No specific limit - account limit.

        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"]:
        '''Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        :default:

        - A unique role will be generated for this lambda function.
        Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional["_aws_cdk_aws_iam_ceddda9d.IRole"], result)

    @builtins.property
    def runtime_management_mode(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode"]:
        '''Sets the runtime management configuration for a function's version.

        :default: Auto
        '''
        result = self._values.get("runtime_management_mode")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode"], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]]:
        '''The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroup prop, a dedicated security
        group will be created for this function.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup"]], result)

    @builtins.property
    def snap_start(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.SnapStartConf"]:
        '''Enable SnapStart for Lambda Function.

        SnapStart is currently supported for Java 11, Java 17, Python 3.12, Python 3.13, and .NET 8 runtime

        :default: - No snapstart
        '''
        result = self._values.get("snap_start")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.SnapStartConf"], result)

    @builtins.property
    def system_log_level(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Sets the system log level for the function.

        :default: "INFO"

        :deprecated: Use ``systemLogLevelV2`` as a property instead.

        :stability: deprecated
        '''
        result = self._values.get("system_log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def system_log_level_v2(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel"]:
        '''Sets the system log level for the function.

        :default: SystemLogLevel.INFO
        '''
        result = self._values.get("system_log_level_v2")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.seconds(3)
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def tracing(self) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Tracing"]:
        '''Enable AWS X-Ray Tracing for Lambda Function.

        :default: Tracing.Disabled
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Tracing"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"]:
        '''VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.
        This is required when ``vpcSubnets`` is specified.

        :default: - Function is not placed within a VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.IVpc"], result)

    @builtins.property
    def vpc_subnets(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''Where to place the network interfaces within the VPC.

        This requires ``vpc`` to be specified in order for interfaces to actually be
        placed in the subnets. If ``vpc`` is not specify, this will raise an error.

        Note: Internet access for Lambda Functions requires a NAT Gateway, so picking
        public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``).

        :default: - the Vpc default strategy if not specified
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    @builtins.property
    def code(self) -> "_aws_cdk_aws_lambda_ceddda9d.Code":
        '''The source code of your Lambda function.

        You can point to a file in an
        Amazon Simple Storage Service (Amazon S3) bucket or specify your source
        code as inline text.
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast("_aws_cdk_aws_lambda_ceddda9d.Code", result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''The name of the method within your code that Lambda calls to execute your function.

        The format includes the file name. It can also include
        namespaces and other qualifiers, depending on the runtime.
        For more information, see https://docs.aws.amazon.com/lambda/latest/dg/foundation-progmodel.html.

        Use ``Handler.FROM_IMAGE`` when defining a function from a Docker image.

        NOTE: If you specify your source code as inline text by specifying the
        ZipFile property within the Code property, specify index.function_name as
        the handler.
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime(self) -> "_aws_cdk_aws_lambda_ceddda9d.Runtime":
        '''The runtime environment for the Lambda function that you are uploading.

        For valid values, see the Runtime property in the AWS Lambda Developer
        Guide.

        Use ``Runtime.FROM_IMAGE`` when defining a function from a Docker image.
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast("_aws_cdk_aws_lambda_ceddda9d.Runtime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaArmFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AWSManagedPolicies",
    "LambdaArmFunction",
    "LambdaArmFunctionProps",
]

publication.publish()

def _typecheckingstub__a2e3bf296f8f93487cf70874ee83259ced40125114b74561132f89f028cf123d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    code: _aws_cdk_aws_lambda_ceddda9d.Code,
    handler: builtins.str,
    runtime: _aws_cdk_aws_lambda_ceddda9d.Runtime,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    application_log_level: typing.Optional[builtins.str] = None,
    application_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_format: typing.Optional[builtins.str] = None,
    logging_format: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    params_and_secrets: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    recursive_loop: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    snap_start: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf] = None,
    system_log_level: typing.Optional[builtins.str] = None,
    system_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40eefcd7535af0a73fd2cbf4f236c945325c5f550487a9083a190243b2b72ae2(
    *,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    application_log_level: typing.Optional[builtins.str] = None,
    application_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_format: typing.Optional[builtins.str] = None,
    logging_format: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    params_and_secrets: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    recursive_loop: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    snap_start: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf] = None,
    system_log_level: typing.Optional[builtins.str] = None,
    system_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    code: _aws_cdk_aws_lambda_ceddda9d.Code,
    handler: builtins.str,
    runtime: _aws_cdk_aws_lambda_ceddda9d.Runtime,
) -> None:
    """Type checking stubs"""
    pass
