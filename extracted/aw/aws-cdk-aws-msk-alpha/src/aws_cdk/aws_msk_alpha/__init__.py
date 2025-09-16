r'''
# Amazon Managed Streaming for Apache Kafka Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[Amazon MSK](https://aws.amazon.com/msk/) is a fully managed service that makes it easy for you to build and run applications that use Apache Kafka to process streaming data.

The following example creates an MSK Cluster.

```python
# vpc: ec2.Vpc

cluster = msk.Cluster(self, "Cluster",
    cluster_name="myCluster",
    kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
    vpc=vpc
)
```

## Allowing Connections

To control who can access the Cluster, use the `.connections` attribute. For a list of ports used by MSK, refer to the [MSK documentation](https://docs.aws.amazon.com/msk/latest/developerguide/client-access.html#port-info).

```python
# vpc: ec2.Vpc

cluster = msk.Cluster(self, "Cluster",
    cluster_name="myCluster",
    kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
    vpc=vpc
)

cluster.connections.allow_from(
    ec2.Peer.ipv4("1.2.3.4/8"),
    ec2.Port.tcp(2181))
cluster.connections.allow_from(
    ec2.Peer.ipv4("1.2.3.4/8"),
    ec2.Port.tcp(9094))
```

## Cluster Endpoints

You can use the following attributes to get a list of the Kafka broker or ZooKeeper node endpoints

```python
# cluster: msk.Cluster

CfnOutput(self, "BootstrapBrokers", value=cluster.bootstrap_brokers)
CfnOutput(self, "BootstrapBrokersTls", value=cluster.bootstrap_brokers_tls)
CfnOutput(self, "BootstrapBrokersSaslScram", value=cluster.bootstrap_brokers_sasl_scram)
CfnOutput(self, "BootstrapBrokerStringSaslIam", value=cluster.bootstrap_brokers_sasl_iam)
CfnOutput(self, "ZookeeperConnection", value=cluster.zookeeper_connection_string)
CfnOutput(self, "ZookeeperConnectionTls", value=cluster.zookeeper_connection_string_tls)
```

## Importing an existing Cluster

To import an existing MSK cluster into your CDK app use the `.fromClusterArn()` method.

```python
cluster = msk.Cluster.from_cluster_arn(self, "Cluster", "arn:aws:kafka:us-west-2:1234567890:cluster/a-cluster/11111111-1111-1111-1111-111111111111-1")
```

## Client Authentication

[MSK supports](https://docs.aws.amazon.com/msk/latest/developerguide/kafka_apis_iam.html) the following authentication mechanisms.

### TLS

To enable client authentication with TLS set the `certificateAuthorityArns` property to reference your ACM Private CA. [More info on Private CAs.](https://docs.aws.amazon.com/msk/latest/developerguide/msk-authentication.html)

```python
import aws_cdk.aws_acmpca as acmpca

# vpc: ec2.Vpc

cluster = msk.Cluster(self, "Cluster",
    cluster_name="myCluster",
    kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
    vpc=vpc,
    encryption_in_transit=msk.EncryptionInTransitConfig(
        client_broker=msk.ClientBrokerEncryption.TLS
    ),
    client_authentication=msk.ClientAuthentication.tls(
        certificate_authorities=[
            acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", "arn:aws:acm-pca:us-west-2:1234567890:certificate-authority/11111111-1111-1111-1111-111111111111")
        ]
    )
)
```

### SASL/SCRAM

Enable client authentication with [SASL/SCRAM](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html):

```python
# vpc: ec2.Vpc

cluster = msk.Cluster(self, "cluster",
    cluster_name="myCluster",
    kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
    vpc=vpc,
    encryption_in_transit=msk.EncryptionInTransitConfig(
        client_broker=msk.ClientBrokerEncryption.TLS
    ),
    client_authentication=msk.ClientAuthentication.sasl(
        scram=True
    )
)
```

### IAM

Enable client authentication with [IAM](https://docs.aws.amazon.com/msk/latest/developerguide/iam-access-control.html):

```python
# vpc: ec2.Vpc

cluster = msk.Cluster(self, "cluster",
    cluster_name="myCluster",
    kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
    vpc=vpc,
    encryption_in_transit=msk.EncryptionInTransitConfig(
        client_broker=msk.ClientBrokerEncryption.TLS
    ),
    client_authentication=msk.ClientAuthentication.sasl(
        iam=True
    )
)
```

### SASL/IAM + TLS

Enable client authentication with [IAM](https://docs.aws.amazon.com/msk/latest/developerguide/iam-access-control.html)
as well as enable client authentication with TLS by setting the `certificateAuthorityArns` property to reference your ACM Private CA. [More info on Private CAs.](https://docs.aws.amazon.com/msk/latest/developerguide/msk-authentication.html)

```python
import aws_cdk.aws_acmpca as acmpca

# vpc: ec2.Vpc

cluster = msk.Cluster(self, "Cluster",
    cluster_name="myCluster",
    kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
    vpc=vpc,
    encryption_in_transit=msk.EncryptionInTransitConfig(
        client_broker=msk.ClientBrokerEncryption.TLS
    ),
    client_authentication=msk.ClientAuthentication.sasl_tls(
        iam=True,
        certificate_authorities=[
            acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", "arn:aws:acm-pca:us-west-2:1234567890:certificate-authority/11111111-1111-1111-1111-111111111111")
        ]
    )
)
```

## Logging

You can deliver Apache Kafka broker logs to one or more of the following destination types:
Amazon CloudWatch Logs, Amazon S3, Amazon Data Firehose.

To configure logs to be sent to an S3 bucket, provide a bucket in the `logging` config.

```python
# vpc: ec2.Vpc
# bucket: s3.IBucket

cluster = msk.Cluster(self, "cluster",
    cluster_name="myCluster",
    kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
    vpc=vpc,
    logging=msk.BrokerLogging(
        s3=msk.S3LoggingConfiguration(
            bucket=bucket
        )
    )
)
```

When the S3 destination is configured, AWS will automatically create an S3 bucket policy
that allows the service to write logs to the bucket. This makes it impossible to later update
that bucket policy. To have CDK create the bucket policy so that future updates can be made,
the `@aws-cdk/aws-s3:createDefaultLoggingPolicy` [feature flag](https://docs.aws.amazon.com/cdk/v2/guide/featureflags.html) can be used. This can be set
in the `cdk.json` file.

```json
{
  "context": {
    "@aws-cdk/aws-s3:createDefaultLoggingPolicy": true
  }
}
```

## Storage Mode

You can configure an MSK cluster storage mode using the `storageMode` property.

Tiered storage is a low-cost storage tier for Amazon MSK that scales to virtually unlimited storage,
making it cost-effective to build streaming data applications.

> Visit [Tiered storage](https://docs.aws.amazon.com/msk/latest/developerguide/msk-tiered-storage.html)
> to see the list of compatible Kafka versions and for more details.

```python
# vpc: ec2.Vpc
# bucket: s3.IBucket


cluster = msk.Cluster(self, "cluster",
    cluster_name="myCluster",
    kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
    vpc=vpc,
    storage_mode=msk.StorageMode.TIERED
)
```

## MSK Serverless

You can also use MSK Serverless by using `ServerlessCluster` class.

MSK Serverless is a cluster type for Amazon MSK that makes it possible for you to run Apache Kafka without having to manage and scale cluster capacity.

MSK Serverless requires IAM access control for all clusters.

For more infomation, see [Use MSK Serverless clusters](https://docs.aws.amazon.com/msk/latest/developerguide/serverless-getting-started.html).

```python
# vpc: ec2.Vpc


serverless_cluster = msk.ServerlessCluster(self, "ServerlessCluster",
    cluster_name="MyServerlessCluster",
    vpc_configs=[msk.VpcConfig(vpc=vpc)
    ]
)
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
import aws_cdk.aws_acmpca as _aws_cdk_aws_acmpca_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.BrokerLogging",
    jsii_struct_bases=[],
    name_mapping={
        "cloudwatch_log_group": "cloudwatchLogGroup",
        "firehose_delivery_stream_name": "firehoseDeliveryStreamName",
        "s3": "s3",
    },
)
class BrokerLogging:
    def __init__(
        self,
        *,
        cloudwatch_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        firehose_delivery_stream_name: typing.Optional[builtins.str] = None,
        s3: typing.Optional[typing.Union["S3LoggingConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Configuration details related to broker logs.

        :param cloudwatch_log_group: (experimental) The CloudWatch Logs group that is the destination for broker logs. Default: - disabled
        :param firehose_delivery_stream_name: (experimental) The Amazon Data Firehose delivery stream that is the destination for broker logs. Default: - disabled
        :param s3: (experimental) Details of the Amazon S3 destination for broker logs. Default: - disabled

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            # bucket: s3.IBucket
            
            cluster = msk.Cluster(self, "cluster",
                cluster_name="myCluster",
                kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
                vpc=vpc,
                logging=msk.BrokerLogging(
                    s3=msk.S3LoggingConfiguration(
                        bucket=bucket
                    )
                )
            )
        '''
        if isinstance(s3, dict):
            s3 = S3LoggingConfiguration(**s3)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba586b7db9e5dd092a5b8f9676408abd0e8865e17a5980b7acb9ac4b970f225)
            check_type(argname="argument cloudwatch_log_group", value=cloudwatch_log_group, expected_type=type_hints["cloudwatch_log_group"])
            check_type(argname="argument firehose_delivery_stream_name", value=firehose_delivery_stream_name, expected_type=type_hints["firehose_delivery_stream_name"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloudwatch_log_group is not None:
            self._values["cloudwatch_log_group"] = cloudwatch_log_group
        if firehose_delivery_stream_name is not None:
            self._values["firehose_delivery_stream_name"] = firehose_delivery_stream_name
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def cloudwatch_log_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''(experimental) The CloudWatch Logs group that is the destination for broker logs.

        :default: - disabled

        :stability: experimental
        '''
        result = self._values.get("cloudwatch_log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def firehose_delivery_stream_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Amazon Data Firehose delivery stream that is the destination for broker logs.

        :default: - disabled

        :stability: experimental
        '''
        result = self._values.get("firehose_delivery_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3(self) -> typing.Optional["S3LoggingConfiguration"]:
        '''(experimental) Details of the Amazon S3 destination for broker logs.

        :default: - disabled

        :stability: experimental
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["S3LoggingConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BrokerLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClientAuthentication(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-msk-alpha.ClientAuthentication",
):
    '''(experimental) Configuration properties for client authentication.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_acmpca as acmpca
        
        # vpc: ec2.Vpc
        
        cluster = msk.Cluster(self, "Cluster",
            cluster_name="myCluster",
            kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
            vpc=vpc,
            encryption_in_transit=msk.EncryptionInTransitConfig(
                client_broker=msk.ClientBrokerEncryption.TLS
            ),
            client_authentication=msk.ClientAuthentication.tls(
                certificate_authorities=[
                    acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", "arn:aws:acm-pca:us-west-2:1234567890:certificate-authority/11111111-1111-1111-1111-111111111111")
                ]
            )
        )
    '''

    @jsii.member(jsii_name="sasl")
    @builtins.classmethod
    def sasl(
        cls,
        *,
        iam: typing.Optional[builtins.bool] = None,
        key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef] = None,
        scram: typing.Optional[builtins.bool] = None,
    ) -> "ClientAuthentication":
        '''(experimental) SASL authentication.

        :param iam: (experimental) Enable IAM access control. Default: false
        :param key: (experimental) KMS Key to encrypt SASL/SCRAM secrets. You must use a customer master key (CMK) when creating users in secrets manager. You cannot use a Secret with Amazon MSK that uses the default Secrets Manager encryption key. Default: - CMK will be created with alias msk/{clusterName}/sasl/scram
        :param scram: (experimental) Enable SASL/SCRAM authentication. Default: false

        :stability: experimental
        '''
        props = SaslAuthProps(iam=iam, key=key, scram=scram)

        return typing.cast("ClientAuthentication", jsii.sinvoke(cls, "sasl", [props]))

    @jsii.member(jsii_name="saslTls")
    @builtins.classmethod
    def sasl_tls(
        cls,
        *,
        iam: typing.Optional[builtins.bool] = None,
        key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef] = None,
        scram: typing.Optional[builtins.bool] = None,
        certificate_authorities: typing.Optional[typing.Sequence[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]] = None,
    ) -> "ClientAuthentication":
        '''(experimental) SASL + TLS authentication.

        :param iam: (experimental) Enable IAM access control. Default: false
        :param key: (experimental) KMS Key to encrypt SASL/SCRAM secrets. You must use a customer master key (CMK) when creating users in secrets manager. You cannot use a Secret with Amazon MSK that uses the default Secrets Manager encryption key. Default: - CMK will be created with alias msk/{clusterName}/sasl/scram
        :param scram: (experimental) Enable SASL/SCRAM authentication. Default: false
        :param certificate_authorities: (experimental) List of ACM Certificate Authorities to enable TLS authentication. Default: - none

        :stability: experimental
        '''
        sasl_tls_props = SaslTlsAuthProps(
            iam=iam,
            key=key,
            scram=scram,
            certificate_authorities=certificate_authorities,
        )

        return typing.cast("ClientAuthentication", jsii.sinvoke(cls, "saslTls", [sasl_tls_props]))

    @jsii.member(jsii_name="tls")
    @builtins.classmethod
    def tls(
        cls,
        *,
        certificate_authorities: typing.Optional[typing.Sequence[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]] = None,
    ) -> "ClientAuthentication":
        '''(experimental) TLS authentication.

        :param certificate_authorities: (experimental) List of ACM Certificate Authorities to enable TLS authentication. Default: - none

        :stability: experimental
        '''
        props = TlsAuthProps(certificate_authorities=certificate_authorities)

        return typing.cast("ClientAuthentication", jsii.sinvoke(cls, "tls", [props]))

    @builtins.property
    @jsii.member(jsii_name="saslProps")
    def sasl_props(self) -> typing.Optional["SaslAuthProps"]:
        '''(experimental) - properties for SASL authentication.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["SaslAuthProps"], jsii.get(self, "saslProps"))

    @builtins.property
    @jsii.member(jsii_name="tlsProps")
    def tls_props(self) -> typing.Optional["TlsAuthProps"]:
        '''(experimental) - properties for TLS authentication.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["TlsAuthProps"], jsii.get(self, "tlsProps"))


@jsii.enum(jsii_type="@aws-cdk/aws-msk-alpha.ClientBrokerEncryption")
class ClientBrokerEncryption(enum.Enum):
    '''(experimental) Indicates the encryption setting for data in transit between clients and brokers.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_acmpca as acmpca
        
        # vpc: ec2.Vpc
        
        cluster = msk.Cluster(self, "Cluster",
            cluster_name="myCluster",
            kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
            vpc=vpc,
            encryption_in_transit=msk.EncryptionInTransitConfig(
                client_broker=msk.ClientBrokerEncryption.TLS
            ),
            client_authentication=msk.ClientAuthentication.tls(
                certificate_authorities=[
                    acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", "arn:aws:acm-pca:us-west-2:1234567890:certificate-authority/11111111-1111-1111-1111-111111111111")
                ]
            )
        )
    '''

    TLS = "TLS"
    '''(experimental) TLS means that client-broker communication is enabled with TLS only.

    :stability: experimental
    '''
    TLS_PLAINTEXT = "TLS_PLAINTEXT"
    '''(experimental) TLS_PLAINTEXT means that client-broker communication is enabled for both TLS-encrypted, as well as plaintext data.

    :stability: experimental
    '''
    PLAINTEXT = "PLAINTEXT"
    '''(experimental) PLAINTEXT means that client-broker communication is enabled in plaintext only.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.ClusterConfigurationInfo",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "revision": "revision"},
)
class ClusterConfigurationInfo:
    def __init__(self, *, arn: builtins.str, revision: jsii.Number) -> None:
        '''(experimental) The Amazon MSK configuration to use for the cluster.

        Note: There is currently no Cloudformation Resource to create a Configuration

        :param arn: (experimental) The Amazon Resource Name (ARN) of the MSK configuration to use. For example, arn:aws:kafka:us-east-1:123456789012:configuration/example-configuration-name/abcdabcd-1234-abcd-1234-abcd123e8e8e-1.
        :param revision: (experimental) The revision of the Amazon MSK configuration to use.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_msk_alpha as msk_alpha
            
            cluster_configuration_info = msk_alpha.ClusterConfigurationInfo(
                arn="arn",
                revision=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c843d4de610e7657dc25ae7cbdd2c8bba8b60a980c8877eba757e6e63c7ebd)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "revision": revision,
        }

    @builtins.property
    def arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the MSK configuration to use.

        For example, arn:aws:kafka:us-east-1:123456789012:configuration/example-configuration-name/abcdabcd-1234-abcd-1234-abcd123e8e8e-1.

        :stability: experimental
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def revision(self) -> jsii.Number:
        '''(experimental) The revision of the Amazon MSK configuration to use.

        :stability: experimental
        '''
        result = self._values.get("revision")
        assert result is not None, "Required property 'revision' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterConfigurationInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-msk-alpha.ClusterMonitoringLevel")
class ClusterMonitoringLevel(enum.Enum):
    '''(experimental) The level of monitoring for the MSK cluster.

    :see: https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html#metrics-details
    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''(experimental) Default metrics are the essential metrics to monitor.

    :stability: experimental
    '''
    PER_BROKER = "PER_BROKER"
    '''(experimental) Per Broker metrics give you metrics at the broker level.

    :stability: experimental
    '''
    PER_TOPIC_PER_BROKER = "PER_TOPIC_PER_BROKER"
    '''(experimental) Per Topic Per Broker metrics help you understand volume at the topic level.

    :stability: experimental
    '''
    PER_TOPIC_PER_PARTITION = "PER_TOPIC_PER_PARTITION"
    '''(experimental) Per Topic Per Partition metrics help you understand consumer group lag at the topic partition level.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.ClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "kafka_version": "kafkaVersion",
        "vpc": "vpc",
        "client_authentication": "clientAuthentication",
        "configuration_info": "configurationInfo",
        "ebs_storage_info": "ebsStorageInfo",
        "encryption_in_transit": "encryptionInTransit",
        "instance_type": "instanceType",
        "logging": "logging",
        "monitoring": "monitoring",
        "number_of_broker_nodes": "numberOfBrokerNodes",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "storage_mode": "storageMode",
        "vpc_subnets": "vpcSubnets",
    },
)
class ClusterProps:
    def __init__(
        self,
        *,
        cluster_name: builtins.str,
        kafka_version: "KafkaVersion",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        client_authentication: typing.Optional[ClientAuthentication] = None,
        configuration_info: typing.Optional[typing.Union[ClusterConfigurationInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        ebs_storage_info: typing.Optional[typing.Union["EbsStorageInfo", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_in_transit: typing.Optional[typing.Union["EncryptionInTransitConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        logging: typing.Optional[typing.Union[BrokerLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring: typing.Optional[typing.Union["MonitoringConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        number_of_broker_nodes: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        storage_mode: typing.Optional["StorageMode"] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for a MSK Cluster.

        :param cluster_name: (experimental) The physical name of the cluster.
        :param kafka_version: (experimental) The version of Apache Kafka.
        :param vpc: (experimental) Defines the virtual networking environment for this cluster. Must have at least 2 subnets in two different AZs.
        :param client_authentication: (experimental) Configuration properties for client authentication. MSK supports using private TLS certificates or SASL/SCRAM to authenticate the identity of clients. Default: - disabled
        :param configuration_info: (experimental) The Amazon MSK configuration to use for the cluster. Default: - none
        :param ebs_storage_info: (experimental) Information about storage volumes attached to MSK broker nodes. Default: - 1000 GiB EBS volume
        :param encryption_in_transit: (experimental) Config details for encryption in transit. Default: - enabled
        :param instance_type: (experimental) The EC2 instance type that you want Amazon MSK to use when it creates your brokers. Default: kafka.m5.large
        :param logging: (experimental) Configure your MSK cluster to send broker logs to different destination types. Default: - disabled
        :param monitoring: (experimental) Cluster monitoring configuration. Default: - DEFAULT monitoring level
        :param number_of_broker_nodes: (experimental) Number of Apache Kafka brokers deployed in each Availability Zone. Default: 1
        :param removal_policy: (experimental) What to do when this resource is deleted from a stack. Default: RemovalPolicy.RETAIN
        :param security_groups: (experimental) The AWS security groups to associate with the elastic network interfaces in order to specify who can connect to and communicate with the Amazon MSK cluster. Default: - create new security group
        :param storage_mode: (experimental) This controls storage mode for supported storage tiers. Default: - StorageMode.LOCAL
        :param vpc_subnets: (experimental) Where to place the nodes within the VPC. Amazon MSK distributes the broker nodes evenly across the subnets that you specify. The subnets that you specify must be in distinct Availability Zones. Client subnets can't be in Availability Zone us-east-1e. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            cluster = msk.Cluster(self, "cluster",
                cluster_name="myCluster",
                kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
                vpc=vpc,
                encryption_in_transit=msk.EncryptionInTransitConfig(
                    client_broker=msk.ClientBrokerEncryption.TLS
                ),
                client_authentication=msk.ClientAuthentication.sasl(
                    scram=True
                )
            )
        '''
        if isinstance(configuration_info, dict):
            configuration_info = ClusterConfigurationInfo(**configuration_info)
        if isinstance(ebs_storage_info, dict):
            ebs_storage_info = EbsStorageInfo(**ebs_storage_info)
        if isinstance(encryption_in_transit, dict):
            encryption_in_transit = EncryptionInTransitConfig(**encryption_in_transit)
        if isinstance(logging, dict):
            logging = BrokerLogging(**logging)
        if isinstance(monitoring, dict):
            monitoring = MonitoringConfiguration(**monitoring)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7acb1d0e21413d16efb1d11f4a29cc860b92ac278e0b0187d75e3eb1f71b1492)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument kafka_version", value=kafka_version, expected_type=type_hints["kafka_version"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument client_authentication", value=client_authentication, expected_type=type_hints["client_authentication"])
            check_type(argname="argument configuration_info", value=configuration_info, expected_type=type_hints["configuration_info"])
            check_type(argname="argument ebs_storage_info", value=ebs_storage_info, expected_type=type_hints["ebs_storage_info"])
            check_type(argname="argument encryption_in_transit", value=encryption_in_transit, expected_type=type_hints["encryption_in_transit"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
            check_type(argname="argument number_of_broker_nodes", value=number_of_broker_nodes, expected_type=type_hints["number_of_broker_nodes"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument storage_mode", value=storage_mode, expected_type=type_hints["storage_mode"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "kafka_version": kafka_version,
            "vpc": vpc,
        }
        if client_authentication is not None:
            self._values["client_authentication"] = client_authentication
        if configuration_info is not None:
            self._values["configuration_info"] = configuration_info
        if ebs_storage_info is not None:
            self._values["ebs_storage_info"] = ebs_storage_info
        if encryption_in_transit is not None:
            self._values["encryption_in_transit"] = encryption_in_transit
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if logging is not None:
            self._values["logging"] = logging
        if monitoring is not None:
            self._values["monitoring"] = monitoring
        if number_of_broker_nodes is not None:
            self._values["number_of_broker_nodes"] = number_of_broker_nodes
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_mode is not None:
            self._values["storage_mode"] = storage_mode
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''(experimental) The physical name of the cluster.

        :stability: experimental
        '''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kafka_version(self) -> "KafkaVersion":
        '''(experimental) The version of Apache Kafka.

        :stability: experimental
        '''
        result = self._values.get("kafka_version")
        assert result is not None, "Required property 'kafka_version' is missing"
        return typing.cast("KafkaVersion", result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) Defines the virtual networking environment for this cluster.

        Must have at least 2 subnets in two different AZs.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def client_authentication(self) -> typing.Optional[ClientAuthentication]:
        '''(experimental) Configuration properties for client authentication.

        MSK supports using private TLS certificates or SASL/SCRAM to authenticate the identity of clients.

        :default: - disabled

        :stability: experimental
        '''
        result = self._values.get("client_authentication")
        return typing.cast(typing.Optional[ClientAuthentication], result)

    @builtins.property
    def configuration_info(self) -> typing.Optional[ClusterConfigurationInfo]:
        '''(experimental) The Amazon MSK configuration to use for the cluster.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("configuration_info")
        return typing.cast(typing.Optional[ClusterConfigurationInfo], result)

    @builtins.property
    def ebs_storage_info(self) -> typing.Optional["EbsStorageInfo"]:
        '''(experimental) Information about storage volumes attached to MSK broker nodes.

        :default: - 1000 GiB EBS volume

        :stability: experimental
        '''
        result = self._values.get("ebs_storage_info")
        return typing.cast(typing.Optional["EbsStorageInfo"], result)

    @builtins.property
    def encryption_in_transit(self) -> typing.Optional["EncryptionInTransitConfig"]:
        '''(experimental) Config details for encryption in transit.

        :default: - enabled

        :stability: experimental
        '''
        result = self._values.get("encryption_in_transit")
        return typing.cast(typing.Optional["EncryptionInTransitConfig"], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The EC2 instance type that you want Amazon MSK to use when it creates your brokers.

        :default: kafka.m5.large

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/msk-create-cluster.html#broker-instance-types
        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def logging(self) -> typing.Optional[BrokerLogging]:
        '''(experimental) Configure your MSK cluster to send broker logs to different destination types.

        :default: - disabled

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[BrokerLogging], result)

    @builtins.property
    def monitoring(self) -> typing.Optional["MonitoringConfiguration"]:
        '''(experimental) Cluster monitoring configuration.

        :default: - DEFAULT monitoring level

        :stability: experimental
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["MonitoringConfiguration"], result)

    @builtins.property
    def number_of_broker_nodes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of Apache Kafka brokers deployed in each Availability Zone.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("number_of_broker_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(experimental) What to do when this resource is deleted from a stack.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The AWS security groups to associate with the elastic network interfaces in order to specify who can connect to and communicate with the Amazon MSK cluster.

        :default: - create new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def storage_mode(self) -> typing.Optional["StorageMode"]:
        '''(experimental) This controls storage mode for supported storage tiers.

        :default: - StorageMode.LOCAL

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/msk-tiered-storage.html
        :stability: experimental
        '''
        result = self._values.get("storage_mode")
        return typing.cast(typing.Optional["StorageMode"], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Where to place the nodes within the VPC.

        Amazon MSK distributes the broker nodes evenly across the subnets that you specify.
        The subnets that you specify must be in distinct Availability Zones.
        Client subnets can't be in Availability Zone us-east-1e.

        :default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.EbsStorageInfo",
    jsii_struct_bases=[],
    name_mapping={"encryption_key": "encryptionKey", "volume_size": "volumeSize"},
)
class EbsStorageInfo:
    def __init__(
        self,
        *,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef] = None,
        volume_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) EBS volume information.

        :param encryption_key: (experimental) The AWS KMS key for encrypting data at rest. Default: Uses AWS managed CMK (aws/kafka)
        :param volume_size: (experimental) The size in GiB of the EBS volume for the data drive on each broker node. Default: 1000

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_msk_alpha as msk_alpha
            from aws_cdk import aws_kms as kms
            
            # key_ref: kms.IKeyRef
            
            ebs_storage_info = msk_alpha.EbsStorageInfo(
                encryption_key=key_ref,
                volume_size=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f71898e3644c01cacd375914aebc2f51bc973e16dca3550d856073a05c90ee)
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if volume_size is not None:
            self._values["volume_size"] = volume_size

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef]:
        '''(experimental) The AWS KMS key for encrypting data at rest.

        :default: Uses AWS managed CMK (aws/kafka)

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size in GiB of the EBS volume for the data drive on each broker node.

        :default: 1000

        :stability: experimental
        '''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EbsStorageInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.EncryptionInTransitConfig",
    jsii_struct_bases=[],
    name_mapping={
        "client_broker": "clientBroker",
        "enable_in_cluster": "enableInCluster",
    },
)
class EncryptionInTransitConfig:
    def __init__(
        self,
        *,
        client_broker: typing.Optional[ClientBrokerEncryption] = None,
        enable_in_cluster: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The settings for encrypting data in transit.

        :param client_broker: (experimental) Indicates the encryption setting for data in transit between clients and brokers. Default: - TLS
        :param enable_in_cluster: (experimental) Indicates that data communication among the broker nodes of the cluster is encrypted. Default: true

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/msk-encryption.html#msk-encryption-in-transit
        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_acmpca as acmpca
            
            # vpc: ec2.Vpc
            
            cluster = msk.Cluster(self, "Cluster",
                cluster_name="myCluster",
                kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
                vpc=vpc,
                encryption_in_transit=msk.EncryptionInTransitConfig(
                    client_broker=msk.ClientBrokerEncryption.TLS
                ),
                client_authentication=msk.ClientAuthentication.tls(
                    certificate_authorities=[
                        acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", "arn:aws:acm-pca:us-west-2:1234567890:certificate-authority/11111111-1111-1111-1111-111111111111")
                    ]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b66a42c0d765a1bd551981cf4b9d5840e1974336776a8da3877d190634cf50)
            check_type(argname="argument client_broker", value=client_broker, expected_type=type_hints["client_broker"])
            check_type(argname="argument enable_in_cluster", value=enable_in_cluster, expected_type=type_hints["enable_in_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_broker is not None:
            self._values["client_broker"] = client_broker
        if enable_in_cluster is not None:
            self._values["enable_in_cluster"] = enable_in_cluster

    @builtins.property
    def client_broker(self) -> typing.Optional[ClientBrokerEncryption]:
        '''(experimental) Indicates the encryption setting for data in transit between clients and brokers.

        :default: - TLS

        :stability: experimental
        '''
        result = self._values.get("client_broker")
        return typing.cast(typing.Optional[ClientBrokerEncryption], result)

    @builtins.property
    def enable_in_cluster(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates that data communication among the broker nodes of the cluster is encrypted.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enable_in_cluster")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptionInTransitConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-msk-alpha.ICluster")
class ICluster(
    _aws_cdk_ceddda9d.IResource,
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    typing_extensions.Protocol,
):
    '''(experimental) Represents a MSK Cluster.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        '''(experimental) The ARN of cluster.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        '''(experimental) The physical name of the cluster.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IClusterProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
):
    '''(experimental) Represents a MSK Cluster.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-msk-alpha.ICluster"

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        '''(experimental) The ARN of cluster.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterArn"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        '''(experimental) The physical name of the cluster.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICluster).__jsii_proxy_class__ = lambda : _IClusterProxy


class KafkaVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-msk-alpha.KafkaVersion",
):
    '''(experimental) Kafka cluster version.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # vpc: ec2.Vpc
        
        cluster = msk.Cluster(self, "cluster",
            cluster_name="myCluster",
            kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
            vpc=vpc,
            encryption_in_transit=msk.EncryptionInTransitConfig(
                client_broker=msk.ClientBrokerEncryption.TLS
            ),
            client_authentication=msk.ClientAuthentication.sasl(
                scram=True
            )
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        version: builtins.str,
        *,
        tiered_storage: typing.Optional[builtins.bool] = None,
    ) -> "KafkaVersion":
        '''(experimental) Custom cluster version.

        :param version: custom version number.
        :param tiered_storage: (experimental) Whether the Kafka version supports tiered storage mode. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e717a461a7dfd2af4c0ea436fee0dcfb2c9d05e9d05e0ff37e25c47c088b68ff)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        features = KafkaVersionFeatures(tiered_storage=tiered_storage)

        return typing.cast("KafkaVersion", jsii.sinvoke(cls, "of", [version, features]))

    @jsii.member(jsii_name="isTieredStorageCompatible")
    def is_tiered_storage_compatible(self) -> builtins.bool:
        '''(experimental) Checks if the cluster version supports tiered storage mode.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "isTieredStorageCompatible", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_1_1")
    def V1_1_1(cls) -> "KafkaVersion":
        '''(deprecated) **Deprecated by Amazon MSK. You can't create a Kafka cluster with a deprecated version.**.

        Kafka version 1.1.1

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V1_1_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_1_0")
    def V2_1_0(cls) -> "KafkaVersion":
        '''(deprecated) **Deprecated by Amazon MSK. You can't create a Kafka cluster with a deprecated version.**.

        Kafka version 2.1.0

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_2_1")
    def V2_2_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.2.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_2_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_3_1")
    def V2_3_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.3.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_3_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_4_1")
    def V2_4_1(cls) -> "KafkaVersion":
        '''(deprecated) **Deprecated by Amazon MSK. You can't create a Kafka cluster with a deprecated version.**.

        Kafka version 2.4.1

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_4_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_4_1_1")
    def V2_4_1_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.4.1.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_4_1_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_5_1")
    def V2_5_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.5.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_5_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_6_0")
    def V2_6_0(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.6.0.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_6_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_6_1")
    def V2_6_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.6.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_6_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_6_2")
    def V2_6_2(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.6.2.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_6_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_6_3")
    def V2_6_3(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.6.3.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_6_3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_7_0")
    def V2_7_0(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.7.0.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_7_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_7_1")
    def V2_7_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.7.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_7_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_7_2")
    def V2_7_2(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.7.2.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_7_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_8_0")
    def V2_8_0(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.8.0.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_8_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_8_1")
    def V2_8_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 2.8.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_8_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_8_2_TIERED")
    def V2_8_2_TIERED(cls) -> "KafkaVersion":
        '''(deprecated) AWS MSK Kafka version 2.8.2.tiered.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V2_8_2_TIERED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_1_1")
    def V3_1_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 3.1.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_1_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_2_0")
    def V3_2_0(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 3.2.0.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_2_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_3_1")
    def V3_3_1(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 3.3.1.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_3_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_3_2")
    def V3_3_2(cls) -> "KafkaVersion":
        '''(deprecated) Kafka version 3.3.2.

        :deprecated: use the latest runtime instead

        :stability: deprecated
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_3_2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_4_0")
    def V3_4_0(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.4.0.

        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_4_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_5_1")
    def V3_5_1(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.5.1.

        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_5_1"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_6_0")
    def V3_6_0(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.6.0.

        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_6_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_7_X")
    def V3_7_X(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.7.x with ZooKeeper metadata mode support.

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/metadata-management.html#msk-get-connection-string
        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_7_X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_7_X_KRAFT")
    def V3_7_X_KRAFT(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.7.x with KRaft (Apache Kafka Raft) metadata mode support.

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/metadata-management.html#kraft-intro
        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_7_X_KRAFT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_8_X")
    def V3_8_X(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.8.x with ZooKeeper metadata mode support.

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/metadata-management.html#msk-get-connection-string
        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_8_X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_8_X_KRAFT")
    def V3_8_X_KRAFT(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.8.x with KRaft (Apache Kafka Raft) metadata mode support.

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/metadata-management.html#kraft-intro
        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_8_X_KRAFT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_9_X")
    def V3_9_X(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.9.x with ZooKeeper metadata mode support.

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/metadata-management.html#msk-get-connection-string
        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_9_X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_9_X_KRAFT")
    def V3_9_X_KRAFT(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 3.9.x with KRaft (Apache Kafka Raft) metadata mode support.

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/metadata-management.html#kraft-intro
        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V3_9_X_KRAFT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V4_0_X_KRAFT")
    def V4_0_X_KRAFT(cls) -> "KafkaVersion":
        '''(experimental) Kafka version 4.0.x with KRaft (Apache Kafka Raft) metadata mode support.

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/metadata-management.html#kraft-intro
        :stability: experimental
        '''
        return typing.cast("KafkaVersion", jsii.sget(cls, "V4_0_X_KRAFT"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) cluster version number.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="features")
    def features(self) -> typing.Optional["KafkaVersionFeatures"]:
        '''(experimental) features for the cluster version.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["KafkaVersionFeatures"], jsii.get(self, "features"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.KafkaVersionFeatures",
    jsii_struct_bases=[],
    name_mapping={"tiered_storage": "tieredStorage"},
)
class KafkaVersionFeatures:
    def __init__(
        self,
        *,
        tiered_storage: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Available features for a given Kafka version.

        :param tiered_storage: (experimental) Whether the Kafka version supports tiered storage mode. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_msk_alpha as msk_alpha
            
            kafka_version_features = msk_alpha.KafkaVersionFeatures(
                tiered_storage=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f212f8dee8918151007b4ec07ef2f051ac574a03eb7230a5d494fdbd5c44105)
            check_type(argname="argument tiered_storage", value=tiered_storage, expected_type=type_hints["tiered_storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tiered_storage is not None:
            self._values["tiered_storage"] = tiered_storage

    @builtins.property
    def tiered_storage(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the Kafka version supports tiered storage mode.

        :default: false

        :see: https://docs.aws.amazon.com/msk/latest/developerguide/msk-tiered-storage.html#msk-tiered-storage-requirements
        :stability: experimental
        '''
        result = self._values.get("tiered_storage")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KafkaVersionFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.MonitoringConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_monitoring_level": "clusterMonitoringLevel",
        "enable_prometheus_jmx_exporter": "enablePrometheusJmxExporter",
        "enable_prometheus_node_exporter": "enablePrometheusNodeExporter",
    },
)
class MonitoringConfiguration:
    def __init__(
        self,
        *,
        cluster_monitoring_level: typing.Optional[ClusterMonitoringLevel] = None,
        enable_prometheus_jmx_exporter: typing.Optional[builtins.bool] = None,
        enable_prometheus_node_exporter: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Monitoring Configuration.

        :param cluster_monitoring_level: (experimental) Specifies the level of monitoring for the MSK cluster. Default: DEFAULT
        :param enable_prometheus_jmx_exporter: (experimental) Indicates whether you want to enable or disable the JMX Exporter. Default: false
        :param enable_prometheus_node_exporter: (experimental) Indicates whether you want to enable or disable the Prometheus Node Exporter. You can use the Prometheus Node Exporter to get CPU and disk metrics for the broker nodes. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_msk_alpha as msk_alpha
            
            monitoring_configuration = msk_alpha.MonitoringConfiguration(
                cluster_monitoring_level=msk_alpha.ClusterMonitoringLevel.DEFAULT,
                enable_prometheus_jmx_exporter=False,
                enable_prometheus_node_exporter=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af85a63aa3f07c68569eb1f6e9732a882ddeb2b7738ae8b80717edf2c96ef123)
            check_type(argname="argument cluster_monitoring_level", value=cluster_monitoring_level, expected_type=type_hints["cluster_monitoring_level"])
            check_type(argname="argument enable_prometheus_jmx_exporter", value=enable_prometheus_jmx_exporter, expected_type=type_hints["enable_prometheus_jmx_exporter"])
            check_type(argname="argument enable_prometheus_node_exporter", value=enable_prometheus_node_exporter, expected_type=type_hints["enable_prometheus_node_exporter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_monitoring_level is not None:
            self._values["cluster_monitoring_level"] = cluster_monitoring_level
        if enable_prometheus_jmx_exporter is not None:
            self._values["enable_prometheus_jmx_exporter"] = enable_prometheus_jmx_exporter
        if enable_prometheus_node_exporter is not None:
            self._values["enable_prometheus_node_exporter"] = enable_prometheus_node_exporter

    @builtins.property
    def cluster_monitoring_level(self) -> typing.Optional[ClusterMonitoringLevel]:
        '''(experimental) Specifies the level of monitoring for the MSK cluster.

        :default: DEFAULT

        :stability: experimental
        '''
        result = self._values.get("cluster_monitoring_level")
        return typing.cast(typing.Optional[ClusterMonitoringLevel], result)

    @builtins.property
    def enable_prometheus_jmx_exporter(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether you want to enable or disable the JMX Exporter.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_prometheus_jmx_exporter")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_prometheus_node_exporter(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether you want to enable or disable the Prometheus Node Exporter.

        You can use the Prometheus Node Exporter to get CPU and disk metrics for the broker nodes.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_prometheus_node_exporter")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitoringConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.S3LoggingConfiguration",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "prefix": "prefix"},
)
class S3LoggingConfiguration:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Details of the Amazon S3 destination for broker logs.

        :param bucket: (experimental) The S3 bucket that is the destination for broker logs.
        :param prefix: (experimental) The S3 prefix that is the destination for broker logs. Default: - no prefix

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            # bucket: s3.IBucket
            
            cluster = msk.Cluster(self, "cluster",
                cluster_name="myCluster",
                kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
                vpc=vpc,
                logging=msk.BrokerLogging(
                    s3=msk.S3LoggingConfiguration(
                        bucket=bucket
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51fbd5191484562bb80360937520b2fcdc78a672c23d4c600aff0554ad23aa62)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The S3 bucket that is the destination for broker logs.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 prefix that is the destination for broker logs.

        :default: - no prefix

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3LoggingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.SaslAuthProps",
    jsii_struct_bases=[],
    name_mapping={"iam": "iam", "key": "key", "scram": "scram"},
)
class SaslAuthProps:
    def __init__(
        self,
        *,
        iam: typing.Optional[builtins.bool] = None,
        key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef] = None,
        scram: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) SASL authentication properties.

        :param iam: (experimental) Enable IAM access control. Default: false
        :param key: (experimental) KMS Key to encrypt SASL/SCRAM secrets. You must use a customer master key (CMK) when creating users in secrets manager. You cannot use a Secret with Amazon MSK that uses the default Secrets Manager encryption key. Default: - CMK will be created with alias msk/{clusterName}/sasl/scram
        :param scram: (experimental) Enable SASL/SCRAM authentication. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            cluster = msk.Cluster(self, "cluster",
                cluster_name="myCluster",
                kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
                vpc=vpc,
                encryption_in_transit=msk.EncryptionInTransitConfig(
                    client_broker=msk.ClientBrokerEncryption.TLS
                ),
                client_authentication=msk.ClientAuthentication.sasl(
                    scram=True
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f186e6270f30759471573a6fdea8241e1a52ec3ddb6f61ac669172717e5a8ea6)
            check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument scram", value=scram, expected_type=type_hints["scram"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iam is not None:
            self._values["iam"] = iam
        if key is not None:
            self._values["key"] = key
        if scram is not None:
            self._values["scram"] = scram

    @builtins.property
    def iam(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable IAM access control.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("iam")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef]:
        '''(experimental) KMS Key to encrypt SASL/SCRAM secrets.

        You must use a customer master key (CMK) when creating users in secrets manager.
        You cannot use a Secret with Amazon MSK that uses the default Secrets Manager encryption key.

        :default: - CMK will be created with alias msk/{clusterName}/sasl/scram

        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef], result)

    @builtins.property
    def scram(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable SASL/SCRAM authentication.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("scram")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SaslAuthProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.ServerlessClusterProps",
    jsii_struct_bases=[],
    name_mapping={"vpc_configs": "vpcConfigs", "cluster_name": "clusterName"},
)
class ServerlessClusterProps:
    def __init__(
        self,
        *,
        vpc_configs: typing.Sequence[typing.Union["VpcConfig", typing.Dict[builtins.str, typing.Any]]],
        cluster_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a MSK Serverless Cluster.

        :param vpc_configs: (experimental) The configuration of the Amazon VPCs for the cluster. You can specify up to 5 VPC configurations.
        :param cluster_name: (experimental) The physical name of the cluster. Default: - auto generate

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            
            serverless_cluster = msk.ServerlessCluster(self, "ServerlessCluster",
                cluster_name="MyServerlessCluster",
                vpc_configs=[msk.VpcConfig(vpc=vpc)
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c03e39f4115d77352d0f522ecace92f4230384648b83e2ef9753753a1e46fb90)
            check_type(argname="argument vpc_configs", value=vpc_configs, expected_type=type_hints["vpc_configs"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_configs": vpc_configs,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name

    @builtins.property
    def vpc_configs(self) -> typing.List["VpcConfig"]:
        '''(experimental) The configuration of the Amazon VPCs for the cluster.

        You can specify up to 5 VPC configurations.

        :stability: experimental
        '''
        result = self._values.get("vpc_configs")
        assert result is not None, "Required property 'vpc_configs' is missing"
        return typing.cast(typing.List["VpcConfig"], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical name of the cluster.

        :default: - auto generate

        :stability: experimental
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-msk-alpha.StorageMode")
class StorageMode(enum.Enum):
    '''(experimental) The storage mode for the cluster brokers.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # vpc: ec2.Vpc
        # bucket: s3.IBucket
        
        
        cluster = msk.Cluster(self, "cluster",
            cluster_name="myCluster",
            kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
            vpc=vpc,
            storage_mode=msk.StorageMode.TIERED
        )
    '''

    LOCAL = "LOCAL"
    '''(experimental) Local storage mode utilizes network attached EBS storage.

    :stability: experimental
    '''
    TIERED = "TIERED"
    '''(experimental) Tiered storage mode utilizes EBS storage and Tiered storage.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.TlsAuthProps",
    jsii_struct_bases=[],
    name_mapping={"certificate_authorities": "certificateAuthorities"},
)
class TlsAuthProps:
    def __init__(
        self,
        *,
        certificate_authorities: typing.Optional[typing.Sequence[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]] = None,
    ) -> None:
        '''(experimental) TLS authentication properties.

        :param certificate_authorities: (experimental) List of ACM Certificate Authorities to enable TLS authentication. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_acmpca as acmpca
            
            # vpc: ec2.Vpc
            
            cluster = msk.Cluster(self, "Cluster",
                cluster_name="myCluster",
                kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
                vpc=vpc,
                encryption_in_transit=msk.EncryptionInTransitConfig(
                    client_broker=msk.ClientBrokerEncryption.TLS
                ),
                client_authentication=msk.ClientAuthentication.tls(
                    certificate_authorities=[
                        acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", "arn:aws:acm-pca:us-west-2:1234567890:certificate-authority/11111111-1111-1111-1111-111111111111")
                    ]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e699112e7fd831ecbdb6721274774f9c6ca4c3a0a7bee752f311fcbdf1e3eb25)
            check_type(argname="argument certificate_authorities", value=certificate_authorities, expected_type=type_hints["certificate_authorities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_authorities is not None:
            self._values["certificate_authorities"] = certificate_authorities

    @builtins.property
    def certificate_authorities(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]]:
        '''(experimental) List of ACM Certificate Authorities to enable TLS authentication.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("certificate_authorities")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TlsAuthProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.VpcConfig",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "security_groups": "securityGroups",
        "vpc_subnets": "vpcSubnets",
    },
)
class VpcConfig:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The configuration of the Amazon VPCs for the cluster.

        :param vpc: (experimental) Defines the virtual networking environment for this cluster. Must have at least 2 subnets in two different AZs.
        :param security_groups: (experimental) The security groups associated with the cluster. You can specify up to 5 security groups. Default: - create new security group
        :param vpc_subnets: (experimental) The subnets associated with the cluster. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_msk_alpha as msk_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # vpc: ec2.Vpc
            
            vpc_config = msk_alpha.VpcConfig(
                vpc=vpc,
            
                # the properties below are optional
                security_groups=[security_group],
                vpc_subnets=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                )
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91169702f15def3f5a9b5f148b0b7a24188145c514a0bffb1ab1ceaad4e2a8f)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) Defines the virtual networking environment for this cluster.

        Must have at least 2 subnets in two different AZs.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The security groups associated with the cluster.

        You can specify up to 5 security groups.

        :default: - create new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The subnets associated with the cluster.

        :default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICluster)
class ClusterBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-msk-alpha.ClusterBase",
):
    '''(experimental) A new or imported MSK Cluster.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a14559760ddb0ea87ad0006d42a695b4e14406b32f4cbbde9cea07b2dbd8907)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    @abc.abstractmethod
    def cluster_arn(self) -> builtins.str:
        '''(experimental) The ARN of cluster.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    @abc.abstractmethod
    def cluster_name(self) -> builtins.str:
        '''(experimental) The physical name of the cluster.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) Manages connections for the cluster.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))


class _ClusterBaseProxy(
    ClusterBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        '''(experimental) The ARN of cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterArn"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        '''(experimental) The physical name of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ClusterBase).__jsii_proxy_class__ = lambda : _ClusterBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-msk-alpha.SaslTlsAuthProps",
    jsii_struct_bases=[SaslAuthProps, TlsAuthProps],
    name_mapping={
        "iam": "iam",
        "key": "key",
        "scram": "scram",
        "certificate_authorities": "certificateAuthorities",
    },
)
class SaslTlsAuthProps(SaslAuthProps, TlsAuthProps):
    def __init__(
        self,
        *,
        iam: typing.Optional[builtins.bool] = None,
        key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef] = None,
        scram: typing.Optional[builtins.bool] = None,
        certificate_authorities: typing.Optional[typing.Sequence[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]] = None,
    ) -> None:
        '''(experimental) SASL + TLS authentication properties.

        :param iam: (experimental) Enable IAM access control. Default: false
        :param key: (experimental) KMS Key to encrypt SASL/SCRAM secrets. You must use a customer master key (CMK) when creating users in secrets manager. You cannot use a Secret with Amazon MSK that uses the default Secrets Manager encryption key. Default: - CMK will be created with alias msk/{clusterName}/sasl/scram
        :param scram: (experimental) Enable SASL/SCRAM authentication. Default: false
        :param certificate_authorities: (experimental) List of ACM Certificate Authorities to enable TLS authentication. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_acmpca as acmpca
            
            # vpc: ec2.Vpc
            
            cluster = msk.Cluster(self, "Cluster",
                cluster_name="myCluster",
                kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
                vpc=vpc,
                encryption_in_transit=msk.EncryptionInTransitConfig(
                    client_broker=msk.ClientBrokerEncryption.TLS
                ),
                client_authentication=msk.ClientAuthentication.sasl_tls(
                    iam=True,
                    certificate_authorities=[
                        acmpca.CertificateAuthority.from_certificate_authority_arn(self, "CertificateAuthority", "arn:aws:acm-pca:us-west-2:1234567890:certificate-authority/11111111-1111-1111-1111-111111111111")
                    ]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26cb615593ec2787153e2c44f8002c0d2c4cc00110f82aa3f2d4f8d6666b9b1)
            check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument scram", value=scram, expected_type=type_hints["scram"])
            check_type(argname="argument certificate_authorities", value=certificate_authorities, expected_type=type_hints["certificate_authorities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iam is not None:
            self._values["iam"] = iam
        if key is not None:
            self._values["key"] = key
        if scram is not None:
            self._values["scram"] = scram
        if certificate_authorities is not None:
            self._values["certificate_authorities"] = certificate_authorities

    @builtins.property
    def iam(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable IAM access control.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("iam")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef]:
        '''(experimental) KMS Key to encrypt SASL/SCRAM secrets.

        You must use a customer master key (CMK) when creating users in secrets manager.
        You cannot use a Secret with Amazon MSK that uses the default Secrets Manager encryption key.

        :default: - CMK will be created with alias msk/{clusterName}/sasl/scram

        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef], result)

    @builtins.property
    def scram(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable SASL/SCRAM authentication.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("scram")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def certificate_authorities(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]]:
        '''(experimental) List of ACM Certificate Authorities to enable TLS authentication.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("certificate_authorities")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SaslTlsAuthProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServerlessCluster(
    ClusterBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-msk-alpha.ServerlessCluster",
):
    '''(experimental) Create a MSK Serverless Cluster.

    :stability: experimental
    :resource: AWS::MSK::ServerlessCluster
    :exampleMetadata: infused

    Example::

        # vpc: ec2.Vpc
        
        
        serverless_cluster = msk.ServerlessCluster(self, "ServerlessCluster",
            cluster_name="MyServerlessCluster",
            vpc_configs=[msk.VpcConfig(vpc=vpc)
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc_configs: typing.Sequence[typing.Union[VpcConfig, typing.Dict[builtins.str, typing.Any]]],
        cluster_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc_configs: (experimental) The configuration of the Amazon VPCs for the cluster. You can specify up to 5 VPC configurations.
        :param cluster_name: (experimental) The physical name of the cluster. Default: - auto generate

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6597080dc18e00dd83f34a571e43041faf1d4d8ea8ca939a0bb73f6e170e8c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServerlessClusterProps(
            vpc_configs=vpc_configs, cluster_name=cluster_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterArn")
    @builtins.classmethod
    def from_cluster_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        cluster_arn: builtins.str,
    ) -> ICluster:
        '''(experimental) Reference an existing cluster, defined outside of the CDK code, by name.

        :param scope: -
        :param id: -
        :param cluster_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacff172b1809812bce72e5cf8fec5ce71e24e193325c2c1ed4bb2e117eb6f12)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
        return typing.cast(ICluster, jsii.sinvoke(cls, "fromClusterArn", [scope, id, cluster_arn]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        '''(experimental) The ARN of cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterArn"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        '''(experimental) The physical name of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))


class Cluster(
    ClusterBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-msk-alpha.Cluster",
):
    '''(experimental) Create a MSK Cluster.

    :stability: experimental
    :resource: AWS::MSK::Cluster
    :exampleMetadata: infused

    Example::

        # vpc: ec2.Vpc
        
        cluster = msk.Cluster(self, "cluster",
            cluster_name="myCluster",
            kafka_version=msk.KafkaVersion.V4_0_X_KRAFT,
            vpc=vpc,
            encryption_in_transit=msk.EncryptionInTransitConfig(
                client_broker=msk.ClientBrokerEncryption.TLS
            ),
            client_authentication=msk.ClientAuthentication.sasl(
                scram=True
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster_name: builtins.str,
        kafka_version: KafkaVersion,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        client_authentication: typing.Optional[ClientAuthentication] = None,
        configuration_info: typing.Optional[typing.Union[ClusterConfigurationInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        ebs_storage_info: typing.Optional[typing.Union[EbsStorageInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_in_transit: typing.Optional[typing.Union[EncryptionInTransitConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        logging: typing.Optional[typing.Union[BrokerLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring: typing.Optional[typing.Union[MonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        number_of_broker_nodes: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        storage_mode: typing.Optional[StorageMode] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster_name: (experimental) The physical name of the cluster.
        :param kafka_version: (experimental) The version of Apache Kafka.
        :param vpc: (experimental) Defines the virtual networking environment for this cluster. Must have at least 2 subnets in two different AZs.
        :param client_authentication: (experimental) Configuration properties for client authentication. MSK supports using private TLS certificates or SASL/SCRAM to authenticate the identity of clients. Default: - disabled
        :param configuration_info: (experimental) The Amazon MSK configuration to use for the cluster. Default: - none
        :param ebs_storage_info: (experimental) Information about storage volumes attached to MSK broker nodes. Default: - 1000 GiB EBS volume
        :param encryption_in_transit: (experimental) Config details for encryption in transit. Default: - enabled
        :param instance_type: (experimental) The EC2 instance type that you want Amazon MSK to use when it creates your brokers. Default: kafka.m5.large
        :param logging: (experimental) Configure your MSK cluster to send broker logs to different destination types. Default: - disabled
        :param monitoring: (experimental) Cluster monitoring configuration. Default: - DEFAULT monitoring level
        :param number_of_broker_nodes: (experimental) Number of Apache Kafka brokers deployed in each Availability Zone. Default: 1
        :param removal_policy: (experimental) What to do when this resource is deleted from a stack. Default: RemovalPolicy.RETAIN
        :param security_groups: (experimental) The AWS security groups to associate with the elastic network interfaces in order to specify who can connect to and communicate with the Amazon MSK cluster. Default: - create new security group
        :param storage_mode: (experimental) This controls storage mode for supported storage tiers. Default: - StorageMode.LOCAL
        :param vpc_subnets: (experimental) Where to place the nodes within the VPC. Amazon MSK distributes the broker nodes evenly across the subnets that you specify. The subnets that you specify must be in distinct Availability Zones. Client subnets can't be in Availability Zone us-east-1e. Default: - the Vpc default strategy if not specified.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915d701802577130bfeeac000a90d2329d756ddabd799173074e0b31599dc1da)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ClusterProps(
            cluster_name=cluster_name,
            kafka_version=kafka_version,
            vpc=vpc,
            client_authentication=client_authentication,
            configuration_info=configuration_info,
            ebs_storage_info=ebs_storage_info,
            encryption_in_transit=encryption_in_transit,
            instance_type=instance_type,
            logging=logging,
            monitoring=monitoring,
            number_of_broker_nodes=number_of_broker_nodes,
            removal_policy=removal_policy,
            security_groups=security_groups,
            storage_mode=storage_mode,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterArn")
    @builtins.classmethod
    def from_cluster_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        cluster_arn: builtins.str,
    ) -> ICluster:
        '''(experimental) Reference an existing cluster, defined outside of the CDK code, by name.

        :param scope: -
        :param id: -
        :param cluster_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fc7f5a603e4a4a7570b1cb9dd88e7dc03e0e3a033edb8431d1c192ea70e3d31)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
        return typing.cast(ICluster, jsii.sinvoke(cls, "fromClusterArn", [scope, id, cluster_arn]))

    @jsii.member(jsii_name="addUser")
    def add_user(self, *usernames: builtins.str) -> None:
        '''(experimental) A list of usersnames to register with the cluster.

        The password will automatically be generated using Secrets
        Manager and the { username, password } JSON object stored in Secrets Manager as ``AmazonMSK_username``.

        Must be using the SASL/SCRAM authentication mechanism.

        :param usernames: - username(s) to register with the cluster.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086a8d99e45ecd0f3befc0016a11c7cd032f40be57774b5485d2c4cf9efbda59)
            check_type(argname="argument usernames", value=usernames, expected_type=typing.Tuple[type_hints["usernames"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addUser", [*usernames]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapBrokers")
    def bootstrap_brokers(self) -> builtins.str:
        '''(experimental) Get the list of brokers that a client application can use to bootstrap.

        Uses a Custom Resource to make an API call to ``getBootstrapBrokers`` using the Javascript SDK

        :return: - A string containing one or more hostname:port pairs.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bootstrapBrokers"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapBrokersSaslIam")
    def bootstrap_brokers_sasl_iam(self) -> builtins.str:
        '''(experimental) Get the list of brokers that a SASL/IAM authenticated client application can use to bootstrap.

        Uses a Custom Resource to make an API call to ``getBootstrapBrokers`` using the Javascript SDK

        :return: - A string containing one or more DNS names (or IP) and TLS port pairs.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bootstrapBrokersSaslIam"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapBrokersSaslScram")
    def bootstrap_brokers_sasl_scram(self) -> builtins.str:
        '''(experimental) Get the list of brokers that a SASL/SCRAM authenticated client application can use to bootstrap.

        Uses a Custom Resource to make an API call to ``getBootstrapBrokers`` using the Javascript SDK

        :return: - A string containing one or more dns name (or IP) and SASL SCRAM port pairs.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bootstrapBrokersSaslScram"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapBrokersTls")
    def bootstrap_brokers_tls(self) -> builtins.str:
        '''(experimental) Get the list of brokers that a TLS authenticated client application can use to bootstrap.

        Uses a Custom Resource to make an API call to ``getBootstrapBrokers`` using the Javascript SDK

        :return: - A string containing one or more DNS names (or IP) and TLS port pairs.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bootstrapBrokersTls"))

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        '''(experimental) The ARN of cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterArn"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        '''(experimental) The physical name of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperConnectionString")
    def zookeeper_connection_string(self) -> builtins.str:
        '''(experimental) Get the ZooKeeper Connection string.

        Uses a Custom Resource to make an API call to ``describeCluster`` using the Javascript SDK

        :return: - The connection string to use to connect to the Apache ZooKeeper cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "zookeeperConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="zookeeperConnectionStringTls")
    def zookeeper_connection_string_tls(self) -> builtins.str:
        '''(experimental) Get the ZooKeeper Connection string for a TLS enabled cluster.

        Uses a Custom Resource to make an API call to ``describeCluster`` using the Javascript SDK

        :return: - The connection string to use to connect to zookeeper cluster on TLS port.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "zookeeperConnectionStringTls"))

    @builtins.property
    @jsii.member(jsii_name="saslScramAuthenticationKey")
    def sasl_scram_authentication_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) Key used to encrypt SASL/SCRAM users.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "saslScramAuthenticationKey"))


