r'''
# `opentelekomcloud_dms_smart_connect_task_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dms_smart_connect_task_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2).
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


class DmsSmartConnectTaskV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsSmartConnectTaskV2.DmsSmartConnectTaskV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2 opentelekomcloud_dms_smart_connect_task_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        instance_id: builtins.str,
        task_name: builtins.str,
        destination_task: typing.Optional[typing.Union["DmsSmartConnectTaskV2DestinationTask", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        source_task: typing.Optional[typing.Union["DmsSmartConnectTaskV2SourceTask", typing.Dict[builtins.str, typing.Any]]] = None,
        source_type: typing.Optional[builtins.str] = None,
        start_later: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["DmsSmartConnectTaskV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        topics_regex: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2 opentelekomcloud_dms_smart_connect_task_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#instance_id DmsSmartConnectTaskV2#instance_id}.
        :param task_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#task_name DmsSmartConnectTaskV2#task_name}.
        :param destination_task: destination_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_task DmsSmartConnectTaskV2#destination_task}
        :param destination_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_type DmsSmartConnectTaskV2#destination_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#id DmsSmartConnectTaskV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source_task: source_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#source_task DmsSmartConnectTaskV2#source_task}
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#source_type DmsSmartConnectTaskV2#source_type}.
        :param start_later: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#start_later DmsSmartConnectTaskV2#start_later}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#timeouts DmsSmartConnectTaskV2#timeouts}
        :param topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics DmsSmartConnectTaskV2#topics}.
        :param topics_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics_regex DmsSmartConnectTaskV2#topics_regex}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c94869d135426693524f66c555cdeb988bfcc59763380a45bd378d70f9d88c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DmsSmartConnectTaskV2Config(
            instance_id=instance_id,
            task_name=task_name,
            destination_task=destination_task,
            destination_type=destination_type,
            id=id,
            source_task=source_task,
            source_type=source_type,
            start_later=start_later,
            timeouts=timeouts,
            topics=topics,
            topics_regex=topics_regex,
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
        '''Generates CDKTF code for importing a DmsSmartConnectTaskV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DmsSmartConnectTaskV2 to import.
        :param import_from_id: The id of the existing DmsSmartConnectTaskV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DmsSmartConnectTaskV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__618580678454e1e43eedd5707713dd688c013a2b7a5f7d9fe9d82b419c532310)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDestinationTask")
    def put_destination_task(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        consumer_strategy: typing.Optional[builtins.str] = None,
        deliver_time_interval: typing.Optional[jsii.Number] = None,
        destination_file_type: typing.Optional[builtins.str] = None,
        obs_bucket_name: typing.Optional[builtins.str] = None,
        obs_path: typing.Optional[builtins.str] = None,
        partition_format: typing.Optional[builtins.str] = None,
        record_delimiter: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        store_keys: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#access_key DmsSmartConnectTaskV2#access_key}.
        :param consumer_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#consumer_strategy DmsSmartConnectTaskV2#consumer_strategy}.
        :param deliver_time_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#deliver_time_interval DmsSmartConnectTaskV2#deliver_time_interval}.
        :param destination_file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_file_type DmsSmartConnectTaskV2#destination_file_type}.
        :param obs_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#obs_bucket_name DmsSmartConnectTaskV2#obs_bucket_name}.
        :param obs_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#obs_path DmsSmartConnectTaskV2#obs_path}.
        :param partition_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#partition_format DmsSmartConnectTaskV2#partition_format}.
        :param record_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#record_delimiter DmsSmartConnectTaskV2#record_delimiter}.
        :param secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#secret_key DmsSmartConnectTaskV2#secret_key}.
        :param store_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#store_keys DmsSmartConnectTaskV2#store_keys}.
        '''
        value = DmsSmartConnectTaskV2DestinationTask(
            access_key=access_key,
            consumer_strategy=consumer_strategy,
            deliver_time_interval=deliver_time_interval,
            destination_file_type=destination_file_type,
            obs_bucket_name=obs_bucket_name,
            obs_path=obs_path,
            partition_format=partition_format,
            record_delimiter=record_delimiter,
            secret_key=secret_key,
            store_keys=store_keys,
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationTask", [value]))

    @jsii.member(jsii_name="putSourceTask")
    def put_source_task(
        self,
        *,
        compression_type: typing.Optional[builtins.str] = None,
        consumer_strategy: typing.Optional[builtins.str] = None,
        current_instance_alias: typing.Optional[builtins.str] = None,
        direction: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        peer_instance_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        peer_instance_alias: typing.Optional[builtins.str] = None,
        peer_instance_id: typing.Optional[builtins.str] = None,
        provenance_header_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rename_topic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
        sasl_mechanism: typing.Optional[builtins.str] = None,
        security_protocol: typing.Optional[builtins.str] = None,
        sync_consumer_offsets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        task_num: typing.Optional[jsii.Number] = None,
        topics_mapping: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#compression_type DmsSmartConnectTaskV2#compression_type}.
        :param consumer_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#consumer_strategy DmsSmartConnectTaskV2#consumer_strategy}.
        :param current_instance_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#current_instance_alias DmsSmartConnectTaskV2#current_instance_alias}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#direction DmsSmartConnectTaskV2#direction}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#password DmsSmartConnectTaskV2#password}.
        :param peer_instance_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_address DmsSmartConnectTaskV2#peer_instance_address}.
        :param peer_instance_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_alias DmsSmartConnectTaskV2#peer_instance_alias}.
        :param peer_instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_id DmsSmartConnectTaskV2#peer_instance_id}.
        :param provenance_header_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#provenance_header_enabled DmsSmartConnectTaskV2#provenance_header_enabled}.
        :param rename_topic_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#rename_topic_enabled DmsSmartConnectTaskV2#rename_topic_enabled}.
        :param replication_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#replication_factor DmsSmartConnectTaskV2#replication_factor}.
        :param sasl_mechanism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#sasl_mechanism DmsSmartConnectTaskV2#sasl_mechanism}.
        :param security_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#security_protocol DmsSmartConnectTaskV2#security_protocol}.
        :param sync_consumer_offsets_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#sync_consumer_offsets_enabled DmsSmartConnectTaskV2#sync_consumer_offsets_enabled}.
        :param task_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#task_num DmsSmartConnectTaskV2#task_num}.
        :param topics_mapping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics_mapping DmsSmartConnectTaskV2#topics_mapping}.
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#user_name DmsSmartConnectTaskV2#user_name}.
        '''
        value = DmsSmartConnectTaskV2SourceTask(
            compression_type=compression_type,
            consumer_strategy=consumer_strategy,
            current_instance_alias=current_instance_alias,
            direction=direction,
            password=password,
            peer_instance_address=peer_instance_address,
            peer_instance_alias=peer_instance_alias,
            peer_instance_id=peer_instance_id,
            provenance_header_enabled=provenance_header_enabled,
            rename_topic_enabled=rename_topic_enabled,
            replication_factor=replication_factor,
            sasl_mechanism=sasl_mechanism,
            security_protocol=security_protocol,
            sync_consumer_offsets_enabled=sync_consumer_offsets_enabled,
            task_num=task_num,
            topics_mapping=topics_mapping,
            user_name=user_name,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceTask", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#create DmsSmartConnectTaskV2#create}.
        '''
        value = DmsSmartConnectTaskV2Timeouts(create=create)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDestinationTask")
    def reset_destination_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationTask", []))

    @jsii.member(jsii_name="resetDestinationType")
    def reset_destination_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSourceTask")
    def reset_source_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceTask", []))

    @jsii.member(jsii_name="resetSourceType")
    def reset_source_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceType", []))

    @jsii.member(jsii_name="resetStartLater")
    def reset_start_later(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartLater", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTopics")
    def reset_topics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopics", []))

    @jsii.member(jsii_name="resetTopicsRegex")
    def reset_topics_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicsRegex", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="destinationTask")
    def destination_task(self) -> "DmsSmartConnectTaskV2DestinationTaskOutputReference":
        return typing.cast("DmsSmartConnectTaskV2DestinationTaskOutputReference", jsii.get(self, "destinationTask"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="sourceTask")
    def source_task(self) -> "DmsSmartConnectTaskV2SourceTaskOutputReference":
        return typing.cast("DmsSmartConnectTaskV2SourceTaskOutputReference", jsii.get(self, "sourceTask"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DmsSmartConnectTaskV2TimeoutsOutputReference":
        return typing.cast("DmsSmartConnectTaskV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="destinationTaskInput")
    def destination_task_input(
        self,
    ) -> typing.Optional["DmsSmartConnectTaskV2DestinationTask"]:
        return typing.cast(typing.Optional["DmsSmartConnectTaskV2DestinationTask"], jsii.get(self, "destinationTaskInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationTypeInput")
    def destination_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTaskInput")
    def source_task_input(self) -> typing.Optional["DmsSmartConnectTaskV2SourceTask"]:
        return typing.cast(typing.Optional["DmsSmartConnectTaskV2SourceTask"], jsii.get(self, "sourceTaskInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="startLaterInput")
    def start_later_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startLaterInput"))

    @builtins.property
    @jsii.member(jsii_name="taskNameInput")
    def task_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DmsSmartConnectTaskV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DmsSmartConnectTaskV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsInput")
    def topics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsRegexInput")
    def topics_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicsRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationType")
    def destination_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationType"))

    @destination_type.setter
    def destination_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b655442fc520b01329baa13f1563cba240be5d8c54e97934a512861952a2b3a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94b12b088ea21c9357b236112fb9399119ae7a0d8bbe3eca2006f8641ea7caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11d67dd3bef20a11c8a3d9eb4cc5cd2062b8d42d3f9adafd70126da47377518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c34680b37b7d71e78a462beb8d741ffe2e1c3f2aee8bdeb8d65b96d736dabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startLater")
    def start_later(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startLater"))

    @start_later.setter
    def start_later(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fe7e9c554c631987a7c2cf38f41f65d54a077fa2bcaa938eb980533aeddcce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startLater", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskName")
    def task_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskName"))

    @task_name.setter
    def task_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f89ac4d26655b6a229eb031d20fec9e1e63206065cda482688668b1c2f12d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topics"))

    @topics.setter
    def topics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68832ae161ea0449f976b77322b46fd4b3a904df3da4d72f9d2583c9f1fd3054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicsRegex")
    def topics_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicsRegex"))

    @topics_regex.setter
    def topics_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18392a9b9e6cdad0c5c97e8cb3ad62001f2cdfb8859794b15ab3fba272289d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicsRegex", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsSmartConnectTaskV2.DmsSmartConnectTaskV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "instance_id": "instanceId",
        "task_name": "taskName",
        "destination_task": "destinationTask",
        "destination_type": "destinationType",
        "id": "id",
        "source_task": "sourceTask",
        "source_type": "sourceType",
        "start_later": "startLater",
        "timeouts": "timeouts",
        "topics": "topics",
        "topics_regex": "topicsRegex",
    },
)
class DmsSmartConnectTaskV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_id: builtins.str,
        task_name: builtins.str,
        destination_task: typing.Optional[typing.Union["DmsSmartConnectTaskV2DestinationTask", typing.Dict[builtins.str, typing.Any]]] = None,
        destination_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        source_task: typing.Optional[typing.Union["DmsSmartConnectTaskV2SourceTask", typing.Dict[builtins.str, typing.Any]]] = None,
        source_type: typing.Optional[builtins.str] = None,
        start_later: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["DmsSmartConnectTaskV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
        topics_regex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#instance_id DmsSmartConnectTaskV2#instance_id}.
        :param task_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#task_name DmsSmartConnectTaskV2#task_name}.
        :param destination_task: destination_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_task DmsSmartConnectTaskV2#destination_task}
        :param destination_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_type DmsSmartConnectTaskV2#destination_type}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#id DmsSmartConnectTaskV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param source_task: source_task block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#source_task DmsSmartConnectTaskV2#source_task}
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#source_type DmsSmartConnectTaskV2#source_type}.
        :param start_later: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#start_later DmsSmartConnectTaskV2#start_later}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#timeouts DmsSmartConnectTaskV2#timeouts}
        :param topics: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics DmsSmartConnectTaskV2#topics}.
        :param topics_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics_regex DmsSmartConnectTaskV2#topics_regex}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination_task, dict):
            destination_task = DmsSmartConnectTaskV2DestinationTask(**destination_task)
        if isinstance(source_task, dict):
            source_task = DmsSmartConnectTaskV2SourceTask(**source_task)
        if isinstance(timeouts, dict):
            timeouts = DmsSmartConnectTaskV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a570fa5e29b90908d0ce1d7c6019a116ade2bf0838e733c5b6196bd88ce675be)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument task_name", value=task_name, expected_type=type_hints["task_name"])
            check_type(argname="argument destination_task", value=destination_task, expected_type=type_hints["destination_task"])
            check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument source_task", value=source_task, expected_type=type_hints["source_task"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument start_later", value=start_later, expected_type=type_hints["start_later"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument topics_regex", value=topics_regex, expected_type=type_hints["topics_regex"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_id": instance_id,
            "task_name": task_name,
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
        if destination_task is not None:
            self._values["destination_task"] = destination_task
        if destination_type is not None:
            self._values["destination_type"] = destination_type
        if id is not None:
            self._values["id"] = id
        if source_task is not None:
            self._values["source_task"] = source_task
        if source_type is not None:
            self._values["source_type"] = source_type
        if start_later is not None:
            self._values["start_later"] = start_later
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if topics is not None:
            self._values["topics"] = topics
        if topics_regex is not None:
            self._values["topics_regex"] = topics_regex

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
    def instance_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#instance_id DmsSmartConnectTaskV2#instance_id}.'''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#task_name DmsSmartConnectTaskV2#task_name}.'''
        result = self._values.get("task_name")
        assert result is not None, "Required property 'task_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_task(
        self,
    ) -> typing.Optional["DmsSmartConnectTaskV2DestinationTask"]:
        '''destination_task block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_task DmsSmartConnectTaskV2#destination_task}
        '''
        result = self._values.get("destination_task")
        return typing.cast(typing.Optional["DmsSmartConnectTaskV2DestinationTask"], result)

    @builtins.property
    def destination_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_type DmsSmartConnectTaskV2#destination_type}.'''
        result = self._values.get("destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#id DmsSmartConnectTaskV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_task(self) -> typing.Optional["DmsSmartConnectTaskV2SourceTask"]:
        '''source_task block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#source_task DmsSmartConnectTaskV2#source_task}
        '''
        result = self._values.get("source_task")
        return typing.cast(typing.Optional["DmsSmartConnectTaskV2SourceTask"], result)

    @builtins.property
    def source_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#source_type DmsSmartConnectTaskV2#source_type}.'''
        result = self._values.get("source_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_later(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#start_later DmsSmartConnectTaskV2#start_later}.'''
        result = self._values.get("start_later")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DmsSmartConnectTaskV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#timeouts DmsSmartConnectTaskV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DmsSmartConnectTaskV2Timeouts"], result)

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics DmsSmartConnectTaskV2#topics}.'''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def topics_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics_regex DmsSmartConnectTaskV2#topics_regex}.'''
        result = self._values.get("topics_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsSmartConnectTaskV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsSmartConnectTaskV2.DmsSmartConnectTaskV2DestinationTask",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "consumer_strategy": "consumerStrategy",
        "deliver_time_interval": "deliverTimeInterval",
        "destination_file_type": "destinationFileType",
        "obs_bucket_name": "obsBucketName",
        "obs_path": "obsPath",
        "partition_format": "partitionFormat",
        "record_delimiter": "recordDelimiter",
        "secret_key": "secretKey",
        "store_keys": "storeKeys",
    },
)
class DmsSmartConnectTaskV2DestinationTask:
    def __init__(
        self,
        *,
        access_key: typing.Optional[builtins.str] = None,
        consumer_strategy: typing.Optional[builtins.str] = None,
        deliver_time_interval: typing.Optional[jsii.Number] = None,
        destination_file_type: typing.Optional[builtins.str] = None,
        obs_bucket_name: typing.Optional[builtins.str] = None,
        obs_path: typing.Optional[builtins.str] = None,
        partition_format: typing.Optional[builtins.str] = None,
        record_delimiter: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        store_keys: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#access_key DmsSmartConnectTaskV2#access_key}.
        :param consumer_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#consumer_strategy DmsSmartConnectTaskV2#consumer_strategy}.
        :param deliver_time_interval: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#deliver_time_interval DmsSmartConnectTaskV2#deliver_time_interval}.
        :param destination_file_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_file_type DmsSmartConnectTaskV2#destination_file_type}.
        :param obs_bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#obs_bucket_name DmsSmartConnectTaskV2#obs_bucket_name}.
        :param obs_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#obs_path DmsSmartConnectTaskV2#obs_path}.
        :param partition_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#partition_format DmsSmartConnectTaskV2#partition_format}.
        :param record_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#record_delimiter DmsSmartConnectTaskV2#record_delimiter}.
        :param secret_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#secret_key DmsSmartConnectTaskV2#secret_key}.
        :param store_keys: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#store_keys DmsSmartConnectTaskV2#store_keys}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6393742e45367514d39edb30963084ed3f56ddb8af5251b2dc54d291acedc84c)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument consumer_strategy", value=consumer_strategy, expected_type=type_hints["consumer_strategy"])
            check_type(argname="argument deliver_time_interval", value=deliver_time_interval, expected_type=type_hints["deliver_time_interval"])
            check_type(argname="argument destination_file_type", value=destination_file_type, expected_type=type_hints["destination_file_type"])
            check_type(argname="argument obs_bucket_name", value=obs_bucket_name, expected_type=type_hints["obs_bucket_name"])
            check_type(argname="argument obs_path", value=obs_path, expected_type=type_hints["obs_path"])
            check_type(argname="argument partition_format", value=partition_format, expected_type=type_hints["partition_format"])
            check_type(argname="argument record_delimiter", value=record_delimiter, expected_type=type_hints["record_delimiter"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument store_keys", value=store_keys, expected_type=type_hints["store_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_key is not None:
            self._values["access_key"] = access_key
        if consumer_strategy is not None:
            self._values["consumer_strategy"] = consumer_strategy
        if deliver_time_interval is not None:
            self._values["deliver_time_interval"] = deliver_time_interval
        if destination_file_type is not None:
            self._values["destination_file_type"] = destination_file_type
        if obs_bucket_name is not None:
            self._values["obs_bucket_name"] = obs_bucket_name
        if obs_path is not None:
            self._values["obs_path"] = obs_path
        if partition_format is not None:
            self._values["partition_format"] = partition_format
        if record_delimiter is not None:
            self._values["record_delimiter"] = record_delimiter
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if store_keys is not None:
            self._values["store_keys"] = store_keys

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#access_key DmsSmartConnectTaskV2#access_key}.'''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#consumer_strategy DmsSmartConnectTaskV2#consumer_strategy}.'''
        result = self._values.get("consumer_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deliver_time_interval(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#deliver_time_interval DmsSmartConnectTaskV2#deliver_time_interval}.'''
        result = self._values.get("deliver_time_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def destination_file_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#destination_file_type DmsSmartConnectTaskV2#destination_file_type}.'''
        result = self._values.get("destination_file_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#obs_bucket_name DmsSmartConnectTaskV2#obs_bucket_name}.'''
        result = self._values.get("obs_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def obs_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#obs_path DmsSmartConnectTaskV2#obs_path}.'''
        result = self._values.get("obs_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#partition_format DmsSmartConnectTaskV2#partition_format}.'''
        result = self._values.get("partition_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def record_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#record_delimiter DmsSmartConnectTaskV2#record_delimiter}.'''
        result = self._values.get("record_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#secret_key DmsSmartConnectTaskV2#secret_key}.'''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def store_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#store_keys DmsSmartConnectTaskV2#store_keys}.'''
        result = self._values.get("store_keys")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsSmartConnectTaskV2DestinationTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsSmartConnectTaskV2DestinationTaskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsSmartConnectTaskV2.DmsSmartConnectTaskV2DestinationTaskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8904009489cecdcdfba5c17cdb0dafa78f170e4be0b5aac06cf9870af820623a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccessKey")
    def reset_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessKey", []))

    @jsii.member(jsii_name="resetConsumerStrategy")
    def reset_consumer_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerStrategy", []))

    @jsii.member(jsii_name="resetDeliverTimeInterval")
    def reset_deliver_time_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliverTimeInterval", []))

    @jsii.member(jsii_name="resetDestinationFileType")
    def reset_destination_file_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinationFileType", []))

    @jsii.member(jsii_name="resetObsBucketName")
    def reset_obs_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsBucketName", []))

    @jsii.member(jsii_name="resetObsPath")
    def reset_obs_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetObsPath", []))

    @jsii.member(jsii_name="resetPartitionFormat")
    def reset_partition_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionFormat", []))

    @jsii.member(jsii_name="resetRecordDelimiter")
    def reset_record_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordDelimiter", []))

    @jsii.member(jsii_name="resetSecretKey")
    def reset_secret_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKey", []))

    @jsii.member(jsii_name="resetStoreKeys")
    def reset_store_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStoreKeys", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerStrategyInput")
    def consumer_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="deliverTimeIntervalInput")
    def deliver_time_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deliverTimeIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationFileTypeInput")
    def destination_file_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationFileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="obsBucketNameInput")
    def obs_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsBucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="obsPathInput")
    def obs_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "obsPathInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionFormatInput")
    def partition_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partitionFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="recordDelimiterInput")
    def record_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storeKeysInput")
    def store_keys_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storeKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb3b3b034c66492c87e805ed732a7ab7a61919eefcf497048c39e8a989ec004c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerStrategy")
    def consumer_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerStrategy"))

    @consumer_strategy.setter
    def consumer_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61f4e63485a8955a9ed04be5333fb697c3e2a1542685681435c4f0c4d1c9921d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deliverTimeInterval")
    def deliver_time_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "deliverTimeInterval"))

    @deliver_time_interval.setter
    def deliver_time_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a06f40c9fa6bc36bf12f4c44ba5c9fe54e991505d1c5a33536edaf070739db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliverTimeInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="destinationFileType")
    def destination_file_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationFileType"))

    @destination_file_type.setter
    def destination_file_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2949c6e58e5821920403b143dd3ba17430ed5777e79bcd7e0d311634cab2851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationFileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsBucketName")
    def obs_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsBucketName"))

    @obs_bucket_name.setter
    def obs_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acbd6ce5949798c8c51a70d20e72552f80729b7d8c496bb9a016e5c36ef94750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsBucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="obsPath")
    def obs_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "obsPath"))

    @obs_path.setter
    def obs_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49bee74eb837aaf691dbdd68883ba2078aef0605ab3b5ecfcace449f6d18ba24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "obsPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partitionFormat")
    def partition_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "partitionFormat"))

    @partition_format.setter
    def partition_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd89dd4e2ddc92fc80d1bf313bf8e5951c9ccff754ee2f3b265c19106dccc23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partitionFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recordDelimiter")
    def record_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recordDelimiter"))

    @record_delimiter.setter
    def record_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb27d9b658ac11c8a816597f740b415bb63fc947649f6c15318d8913dee6d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799313c59b809f5692ee2f57c56d05e63e8f4e6428e41dbbbcf0bbcc23ec7b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storeKeys")
    def store_keys(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "storeKeys"))

    @store_keys.setter
    def store_keys(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c271fe7c262b81fc7e1ad51aa40c6a6e4945167125705d3b3e2bd1e52a1de062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsSmartConnectTaskV2DestinationTask]:
        return typing.cast(typing.Optional[DmsSmartConnectTaskV2DestinationTask], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DmsSmartConnectTaskV2DestinationTask],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d983ee759c54e0994c18eb49e62c9611b284abd2e877445523d18b37a985c5ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsSmartConnectTaskV2.DmsSmartConnectTaskV2SourceTask",
    jsii_struct_bases=[],
    name_mapping={
        "compression_type": "compressionType",
        "consumer_strategy": "consumerStrategy",
        "current_instance_alias": "currentInstanceAlias",
        "direction": "direction",
        "password": "password",
        "peer_instance_address": "peerInstanceAddress",
        "peer_instance_alias": "peerInstanceAlias",
        "peer_instance_id": "peerInstanceId",
        "provenance_header_enabled": "provenanceHeaderEnabled",
        "rename_topic_enabled": "renameTopicEnabled",
        "replication_factor": "replicationFactor",
        "sasl_mechanism": "saslMechanism",
        "security_protocol": "securityProtocol",
        "sync_consumer_offsets_enabled": "syncConsumerOffsetsEnabled",
        "task_num": "taskNum",
        "topics_mapping": "topicsMapping",
        "user_name": "userName",
    },
)
class DmsSmartConnectTaskV2SourceTask:
    def __init__(
        self,
        *,
        compression_type: typing.Optional[builtins.str] = None,
        consumer_strategy: typing.Optional[builtins.str] = None,
        current_instance_alias: typing.Optional[builtins.str] = None,
        direction: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        peer_instance_address: typing.Optional[typing.Sequence[builtins.str]] = None,
        peer_instance_alias: typing.Optional[builtins.str] = None,
        peer_instance_id: typing.Optional[builtins.str] = None,
        provenance_header_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rename_topic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
        sasl_mechanism: typing.Optional[builtins.str] = None,
        security_protocol: typing.Optional[builtins.str] = None,
        sync_consumer_offsets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        task_num: typing.Optional[jsii.Number] = None,
        topics_mapping: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compression_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#compression_type DmsSmartConnectTaskV2#compression_type}.
        :param consumer_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#consumer_strategy DmsSmartConnectTaskV2#consumer_strategy}.
        :param current_instance_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#current_instance_alias DmsSmartConnectTaskV2#current_instance_alias}.
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#direction DmsSmartConnectTaskV2#direction}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#password DmsSmartConnectTaskV2#password}.
        :param peer_instance_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_address DmsSmartConnectTaskV2#peer_instance_address}.
        :param peer_instance_alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_alias DmsSmartConnectTaskV2#peer_instance_alias}.
        :param peer_instance_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_id DmsSmartConnectTaskV2#peer_instance_id}.
        :param provenance_header_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#provenance_header_enabled DmsSmartConnectTaskV2#provenance_header_enabled}.
        :param rename_topic_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#rename_topic_enabled DmsSmartConnectTaskV2#rename_topic_enabled}.
        :param replication_factor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#replication_factor DmsSmartConnectTaskV2#replication_factor}.
        :param sasl_mechanism: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#sasl_mechanism DmsSmartConnectTaskV2#sasl_mechanism}.
        :param security_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#security_protocol DmsSmartConnectTaskV2#security_protocol}.
        :param sync_consumer_offsets_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#sync_consumer_offsets_enabled DmsSmartConnectTaskV2#sync_consumer_offsets_enabled}.
        :param task_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#task_num DmsSmartConnectTaskV2#task_num}.
        :param topics_mapping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics_mapping DmsSmartConnectTaskV2#topics_mapping}.
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#user_name DmsSmartConnectTaskV2#user_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3046a7675ef2bcb1112116f67b2ec91e55fdf256288239c3c701419a5dbf4c4a)
            check_type(argname="argument compression_type", value=compression_type, expected_type=type_hints["compression_type"])
            check_type(argname="argument consumer_strategy", value=consumer_strategy, expected_type=type_hints["consumer_strategy"])
            check_type(argname="argument current_instance_alias", value=current_instance_alias, expected_type=type_hints["current_instance_alias"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument peer_instance_address", value=peer_instance_address, expected_type=type_hints["peer_instance_address"])
            check_type(argname="argument peer_instance_alias", value=peer_instance_alias, expected_type=type_hints["peer_instance_alias"])
            check_type(argname="argument peer_instance_id", value=peer_instance_id, expected_type=type_hints["peer_instance_id"])
            check_type(argname="argument provenance_header_enabled", value=provenance_header_enabled, expected_type=type_hints["provenance_header_enabled"])
            check_type(argname="argument rename_topic_enabled", value=rename_topic_enabled, expected_type=type_hints["rename_topic_enabled"])
            check_type(argname="argument replication_factor", value=replication_factor, expected_type=type_hints["replication_factor"])
            check_type(argname="argument sasl_mechanism", value=sasl_mechanism, expected_type=type_hints["sasl_mechanism"])
            check_type(argname="argument security_protocol", value=security_protocol, expected_type=type_hints["security_protocol"])
            check_type(argname="argument sync_consumer_offsets_enabled", value=sync_consumer_offsets_enabled, expected_type=type_hints["sync_consumer_offsets_enabled"])
            check_type(argname="argument task_num", value=task_num, expected_type=type_hints["task_num"])
            check_type(argname="argument topics_mapping", value=topics_mapping, expected_type=type_hints["topics_mapping"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compression_type is not None:
            self._values["compression_type"] = compression_type
        if consumer_strategy is not None:
            self._values["consumer_strategy"] = consumer_strategy
        if current_instance_alias is not None:
            self._values["current_instance_alias"] = current_instance_alias
        if direction is not None:
            self._values["direction"] = direction
        if password is not None:
            self._values["password"] = password
        if peer_instance_address is not None:
            self._values["peer_instance_address"] = peer_instance_address
        if peer_instance_alias is not None:
            self._values["peer_instance_alias"] = peer_instance_alias
        if peer_instance_id is not None:
            self._values["peer_instance_id"] = peer_instance_id
        if provenance_header_enabled is not None:
            self._values["provenance_header_enabled"] = provenance_header_enabled
        if rename_topic_enabled is not None:
            self._values["rename_topic_enabled"] = rename_topic_enabled
        if replication_factor is not None:
            self._values["replication_factor"] = replication_factor
        if sasl_mechanism is not None:
            self._values["sasl_mechanism"] = sasl_mechanism
        if security_protocol is not None:
            self._values["security_protocol"] = security_protocol
        if sync_consumer_offsets_enabled is not None:
            self._values["sync_consumer_offsets_enabled"] = sync_consumer_offsets_enabled
        if task_num is not None:
            self._values["task_num"] = task_num
        if topics_mapping is not None:
            self._values["topics_mapping"] = topics_mapping
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def compression_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#compression_type DmsSmartConnectTaskV2#compression_type}.'''
        result = self._values.get("compression_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_strategy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#consumer_strategy DmsSmartConnectTaskV2#consumer_strategy}.'''
        result = self._values.get("consumer_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def current_instance_alias(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#current_instance_alias DmsSmartConnectTaskV2#current_instance_alias}.'''
        result = self._values.get("current_instance_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direction(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#direction DmsSmartConnectTaskV2#direction}.'''
        result = self._values.get("direction")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#password DmsSmartConnectTaskV2#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_instance_address(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_address DmsSmartConnectTaskV2#peer_instance_address}.'''
        result = self._values.get("peer_instance_address")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def peer_instance_alias(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_alias DmsSmartConnectTaskV2#peer_instance_alias}.'''
        result = self._values.get("peer_instance_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_instance_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#peer_instance_id DmsSmartConnectTaskV2#peer_instance_id}.'''
        result = self._values.get("peer_instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provenance_header_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#provenance_header_enabled DmsSmartConnectTaskV2#provenance_header_enabled}.'''
        result = self._values.get("provenance_header_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rename_topic_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#rename_topic_enabled DmsSmartConnectTaskV2#rename_topic_enabled}.'''
        result = self._values.get("rename_topic_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replication_factor(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#replication_factor DmsSmartConnectTaskV2#replication_factor}.'''
        result = self._values.get("replication_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sasl_mechanism(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#sasl_mechanism DmsSmartConnectTaskV2#sasl_mechanism}.'''
        result = self._values.get("sasl_mechanism")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#security_protocol DmsSmartConnectTaskV2#security_protocol}.'''
        result = self._values.get("security_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_consumer_offsets_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#sync_consumer_offsets_enabled DmsSmartConnectTaskV2#sync_consumer_offsets_enabled}.'''
        result = self._values.get("sync_consumer_offsets_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def task_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#task_num DmsSmartConnectTaskV2#task_num}.'''
        result = self._values.get("task_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def topics_mapping(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#topics_mapping DmsSmartConnectTaskV2#topics_mapping}.'''
        result = self._values.get("topics_mapping")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#user_name DmsSmartConnectTaskV2#user_name}.'''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsSmartConnectTaskV2SourceTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsSmartConnectTaskV2SourceTaskOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsSmartConnectTaskV2.DmsSmartConnectTaskV2SourceTaskOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__577b08d6b0079ecbf3779de36b431cc7e5b7fa60b8e967e7c453ee412bf259ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCompressionType")
    def reset_compression_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompressionType", []))

    @jsii.member(jsii_name="resetConsumerStrategy")
    def reset_consumer_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerStrategy", []))

    @jsii.member(jsii_name="resetCurrentInstanceAlias")
    def reset_current_instance_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCurrentInstanceAlias", []))

    @jsii.member(jsii_name="resetDirection")
    def reset_direction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirection", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPeerInstanceAddress")
    def reset_peer_instance_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerInstanceAddress", []))

    @jsii.member(jsii_name="resetPeerInstanceAlias")
    def reset_peer_instance_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerInstanceAlias", []))

    @jsii.member(jsii_name="resetPeerInstanceId")
    def reset_peer_instance_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerInstanceId", []))

    @jsii.member(jsii_name="resetProvenanceHeaderEnabled")
    def reset_provenance_header_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProvenanceHeaderEnabled", []))

    @jsii.member(jsii_name="resetRenameTopicEnabled")
    def reset_rename_topic_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenameTopicEnabled", []))

    @jsii.member(jsii_name="resetReplicationFactor")
    def reset_replication_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationFactor", []))

    @jsii.member(jsii_name="resetSaslMechanism")
    def reset_sasl_mechanism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSaslMechanism", []))

    @jsii.member(jsii_name="resetSecurityProtocol")
    def reset_security_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityProtocol", []))

    @jsii.member(jsii_name="resetSyncConsumerOffsetsEnabled")
    def reset_sync_consumer_offsets_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncConsumerOffsetsEnabled", []))

    @jsii.member(jsii_name="resetTaskNum")
    def reset_task_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskNum", []))

    @jsii.member(jsii_name="resetTopicsMapping")
    def reset_topics_mapping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTopicsMapping", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

    @builtins.property
    @jsii.member(jsii_name="compressionTypeInput")
    def compression_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerStrategyInput")
    def consumer_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="currentInstanceAliasInput")
    def current_instance_alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentInstanceAliasInput"))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="peerInstanceAddressInput")
    def peer_instance_address_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "peerInstanceAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="peerInstanceAliasInput")
    def peer_instance_alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerInstanceAliasInput"))

    @builtins.property
    @jsii.member(jsii_name="peerInstanceIdInput")
    def peer_instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerInstanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="provenanceHeaderEnabledInput")
    def provenance_header_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "provenanceHeaderEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="renameTopicEnabledInput")
    def rename_topic_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "renameTopicEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationFactorInput")
    def replication_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicationFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="saslMechanismInput")
    def sasl_mechanism_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "saslMechanismInput"))

    @builtins.property
    @jsii.member(jsii_name="securityProtocolInput")
    def security_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="syncConsumerOffsetsEnabledInput")
    def sync_consumer_offsets_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncConsumerOffsetsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="taskNumInput")
    def task_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "taskNumInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsMappingInput")
    def topics_mapping_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "topicsMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionType")
    def compression_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compressionType"))

    @compression_type.setter
    def compression_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10a8610a49516bc10f65ac4c1e0f1c8e760466421aa301d09633a7c22e96aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compressionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerStrategy")
    def consumer_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerStrategy"))

    @consumer_strategy.setter
    def consumer_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46dd725c79afc47c4c88212d5673f0e321abf7520689028e4fdd41d29f7a3e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="currentInstanceAlias")
    def current_instance_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "currentInstanceAlias"))

    @current_instance_alias.setter
    def current_instance_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e46b08b82877a901c0dda3d2bb2acf6f607fe914a8633a5f6d37da25c75819)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currentInstanceAlias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ff9512261254c8587484b93dfa2092eeb9bab415032426313502f7465f1636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e2667c1639e08cf341579676f73c6a1b84265b3ebe25ae728caf1992c952eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerInstanceAddress")
    def peer_instance_address(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "peerInstanceAddress"))

    @peer_instance_address.setter
    def peer_instance_address(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8551dbf443f6e7ff8f8e10380b8562817d75fec2faeedf8d165a3ce2dfeff932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerInstanceAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerInstanceAlias")
    def peer_instance_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerInstanceAlias"))

    @peer_instance_alias.setter
    def peer_instance_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__becd0f07cd3b9bd058b7abd7a370a69a1093df036ffbc0bbd880010ca62f144c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerInstanceAlias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peerInstanceId")
    def peer_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerInstanceId"))

    @peer_instance_id.setter
    def peer_instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242fad0b3ec42a3a10ab7714e447354e1bfcbb76013c4a977fe3c1c08538b1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerInstanceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provenanceHeaderEnabled")
    def provenance_header_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "provenanceHeaderEnabled"))

    @provenance_header_enabled.setter
    def provenance_header_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6175f5a9b1eb35896d14218c26ca585cdeab59c9ba83d3ea056d6389ae196bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provenanceHeaderEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renameTopicEnabled")
    def rename_topic_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "renameTopicEnabled"))

    @rename_topic_enabled.setter
    def rename_topic_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8210fc5ddf2270028b9eb777c2416446da5042003009962b7c13b4ffc57fafc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renameTopicEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationFactor")
    def replication_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicationFactor"))

    @replication_factor.setter
    def replication_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31bae94306a7bbbfd0e6371337928279e405cd741fdc87b0bb318a35268c028)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationFactor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="saslMechanism")
    def sasl_mechanism(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saslMechanism"))

    @sasl_mechanism.setter
    def sasl_mechanism(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098e5a047ac954716580193d6acfb07d7005a0151ec1b26a4017e64b3fc4bbd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "saslMechanism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityProtocol")
    def security_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityProtocol"))

    @security_protocol.setter
    def security_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d685028829e2fb0afdb9ef863b77dfd5eeef6906101e3e6bdf5312761449bc8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncConsumerOffsetsEnabled")
    def sync_consumer_offsets_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncConsumerOffsetsEnabled"))

    @sync_consumer_offsets_enabled.setter
    def sync_consumer_offsets_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c71197ef083fbe8861aa950dbf936f297e55b0155eb511fcc908a9f8a811281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncConsumerOffsetsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskNum")
    def task_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskNum"))

    @task_num.setter
    def task_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5cdaa9f69309eb7ff2c2e8c9c93f20adf5d26d08719e20ca33f949667b2c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicsMapping")
    def topics_mapping(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "topicsMapping"))

    @topics_mapping.setter
    def topics_mapping(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c019b31f12d3728ed5958559673a76d6139eda35c4aa02ae9418a2e8444443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicsMapping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2bbf51c75c81df024597a71eda764e528688a5511e9f8d06f1bda7e06bec211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DmsSmartConnectTaskV2SourceTask]:
        return typing.cast(typing.Optional[DmsSmartConnectTaskV2SourceTask], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DmsSmartConnectTaskV2SourceTask],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc3a97c1bf4bec0779f655a185b06ff01858c3b32e966069018a02b5b62973b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dmsSmartConnectTaskV2.DmsSmartConnectTaskV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create"},
)
class DmsSmartConnectTaskV2Timeouts:
    def __init__(self, *, create: typing.Optional[builtins.str] = None) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#create DmsSmartConnectTaskV2#create}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f75db80e42abc79fcfa4c2e0663ac39491a863d66ac18e6fd78914551a4fe5d)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dms_smart_connect_task_v2#create DmsSmartConnectTaskV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DmsSmartConnectTaskV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DmsSmartConnectTaskV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dmsSmartConnectTaskV2.DmsSmartConnectTaskV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66eb860cc0c5430f5dfadcb2325bc855f0395d9eb2edc3d481aa6da0e7faa97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65255ac8bdb8b09d0d93dcb2daa2ff6eff3fc7e524b31b2fcfa72caf3132ca8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsSmartConnectTaskV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsSmartConnectTaskV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsSmartConnectTaskV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c31b11c0d4761a0a25be6bd0c658c760fecba581159d86c54dc55629655d7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DmsSmartConnectTaskV2",
    "DmsSmartConnectTaskV2Config",
    "DmsSmartConnectTaskV2DestinationTask",
    "DmsSmartConnectTaskV2DestinationTaskOutputReference",
    "DmsSmartConnectTaskV2SourceTask",
    "DmsSmartConnectTaskV2SourceTaskOutputReference",
    "DmsSmartConnectTaskV2Timeouts",
    "DmsSmartConnectTaskV2TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2c94869d135426693524f66c555cdeb988bfcc59763380a45bd378d70f9d88c4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    instance_id: builtins.str,
    task_name: builtins.str,
    destination_task: typing.Optional[typing.Union[DmsSmartConnectTaskV2DestinationTask, typing.Dict[builtins.str, typing.Any]]] = None,
    destination_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    source_task: typing.Optional[typing.Union[DmsSmartConnectTaskV2SourceTask, typing.Dict[builtins.str, typing.Any]]] = None,
    source_type: typing.Optional[builtins.str] = None,
    start_later: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[DmsSmartConnectTaskV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    topics_regex: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__618580678454e1e43eedd5707713dd688c013a2b7a5f7d9fe9d82b419c532310(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b655442fc520b01329baa13f1563cba240be5d8c54e97934a512861952a2b3a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94b12b088ea21c9357b236112fb9399119ae7a0d8bbe3eca2006f8641ea7caf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11d67dd3bef20a11c8a3d9eb4cc5cd2062b8d42d3f9adafd70126da47377518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c34680b37b7d71e78a462beb8d741ffe2e1c3f2aee8bdeb8d65b96d736dabe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fe7e9c554c631987a7c2cf38f41f65d54a077fa2bcaa938eb980533aeddcce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f89ac4d26655b6a229eb031d20fec9e1e63206065cda482688668b1c2f12d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68832ae161ea0449f976b77322b46fd4b3a904df3da4d72f9d2583c9f1fd3054(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18392a9b9e6cdad0c5c97e8cb3ad62001f2cdfb8859794b15ab3fba272289d11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a570fa5e29b90908d0ce1d7c6019a116ade2bf0838e733c5b6196bd88ce675be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    instance_id: builtins.str,
    task_name: builtins.str,
    destination_task: typing.Optional[typing.Union[DmsSmartConnectTaskV2DestinationTask, typing.Dict[builtins.str, typing.Any]]] = None,
    destination_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    source_task: typing.Optional[typing.Union[DmsSmartConnectTaskV2SourceTask, typing.Dict[builtins.str, typing.Any]]] = None,
    source_type: typing.Optional[builtins.str] = None,
    start_later: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[DmsSmartConnectTaskV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    topics_regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6393742e45367514d39edb30963084ed3f56ddb8af5251b2dc54d291acedc84c(
    *,
    access_key: typing.Optional[builtins.str] = None,
    consumer_strategy: typing.Optional[builtins.str] = None,
    deliver_time_interval: typing.Optional[jsii.Number] = None,
    destination_file_type: typing.Optional[builtins.str] = None,
    obs_bucket_name: typing.Optional[builtins.str] = None,
    obs_path: typing.Optional[builtins.str] = None,
    partition_format: typing.Optional[builtins.str] = None,
    record_delimiter: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    store_keys: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8904009489cecdcdfba5c17cdb0dafa78f170e4be0b5aac06cf9870af820623a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3b3b034c66492c87e805ed732a7ab7a61919eefcf497048c39e8a989ec004c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f4e63485a8955a9ed04be5333fb697c3e2a1542685681435c4f0c4d1c9921d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a06f40c9fa6bc36bf12f4c44ba5c9fe54e991505d1c5a33536edaf070739db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2949c6e58e5821920403b143dd3ba17430ed5777e79bcd7e0d311634cab2851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acbd6ce5949798c8c51a70d20e72552f80729b7d8c496bb9a016e5c36ef94750(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49bee74eb837aaf691dbdd68883ba2078aef0605ab3b5ecfcace449f6d18ba24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd89dd4e2ddc92fc80d1bf313bf8e5951c9ccff754ee2f3b265c19106dccc23a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb27d9b658ac11c8a816597f740b415bb63fc947649f6c15318d8913dee6d56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799313c59b809f5692ee2f57c56d05e63e8f4e6428e41dbbbcf0bbcc23ec7b2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c271fe7c262b81fc7e1ad51aa40c6a6e4945167125705d3b3e2bd1e52a1de062(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d983ee759c54e0994c18eb49e62c9611b284abd2e877445523d18b37a985c5ae(
    value: typing.Optional[DmsSmartConnectTaskV2DestinationTask],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3046a7675ef2bcb1112116f67b2ec91e55fdf256288239c3c701419a5dbf4c4a(
    *,
    compression_type: typing.Optional[builtins.str] = None,
    consumer_strategy: typing.Optional[builtins.str] = None,
    current_instance_alias: typing.Optional[builtins.str] = None,
    direction: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    peer_instance_address: typing.Optional[typing.Sequence[builtins.str]] = None,
    peer_instance_alias: typing.Optional[builtins.str] = None,
    peer_instance_id: typing.Optional[builtins.str] = None,
    provenance_header_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rename_topic_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replication_factor: typing.Optional[jsii.Number] = None,
    sasl_mechanism: typing.Optional[builtins.str] = None,
    security_protocol: typing.Optional[builtins.str] = None,
    sync_consumer_offsets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    task_num: typing.Optional[jsii.Number] = None,
    topics_mapping: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577b08d6b0079ecbf3779de36b431cc7e5b7fa60b8e967e7c453ee412bf259ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10a8610a49516bc10f65ac4c1e0f1c8e760466421aa301d09633a7c22e96aa5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46dd725c79afc47c4c88212d5673f0e321abf7520689028e4fdd41d29f7a3e01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e46b08b82877a901c0dda3d2bb2acf6f607fe914a8633a5f6d37da25c75819(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ff9512261254c8587484b93dfa2092eeb9bab415032426313502f7465f1636(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e2667c1639e08cf341579676f73c6a1b84265b3ebe25ae728caf1992c952eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8551dbf443f6e7ff8f8e10380b8562817d75fec2faeedf8d165a3ce2dfeff932(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__becd0f07cd3b9bd058b7abd7a370a69a1093df036ffbc0bbd880010ca62f144c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242fad0b3ec42a3a10ab7714e447354e1bfcbb76013c4a977fe3c1c08538b1ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6175f5a9b1eb35896d14218c26ca585cdeab59c9ba83d3ea056d6389ae196bf2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8210fc5ddf2270028b9eb777c2416446da5042003009962b7c13b4ffc57fafc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31bae94306a7bbbfd0e6371337928279e405cd741fdc87b0bb318a35268c028(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098e5a047ac954716580193d6acfb07d7005a0151ec1b26a4017e64b3fc4bbd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d685028829e2fb0afdb9ef863b77dfd5eeef6906101e3e6bdf5312761449bc8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c71197ef083fbe8861aa950dbf936f297e55b0155eb511fcc908a9f8a811281(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5cdaa9f69309eb7ff2c2e8c9c93f20adf5d26d08719e20ca33f949667b2c50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c019b31f12d3728ed5958559673a76d6139eda35c4aa02ae9418a2e8444443(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bbf51c75c81df024597a71eda764e528688a5511e9f8d06f1bda7e06bec211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc3a97c1bf4bec0779f655a185b06ff01858c3b32e966069018a02b5b62973b(
    value: typing.Optional[DmsSmartConnectTaskV2SourceTask],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f75db80e42abc79fcfa4c2e0663ac39491a863d66ac18e6fd78914551a4fe5d(
    *,
    create: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66eb860cc0c5430f5dfadcb2325bc855f0395d9eb2edc3d481aa6da0e7faa97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65255ac8bdb8b09d0d93dcb2daa2ff6eff3fc7e524b31b2fcfa72caf3132ca8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c31b11c0d4761a0a25be6bd0c658c760fecba581159d86c54dc55629655d7b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DmsSmartConnectTaskV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
