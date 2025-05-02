r'''
# `aws_msk_replicator`

Refer to the Terraform Registry for docs: [`aws_msk_replicator`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator).
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


class MskReplicator(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicator",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator aws_msk_replicator}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        kafka_cluster: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorKafkaCluster", typing.Dict[builtins.str, typing.Any]]]],
        replication_info_list: typing.Union["MskReplicatorReplicationInfoListStruct", typing.Dict[builtins.str, typing.Any]],
        replicator_name: builtins.str,
        service_execution_role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MskReplicatorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator aws_msk_replicator} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param kafka_cluster: kafka_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#kafka_cluster MskReplicator#kafka_cluster}
        :param replication_info_list: replication_info_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#replication_info_list MskReplicator#replication_info_list}
        :param replicator_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#replicator_name MskReplicator#replicator_name}.
        :param service_execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#service_execution_role_arn MskReplicator#service_execution_role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#description MskReplicator#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#id MskReplicator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#tags MskReplicator#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#tags_all MskReplicator#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#timeouts MskReplicator#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94bce509affa29908bc7cb438ce56e1b60dd60f41cd22289e0e544f5e2520765)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MskReplicatorConfig(
            kafka_cluster=kafka_cluster,
            replication_info_list=replication_info_list,
            replicator_name=replicator_name,
            service_execution_role_arn=service_execution_role_arn,
            description=description,
            id=id,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a MskReplicator resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MskReplicator to import.
        :param import_from_id: The id of the existing MskReplicator that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MskReplicator to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a94a16bbcd335e6f9a88fa8a0b0dc6ee88ca43283d855cfe71e80ea19c2f20b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putKafkaCluster")
    def put_kafka_cluster(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorKafkaCluster", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8984721c0196cf8c2553735e86f5aeb4c0f6947f2cb09067f0ef5d163370b2dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKafkaCluster", [value]))

    @jsii.member(jsii_name="putReplicationInfoList")
    def put_replication_info_list(
        self,
        *,
        consumer_group_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorReplicationInfoListConsumerGroupReplication", typing.Dict[builtins.str, typing.Any]]]],
        source_kafka_cluster_arn: builtins.str,
        target_compression_type: builtins.str,
        target_kafka_cluster_arn: builtins.str,
        topic_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorReplicationInfoListTopicReplication", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param consumer_group_replication: consumer_group_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#consumer_group_replication MskReplicator#consumer_group_replication}
        :param source_kafka_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#source_kafka_cluster_arn MskReplicator#source_kafka_cluster_arn}.
        :param target_compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#target_compression_type MskReplicator#target_compression_type}.
        :param target_kafka_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#target_kafka_cluster_arn MskReplicator#target_kafka_cluster_arn}.
        :param topic_replication: topic_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topic_replication MskReplicator#topic_replication}
        '''
        value = MskReplicatorReplicationInfoListStruct(
            consumer_group_replication=consumer_group_replication,
            source_kafka_cluster_arn=source_kafka_cluster_arn,
            target_compression_type=target_compression_type,
            target_kafka_cluster_arn=target_kafka_cluster_arn,
            topic_replication=topic_replication,
        )

        return typing.cast(None, jsii.invoke(self, "putReplicationInfoList", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#create MskReplicator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#delete MskReplicator#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#update MskReplicator#update}.
        '''
        value = MskReplicatorTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="currentVersion")
    def current_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentVersion"))

    @builtins.property
    @jsii.member(jsii_name="kafkaCluster")
    def kafka_cluster(self) -> "MskReplicatorKafkaClusterList":
        return typing.cast("MskReplicatorKafkaClusterList", jsii.get(self, "kafkaCluster"))

    @builtins.property
    @jsii.member(jsii_name="replicationInfoList")
    def replication_info_list(
        self,
    ) -> "MskReplicatorReplicationInfoListStructOutputReference":
        return typing.cast("MskReplicatorReplicationInfoListStructOutputReference", jsii.get(self, "replicationInfoList"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MskReplicatorTimeoutsOutputReference":
        return typing.cast("MskReplicatorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kafkaClusterInput")
    def kafka_cluster_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorKafkaCluster"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorKafkaCluster"]]], jsii.get(self, "kafkaClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationInfoListInput")
    def replication_info_list_input(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListStruct"]:
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListStruct"], jsii.get(self, "replicationInfoListInput"))

    @builtins.property
    @jsii.member(jsii_name="replicatorNameInput")
    def replicator_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicatorNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceExecutionRoleArnInput")
    def service_execution_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceExecutionRoleArnInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MskReplicatorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MskReplicatorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb8dfcf1f13ed278359c5f1c96ee48b7748131f3adeeb8a44e13333cc67d17e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979ca3777545d110a54572e412d4d222cb256907f4f4784ed73defacfd423760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicatorName")
    def replicator_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicatorName"))

    @replicator_name.setter
    def replicator_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a627e51c65666ef79d287eee28f1b46350783231267ba41c90af71ccfdbce21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicatorName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceExecutionRoleArn")
    def service_execution_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceExecutionRoleArn"))

    @service_execution_role_arn.setter
    def service_execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef3f63422c9fffb38a550fa6ba5213964de8e1fbbb839346639eda9c572db51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceExecutionRoleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae06f4314d9f73b7fd3eedd164f02db9f932598264c8f956ddb9a83055c1549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a780466809bc40852951c572b54707d350908095ca18955caeee3ae433f27837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "kafka_cluster": "kafkaCluster",
        "replication_info_list": "replicationInfoList",
        "replicator_name": "replicatorName",
        "service_execution_role_arn": "serviceExecutionRoleArn",
        "description": "description",
        "id": "id",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class MskReplicatorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        kafka_cluster: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorKafkaCluster", typing.Dict[builtins.str, typing.Any]]]],
        replication_info_list: typing.Union["MskReplicatorReplicationInfoListStruct", typing.Dict[builtins.str, typing.Any]],
        replicator_name: builtins.str,
        service_execution_role_arn: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MskReplicatorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param kafka_cluster: kafka_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#kafka_cluster MskReplicator#kafka_cluster}
        :param replication_info_list: replication_info_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#replication_info_list MskReplicator#replication_info_list}
        :param replicator_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#replicator_name MskReplicator#replicator_name}.
        :param service_execution_role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#service_execution_role_arn MskReplicator#service_execution_role_arn}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#description MskReplicator#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#id MskReplicator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#tags MskReplicator#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#tags_all MskReplicator#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#timeouts MskReplicator#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(replication_info_list, dict):
            replication_info_list = MskReplicatorReplicationInfoListStruct(**replication_info_list)
        if isinstance(timeouts, dict):
            timeouts = MskReplicatorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76f0d692bcc87e4a2f71e8f9c954fc554cb38322bcc29eeac3fc91fb5b6d7f7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument kafka_cluster", value=kafka_cluster, expected_type=type_hints["kafka_cluster"])
            check_type(argname="argument replication_info_list", value=replication_info_list, expected_type=type_hints["replication_info_list"])
            check_type(argname="argument replicator_name", value=replicator_name, expected_type=type_hints["replicator_name"])
            check_type(argname="argument service_execution_role_arn", value=service_execution_role_arn, expected_type=type_hints["service_execution_role_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kafka_cluster": kafka_cluster,
            "replication_info_list": replication_info_list,
            "replicator_name": replicator_name,
            "service_execution_role_arn": service_execution_role_arn,
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
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
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
    def kafka_cluster(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorKafkaCluster"]]:
        '''kafka_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#kafka_cluster MskReplicator#kafka_cluster}
        '''
        result = self._values.get("kafka_cluster")
        assert result is not None, "Required property 'kafka_cluster' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorKafkaCluster"]], result)

    @builtins.property
    def replication_info_list(self) -> "MskReplicatorReplicationInfoListStruct":
        '''replication_info_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#replication_info_list MskReplicator#replication_info_list}
        '''
        result = self._values.get("replication_info_list")
        assert result is not None, "Required property 'replication_info_list' is missing"
        return typing.cast("MskReplicatorReplicationInfoListStruct", result)

    @builtins.property
    def replicator_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#replicator_name MskReplicator#replicator_name}.'''
        result = self._values.get("replicator_name")
        assert result is not None, "Required property 'replicator_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_execution_role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#service_execution_role_arn MskReplicator#service_execution_role_arn}.'''
        result = self._values.get("service_execution_role_arn")
        assert result is not None, "Required property 'service_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#description MskReplicator#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#id MskReplicator#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#tags MskReplicator#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#tags_all MskReplicator#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MskReplicatorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#timeouts MskReplicator#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MskReplicatorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorKafkaCluster",
    jsii_struct_bases=[],
    name_mapping={"amazon_msk_cluster": "amazonMskCluster", "vpc_config": "vpcConfig"},
)
class MskReplicatorKafkaCluster:
    def __init__(
        self,
        *,
        amazon_msk_cluster: typing.Union["MskReplicatorKafkaClusterAmazonMskCluster", typing.Dict[builtins.str, typing.Any]],
        vpc_config: typing.Union["MskReplicatorKafkaClusterVpcConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param amazon_msk_cluster: amazon_msk_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#amazon_msk_cluster MskReplicator#amazon_msk_cluster}
        :param vpc_config: vpc_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#vpc_config MskReplicator#vpc_config}
        '''
        if isinstance(amazon_msk_cluster, dict):
            amazon_msk_cluster = MskReplicatorKafkaClusterAmazonMskCluster(**amazon_msk_cluster)
        if isinstance(vpc_config, dict):
            vpc_config = MskReplicatorKafkaClusterVpcConfig(**vpc_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28124b6b83502af775c3ef35e3b085677cd08935f335d654e2c53c5a73b1430e)
            check_type(argname="argument amazon_msk_cluster", value=amazon_msk_cluster, expected_type=type_hints["amazon_msk_cluster"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "amazon_msk_cluster": amazon_msk_cluster,
            "vpc_config": vpc_config,
        }

    @builtins.property
    def amazon_msk_cluster(self) -> "MskReplicatorKafkaClusterAmazonMskCluster":
        '''amazon_msk_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#amazon_msk_cluster MskReplicator#amazon_msk_cluster}
        '''
        result = self._values.get("amazon_msk_cluster")
        assert result is not None, "Required property 'amazon_msk_cluster' is missing"
        return typing.cast("MskReplicatorKafkaClusterAmazonMskCluster", result)

    @builtins.property
    def vpc_config(self) -> "MskReplicatorKafkaClusterVpcConfig":
        '''vpc_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#vpc_config MskReplicator#vpc_config}
        '''
        result = self._values.get("vpc_config")
        assert result is not None, "Required property 'vpc_config' is missing"
        return typing.cast("MskReplicatorKafkaClusterVpcConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorKafkaCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorKafkaClusterAmazonMskCluster",
    jsii_struct_bases=[],
    name_mapping={"msk_cluster_arn": "mskClusterArn"},
)
class MskReplicatorKafkaClusterAmazonMskCluster:
    def __init__(self, *, msk_cluster_arn: builtins.str) -> None:
        '''
        :param msk_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#msk_cluster_arn MskReplicator#msk_cluster_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b89a57bcf422144c9001634c3633498c44b8d66c291733cb5e97b3a27bfb15)
            check_type(argname="argument msk_cluster_arn", value=msk_cluster_arn, expected_type=type_hints["msk_cluster_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "msk_cluster_arn": msk_cluster_arn,
        }

    @builtins.property
    def msk_cluster_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#msk_cluster_arn MskReplicator#msk_cluster_arn}.'''
        result = self._values.get("msk_cluster_arn")
        assert result is not None, "Required property 'msk_cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorKafkaClusterAmazonMskCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorKafkaClusterAmazonMskClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorKafkaClusterAmazonMskClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb4bba4a4f713a49a53ccef7edfb01378286b72e2834bd93cb2bc48a5635257e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="mskClusterArnInput")
    def msk_cluster_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mskClusterArnInput"))

    @builtins.property
    @jsii.member(jsii_name="mskClusterArn")
    def msk_cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mskClusterArn"))

    @msk_cluster_arn.setter
    def msk_cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30902fc7aae6d07df2f146613f0706c8b112d4cfb464b41ca5429d731a26df41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mskClusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster]:
        return typing.cast(typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75fd7f402fe2f2b0c2dd3e82d1ae53ec2982346c469bc81c548337097934126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskReplicatorKafkaClusterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorKafkaClusterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5275e70eb4cde3e5a5d3ee7cdbcda74fe0672e9bb1f54bd1fca58ffae6600df5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MskReplicatorKafkaClusterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d4d1e98b2ccef9274ca470e661d369cd27326aed6346e411620cf4ec2cd172)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MskReplicatorKafkaClusterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6146e425bde7e8a7753285e304dd9ccce062fb30766ea0aeb8f900719c46eefb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e88a089735ce2b712b42494d7c6038b439da6d0dcf672ec7e9459ee56486768)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8be7192716872798f60736c0ff5f25574484a1584fe503045e53e65686021364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorKafkaCluster]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorKafkaCluster]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorKafkaCluster]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c062023520a1068bbf2504b1dc79efd3881c14273f9d8e010a0da05ecad6dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskReplicatorKafkaClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorKafkaClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7641394732c309889d033abd18113e19421211f491fc949f78b0675ec0f7a4f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAmazonMskCluster")
    def put_amazon_msk_cluster(self, *, msk_cluster_arn: builtins.str) -> None:
        '''
        :param msk_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#msk_cluster_arn MskReplicator#msk_cluster_arn}.
        '''
        value = MskReplicatorKafkaClusterAmazonMskCluster(
            msk_cluster_arn=msk_cluster_arn
        )

        return typing.cast(None, jsii.invoke(self, "putAmazonMskCluster", [value]))

    @jsii.member(jsii_name="putVpcConfig")
    def put_vpc_config(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        security_groups_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#subnet_ids MskReplicator#subnet_ids}.
        :param security_groups_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#security_groups_ids MskReplicator#security_groups_ids}.
        '''
        value = MskReplicatorKafkaClusterVpcConfig(
            subnet_ids=subnet_ids, security_groups_ids=security_groups_ids
        )

        return typing.cast(None, jsii.invoke(self, "putVpcConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="amazonMskCluster")
    def amazon_msk_cluster(
        self,
    ) -> MskReplicatorKafkaClusterAmazonMskClusterOutputReference:
        return typing.cast(MskReplicatorKafkaClusterAmazonMskClusterOutputReference, jsii.get(self, "amazonMskCluster"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> "MskReplicatorKafkaClusterVpcConfigOutputReference":
        return typing.cast("MskReplicatorKafkaClusterVpcConfigOutputReference", jsii.get(self, "vpcConfig"))

    @builtins.property
    @jsii.member(jsii_name="amazonMskClusterInput")
    def amazon_msk_cluster_input(
        self,
    ) -> typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster]:
        return typing.cast(typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster], jsii.get(self, "amazonMskClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcConfigInput")
    def vpc_config_input(self) -> typing.Optional["MskReplicatorKafkaClusterVpcConfig"]:
        return typing.cast(typing.Optional["MskReplicatorKafkaClusterVpcConfig"], jsii.get(self, "vpcConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorKafkaCluster]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorKafkaCluster]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorKafkaCluster]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00bd7033cc399e0c285dea53ea54766aa23f293a1a2953c01c7310e1e981ceeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorKafkaClusterVpcConfig",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_ids": "subnetIds",
        "security_groups_ids": "securityGroupsIds",
    },
)
class MskReplicatorKafkaClusterVpcConfig:
    def __init__(
        self,
        *,
        subnet_ids: typing.Sequence[builtins.str],
        security_groups_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#subnet_ids MskReplicator#subnet_ids}.
        :param security_groups_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#security_groups_ids MskReplicator#security_groups_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874166509df2a84effd1862f6da6206aee7e5361f2327c2fb4da5c3559bbe069)
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument security_groups_ids", value=security_groups_ids, expected_type=type_hints["security_groups_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_ids": subnet_ids,
        }
        if security_groups_ids is not None:
            self._values["security_groups_ids"] = security_groups_ids

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#subnet_ids MskReplicator#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def security_groups_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#security_groups_ids MskReplicator#security_groups_ids}.'''
        result = self._values.get("security_groups_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorKafkaClusterVpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorKafkaClusterVpcConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorKafkaClusterVpcConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f540e736f439c6bc069ec64b21489e8f3370a299f89588e42c730c096148a8d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSecurityGroupsIds")
    def reset_security_groups_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupsIds", []))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsIdsInput")
    def security_groups_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsIds")
    def security_groups_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupsIds"))

    @security_groups_ids.setter
    def security_groups_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d41fc942785e57fbf44840de1b8fa35a6177d38c7c0354160d8f03b0963335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupsIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7956ef8d8975696e9f54bf130aa83220ffa6598e4ea4e0d22d7f41fe382d3fa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskReplicatorKafkaClusterVpcConfig]:
        return typing.cast(typing.Optional[MskReplicatorKafkaClusterVpcConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorKafkaClusterVpcConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d27acfb20be793924549fe0ca1fea3a713bf8b5a07628d44ffb06bd1876491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListConsumerGroupReplication",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_groups_to_replicate": "consumerGroupsToReplicate",
        "consumer_groups_to_exclude": "consumerGroupsToExclude",
        "detect_and_copy_new_consumer_groups": "detectAndCopyNewConsumerGroups",
        "synchronise_consumer_group_offsets": "synchroniseConsumerGroupOffsets",
    },
)
class MskReplicatorReplicationInfoListConsumerGroupReplication:
    def __init__(
        self,
        *,
        consumer_groups_to_replicate: typing.Sequence[builtins.str],
        consumer_groups_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        detect_and_copy_new_consumer_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        synchronise_consumer_group_offsets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param consumer_groups_to_replicate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#consumer_groups_to_replicate MskReplicator#consumer_groups_to_replicate}.
        :param consumer_groups_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#consumer_groups_to_exclude MskReplicator#consumer_groups_to_exclude}.
        :param detect_and_copy_new_consumer_groups: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#detect_and_copy_new_consumer_groups MskReplicator#detect_and_copy_new_consumer_groups}.
        :param synchronise_consumer_group_offsets: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#synchronise_consumer_group_offsets MskReplicator#synchronise_consumer_group_offsets}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4962a2c44526beea016e978830d1aa4be819b84e9a1a169e06e6ec9eba9f6b)
            check_type(argname="argument consumer_groups_to_replicate", value=consumer_groups_to_replicate, expected_type=type_hints["consumer_groups_to_replicate"])
            check_type(argname="argument consumer_groups_to_exclude", value=consumer_groups_to_exclude, expected_type=type_hints["consumer_groups_to_exclude"])
            check_type(argname="argument detect_and_copy_new_consumer_groups", value=detect_and_copy_new_consumer_groups, expected_type=type_hints["detect_and_copy_new_consumer_groups"])
            check_type(argname="argument synchronise_consumer_group_offsets", value=synchronise_consumer_group_offsets, expected_type=type_hints["synchronise_consumer_group_offsets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_groups_to_replicate": consumer_groups_to_replicate,
        }
        if consumer_groups_to_exclude is not None:
            self._values["consumer_groups_to_exclude"] = consumer_groups_to_exclude
        if detect_and_copy_new_consumer_groups is not None:
            self._values["detect_and_copy_new_consumer_groups"] = detect_and_copy_new_consumer_groups
        if synchronise_consumer_group_offsets is not None:
            self._values["synchronise_consumer_group_offsets"] = synchronise_consumer_group_offsets

    @builtins.property
    def consumer_groups_to_replicate(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#consumer_groups_to_replicate MskReplicator#consumer_groups_to_replicate}.'''
        result = self._values.get("consumer_groups_to_replicate")
        assert result is not None, "Required property 'consumer_groups_to_replicate' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def consumer_groups_to_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#consumer_groups_to_exclude MskReplicator#consumer_groups_to_exclude}.'''
        result = self._values.get("consumer_groups_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def detect_and_copy_new_consumer_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#detect_and_copy_new_consumer_groups MskReplicator#detect_and_copy_new_consumer_groups}.'''
        result = self._values.get("detect_and_copy_new_consumer_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def synchronise_consumer_group_offsets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#synchronise_consumer_group_offsets MskReplicator#synchronise_consumer_group_offsets}.'''
        result = self._values.get("synchronise_consumer_group_offsets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListConsumerGroupReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListConsumerGroupReplicationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListConsumerGroupReplicationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__134ea0513ca91cceb3820c5a208eb31be94b5cbdc1ad121b0302d7d178d27a01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8126c1eb1dd3dbe34841f0639a618b102effc337f36f9c2008fc791575aff9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730b4942071536122f747e699afcc0590cebb2946f4718e3f2c1b461f13d9d9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8196d25de2b707a59b3d04a2117e74e71b1d6f438d9388649ef2b6ba154b75d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ead9106813a582ee7e7bb27108e521a3274972692bdb6382738575c0e5491a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c502dd290334c8aff1afe308881695ec5c0167c81bea759a9fa0bbce81af01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81098739525fab475712cbf952aa1ed769510d550f7e5f55b84c9081c17aa1cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConsumerGroupsToExclude")
    def reset_consumer_groups_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerGroupsToExclude", []))

    @jsii.member(jsii_name="resetDetectAndCopyNewConsumerGroups")
    def reset_detect_and_copy_new_consumer_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectAndCopyNewConsumerGroups", []))

    @jsii.member(jsii_name="resetSynchroniseConsumerGroupOffsets")
    def reset_synchronise_consumer_group_offsets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSynchroniseConsumerGroupOffsets", []))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupsToExcludeInput")
    def consumer_groups_to_exclude_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "consumerGroupsToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupsToReplicateInput")
    def consumer_groups_to_replicate_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "consumerGroupsToReplicateInput"))

    @builtins.property
    @jsii.member(jsii_name="detectAndCopyNewConsumerGroupsInput")
    def detect_and_copy_new_consumer_groups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "detectAndCopyNewConsumerGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="synchroniseConsumerGroupOffsetsInput")
    def synchronise_consumer_group_offsets_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "synchroniseConsumerGroupOffsetsInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupsToExclude")
    def consumer_groups_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "consumerGroupsToExclude"))

    @consumer_groups_to_exclude.setter
    def consumer_groups_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3365ac645300cf30eea22e3e76c6460cf4893732ac650a39438578a90a346e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupsToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerGroupsToReplicate")
    def consumer_groups_to_replicate(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "consumerGroupsToReplicate"))

    @consumer_groups_to_replicate.setter
    def consumer_groups_to_replicate(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e32cac43a8da5593a965240f595875dcfc22f4b46b8fafec0c73ddbe2a11c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupsToReplicate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectAndCopyNewConsumerGroups")
    def detect_and_copy_new_consumer_groups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "detectAndCopyNewConsumerGroups"))

    @detect_and_copy_new_consumer_groups.setter
    def detect_and_copy_new_consumer_groups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d973ee17499d8ee0dff565185268eb27cfee6c72e4dabf9dca899b36618d2c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectAndCopyNewConsumerGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="synchroniseConsumerGroupOffsets")
    def synchronise_consumer_group_offsets(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "synchroniseConsumerGroupOffsets"))

    @synchronise_consumer_group_offsets.setter
    def synchronise_consumer_group_offsets(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443fd50596a07049341193c466ff832c018083271324dca96ac9d444e690da32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synchroniseConsumerGroupOffsets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListConsumerGroupReplication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListConsumerGroupReplication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListConsumerGroupReplication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ba9c7335ad331f1b975a2ecf5bcbca0938cb928b596ce3279c23b575362e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListStruct",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_group_replication": "consumerGroupReplication",
        "source_kafka_cluster_arn": "sourceKafkaClusterArn",
        "target_compression_type": "targetCompressionType",
        "target_kafka_cluster_arn": "targetKafkaClusterArn",
        "topic_replication": "topicReplication",
    },
)
class MskReplicatorReplicationInfoListStruct:
    def __init__(
        self,
        *,
        consumer_group_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListConsumerGroupReplication, typing.Dict[builtins.str, typing.Any]]]],
        source_kafka_cluster_arn: builtins.str,
        target_compression_type: builtins.str,
        target_kafka_cluster_arn: builtins.str,
        topic_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorReplicationInfoListTopicReplication", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param consumer_group_replication: consumer_group_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#consumer_group_replication MskReplicator#consumer_group_replication}
        :param source_kafka_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#source_kafka_cluster_arn MskReplicator#source_kafka_cluster_arn}.
        :param target_compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#target_compression_type MskReplicator#target_compression_type}.
        :param target_kafka_cluster_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#target_kafka_cluster_arn MskReplicator#target_kafka_cluster_arn}.
        :param topic_replication: topic_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topic_replication MskReplicator#topic_replication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82598980ad7f2827bb0bfc995d2fff7e769d47cb047bdc26be8b9347fabd327b)
            check_type(argname="argument consumer_group_replication", value=consumer_group_replication, expected_type=type_hints["consumer_group_replication"])
            check_type(argname="argument source_kafka_cluster_arn", value=source_kafka_cluster_arn, expected_type=type_hints["source_kafka_cluster_arn"])
            check_type(argname="argument target_compression_type", value=target_compression_type, expected_type=type_hints["target_compression_type"])
            check_type(argname="argument target_kafka_cluster_arn", value=target_kafka_cluster_arn, expected_type=type_hints["target_kafka_cluster_arn"])
            check_type(argname="argument topic_replication", value=topic_replication, expected_type=type_hints["topic_replication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_group_replication": consumer_group_replication,
            "source_kafka_cluster_arn": source_kafka_cluster_arn,
            "target_compression_type": target_compression_type,
            "target_kafka_cluster_arn": target_kafka_cluster_arn,
            "topic_replication": topic_replication,
        }

    @builtins.property
    def consumer_group_replication(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]:
        '''consumer_group_replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#consumer_group_replication MskReplicator#consumer_group_replication}
        '''
        result = self._values.get("consumer_group_replication")
        assert result is not None, "Required property 'consumer_group_replication' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]], result)

    @builtins.property
    def source_kafka_cluster_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#source_kafka_cluster_arn MskReplicator#source_kafka_cluster_arn}.'''
        result = self._values.get("source_kafka_cluster_arn")
        assert result is not None, "Required property 'source_kafka_cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_compression_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#target_compression_type MskReplicator#target_compression_type}.'''
        result = self._values.get("target_compression_type")
        assert result is not None, "Required property 'target_compression_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_kafka_cluster_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#target_kafka_cluster_arn MskReplicator#target_kafka_cluster_arn}.'''
        result = self._values.get("target_kafka_cluster_arn")
        assert result is not None, "Required property 'target_kafka_cluster_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_replication(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorReplicationInfoListTopicReplication"]]:
        '''topic_replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topic_replication MskReplicator#topic_replication}
        '''
        result = self._values.get("topic_replication")
        assert result is not None, "Required property 'topic_replication' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorReplicationInfoListTopicReplication"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92e261038d0b609b70af2e080333847a763732d0ccc11b15aa03d558e0a3709f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConsumerGroupReplication")
    def put_consumer_group_replication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListConsumerGroupReplication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc32df6621bad565ec721ac79a7e83099d95491d5c13b2663865e175116dec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConsumerGroupReplication", [value]))

    @jsii.member(jsii_name="putTopicReplication")
    def put_topic_replication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MskReplicatorReplicationInfoListTopicReplication", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7656c7335f49a403636af151eefb78520eb2b13cf3c29f0a856287aec758aa11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTopicReplication", [value]))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupReplication")
    def consumer_group_replication(
        self,
    ) -> MskReplicatorReplicationInfoListConsumerGroupReplicationList:
        return typing.cast(MskReplicatorReplicationInfoListConsumerGroupReplicationList, jsii.get(self, "consumerGroupReplication"))

    @builtins.property
    @jsii.member(jsii_name="sourceKafkaClusterAlias")
    def source_kafka_cluster_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceKafkaClusterAlias"))

    @builtins.property
    @jsii.member(jsii_name="targetKafkaClusterAlias")
    def target_kafka_cluster_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetKafkaClusterAlias"))

    @builtins.property
    @jsii.member(jsii_name="topicReplication")
    def topic_replication(
        self,
    ) -> "MskReplicatorReplicationInfoListTopicReplicationList":
        return typing.cast("MskReplicatorReplicationInfoListTopicReplicationList", jsii.get(self, "topicReplication"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupReplicationInput")
    def consumer_group_replication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]], jsii.get(self, "consumerGroupReplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceKafkaClusterArnInput")
    def source_kafka_cluster_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceKafkaClusterArnInput"))

    @builtins.property
    @jsii.member(jsii_name="targetCompressionTypeInput")
    def target_compression_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetCompressionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetKafkaClusterArnInput")
    def target_kafka_cluster_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetKafkaClusterArnInput"))

    @builtins.property
    @jsii.member(jsii_name="topicReplicationInput")
    def topic_replication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorReplicationInfoListTopicReplication"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MskReplicatorReplicationInfoListTopicReplication"]]], jsii.get(self, "topicReplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceKafkaClusterArn")
    def source_kafka_cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceKafkaClusterArn"))

    @source_kafka_cluster_arn.setter
    def source_kafka_cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee5fcffe8758f0ea5c22d63098d89939942370597c27fef5b8c9df5ee02ab6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceKafkaClusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetCompressionType")
    def target_compression_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetCompressionType"))

    @target_compression_type.setter
    def target_compression_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672378123a38f77a975f0f171099407ad43b61eaa551e37808683ef2a1d1c284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetCompressionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetKafkaClusterArn")
    def target_kafka_cluster_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetKafkaClusterArn"))

    @target_kafka_cluster_arn.setter
    def target_kafka_cluster_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590132d8f467bdef8618265949845fa90e0a9f9ebba543340f182e38d3aa1577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetKafkaClusterArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MskReplicatorReplicationInfoListStruct]:
        return typing.cast(typing.Optional[MskReplicatorReplicationInfoListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorReplicationInfoListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c21640e1ad311c30e6447726b2b84e112c132fed401dd9c841d77fa209369c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplication",
    jsii_struct_bases=[],
    name_mapping={
        "topics_to_replicate": "topicsToReplicate",
        "copy_access_control_lists_for_topics": "copyAccessControlListsForTopics",
        "copy_topic_configurations": "copyTopicConfigurations",
        "detect_and_copy_new_topics": "detectAndCopyNewTopics",
        "starting_position": "startingPosition",
        "topic_name_configuration": "topicNameConfiguration",
        "topics_to_exclude": "topicsToExclude",
    },
)
class MskReplicatorReplicationInfoListTopicReplication:
    def __init__(
        self,
        *,
        topics_to_replicate: typing.Sequence[builtins.str],
        copy_access_control_lists_for_topics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        copy_topic_configurations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        detect_and_copy_new_topics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        starting_position: typing.Optional[typing.Union["MskReplicatorReplicationInfoListTopicReplicationStartingPosition", typing.Dict[builtins.str, typing.Any]]] = None,
        topic_name_configuration: typing.Optional[typing.Union["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        topics_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param topics_to_replicate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topics_to_replicate MskReplicator#topics_to_replicate}.
        :param copy_access_control_lists_for_topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#copy_access_control_lists_for_topics MskReplicator#copy_access_control_lists_for_topics}.
        :param copy_topic_configurations: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#copy_topic_configurations MskReplicator#copy_topic_configurations}.
        :param detect_and_copy_new_topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#detect_and_copy_new_topics MskReplicator#detect_and_copy_new_topics}.
        :param starting_position: starting_position block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#starting_position MskReplicator#starting_position}
        :param topic_name_configuration: topic_name_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topic_name_configuration MskReplicator#topic_name_configuration}
        :param topics_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topics_to_exclude MskReplicator#topics_to_exclude}.
        '''
        if isinstance(starting_position, dict):
            starting_position = MskReplicatorReplicationInfoListTopicReplicationStartingPosition(**starting_position)
        if isinstance(topic_name_configuration, dict):
            topic_name_configuration = MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration(**topic_name_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076c0d2400643415aa49e5d0215f40ea2841a3805e9d88a098b0e2ac3b544dc1)
            check_type(argname="argument topics_to_replicate", value=topics_to_replicate, expected_type=type_hints["topics_to_replicate"])
            check_type(argname="argument copy_access_control_lists_for_topics", value=copy_access_control_lists_for_topics, expected_type=type_hints["copy_access_control_lists_for_topics"])
            check_type(argname="argument copy_topic_configurations", value=copy_topic_configurations, expected_type=type_hints["copy_topic_configurations"])
            check_type(argname="argument detect_and_copy_new_topics", value=detect_and_copy_new_topics, expected_type=type_hints["detect_and_copy_new_topics"])
            check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
            check_type(argname="argument topic_name_configuration", value=topic_name_configuration, expected_type=type_hints["topic_name_configuration"])
            check_type(argname="argument topics_to_exclude", value=topics_to_exclude, expected_type=type_hints["topics_to_exclude"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topics_to_replicate": topics_to_replicate,
        }
        if copy_access_control_lists_for_topics is not None:
            self._values["copy_access_control_lists_for_topics"] = copy_access_control_lists_for_topics
        if copy_topic_configurations is not None:
            self._values["copy_topic_configurations"] = copy_topic_configurations
        if detect_and_copy_new_topics is not None:
            self._values["detect_and_copy_new_topics"] = detect_and_copy_new_topics
        if starting_position is not None:
            self._values["starting_position"] = starting_position
        if topic_name_configuration is not None:
            self._values["topic_name_configuration"] = topic_name_configuration
        if topics_to_exclude is not None:
            self._values["topics_to_exclude"] = topics_to_exclude

    @builtins.property
    def topics_to_replicate(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topics_to_replicate MskReplicator#topics_to_replicate}.'''
        result = self._values.get("topics_to_replicate")
        assert result is not None, "Required property 'topics_to_replicate' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def copy_access_control_lists_for_topics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#copy_access_control_lists_for_topics MskReplicator#copy_access_control_lists_for_topics}.'''
        result = self._values.get("copy_access_control_lists_for_topics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def copy_topic_configurations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#copy_topic_configurations MskReplicator#copy_topic_configurations}.'''
        result = self._values.get("copy_topic_configurations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def detect_and_copy_new_topics(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#detect_and_copy_new_topics MskReplicator#detect_and_copy_new_topics}.'''
        result = self._values.get("detect_and_copy_new_topics")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def starting_position(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListTopicReplicationStartingPosition"]:
        '''starting_position block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#starting_position MskReplicator#starting_position}
        '''
        result = self._values.get("starting_position")
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListTopicReplicationStartingPosition"], result)

    @builtins.property
    def topic_name_configuration(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration"]:
        '''topic_name_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topic_name_configuration MskReplicator#topic_name_configuration}
        '''
        result = self._values.get("topic_name_configuration")
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration"], result)

    @builtins.property
    def topics_to_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#topics_to_exclude MskReplicator#topics_to_exclude}.'''
        result = self._values.get("topics_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListTopicReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListTopicReplicationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43a68d3d4329a8bea3ecdd30cb3dc76f41cef5d668e8d96829bcec74dd6ea89d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MskReplicatorReplicationInfoListTopicReplicationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94def4a5205a6c65a70558a254d8215cb8f50a57fe1dcda589a5193c5a97ac7a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MskReplicatorReplicationInfoListTopicReplicationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f9b411cc3304354ab17f973e5d696a5595117ab2272a073b02e9097997175d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9500ea88cf73db532bb705e774d7f9376d7e1467ee11bbb9a7a7b50476bb22ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1be62bf5c204db75c0702476da87928d4c0f9eeabda6ac27fce2efa7aee14fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListTopicReplication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListTopicReplication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListTopicReplication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e0c9bcc5555dcc8fc20a9687aaa64886643bb745a96cb0b5807fd5ce6953df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MskReplicatorReplicationInfoListTopicReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c817e6e02a09c946383a92af0858127d517e89b7babc5549ca16bda75e1d6917)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putStartingPosition")
    def put_starting_position(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#type MskReplicator#type}.
        '''
        value = MskReplicatorReplicationInfoListTopicReplicationStartingPosition(
            type=type
        )

        return typing.cast(None, jsii.invoke(self, "putStartingPosition", [value]))

    @jsii.member(jsii_name="putTopicNameConfiguration")
    def put_topic_name_configuration(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#type MskReplicator#type}.
        '''
        value = MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration(
            type=type
        )

        return typing.cast(None, jsii.invoke(self, "putTopicNameConfiguration", [value]))

    @jsii.member(jsii_name="resetCopyAccessControlListsForTopics")
    def reset_copy_access_control_lists_for_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyAccessControlListsForTopics", []))

    @jsii.member(jsii_name="resetCopyTopicConfigurations")
    def reset_copy_topic_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCopyTopicConfigurations", []))

    @jsii.member(jsii_name="resetDetectAndCopyNewTopics")
    def reset_detect_and_copy_new_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectAndCopyNewTopics", []))

    @jsii.member(jsii_name="resetStartingPosition")
    def reset_starting_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartingPosition", []))

    @jsii.member(jsii_name="resetTopicNameConfiguration")
    def reset_topic_name_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicNameConfiguration", []))

    @jsii.member(jsii_name="resetTopicsToExclude")
    def reset_topics_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicsToExclude", []))

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(
        self,
    ) -> "MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference":
        return typing.cast("MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference", jsii.get(self, "startingPosition"))

    @builtins.property
    @jsii.member(jsii_name="topicNameConfiguration")
    def topic_name_configuration(
        self,
    ) -> "MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference":
        return typing.cast("MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference", jsii.get(self, "topicNameConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="copyAccessControlListsForTopicsInput")
    def copy_access_control_lists_for_topics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyAccessControlListsForTopicsInput"))

    @builtins.property
    @jsii.member(jsii_name="copyTopicConfigurationsInput")
    def copy_topic_configurations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "copyTopicConfigurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="detectAndCopyNewTopicsInput")
    def detect_and_copy_new_topics_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "detectAndCopyNewTopicsInput"))

    @builtins.property
    @jsii.member(jsii_name="startingPositionInput")
    def starting_position_input(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListTopicReplicationStartingPosition"]:
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListTopicReplicationStartingPosition"], jsii.get(self, "startingPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="topicNameConfigurationInput")
    def topic_name_configuration_input(
        self,
    ) -> typing.Optional["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration"]:
        return typing.cast(typing.Optional["MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration"], jsii.get(self, "topicNameConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsToExcludeInput")
    def topics_to_exclude_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsToReplicateInput")
    def topics_to_replicate_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsToReplicateInput"))

    @builtins.property
    @jsii.member(jsii_name="copyAccessControlListsForTopics")
    def copy_access_control_lists_for_topics(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyAccessControlListsForTopics"))

    @copy_access_control_lists_for_topics.setter
    def copy_access_control_lists_for_topics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae6820d743273684a6f1a4cf78dcb97b79402b58102e9e5d56ec8284c68c27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyAccessControlListsForTopics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyTopicConfigurations")
    def copy_topic_configurations(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "copyTopicConfigurations"))

    @copy_topic_configurations.setter
    def copy_topic_configurations(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d103c57479e57593f47a0d3c8c85e3a2a9d8aa1bceba21c2c9eaa3264bf6b901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTopicConfigurations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="detectAndCopyNewTopics")
    def detect_and_copy_new_topics(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "detectAndCopyNewTopics"))

    @detect_and_copy_new_topics.setter
    def detect_and_copy_new_topics(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d447db7168e43fe4b1144077eed9f6ee04ce8cb98f31a19ddb309d9a9d2e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectAndCopyNewTopics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicsToExclude")
    def topics_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topicsToExclude"))

    @topics_to_exclude.setter
    def topics_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2b7938c880b71221a28e3cb952d92369358a505fed0a0557a008d811ad6f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicsToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicsToReplicate")
    def topics_to_replicate(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topicsToReplicate"))

    @topics_to_replicate.setter
    def topics_to_replicate(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59b599b847f780d75a6ab2bb797ffb48a2d6ac0e8adf6071a9e5b731615f115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicsToReplicate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListTopicReplication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListTopicReplication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListTopicReplication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a18fc68ee40ddd83f364458cb8d84833c5f1ca0a7ea849daf877887ed2cf0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationStartingPosition",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class MskReplicatorReplicationInfoListTopicReplicationStartingPosition:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#type MskReplicator#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063077220f657812d6f96b6f9c8eeeafcef8989965bb95c12a5a69dc39cdd3e6)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#type MskReplicator#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListTopicReplicationStartingPosition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f695718aca0e8d0e60b55f2561b25293366dbebb6134b361da85e63cc6b38b99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7433f42f088cd55c0ab381f8f1cda6a0f9163696e8ab73f1d6cef3efbf128304)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskReplicatorReplicationInfoListTopicReplicationStartingPosition]:
        return typing.cast(typing.Optional[MskReplicatorReplicationInfoListTopicReplicationStartingPosition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorReplicationInfoListTopicReplicationStartingPosition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac78eeb943c852112075665a837778ccc1324cb72a6673645fb67b4b4a560c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#type MskReplicator#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb1919d26dd7427b669b75a11a269ab86131b544332a7964a331576522e2cb7)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#type MskReplicator#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93bb52d02283c22eeb29105fd2b46ef338303450ec9ddea86e6bb29fae77bc11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35927770a1c42110778ef3ea412a6feb1e73acf0023b489214e0d60636f735f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration]:
        return typing.cast(typing.Optional[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83af1c0e75f546ce6c831add518811cc8607d3dfc78c6e924fe25e2a081e9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class MskReplicatorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#create MskReplicator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#delete MskReplicator#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#update MskReplicator#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097972b0c1c055b2fd4950139334d092e2b1c095ec7caa228b43fe1e227dbd51)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#create MskReplicator#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#delete MskReplicator#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/msk_replicator#update MskReplicator#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MskReplicatorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MskReplicatorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.mskReplicator.MskReplicatorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfec71e311a2457b98f4d7b6929fbfb48e2f9d673717545265dfab039e2377f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9ecead12290584dc313df1e3edbc3f509339aed4ec29af08670b6338d808af8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75ae8154181c605be4e785cb9a6c941ec6e749b4bb38ee7bdc7bce722fdc2e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37342265491ee90e3da19276ed6fc02eb93db303eca63361ddffa776628cf36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda22b2256b546a42ef013102d953ba5fdd80529d821b2897efcd7f4b613655a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MskReplicator",
    "MskReplicatorConfig",
    "MskReplicatorKafkaCluster",
    "MskReplicatorKafkaClusterAmazonMskCluster",
    "MskReplicatorKafkaClusterAmazonMskClusterOutputReference",
    "MskReplicatorKafkaClusterList",
    "MskReplicatorKafkaClusterOutputReference",
    "MskReplicatorKafkaClusterVpcConfig",
    "MskReplicatorKafkaClusterVpcConfigOutputReference",
    "MskReplicatorReplicationInfoListConsumerGroupReplication",
    "MskReplicatorReplicationInfoListConsumerGroupReplicationList",
    "MskReplicatorReplicationInfoListConsumerGroupReplicationOutputReference",
    "MskReplicatorReplicationInfoListStruct",
    "MskReplicatorReplicationInfoListStructOutputReference",
    "MskReplicatorReplicationInfoListTopicReplication",
    "MskReplicatorReplicationInfoListTopicReplicationList",
    "MskReplicatorReplicationInfoListTopicReplicationOutputReference",
    "MskReplicatorReplicationInfoListTopicReplicationStartingPosition",
    "MskReplicatorReplicationInfoListTopicReplicationStartingPositionOutputReference",
    "MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration",
    "MskReplicatorReplicationInfoListTopicReplicationTopicNameConfigurationOutputReference",
    "MskReplicatorTimeouts",
    "MskReplicatorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__94bce509affa29908bc7cb438ce56e1b60dd60f41cd22289e0e544f5e2520765(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    kafka_cluster: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorKafkaCluster, typing.Dict[builtins.str, typing.Any]]]],
    replication_info_list: typing.Union[MskReplicatorReplicationInfoListStruct, typing.Dict[builtins.str, typing.Any]],
    replicator_name: builtins.str,
    service_execution_role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MskReplicatorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__0a94a16bbcd335e6f9a88fa8a0b0dc6ee88ca43283d855cfe71e80ea19c2f20b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8984721c0196cf8c2553735e86f5aeb4c0f6947f2cb09067f0ef5d163370b2dd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorKafkaCluster, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb8dfcf1f13ed278359c5f1c96ee48b7748131f3adeeb8a44e13333cc67d17e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979ca3777545d110a54572e412d4d222cb256907f4f4784ed73defacfd423760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a627e51c65666ef79d287eee28f1b46350783231267ba41c90af71ccfdbce21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef3f63422c9fffb38a550fa6ba5213964de8e1fbbb839346639eda9c572db51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae06f4314d9f73b7fd3eedd164f02db9f932598264c8f956ddb9a83055c1549(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a780466809bc40852951c572b54707d350908095ca18955caeee3ae433f27837(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76f0d692bcc87e4a2f71e8f9c954fc554cb38322bcc29eeac3fc91fb5b6d7f7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    kafka_cluster: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorKafkaCluster, typing.Dict[builtins.str, typing.Any]]]],
    replication_info_list: typing.Union[MskReplicatorReplicationInfoListStruct, typing.Dict[builtins.str, typing.Any]],
    replicator_name: builtins.str,
    service_execution_role_arn: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MskReplicatorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28124b6b83502af775c3ef35e3b085677cd08935f335d654e2c53c5a73b1430e(
    *,
    amazon_msk_cluster: typing.Union[MskReplicatorKafkaClusterAmazonMskCluster, typing.Dict[builtins.str, typing.Any]],
    vpc_config: typing.Union[MskReplicatorKafkaClusterVpcConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b89a57bcf422144c9001634c3633498c44b8d66c291733cb5e97b3a27bfb15(
    *,
    msk_cluster_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4bba4a4f713a49a53ccef7edfb01378286b72e2834bd93cb2bc48a5635257e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30902fc7aae6d07df2f146613f0706c8b112d4cfb464b41ca5429d731a26df41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75fd7f402fe2f2b0c2dd3e82d1ae53ec2982346c469bc81c548337097934126(
    value: typing.Optional[MskReplicatorKafkaClusterAmazonMskCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5275e70eb4cde3e5a5d3ee7cdbcda74fe0672e9bb1f54bd1fca58ffae6600df5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d4d1e98b2ccef9274ca470e661d369cd27326aed6346e411620cf4ec2cd172(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6146e425bde7e8a7753285e304dd9ccce062fb30766ea0aeb8f900719c46eefb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e88a089735ce2b712b42494d7c6038b439da6d0dcf672ec7e9459ee56486768(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be7192716872798f60736c0ff5f25574484a1584fe503045e53e65686021364(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c062023520a1068bbf2504b1dc79efd3881c14273f9d8e010a0da05ecad6dfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorKafkaCluster]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7641394732c309889d033abd18113e19421211f491fc949f78b0675ec0f7a4f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00bd7033cc399e0c285dea53ea54766aa23f293a1a2953c01c7310e1e981ceeb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorKafkaCluster]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874166509df2a84effd1862f6da6206aee7e5361f2327c2fb4da5c3559bbe069(
    *,
    subnet_ids: typing.Sequence[builtins.str],
    security_groups_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f540e736f439c6bc069ec64b21489e8f3370a299f89588e42c730c096148a8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d41fc942785e57fbf44840de1b8fa35a6177d38c7c0354160d8f03b0963335(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7956ef8d8975696e9f54bf130aa83220ffa6598e4ea4e0d22d7f41fe382d3fa9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d27acfb20be793924549fe0ca1fea3a713bf8b5a07628d44ffb06bd1876491(
    value: typing.Optional[MskReplicatorKafkaClusterVpcConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4962a2c44526beea016e978830d1aa4be819b84e9a1a169e06e6ec9eba9f6b(
    *,
    consumer_groups_to_replicate: typing.Sequence[builtins.str],
    consumer_groups_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    detect_and_copy_new_consumer_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    synchronise_consumer_group_offsets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134ea0513ca91cceb3820c5a208eb31be94b5cbdc1ad121b0302d7d178d27a01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8126c1eb1dd3dbe34841f0639a618b102effc337f36f9c2008fc791575aff9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730b4942071536122f747e699afcc0590cebb2946f4718e3f2c1b461f13d9d9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8196d25de2b707a59b3d04a2117e74e71b1d6f438d9388649ef2b6ba154b75d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ead9106813a582ee7e7bb27108e521a3274972692bdb6382738575c0e5491a1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c502dd290334c8aff1afe308881695ec5c0167c81bea759a9fa0bbce81af01(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListConsumerGroupReplication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81098739525fab475712cbf952aa1ed769510d550f7e5f55b84c9081c17aa1cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3365ac645300cf30eea22e3e76c6460cf4893732ac650a39438578a90a346e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e32cac43a8da5593a965240f595875dcfc22f4b46b8fafec0c73ddbe2a11c32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d973ee17499d8ee0dff565185268eb27cfee6c72e4dabf9dca899b36618d2c02(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443fd50596a07049341193c466ff832c018083271324dca96ac9d444e690da32(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ba9c7335ad331f1b975a2ecf5bcbca0938cb928b596ce3279c23b575362e8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListConsumerGroupReplication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82598980ad7f2827bb0bfc995d2fff7e769d47cb047bdc26be8b9347fabd327b(
    *,
    consumer_group_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListConsumerGroupReplication, typing.Dict[builtins.str, typing.Any]]]],
    source_kafka_cluster_arn: builtins.str,
    target_compression_type: builtins.str,
    target_kafka_cluster_arn: builtins.str,
    topic_replication: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListTopicReplication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e261038d0b609b70af2e080333847a763732d0ccc11b15aa03d558e0a3709f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc32df6621bad565ec721ac79a7e83099d95491d5c13b2663865e175116dec0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListConsumerGroupReplication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7656c7335f49a403636af151eefb78520eb2b13cf3c29f0a856287aec758aa11(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MskReplicatorReplicationInfoListTopicReplication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee5fcffe8758f0ea5c22d63098d89939942370597c27fef5b8c9df5ee02ab6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672378123a38f77a975f0f171099407ad43b61eaa551e37808683ef2a1d1c284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590132d8f467bdef8618265949845fa90e0a9f9ebba543340f182e38d3aa1577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c21640e1ad311c30e6447726b2b84e112c132fed401dd9c841d77fa209369c(
    value: typing.Optional[MskReplicatorReplicationInfoListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076c0d2400643415aa49e5d0215f40ea2841a3805e9d88a098b0e2ac3b544dc1(
    *,
    topics_to_replicate: typing.Sequence[builtins.str],
    copy_access_control_lists_for_topics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    copy_topic_configurations: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    detect_and_copy_new_topics: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    starting_position: typing.Optional[typing.Union[MskReplicatorReplicationInfoListTopicReplicationStartingPosition, typing.Dict[builtins.str, typing.Any]]] = None,
    topic_name_configuration: typing.Optional[typing.Union[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    topics_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a68d3d4329a8bea3ecdd30cb3dc76f41cef5d668e8d96829bcec74dd6ea89d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94def4a5205a6c65a70558a254d8215cb8f50a57fe1dcda589a5193c5a97ac7a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f9b411cc3304354ab17f973e5d696a5595117ab2272a073b02e9097997175d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9500ea88cf73db532bb705e774d7f9376d7e1467ee11bbb9a7a7b50476bb22ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be62bf5c204db75c0702476da87928d4c0f9eeabda6ac27fce2efa7aee14fa3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e0c9bcc5555dcc8fc20a9687aaa64886643bb745a96cb0b5807fd5ce6953df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MskReplicatorReplicationInfoListTopicReplication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c817e6e02a09c946383a92af0858127d517e89b7babc5549ca16bda75e1d6917(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae6820d743273684a6f1a4cf78dcb97b79402b58102e9e5d56ec8284c68c27a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d103c57479e57593f47a0d3c8c85e3a2a9d8aa1bceba21c2c9eaa3264bf6b901(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d447db7168e43fe4b1144077eed9f6ee04ce8cb98f31a19ddb309d9a9d2e02(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2b7938c880b71221a28e3cb952d92369358a505fed0a0557a008d811ad6f2c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59b599b847f780d75a6ab2bb797ffb48a2d6ac0e8adf6071a9e5b731615f115(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a18fc68ee40ddd83f364458cb8d84833c5f1ca0a7ea849daf877887ed2cf0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorReplicationInfoListTopicReplication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063077220f657812d6f96b6f9c8eeeafcef8989965bb95c12a5a69dc39cdd3e6(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f695718aca0e8d0e60b55f2561b25293366dbebb6134b361da85e63cc6b38b99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7433f42f088cd55c0ab381f8f1cda6a0f9163696e8ab73f1d6cef3efbf128304(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac78eeb943c852112075665a837778ccc1324cb72a6673645fb67b4b4a560c06(
    value: typing.Optional[MskReplicatorReplicationInfoListTopicReplicationStartingPosition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb1919d26dd7427b669b75a11a269ab86131b544332a7964a331576522e2cb7(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93bb52d02283c22eeb29105fd2b46ef338303450ec9ddea86e6bb29fae77bc11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35927770a1c42110778ef3ea412a6feb1e73acf0023b489214e0d60636f735f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83af1c0e75f546ce6c831add518811cc8607d3dfc78c6e924fe25e2a081e9ab(
    value: typing.Optional[MskReplicatorReplicationInfoListTopicReplicationTopicNameConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097972b0c1c055b2fd4950139334d092e2b1c095ec7caa228b43fe1e227dbd51(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfec71e311a2457b98f4d7b6929fbfb48e2f9d673717545265dfab039e2377f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ecead12290584dc313df1e3edbc3f509339aed4ec29af08670b6338d808af8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75ae8154181c605be4e785cb9a6c941ec6e749b4bb38ee7bdc7bce722fdc2e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37342265491ee90e3da19276ed6fc02eb93db303eca63361ddffa776628cf36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda22b2256b546a42ef013102d953ba5fdd80529d821b2897efcd7f4b613655a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MskReplicatorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
