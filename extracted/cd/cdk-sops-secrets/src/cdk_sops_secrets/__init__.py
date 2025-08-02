r'''
<img src="https://github.com/dbsystel/cdk-sops-secrets/blob/main/img/banner-dl-small.png?raw=true">

![stability](https://img.shields.io/badge/Stability-stable-green)
[![release](https://github.com/dbsystel/cdk-sops-secrets/actions/workflows/release.yml/badge.svg)](https://github.com/dbsystel/cdk-sops-secrets/actions/workflows/release.yml)
[![cdk-construct-hub](https://img.shields.io/badge/CDK-ConstructHub-blue)](https://constructs.dev/packages/cdk-sops-secrets)
[![npm](https://img.shields.io/npm/v/cdk-sops-secrets.svg)](https://www.npmjs.com/package/cdk-sops-secrets)
[![npm downloads](https://img.shields.io/npm/dw/cdk-sops-secrets)](https://www.npmjs.com/package/cdk-sops-secrets)
[![pypi](https://img.shields.io/pypi/v/cdk-sops-secrets.svg)](https://pypi.org/project/cdk-sops-secrets)
[![pypi downloads](https://img.shields.io/pypi/dw/cdk-sops-secrets)](https://pypi.org/project/cdk-sops-secrets)
[![codecov](https://codecov.io/gh/dbsystel/cdk-sops-secrets/branch/main/graph/badge.svg?token=OT7P7HQHXB)](https://codecov.io/gh/dbsystel/cdk-sops-secrets)
[![security-vulnerabilities](https://img.shields.io/github/issues-search/dbsystel/cdk-sops-secrets?color=%23ff0000&label=security-vulnerabilities&query=is%3Aissue%20is%3Aopen%20label%3A%22Mend%3A%20dependency%20security%20vulnerability%22)](https://github.com/dbsystel/cdk-sops-secrets/issues?q=is%3Aissue+is%3Aopen+label%3A%22security+vulnerability%22)

# Introduction

*Create secret values in AWS with infrastructure-as-code easily*

This construct library offers CDK Constructs that facilitate syncing [SOPS-encrypted secrets](https://github.com/getsops/sops) to AWS Secrets Manager and SSM Parameter Store.
It enables secure storage of secrets in Git repositories while allowing seamless synchronization and usage within AWS. Even large sets of SSM Parameters can be created quickly from a single file.

* Create AWS Secrets Manager secrets
* Create single SSM Parameter
* Create multiple SSM Parameter in a batch from a file
* Use SOPS json, yaml or dotenv as input files, as well as binary data
* No need for manual permission setups for the Custom Ressource due to automatic least-privilege generation for the SyncProvider

# Table Of Contents

* [Introduction](#introduction)
* [Table Of Contents](#table-of-contents)
* [Available Constructs](#available-constructs)

  * [SopsSecret — Sops to SecretsManager](#sopssecret--sops-to-secretsmanager)
  * [SopsStringParameter — Sops to single SSM ParameterStore Parameter](#sopsstringparameter--sops-to-single-ssm-parameterstore-parameter)
  * [MultiStringParameter — Sops to multiple SSM ParameterStore Parameters](#multistringparameter--sops-to-multiple-ssm-parameterstore-parameters)
  * [SopsSyncProvider](#sopssyncprovider)
  * [Common configuration options for SopsSecret, SopsStringParameter and MultiStringParameter](#common-configuration-options-for-sopssecret-sopsstringparameter-and-multistringparameter)
* [Considerations](#considerations)

  * [UploadType: INLINE / ASSET](#uploadtype-inline--asset)
  * [Stability](#stability)
* [FAQ](#faq)

  * [How can I migrate to V2](#how-can-i-migrate-to-v2)

    * [SecretsManager](#secretsmanager)
    * [Parameter](#parameter)
    * [MultiParameter](#multiparameter)
  * [It does not work, what can I do?](#it-does-not-work-what-can-i-do)
  * [I get errors with `dotenv` formatted files](#i-get-errors-with-dotenv-formatted-files)
  * [Error: Error getting data key: 0 successful groups required, got 0](#error-error-getting-data-key-0-successful-groups-required-got-0)
  * [Error: Asset of sync lambda not found](#error-asset-of-sync-lambda-not-found)
  * [Can I upload the sops file myself and provide the required information as CloudFormation Parameter?](#can-i-upload-the-sops-file-myself-and-provide-the-required-information-as-cloudformation-parameter)
  * [Can I access older versions of the secret stored in the SecretsManager?](#can-i-access-older-versions-of-the-secret-stored-in-the-secretsmanager)
  * [I want the `raw` content of the sops file, but I always get the content nested in json](#i-want-the-raw-content-of-the-sops-file-but-i-always-get-the-content-nested-in-json)
* [License](#license)

# Available Constructs

The construct library cdk-sops-secrets supports three different Constructs that help you to sync your encrypted sops secrets to secure places in AWS.

Let's assume we want to store the following secret information in AWS:

```json
{
  "apiKey": "sk-1234567890abcdef",
  "database": {
    "user": "admin",
    "password": "P@ssw0rd!",
    "host": "db.example.com"
  },
  "tokens": [
    { "service": "github", "token": "ghp_abcd1234" },
    { "service": "aws", "token": "AKIAIOSFODNN7EXAMPLE" }
  ],
  "someOtherKey": "base64:VGhpcyBpcyBhIHNlY3JldCBrZXk="
}
```

It doesn't matter if this data is in `json`, `yaml` or `dotenv` format, `cdk-sops-secret` can handle them all.
Even binary data is supported with some limitations.

## SopsSecret — Sops to SecretsManager

If you want to store your secret data in the AWS SecretsManager, use the `SopsSecret` construct. This is a "drop-in-replacement" for the [Secret Construct](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_secretsmanager.Secret.html) of the AWS CDK.

Minimal Example:

```python
const secret = new SopsSecret(stack, 'MySopsSecret', {
  secretName: 'mySecret', // name of the secret in AWS SecretsManager
  sopsFilePath: 'secrets/sopsfile-encrypted-secret.json', // filepath to the sops encrypted file
});
```

The content referenced sops secret file will be synced to the AWS SecretsManager Secret with the name `mySecret`.
For convenience, several transformations apply:

* Nested structures and arrays will be resolved and flattened to a JSONPath notation
* All values will be stored as strings

This is done also because of limitations of CDK in conjunction with
[dynamic references](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-secretsmanager.html) and limitiations
of the `Key/Value` view of the AWS SecretsManager WebConsole. So the result, saved in the AWS SecretsManager will actually be:

```json
{
  "apiKey": "sk-1234567890abcdef",
  "database.user": "admin",
  "database.password": "P@ssw0rd!",
  "database.host": "db.example.com",
  "tokens[0].service": "github",
  "tokens[0].token": "ghp_abcd1234",
  "tokens[1].service": "aws",
  "tokens[1].token": "AKIAIOSFODNN7EXAMPLE",
  "someOtherKey": "base64:VGhpcyBpcyBhIHNlY3JldCBrZXk="
}
```

This allows you to access the values from your secret via CDK:

```python
secret.secretValueFromJson('"database.password"').toString(),
  secret.secretValueFromJson('"tokens[0].token"').toString();
```

If you don't want these conversions, you can completely disable them by using the `rawOutput` property.

```python
const secret = new SopsSecret(stack, 'MySopsSecret', {
  rawOutput: RawOutput.STRING,
  ...
});
```

This will turn off the conversions and just place the decrypted content in the target secret. It's also possible to use
`RawOutput.BINARY` than the AWS SecretsManager Secret will be populted with binary, instead of string data.

## SopsStringParameter — Sops to single SSM ParameterStore Parameter

If you want to sync the whole content of a sops encrypted file to an encrypted AWS SSM ParameterStore Parameter, you can use the SopsStringParameter Construct.

```python
const parameter = new SopsStringParameter(stack, 'MySopsParameter', {
  encryptionKey: Key.fromLookup(stack, 'DefaultKey', {
    aliasName: 'alias/aws/ssm',
  }),
  sopsFilePath: 'secrets/sopsfile-encrypted-secret.json',
});
```

This will create a Parameter with the value of the decrypted sops file content. No transformations are applied.

## MultiStringParameter — Sops to multiple SSM ParameterStore Parameters

If you have a structured sops file (yaml, json, dotenv) and want to populate the AWS SSM ParameterStore with it, you want to use the MultiStringParameter Construct.

```python
const multi = new MultiStringParameter(stack, 'MyMultiParameter', {
  encryptionKey: Key.fromLookup(stack, 'DefaultKey', {
    aliasName: 'alias/aws/ssm',
  }),
  sopsFilePath: 'secrets/sopsfile-encrypted-secret.json',
});
```

This will create several AWS SSM ParameterStore Parameters:

```bash
ParameterName       => Value

/apiKey             => "sk-1234567890abcdef"
/database/user      => "admin"
/database/password  => "P@ssw0rd!"
/database/host      => "db.example.com"
/tokens/0/service   => "github"
/tokens/0/token     => "ghp_abcd1234"
/tokens/1/service   => "aws"
/tokens/1/token     => "AKIAIOSFODNN7EXAMPLE"
/someOtherKey       => "base64:VGhpcyBpcyBhIHNlY3JldCBrZXk="
```

You can configure the naming schema via the properties `keySeperator` and `keyPrefix`:

```python
const multi = new MultiStringParameter(stack, 'MyMultiParameter', {
  keyPrefix: 'mykeyprefix.'  // All keys will start with this string, default '/'
  keySeperator: '-'         // This seperator is used when converting to a flat structure, default '/'
})
```

This would lead to Parameters

```bash
ParameterName       => Value

mykeyprefix.apiKey             => "sk-1234567890abcdef"
mykeyprefix.database-user      => "admin"
mykeyprefix.tokens-0-service   => "github"
...
```

## SopsSyncProvider

The SOPS-Provider is the custom resource AWS Lambda Function, that is doing all the work. It downloads, decrypts
and stores the secret content in your desired location. This Lambda Function needs several IAM permissions to do it's work.

For most use cases, you don't need to create it on your own, as the other Constructs try to create this and derive the required IAM permissions from your input.

But there are use cases, that require you to change the defaults of this Provider. If this is the case,
you have to create the provider on your own and add it to the other constructs.

Note that a SopsSyncProvider is a [SingletonLambda](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lambda.SingletonFunction.html) that can only exist once.

```python
const provider = new SopsSyncProvider(this, 'MySopsSyncProvider', {
  role: customRole,       // you can pass a custom role

  vpc: customVpc,         // The default SopsSync Provider
  vpcSubnets: {           // won't run in any VPC,
    subnets: [            // as it does not require
      customSubnet1,      // access to any VPC resources.
      customSubnet2,      // But if you want,
    ]                     // you can change this behaviour
  },                      // and set vpc, subnet and
  securityGroups: [       // securitygroups to your
    customSecurityGroup   // needs.
  ],
  logGroup: new LogGroup(this, 'MyLogGroup', {  // you can add a custom log group
    retention: RetentionDays.THREE_MONTHS,      // with a custom retention period
    encryptionKey: new KmsKey(this, 'MyKmsKey') // and custom encryption
  }),                                           //
  uuid: 'MySopsSyncProvider',  // Create a custom singleton by changing default uuid.
});

provider.addToRolePolicy( // You cann pass PolicyStatements
  new PolicyStatement({   // via the addToRolePolicy Method
    actions: ['...'],     //
    resources: ['...'],   //
  })                      //
);                        //

kmsKey.grantDecrypt(      // The provider implements
  provider                // the IGrantable interface,
);                        // so you can use it as grant target

const secret = new SopsSecret(this, 'MySecret', {
  sopsProvider: provider, // this property is available in all Constructs
  ...
});
```

## Common configuration options for SopsSecret, SopsStringParameter and MultiStringParameter

```python

const construct = new Sops...(this, 'My' {
  /**
   * use your own SopsSyncProvider
   * @see SopsSyncProvider
   */
  sopsProvider: myCustomProvider      // default - a new provider will be created

  /**
   * the constructs try to derive the required iam permissions from the sops file
   * and the target. If you don't want this, you can disable this behaviour.
   * You have to take care of all required permissions on your own.
   */
  autoGenerateIamPermissions: false,  // default: true

  /**
   * the default behaviour of passing the sops file content to the provider is
   * by embedding the base64 encoded content in the cloudformation template.
   * Using CKD Assets is also supported. It might be required to switch to
   * Assets, if your sops files are very large.
   */
  uploadType: UploadType.ASSET,       // default: UploadType.INLINE

  /**
   * if you don't want this constructs to take care of passing the encrypted
   * sops file to the sops provider, you can upload them yourself to a
   * S3 bucket.
   * You can pass bucket and key, and the constructs won't pass the content
   * as ASSET or in the CloudFormation Template.
   * As the construct isn't aware of the sopsfile, we can't derive the required
   * permissions to decrypt the sops file. The same applies to the sopsFileFormat.
   * You have to pass them all manually.
   */
  sopsS3Bucket: 'my-custom-bucket',
  sopsS3Key: 'encoded-sops.json',
  sopsKmsKey: [
    kmsKeyUsedForEncryption,
  ]
  sopsFileFormat: 'json',   // Allowed values are json, yaml, dotenv and binary
})
```

# Considerations

## UploadType: INLINE / ASSET

I decided, that the default behavior should be "INLINE" because of the following consideration:

* Fewer permissions

  *If we use inline content instead of a S3 asset, the SopsSyncProvider does not need permissions to access the asset bucket and its KMS key.*
* Faster

  *If we don't have to upload and download things from and to S3, it should be a little faster.*
* Interchangeable

  *As we use the same information to generate the version of the secret,
  no new version of the secret should be created, if you change from INLINE to ASSET or vice versa,
  even if the CloudFormation resource updates.*

## Stability

You can consider this package as stable. Updates will follow [Semantic Versioning](https://semver.org/).

Nevertheless, I would recommend pinning the exact version of this library in your `package.json`.

# FAQ

## How can I migrate to V2

It was required to change some user facing configuration properties. So minor changes are required to make things work again.

### SecretsManager

* Removed property convertToJSON, flatten, stringifiedValues
* Use property rawOutput instaed:

  * `undefined / not set` => (default) convertToJSON and flatten and stringifiedValues = true
  * `RawOutput.STRING` => convertToJSON and flatten and stringifiedValues = false
  * `RawOutput.BINARY` => convertToJSON and flatten and stringifiedValues = false and Secret is binary

### Parameter

* Removed property convertToJSON, flatten, stringifiedValues => all of them made no sense - now only raw output of decrypted secret

### MultiParameter

* Removed property convertToJSON, flatten, stringifiedValues => most of this combinations made no sense
* Allways convertToJson and flatten (as we have to parse it to create multiple parameters)
* You are allowed to chose the flattenSeperator

## It does not work, what can I do?

Even if this construct has some unit and integration tests performed, there can be bugs and issues. As everything is performed by a cloudformation custom resource provider, a good starting point is the log of the corresponding lambda function. It should be located in your AWS Account under Cloudwatch -> Log groups:

`/aws/lambda/<YOUR-STACK-NAME>-SingletonLambdaSopsSyncProvider<SOMETHINGsomething1234>`

## I get errors with `dotenv` formatted files

Only very basic dotenv syntax is working right now. Only single line values are accepted. The format must match:

```dotenv
key=value
```

comments must be a single line, not after value assignments.

## Error: Error getting data key: 0 successful groups required, got 0

This error message (and failed sync) is related to the getsops/sops issues [#948](https://github.com/getsops/sops/issues/948) and [#634](https://github.com/getsops/sops/issues/634). You must not create your secret with the `--aws-profile` flag. This profile will be written to your sops filed and is required in every runtime environment. You have to define the profile to use via the environment variable `AWS_PROFILE` instead, to avoid this.

## Error: Asset of sync lambda not found

The lambda asset code is generated relative to the path of the index.ts in this package. With tools like nx this can lead to wrong results, so that the asset could not be found.

You can override the asset path via the [cdk.json](https://docs.aws.amazon.com/cdk/v2/guide/get_context_var.html) or via the flag `-c`of the cdk cli.

The context used for this override is `sops_sync_provider_asset_path`.

So for example you can use

```bash
cdk deploy -c "sops_sync_provider_asset_path=some/path/asset.zip"
```

or in your cdk.json

```json
{
  "context": {
    "sops_sync_provider_asset_path": "some/path/asset.zip"
  }
}
```

## Can I upload the sops file myself and provide the required information as CloudFormation Parameter?

This should be possible the following way. Ensure, that you have created a custom sops provider,
with proper IAM permissions.

```python
const sopsS3BucketParam = new CfnParameter(this, "s3BucketName", {
  type: "String",
  description: "The name of the Amazon S3 bucket where your sopsFile was uploaded."});

const sopsS3KeyParam = new CfnParameter(this, "s3KeyName", {
  type: "String",
  description: "The name of the key of the sopsFile inside the Amazon S3 bucket."});

const sopsKmsKeyArn = new CfnParameter(this, "sopsKeyArn", {
  type: "String",
  description: "The ARN of the KMS Key used for sops encryption"});

const sopsKmsKey = Key.fromKeyArn(this, 'Key', sopsKmsKeyArn.valueAsString)

new SopsSecret(stack, 'SopsSecret', {
  sopsS3Bucket: sopsS3BucketParam.valueAsString,
  sopsS3Key: sopsS3KeyParam.valueAsString,
  sopsKmsKey: [
    sopsKmsKey
  ],
  sopsFileFormat: 'json',
  ...
});
```

## Can I access older versions of the secret stored in the SecretsManager?

While creating the secret or updating the entries of a secret, the native CDK function `cdk.FileSystem.fingerprint(...)` is used
to generate the version information of the AWS SecretsManager secret.
Therefore, it is possible to reference the entries from a specific AWS SecretsManager version.

```python
const versionId = cdk.FileSystem.fingerprint(`./sops/SomeSecrets.json`);
const passphrase = ecs.Secret.fromSecretsManagerVersion(
  secretMgmt,
  { versionId: versionId },
  'MY_PRIVATE_PASSPHRASE',
);

const container = TaskDef.addContainer('Container', {
  secrets: {
    MY_PRIVATE_PASSPHRASE: passphrase,
  },
});
```

## I want the `raw` content of the sops file, but I always get the content nested in json

To get the best raw experience, you should encrypt your sops files in binary format:

```bash
sops encrypt ... my-whatever-file --output my-secret-information.sops.binary --input-type binary
```

You will lose features like only encrypting the values, not the keys.
The whole file content will be stored in the sops file.
You can store everything you like as binary, even binary data[^1].

When using binary encrypted secrets with this constructs, ensure the ending is also binary, or override via
`sopsFormat` property.

This does not work for `MultiStringParameter`

[^1] Even if sops can handle binary data, only the AWS SecretsManager allows to store it.

# License

The Apache-2.0 license. Please have a look at the [LICENSE](LICENSE) and [LICENSE-3RD-PARTY](LICENSE-3RD-PARTY).
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
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d
import constructs as _constructs_77d1e7e8


class MultiStringParameter(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.MultiStringParameter",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        key_prefix: typing.Optional[builtins.str] = None,
        key_separator: typing.Optional[builtins.str] = None,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        description: typing.Optional[builtins.str] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional["UploadType"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param key_prefix: The prefix used for all parameters. Default: - '/'
        :param key_separator: The seperator used to seperate keys. Default: - '/'
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param tier: The tier of the string parameter. Default: - undefined
        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520cbd9adefd0e4a3135f2f09bd2fa26acb8be581e0f77b06f12862c0125b5b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MultiStringParameterProps(
            key_prefix=key_prefix,
            key_separator=key_separator,
            encryption_key=encryption_key,
            description=description,
            tier=tier,
            asset_encryption_key=asset_encryption_key,
            auto_generate_iam_permissions=auto_generate_iam_permissions,
            sops_age_key=sops_age_key,
            sops_file_format=sops_file_format,
            sops_file_path=sops_file_path,
            sops_kms_key=sops_kms_key,
            sops_provider=sops_provider,
            sops_s3_bucket=sops_s3_bucket,
            sops_s3_key=sops_s3_key,
            upload_type=upload_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> _aws_cdk_ceddda9d.ResourceEnvironment:
        return typing.cast(_aws_cdk_ceddda9d.ResourceEnvironment, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="keyPrefix")
    def key_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPrefix"))

    @builtins.property
    @jsii.member(jsii_name="keySeparator")
    def key_separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keySeparator"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="sync")
    def sync(self) -> "SopsSync":
        return typing.cast("SopsSync", jsii.get(self, "sync"))


@jsii.enum(jsii_type="cdk-sops-secrets.RawOutput")
class RawOutput(enum.Enum):
    STRING = "STRING"
    '''Parse the secret as a string.'''
    BINARY = "BINARY"
    '''Parse the secret as a binary.'''


@jsii.enum(jsii_type="cdk-sops-secrets.ResourceType")
class ResourceType(enum.Enum):
    SECRET = "SECRET"
    SECRET_RAW = "SECRET_RAW"
    SECRET_BINARY = "SECRET_BINARY"
    PARAMETER = "PARAMETER"
    PARAMETER_MULTI = "PARAMETER_MULTI"


@jsii.implements(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret)
class SopsSecret(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.SopsSecret",
):
    '''A drop in replacement for the normal Secret, that is populated with the encrypted content of the given sops file.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        raw_output: typing.Optional[RawOutput] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        replica_regions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
        secret_name: typing.Optional[builtins.str] = None,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional["UploadType"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param raw_output: Should the secret parsed and transformed to json? Default: - undefined - STRING for binary secrets, else no raw output
        :param removal_policy: Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param replica_regions: A list of regions where to replicate this secret. Default: - Secret is not replicated
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641b47276285e7c457eb639fea01f8b2e2f54dd58d3bc6f9e184404914516a11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SopsSecretProps(
            description=description,
            encryption_key=encryption_key,
            raw_output=raw_output,
            removal_policy=removal_policy,
            replica_regions=replica_regions,
            secret_name=secret_name,
            asset_encryption_key=asset_encryption_key,
            auto_generate_iam_permissions=auto_generate_iam_permissions,
            sops_age_key=sops_age_key,
            sops_file_format=sops_file_format,
            sops_file_path=sops_file_path,
            sops_kms_key=sops_kms_key,
            sops_provider=sops_provider,
            sops_s3_bucket=sops_s3_bucket,
            sops_s3_key=sops_s3_key,
            upload_type=upload_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        hosted_rotation: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.HostedRotation] = None,
        rotate_immediately_on_update: typing.Optional[builtins.bool] = None,
        rotation_lambda: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.RotationSchedule:
        '''Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. The minimum value is 4 hours. The maximum value is 1000 days. A value of zero (``Duration.days(0)``) will not create RotationRules. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotate_immediately_on_update: Specifies whether to rotate the secret immediately or wait until the next scheduled rotation window. Default: true
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd08508625195135b318d9657d717ca369ecceb1cc51cd6b3fa8c66c489c3dad)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_secretsmanager_ceddda9d.RotationScheduleOptions(
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotate_immediately_on_update=rotate_immediately_on_update,
            rotation_lambda=rotation_lambda,
        )

        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.RotationSchedule, jsii.invoke(self, "addRotationSchedule", [id, options]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    ) -> _aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult:
        '''Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54076b0a3bb41bb64b3bbd471f51ee813e6ce6437b4b2ee14f76246051614126)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="applyRemovalPolicy")
    def apply_removal_policy(self, policy: _aws_cdk_ceddda9d.RemovalPolicy) -> None:
        '''Apply the given removal policy to this resource.

        The Removal Policy controls what happens to this resource when it stops
        being managed by CloudFormation, either because you've removed it from the
        CDK application or because you've made a change that requires the resource
        to be replaced.

        The resource can be deleted (``RemovalPolicy.DESTROY``), or left in your AWS
        account for data recovery and cleanup later (``RemovalPolicy.RETAIN``).

        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d3b1469d7d365dc715e5fc30a5ca749e3a126bab5731a9cb3e3bd09de54905)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "applyRemovalPolicy", [policy]))

    @jsii.member(jsii_name="attach")
    def attach(
        self,
        target: _aws_cdk_aws_secretsmanager_ceddda9d.ISecretAttachmentTarget,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''Attach a target to this secret.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7169bcc05cc9fef09daa2e6732c5c382897a8dace487c441a5df1ea46b3123fc)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.invoke(self, "attach", [target]))

    @jsii.member(jsii_name="currentVersionId")
    def current_version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "currentVersionId", []))

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        '''Denies the ``DeleteSecret`` action to all principals within the current account.'''
        return typing.cast(None, jsii.invoke(self, "denyAccountRootDelete", []))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84d1e6becdb6cf951b358b8a8bc63f668e555a12d11b0028528af866931a1c8)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument version_stages", value=version_stages, expected_type=type_hints["version_stages"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee, version_stages]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        _grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grants writing and updating the secret value to some role.

        :param _grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd3a17eb68d15973a8af9441eb6cd97ed5338dead66b7679f005db68637eb5f)
            check_type(argname="argument _grantee", value=_grantee, expected_type=type_hints["_grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [_grantee]))

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(
        self,
        json_field: builtins.str,
    ) -> _aws_cdk_ceddda9d.SecretValue:
        '''Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65919d041d660423e596dfdaa79882405d878d5eda9d3e1171335aa874544f9)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, jsii.invoke(self, "secretValueFromJson", [json_field]))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> _aws_cdk_ceddda9d.ResourceEnvironment:
        '''The environment this resource belongs to.

        For resources that are created and managed by the CDK
        (generally, those created by creating new class instances like Role, Bucket, etc.),
        this is always the same as the environment of the stack they belong to;
        however, for imported resources
        (those obtained from static methods like fromRoleArn, fromBucketName, etc.),
        that might be different than the stack they were imported into.
        '''
        return typing.cast(_aws_cdk_ceddda9d.ResourceEnvironment, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        '''The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        '''The name of the secret.

        For "owned" secrets, this will be the full resource name (secret name + suffix), unless the
        '@aws-cdk/aws-secretsmanager:parseOwnedSecretName' feature flag is set.
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _aws_cdk_ceddda9d.SecretValue:
        '''Retrieve the value of the stored secret as a ``SecretValue``.'''
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        '''The stack in which this resource is defined.'''
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="sync")
    def sync(self) -> "SopsSync":
        return typing.cast("SopsSync", jsii.get(self, "sync"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        '''The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretFullArn"))


@jsii.implements(_aws_cdk_aws_ssm_ceddda9d.IStringParameter)
class SopsStringParameter(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.SopsStringParameter",
):
    '''A drop in replacement for the normal String Parameter, that is populated with the encrypted content of the given sops file.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        parameter_name: typing.Optional[builtins.str] = None,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        description: typing.Optional[builtins.str] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional["UploadType"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param tier: The tier of the string parameter. Default: - undefined
        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c9bb48fa41cbb41be59793bbe0b888d5730c69b1bf3580c6c19d7d6be65d8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SopsStringParameterProps(
            parameter_name=parameter_name,
            encryption_key=encryption_key,
            description=description,
            tier=tier,
            asset_encryption_key=asset_encryption_key,
            auto_generate_iam_permissions=auto_generate_iam_permissions,
            sops_age_key=sops_age_key,
            sops_file_format=sops_file_format,
            sops_file_path=sops_file_path,
            sops_kms_key=sops_kms_key,
            sops_provider=sops_provider,
            sops_s3_bucket=sops_s3_bucket,
            sops_s3_key=sops_s3_key,
            upload_type=upload_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="applyRemovalPolicy")
    def apply_removal_policy(self, policy: _aws_cdk_ceddda9d.RemovalPolicy) -> None:
        '''Apply the given removal policy to this resource.

        The Removal Policy controls what happens to this resource when it stops
        being managed by CloudFormation, either because you've removed it from the
        CDK application or because you've made a change that requires the resource
        to be replaced.

        The resource can be deleted (``RemovalPolicy.DESTROY``), or left in your AWS
        account for data recovery and cleanup later (``RemovalPolicy.RETAIN``).

        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df10361f8a5b128d2433c218086d617e482ecd374cb8020cdc94262ee0764ad)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "applyRemovalPolicy", [policy]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grants read (DescribeParameter, GetParameters, GetParameter, GetParameterHistory) permissions on the SSM Parameter.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77542577a7e47c1c7b3090197d5a0c6f281fe2b6578631e3d20a4d286277d0ff)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grants write (PutParameter) permissions on the SSM Parameter.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96018dc2f4a57e7a385eced7113b3297dcd94c0473ff9eb0d54ebc35edd378de)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> _aws_cdk_ceddda9d.ResourceEnvironment:
        '''The environment this resource belongs to.

        For resources that are created and managed by the CDK
        (generally, those created by creating new class instances like Role, Bucket, etc.),
        this is always the same as the environment of the stack they belong to;
        however, for imported resources
        (those obtained from static methods like fromRoleArn, fromBucketName, etc.),
        that might be different than the stack they were imported into.
        '''
        return typing.cast(_aws_cdk_ceddda9d.ResourceEnvironment, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> builtins.str:
        '''The ARN of the SSM Parameter resource.'''
        return typing.cast(builtins.str, jsii.get(self, "parameterArn"))

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        '''The name of the SSM Parameter resource.'''
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        '''The type of the SSM Parameter resource.'''
        return typing.cast(builtins.str, jsii.get(self, "parameterType"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        '''The stack in which this resource is defined.'''
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        '''The parameter value.

        Value must not nest another parameter. Do not use {{}} in the value.
        '''
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @builtins.property
    @jsii.member(jsii_name="sync")
    def sync(self) -> "SopsSync":
        return typing.cast("SopsSync", jsii.get(self, "sync"))


class SopsSync(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.SopsSync",
):
    '''The custom resource, that is syncing the content from a sops file to a secret.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        resource_type: ResourceType,
        target: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional["UploadType"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param resource_type: Will this Sync deploy a Secret or Parameter(s).
        :param target: The target to populate with the sops file content. - for secret, it's the name or arn of the secret - for parameter, it's the name of the parameter - for parameter multi, it's the prefix of the parameters
        :param encryption_key: The encryption key used for encrypting the ssm parameter if ``parameterName`` is set.
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: - undefined
        :param parameter_names: 
        :param secret: 
        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3134de7215a676a4feb3291975d227477d2dc9d5914405b8ab165ac30d7bad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SopsSyncProps(
            resource_type=resource_type,
            target=target,
            encryption_key=encryption_key,
            flatten_separator=flatten_separator,
            parameter_names=parameter_names,
            secret=secret,
            asset_encryption_key=asset_encryption_key,
            auto_generate_iam_permissions=auto_generate_iam_permissions,
            sops_age_key=sops_age_key,
            sops_file_format=sops_file_format,
            sops_file_path=sops_file_path,
            sops_kms_key=sops_kms_key,
            sops_provider=sops_provider,
            sops_s3_bucket=sops_s3_bucket,
            sops_s3_key=sops_s3_key,
            upload_type=upload_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        '''The current versionId of the secret populated via this resource.'''
        return typing.cast(builtins.str, jsii.get(self, "versionId"))


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsSyncOptions",
    jsii_struct_bases=[],
    name_mapping={
        "asset_encryption_key": "assetEncryptionKey",
        "auto_generate_iam_permissions": "autoGenerateIamPermissions",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "upload_type": "uploadType",
    },
)
class SopsSyncOptions:
    def __init__(
        self,
        *,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional["UploadType"] = None,
    ) -> None:
        '''Configuration options for the SopsSync.

        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e7f5d5a68ee1675b645864f7bab39e30d7c7922956c69686578f4d6fb05723)
            check_type(argname="argument asset_encryption_key", value=asset_encryption_key, expected_type=type_hints["asset_encryption_key"])
            check_type(argname="argument auto_generate_iam_permissions", value=auto_generate_iam_permissions, expected_type=type_hints["auto_generate_iam_permissions"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_encryption_key is not None:
            self._values["asset_encryption_key"] = asset_encryption_key
        if auto_generate_iam_permissions is not None:
            self._values["auto_generate_iam_permissions"] = auto_generate_iam_permissions
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if upload_type is not None:
            self._values["upload_type"] = upload_type

    @builtins.property
    def asset_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The encryption key used by the CDK default Asset S3 Bucket.

        :default: - Trying to get the key using the CDK Bootstrap context.
        '''
        result = self._values.get("asset_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def auto_generate_iam_permissions(self) -> typing.Optional[builtins.bool]:
        '''Should this construct automatically create IAM permissions?

        :default: true
        '''
        result = self._values.get("auto_generate_iam_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional["SopsSyncProvider"]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional["SopsSyncProvider"], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_type(self) -> typing.Optional["UploadType"]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional["UploadType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsSyncOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsSyncProps",
    jsii_struct_bases=[SopsSyncOptions],
    name_mapping={
        "asset_encryption_key": "assetEncryptionKey",
        "auto_generate_iam_permissions": "autoGenerateIamPermissions",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "upload_type": "uploadType",
        "resource_type": "resourceType",
        "target": "target",
        "encryption_key": "encryptionKey",
        "flatten_separator": "flattenSeparator",
        "parameter_names": "parameterNames",
        "secret": "secret",
    },
)
class SopsSyncProps(SopsSyncOptions):
    def __init__(
        self,
        *,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional["UploadType"] = None,
        resource_type: ResourceType,
        target: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    ) -> None:
        '''The configuration options extended by the target Secret / Parameter.

        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param resource_type: Will this Sync deploy a Secret or Parameter(s).
        :param target: The target to populate with the sops file content. - for secret, it's the name or arn of the secret - for parameter, it's the name of the parameter - for parameter multi, it's the prefix of the parameters
        :param encryption_key: The encryption key used for encrypting the ssm parameter if ``parameterName`` is set.
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: - undefined
        :param parameter_names: 
        :param secret: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baaf21b8ae44e7f4d83d5677857cc4141222b3d41237073b75dca6d425c2c34)
            check_type(argname="argument asset_encryption_key", value=asset_encryption_key, expected_type=type_hints["asset_encryption_key"])
            check_type(argname="argument auto_generate_iam_permissions", value=auto_generate_iam_permissions, expected_type=type_hints["auto_generate_iam_permissions"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument flatten_separator", value=flatten_separator, expected_type=type_hints["flatten_separator"])
            check_type(argname="argument parameter_names", value=parameter_names, expected_type=type_hints["parameter_names"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_type": resource_type,
            "target": target,
        }
        if asset_encryption_key is not None:
            self._values["asset_encryption_key"] = asset_encryption_key
        if auto_generate_iam_permissions is not None:
            self._values["auto_generate_iam_permissions"] = auto_generate_iam_permissions
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if upload_type is not None:
            self._values["upload_type"] = upload_type
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if flatten_separator is not None:
            self._values["flatten_separator"] = flatten_separator
        if parameter_names is not None:
            self._values["parameter_names"] = parameter_names
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def asset_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The encryption key used by the CDK default Asset S3 Bucket.

        :default: - Trying to get the key using the CDK Bootstrap context.
        '''
        result = self._values.get("asset_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def auto_generate_iam_permissions(self) -> typing.Optional[builtins.bool]:
        '''Should this construct automatically create IAM permissions?

        :default: true
        '''
        result = self._values.get("auto_generate_iam_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional["SopsSyncProvider"]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional["SopsSyncProvider"], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_type(self) -> typing.Optional["UploadType"]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional["UploadType"], result)

    @builtins.property
    def resource_type(self) -> ResourceType:
        '''Will this Sync deploy a Secret or Parameter(s).'''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(ResourceType, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''The target to populate with the sops file content.

        - for secret, it's the name or arn of the secret
        - for parameter, it's the name of the parameter
        - for parameter multi, it's the prefix of the parameters
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The encryption key used for encrypting the ssm parameter if ``parameterName`` is set.'''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def flatten_separator(self) -> typing.Optional[builtins.str]:
        '''If the structure should be flattened use the provided separator between keys.

        :default: - undefined
        '''
        result = self._values.get("flatten_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_names(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("parameter_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        result = self._values.get("secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsSyncProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable)
class SopsSyncProvider(
    _aws_cdk_aws_lambda_ceddda9d.SingletonFunction,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.SopsSyncProvider",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: typing.Optional[builtins.str] = None,
        *,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        uuid: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param log_group: The log group the function sends logs to. By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/<function name>. However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention. Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it. Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16. If you are deploying to another type of region, please check regional availability first. Default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. This is a legacy API and we strongly recommend you move away from it if you can. Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property to instruct the Lambda function to send logs to it. Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change. Users and code and referencing the name verbatim will have to adjust. In AWS CDK code, you can access the log group name directly from the LogGroup construct:: import * as logs from 'aws-cdk-lib/aws-logs'; declare const myLogGroup: logs.LogGroup; myLogGroup.logGroupName; Default: logs.RetentionDays.INFINITE
        :param role: The role that should be used for the custom resource provider. If you don't specify any, a new role will be created with all required permissions Default: - a new role will be created
        :param security_groups: Only if ``vpc`` is supplied: The list of security groups to associate with the Lambda's network interfaces. Default: - A dedicated security group will be created for the lambda function.
        :param uuid: A unique identifier to identify this provider. Overwrite the default, if you need a dedicated provider. Default: SopsSyncProvider
        :param vpc: VPC network to place Lambda network interfaces. Default: - Lambda function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Default: - Subnets will be chosen automatically.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2ccd4bddb65030756f5b6473575c1a4cc9c9ef0202c6dbe31603b006c05734)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SopsSyncProviderProps(
            log_group=log_group,
            log_retention=log_retention,
            role=role,
            security_groups=security_groups,
            uuid=uuid,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAgeKey")
    def add_age_key(self, key: _aws_cdk_ceddda9d.SecretValue) -> None:
        '''
        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2a1da09ecfa1b4ae9738b2c30c913950581a07762445e7b2bb6fc32606a17d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(None, jsii.invoke(self, "addAgeKey", [key]))


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsSyncProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group": "logGroup",
        "log_retention": "logRetention",
        "role": "role",
        "security_groups": "securityGroups",
        "uuid": "uuid",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class SopsSyncProviderProps:
    def __init__(
        self,
        *,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        uuid: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Configuration options for a custom SopsSyncProvider.

        :param log_group: The log group the function sends logs to. By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/<function name>. However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention. Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it. Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16. If you are deploying to another type of region, please check regional availability first. Default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. This is a legacy API and we strongly recommend you move away from it if you can. Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property to instruct the Lambda function to send logs to it. Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change. Users and code and referencing the name verbatim will have to adjust. In AWS CDK code, you can access the log group name directly from the LogGroup construct:: import * as logs from 'aws-cdk-lib/aws-logs'; declare const myLogGroup: logs.LogGroup; myLogGroup.logGroupName; Default: logs.RetentionDays.INFINITE
        :param role: The role that should be used for the custom resource provider. If you don't specify any, a new role will be created with all required permissions Default: - a new role will be created
        :param security_groups: Only if ``vpc`` is supplied: The list of security groups to associate with the Lambda's network interfaces. Default: - A dedicated security group will be created for the lambda function.
        :param uuid: A unique identifier to identify this provider. Overwrite the default, if you need a dedicated provider. Default: SopsSyncProvider
        :param vpc: VPC network to place Lambda network interfaces. Default: - Lambda function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Default: - Subnets will be chosen automatically.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1cafbc66169426f4b5af87376d7258f7064772025b196978a5b2312e359079)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if uuid is not None:
            self._values["uuid"] = uuid
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''The log group the function sends logs to.

        By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/.
        However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention.

        Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it.

        Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16.
        If you are deploying to another type of region, please check regional availability first.

        :default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
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
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The role that should be used for the custom resource provider.

        If you don't specify any, a new role will be created with all required permissions

        :default: - a new role will be created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''Only if ``vpc`` is supplied: The list of security groups to associate with the Lambda's network interfaces.

        :default: - A dedicated security group will be created for the lambda function.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def uuid(self) -> typing.Optional[builtins.str]:
        '''A unique identifier to identify this provider.

        Overwrite the default, if you need a dedicated provider.

        :default: SopsSyncProvider
        '''
        result = self._values.get("uuid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC network to place Lambda network interfaces.

        :default: - Lambda function is not placed within a VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the network interfaces within the VPC.

        :default: - Subnets will be chosen automatically.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsSyncProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-sops-secrets.UploadType")
class UploadType(enum.Enum):
    INLINE = "INLINE"
    '''Pass the secret data inline (base64 encoded and compressed).'''
    ASSET = "ASSET"
    '''Uplaod the secret data as asset.'''


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsCommonParameterProps",
    jsii_struct_bases=[SopsSyncOptions],
    name_mapping={
        "asset_encryption_key": "assetEncryptionKey",
        "auto_generate_iam_permissions": "autoGenerateIamPermissions",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "upload_type": "uploadType",
        "encryption_key": "encryptionKey",
        "description": "description",
        "tier": "tier",
    },
)
class SopsCommonParameterProps(SopsSyncOptions):
    def __init__(
        self,
        *,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional[SopsSyncProvider] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional[UploadType] = None,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        description: typing.Optional[builtins.str] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    ) -> None:
        '''The configuration options of the StringParameter.

        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param tier: The tier of the string parameter. Default: - undefined
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294699c7977f51cc62460b5f60be1889a1e2fef24597848df175f2ab3fd4485a)
            check_type(argname="argument asset_encryption_key", value=asset_encryption_key, expected_type=type_hints["asset_encryption_key"])
            check_type(argname="argument auto_generate_iam_permissions", value=auto_generate_iam_permissions, expected_type=type_hints["auto_generate_iam_permissions"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encryption_key": encryption_key,
        }
        if asset_encryption_key is not None:
            self._values["asset_encryption_key"] = asset_encryption_key
        if auto_generate_iam_permissions is not None:
            self._values["auto_generate_iam_permissions"] = auto_generate_iam_permissions
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if upload_type is not None:
            self._values["upload_type"] = upload_type
        if description is not None:
            self._values["description"] = description
        if tier is not None:
            self._values["tier"] = tier

    @builtins.property
    def asset_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The encryption key used by the CDK default Asset S3 Bucket.

        :default: - Trying to get the key using the CDK Bootstrap context.
        '''
        result = self._values.get("asset_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def auto_generate_iam_permissions(self) -> typing.Optional[builtins.bool]:
        '''Should this construct automatically create IAM permissions?

        :default: true
        '''
        result = self._values.get("auto_generate_iam_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional[SopsSyncProvider]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional[SopsSyncProvider], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_type(self) -> typing.Optional[UploadType]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional[UploadType], result)

    @builtins.property
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The customer-managed encryption key to use for encrypting the secret value.

        :default: - A default KMS key for the account and region is used.
        '''
        result = self._values.get("encryption_key")
        assert result is not None, "Required property 'encryption_key' is missing"
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Information about the parameter that you want to add to the system.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier]:
        '''The tier of the string parameter.

        :default: - undefined
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsCommonParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsSecretProps",
    jsii_struct_bases=[SopsSyncOptions],
    name_mapping={
        "asset_encryption_key": "assetEncryptionKey",
        "auto_generate_iam_permissions": "autoGenerateIamPermissions",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "upload_type": "uploadType",
        "description": "description",
        "encryption_key": "encryptionKey",
        "raw_output": "rawOutput",
        "removal_policy": "removalPolicy",
        "replica_regions": "replicaRegions",
        "secret_name": "secretName",
    },
)
class SopsSecretProps(SopsSyncOptions):
    def __init__(
        self,
        *,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional[SopsSyncProvider] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional[UploadType] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        raw_output: typing.Optional[RawOutput] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        replica_regions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
        secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The configuration options of the SopsSecret.

        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param raw_output: Should the secret parsed and transformed to json? Default: - undefined - STRING for binary secrets, else no raw output
        :param removal_policy: Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param replica_regions: A list of regions where to replicate this secret. Default: - Secret is not replicated
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5ff836a3767bbc726a1167e9f5e789f0fad2dcaf72b41a245494f0a121a8a3)
            check_type(argname="argument asset_encryption_key", value=asset_encryption_key, expected_type=type_hints["asset_encryption_key"])
            check_type(argname="argument auto_generate_iam_permissions", value=auto_generate_iam_permissions, expected_type=type_hints["auto_generate_iam_permissions"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument raw_output", value=raw_output, expected_type=type_hints["raw_output"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument replica_regions", value=replica_regions, expected_type=type_hints["replica_regions"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_encryption_key is not None:
            self._values["asset_encryption_key"] = asset_encryption_key
        if auto_generate_iam_permissions is not None:
            self._values["auto_generate_iam_permissions"] = auto_generate_iam_permissions
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if upload_type is not None:
            self._values["upload_type"] = upload_type
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if raw_output is not None:
            self._values["raw_output"] = raw_output
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replica_regions is not None:
            self._values["replica_regions"] = replica_regions
        if secret_name is not None:
            self._values["secret_name"] = secret_name

    @builtins.property
    def asset_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The encryption key used by the CDK default Asset S3 Bucket.

        :default: - Trying to get the key using the CDK Bootstrap context.
        '''
        result = self._values.get("asset_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def auto_generate_iam_permissions(self) -> typing.Optional[builtins.bool]:
        '''Should this construct automatically create IAM permissions?

        :default: true
        '''
        result = self._values.get("auto_generate_iam_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional[SopsSyncProvider]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional[SopsSyncProvider], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_type(self) -> typing.Optional[UploadType]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional[UploadType], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional, human-friendly description of the secret.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The customer-managed encryption key to use for encrypting the secret value.

        :default: - A default KMS key for the account and region is used.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def raw_output(self) -> typing.Optional[RawOutput]:
        '''Should the secret parsed and transformed to json?

        :default: - undefined - STRING for binary secrets, else no raw output
        '''
        result = self._values.get("raw_output")
        return typing.cast(typing.Optional[RawOutput], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Policy to apply when the secret is removed from this stack.

        :default: - Not set.
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def replica_regions(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion]]:
        '''A list of regions where to replicate this secret.

        :default: - Secret is not replicated
        '''
        result = self._values.get("replica_regions")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion]], result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''A name for the secret.

        Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to
        30 days blackout period. During that period, it is not possible to create another secret that shares the same name.

        :default: - A name is generated by CloudFormation.
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsStringParameterProps",
    jsii_struct_bases=[SopsCommonParameterProps],
    name_mapping={
        "asset_encryption_key": "assetEncryptionKey",
        "auto_generate_iam_permissions": "autoGenerateIamPermissions",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "upload_type": "uploadType",
        "encryption_key": "encryptionKey",
        "description": "description",
        "tier": "tier",
        "parameter_name": "parameterName",
    },
)
class SopsStringParameterProps(SopsCommonParameterProps):
    def __init__(
        self,
        *,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional[SopsSyncProvider] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional[UploadType] = None,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        description: typing.Optional[builtins.str] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
        parameter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param tier: The tier of the string parameter. Default: - undefined
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4c6b41b250704c51710cadcac0559f659733c6085f47a56587b680e5275a68)
            check_type(argname="argument asset_encryption_key", value=asset_encryption_key, expected_type=type_hints["asset_encryption_key"])
            check_type(argname="argument auto_generate_iam_permissions", value=auto_generate_iam_permissions, expected_type=type_hints["auto_generate_iam_permissions"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encryption_key": encryption_key,
        }
        if asset_encryption_key is not None:
            self._values["asset_encryption_key"] = asset_encryption_key
        if auto_generate_iam_permissions is not None:
            self._values["auto_generate_iam_permissions"] = auto_generate_iam_permissions
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if upload_type is not None:
            self._values["upload_type"] = upload_type
        if description is not None:
            self._values["description"] = description
        if tier is not None:
            self._values["tier"] = tier
        if parameter_name is not None:
            self._values["parameter_name"] = parameter_name

    @builtins.property
    def asset_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The encryption key used by the CDK default Asset S3 Bucket.

        :default: - Trying to get the key using the CDK Bootstrap context.
        '''
        result = self._values.get("asset_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def auto_generate_iam_permissions(self) -> typing.Optional[builtins.bool]:
        '''Should this construct automatically create IAM permissions?

        :default: true
        '''
        result = self._values.get("auto_generate_iam_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional[SopsSyncProvider]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional[SopsSyncProvider], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_type(self) -> typing.Optional[UploadType]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional[UploadType], result)

    @builtins.property
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The customer-managed encryption key to use for encrypting the secret value.

        :default: - A default KMS key for the account and region is used.
        '''
        result = self._values.get("encryption_key")
        assert result is not None, "Required property 'encryption_key' is missing"
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Information about the parameter that you want to add to the system.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier]:
        '''The tier of the string parameter.

        :default: - undefined
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier], result)

    @builtins.property
    def parameter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter.

        :default: - a name will be generated by CloudFormation
        '''
        result = self._values.get("parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsStringParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-sops-secrets.MultiStringParameterProps",
    jsii_struct_bases=[SopsCommonParameterProps],
    name_mapping={
        "asset_encryption_key": "assetEncryptionKey",
        "auto_generate_iam_permissions": "autoGenerateIamPermissions",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "upload_type": "uploadType",
        "encryption_key": "encryptionKey",
        "description": "description",
        "tier": "tier",
        "key_prefix": "keyPrefix",
        "key_separator": "keySeparator",
    },
)
class MultiStringParameterProps(SopsCommonParameterProps):
    def __init__(
        self,
        *,
        asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional[SopsSyncProvider] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        upload_type: typing.Optional[UploadType] = None,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        description: typing.Optional[builtins.str] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        key_separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param asset_encryption_key: The encryption key used by the CDK default Asset S3 Bucket. Default: - Trying to get the key using the CDK Bootstrap context.
        :param auto_generate_iam_permissions: Should this construct automatically create IAM permissions? Default: true
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param tier: The tier of the string parameter. Default: - undefined
        :param key_prefix: The prefix used for all parameters. Default: - '/'
        :param key_separator: The seperator used to seperate keys. Default: - '/'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7b531b153efe4b2be69da7047a42a42b5f4c97525cc7994a39eb4156186e11)
            check_type(argname="argument asset_encryption_key", value=asset_encryption_key, expected_type=type_hints["asset_encryption_key"])
            check_type(argname="argument auto_generate_iam_permissions", value=auto_generate_iam_permissions, expected_type=type_hints["auto_generate_iam_permissions"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            check_type(argname="argument key_separator", value=key_separator, expected_type=type_hints["key_separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encryption_key": encryption_key,
        }
        if asset_encryption_key is not None:
            self._values["asset_encryption_key"] = asset_encryption_key
        if auto_generate_iam_permissions is not None:
            self._values["auto_generate_iam_permissions"] = auto_generate_iam_permissions
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if upload_type is not None:
            self._values["upload_type"] = upload_type
        if description is not None:
            self._values["description"] = description
        if tier is not None:
            self._values["tier"] = tier
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix
        if key_separator is not None:
            self._values["key_separator"] = key_separator

    @builtins.property
    def asset_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The encryption key used by the CDK default Asset S3 Bucket.

        :default: - Trying to get the key using the CDK Bootstrap context.
        '''
        result = self._values.get("asset_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def auto_generate_iam_permissions(self) -> typing.Optional[builtins.bool]:
        '''Should this construct automatically create IAM permissions?

        :default: true
        '''
        result = self._values.get("auto_generate_iam_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional[SopsSyncProvider]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional[SopsSyncProvider], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def upload_type(self) -> typing.Optional[UploadType]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional[UploadType], result)

    @builtins.property
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The customer-managed encryption key to use for encrypting the secret value.

        :default: - A default KMS key for the account and region is used.
        '''
        result = self._values.get("encryption_key")
        assert result is not None, "Required property 'encryption_key' is missing"
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Information about the parameter that you want to add to the system.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier]:
        '''The tier of the string parameter.

        :default: - undefined
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier], result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix used for all parameters.

        :default: - '/'
        '''
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_separator(self) -> typing.Optional[builtins.str]:
        '''The seperator used to seperate keys.

        :default: - '/'
        '''
        result = self._values.get("key_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultiStringParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MultiStringParameter",
    "MultiStringParameterProps",
    "RawOutput",
    "ResourceType",
    "SopsCommonParameterProps",
    "SopsSecret",
    "SopsSecretProps",
    "SopsStringParameter",
    "SopsStringParameterProps",
    "SopsSync",
    "SopsSyncOptions",
    "SopsSyncProps",
    "SopsSyncProvider",
    "SopsSyncProviderProps",
    "UploadType",
]

publication.publish()

def _typecheckingstub__520cbd9adefd0e4a3135f2f09bd2fa26acb8be581e0f77b06f12862c0125b5b4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    key_prefix: typing.Optional[builtins.str] = None,
    key_separator: typing.Optional[builtins.str] = None,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    description: typing.Optional[builtins.str] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641b47276285e7c457eb639fea01f8b2e2f54dd58d3bc6f9e184404914516a11(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    raw_output: typing.Optional[RawOutput] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    replica_regions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_name: typing.Optional[builtins.str] = None,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd08508625195135b318d9657d717ca369ecceb1cc51cd6b3fa8c66c489c3dad(
    id: builtins.str,
    *,
    automatically_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    hosted_rotation: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.HostedRotation] = None,
    rotate_immediately_on_update: typing.Optional[builtins.bool] = None,
    rotation_lambda: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54076b0a3bb41bb64b3bbd471f51ee813e6ce6437b4b2ee14f76246051614126(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d3b1469d7d365dc715e5fc30a5ca749e3a126bab5731a9cb3e3bd09de54905(
    policy: _aws_cdk_ceddda9d.RemovalPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7169bcc05cc9fef09daa2e6732c5c382897a8dace487c441a5df1ea46b3123fc(
    target: _aws_cdk_aws_secretsmanager_ceddda9d.ISecretAttachmentTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84d1e6becdb6cf951b358b8a8bc63f668e555a12d11b0028528af866931a1c8(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd3a17eb68d15973a8af9441eb6cd97ed5338dead66b7679f005db68637eb5f(
    _grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65919d041d660423e596dfdaa79882405d878d5eda9d3e1171335aa874544f9(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c9bb48fa41cbb41be59793bbe0b888d5730c69b1bf3580c6c19d7d6be65d8d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    description: typing.Optional[builtins.str] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df10361f8a5b128d2433c218086d617e482ecd374cb8020cdc94262ee0764ad(
    policy: _aws_cdk_ceddda9d.RemovalPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77542577a7e47c1c7b3090197d5a0c6f281fe2b6578631e3d20a4d286277d0ff(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96018dc2f4a57e7a385eced7113b3297dcd94c0473ff9eb0d54ebc35edd378de(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3134de7215a676a4feb3291975d227477d2dc9d5914405b8ab165ac30d7bad(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    resource_type: ResourceType,
    target: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e7f5d5a68ee1675b645864f7bab39e30d7c7922956c69686578f4d6fb05723(
    *,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baaf21b8ae44e7f4d83d5677857cc4141222b3d41237073b75dca6d425c2c34(
    *,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
    resource_type: ResourceType,
    target: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2ccd4bddb65030756f5b6473575c1a4cc9c9ef0202c6dbe31603b006c05734(
    scope: _constructs_77d1e7e8.Construct,
    id: typing.Optional[builtins.str] = None,
    *,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    uuid: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2a1da09ecfa1b4ae9738b2c30c913950581a07762445e7b2bb6fc32606a17d(
    key: _aws_cdk_ceddda9d.SecretValue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1cafbc66169426f4b5af87376d7258f7064772025b196978a5b2312e359079(
    *,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    uuid: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294699c7977f51cc62460b5f60be1889a1e2fef24597848df175f2ab3fd4485a(
    *,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    description: typing.Optional[builtins.str] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5ff836a3767bbc726a1167e9f5e789f0fad2dcaf72b41a245494f0a121a8a3(
    *,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    raw_output: typing.Optional[RawOutput] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    replica_regions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4c6b41b250704c51710cadcac0559f659733c6085f47a56587b680e5275a68(
    *,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    description: typing.Optional[builtins.str] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    parameter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7b531b153efe4b2be69da7047a42a42b5f4c97525cc7994a39eb4156186e11(
    *,
    asset_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    auto_generate_iam_permissions: typing.Optional[builtins.bool] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    upload_type: typing.Optional[UploadType] = None,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    description: typing.Optional[builtins.str] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    key_separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
