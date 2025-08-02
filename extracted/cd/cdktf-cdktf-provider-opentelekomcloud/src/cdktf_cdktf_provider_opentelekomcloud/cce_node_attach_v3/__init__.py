r'''
# `opentelekomcloud_cce_node_attach_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_cce_node_attach_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3).
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


class CceNodeAttachV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3 opentelekomcloud_cce_node_attach_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_id: builtins.str,
        os: builtins.str,
        server_id: builtins.str,
        docker_base_size: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        key_pair: typing.Optional[builtins.str] = None,
        lvm_config: typing.Optional[builtins.str] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        postinstall: typing.Optional[builtins.str] = None,
        preinstall: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Union["CceNodeAttachV3Storage", typing.Dict[builtins.str, typing.Any]]] = None,
        system_disk_kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3Taints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CceNodeAttachV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3 opentelekomcloud_cce_node_attach_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#cluster_id CceNodeAttachV3#cluster_id}.
        :param os: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#os CceNodeAttachV3#os}.
        :param server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#server_id CceNodeAttachV3#server_id}.
        :param docker_base_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#docker_base_size CceNodeAttachV3#docker_base_size}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#id CceNodeAttachV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param k8_s_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#k8s_tags CceNodeAttachV3#k8s_tags}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#key_pair CceNodeAttachV3#key_pair}.
        :param lvm_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#lvm_config CceNodeAttachV3#lvm_config}.
        :param max_pods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#max_pods CceNodeAttachV3#max_pods}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#password CceNodeAttachV3#password}.
        :param postinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#postinstall CceNodeAttachV3#postinstall}.
        :param preinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#preinstall CceNodeAttachV3#preinstall}.
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#private_key CceNodeAttachV3#private_key}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#runtime CceNodeAttachV3#runtime}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#storage CceNodeAttachV3#storage}
        :param system_disk_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#system_disk_kms_key_id CceNodeAttachV3#system_disk_kms_key_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#tags CceNodeAttachV3#tags}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#taints CceNodeAttachV3#taints}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#timeouts CceNodeAttachV3#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a431a842a032404e8db5d93a7bce250b3dff1e1946d6110816fe3a326cc80c37)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CceNodeAttachV3Config(
            cluster_id=cluster_id,
            os=os,
            server_id=server_id,
            docker_base_size=docker_base_size,
            id=id,
            k8_s_tags=k8_s_tags,
            key_pair=key_pair,
            lvm_config=lvm_config,
            max_pods=max_pods,
            name=name,
            password=password,
            postinstall=postinstall,
            preinstall=preinstall,
            private_key=private_key,
            runtime=runtime,
            storage=storage,
            system_disk_kms_key_id=system_disk_kms_key_id,
            tags=tags,
            taints=taints,
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
        '''Generates CDKTF code for importing a CceNodeAttachV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CceNodeAttachV3 to import.
        :param import_from_id: The id of the existing CceNodeAttachV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CceNodeAttachV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bee0f6ee581fe26746ca48eb22cbda04b0472ca717178e79c27e3f8f44a285)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3StorageGroups", typing.Dict[builtins.str, typing.Any]]]],
        selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3StorageSelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param groups: groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#groups CceNodeAttachV3#groups}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#selectors CceNodeAttachV3#selectors}
        '''
        value = CceNodeAttachV3Storage(groups=groups, selectors=selectors)

        return typing.cast(None, jsii.invoke(self, "putStorage", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3Taints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b612c1e4462991e0bcaa5410d66750e7207970c360999c43016401afa2ab201a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#create CceNodeAttachV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#delete CceNodeAttachV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#update CceNodeAttachV3#update}.
        '''
        value = CceNodeAttachV3Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDockerBaseSize")
    def reset_docker_base_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerBaseSize", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetK8STags")
    def reset_k8_s_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetK8STags", []))

    @jsii.member(jsii_name="resetKeyPair")
    def reset_key_pair(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPair", []))

    @jsii.member(jsii_name="resetLvmConfig")
    def reset_lvm_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLvmConfig", []))

    @jsii.member(jsii_name="resetMaxPods")
    def reset_max_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPods", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPostinstall")
    def reset_postinstall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostinstall", []))

    @jsii.member(jsii_name="resetPreinstall")
    def reset_preinstall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreinstall", []))

    @jsii.member(jsii_name="resetPrivateKey")
    def reset_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKey", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @jsii.member(jsii_name="resetSystemDiskKmsKeyId")
    def reset_system_disk_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemDiskKmsKeyId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

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
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="billingMode")
    def billing_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "billingMode"))

    @builtins.property
    @jsii.member(jsii_name="dataVolumes")
    def data_volumes(self) -> "CceNodeAttachV3DataVolumesList":
        return typing.cast("CceNodeAttachV3DataVolumesList", jsii.get(self, "dataVolumes"))

    @builtins.property
    @jsii.member(jsii_name="flavorId")
    def flavor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flavorId"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="rootVolume")
    def root_volume(self) -> "CceNodeAttachV3RootVolumeList":
        return typing.cast("CceNodeAttachV3RootVolumeList", jsii.get(self, "rootVolume"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "CceNodeAttachV3StorageOutputReference":
        return typing.cast("CceNodeAttachV3StorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "CceNodeAttachV3TaintsList":
        return typing.cast("CceNodeAttachV3TaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CceNodeAttachV3TimeoutsOutputReference":
        return typing.cast("CceNodeAttachV3TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerBaseSizeInput")
    def docker_base_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dockerBaseSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="k8STagsInput")
    def k8_s_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "k8STagsInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPairInput")
    def key_pair_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPairInput"))

    @builtins.property
    @jsii.member(jsii_name="lvmConfigInput")
    def lvm_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lvmConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsInput")
    def max_pods_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="postinstallInput")
    def postinstall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "postinstallInput"))

    @builtins.property
    @jsii.member(jsii_name="preinstallInput")
    def preinstall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preinstallInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="serverIdInput")
    def server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional["CceNodeAttachV3Storage"]:
        return typing.cast(typing.Optional["CceNodeAttachV3Storage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="systemDiskKmsKeyIdInput")
    def system_disk_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "systemDiskKmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3Taints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3Taints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CceNodeAttachV3Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CceNodeAttachV3Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ff3dacadd868db6fd2c78450cf739dcd746807729e5703d1e2ef87d7242757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerBaseSize")
    def docker_base_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dockerBaseSize"))

    @docker_base_size.setter
    def docker_base_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380aa8ecf1f8af5b4c690c16b2adbcaca30e1816262f70f232d264dab987bd90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerBaseSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d801dfa9b6d5863ea129943ee7cb72e3dc581552ed61b4af464520abb1bfad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="k8STags")
    def k8_s_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "k8STags"))

    @k8_s_tags.setter
    def k8_s_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0567a66883b8d7c92b5f72ac5a9a34340ce730e635696b7e05b25df9bb58aae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "k8STags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPair")
    def key_pair(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPair"))

    @key_pair.setter
    def key_pair(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767405d7f295b586f39faa4ff8bf3dc126d96e50199d6ffaabf42e7641b72917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPair", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lvmConfig")
    def lvm_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lvmConfig"))

    @lvm_config.setter
    def lvm_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2c1b0abf8e5836c69cb4793212d0cb75de6f2469a73e07e74a831bbafe544a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lvmConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPods")
    def max_pods(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPods"))

    @max_pods.setter
    def max_pods(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92b7b30157b21c2c8cd1a395ae0e528557476276b2d423f5cae677d9788d467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3e0ede18100d72e2c8bcf1bdd0dc947acdb0b586f989bf08fcb8ea45326544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67a39516efc02123a223a6bb0059b21367a3dbc12f0060c7b9c50a05c1b86d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__881f45b2ee54188793ff164acf5dc3570d5a3f306e85b5a536ad6c935cc70665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="postinstall")
    def postinstall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postinstall"))

    @postinstall.setter
    def postinstall(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b7285d855fec6f4d7a6cb97a753bcc69ebfe9c6f8f4facafa371bda7e3b66e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "postinstall", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preinstall")
    def preinstall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preinstall"))

    @preinstall.setter
    def preinstall(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc6995b7a57bfb1b7c639fc9e38d008c89bd1555db496cbd7417cb1bb0776c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preinstall", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02f2fc6dbb9cde79bc9ec577a7a9cc67e74d66ac9b07347b68f93efe206237e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1e3fd8dfa4bf8cebe5862ec848976696ef9f7014ce05b893b00476f572c2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverId"))

    @server_id.setter
    def server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724e8d641cd307abbf5693c17802d6ce77a964dc91bcdcce61863766d793e7e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemDiskKmsKeyId")
    def system_disk_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "systemDiskKmsKeyId"))

    @system_disk_kms_key_id.setter
    def system_disk_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff1f431dce05bc2e954f16d366e570f6be3aced2504153013e8e942251a7c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemDiskKmsKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6cba3d71dd3630e795959cb6436431cc6c395893072df57dbce07e86d298d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_id": "clusterId",
        "os": "os",
        "server_id": "serverId",
        "docker_base_size": "dockerBaseSize",
        "id": "id",
        "k8_s_tags": "k8STags",
        "key_pair": "keyPair",
        "lvm_config": "lvmConfig",
        "max_pods": "maxPods",
        "name": "name",
        "password": "password",
        "postinstall": "postinstall",
        "preinstall": "preinstall",
        "private_key": "privateKey",
        "runtime": "runtime",
        "storage": "storage",
        "system_disk_kms_key_id": "systemDiskKmsKeyId",
        "tags": "tags",
        "taints": "taints",
        "timeouts": "timeouts",
    },
)
class CceNodeAttachV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_id: builtins.str,
        os: builtins.str,
        server_id: builtins.str,
        docker_base_size: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        key_pair: typing.Optional[builtins.str] = None,
        lvm_config: typing.Optional[builtins.str] = None,
        max_pods: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        postinstall: typing.Optional[builtins.str] = None,
        preinstall: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Union["CceNodeAttachV3Storage", typing.Dict[builtins.str, typing.Any]]] = None,
        system_disk_kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3Taints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["CceNodeAttachV3Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#cluster_id CceNodeAttachV3#cluster_id}.
        :param os: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#os CceNodeAttachV3#os}.
        :param server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#server_id CceNodeAttachV3#server_id}.
        :param docker_base_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#docker_base_size CceNodeAttachV3#docker_base_size}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#id CceNodeAttachV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param k8_s_tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#k8s_tags CceNodeAttachV3#k8s_tags}.
        :param key_pair: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#key_pair CceNodeAttachV3#key_pair}.
        :param lvm_config: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#lvm_config CceNodeAttachV3#lvm_config}.
        :param max_pods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#max_pods CceNodeAttachV3#max_pods}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#password CceNodeAttachV3#password}.
        :param postinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#postinstall CceNodeAttachV3#postinstall}.
        :param preinstall: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#preinstall CceNodeAttachV3#preinstall}.
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#private_key CceNodeAttachV3#private_key}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#runtime CceNodeAttachV3#runtime}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#storage CceNodeAttachV3#storage}
        :param system_disk_kms_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#system_disk_kms_key_id CceNodeAttachV3#system_disk_kms_key_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#tags CceNodeAttachV3#tags}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#taints CceNodeAttachV3#taints}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#timeouts CceNodeAttachV3#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(storage, dict):
            storage = CceNodeAttachV3Storage(**storage)
        if isinstance(timeouts, dict):
            timeouts = CceNodeAttachV3Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f4b698b555914c62d5e1619083f1b3bdb67983e4b7d92713262c24817803c7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
            check_type(argname="argument docker_base_size", value=docker_base_size, expected_type=type_hints["docker_base_size"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument k8_s_tags", value=k8_s_tags, expected_type=type_hints["k8_s_tags"])
            check_type(argname="argument key_pair", value=key_pair, expected_type=type_hints["key_pair"])
            check_type(argname="argument lvm_config", value=lvm_config, expected_type=type_hints["lvm_config"])
            check_type(argname="argument max_pods", value=max_pods, expected_type=type_hints["max_pods"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument postinstall", value=postinstall, expected_type=type_hints["postinstall"])
            check_type(argname="argument preinstall", value=preinstall, expected_type=type_hints["preinstall"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument system_disk_kms_key_id", value=system_disk_kms_key_id, expected_type=type_hints["system_disk_kms_key_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_id": cluster_id,
            "os": os,
            "server_id": server_id,
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
        if docker_base_size is not None:
            self._values["docker_base_size"] = docker_base_size
        if id is not None:
            self._values["id"] = id
        if k8_s_tags is not None:
            self._values["k8_s_tags"] = k8_s_tags
        if key_pair is not None:
            self._values["key_pair"] = key_pair
        if lvm_config is not None:
            self._values["lvm_config"] = lvm_config
        if max_pods is not None:
            self._values["max_pods"] = max_pods
        if name is not None:
            self._values["name"] = name
        if password is not None:
            self._values["password"] = password
        if postinstall is not None:
            self._values["postinstall"] = postinstall
        if preinstall is not None:
            self._values["preinstall"] = preinstall
        if private_key is not None:
            self._values["private_key"] = private_key
        if runtime is not None:
            self._values["runtime"] = runtime
        if storage is not None:
            self._values["storage"] = storage
        if system_disk_kms_key_id is not None:
            self._values["system_disk_kms_key_id"] = system_disk_kms_key_id
        if tags is not None:
            self._values["tags"] = tags
        if taints is not None:
            self._values["taints"] = taints
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
    def cluster_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#cluster_id CceNodeAttachV3#cluster_id}.'''
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#os CceNodeAttachV3#os}.'''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#server_id CceNodeAttachV3#server_id}.'''
        result = self._values.get("server_id")
        assert result is not None, "Required property 'server_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def docker_base_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#docker_base_size CceNodeAttachV3#docker_base_size}.'''
        result = self._values.get("docker_base_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#id CceNodeAttachV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def k8_s_tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#k8s_tags CceNodeAttachV3#k8s_tags}.'''
        result = self._values.get("k8_s_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def key_pair(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#key_pair CceNodeAttachV3#key_pair}.'''
        result = self._values.get("key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lvm_config(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#lvm_config CceNodeAttachV3#lvm_config}.'''
        result = self._values.get("lvm_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_pods(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#max_pods CceNodeAttachV3#max_pods}.'''
        result = self._values.get("max_pods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#password CceNodeAttachV3#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postinstall(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#postinstall CceNodeAttachV3#postinstall}.'''
        result = self._values.get("postinstall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preinstall(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#preinstall CceNodeAttachV3#preinstall}.'''
        result = self._values.get("preinstall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#private_key CceNodeAttachV3#private_key}.'''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#runtime CceNodeAttachV3#runtime}.'''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage(self) -> typing.Optional["CceNodeAttachV3Storage"]:
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#storage CceNodeAttachV3#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional["CceNodeAttachV3Storage"], result)

    @builtins.property
    def system_disk_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#system_disk_kms_key_id CceNodeAttachV3#system_disk_kms_key_id}.'''
        result = self._values.get("system_disk_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#tags CceNodeAttachV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3Taints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#taints CceNodeAttachV3#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3Taints"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CceNodeAttachV3Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#timeouts CceNodeAttachV3#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CceNodeAttachV3Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3DataVolumes",
    jsii_struct_bases=[],
    name_mapping={},
)
class CceNodeAttachV3DataVolumes:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3DataVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeAttachV3DataVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3DataVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b1043464c5a741fbd330e9016ff9f709124bc203093874d20370a6220ef8c48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceNodeAttachV3DataVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5013f6592da7ba5a92f3e1778935e57f991d257c3a866ca25df174efbc3384d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeAttachV3DataVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6954eff6e571b9b517eefd722a1fb3cd3f736ad1591119d242f011433be6e860)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea0b98fa8a4104dddb4575e84a546af9fe663e02aed608423b13443271e8083e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d189b252ad1b89d210adfaec059c47e2c7be8d799bf3dee24e34da99965d6d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CceNodeAttachV3DataVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3DataVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32fdea96f359568528253e3f32106a863e370c554acb4c855d3319f0011444e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dssPoolId")
    def dss_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dssPoolId"))

    @builtins.property
    @jsii.member(jsii_name="extendParam")
    def extend_param(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extendParam"))

    @builtins.property
    @jsii.member(jsii_name="extendParams")
    def extend_params(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "extendParams"))

    @builtins.property
    @jsii.member(jsii_name="hwPassthrough")
    def hw_passthrough(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "hwPassthrough"))

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @builtins.property
    @jsii.member(jsii_name="volumetype")
    def volumetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumetype"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceNodeAttachV3DataVolumes]:
        return typing.cast(typing.Optional[CceNodeAttachV3DataVolumes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CceNodeAttachV3DataVolumes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e1987f73f5d1f8077eb0d32a2b08c0fc3cda6aaf176c9e1ee3aa9c55ace0c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3RootVolume",
    jsii_struct_bases=[],
    name_mapping={},
)
class CceNodeAttachV3RootVolume:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3RootVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeAttachV3RootVolumeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3RootVolumeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6700b2a18849105c07c6d5ddabda099ae6c816d73a677b68e945c3a9b5f0b49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceNodeAttachV3RootVolumeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed3dc6f8498df3ac8019e78cae2a6e140773201722032856ff80d2c4d4c9bfb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeAttachV3RootVolumeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ebf13c9065fc854c80964fa27346f84864e34b26f29a681987fd5b6ab51f1c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f419ee88bdfc2d1ebd5b9a080ce2342707eabe5e69f4f0cfcb2254444db21a00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8f187812442a9fa253acfa2004359c7e226802447c1b8703aa6141addf95885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CceNodeAttachV3RootVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3RootVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fecb65b452dabd3e0dcbfd5a78d9f8923d0fbc0e8ad2365d7d763d18b56aa52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="extendParam")
    def extend_param(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extendParam"))

    @builtins.property
    @jsii.member(jsii_name="extendParams")
    def extend_params(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "extendParams"))

    @builtins.property
    @jsii.member(jsii_name="kmsId")
    def kms_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsId"))

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @builtins.property
    @jsii.member(jsii_name="volumetype")
    def volumetype(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumetype"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceNodeAttachV3RootVolume]:
        return typing.cast(typing.Optional[CceNodeAttachV3RootVolume], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CceNodeAttachV3RootVolume]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9366b004ef2e92c8d6159f0a9e43a5cad933a8d06c60cd54c69fc0c9f3d8ef3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3Storage",
    jsii_struct_bases=[],
    name_mapping={"groups": "groups", "selectors": "selectors"},
)
class CceNodeAttachV3Storage:
    def __init__(
        self,
        *,
        groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3StorageGroups", typing.Dict[builtins.str, typing.Any]]]],
        selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3StorageSelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param groups: groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#groups CceNodeAttachV3#groups}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#selectors CceNodeAttachV3#selectors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784d2719d963496233e2da9a44251c6fd441bc1afc55e086f11dc6061c41c06b)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "groups": groups,
            "selectors": selectors,
        }

    @builtins.property
    def groups(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageGroups"]]:
        '''groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#groups CceNodeAttachV3#groups}
        '''
        result = self._values.get("groups")
        assert result is not None, "Required property 'groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageGroups"]], result)

    @builtins.property
    def selectors(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageSelectors"]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#selectors CceNodeAttachV3#selectors}
        '''
        result = self._values.get("selectors")
        assert result is not None, "Required property 'selectors' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageSelectors"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3Storage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageGroups",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "selector_names": "selectorNames",
        "virtual_spaces": "virtualSpaces",
        "cce_managed": "cceManaged",
    },
)
class CceNodeAttachV3StorageGroups:
    def __init__(
        self,
        *,
        name: builtins.str,
        selector_names: typing.Sequence[builtins.str],
        virtual_spaces: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3StorageGroupsVirtualSpaces", typing.Dict[builtins.str, typing.Any]]]],
        cce_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.
        :param selector_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#selector_names CceNodeAttachV3#selector_names}.
        :param virtual_spaces: virtual_spaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#virtual_spaces CceNodeAttachV3#virtual_spaces}
        :param cce_managed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#cce_managed CceNodeAttachV3#cce_managed}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71f281a919d8f55282457d1b56725ed41fb10f95864b8f701c4f27773ed0766)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument selector_names", value=selector_names, expected_type=type_hints["selector_names"])
            check_type(argname="argument virtual_spaces", value=virtual_spaces, expected_type=type_hints["virtual_spaces"])
            check_type(argname="argument cce_managed", value=cce_managed, expected_type=type_hints["cce_managed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "selector_names": selector_names,
            "virtual_spaces": virtual_spaces,
        }
        if cce_managed is not None:
            self._values["cce_managed"] = cce_managed

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def selector_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#selector_names CceNodeAttachV3#selector_names}.'''
        result = self._values.get("selector_names")
        assert result is not None, "Required property 'selector_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def virtual_spaces(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageGroupsVirtualSpaces"]]:
        '''virtual_spaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#virtual_spaces CceNodeAttachV3#virtual_spaces}
        '''
        result = self._values.get("virtual_spaces")
        assert result is not None, "Required property 'virtual_spaces' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageGroupsVirtualSpaces"]], result)

    @builtins.property
    def cce_managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#cce_managed CceNodeAttachV3#cce_managed}.'''
        result = self._values.get("cce_managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3StorageGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeAttachV3StorageGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95880b6acfb99027cd114b86f3369f0b3315fd13e886d41db8966b59d6f73091)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceNodeAttachV3StorageGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6067aeb9b39714c3627d0b9efd28f7482b34b5e7d718d6bad3c67cd64699ce8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeAttachV3StorageGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7dcb3b2927ab6df892c52b9fb8aa208ae2474296fd7b14e6d62599b0eef1c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8da22bb72c3016592022ab266f29a9d067932bc4960906e11b42549d035744b0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__059319ede4fef68704fb0c3958d19c1e6b51232b78a80076970e2063b0c846e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4f3cb3efbd4be97551c034008a5ab32cb5702ca182228275e127aca795cf1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodeAttachV3StorageGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49959fb42e1609316be52ab7177ac34f9e0dea4559f468ffeb36dd331a2b5641)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putVirtualSpaces")
    def put_virtual_spaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3StorageGroupsVirtualSpaces", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c497760ea0994f07c773419315bdfd6de688504efdd8c13c9d8fec0ed8b422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVirtualSpaces", [value]))

    @jsii.member(jsii_name="resetCceManaged")
    def reset_cce_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCceManaged", []))

    @builtins.property
    @jsii.member(jsii_name="virtualSpaces")
    def virtual_spaces(self) -> "CceNodeAttachV3StorageGroupsVirtualSpacesList":
        return typing.cast("CceNodeAttachV3StorageGroupsVirtualSpacesList", jsii.get(self, "virtualSpaces"))

    @builtins.property
    @jsii.member(jsii_name="cceManagedInput")
    def cce_managed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cceManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorNamesInput")
    def selector_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "selectorNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualSpacesInput")
    def virtual_spaces_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageGroupsVirtualSpaces"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageGroupsVirtualSpaces"]]], jsii.get(self, "virtualSpacesInput"))

    @builtins.property
    @jsii.member(jsii_name="cceManaged")
    def cce_managed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cceManaged"))

    @cce_managed.setter
    def cce_managed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6afb7c179cad294e03b2352632f755ea7bff4ad7ec450c853745a68aa4c23a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cceManaged", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc18960207f5110897f7f7737800d21d99de1ff3f4d2edd7665751e92caeb15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="selectorNames")
    def selector_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "selectorNames"))

    @selector_names.setter
    def selector_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1813daa1d04dde2d030426e268edb32bb490fa8aabaa30a92ff70cbae0d48607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "selectorNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d847e2eceedd766ba70b69e0cf995bbb895e60d377626934d09e4992ff4c15c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageGroupsVirtualSpaces",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "size": "size",
        "lvm_lv_type": "lvmLvType",
        "lvm_path": "lvmPath",
        "runtime_lv_type": "runtimeLvType",
    },
)
class CceNodeAttachV3StorageGroupsVirtualSpaces:
    def __init__(
        self,
        *,
        name: builtins.str,
        size: builtins.str,
        lvm_lv_type: typing.Optional[builtins.str] = None,
        lvm_path: typing.Optional[builtins.str] = None,
        runtime_lv_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#size CceNodeAttachV3#size}.
        :param lvm_lv_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#lvm_lv_type CceNodeAttachV3#lvm_lv_type}.
        :param lvm_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#lvm_path CceNodeAttachV3#lvm_path}.
        :param runtime_lv_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#runtime_lv_type CceNodeAttachV3#runtime_lv_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d530945b8531349a29cf2e81d83e4450d63965ba7957c2ac862dcb50ba958b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument lvm_lv_type", value=lvm_lv_type, expected_type=type_hints["lvm_lv_type"])
            check_type(argname="argument lvm_path", value=lvm_path, expected_type=type_hints["lvm_path"])
            check_type(argname="argument runtime_lv_type", value=runtime_lv_type, expected_type=type_hints["runtime_lv_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "size": size,
        }
        if lvm_lv_type is not None:
            self._values["lvm_lv_type"] = lvm_lv_type
        if lvm_path is not None:
            self._values["lvm_path"] = lvm_path
        if runtime_lv_type is not None:
            self._values["runtime_lv_type"] = runtime_lv_type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#size CceNodeAttachV3#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lvm_lv_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#lvm_lv_type CceNodeAttachV3#lvm_lv_type}.'''
        result = self._values.get("lvm_lv_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lvm_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#lvm_path CceNodeAttachV3#lvm_path}.'''
        result = self._values.get("lvm_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_lv_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#runtime_lv_type CceNodeAttachV3#runtime_lv_type}.'''
        result = self._values.get("runtime_lv_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3StorageGroupsVirtualSpaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeAttachV3StorageGroupsVirtualSpacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageGroupsVirtualSpacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d36a9f19bf9d00edc91ee3a9454306111e1d64169a6201574a8f6a1e8933447)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CceNodeAttachV3StorageGroupsVirtualSpacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2055bb52327a1f84d7dfde333487e5156f056bfc51741acd2abeed7a2ca7942d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeAttachV3StorageGroupsVirtualSpacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1994a6a0464df967162e687fec6a45b6823ec9000965d79411606d594bb774)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9729448391f43ecff4b73e3799af002c7b3cf74c1f527d0acfe91648e53b47c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cef64f5f295dc8e2047b1570697d59b587177012a7aecf27fd14f8a655228e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroupsVirtualSpaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroupsVirtualSpaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroupsVirtualSpaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24243db5d77105bea8a634172df7d7c1c652071cb7a770005d489e2e7fa8b8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodeAttachV3StorageGroupsVirtualSpacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageGroupsVirtualSpacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e6d24e7195a38e47d093a5a75c053afe0820395c4f5bd65861644f22c11ae2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLvmLvType")
    def reset_lvm_lv_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLvmLvType", []))

    @jsii.member(jsii_name="resetLvmPath")
    def reset_lvm_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLvmPath", []))

    @jsii.member(jsii_name="resetRuntimeLvType")
    def reset_runtime_lv_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeLvType", []))

    @builtins.property
    @jsii.member(jsii_name="lvmLvTypeInput")
    def lvm_lv_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lvmLvTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lvmPathInput")
    def lvm_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lvmPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeLvTypeInput")
    def runtime_lv_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeLvTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="lvmLvType")
    def lvm_lv_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lvmLvType"))

    @lvm_lv_type.setter
    def lvm_lv_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3493b653fd174eb0ecb38c6cc21ab074209b0bb405c6876accea1401ad081e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lvmLvType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lvmPath")
    def lvm_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lvmPath"))

    @lvm_path.setter
    def lvm_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfecd6569b79fc63b02fa7ebfb6753c86ae633d36edfa58fc11607b9cfc89c60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lvmPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74fc1cd107ecfacafb9728198faa20a11bf11f8e48475aa0dd0f3dac73570ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeLvType")
    def runtime_lv_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeLvType"))

    @runtime_lv_type.setter
    def runtime_lv_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1fc94aae9cc0dc60366bbba1bb317d5dae353c57f34ad31bda88f641b49ddb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeLvType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "size"))

    @size.setter
    def size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbae5ed3103a4985f69007c73da678aebc420859f1255b10dee57295b6e7348f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageGroupsVirtualSpaces]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageGroupsVirtualSpaces]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageGroupsVirtualSpaces]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fd58adfb2a250e4531d4898af4e9ed80dd89ad6857f930cf86053c14a4e5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodeAttachV3StorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1ec5033284206fc7639341338d9727a8ae9de00a59b9e51bb70afca89c0842a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGroups")
    def put_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3StorageGroups, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a85f3c727445f1fc24e8370cf74cd8a51da7706c6fd86c70d8f6fed5e42da97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGroups", [value]))

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CceNodeAttachV3StorageSelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb332f2cac04e9977f2793ed63f1e7db704f3f86802a5b6efe8645d45385ed03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> CceNodeAttachV3StorageGroupsList:
        return typing.cast(CceNodeAttachV3StorageGroupsList, jsii.get(self, "groups"))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(self) -> "CceNodeAttachV3StorageSelectorsList":
        return typing.cast("CceNodeAttachV3StorageSelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroups]]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageSelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CceNodeAttachV3StorageSelectors"]]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CceNodeAttachV3Storage]:
        return typing.cast(typing.Optional[CceNodeAttachV3Storage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CceNodeAttachV3Storage]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__491cee4abe97fcc5e5326a27cba3939cb4f5ce01d6d9f99fb38d70bea227f348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageSelectors",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "match_label_count": "matchLabelCount",
        "match_label_metadata_cmkid": "matchLabelMetadataCmkid",
        "match_label_metadata_encrypted": "matchLabelMetadataEncrypted",
        "match_label_size": "matchLabelSize",
        "match_label_volume_type": "matchLabelVolumeType",
        "type": "type",
    },
)
class CceNodeAttachV3StorageSelectors:
    def __init__(
        self,
        *,
        name: builtins.str,
        match_label_count: typing.Optional[builtins.str] = None,
        match_label_metadata_cmkid: typing.Optional[builtins.str] = None,
        match_label_metadata_encrypted: typing.Optional[builtins.str] = None,
        match_label_size: typing.Optional[builtins.str] = None,
        match_label_volume_type: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.
        :param match_label_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_count CceNodeAttachV3#match_label_count}.
        :param match_label_metadata_cmkid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_metadata_cmkid CceNodeAttachV3#match_label_metadata_cmkid}.
        :param match_label_metadata_encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_metadata_encrypted CceNodeAttachV3#match_label_metadata_encrypted}.
        :param match_label_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_size CceNodeAttachV3#match_label_size}.
        :param match_label_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_volume_type CceNodeAttachV3#match_label_volume_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#type CceNodeAttachV3#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38eb1d5ee70139a9814f943d71cf45d90a8e5b707447444e912bb4bd1c76d0ed)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument match_label_count", value=match_label_count, expected_type=type_hints["match_label_count"])
            check_type(argname="argument match_label_metadata_cmkid", value=match_label_metadata_cmkid, expected_type=type_hints["match_label_metadata_cmkid"])
            check_type(argname="argument match_label_metadata_encrypted", value=match_label_metadata_encrypted, expected_type=type_hints["match_label_metadata_encrypted"])
            check_type(argname="argument match_label_size", value=match_label_size, expected_type=type_hints["match_label_size"])
            check_type(argname="argument match_label_volume_type", value=match_label_volume_type, expected_type=type_hints["match_label_volume_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if match_label_count is not None:
            self._values["match_label_count"] = match_label_count
        if match_label_metadata_cmkid is not None:
            self._values["match_label_metadata_cmkid"] = match_label_metadata_cmkid
        if match_label_metadata_encrypted is not None:
            self._values["match_label_metadata_encrypted"] = match_label_metadata_encrypted
        if match_label_size is not None:
            self._values["match_label_size"] = match_label_size
        if match_label_volume_type is not None:
            self._values["match_label_volume_type"] = match_label_volume_type
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#name CceNodeAttachV3#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_label_count(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_count CceNodeAttachV3#match_label_count}.'''
        result = self._values.get("match_label_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_label_metadata_cmkid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_metadata_cmkid CceNodeAttachV3#match_label_metadata_cmkid}.'''
        result = self._values.get("match_label_metadata_cmkid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_label_metadata_encrypted(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_metadata_encrypted CceNodeAttachV3#match_label_metadata_encrypted}.'''
        result = self._values.get("match_label_metadata_encrypted")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_label_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_size CceNodeAttachV3#match_label_size}.'''
        result = self._values.get("match_label_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_label_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#match_label_volume_type CceNodeAttachV3#match_label_volume_type}.'''
        result = self._values.get("match_label_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#type CceNodeAttachV3#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3StorageSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeAttachV3StorageSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__396fb2de347d7e503c3adf8b8e78fa4699d443c26d51e14ee342a44866ab47a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CceNodeAttachV3StorageSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3efb7355529912f16b3e24f4b662e019124877006ec8ca666a76640faa69c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeAttachV3StorageSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0d5a2b6bfa49584291aeb6ac9935cf7c1a8ef2b3c0a954b62182666c4a5c07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42f1f7755784e73d6afee82d6fe42084184183c727766999e68db0b914d93241)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d6c2268a58e36d2f0e39d0810cdb84892ed4b92c6b13f21be4abe5ca61a536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d08dc5dfa3647bbe94c85b82be450e15d4abd3fbc6152f0b7385bce434b341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodeAttachV3StorageSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3StorageSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3a183fef8f34f176884a155dfd0273d44b9971de4147604f58bb7a7c05b7686)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchLabelCount")
    def reset_match_label_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabelCount", []))

    @jsii.member(jsii_name="resetMatchLabelMetadataCmkid")
    def reset_match_label_metadata_cmkid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabelMetadataCmkid", []))

    @jsii.member(jsii_name="resetMatchLabelMetadataEncrypted")
    def reset_match_label_metadata_encrypted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabelMetadataEncrypted", []))

    @jsii.member(jsii_name="resetMatchLabelSize")
    def reset_match_label_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabelSize", []))

    @jsii.member(jsii_name="resetMatchLabelVolumeType")
    def reset_match_label_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchLabelVolumeType", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="matchLabelCountInput")
    def match_label_count_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchLabelCountInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelMetadataCmkidInput")
    def match_label_metadata_cmkid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchLabelMetadataCmkidInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelMetadataEncryptedInput")
    def match_label_metadata_encrypted_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchLabelMetadataEncryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelSizeInput")
    def match_label_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchLabelSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelVolumeTypeInput")
    def match_label_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchLabelVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="matchLabelCount")
    def match_label_count(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchLabelCount"))

    @match_label_count.setter
    def match_label_count(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c4d3bcf8b1dc2f25474718d0adcb85a7cad02facfe3d737f9105eadb9afbb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabelCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchLabelMetadataCmkid")
    def match_label_metadata_cmkid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchLabelMetadataCmkid"))

    @match_label_metadata_cmkid.setter
    def match_label_metadata_cmkid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d60c676b2b545ab361f7f122a6a366c4e63047a474c6bc12e4691e53e20e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabelMetadataCmkid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchLabelMetadataEncrypted")
    def match_label_metadata_encrypted(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchLabelMetadataEncrypted"))

    @match_label_metadata_encrypted.setter
    def match_label_metadata_encrypted(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e250808d3e65087497c8539dfae10aef2869af73d1062e30e2abd83d1cf872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabelMetadataEncrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchLabelSize")
    def match_label_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchLabelSize"))

    @match_label_size.setter
    def match_label_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bc71d3bdee1afad6e33c2f89dde208f4826913a34e64d665d2a093c7b1aaca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabelSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchLabelVolumeType")
    def match_label_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchLabelVolumeType"))

    @match_label_volume_type.setter
    def match_label_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80648a3870aa3829be322688902fa7f31348d6362aaef72e7c552b6b8626a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchLabelVolumeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65038878d6bdeee0ee86a62d9fd92258a6273a4b2c59f6e13f75800e1c399df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4a7b9bb48965d6e01b616d338f72d44f006fc8fd3dd9a454ac6e1f4d8c390a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b705eb5f8155ab47861c9561f94bb2c9d29daa0f7a84dea03399444c6be471d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3Taints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class CceNodeAttachV3Taints:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#effect CceNodeAttachV3#effect}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#key CceNodeAttachV3#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#value CceNodeAttachV3#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47da96db44c57f1ac5c9665d46a0f169eadd3f095695addad779b9881ff00a0)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
            "key": key,
            "value": value,
        }

    @builtins.property
    def effect(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#effect CceNodeAttachV3#effect}.'''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#key CceNodeAttachV3#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#value CceNodeAttachV3#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3Taints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeAttachV3TaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3TaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b3205d307d703530d14118541994f59f86219cc25a6c71da72db096229d332f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CceNodeAttachV3TaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb8a3ae370e8756f88c6c13986cf15a3fd12b9ed5eec6596daefd5b3d768cac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CceNodeAttachV3TaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67cb6a21a3c6ebcf535597a239e67fe2340b8485d9f67eb9ad21e10ae423867)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5183328a195c001885a92e54c22bd07a6582443f1fe536aa7af87064a99779a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__495ac56a2e8cfd1041ebe230f12d8aecc3ca03d97a0deadfab2c70326a498b1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3Taints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3Taints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3Taints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1bb58aa7268f6f8428d5e4515c9893e3776266e839260a879b76b159e3267f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CceNodeAttachV3TaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3TaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__022ab7ebe5d215bc879f0e8a5cb3819b0367e3dcc08117d36f854bed28fc4564)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39233223d0236f51d34197840b842cbf7fc95a018b1c839aca24c437cea71c31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a99325bbcc154088bb052bc2eb7f71def60999eecf086a975e79941dd905986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a193fd1695a9d66b216dc4f573c21542519ae262116c644e3f3b74f75ae15b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3Taints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3Taints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3Taints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730c13b67fefdc8a1f1dc330fc60d8aa8595b2bb5e2fb2cf68b335dfb187963e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CceNodeAttachV3Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#create CceNodeAttachV3#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#delete CceNodeAttachV3#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#update CceNodeAttachV3#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e15862624ce22b449e6a5a16fa8293882a87d9e0437bf9c8e2977bdc0dcec3d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#create CceNodeAttachV3#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#delete CceNodeAttachV3#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cce_node_attach_v3#update CceNodeAttachV3#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CceNodeAttachV3Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CceNodeAttachV3TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cceNodeAttachV3.CceNodeAttachV3TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1394bec3b171c861814c1b0969231d8b8ee64c58c3cdf36c3015e501a7536816)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27926b292f9e700af825c04da0cd368081b397183ca48167873f5511d263ce0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3960b78d4f192a4e96ba62158ded6c0233a0f5ce4457eeb69aacb4a2d945008b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab326aebaaf119105f40ae7177be1cf543d2073fd1a784a6edfc8f6d4019773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679cf19e59aaa3df6d701ebb2ab767c59193b5322832693e614f29a67460feb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CceNodeAttachV3",
    "CceNodeAttachV3Config",
    "CceNodeAttachV3DataVolumes",
    "CceNodeAttachV3DataVolumesList",
    "CceNodeAttachV3DataVolumesOutputReference",
    "CceNodeAttachV3RootVolume",
    "CceNodeAttachV3RootVolumeList",
    "CceNodeAttachV3RootVolumeOutputReference",
    "CceNodeAttachV3Storage",
    "CceNodeAttachV3StorageGroups",
    "CceNodeAttachV3StorageGroupsList",
    "CceNodeAttachV3StorageGroupsOutputReference",
    "CceNodeAttachV3StorageGroupsVirtualSpaces",
    "CceNodeAttachV3StorageGroupsVirtualSpacesList",
    "CceNodeAttachV3StorageGroupsVirtualSpacesOutputReference",
    "CceNodeAttachV3StorageOutputReference",
    "CceNodeAttachV3StorageSelectors",
    "CceNodeAttachV3StorageSelectorsList",
    "CceNodeAttachV3StorageSelectorsOutputReference",
    "CceNodeAttachV3Taints",
    "CceNodeAttachV3TaintsList",
    "CceNodeAttachV3TaintsOutputReference",
    "CceNodeAttachV3Timeouts",
    "CceNodeAttachV3TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a431a842a032404e8db5d93a7bce250b3dff1e1946d6110816fe3a326cc80c37(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_id: builtins.str,
    os: builtins.str,
    server_id: builtins.str,
    docker_base_size: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    key_pair: typing.Optional[builtins.str] = None,
    lvm_config: typing.Optional[builtins.str] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    postinstall: typing.Optional[builtins.str] = None,
    preinstall: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Union[CceNodeAttachV3Storage, typing.Dict[builtins.str, typing.Any]]] = None,
    system_disk_kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3Taints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CceNodeAttachV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b8bee0f6ee581fe26746ca48eb22cbda04b0472ca717178e79c27e3f8f44a285(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b612c1e4462991e0bcaa5410d66750e7207970c360999c43016401afa2ab201a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3Taints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ff3dacadd868db6fd2c78450cf739dcd746807729e5703d1e2ef87d7242757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380aa8ecf1f8af5b4c690c16b2adbcaca30e1816262f70f232d264dab987bd90(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d801dfa9b6d5863ea129943ee7cb72e3dc581552ed61b4af464520abb1bfad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0567a66883b8d7c92b5f72ac5a9a34340ce730e635696b7e05b25df9bb58aae(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767405d7f295b586f39faa4ff8bf3dc126d96e50199d6ffaabf42e7641b72917(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2c1b0abf8e5836c69cb4793212d0cb75de6f2469a73e07e74a831bbafe544a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92b7b30157b21c2c8cd1a395ae0e528557476276b2d423f5cae677d9788d467(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3e0ede18100d72e2c8bcf1bdd0dc947acdb0b586f989bf08fcb8ea45326544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67a39516efc02123a223a6bb0059b21367a3dbc12f0060c7b9c50a05c1b86d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881f45b2ee54188793ff164acf5dc3570d5a3f306e85b5a536ad6c935cc70665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b7285d855fec6f4d7a6cb97a753bcc69ebfe9c6f8f4facafa371bda7e3b66e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc6995b7a57bfb1b7c639fc9e38d008c89bd1555db496cbd7417cb1bb0776c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02f2fc6dbb9cde79bc9ec577a7a9cc67e74d66ac9b07347b68f93efe206237e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1e3fd8dfa4bf8cebe5862ec848976696ef9f7014ce05b893b00476f572c2ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724e8d641cd307abbf5693c17802d6ce77a964dc91bcdcce61863766d793e7e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff1f431dce05bc2e954f16d366e570f6be3aced2504153013e8e942251a7c7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6cba3d71dd3630e795959cb6436431cc6c395893072df57dbce07e86d298d6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f4b698b555914c62d5e1619083f1b3bdb67983e4b7d92713262c24817803c7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_id: builtins.str,
    os: builtins.str,
    server_id: builtins.str,
    docker_base_size: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    k8_s_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    key_pair: typing.Optional[builtins.str] = None,
    lvm_config: typing.Optional[builtins.str] = None,
    max_pods: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    postinstall: typing.Optional[builtins.str] = None,
    preinstall: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Union[CceNodeAttachV3Storage, typing.Dict[builtins.str, typing.Any]]] = None,
    system_disk_kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3Taints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[CceNodeAttachV3Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1043464c5a741fbd330e9016ff9f709124bc203093874d20370a6220ef8c48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5013f6592da7ba5a92f3e1778935e57f991d257c3a866ca25df174efbc3384d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6954eff6e571b9b517eefd722a1fb3cd3f736ad1591119d242f011433be6e860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0b98fa8a4104dddb4575e84a546af9fe663e02aed608423b13443271e8083e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d189b252ad1b89d210adfaec059c47e2c7be8d799bf3dee24e34da99965d6d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fdea96f359568528253e3f32106a863e370c554acb4c855d3319f0011444e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e1987f73f5d1f8077eb0d32a2b08c0fc3cda6aaf176c9e1ee3aa9c55ace0c87(
    value: typing.Optional[CceNodeAttachV3DataVolumes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6700b2a18849105c07c6d5ddabda099ae6c816d73a677b68e945c3a9b5f0b49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed3dc6f8498df3ac8019e78cae2a6e140773201722032856ff80d2c4d4c9bfb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ebf13c9065fc854c80964fa27346f84864e34b26f29a681987fd5b6ab51f1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f419ee88bdfc2d1ebd5b9a080ce2342707eabe5e69f4f0cfcb2254444db21a00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f187812442a9fa253acfa2004359c7e226802447c1b8703aa6141addf95885(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fecb65b452dabd3e0dcbfd5a78d9f8923d0fbc0e8ad2365d7d763d18b56aa52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9366b004ef2e92c8d6159f0a9e43a5cad933a8d06c60cd54c69fc0c9f3d8ef3d(
    value: typing.Optional[CceNodeAttachV3RootVolume],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784d2719d963496233e2da9a44251c6fd441bc1afc55e086f11dc6061c41c06b(
    *,
    groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3StorageGroups, typing.Dict[builtins.str, typing.Any]]]],
    selectors: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3StorageSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71f281a919d8f55282457d1b56725ed41fb10f95864b8f701c4f27773ed0766(
    *,
    name: builtins.str,
    selector_names: typing.Sequence[builtins.str],
    virtual_spaces: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3StorageGroupsVirtualSpaces, typing.Dict[builtins.str, typing.Any]]]],
    cce_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95880b6acfb99027cd114b86f3369f0b3315fd13e886d41db8966b59d6f73091(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6067aeb9b39714c3627d0b9efd28f7482b34b5e7d718d6bad3c67cd64699ce8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7dcb3b2927ab6df892c52b9fb8aa208ae2474296fd7b14e6d62599b0eef1c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da22bb72c3016592022ab266f29a9d067932bc4960906e11b42549d035744b0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059319ede4fef68704fb0c3958d19c1e6b51232b78a80076970e2063b0c846e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4f3cb3efbd4be97551c034008a5ab32cb5702ca182228275e127aca795cf1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49959fb42e1609316be52ab7177ac34f9e0dea4559f468ffeb36dd331a2b5641(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c497760ea0994f07c773419315bdfd6de688504efdd8c13c9d8fec0ed8b422(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3StorageGroupsVirtualSpaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6afb7c179cad294e03b2352632f755ea7bff4ad7ec450c853745a68aa4c23a22(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc18960207f5110897f7f7737800d21d99de1ff3f4d2edd7665751e92caeb15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1813daa1d04dde2d030426e268edb32bb490fa8aabaa30a92ff70cbae0d48607(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d847e2eceedd766ba70b69e0cf995bbb895e60d377626934d09e4992ff4c15c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d530945b8531349a29cf2e81d83e4450d63965ba7957c2ac862dcb50ba958b(
    *,
    name: builtins.str,
    size: builtins.str,
    lvm_lv_type: typing.Optional[builtins.str] = None,
    lvm_path: typing.Optional[builtins.str] = None,
    runtime_lv_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d36a9f19bf9d00edc91ee3a9454306111e1d64169a6201574a8f6a1e8933447(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2055bb52327a1f84d7dfde333487e5156f056bfc51741acd2abeed7a2ca7942d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1994a6a0464df967162e687fec6a45b6823ec9000965d79411606d594bb774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9729448391f43ecff4b73e3799af002c7b3cf74c1f527d0acfe91648e53b47c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef64f5f295dc8e2047b1570697d59b587177012a7aecf27fd14f8a655228e70(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24243db5d77105bea8a634172df7d7c1c652071cb7a770005d489e2e7fa8b8ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageGroupsVirtualSpaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6d24e7195a38e47d093a5a75c053afe0820395c4f5bd65861644f22c11ae2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3493b653fd174eb0ecb38c6cc21ab074209b0bb405c6876accea1401ad081e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfecd6569b79fc63b02fa7ebfb6753c86ae633d36edfa58fc11607b9cfc89c60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74fc1cd107ecfacafb9728198faa20a11bf11f8e48475aa0dd0f3dac73570ee6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1fc94aae9cc0dc60366bbba1bb317d5dae353c57f34ad31bda88f641b49ddb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbae5ed3103a4985f69007c73da678aebc420859f1255b10dee57295b6e7348f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fd58adfb2a250e4531d4898af4e9ed80dd89ad6857f930cf86053c14a4e5eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageGroupsVirtualSpaces]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ec5033284206fc7639341338d9727a8ae9de00a59b9e51bb70afca89c0842a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a85f3c727445f1fc24e8370cf74cd8a51da7706c6fd86c70d8f6fed5e42da97(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3StorageGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb332f2cac04e9977f2793ed63f1e7db704f3f86802a5b6efe8645d45385ed03(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CceNodeAttachV3StorageSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491cee4abe97fcc5e5326a27cba3939cb4f5ce01d6d9f99fb38d70bea227f348(
    value: typing.Optional[CceNodeAttachV3Storage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38eb1d5ee70139a9814f943d71cf45d90a8e5b707447444e912bb4bd1c76d0ed(
    *,
    name: builtins.str,
    match_label_count: typing.Optional[builtins.str] = None,
    match_label_metadata_cmkid: typing.Optional[builtins.str] = None,
    match_label_metadata_encrypted: typing.Optional[builtins.str] = None,
    match_label_size: typing.Optional[builtins.str] = None,
    match_label_volume_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396fb2de347d7e503c3adf8b8e78fa4699d443c26d51e14ee342a44866ab47a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3efb7355529912f16b3e24f4b662e019124877006ec8ca666a76640faa69c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0d5a2b6bfa49584291aeb6ac9935cf7c1a8ef2b3c0a954b62182666c4a5c07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42f1f7755784e73d6afee82d6fe42084184183c727766999e68db0b914d93241(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d6c2268a58e36d2f0e39d0810cdb84892ed4b92c6b13f21be4abe5ca61a536(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d08dc5dfa3647bbe94c85b82be450e15d4abd3fbc6152f0b7385bce434b341(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3StorageSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a183fef8f34f176884a155dfd0273d44b9971de4147604f58bb7a7c05b7686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c4d3bcf8b1dc2f25474718d0adcb85a7cad02facfe3d737f9105eadb9afbb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d60c676b2b545ab361f7f122a6a366c4e63047a474c6bc12e4691e53e20e31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e250808d3e65087497c8539dfae10aef2869af73d1062e30e2abd83d1cf872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bc71d3bdee1afad6e33c2f89dde208f4826913a34e64d665d2a093c7b1aaca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80648a3870aa3829be322688902fa7f31348d6362aaef72e7c552b6b8626a58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65038878d6bdeee0ee86a62d9fd92258a6273a4b2c59f6e13f75800e1c399df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4a7b9bb48965d6e01b616d338f72d44f006fc8fd3dd9a454ac6e1f4d8c390a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b705eb5f8155ab47861c9561f94bb2c9d29daa0f7a84dea03399444c6be471d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3StorageSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47da96db44c57f1ac5c9665d46a0f169eadd3f095695addad779b9881ff00a0(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3205d307d703530d14118541994f59f86219cc25a6c71da72db096229d332f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb8a3ae370e8756f88c6c13986cf15a3fd12b9ed5eec6596daefd5b3d768cac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67cb6a21a3c6ebcf535597a239e67fe2340b8485d9f67eb9ad21e10ae423867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5183328a195c001885a92e54c22bd07a6582443f1fe536aa7af87064a99779a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__495ac56a2e8cfd1041ebe230f12d8aecc3ca03d97a0deadfab2c70326a498b1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1bb58aa7268f6f8428d5e4515c9893e3776266e839260a879b76b159e3267f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CceNodeAttachV3Taints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022ab7ebe5d215bc879f0e8a5cb3819b0367e3dcc08117d36f854bed28fc4564(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39233223d0236f51d34197840b842cbf7fc95a018b1c839aca24c437cea71c31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a99325bbcc154088bb052bc2eb7f71def60999eecf086a975e79941dd905986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a193fd1695a9d66b216dc4f573c21542519ae262116c644e3f3b74f75ae15b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730c13b67fefdc8a1f1dc330fc60d8aa8595b2bb5e2fb2cf68b335dfb187963e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3Taints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e15862624ce22b449e6a5a16fa8293882a87d9e0437bf9c8e2977bdc0dcec3d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1394bec3b171c861814c1b0969231d8b8ee64c58c3cdf36c3015e501a7536816(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27926b292f9e700af825c04da0cd368081b397183ca48167873f5511d263ce0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3960b78d4f192a4e96ba62158ded6c0233a0f5ce4457eeb69aacb4a2d945008b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab326aebaaf119105f40ae7177be1cf543d2073fd1a784a6edfc8f6d4019773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679cf19e59aaa3df6d701ebb2ab767c59193b5322832693e614f29a67460feb0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CceNodeAttachV3Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
