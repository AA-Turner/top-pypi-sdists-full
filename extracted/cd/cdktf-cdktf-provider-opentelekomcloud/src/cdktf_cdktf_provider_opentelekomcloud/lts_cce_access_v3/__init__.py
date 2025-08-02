r'''
# `opentelekomcloud_lts_cce_access_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_lts_cce_access_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3).
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


class LtsCceAccessV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCceAccessV3.LtsCceAccessV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3 opentelekomcloud_lts_cce_access_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        access_config: typing.Union["LtsCceAccessV3AccessConfig", typing.Dict[builtins.str, typing.Any]],
        cluster_id: builtins.str,
        log_group_id: builtins.str,
        log_stream_id: builtins.str,
        name: builtins.str,
        binary_collect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        log_split: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3 opentelekomcloud_lts_cce_access_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#access_config LtsCceAccessV3#access_config}
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#cluster_id LtsCceAccessV3#cluster_id}.
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_group_id LtsCceAccessV3#log_group_id}.
        :param log_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_stream_id LtsCceAccessV3#log_stream_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#name LtsCceAccessV3#name}.
        :param binary_collect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#binary_collect LtsCceAccessV3#binary_collect}.
        :param host_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#host_group_ids LtsCceAccessV3#host_group_ids}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#id LtsCceAccessV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_split: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_split LtsCceAccessV3#log_split}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#tags LtsCceAccessV3#tags}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04d6d041238d2b52a034d0b84597058a34c8ba87da6e5f9a383021b336cf53a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LtsCceAccessV3Config(
            access_config=access_config,
            cluster_id=cluster_id,
            log_group_id=log_group_id,
            log_stream_id=log_stream_id,
            name=name,
            binary_collect=binary_collect,
            host_group_ids=host_group_ids,
            id=id,
            log_split=log_split,
            tags=tags,
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
        '''Generates CDKTF code for importing a LtsCceAccessV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LtsCceAccessV3 to import.
        :param import_from_id: The id of the existing LtsCceAccessV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LtsCceAccessV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfd3402b6aa9a6167ecca0b00e5c1112403c637761aa18afb9e7028ee57b097)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAccessConfig")
    def put_access_config(
        self,
        *,
        path_type: builtins.str,
        black_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_name_regex: typing.Optional[builtins.str] = None,
        exclude_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        exclude_k8_s_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        exclude_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        include_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        include_k8_s_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        include_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_k8_s: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        multi_log_format: typing.Optional[typing.Union["LtsCceAccessV3AccessConfigMultiLogFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        name_space_regex: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        pod_name_regex: typing.Optional[builtins.str] = None,
        single_log_format: typing.Optional[typing.Union["LtsCceAccessV3AccessConfigSingleLogFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        stderr: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stdout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#path_type LtsCceAccessV3#path_type}.
        :param black_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#black_paths LtsCceAccessV3#black_paths}.
        :param container_name_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#container_name_regex LtsCceAccessV3#container_name_regex}.
        :param exclude_envs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_envs LtsCceAccessV3#exclude_envs}.
        :param exclude_k8_s_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_k8s_labels LtsCceAccessV3#exclude_k8s_labels}.
        :param exclude_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_labels LtsCceAccessV3#exclude_labels}.
        :param include_envs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_envs LtsCceAccessV3#include_envs}.
        :param include_k8_s_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_k8s_labels LtsCceAccessV3#include_k8s_labels}.
        :param include_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_labels LtsCceAccessV3#include_labels}.
        :param log_envs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_envs LtsCceAccessV3#log_envs}.
        :param log_k8_s: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_k8s LtsCceAccessV3#log_k8s}.
        :param log_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_labels LtsCceAccessV3#log_labels}.
        :param multi_log_format: multi_log_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#multi_log_format LtsCceAccessV3#multi_log_format}
        :param name_space_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#name_space_regex LtsCceAccessV3#name_space_regex}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#paths LtsCceAccessV3#paths}.
        :param pod_name_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#pod_name_regex LtsCceAccessV3#pod_name_regex}.
        :param single_log_format: single_log_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#single_log_format LtsCceAccessV3#single_log_format}
        :param stderr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#stderr LtsCceAccessV3#stderr}.
        :param stdout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#stdout LtsCceAccessV3#stdout}.
        '''
        value = LtsCceAccessV3AccessConfig(
            path_type=path_type,
            black_paths=black_paths,
            container_name_regex=container_name_regex,
            exclude_envs=exclude_envs,
            exclude_k8_s_labels=exclude_k8_s_labels,
            exclude_labels=exclude_labels,
            include_envs=include_envs,
            include_k8_s_labels=include_k8_s_labels,
            include_labels=include_labels,
            log_envs=log_envs,
            log_k8_s=log_k8_s,
            log_labels=log_labels,
            multi_log_format=multi_log_format,
            name_space_regex=name_space_regex,
            paths=paths,
            pod_name_regex=pod_name_regex,
            single_log_format=single_log_format,
            stderr=stderr,
            stdout=stdout,
        )

        return typing.cast(None, jsii.invoke(self, "putAccessConfig", [value]))

    @jsii.member(jsii_name="resetBinaryCollect")
    def reset_binary_collect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryCollect", []))

    @jsii.member(jsii_name="resetHostGroupIds")
    def reset_host_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostGroupIds", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogSplit")
    def reset_log_split(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogSplit", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="accessConfig")
    def access_config(self) -> "LtsCceAccessV3AccessConfigOutputReference":
        return typing.cast("LtsCceAccessV3AccessConfigOutputReference", jsii.get(self, "accessConfig"))

    @builtins.property
    @jsii.member(jsii_name="accessType")
    def access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessType"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamName"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="accessConfigInput")
    def access_config_input(self) -> typing.Optional["LtsCceAccessV3AccessConfig"]:
        return typing.cast(typing.Optional["LtsCceAccessV3AccessConfig"], jsii.get(self, "accessConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryCollectInput")
    def binary_collect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "binaryCollectInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostGroupIdsInput")
    def host_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupIdInput")
    def log_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logSplitInput")
    def log_split_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logSplitInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamIdInput")
    def log_stream_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryCollect")
    def binary_collect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "binaryCollect"))

    @binary_collect.setter
    def binary_collect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790c3a0af29986211a6c6a8cbb7d4d9734a0ad25dce2c04a007a1b191e22cbee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryCollect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83183063cb471ccf0ac55fb99eed158adb654a89e936b11cca6c188ec289dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostGroupIds")
    def host_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostGroupIds"))

    @host_group_ids.setter
    def host_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd3041787d85e6671532f34e978d905d29704a06b859fef5ff59823a67d71a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba90a364767faa61fa8cbbe2a1f13fff703af413917a494c0d7bcbcc5a041360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupId")
    def log_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupId"))

    @log_group_id.setter
    def log_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47befd5fd6c5840dd900af51bc954fb802879b5e4e51cf348fd6813a63015dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logSplit")
    def log_split(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logSplit"))

    @log_split.setter
    def log_split(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4f7e485c6ebd8a8250fa281355f977d88c0db86dc2a35c082d110fea8f6aa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logSplit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamId")
    def log_stream_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamId"))

    @log_stream_id.setter
    def log_stream_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07648ce7545b85ad5d96e129b845a08c7e6d039a4418810136d1f6f986adcd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce700488c46912eedf32fb92c7321614be425b93010fa5c9702afb3cafa9e6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc10500c9d2852e10bd062a2089a36ec2bb9634302412818039212ba70bbfce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCceAccessV3.LtsCceAccessV3AccessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "path_type": "pathType",
        "black_paths": "blackPaths",
        "container_name_regex": "containerNameRegex",
        "exclude_envs": "excludeEnvs",
        "exclude_k8_s_labels": "excludeK8SLabels",
        "exclude_labels": "excludeLabels",
        "include_envs": "includeEnvs",
        "include_k8_s_labels": "includeK8SLabels",
        "include_labels": "includeLabels",
        "log_envs": "logEnvs",
        "log_k8_s": "logK8S",
        "log_labels": "logLabels",
        "multi_log_format": "multiLogFormat",
        "name_space_regex": "nameSpaceRegex",
        "paths": "paths",
        "pod_name_regex": "podNameRegex",
        "single_log_format": "singleLogFormat",
        "stderr": "stderr",
        "stdout": "stdout",
    },
)
class LtsCceAccessV3AccessConfig:
    def __init__(
        self,
        *,
        path_type: builtins.str,
        black_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        container_name_regex: typing.Optional[builtins.str] = None,
        exclude_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        exclude_k8_s_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        exclude_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        include_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        include_k8_s_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        include_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_k8_s: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        multi_log_format: typing.Optional[typing.Union["LtsCceAccessV3AccessConfigMultiLogFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        name_space_regex: typing.Optional[builtins.str] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        pod_name_regex: typing.Optional[builtins.str] = None,
        single_log_format: typing.Optional[typing.Union["LtsCceAccessV3AccessConfigSingleLogFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        stderr: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        stdout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#path_type LtsCceAccessV3#path_type}.
        :param black_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#black_paths LtsCceAccessV3#black_paths}.
        :param container_name_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#container_name_regex LtsCceAccessV3#container_name_regex}.
        :param exclude_envs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_envs LtsCceAccessV3#exclude_envs}.
        :param exclude_k8_s_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_k8s_labels LtsCceAccessV3#exclude_k8s_labels}.
        :param exclude_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_labels LtsCceAccessV3#exclude_labels}.
        :param include_envs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_envs LtsCceAccessV3#include_envs}.
        :param include_k8_s_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_k8s_labels LtsCceAccessV3#include_k8s_labels}.
        :param include_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_labels LtsCceAccessV3#include_labels}.
        :param log_envs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_envs LtsCceAccessV3#log_envs}.
        :param log_k8_s: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_k8s LtsCceAccessV3#log_k8s}.
        :param log_labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_labels LtsCceAccessV3#log_labels}.
        :param multi_log_format: multi_log_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#multi_log_format LtsCceAccessV3#multi_log_format}
        :param name_space_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#name_space_regex LtsCceAccessV3#name_space_regex}.
        :param paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#paths LtsCceAccessV3#paths}.
        :param pod_name_regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#pod_name_regex LtsCceAccessV3#pod_name_regex}.
        :param single_log_format: single_log_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#single_log_format LtsCceAccessV3#single_log_format}
        :param stderr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#stderr LtsCceAccessV3#stderr}.
        :param stdout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#stdout LtsCceAccessV3#stdout}.
        '''
        if isinstance(multi_log_format, dict):
            multi_log_format = LtsCceAccessV3AccessConfigMultiLogFormat(**multi_log_format)
        if isinstance(single_log_format, dict):
            single_log_format = LtsCceAccessV3AccessConfigSingleLogFormat(**single_log_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b35f715f9646c628cfc8d860f33f37bd0411c2c8893ae120fe2f1cfbc02092)
            check_type(argname="argument path_type", value=path_type, expected_type=type_hints["path_type"])
            check_type(argname="argument black_paths", value=black_paths, expected_type=type_hints["black_paths"])
            check_type(argname="argument container_name_regex", value=container_name_regex, expected_type=type_hints["container_name_regex"])
            check_type(argname="argument exclude_envs", value=exclude_envs, expected_type=type_hints["exclude_envs"])
            check_type(argname="argument exclude_k8_s_labels", value=exclude_k8_s_labels, expected_type=type_hints["exclude_k8_s_labels"])
            check_type(argname="argument exclude_labels", value=exclude_labels, expected_type=type_hints["exclude_labels"])
            check_type(argname="argument include_envs", value=include_envs, expected_type=type_hints["include_envs"])
            check_type(argname="argument include_k8_s_labels", value=include_k8_s_labels, expected_type=type_hints["include_k8_s_labels"])
            check_type(argname="argument include_labels", value=include_labels, expected_type=type_hints["include_labels"])
            check_type(argname="argument log_envs", value=log_envs, expected_type=type_hints["log_envs"])
            check_type(argname="argument log_k8_s", value=log_k8_s, expected_type=type_hints["log_k8_s"])
            check_type(argname="argument log_labels", value=log_labels, expected_type=type_hints["log_labels"])
            check_type(argname="argument multi_log_format", value=multi_log_format, expected_type=type_hints["multi_log_format"])
            check_type(argname="argument name_space_regex", value=name_space_regex, expected_type=type_hints["name_space_regex"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument pod_name_regex", value=pod_name_regex, expected_type=type_hints["pod_name_regex"])
            check_type(argname="argument single_log_format", value=single_log_format, expected_type=type_hints["single_log_format"])
            check_type(argname="argument stderr", value=stderr, expected_type=type_hints["stderr"])
            check_type(argname="argument stdout", value=stdout, expected_type=type_hints["stdout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_type": path_type,
        }
        if black_paths is not None:
            self._values["black_paths"] = black_paths
        if container_name_regex is not None:
            self._values["container_name_regex"] = container_name_regex
        if exclude_envs is not None:
            self._values["exclude_envs"] = exclude_envs
        if exclude_k8_s_labels is not None:
            self._values["exclude_k8_s_labels"] = exclude_k8_s_labels
        if exclude_labels is not None:
            self._values["exclude_labels"] = exclude_labels
        if include_envs is not None:
            self._values["include_envs"] = include_envs
        if include_k8_s_labels is not None:
            self._values["include_k8_s_labels"] = include_k8_s_labels
        if include_labels is not None:
            self._values["include_labels"] = include_labels
        if log_envs is not None:
            self._values["log_envs"] = log_envs
        if log_k8_s is not None:
            self._values["log_k8_s"] = log_k8_s
        if log_labels is not None:
            self._values["log_labels"] = log_labels
        if multi_log_format is not None:
            self._values["multi_log_format"] = multi_log_format
        if name_space_regex is not None:
            self._values["name_space_regex"] = name_space_regex
        if paths is not None:
            self._values["paths"] = paths
        if pod_name_regex is not None:
            self._values["pod_name_regex"] = pod_name_regex
        if single_log_format is not None:
            self._values["single_log_format"] = single_log_format
        if stderr is not None:
            self._values["stderr"] = stderr
        if stdout is not None:
            self._values["stdout"] = stdout

    @builtins.property
    def path_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#path_type LtsCceAccessV3#path_type}.'''
        result = self._values.get("path_type")
        assert result is not None, "Required property 'path_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def black_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#black_paths LtsCceAccessV3#black_paths}.'''
        result = self._values.get("black_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def container_name_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#container_name_regex LtsCceAccessV3#container_name_regex}.'''
        result = self._values.get("container_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclude_envs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_envs LtsCceAccessV3#exclude_envs}.'''
        result = self._values.get("exclude_envs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def exclude_k8_s_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_k8s_labels LtsCceAccessV3#exclude_k8s_labels}.'''
        result = self._values.get("exclude_k8_s_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def exclude_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#exclude_labels LtsCceAccessV3#exclude_labels}.'''
        result = self._values.get("exclude_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def include_envs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_envs LtsCceAccessV3#include_envs}.'''
        result = self._values.get("include_envs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def include_k8_s_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_k8s_labels LtsCceAccessV3#include_k8s_labels}.'''
        result = self._values.get("include_k8_s_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def include_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#include_labels LtsCceAccessV3#include_labels}.'''
        result = self._values.get("include_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_envs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_envs LtsCceAccessV3#log_envs}.'''
        result = self._values.get("log_envs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_k8_s(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_k8s LtsCceAccessV3#log_k8s}.'''
        result = self._values.get("log_k8_s")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_labels LtsCceAccessV3#log_labels}.'''
        result = self._values.get("log_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def multi_log_format(
        self,
    ) -> typing.Optional["LtsCceAccessV3AccessConfigMultiLogFormat"]:
        '''multi_log_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#multi_log_format LtsCceAccessV3#multi_log_format}
        '''
        result = self._values.get("multi_log_format")
        return typing.cast(typing.Optional["LtsCceAccessV3AccessConfigMultiLogFormat"], result)

    @builtins.property
    def name_space_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#name_space_regex LtsCceAccessV3#name_space_regex}.'''
        result = self._values.get("name_space_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#paths LtsCceAccessV3#paths}.'''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pod_name_regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#pod_name_regex LtsCceAccessV3#pod_name_regex}.'''
        result = self._values.get("pod_name_regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_log_format(
        self,
    ) -> typing.Optional["LtsCceAccessV3AccessConfigSingleLogFormat"]:
        '''single_log_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#single_log_format LtsCceAccessV3#single_log_format}
        '''
        result = self._values.get("single_log_format")
        return typing.cast(typing.Optional["LtsCceAccessV3AccessConfigSingleLogFormat"], result)

    @builtins.property
    def stderr(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#stderr LtsCceAccessV3#stderr}.'''
        result = self._values.get("stderr")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def stdout(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#stdout LtsCceAccessV3#stdout}.'''
        result = self._values.get("stdout")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsCceAccessV3AccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCceAccessV3.LtsCceAccessV3AccessConfigMultiLogFormat",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class LtsCceAccessV3AccessConfigMultiLogFormat:
    def __init__(
        self,
        *,
        mode: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#mode LtsCceAccessV3#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#value LtsCceAccessV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d93b67b638e21c3b75abe3acf7dee5f82f03271ca409b73d119858f279f905d)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#mode LtsCceAccessV3#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#value LtsCceAccessV3#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsCceAccessV3AccessConfigMultiLogFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsCceAccessV3AccessConfigMultiLogFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCceAccessV3.LtsCceAccessV3AccessConfigMultiLogFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc17698ace0e88b5476e9f82f9abe75ae40ddf2c1b97aac2a5ae3acd36323cfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25000ecc89520b3fd5d726ed158e76d48b27370c57f2f15ad5e7c629801ddc42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7e62a58f3b1298db14310fbb8759dbb1f4d80f26c72910df717c59c2b38889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LtsCceAccessV3AccessConfigMultiLogFormat]:
        return typing.cast(typing.Optional[LtsCceAccessV3AccessConfigMultiLogFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsCceAccessV3AccessConfigMultiLogFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c81ef22183f31bbc0e1cf238e08720958c77087c530f50c4e35080d78da11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LtsCceAccessV3AccessConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCceAccessV3.LtsCceAccessV3AccessConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d42f8b609381e393ac083f2e6c94bad65586e35631de39010ccd1787b7f051f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMultiLogFormat")
    def put_multi_log_format(
        self,
        *,
        mode: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#mode LtsCceAccessV3#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#value LtsCceAccessV3#value}.
        '''
        value_ = LtsCceAccessV3AccessConfigMultiLogFormat(mode=mode, value=value)

        return typing.cast(None, jsii.invoke(self, "putMultiLogFormat", [value_]))

    @jsii.member(jsii_name="putSingleLogFormat")
    def put_single_log_format(
        self,
        *,
        mode: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#mode LtsCceAccessV3#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#value LtsCceAccessV3#value}.
        '''
        value_ = LtsCceAccessV3AccessConfigSingleLogFormat(mode=mode, value=value)

        return typing.cast(None, jsii.invoke(self, "putSingleLogFormat", [value_]))

    @jsii.member(jsii_name="resetBlackPaths")
    def reset_black_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlackPaths", []))

    @jsii.member(jsii_name="resetContainerNameRegex")
    def reset_container_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerNameRegex", []))

    @jsii.member(jsii_name="resetExcludeEnvs")
    def reset_exclude_envs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeEnvs", []))

    @jsii.member(jsii_name="resetExcludeK8SLabels")
    def reset_exclude_k8_s_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeK8SLabels", []))

    @jsii.member(jsii_name="resetExcludeLabels")
    def reset_exclude_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeLabels", []))

    @jsii.member(jsii_name="resetIncludeEnvs")
    def reset_include_envs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeEnvs", []))

    @jsii.member(jsii_name="resetIncludeK8SLabels")
    def reset_include_k8_s_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeK8SLabels", []))

    @jsii.member(jsii_name="resetIncludeLabels")
    def reset_include_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeLabels", []))

    @jsii.member(jsii_name="resetLogEnvs")
    def reset_log_envs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogEnvs", []))

    @jsii.member(jsii_name="resetLogK8S")
    def reset_log_k8_s(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogK8S", []))

    @jsii.member(jsii_name="resetLogLabels")
    def reset_log_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLabels", []))

    @jsii.member(jsii_name="resetMultiLogFormat")
    def reset_multi_log_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiLogFormat", []))

    @jsii.member(jsii_name="resetNameSpaceRegex")
    def reset_name_space_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameSpaceRegex", []))

    @jsii.member(jsii_name="resetPaths")
    def reset_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaths", []))

    @jsii.member(jsii_name="resetPodNameRegex")
    def reset_pod_name_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPodNameRegex", []))

    @jsii.member(jsii_name="resetSingleLogFormat")
    def reset_single_log_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleLogFormat", []))

    @jsii.member(jsii_name="resetStderr")
    def reset_stderr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStderr", []))

    @jsii.member(jsii_name="resetStdout")
    def reset_stdout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStdout", []))

    @builtins.property
    @jsii.member(jsii_name="multiLogFormat")
    def multi_log_format(
        self,
    ) -> LtsCceAccessV3AccessConfigMultiLogFormatOutputReference:
        return typing.cast(LtsCceAccessV3AccessConfigMultiLogFormatOutputReference, jsii.get(self, "multiLogFormat"))

    @builtins.property
    @jsii.member(jsii_name="singleLogFormat")
    def single_log_format(
        self,
    ) -> "LtsCceAccessV3AccessConfigSingleLogFormatOutputReference":
        return typing.cast("LtsCceAccessV3AccessConfigSingleLogFormatOutputReference", jsii.get(self, "singleLogFormat"))

    @builtins.property
    @jsii.member(jsii_name="blackPathsInput")
    def black_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "blackPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="containerNameRegexInput")
    def container_name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerNameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeEnvsInput")
    def exclude_envs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "excludeEnvsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeK8SLabelsInput")
    def exclude_k8_s_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "excludeK8SLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeLabelsInput")
    def exclude_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "excludeLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeEnvsInput")
    def include_envs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "includeEnvsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeK8SLabelsInput")
    def include_k8_s_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "includeK8SLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeLabelsInput")
    def include_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "includeLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="logEnvsInput")
    def log_envs_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "logEnvsInput"))

    @builtins.property
    @jsii.member(jsii_name="logK8SInput")
    def log_k8_s_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "logK8SInput"))

    @builtins.property
    @jsii.member(jsii_name="logLabelsInput")
    def log_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "logLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="multiLogFormatInput")
    def multi_log_format_input(
        self,
    ) -> typing.Optional[LtsCceAccessV3AccessConfigMultiLogFormat]:
        return typing.cast(typing.Optional[LtsCceAccessV3AccessConfigMultiLogFormat], jsii.get(self, "multiLogFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="nameSpaceRegexInput")
    def name_space_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameSpaceRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="pathsInput")
    def paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pathsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathTypeInput")
    def path_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="podNameRegexInput")
    def pod_name_regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "podNameRegexInput"))

    @builtins.property
    @jsii.member(jsii_name="singleLogFormatInput")
    def single_log_format_input(
        self,
    ) -> typing.Optional["LtsCceAccessV3AccessConfigSingleLogFormat"]:
        return typing.cast(typing.Optional["LtsCceAccessV3AccessConfigSingleLogFormat"], jsii.get(self, "singleLogFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="stderrInput")
    def stderr_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stderrInput"))

    @builtins.property
    @jsii.member(jsii_name="stdoutInput")
    def stdout_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stdoutInput"))

    @builtins.property
    @jsii.member(jsii_name="blackPaths")
    def black_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "blackPaths"))

    @black_paths.setter
    def black_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbfc696f4184f58d19ccfce25c6c7f3e89f83928139ac8433d0fdf4cc18bcc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blackPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerNameRegex")
    def container_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerNameRegex"))

    @container_name_regex.setter
    def container_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd1ce42ea96efdfa4165f9c60284408a8753d66f1a2861f479b9661017af710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeEnvs")
    def exclude_envs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "excludeEnvs"))

    @exclude_envs.setter
    def exclude_envs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eda164bdf4e93ca396765558d6b0157d80b4d5084e28710e256831abd856736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeEnvs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeK8SLabels")
    def exclude_k8_s_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "excludeK8SLabels"))

    @exclude_k8_s_labels.setter
    def exclude_k8_s_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd26c3afe69959a6e1ab1097a68f6b8fa9b717e3a37077204d03aa67975d578f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeK8SLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeLabels")
    def exclude_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "excludeLabels"))

    @exclude_labels.setter
    def exclude_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a220771f24b29f6705e6dfbf3151db8ab113fc120a6b5dade6f0fa76a55a81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeEnvs")
    def include_envs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "includeEnvs"))

    @include_envs.setter
    def include_envs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9294c503f99b4bcf13567143c6c121c1272e5103f9dde3ccc07e46a83fc6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeEnvs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeK8SLabels")
    def include_k8_s_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "includeK8SLabels"))

    @include_k8_s_labels.setter
    def include_k8_s_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd515739df323ff1db67d5cadd9dd8934a6d4b996c55fc2a1357d016ab6db6b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeK8SLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeLabels")
    def include_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "includeLabels"))

    @include_labels.setter
    def include_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785cfb1315b60acd90dfb22b786d03eb0d2e3025fe065b0326e27938ef9cd686)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logEnvs")
    def log_envs(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logEnvs"))

    @log_envs.setter
    def log_envs(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bc1988ef47b8732762269d41109a91a4bdf0684153df2588b5ff554f7ee546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logEnvs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logK8S")
    def log_k8_s(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logK8S"))

    @log_k8_s.setter
    def log_k8_s(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6966e4d3ffe509345d8e00422dcfad07aff047db97c560b0ed780e6295c9d386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logK8S", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLabels")
    def log_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "logLabels"))

    @log_labels.setter
    def log_labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3f2701e650af1c4c5ac6774799bd811832d49feabf580657870bd915b8672a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLabels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameSpaceRegex")
    def name_space_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameSpaceRegex"))

    @name_space_regex.setter
    def name_space_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b9cfc8b6ff607f2b81030b50e1a72d98d8ad54ff26632ba34e3bf7dc14cd4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameSpaceRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="paths")
    def paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "paths"))

    @paths.setter
    def paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e784c3db668c346ed353962407754094f009fd67fc0621d1036d41fcb6755d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathType")
    def path_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathType"))

    @path_type.setter
    def path_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db8eaf69e4ad4e4b6a668285c6f175800dc689c1c10828066059fbe06aca826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="podNameRegex")
    def pod_name_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "podNameRegex"))

    @pod_name_regex.setter
    def pod_name_regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1139befff085a2a50d89006bc0995a28b1d209caadfd94035566ba03f10d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "podNameRegex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stderr")
    def stderr(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stderr"))

    @stderr.setter
    def stderr(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a4d61bbf474aada028e366590de7712f908b33166c1e4b7ceb07816eca2037b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stderr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stdout")
    def stdout(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stdout"))

    @stdout.setter
    def stdout(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540a248da1a7d89409c9f418295e0ee8a66f1029544eba90c1a9dfce54c00e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stdout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LtsCceAccessV3AccessConfig]:
        return typing.cast(typing.Optional[LtsCceAccessV3AccessConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsCceAccessV3AccessConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b2d700d3d99218bc420fbd0e7ab294636b8236fcaff421292d25d0ebaead29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCceAccessV3.LtsCceAccessV3AccessConfigSingleLogFormat",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class LtsCceAccessV3AccessConfigSingleLogFormat:
    def __init__(
        self,
        *,
        mode: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#mode LtsCceAccessV3#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#value LtsCceAccessV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e531bef20e669ed1994152d02d402fcdb8e0bc8c1c72a182af01aedb5a8a2f19)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#mode LtsCceAccessV3#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#value LtsCceAccessV3#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsCceAccessV3AccessConfigSingleLogFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsCceAccessV3AccessConfigSingleLogFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCceAccessV3.LtsCceAccessV3AccessConfigSingleLogFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aef732d602d662b5f703f90c4f30031f7de2bfd169895b8f3b731206e59b35e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e513b7be47cf6f037675b87a0d7b02afafaf001bac10191a5977fc79682cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf562f4393556db2de9019ccbdd849ef493b94ba635b88632ab95c69bc94cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LtsCceAccessV3AccessConfigSingleLogFormat]:
        return typing.cast(typing.Optional[LtsCceAccessV3AccessConfigSingleLogFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsCceAccessV3AccessConfigSingleLogFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0645a5511edd054b277bb9c5970173ba18922f0fdaa8f0aab92d9fc1d4e0923e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsCceAccessV3.LtsCceAccessV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "access_config": "accessConfig",
        "cluster_id": "clusterId",
        "log_group_id": "logGroupId",
        "log_stream_id": "logStreamId",
        "name": "name",
        "binary_collect": "binaryCollect",
        "host_group_ids": "hostGroupIds",
        "id": "id",
        "log_split": "logSplit",
        "tags": "tags",
    },
)
class LtsCceAccessV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        access_config: typing.Union[LtsCceAccessV3AccessConfig, typing.Dict[builtins.str, typing.Any]],
        cluster_id: builtins.str,
        log_group_id: builtins.str,
        log_stream_id: builtins.str,
        name: builtins.str,
        binary_collect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        log_split: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param access_config: access_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#access_config LtsCceAccessV3#access_config}
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#cluster_id LtsCceAccessV3#cluster_id}.
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_group_id LtsCceAccessV3#log_group_id}.
        :param log_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_stream_id LtsCceAccessV3#log_stream_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#name LtsCceAccessV3#name}.
        :param binary_collect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#binary_collect LtsCceAccessV3#binary_collect}.
        :param host_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#host_group_ids LtsCceAccessV3#host_group_ids}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#id LtsCceAccessV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_split: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_split LtsCceAccessV3#log_split}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#tags LtsCceAccessV3#tags}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(access_config, dict):
            access_config = LtsCceAccessV3AccessConfig(**access_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328e6bfc0e54c441e55d671e3965869c33bbd1f76ba8641fcfd5b3e2e6181486)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument log_group_id", value=log_group_id, expected_type=type_hints["log_group_id"])
            check_type(argname="argument log_stream_id", value=log_stream_id, expected_type=type_hints["log_stream_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument binary_collect", value=binary_collect, expected_type=type_hints["binary_collect"])
            check_type(argname="argument host_group_ids", value=host_group_ids, expected_type=type_hints["host_group_ids"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_split", value=log_split, expected_type=type_hints["log_split"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_config": access_config,
            "cluster_id": cluster_id,
            "log_group_id": log_group_id,
            "log_stream_id": log_stream_id,
            "name": name,
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
        if binary_collect is not None:
            self._values["binary_collect"] = binary_collect
        if host_group_ids is not None:
            self._values["host_group_ids"] = host_group_ids
        if id is not None:
            self._values["id"] = id
        if log_split is not None:
            self._values["log_split"] = log_split
        if tags is not None:
            self._values["tags"] = tags

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
    def access_config(self) -> LtsCceAccessV3AccessConfig:
        '''access_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#access_config LtsCceAccessV3#access_config}
        '''
        result = self._values.get("access_config")
        assert result is not None, "Required property 'access_config' is missing"
        return typing.cast(LtsCceAccessV3AccessConfig, result)

    @builtins.property
    def cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#cluster_id LtsCceAccessV3#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_group_id LtsCceAccessV3#log_group_id}.'''
        result = self._values.get("log_group_id")
        assert result is not None, "Required property 'log_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_stream_id LtsCceAccessV3#log_stream_id}.'''
        result = self._values.get("log_stream_id")
        assert result is not None, "Required property 'log_stream_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#name LtsCceAccessV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def binary_collect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#binary_collect LtsCceAccessV3#binary_collect}.'''
        result = self._values.get("binary_collect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#host_group_ids LtsCceAccessV3#host_group_ids}.'''
        result = self._values.get("host_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#id LtsCceAccessV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_split(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#log_split LtsCceAccessV3#log_split}.'''
        result = self._values.get("log_split")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_cce_access_v3#tags LtsCceAccessV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsCceAccessV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LtsCceAccessV3",
    "LtsCceAccessV3AccessConfig",
    "LtsCceAccessV3AccessConfigMultiLogFormat",
    "LtsCceAccessV3AccessConfigMultiLogFormatOutputReference",
    "LtsCceAccessV3AccessConfigOutputReference",
    "LtsCceAccessV3AccessConfigSingleLogFormat",
    "LtsCceAccessV3AccessConfigSingleLogFormatOutputReference",
    "LtsCceAccessV3Config",
]

publication.publish()

def _typecheckingstub__c04d6d041238d2b52a034d0b84597058a34c8ba87da6e5f9a383021b336cf53a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    access_config: typing.Union[LtsCceAccessV3AccessConfig, typing.Dict[builtins.str, typing.Any]],
    cluster_id: builtins.str,
    log_group_id: builtins.str,
    log_stream_id: builtins.str,
    name: builtins.str,
    binary_collect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    log_split: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__7dfd3402b6aa9a6167ecca0b00e5c1112403c637761aa18afb9e7028ee57b097(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790c3a0af29986211a6c6a8cbb7d4d9734a0ad25dce2c04a007a1b191e22cbee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83183063cb471ccf0ac55fb99eed158adb654a89e936b11cca6c188ec289dde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd3041787d85e6671532f34e978d905d29704a06b859fef5ff59823a67d71a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba90a364767faa61fa8cbbe2a1f13fff703af413917a494c0d7bcbcc5a041360(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47befd5fd6c5840dd900af51bc954fb802879b5e4e51cf348fd6813a63015dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4f7e485c6ebd8a8250fa281355f977d88c0db86dc2a35c082d110fea8f6aa7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07648ce7545b85ad5d96e129b845a08c7e6d039a4418810136d1f6f986adcd75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce700488c46912eedf32fb92c7321614be425b93010fa5c9702afb3cafa9e6ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc10500c9d2852e10bd062a2089a36ec2bb9634302412818039212ba70bbfce(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b35f715f9646c628cfc8d860f33f37bd0411c2c8893ae120fe2f1cfbc02092(
    *,
    path_type: builtins.str,
    black_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_name_regex: typing.Optional[builtins.str] = None,
    exclude_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    exclude_k8_s_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    exclude_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    include_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    include_k8_s_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    include_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_envs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_k8_s: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    multi_log_format: typing.Optional[typing.Union[LtsCceAccessV3AccessConfigMultiLogFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    name_space_regex: typing.Optional[builtins.str] = None,
    paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    pod_name_regex: typing.Optional[builtins.str] = None,
    single_log_format: typing.Optional[typing.Union[LtsCceAccessV3AccessConfigSingleLogFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    stderr: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    stdout: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d93b67b638e21c3b75abe3acf7dee5f82f03271ca409b73d119858f279f905d(
    *,
    mode: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc17698ace0e88b5476e9f82f9abe75ae40ddf2c1b97aac2a5ae3acd36323cfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25000ecc89520b3fd5d726ed158e76d48b27370c57f2f15ad5e7c629801ddc42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7e62a58f3b1298db14310fbb8759dbb1f4d80f26c72910df717c59c2b38889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c81ef22183f31bbc0e1cf238e08720958c77087c530f50c4e35080d78da11b(
    value: typing.Optional[LtsCceAccessV3AccessConfigMultiLogFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42f8b609381e393ac083f2e6c94bad65586e35631de39010ccd1787b7f051f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbfc696f4184f58d19ccfce25c6c7f3e89f83928139ac8433d0fdf4cc18bcc5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd1ce42ea96efdfa4165f9c60284408a8753d66f1a2861f479b9661017af710(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eda164bdf4e93ca396765558d6b0157d80b4d5084e28710e256831abd856736(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd26c3afe69959a6e1ab1097a68f6b8fa9b717e3a37077204d03aa67975d578f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a220771f24b29f6705e6dfbf3151db8ab113fc120a6b5dade6f0fa76a55a81(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9294c503f99b4bcf13567143c6c121c1272e5103f9dde3ccc07e46a83fc6f3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd515739df323ff1db67d5cadd9dd8934a6d4b996c55fc2a1357d016ab6db6b0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785cfb1315b60acd90dfb22b786d03eb0d2e3025fe065b0326e27938ef9cd686(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bc1988ef47b8732762269d41109a91a4bdf0684153df2588b5ff554f7ee546(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6966e4d3ffe509345d8e00422dcfad07aff047db97c560b0ed780e6295c9d386(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3f2701e650af1c4c5ac6774799bd811832d49feabf580657870bd915b8672a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b9cfc8b6ff607f2b81030b50e1a72d98d8ad54ff26632ba34e3bf7dc14cd4f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e784c3db668c346ed353962407754094f009fd67fc0621d1036d41fcb6755d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db8eaf69e4ad4e4b6a668285c6f175800dc689c1c10828066059fbe06aca826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1139befff085a2a50d89006bc0995a28b1d209caadfd94035566ba03f10d58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a4d61bbf474aada028e366590de7712f908b33166c1e4b7ceb07816eca2037b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540a248da1a7d89409c9f418295e0ee8a66f1029544eba90c1a9dfce54c00e86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b2d700d3d99218bc420fbd0e7ab294636b8236fcaff421292d25d0ebaead29(
    value: typing.Optional[LtsCceAccessV3AccessConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e531bef20e669ed1994152d02d402fcdb8e0bc8c1c72a182af01aedb5a8a2f19(
    *,
    mode: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aef732d602d662b5f703f90c4f30031f7de2bfd169895b8f3b731206e59b35e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e513b7be47cf6f037675b87a0d7b02afafaf001bac10191a5977fc79682cf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf562f4393556db2de9019ccbdd849ef493b94ba635b88632ab95c69bc94cc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0645a5511edd054b277bb9c5970173ba18922f0fdaa8f0aab92d9fc1d4e0923e(
    value: typing.Optional[LtsCceAccessV3AccessConfigSingleLogFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328e6bfc0e54c441e55d671e3965869c33bbd1f76ba8641fcfd5b3e2e6181486(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    access_config: typing.Union[LtsCceAccessV3AccessConfig, typing.Dict[builtins.str, typing.Any]],
    cluster_id: builtins.str,
    log_group_id: builtins.str,
    log_stream_id: builtins.str,
    name: builtins.str,
    binary_collect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    log_split: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
