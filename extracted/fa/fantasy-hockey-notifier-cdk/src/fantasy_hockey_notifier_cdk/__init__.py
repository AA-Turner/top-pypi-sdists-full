r'''
# Fantasy Hockey Notifier CDK

> AWS CDK construct to send notifications for adds, drops, and trades in an ESPN Fantasy Hockey league

[![NPM version](https://badge.fury.io/js/fantasy-hockey-notifier-cdk.svg)](https://badge.fury.io/js/fantasy-hockey-notifier-cdk)
[![PyPI version](https://badge.fury.io/py/fantasy-hockey-notifier-cdk.svg)](https://badge.fury.io/py/fantasy-hockey-notifier-cdk)
[![Release](https://github.com/ftalburt/fantasy-hockey-notifier-cdk/actions/workflows/release.yml/badge.svg)](https://github.com/ftalburt/fantasy-hockey-notifier-cdk/actions/workflows/release.yml)

This application checks for and sends notifications about adds, drops, and trades in an ESPN Fantasy Hockey league. All ESPN APIs used are unofficial and undocumented, thus this application may break at some point in the future if ESPN changes the response schema for any of the endpoints. The codebase supports local execution, along with deployment to AWS using [AWS CDK](https://aws.amazon.com/cdk).

## Local Execution

In addition to being consumable as a CDK construct (which is the primary use-case), the project supports local execution for testing purposes.

### Prerequisites for Local Execution

* Node.js 14 or later
* See the [Environment Variables](#environment-variables) section for a list of required and optional variables that should be exported in the shell or set in the .env file
* If using any of the environment variables starting with `AWS_` or ending with `_SSM`, you must configure AWS credentials via a local credentials file or environment variables. See the [AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) for details.

### Shell Commands for Local Execution

```sh
npm ci
npm start
```

## API Reference

See [API.md](./API.md).

## Environment Variables

### Required Variables

`FH_SEASON` or `FH_SEASON_SSM`: The year of the fantasy hockey season (i.e. `2020` for the 2019-2020 season)

`FH_LEAGUE_ID` or `FH_LEAGUE_ID_SSM`: The ID of the ESPN fantasy hockey league (this is displayed in the URL when you go to the `My Team` page) or the path for an SSM parameter with this value (SSM variable takes prescedence if both are specified)

`ESPN_S2_COOKIE` or `ESPN_S2_COOKIE_SSM`: The value of your `espn_s2` cookie to be used for authentication (you can find this by examining stored cookies for espn.com using the Chrome or Firefox developer tools) or the path for an SSM parameter with this value (SSM variable takes prescedence if both are specified)

### Optional Variables

`AWS_SNS_TOPIC_ARN`: The ARN of an existing AWS SNS topic

`AWS_DYNAMO_DB_TABLE_NAME` or `DISCORD_WEBHOOK_SSM`: The name of an existing Dynamo DB table to use for storing last run dates (takes priority over `LAST_RUN_FILE_PATH` if both are set) or the path for an SSM parameter with this value (SSM variable takes prescedence if both are specified)

`DISCORD_WEBHOOK`: A Discord webhook URL

`LAST_RUN_FILE_PATH`: A local file path to use for storing last run dates (defaults to `.lastrun`)

`EARLIEST_DATE`: A unix timestamp in milliseconds to use as the earliest date when looking up transactions

`LATEST_DATE`: A unix timestamp in milliseconds to use as the latest date when looking up transactions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
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
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_lambda_nodejs as _aws_cdk_aws_lambda_nodejs_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="fantasy-hockey-notifier-cdk.FantasyHockeyEnvVars",
    jsii_struct_bases=[],
    name_mapping={
        "discord_webhook": "discordWebhook",
        "espn_s2_cookie": "espnS2Cookie",
        "fh_league_id": "fhLeagueId",
        "fh_season": "fhSeason",
    },
)
class FantasyHockeyEnvVars:
    def __init__(
        self,
        *,
        discord_webhook: typing.Optional[builtins.str] = None,
        espn_s2_cookie: typing.Optional[builtins.str] = None,
        fh_league_id: typing.Optional[builtins.str] = None,
        fh_season: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Environment variables for the Lambda function.

        :param discord_webhook: Value for DISCORD_WEBHOOK.
        :param espn_s2_cookie: Value for ESPN_S2_COOKIE. This is a required parameter and must be set via SSM or clear text env vars
        :param fh_league_id: Value for FH_LEAGUE_ID. This is a required parameter and must be set via SSM or clear text env vars
        :param fh_season: Value for FH_SEASON. This is a required parameter and must be set via SSM or clear text env vars
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4f4bd497a6854db762b6c5d88ccdf4897e864eadf7870db173c0ec663bf728)
            check_type(argname="argument discord_webhook", value=discord_webhook, expected_type=type_hints["discord_webhook"])
            check_type(argname="argument espn_s2_cookie", value=espn_s2_cookie, expected_type=type_hints["espn_s2_cookie"])
            check_type(argname="argument fh_league_id", value=fh_league_id, expected_type=type_hints["fh_league_id"])
            check_type(argname="argument fh_season", value=fh_season, expected_type=type_hints["fh_season"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if discord_webhook is not None:
            self._values["discord_webhook"] = discord_webhook
        if espn_s2_cookie is not None:
            self._values["espn_s2_cookie"] = espn_s2_cookie
        if fh_league_id is not None:
            self._values["fh_league_id"] = fh_league_id
        if fh_season is not None:
            self._values["fh_season"] = fh_season

    @builtins.property
    def discord_webhook(self) -> typing.Optional[builtins.str]:
        '''Value for DISCORD_WEBHOOK.'''
        result = self._values.get("discord_webhook")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def espn_s2_cookie(self) -> typing.Optional[builtins.str]:
        '''Value for ESPN_S2_COOKIE.

        This is a required parameter and must be set via SSM or
        clear text env vars
        '''
        result = self._values.get("espn_s2_cookie")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fh_league_id(self) -> typing.Optional[builtins.str]:
        '''Value for FH_LEAGUE_ID.

        This is a required parameter and must be set via SSM or
        clear text env vars
        '''
        result = self._values.get("fh_league_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fh_season(self) -> typing.Optional[builtins.str]:
        '''Value for FH_SEASON.

        This is a required parameter and must be set via SSM or
        clear text env vars
        '''
        result = self._values.get("fh_season")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FantasyHockeyEnvVars(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FantasyHockeyNotifier(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="fantasy-hockey-notifier-cdk.FantasyHockeyNotifier",
):
    '''A Lambda function to send notifications for transactions in an ESPN Fantasy Hockey league.'''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        dynamo_table: typing.Optional["_aws_cdk_aws_dynamodb_ceddda9d.ITable"] = None,
        dynamo_table_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        env_var_values: typing.Optional[typing.Union["FantasyHockeyEnvVars", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_keys: typing.Optional[typing.Sequence["_aws_cdk_aws_kms_ceddda9d.IKey"]] = None,
        lambda_architecture: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Architecture"] = None,
        lambda_schedule: typing.Optional["_aws_cdk_aws_events_ceddda9d.Schedule"] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        sns_topic: typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"] = None,
        ssm_paths: typing.Optional[typing.Union["FantasyHockeyEnvVars", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
    ) -> None:
        '''Constructor for FantasyHockeyNotifier.

        :param scope: Scope.
        :param id: ID.
        :param dynamo_table: An existing DynamoDB Table to use. Default: - a new Table will be created
        :param dynamo_table_removal_policy: The removal policy for the DynamoDB table. Default: RemovalPolicy.RETAIN
        :param env_var_values: Values for the env vars. If a value is specifed here and in ``ssmPaths``, the value in ``ssmPaths`` takes prescedence
        :param kms_keys: Existing KMS keys that are used to encrypt the SSM parameters. This must be specified to allow Lambda to read SecureString SSM parameteers
        :param lambda_architecture: The system architecture to use for the lambda function. Default: Architecture.ARM_64
        :param lambda_schedule: The schedule to use for the Lambda function. Default: Schedule.rate(Duration.minutes(1))
        :param memory_size: The amount of memory, in MB, to allocate to the Lambda function. Default: 128
        :param sns_topic: An existing SNS topic to send league event notifications to.
        :param ssm_paths: Paths for existing SSM parmeters with values for the env vars. If a value is specifed here and in ``envVarValues``, this value takes prescedence
        :param timeout: The function execution time after which Lambda terminates the function. Default: Duration.seconds(10)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ebec67c2f1298d4174071913a0e930f601c0a8f1fc85c63fb8cc8c1281fb7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FantasyHockeyNotifierProps(
            dynamo_table=dynamo_table,
            dynamo_table_removal_policy=dynamo_table_removal_policy,
            env_var_values=env_var_values,
            kms_keys=kms_keys,
            lambda_architecture=lambda_architecture,
            lambda_schedule=lambda_schedule,
            memory_size=memory_size,
            sns_topic=sns_topic,
            ssm_paths=ssm_paths,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dynamoTable")
    def dynamo_table(self) -> "_aws_cdk_aws_dynamodb_ceddda9d.ITable":
        '''The DynamoDB Table used for storing state.'''
        return typing.cast("_aws_cdk_aws_dynamodb_ceddda9d.ITable", jsii.get(self, "dynamoTable"))

    @builtins.property
    @jsii.member(jsii_name="dynamoTableRemovalPolicy")
    def dynamo_table_removal_policy(self) -> "_aws_cdk_ceddda9d.RemovalPolicy":
        '''The removal policy for the DynamoDB table.'''
        return typing.cast("_aws_cdk_ceddda9d.RemovalPolicy", jsii.get(self, "dynamoTableRemovalPolicy"))

    @builtins.property
    @jsii.member(jsii_name="eventRule")
    def event_rule(self) -> "_aws_cdk_aws_events_ceddda9d.Rule":
        '''The event rule for the Lambda function.'''
        return typing.cast("_aws_cdk_aws_events_ceddda9d.Rule", jsii.get(self, "eventRule"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArchitecture")
    def lambda_architecture(self) -> "_aws_cdk_aws_lambda_ceddda9d.Architecture":
        '''The system architecture for the Lambda function.'''
        return typing.cast("_aws_cdk_aws_lambda_ceddda9d.Architecture", jsii.get(self, "lambdaArchitecture"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> "_aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction":
        '''The Lambda function.'''
        return typing.cast("_aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction", jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="snsTopic")
    def sns_topic(self) -> typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"]:
        '''The SNS topic that recieves notifications about league events.'''
        return typing.cast(typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"], jsii.get(self, "snsTopic"))


@jsii.data_type(
    jsii_type="fantasy-hockey-notifier-cdk.FantasyHockeyNotifierProps",
    jsii_struct_bases=[],
    name_mapping={
        "dynamo_table": "dynamoTable",
        "dynamo_table_removal_policy": "dynamoTableRemovalPolicy",
        "env_var_values": "envVarValues",
        "kms_keys": "kmsKeys",
        "lambda_architecture": "lambdaArchitecture",
        "lambda_schedule": "lambdaSchedule",
        "memory_size": "memorySize",
        "sns_topic": "snsTopic",
        "ssm_paths": "ssmPaths",
        "timeout": "timeout",
    },
)
class FantasyHockeyNotifierProps:
    def __init__(
        self,
        *,
        dynamo_table: typing.Optional["_aws_cdk_aws_dynamodb_ceddda9d.ITable"] = None,
        dynamo_table_removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        env_var_values: typing.Optional[typing.Union["FantasyHockeyEnvVars", typing.Dict[builtins.str, typing.Any]]] = None,
        kms_keys: typing.Optional[typing.Sequence["_aws_cdk_aws_kms_ceddda9d.IKey"]] = None,
        lambda_architecture: typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Architecture"] = None,
        lambda_schedule: typing.Optional["_aws_cdk_aws_events_ceddda9d.Schedule"] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        sns_topic: typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"] = None,
        ssm_paths: typing.Optional[typing.Union["FantasyHockeyEnvVars", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
    ) -> None:
        '''Properties for a FantasyHockeyNotifier.

        :param dynamo_table: An existing DynamoDB Table to use. Default: - a new Table will be created
        :param dynamo_table_removal_policy: The removal policy for the DynamoDB table. Default: RemovalPolicy.RETAIN
        :param env_var_values: Values for the env vars. If a value is specifed here and in ``ssmPaths``, the value in ``ssmPaths`` takes prescedence
        :param kms_keys: Existing KMS keys that are used to encrypt the SSM parameters. This must be specified to allow Lambda to read SecureString SSM parameteers
        :param lambda_architecture: The system architecture to use for the lambda function. Default: Architecture.ARM_64
        :param lambda_schedule: The schedule to use for the Lambda function. Default: Schedule.rate(Duration.minutes(1))
        :param memory_size: The amount of memory, in MB, to allocate to the Lambda function. Default: 128
        :param sns_topic: An existing SNS topic to send league event notifications to.
        :param ssm_paths: Paths for existing SSM parmeters with values for the env vars. If a value is specifed here and in ``envVarValues``, this value takes prescedence
        :param timeout: The function execution time after which Lambda terminates the function. Default: Duration.seconds(10)
        '''
        if isinstance(env_var_values, dict):
            env_var_values = FantasyHockeyEnvVars(**env_var_values)
        if isinstance(ssm_paths, dict):
            ssm_paths = FantasyHockeyEnvVars(**ssm_paths)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3701be0255db56da1417df3ea1008dc187651580f9027ed672882004f4c41656)
            check_type(argname="argument dynamo_table", value=dynamo_table, expected_type=type_hints["dynamo_table"])
            check_type(argname="argument dynamo_table_removal_policy", value=dynamo_table_removal_policy, expected_type=type_hints["dynamo_table_removal_policy"])
            check_type(argname="argument env_var_values", value=env_var_values, expected_type=type_hints["env_var_values"])
            check_type(argname="argument kms_keys", value=kms_keys, expected_type=type_hints["kms_keys"])
            check_type(argname="argument lambda_architecture", value=lambda_architecture, expected_type=type_hints["lambda_architecture"])
            check_type(argname="argument lambda_schedule", value=lambda_schedule, expected_type=type_hints["lambda_schedule"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument sns_topic", value=sns_topic, expected_type=type_hints["sns_topic"])
            check_type(argname="argument ssm_paths", value=ssm_paths, expected_type=type_hints["ssm_paths"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dynamo_table is not None:
            self._values["dynamo_table"] = dynamo_table
        if dynamo_table_removal_policy is not None:
            self._values["dynamo_table_removal_policy"] = dynamo_table_removal_policy
        if env_var_values is not None:
            self._values["env_var_values"] = env_var_values
        if kms_keys is not None:
            self._values["kms_keys"] = kms_keys
        if lambda_architecture is not None:
            self._values["lambda_architecture"] = lambda_architecture
        if lambda_schedule is not None:
            self._values["lambda_schedule"] = lambda_schedule
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if sns_topic is not None:
            self._values["sns_topic"] = sns_topic
        if ssm_paths is not None:
            self._values["ssm_paths"] = ssm_paths
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def dynamo_table(self) -> typing.Optional["_aws_cdk_aws_dynamodb_ceddda9d.ITable"]:
        '''An existing DynamoDB Table to use.

        :default: - a new Table will be created
        '''
        result = self._values.get("dynamo_table")
        return typing.cast(typing.Optional["_aws_cdk_aws_dynamodb_ceddda9d.ITable"], result)

    @builtins.property
    def dynamo_table_removal_policy(
        self,
    ) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''The removal policy for the DynamoDB table.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("dynamo_table_removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def env_var_values(self) -> typing.Optional["FantasyHockeyEnvVars"]:
        '''Values for the env vars.

        If a value is specifed here and in ``ssmPaths``, the value in ``ssmPaths`` takes prescedence
        '''
        result = self._values.get("env_var_values")
        return typing.cast(typing.Optional["FantasyHockeyEnvVars"], result)

    @builtins.property
    def kms_keys(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_kms_ceddda9d.IKey"]]:
        '''Existing KMS keys that are used to encrypt the SSM parameters.

        This must be specified to allow Lambda to read SecureString SSM parameteers
        '''
        result = self._values.get("kms_keys")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_kms_ceddda9d.IKey"]], result)

    @builtins.property
    def lambda_architecture(
        self,
    ) -> typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Architecture"]:
        '''The system architecture to use for the lambda function.

        :default: Architecture.ARM_64
        '''
        result = self._values.get("lambda_architecture")
        return typing.cast(typing.Optional["_aws_cdk_aws_lambda_ceddda9d.Architecture"], result)

    @builtins.property
    def lambda_schedule(
        self,
    ) -> typing.Optional["_aws_cdk_aws_events_ceddda9d.Schedule"]:
        '''The schedule to use for the Lambda function.

        :default: Schedule.rate(Duration.minutes(1))
        '''
        result = self._values.get("lambda_schedule")
        return typing.cast(typing.Optional["_aws_cdk_aws_events_ceddda9d.Schedule"], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory, in MB, to allocate to the Lambda function.

        :default: 128
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sns_topic(self) -> typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"]:
        '''An existing SNS topic to send league event notifications to.'''
        result = self._values.get("sns_topic")
        return typing.cast(typing.Optional["_aws_cdk_aws_sns_ceddda9d.ITopic"], result)

    @builtins.property
    def ssm_paths(self) -> typing.Optional["FantasyHockeyEnvVars"]:
        '''Paths for existing SSM parmeters with values for the env vars.

        If a value is specifed here and in ``envVarValues``, this value takes prescedence
        '''
        result = self._values.get("ssm_paths")
        return typing.cast(typing.Optional["FantasyHockeyEnvVars"], result)

    @builtins.property
    def timeout(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''The function execution time after which Lambda terminates the function.

        :default: Duration.seconds(10)
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FantasyHockeyNotifierProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FantasyHockeyEnvVars",
    "FantasyHockeyNotifier",
    "FantasyHockeyNotifierProps",
]

publication.publish()

def _typecheckingstub__2e4f4bd497a6854db762b6c5d88ccdf4897e864eadf7870db173c0ec663bf728(
    *,
    discord_webhook: typing.Optional[builtins.str] = None,
    espn_s2_cookie: typing.Optional[builtins.str] = None,
    fh_league_id: typing.Optional[builtins.str] = None,
    fh_season: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ebec67c2f1298d4174071913a0e930f601c0a8f1fc85c63fb8cc8c1281fb7f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dynamo_table: typing.Optional[_aws_cdk_aws_dynamodb_ceddda9d.ITable] = None,
    dynamo_table_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    env_var_values: typing.Optional[typing.Union[FantasyHockeyEnvVars, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    lambda_architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    lambda_schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    sns_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    ssm_paths: typing.Optional[typing.Union[FantasyHockeyEnvVars, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3701be0255db56da1417df3ea1008dc187651580f9027ed672882004f4c41656(
    *,
    dynamo_table: typing.Optional[_aws_cdk_aws_dynamodb_ceddda9d.ITable] = None,
    dynamo_table_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    env_var_values: typing.Optional[typing.Union[FantasyHockeyEnvVars, typing.Dict[builtins.str, typing.Any]]] = None,
    kms_keys: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    lambda_architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    lambda_schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    sns_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    ssm_paths: typing.Optional[typing.Union[FantasyHockeyEnvVars, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