__all__ = [
    "BrokerLogging",
    "ClientAuthentication",
    "ClientBrokerEncryption",
    "Cluster",
    "ClusterBase",
    "ClusterConfigurationInfo",
    "ClusterMonitoringLevel",
    "ClusterProps",
    "EbsStorageInfo",
    "EncryptionInTransitConfig",
    "ICluster",
    "KafkaVersion",
    "KafkaVersionFeatures",
    "MonitoringConfiguration",
    "S3LoggingConfiguration",
    "SaslAuthProps",
    "SaslTlsAuthProps",
    "ServerlessCluster",
    "ServerlessClusterProps",
    "StorageMode",
    "TlsAuthProps",
    "VpcConfig",
]

publication.publish()

def _typecheckingstub__9ba586b7db9e5dd092a5b8f9676408abd0e8865e17a5980b7acb9ac4b970f225(
    *,
    cloudwatch_log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    firehose_delivery_stream_name: typing.Optional[builtins.str] = None,
    s3: typing.Optional[typing.Union[S3LoggingConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c843d4de610e7657dc25ae7cbdd2c8bba8b60a980c8877eba757e6e63c7ebd(
    *,
    arn: builtins.str,
    revision: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acb1d0e21413d16efb1d11f4a29cc860b92ac278e0b0187d75e3eb1f71b1492(
    *,
    cluster_name: builtins.str,
    kafka_version: KafkaVersion,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    client_authentication: typing.Optional[ClientAuthentication] = None,
    configuration_info: typing.Optional[typing.Union[ClusterConfigurationInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_storage_info: typing.Optional[typing.Union[EbsStorageInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_in_transit: typing.Optional[typing.Union[EncryptionInTransitConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    logging: typing.Optional[typing.Union[BrokerLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring: typing.Optional[typing.Union[MonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    number_of_broker_nodes: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    storage_mode: typing.Optional[StorageMode] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f71898e3644c01cacd375914aebc2f51bc973e16dca3550d856073a05c90ee(
    *,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef] = None,
    volume_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b66a42c0d765a1bd551981cf4b9d5840e1974336776a8da3877d190634cf50(
    *,
    client_broker: typing.Optional[ClientBrokerEncryption] = None,
    enable_in_cluster: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e717a461a7dfd2af4c0ea436fee0dcfb2c9d05e9d05e0ff37e25c47c088b68ff(
    version: builtins.str,
    *,
    tiered_storage: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f212f8dee8918151007b4ec07ef2f051ac574a03eb7230a5d494fdbd5c44105(
    *,
    tiered_storage: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af85a63aa3f07c68569eb1f6e9732a882ddeb2b7738ae8b80717edf2c96ef123(
    *,
    cluster_monitoring_level: typing.Optional[ClusterMonitoringLevel] = None,
    enable_prometheus_jmx_exporter: typing.Optional[builtins.bool] = None,
    enable_prometheus_node_exporter: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51fbd5191484562bb80360937520b2fcdc78a672c23d4c600aff0554ad23aa62(
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f186e6270f30759471573a6fdea8241e1a52ec3ddb6f61ac669172717e5a8ea6(
    *,
    iam: typing.Optional[builtins.bool] = None,
    key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef] = None,
    scram: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c03e39f4115d77352d0f522ecace92f4230384648b83e2ef9753753a1e46fb90(
    *,
    vpc_configs: typing.Sequence[typing.Union[VpcConfig, typing.Dict[builtins.str, typing.Any]]],
    cluster_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e699112e7fd831ecbdb6721274774f9c6ca4c3a0a7bee752f311fcbdf1e3eb25(
    *,
    certificate_authorities: typing.Optional[typing.Sequence[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91169702f15def3f5a9b5f148b0b7a24188145c514a0bffb1ab1ceaad4e2a8f(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a14559760ddb0ea87ad0006d42a695b4e14406b32f4cbbde9cea07b2dbd8907(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26cb615593ec2787153e2c44f8002c0d2c4cc00110f82aa3f2d4f8d6666b9b1(
    *,
    iam: typing.Optional[builtins.bool] = None,
    key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKeyRef] = None,
    scram: typing.Optional[builtins.bool] = None,
    certificate_authorities: typing.Optional[typing.Sequence[_aws_cdk_aws_acmpca_ceddda9d.ICertificateAuthority]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6597080dc18e00dd83f34a571e43041faf1d4d8ea8ca939a0bb73f6e170e8c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc_configs: typing.Sequence[typing.Union[VpcConfig, typing.Dict[builtins.str, typing.Any]]],
    cluster_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacff172b1809812bce72e5cf8fec5ce71e24e193325c2c1ed4bb2e117eb6f12(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    cluster_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915d701802577130bfeeac000a90d2329d756ddabd799173074e0b31599dc1da(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster_name: builtins.str,
    kafka_version: KafkaVersion,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    client_authentication: typing.Optional[ClientAuthentication] = None,
    configuration_info: typing.Optional[typing.Union[ClusterConfigurationInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_storage_info: typing.Optional[typing.Union[EbsStorageInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_in_transit: typing.Optional[typing.Union[EncryptionInTransitConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    logging: typing.Optional[typing.Union[BrokerLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring: typing.Optional[typing.Union[MonitoringConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    number_of_broker_nodes: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    storage_mode: typing.Optional[StorageMode] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc7f5a603e4a4a7570b1cb9dd88e7dc03e0e3a033edb8431d1c192ea70e3d31(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    cluster_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086a8d99e45ecd0f3befc0016a11c7cd032f40be57774b5485d2c4cf9efbda59(
    *usernames: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
