r'''
# `opentelekomcloud_fgs_function_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_fgs_function_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2).
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


class FgsFunctionV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2 opentelekomcloud_fgs_function_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        memory_size: jsii.Number,
        name: builtins.str,
        runtime: builtins.str,
        timeout: jsii.Number,
        agency: typing.Optional[builtins.str] = None,
        app: typing.Optional[builtins.str] = None,
        app_agency: typing.Optional[builtins.str] = None,
        code_filename: typing.Optional[builtins.str] = None,
        code_type: typing.Optional[builtins.str] = None,
        code_url: typing.Optional[builtins.str] = None,
        concurrency_num: typing.Optional[jsii.Number] = None,
        custom_image: typing.Optional[typing.Union["FgsFunctionV2CustomImage", typing.Dict[builtins.str, typing.Any]]] = None,
        depend_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_dynamic_memory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encrypted_user_data: typing.Optional[builtins.str] = None,
        func_code: typing.Optional[builtins.str] = None,
        func_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2FuncMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        functiongraph_version: typing.Optional[builtins.str] = None,
        gpu_memory: typing.Optional[jsii.Number] = None,
        handler: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initializer_handler: typing.Optional[builtins.str] = None,
        initializer_timeout: typing.Optional[jsii.Number] = None,
        log_group_id: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_topic_id: typing.Optional[builtins.str] = None,
        log_topic_name: typing.Optional[builtins.str] = None,
        max_instance_num: typing.Optional[builtins.str] = None,
        mount_user_group_id: typing.Optional[jsii.Number] = None,
        mount_user_id: typing.Optional[jsii.Number] = None,
        network_controller: typing.Optional[typing.Union["FgsFunctionV2NetworkController", typing.Dict[builtins.str, typing.Any]]] = None,
        network_id: typing.Optional[builtins.str] = None,
        peering_cidr: typing.Optional[builtins.str] = None,
        pre_stop_handler: typing.Optional[builtins.str] = None,
        pre_stop_timeout: typing.Optional[jsii.Number] = None,
        reserved_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2ReservedInstances", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FgsFunctionV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
        versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2Versions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2 opentelekomcloud_fgs_function_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param memory_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#memory_size FgsFunctionV2#memory_size}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#runtime FgsFunctionV2#runtime}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#timeout FgsFunctionV2#timeout}.
        :param agency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#agency FgsFunctionV2#agency}.
        :param app: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#app FgsFunctionV2#app}.
        :param app_agency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#app_agency FgsFunctionV2#app_agency}.
        :param code_filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_filename FgsFunctionV2#code_filename}.
        :param code_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_type FgsFunctionV2#code_type}.
        :param code_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_url FgsFunctionV2#code_url}.
        :param concurrency_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#concurrency_num FgsFunctionV2#concurrency_num}.
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#custom_image FgsFunctionV2#custom_image}
        :param depend_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#depend_list FgsFunctionV2#depend_list}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#description FgsFunctionV2#description}.
        :param enable_dynamic_memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#enable_dynamic_memory FgsFunctionV2#enable_dynamic_memory}.
        :param encrypted_user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#encrypted_user_data FgsFunctionV2#encrypted_user_data}.
        :param func_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#func_code FgsFunctionV2#func_code}.
        :param func_mounts: func_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#func_mounts FgsFunctionV2#func_mounts}
        :param functiongraph_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#functiongraph_version FgsFunctionV2#functiongraph_version}.
        :param gpu_memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#gpu_memory FgsFunctionV2#gpu_memory}.
        :param handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#handler FgsFunctionV2#handler}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#id FgsFunctionV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initializer_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#initializer_handler FgsFunctionV2#initializer_handler}.
        :param initializer_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#initializer_timeout FgsFunctionV2#initializer_timeout}.
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_group_id FgsFunctionV2#log_group_id}.
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_group_name FgsFunctionV2#log_group_name}.
        :param log_topic_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_topic_id FgsFunctionV2#log_topic_id}.
        :param log_topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_topic_name FgsFunctionV2#log_topic_name}.
        :param max_instance_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#max_instance_num FgsFunctionV2#max_instance_num}.
        :param mount_user_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_user_group_id FgsFunctionV2#mount_user_group_id}.
        :param mount_user_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_user_id FgsFunctionV2#mount_user_id}.
        :param network_controller: network_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#network_controller FgsFunctionV2#network_controller}
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#network_id FgsFunctionV2#network_id}.
        :param peering_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#peering_cidr FgsFunctionV2#peering_cidr}.
        :param pre_stop_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#pre_stop_handler FgsFunctionV2#pre_stop_handler}.
        :param pre_stop_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#pre_stop_timeout FgsFunctionV2#pre_stop_timeout}.
        :param reserved_instances: reserved_instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#reserved_instances FgsFunctionV2#reserved_instances}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#tags FgsFunctionV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#timeouts FgsFunctionV2#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#user_data FgsFunctionV2#user_data}.
        :param versions: versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#versions FgsFunctionV2#versions}
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#vpc_id FgsFunctionV2#vpc_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47922e73245a00d256b7f271d3ba3ca26a58540e6850ffd5f58783c4a7249b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FgsFunctionV2Config(
            memory_size=memory_size,
            name=name,
            runtime=runtime,
            timeout=timeout,
            agency=agency,
            app=app,
            app_agency=app_agency,
            code_filename=code_filename,
            code_type=code_type,
            code_url=code_url,
            concurrency_num=concurrency_num,
            custom_image=custom_image,
            depend_list=depend_list,
            description=description,
            enable_dynamic_memory=enable_dynamic_memory,
            encrypted_user_data=encrypted_user_data,
            func_code=func_code,
            func_mounts=func_mounts,
            functiongraph_version=functiongraph_version,
            gpu_memory=gpu_memory,
            handler=handler,
            id=id,
            initializer_handler=initializer_handler,
            initializer_timeout=initializer_timeout,
            log_group_id=log_group_id,
            log_group_name=log_group_name,
            log_topic_id=log_topic_id,
            log_topic_name=log_topic_name,
            max_instance_num=max_instance_num,
            mount_user_group_id=mount_user_group_id,
            mount_user_id=mount_user_id,
            network_controller=network_controller,
            network_id=network_id,
            peering_cidr=peering_cidr,
            pre_stop_handler=pre_stop_handler,
            pre_stop_timeout=pre_stop_timeout,
            reserved_instances=reserved_instances,
            tags=tags,
            timeouts=timeouts,
            user_data=user_data,
            versions=versions,
            vpc_id=vpc_id,
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
        '''Generates CDKTF code for importing a FgsFunctionV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FgsFunctionV2 to import.
        :param import_from_id: The id of the existing FgsFunctionV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FgsFunctionV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5fcb204eb144eef582ef3ba6d0fb1d6fd783096dbf20ca8803c4fc505052bd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCustomImage")
    def put_custom_image(
        self,
        *,
        url: builtins.str,
        args: typing.Optional[builtins.str] = None,
        command: typing.Optional[builtins.str] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#url FgsFunctionV2#url}.
        :param args: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#args FgsFunctionV2#args}.
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#command FgsFunctionV2#command}.
        :param working_dir: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#working_dir FgsFunctionV2#working_dir}.
        '''
        value = FgsFunctionV2CustomImage(
            url=url, args=args, command=command, working_dir=working_dir
        )

        return typing.cast(None, jsii.invoke(self, "putCustomImage", [value]))

    @jsii.member(jsii_name="putFuncMounts")
    def put_func_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2FuncMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e0809ef6329153d82ac25fc1686576563281fec941a74f27d10ac9f9ef20cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFuncMounts", [value]))

    @jsii.member(jsii_name="putNetworkController")
    def put_network_controller(
        self,
        *,
        disable_public_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trigger_access_vpcs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2NetworkControllerTriggerAccessVpcs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param disable_public_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#disable_public_network FgsFunctionV2#disable_public_network}.
        :param trigger_access_vpcs: trigger_access_vpcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#trigger_access_vpcs FgsFunctionV2#trigger_access_vpcs}
        '''
        value = FgsFunctionV2NetworkController(
            disable_public_network=disable_public_network,
            trigger_access_vpcs=trigger_access_vpcs,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkController", [value]))

    @jsii.member(jsii_name="putReservedInstances")
    def put_reserved_instances(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2ReservedInstances", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1ef039a087eee0221c6cd8a6a7b773c0c96c4619193187a76841e1965906a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReservedInstances", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#create FgsFunctionV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#delete FgsFunctionV2#delete}.
        '''
        value = FgsFunctionV2Timeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVersions")
    def put_versions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2Versions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__926ee800ce53b72e63d68dfaa13102ad8a9808f1b4a606a87ee4b7dc0896d812)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVersions", [value]))

    @jsii.member(jsii_name="resetAgency")
    def reset_agency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgency", []))

    @jsii.member(jsii_name="resetApp")
    def reset_app(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApp", []))

    @jsii.member(jsii_name="resetAppAgency")
    def reset_app_agency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppAgency", []))

    @jsii.member(jsii_name="resetCodeFilename")
    def reset_code_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeFilename", []))

    @jsii.member(jsii_name="resetCodeType")
    def reset_code_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeType", []))

    @jsii.member(jsii_name="resetCodeUrl")
    def reset_code_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeUrl", []))

    @jsii.member(jsii_name="resetConcurrencyNum")
    def reset_concurrency_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConcurrencyNum", []))

    @jsii.member(jsii_name="resetCustomImage")
    def reset_custom_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomImage", []))

    @jsii.member(jsii_name="resetDependList")
    def reset_depend_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependList", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnableDynamicMemory")
    def reset_enable_dynamic_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableDynamicMemory", []))

    @jsii.member(jsii_name="resetEncryptedUserData")
    def reset_encrypted_user_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptedUserData", []))

    @jsii.member(jsii_name="resetFuncCode")
    def reset_func_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFuncCode", []))

    @jsii.member(jsii_name="resetFuncMounts")
    def reset_func_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFuncMounts", []))

    @jsii.member(jsii_name="resetFunctiongraphVersion")
    def reset_functiongraph_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctiongraphVersion", []))

    @jsii.member(jsii_name="resetGpuMemory")
    def reset_gpu_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuMemory", []))

    @jsii.member(jsii_name="resetHandler")
    def reset_handler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHandler", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInitializerHandler")
    def reset_initializer_handler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializerHandler", []))

    @jsii.member(jsii_name="resetInitializerTimeout")
    def reset_initializer_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitializerTimeout", []))

    @jsii.member(jsii_name="resetLogGroupId")
    def reset_log_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupId", []))

    @jsii.member(jsii_name="resetLogGroupName")
    def reset_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogGroupName", []))

    @jsii.member(jsii_name="resetLogTopicId")
    def reset_log_topic_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogTopicId", []))

    @jsii.member(jsii_name="resetLogTopicName")
    def reset_log_topic_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogTopicName", []))

    @jsii.member(jsii_name="resetMaxInstanceNum")
    def reset_max_instance_num(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceNum", []))

    @jsii.member(jsii_name="resetMountUserGroupId")
    def reset_mount_user_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountUserGroupId", []))

    @jsii.member(jsii_name="resetMountUserId")
    def reset_mount_user_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountUserId", []))

    @jsii.member(jsii_name="resetNetworkController")
    def reset_network_controller(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkController", []))

    @jsii.member(jsii_name="resetNetworkId")
    def reset_network_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkId", []))

    @jsii.member(jsii_name="resetPeeringCidr")
    def reset_peering_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeeringCidr", []))

    @jsii.member(jsii_name="resetPreStopHandler")
    def reset_pre_stop_handler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreStopHandler", []))

    @jsii.member(jsii_name="resetPreStopTimeout")
    def reset_pre_stop_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreStopTimeout", []))

    @jsii.member(jsii_name="resetReservedInstances")
    def reset_reserved_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedInstances", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserData")
    def reset_user_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserData", []))

    @jsii.member(jsii_name="resetVersions")
    def reset_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersions", []))

    @jsii.member(jsii_name="resetVpcId")
    def reset_vpc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcId", []))

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
    @jsii.member(jsii_name="allowEphemeralStorage")
    def allow_ephemeral_storage(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowEphemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="apigRouteEnable")
    def apig_route_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "apigRouteEnable"))

    @builtins.property
    @jsii.member(jsii_name="customImage")
    def custom_image(self) -> "FgsFunctionV2CustomImageOutputReference":
        return typing.cast("FgsFunctionV2CustomImageOutputReference", jsii.get(self, "customImage"))

    @builtins.property
    @jsii.member(jsii_name="dnsList")
    def dns_list(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsList"))

    @builtins.property
    @jsii.member(jsii_name="enableAuthInHeader")
    def enable_auth_in_header(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableAuthInHeader"))

    @builtins.property
    @jsii.member(jsii_name="enableClassIsolation")
    def enable_class_isolation(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableClassIsolation"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ephemeralStorage"))

    @builtins.property
    @jsii.member(jsii_name="extendConfig")
    def extend_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extendConfig"))

    @builtins.property
    @jsii.member(jsii_name="funcMounts")
    def func_mounts(self) -> "FgsFunctionV2FuncMountsList":
        return typing.cast("FgsFunctionV2FuncMountsList", jsii.get(self, "funcMounts"))

    @builtins.property
    @jsii.member(jsii_name="gpuType")
    def gpu_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpuType"))

    @builtins.property
    @jsii.member(jsii_name="heartbeatHandler")
    def heartbeat_handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "heartbeatHandler"))

    @builtins.property
    @jsii.member(jsii_name="isStatefulFunction")
    def is_stateful_function(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isStatefulFunction"))

    @builtins.property
    @jsii.member(jsii_name="networkController")
    def network_controller(self) -> "FgsFunctionV2NetworkControllerOutputReference":
        return typing.cast("FgsFunctionV2NetworkControllerOutputReference", jsii.get(self, "networkController"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="reservedInstances")
    def reserved_instances(self) -> "FgsFunctionV2ReservedInstancesList":
        return typing.cast("FgsFunctionV2ReservedInstancesList", jsii.get(self, "reservedInstances"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FgsFunctionV2TimeoutsOutputReference":
        return typing.cast("FgsFunctionV2TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="urn")
    def urn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urn"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="versions")
    def versions(self) -> "FgsFunctionV2VersionsList":
        return typing.cast("FgsFunctionV2VersionsList", jsii.get(self, "versions"))

    @builtins.property
    @jsii.member(jsii_name="agencyInput")
    def agency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agencyInput"))

    @builtins.property
    @jsii.member(jsii_name="appAgencyInput")
    def app_agency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appAgencyInput"))

    @builtins.property
    @jsii.member(jsii_name="appInput")
    def app_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appInput"))

    @builtins.property
    @jsii.member(jsii_name="codeFilenameInput")
    def code_filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeFilenameInput"))

    @builtins.property
    @jsii.member(jsii_name="codeTypeInput")
    def code_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="codeUrlInput")
    def code_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "codeUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="concurrencyNumInput")
    def concurrency_num_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "concurrencyNumInput"))

    @builtins.property
    @jsii.member(jsii_name="customImageInput")
    def custom_image_input(self) -> typing.Optional["FgsFunctionV2CustomImage"]:
        return typing.cast(typing.Optional["FgsFunctionV2CustomImage"], jsii.get(self, "customImageInput"))

    @builtins.property
    @jsii.member(jsii_name="dependListInput")
    def depend_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependListInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableDynamicMemoryInput")
    def enable_dynamic_memory_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableDynamicMemoryInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedUserDataInput")
    def encrypted_user_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptedUserDataInput"))

    @builtins.property
    @jsii.member(jsii_name="funcCodeInput")
    def func_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "funcCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="funcMountsInput")
    def func_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2FuncMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2FuncMounts"]]], jsii.get(self, "funcMountsInput"))

    @builtins.property
    @jsii.member(jsii_name="functiongraphVersionInput")
    def functiongraph_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functiongraphVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuMemoryInput")
    def gpu_memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpuMemoryInput"))

    @builtins.property
    @jsii.member(jsii_name="handlerInput")
    def handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handlerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initializerHandlerInput")
    def initializer_handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "initializerHandlerInput"))

    @builtins.property
    @jsii.member(jsii_name="initializerTimeoutInput")
    def initializer_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initializerTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupIdInput")
    def log_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupNameInput")
    def log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="logTopicIdInput")
    def log_topic_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTopicIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logTopicNameInput")
    def log_topic_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logTopicNameInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceNumInput")
    def max_instance_num_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxInstanceNumInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySizeInput")
    def memory_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySizeInput"))

    @builtins.property
    @jsii.member(jsii_name="mountUserGroupIdInput")
    def mount_user_group_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mountUserGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mountUserIdInput")
    def mount_user_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mountUserIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkControllerInput")
    def network_controller_input(
        self,
    ) -> typing.Optional["FgsFunctionV2NetworkController"]:
        return typing.cast(typing.Optional["FgsFunctionV2NetworkController"], jsii.get(self, "networkControllerInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peeringCidrInput")
    def peering_cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeringCidrInput"))

    @builtins.property
    @jsii.member(jsii_name="preStopHandlerInput")
    def pre_stop_handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preStopHandlerInput"))

    @builtins.property
    @jsii.member(jsii_name="preStopTimeoutInput")
    def pre_stop_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "preStopTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedInstancesInput")
    def reserved_instances_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2ReservedInstances"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2ReservedInstances"]]], jsii.get(self, "reservedInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FgsFunctionV2Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FgsFunctionV2Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userDataInput")
    def user_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userDataInput"))

    @builtins.property
    @jsii.member(jsii_name="versionsInput")
    def versions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2Versions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2Versions"]]], jsii.get(self, "versionsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="agency")
    def agency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agency"))

    @agency.setter
    def agency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f373b1340354778405eeb0fad6bf55e9b3d623c569879398f32a1ca0bf47d61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="app")
    def app(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "app"))

    @app.setter
    def app(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f3fe0e0aac9aa97afe6896704e3ab7017bd675d50c43736f7051287466f093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "app", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appAgency")
    def app_agency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appAgency"))

    @app_agency.setter
    def app_agency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a396c68f19f65ecc014e4af8e4a53fdc91bd9f2e68a7fe9908375c9465815106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appAgency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeFilename")
    def code_filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codeFilename"))

    @code_filename.setter
    def code_filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1763affe3cbc2ae9269cd0820353b4d197e6b68274acb767f1eaf9c12de22eab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeFilename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeType")
    def code_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codeType"))

    @code_type.setter
    def code_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa8dc3f8a3cf82ba0c080747060d69087c46194124fb85f668aabe59199b5ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="codeUrl")
    def code_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "codeUrl"))

    @code_url.setter
    def code_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8be754646f543f9f44cf01059dea1bef8a4dbf1e4d6bd09ab69d618e1e531e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codeUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="concurrencyNum")
    def concurrency_num(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "concurrencyNum"))

    @concurrency_num.setter
    def concurrency_num(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14037f6229d2a550511b84a05aaa3ac80cdb3a20173234168948bc82dc71e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "concurrencyNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependList")
    def depend_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependList"))

    @depend_list.setter
    def depend_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e76cbdb78435007f8531426f7fa2efefef352a19cf9a348f293d39895b5d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01178bb2108740e1afaa89baa5c88589b4c003077dc2496f3e8d224bb9fc87b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableDynamicMemory")
    def enable_dynamic_memory(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableDynamicMemory"))

    @enable_dynamic_memory.setter
    def enable_dynamic_memory(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdb435302cbcf4b90b9b9602e1cc6bc8ff8e0bc166b5d3485cc3ddc0c1da3cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDynamicMemory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptedUserData")
    def encrypted_user_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptedUserData"))

    @encrypted_user_data.setter
    def encrypted_user_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19002f94d94aa615505751062586b5257fb3704d0d42b44309bd02ce213c9fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptedUserData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="funcCode")
    def func_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "funcCode"))

    @func_code.setter
    def func_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900ee1038835483ba79a56b31f96fbf37cf07a33f1982740006ffa7d14b20ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "funcCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functiongraphVersion")
    def functiongraph_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functiongraphVersion"))

    @functiongraph_version.setter
    def functiongraph_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ee53159016798f1f87317e908a3fa9ff50294c5a72d0052a3cd749a5f82e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functiongraphVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpuMemory")
    def gpu_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gpuMemory"))

    @gpu_memory.setter
    def gpu_memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e8f65444d70b99eb30951b6b2dc1adf0cfc95d06c8480fae4935c6915e56c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuMemory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68c506ab728ff601c70a5c8e069fb611061f8a6e55d312d06a978b64ad87168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c409cd030ecde6bae6cc9a55b6ddd5514a6233a49d7db0a928013ec52963bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initializerHandler")
    def initializer_handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initializerHandler"))

    @initializer_handler.setter
    def initializer_handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__748822ca0fa57c084b7cec5442d7c0cd92d14450ac4603059366bf276ebc924c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initializerHandler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initializerTimeout")
    def initializer_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initializerTimeout"))

    @initializer_timeout.setter
    def initializer_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40d145748b06679e346c0ab072594d7c56003d3a73119578d6573d39f8a339b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initializerTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupId")
    def log_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupId"))

    @log_group_id.setter
    def log_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66d6077a57efa024c7907b003e123653650d434cd5ca4799893f3b8c1b2a63a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupName"))

    @log_group_name.setter
    def log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b3ae971a966813d5129a90628fbe159638953878d1ec6beab58f1cd6ac0f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logTopicId")
    def log_topic_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logTopicId"))

    @log_topic_id.setter
    def log_topic_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96fd28c4a0aac9fe3fff4192f081d94f937be0e8f44690bb8ee62936efaacf1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logTopicId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logTopicName")
    def log_topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logTopicName"))

    @log_topic_name.setter
    def log_topic_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6e438df19d880201d1db01029e333ea9ca7f197b4485311cd18119757e9156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logTopicName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceNum")
    def max_instance_num(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxInstanceNum"))

    @max_instance_num.setter
    def max_instance_num(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5ebfafdd4b2e3fdb5ab0e1bcaaa5cc034db1fad079914345525030c9c19d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceNum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySize"))

    @memory_size.setter
    def memory_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc6f261ffdab4b9cd49366477da047350b1b0a489d3996dd8dcd27e996e3b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountUserGroupId")
    def mount_user_group_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mountUserGroupId"))

    @mount_user_group_id.setter
    def mount_user_group_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d04e969c5f5c0afab7e7418a8ce61edaefddfefaaade02944b5e2a224d35fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountUserGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountUserId")
    def mount_user_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mountUserId"))

    @mount_user_id.setter
    def mount_user_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954a996bf12dfc597ae3812e36538509cf5ae5e38069f925d22f98d703f8e74a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountUserId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf195fab5f015fe672299859f54c6740d5c22e3d35183c777d3e347443a30f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b05af13f4fa0d8860cb527f67e2da58039ea463eba1d5986f184e48219c0d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeringCidr")
    def peering_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeringCidr"))

    @peering_cidr.setter
    def peering_cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d473a3468ed3e91b232070aaa6102c55f3b22d1552e20f9150fa462ef1d23a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeringCidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preStopHandler")
    def pre_stop_handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preStopHandler"))

    @pre_stop_handler.setter
    def pre_stop_handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dbeab3fa6af056790f5a0d147c6101966896a07bda419eda73300015075d7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preStopHandler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preStopTimeout")
    def pre_stop_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preStopTimeout"))

    @pre_stop_timeout.setter
    def pre_stop_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332fe459c6a0d4a65b5efb96c80f8425e49febca976c49990b52779831792d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preStopTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b893acf3c20ba52104a37e8fae8e17dd6edfd7251bf64536eb3da768d6d3f450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121b1a5b928d14e607e27dc802ca95e659dc2a0f096812095fc7101804ddf6fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad217e4fc65e2f8cdd6ff3ce1644732a761a2e6c5b155f40b7ea7d05695fbb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userData")
    def user_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userData"))

    @user_data.setter
    def user_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456beedc1d43336ef3115559fa4655e181fc3b1743fb7f8cb9fb265754bc875e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userData", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb07a132920b4512eb1be7b66771963d551c7b05d822418dc509cd2782ebbc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "memory_size": "memorySize",
        "name": "name",
        "runtime": "runtime",
        "timeout": "timeout",
        "agency": "agency",
        "app": "app",
        "app_agency": "appAgency",
        "code_filename": "codeFilename",
        "code_type": "codeType",
        "code_url": "codeUrl",
        "concurrency_num": "concurrencyNum",
        "custom_image": "customImage",
        "depend_list": "dependList",
        "description": "description",
        "enable_dynamic_memory": "enableDynamicMemory",
        "encrypted_user_data": "encryptedUserData",
        "func_code": "funcCode",
        "func_mounts": "funcMounts",
        "functiongraph_version": "functiongraphVersion",
        "gpu_memory": "gpuMemory",
        "handler": "handler",
        "id": "id",
        "initializer_handler": "initializerHandler",
        "initializer_timeout": "initializerTimeout",
        "log_group_id": "logGroupId",
        "log_group_name": "logGroupName",
        "log_topic_id": "logTopicId",
        "log_topic_name": "logTopicName",
        "max_instance_num": "maxInstanceNum",
        "mount_user_group_id": "mountUserGroupId",
        "mount_user_id": "mountUserId",
        "network_controller": "networkController",
        "network_id": "networkId",
        "peering_cidr": "peeringCidr",
        "pre_stop_handler": "preStopHandler",
        "pre_stop_timeout": "preStopTimeout",
        "reserved_instances": "reservedInstances",
        "tags": "tags",
        "timeouts": "timeouts",
        "user_data": "userData",
        "versions": "versions",
        "vpc_id": "vpcId",
    },
)
class FgsFunctionV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        memory_size: jsii.Number,
        name: builtins.str,
        runtime: builtins.str,
        timeout: jsii.Number,
        agency: typing.Optional[builtins.str] = None,
        app: typing.Optional[builtins.str] = None,
        app_agency: typing.Optional[builtins.str] = None,
        code_filename: typing.Optional[builtins.str] = None,
        code_type: typing.Optional[builtins.str] = None,
        code_url: typing.Optional[builtins.str] = None,
        concurrency_num: typing.Optional[jsii.Number] = None,
        custom_image: typing.Optional[typing.Union["FgsFunctionV2CustomImage", typing.Dict[builtins.str, typing.Any]]] = None,
        depend_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_dynamic_memory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encrypted_user_data: typing.Optional[builtins.str] = None,
        func_code: typing.Optional[builtins.str] = None,
        func_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2FuncMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        functiongraph_version: typing.Optional[builtins.str] = None,
        gpu_memory: typing.Optional[jsii.Number] = None,
        handler: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        initializer_handler: typing.Optional[builtins.str] = None,
        initializer_timeout: typing.Optional[jsii.Number] = None,
        log_group_id: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_topic_id: typing.Optional[builtins.str] = None,
        log_topic_name: typing.Optional[builtins.str] = None,
        max_instance_num: typing.Optional[builtins.str] = None,
        mount_user_group_id: typing.Optional[jsii.Number] = None,
        mount_user_id: typing.Optional[jsii.Number] = None,
        network_controller: typing.Optional[typing.Union["FgsFunctionV2NetworkController", typing.Dict[builtins.str, typing.Any]]] = None,
        network_id: typing.Optional[builtins.str] = None,
        peering_cidr: typing.Optional[builtins.str] = None,
        pre_stop_handler: typing.Optional[builtins.str] = None,
        pre_stop_timeout: typing.Optional[jsii.Number] = None,
        reserved_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2ReservedInstances", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FgsFunctionV2Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_data: typing.Optional[builtins.str] = None,
        versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2Versions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param memory_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#memory_size FgsFunctionV2#memory_size}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}.
        :param runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#runtime FgsFunctionV2#runtime}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#timeout FgsFunctionV2#timeout}.
        :param agency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#agency FgsFunctionV2#agency}.
        :param app: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#app FgsFunctionV2#app}.
        :param app_agency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#app_agency FgsFunctionV2#app_agency}.
        :param code_filename: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_filename FgsFunctionV2#code_filename}.
        :param code_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_type FgsFunctionV2#code_type}.
        :param code_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_url FgsFunctionV2#code_url}.
        :param concurrency_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#concurrency_num FgsFunctionV2#concurrency_num}.
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#custom_image FgsFunctionV2#custom_image}
        :param depend_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#depend_list FgsFunctionV2#depend_list}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#description FgsFunctionV2#description}.
        :param enable_dynamic_memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#enable_dynamic_memory FgsFunctionV2#enable_dynamic_memory}.
        :param encrypted_user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#encrypted_user_data FgsFunctionV2#encrypted_user_data}.
        :param func_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#func_code FgsFunctionV2#func_code}.
        :param func_mounts: func_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#func_mounts FgsFunctionV2#func_mounts}
        :param functiongraph_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#functiongraph_version FgsFunctionV2#functiongraph_version}.
        :param gpu_memory: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#gpu_memory FgsFunctionV2#gpu_memory}.
        :param handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#handler FgsFunctionV2#handler}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#id FgsFunctionV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param initializer_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#initializer_handler FgsFunctionV2#initializer_handler}.
        :param initializer_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#initializer_timeout FgsFunctionV2#initializer_timeout}.
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_group_id FgsFunctionV2#log_group_id}.
        :param log_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_group_name FgsFunctionV2#log_group_name}.
        :param log_topic_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_topic_id FgsFunctionV2#log_topic_id}.
        :param log_topic_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_topic_name FgsFunctionV2#log_topic_name}.
        :param max_instance_num: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#max_instance_num FgsFunctionV2#max_instance_num}.
        :param mount_user_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_user_group_id FgsFunctionV2#mount_user_group_id}.
        :param mount_user_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_user_id FgsFunctionV2#mount_user_id}.
        :param network_controller: network_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#network_controller FgsFunctionV2#network_controller}
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#network_id FgsFunctionV2#network_id}.
        :param peering_cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#peering_cidr FgsFunctionV2#peering_cidr}.
        :param pre_stop_handler: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#pre_stop_handler FgsFunctionV2#pre_stop_handler}.
        :param pre_stop_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#pre_stop_timeout FgsFunctionV2#pre_stop_timeout}.
        :param reserved_instances: reserved_instances block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#reserved_instances FgsFunctionV2#reserved_instances}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#tags FgsFunctionV2#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#timeouts FgsFunctionV2#timeouts}
        :param user_data: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#user_data FgsFunctionV2#user_data}.
        :param versions: versions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#versions FgsFunctionV2#versions}
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#vpc_id FgsFunctionV2#vpc_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(custom_image, dict):
            custom_image = FgsFunctionV2CustomImage(**custom_image)
        if isinstance(network_controller, dict):
            network_controller = FgsFunctionV2NetworkController(**network_controller)
        if isinstance(timeouts, dict):
            timeouts = FgsFunctionV2Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228c1d4908a19e49c9bb28512aee83a71052b353d2d78f3c45d7126bca03084e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument agency", value=agency, expected_type=type_hints["agency"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument app_agency", value=app_agency, expected_type=type_hints["app_agency"])
            check_type(argname="argument code_filename", value=code_filename, expected_type=type_hints["code_filename"])
            check_type(argname="argument code_type", value=code_type, expected_type=type_hints["code_type"])
            check_type(argname="argument code_url", value=code_url, expected_type=type_hints["code_url"])
            check_type(argname="argument concurrency_num", value=concurrency_num, expected_type=type_hints["concurrency_num"])
            check_type(argname="argument custom_image", value=custom_image, expected_type=type_hints["custom_image"])
            check_type(argname="argument depend_list", value=depend_list, expected_type=type_hints["depend_list"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_dynamic_memory", value=enable_dynamic_memory, expected_type=type_hints["enable_dynamic_memory"])
            check_type(argname="argument encrypted_user_data", value=encrypted_user_data, expected_type=type_hints["encrypted_user_data"])
            check_type(argname="argument func_code", value=func_code, expected_type=type_hints["func_code"])
            check_type(argname="argument func_mounts", value=func_mounts, expected_type=type_hints["func_mounts"])
            check_type(argname="argument functiongraph_version", value=functiongraph_version, expected_type=type_hints["functiongraph_version"])
            check_type(argname="argument gpu_memory", value=gpu_memory, expected_type=type_hints["gpu_memory"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument initializer_handler", value=initializer_handler, expected_type=type_hints["initializer_handler"])
            check_type(argname="argument initializer_timeout", value=initializer_timeout, expected_type=type_hints["initializer_timeout"])
            check_type(argname="argument log_group_id", value=log_group_id, expected_type=type_hints["log_group_id"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_topic_id", value=log_topic_id, expected_type=type_hints["log_topic_id"])
            check_type(argname="argument log_topic_name", value=log_topic_name, expected_type=type_hints["log_topic_name"])
            check_type(argname="argument max_instance_num", value=max_instance_num, expected_type=type_hints["max_instance_num"])
            check_type(argname="argument mount_user_group_id", value=mount_user_group_id, expected_type=type_hints["mount_user_group_id"])
            check_type(argname="argument mount_user_id", value=mount_user_id, expected_type=type_hints["mount_user_id"])
            check_type(argname="argument network_controller", value=network_controller, expected_type=type_hints["network_controller"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument peering_cidr", value=peering_cidr, expected_type=type_hints["peering_cidr"])
            check_type(argname="argument pre_stop_handler", value=pre_stop_handler, expected_type=type_hints["pre_stop_handler"])
            check_type(argname="argument pre_stop_timeout", value=pre_stop_timeout, expected_type=type_hints["pre_stop_timeout"])
            check_type(argname="argument reserved_instances", value=reserved_instances, expected_type=type_hints["reserved_instances"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument versions", value=versions, expected_type=type_hints["versions"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "memory_size": memory_size,
            "name": name,
            "runtime": runtime,
            "timeout": timeout,
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
        if agency is not None:
            self._values["agency"] = agency
        if app is not None:
            self._values["app"] = app
        if app_agency is not None:
            self._values["app_agency"] = app_agency
        if code_filename is not None:
            self._values["code_filename"] = code_filename
        if code_type is not None:
            self._values["code_type"] = code_type
        if code_url is not None:
            self._values["code_url"] = code_url
        if concurrency_num is not None:
            self._values["concurrency_num"] = concurrency_num
        if custom_image is not None:
            self._values["custom_image"] = custom_image
        if depend_list is not None:
            self._values["depend_list"] = depend_list
        if description is not None:
            self._values["description"] = description
        if enable_dynamic_memory is not None:
            self._values["enable_dynamic_memory"] = enable_dynamic_memory
        if encrypted_user_data is not None:
            self._values["encrypted_user_data"] = encrypted_user_data
        if func_code is not None:
            self._values["func_code"] = func_code
        if func_mounts is not None:
            self._values["func_mounts"] = func_mounts
        if functiongraph_version is not None:
            self._values["functiongraph_version"] = functiongraph_version
        if gpu_memory is not None:
            self._values["gpu_memory"] = gpu_memory
        if handler is not None:
            self._values["handler"] = handler
        if id is not None:
            self._values["id"] = id
        if initializer_handler is not None:
            self._values["initializer_handler"] = initializer_handler
        if initializer_timeout is not None:
            self._values["initializer_timeout"] = initializer_timeout
        if log_group_id is not None:
            self._values["log_group_id"] = log_group_id
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_topic_id is not None:
            self._values["log_topic_id"] = log_topic_id
        if log_topic_name is not None:
            self._values["log_topic_name"] = log_topic_name
        if max_instance_num is not None:
            self._values["max_instance_num"] = max_instance_num
        if mount_user_group_id is not None:
            self._values["mount_user_group_id"] = mount_user_group_id
        if mount_user_id is not None:
            self._values["mount_user_id"] = mount_user_id
        if network_controller is not None:
            self._values["network_controller"] = network_controller
        if network_id is not None:
            self._values["network_id"] = network_id
        if peering_cidr is not None:
            self._values["peering_cidr"] = peering_cidr
        if pre_stop_handler is not None:
            self._values["pre_stop_handler"] = pre_stop_handler
        if pre_stop_timeout is not None:
            self._values["pre_stop_timeout"] = pre_stop_timeout
        if reserved_instances is not None:
            self._values["reserved_instances"] = reserved_instances
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_data is not None:
            self._values["user_data"] = user_data
        if versions is not None:
            self._values["versions"] = versions
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

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
    def memory_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#memory_size FgsFunctionV2#memory_size}.'''
        result = self._values.get("memory_size")
        assert result is not None, "Required property 'memory_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#runtime FgsFunctionV2#runtime}.'''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#timeout FgsFunctionV2#timeout}.'''
        result = self._values.get("timeout")
        assert result is not None, "Required property 'timeout' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def agency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#agency FgsFunctionV2#agency}.'''
        result = self._values.get("agency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#app FgsFunctionV2#app}.'''
        result = self._values.get("app")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_agency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#app_agency FgsFunctionV2#app_agency}.'''
        result = self._values.get("app_agency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_filename(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_filename FgsFunctionV2#code_filename}.'''
        result = self._values.get("code_filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_type FgsFunctionV2#code_type}.'''
        result = self._values.get("code_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#code_url FgsFunctionV2#code_url}.'''
        result = self._values.get("code_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def concurrency_num(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#concurrency_num FgsFunctionV2#concurrency_num}.'''
        result = self._values.get("concurrency_num")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def custom_image(self) -> typing.Optional["FgsFunctionV2CustomImage"]:
        '''custom_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#custom_image FgsFunctionV2#custom_image}
        '''
        result = self._values.get("custom_image")
        return typing.cast(typing.Optional["FgsFunctionV2CustomImage"], result)

    @builtins.property
    def depend_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#depend_list FgsFunctionV2#depend_list}.'''
        result = self._values.get("depend_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#description FgsFunctionV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_dynamic_memory(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#enable_dynamic_memory FgsFunctionV2#enable_dynamic_memory}.'''
        result = self._values.get("enable_dynamic_memory")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encrypted_user_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#encrypted_user_data FgsFunctionV2#encrypted_user_data}.'''
        result = self._values.get("encrypted_user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def func_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#func_code FgsFunctionV2#func_code}.'''
        result = self._values.get("func_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def func_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2FuncMounts"]]]:
        '''func_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#func_mounts FgsFunctionV2#func_mounts}
        '''
        result = self._values.get("func_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2FuncMounts"]]], result)

    @builtins.property
    def functiongraph_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#functiongraph_version FgsFunctionV2#functiongraph_version}.'''
        result = self._values.get("functiongraph_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpu_memory(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#gpu_memory FgsFunctionV2#gpu_memory}.'''
        result = self._values.get("gpu_memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#handler FgsFunctionV2#handler}.'''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#id FgsFunctionV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initializer_handler(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#initializer_handler FgsFunctionV2#initializer_handler}.'''
        result = self._values.get("initializer_handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initializer_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#initializer_timeout FgsFunctionV2#initializer_timeout}.'''
        result = self._values.get("initializer_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_group_id FgsFunctionV2#log_group_id}.'''
        result = self._values.get("log_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_group_name FgsFunctionV2#log_group_name}.'''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_topic_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_topic_id FgsFunctionV2#log_topic_id}.'''
        result = self._values.get("log_topic_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_topic_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#log_topic_name FgsFunctionV2#log_topic_name}.'''
        result = self._values.get("log_topic_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_instance_num(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#max_instance_num FgsFunctionV2#max_instance_num}.'''
        result = self._values.get("max_instance_num")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mount_user_group_id(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_user_group_id FgsFunctionV2#mount_user_group_id}.'''
        result = self._values.get("mount_user_group_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mount_user_id(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_user_id FgsFunctionV2#mount_user_id}.'''
        result = self._values.get("mount_user_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_controller(self) -> typing.Optional["FgsFunctionV2NetworkController"]:
        '''network_controller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#network_controller FgsFunctionV2#network_controller}
        '''
        result = self._values.get("network_controller")
        return typing.cast(typing.Optional["FgsFunctionV2NetworkController"], result)

    @builtins.property
    def network_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#network_id FgsFunctionV2#network_id}.'''
        result = self._values.get("network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peering_cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#peering_cidr FgsFunctionV2#peering_cidr}.'''
        result = self._values.get("peering_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_stop_handler(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#pre_stop_handler FgsFunctionV2#pre_stop_handler}.'''
        result = self._values.get("pre_stop_handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_stop_timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#pre_stop_timeout FgsFunctionV2#pre_stop_timeout}.'''
        result = self._values.get("pre_stop_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reserved_instances(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2ReservedInstances"]]]:
        '''reserved_instances block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#reserved_instances FgsFunctionV2#reserved_instances}
        '''
        result = self._values.get("reserved_instances")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2ReservedInstances"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#tags FgsFunctionV2#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FgsFunctionV2Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#timeouts FgsFunctionV2#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FgsFunctionV2Timeouts"], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#user_data FgsFunctionV2#user_data}.'''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def versions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2Versions"]]]:
        '''versions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#versions FgsFunctionV2#versions}
        '''
        result = self._values.get("versions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2Versions"]]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#vpc_id FgsFunctionV2#vpc_id}.'''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2CustomImage",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "args": "args",
        "command": "command",
        "working_dir": "workingDir",
    },
)
class FgsFunctionV2CustomImage:
    def __init__(
        self,
        *,
        url: builtins.str,
        args: typing.Optional[builtins.str] = None,
        command: typing.Optional[builtins.str] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#url FgsFunctionV2#url}.
        :param args: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#args FgsFunctionV2#args}.
        :param command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#command FgsFunctionV2#command}.
        :param working_dir: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#working_dir FgsFunctionV2#working_dir}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1259cc2700c686c31207bc07d6520b12e9e62c845abcfe1598845dba90751c6)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument working_dir", value=working_dir, expected_type=type_hints["working_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#url FgsFunctionV2#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#args FgsFunctionV2#args}.'''
        result = self._values.get("args")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def command(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#command FgsFunctionV2#command}.'''
        result = self._values.get("command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#working_dir FgsFunctionV2#working_dir}.'''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2CustomImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsFunctionV2CustomImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2CustomImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77c2fdc27c666c1383a39ba42f07c2b55c65b8a256135be92a1d4e4548f199fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetWorkingDir")
    def reset_working_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDir", []))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirInput")
    def working_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "args"))

    @args.setter
    def args(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1372aa88d91c5d2ddf214df352db5bd0a02493607a061993773f9361c2e612c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "command"))

    @command.setter
    def command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__214ac0580a3f4cb8b67d536fee533376cebac5c0724421d6b7709d174f9c1364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134569c875ae77d19366e85b750fa7eba19491669c141dc2b0684c01a2b9fde7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42252355ced70547dd05950ee5622b4beaa8e4521fd45a40d0a8a4b8e8b9e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FgsFunctionV2CustomImage]:
        return typing.cast(typing.Optional[FgsFunctionV2CustomImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FgsFunctionV2CustomImage]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed35aefdb873b8879b4a64afdc7c6b309b09d5503f3bcc7545edf21ae1df706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2FuncMounts",
    jsii_struct_bases=[],
    name_mapping={
        "local_mount_path": "localMountPath",
        "mount_resource": "mountResource",
        "mount_share_path": "mountSharePath",
        "mount_type": "mountType",
    },
)
class FgsFunctionV2FuncMounts:
    def __init__(
        self,
        *,
        local_mount_path: builtins.str,
        mount_resource: builtins.str,
        mount_share_path: builtins.str,
        mount_type: builtins.str,
    ) -> None:
        '''
        :param local_mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#local_mount_path FgsFunctionV2#local_mount_path}.
        :param mount_resource: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_resource FgsFunctionV2#mount_resource}.
        :param mount_share_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_share_path FgsFunctionV2#mount_share_path}.
        :param mount_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_type FgsFunctionV2#mount_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa3547ab9b17d65d041982262c8ff1266215add4d14370434ee5b7c2a600909)
            check_type(argname="argument local_mount_path", value=local_mount_path, expected_type=type_hints["local_mount_path"])
            check_type(argname="argument mount_resource", value=mount_resource, expected_type=type_hints["mount_resource"])
            check_type(argname="argument mount_share_path", value=mount_share_path, expected_type=type_hints["mount_share_path"])
            check_type(argname="argument mount_type", value=mount_type, expected_type=type_hints["mount_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_mount_path": local_mount_path,
            "mount_resource": mount_resource,
            "mount_share_path": mount_share_path,
            "mount_type": mount_type,
        }

    @builtins.property
    def local_mount_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#local_mount_path FgsFunctionV2#local_mount_path}.'''
        result = self._values.get("local_mount_path")
        assert result is not None, "Required property 'local_mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_resource(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_resource FgsFunctionV2#mount_resource}.'''
        result = self._values.get("mount_resource")
        assert result is not None, "Required property 'mount_resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_share_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_share_path FgsFunctionV2#mount_share_path}.'''
        result = self._values.get("mount_share_path")
        assert result is not None, "Required property 'mount_share_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#mount_type FgsFunctionV2#mount_type}.'''
        result = self._values.get("mount_type")
        assert result is not None, "Required property 'mount_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2FuncMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsFunctionV2FuncMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2FuncMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49b6ea6ce06388910537b9482732887b7e4efe19f5a1bd65dec0675de8115520)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FgsFunctionV2FuncMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd62bf7d48f0064f3cff8020ceb03f8aa188baa5f6c169296e413a252afeb53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FgsFunctionV2FuncMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1eacf9111a0ea2e3408465530d61922acaac3919a31e319b8520f898661d0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__308930eb9a679b386e58b28f85004177311128b26bd3d52ec6aef716d7a177ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92a053f4b51ea32120b2588893a773fd425f7e61ccef8c6371bf87c966d58e2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2FuncMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2FuncMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2FuncMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48945763a501e4621ad81d0da29b29394f2cc0e27774f7c54364ddc9cf9af20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FgsFunctionV2FuncMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2FuncMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bae55bfec509aa2f71ad6c1d4c97722afb12d3ebda765b89c7211ad42b7044cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="localMountPathInput")
    def local_mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localMountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="mountResourceInput")
    def mount_resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="mountSharePathInput")
    def mount_share_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountSharePathInput"))

    @builtins.property
    @jsii.member(jsii_name="mountTypeInput")
    def mount_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="localMountPath")
    def local_mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localMountPath"))

    @local_mount_path.setter
    def local_mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93e4849f94b5c07899512d5f8dc7341665cbd74113d2def8b1358fdb74497ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localMountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountResource")
    def mount_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountResource"))

    @mount_resource.setter
    def mount_resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294da7b817fa70412aea59147cbd8a74404f6b59e99bd72783a7ed07dfa5a4d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountSharePath")
    def mount_share_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountSharePath"))

    @mount_share_path.setter
    def mount_share_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc956589e8cd62da508762fe1f9d6f19082f7077f55bd670cbd159e21605ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountSharePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountType")
    def mount_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountType"))

    @mount_type.setter
    def mount_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b50384e7f445ca2ad2b8d2910ce5716e467635251c55a6c0480476c3cf8b520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2FuncMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2FuncMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2FuncMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd6f220f7d303dcabbd6d4b724e2c03a81506b4cf6e8b37d3d5732e5718106f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2NetworkController",
    jsii_struct_bases=[],
    name_mapping={
        "disable_public_network": "disablePublicNetwork",
        "trigger_access_vpcs": "triggerAccessVpcs",
    },
)
class FgsFunctionV2NetworkController:
    def __init__(
        self,
        *,
        disable_public_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trigger_access_vpcs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2NetworkControllerTriggerAccessVpcs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param disable_public_network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#disable_public_network FgsFunctionV2#disable_public_network}.
        :param trigger_access_vpcs: trigger_access_vpcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#trigger_access_vpcs FgsFunctionV2#trigger_access_vpcs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c7be383e78d4e69011395c5a7fae48968b76ebde00f6ec57a7977a3de8884d)
            check_type(argname="argument disable_public_network", value=disable_public_network, expected_type=type_hints["disable_public_network"])
            check_type(argname="argument trigger_access_vpcs", value=trigger_access_vpcs, expected_type=type_hints["trigger_access_vpcs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_public_network is not None:
            self._values["disable_public_network"] = disable_public_network
        if trigger_access_vpcs is not None:
            self._values["trigger_access_vpcs"] = trigger_access_vpcs

    @builtins.property
    def disable_public_network(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#disable_public_network FgsFunctionV2#disable_public_network}.'''
        result = self._values.get("disable_public_network")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trigger_access_vpcs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2NetworkControllerTriggerAccessVpcs"]]]:
        '''trigger_access_vpcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#trigger_access_vpcs FgsFunctionV2#trigger_access_vpcs}
        '''
        result = self._values.get("trigger_access_vpcs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2NetworkControllerTriggerAccessVpcs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2NetworkController(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsFunctionV2NetworkControllerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2NetworkControllerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad6e9c801407d34a635639e5271c5f844d47273617ee0c8bc78428a2135d30e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTriggerAccessVpcs")
    def put_trigger_access_vpcs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2NetworkControllerTriggerAccessVpcs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f008ec09eba762108b137d6dc8504911c9332557a108dee922655c9e250e7b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTriggerAccessVpcs", [value]))

    @jsii.member(jsii_name="resetDisablePublicNetwork")
    def reset_disable_public_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisablePublicNetwork", []))

    @jsii.member(jsii_name="resetTriggerAccessVpcs")
    def reset_trigger_access_vpcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerAccessVpcs", []))

    @builtins.property
    @jsii.member(jsii_name="triggerAccessVpcs")
    def trigger_access_vpcs(
        self,
    ) -> "FgsFunctionV2NetworkControllerTriggerAccessVpcsList":
        return typing.cast("FgsFunctionV2NetworkControllerTriggerAccessVpcsList", jsii.get(self, "triggerAccessVpcs"))

    @builtins.property
    @jsii.member(jsii_name="disablePublicNetworkInput")
    def disable_public_network_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disablePublicNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerAccessVpcsInput")
    def trigger_access_vpcs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2NetworkControllerTriggerAccessVpcs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2NetworkControllerTriggerAccessVpcs"]]], jsii.get(self, "triggerAccessVpcsInput"))

    @builtins.property
    @jsii.member(jsii_name="disablePublicNetwork")
    def disable_public_network(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disablePublicNetwork"))

    @disable_public_network.setter
    def disable_public_network(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6bcca82af943d9d5f6a9ffb7d724a461137e84f119a98f763cf77d34b9e0120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disablePublicNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FgsFunctionV2NetworkController]:
        return typing.cast(typing.Optional[FgsFunctionV2NetworkController], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FgsFunctionV2NetworkController],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d98670053a46dd2ef4e3b4059ac413a2b9dc230619dfdbf706d42009d3b87ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2NetworkControllerTriggerAccessVpcs",
    jsii_struct_bases=[],
    name_mapping={"vpc_id": "vpcId", "vpc_name": "vpcName"},
)
class FgsFunctionV2NetworkControllerTriggerAccessVpcs:
    def __init__(
        self,
        *,
        vpc_id: typing.Optional[builtins.str] = None,
        vpc_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#vpc_id FgsFunctionV2#vpc_id}.
        :param vpc_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#vpc_name FgsFunctionV2#vpc_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057051b6f43137385430147e7345a4c763f9c1bb9978f486ee971cd5978faefe)
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#vpc_id FgsFunctionV2#vpc_id}.'''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#vpc_name FgsFunctionV2#vpc_name}.'''
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2NetworkControllerTriggerAccessVpcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsFunctionV2NetworkControllerTriggerAccessVpcsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2NetworkControllerTriggerAccessVpcsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c4bb8a0d4068bb4702bae8d30ec67ba0a8cb079f5aa68feefd1729b09747782)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FgsFunctionV2NetworkControllerTriggerAccessVpcsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5d1ff7694d32a3ee0e8550a49d634ee09c4f37d9f9d12deea159dc41bfbd43)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FgsFunctionV2NetworkControllerTriggerAccessVpcsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6541955e2013ca574213f65d13db07cb8dda0d85160a2e2e8cd77fb7064573e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__650858b69eb587aa2179de9c7b88cd0768368d6a994f9e3fa12995107f44bde2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d59be88b5bb0f9d4d7da197d7089e180084f81b52a6ffe346d211698d0c16b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2NetworkControllerTriggerAccessVpcs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2NetworkControllerTriggerAccessVpcs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2NetworkControllerTriggerAccessVpcs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e951d0e86e275be16493de80e1c6b5a12e03d28802a9d23e9e823c149c57f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FgsFunctionV2NetworkControllerTriggerAccessVpcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2NetworkControllerTriggerAccessVpcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b25354e88fbd95c0fd8b4fdb2f0ffa93e01e10b569535388e4e656b0f10c516)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetVpcId")
    def reset_vpc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcId", []))

    @jsii.member(jsii_name="resetVpcName")
    def reset_vpc_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcName", []))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNameInput")
    def vpc_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcNameInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4595bdc58fa344268bb860898d3077019d8fb7f73dd14ef50fdeff463f4e4f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcName")
    def vpc_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcName"))

    @vpc_name.setter
    def vpc_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f998480d04e1ca75c0a7b61af54ea832b92eadd428c4ea14a9ea83d215a603e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2NetworkControllerTriggerAccessVpcs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2NetworkControllerTriggerAccessVpcs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2NetworkControllerTriggerAccessVpcs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e37cff403d08cb083aaa61281561dbbf9cb0f038b7f1bc00c5d22bd3dc7859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2ReservedInstances",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "qualifier_name": "qualifierName",
        "qualifier_type": "qualifierType",
        "idle_mode": "idleMode",
        "tactics_config": "tacticsConfig",
    },
)
class FgsFunctionV2ReservedInstances:
    def __init__(
        self,
        *,
        count: jsii.Number,
        qualifier_name: builtins.str,
        qualifier_type: builtins.str,
        idle_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tactics_config: typing.Optional[typing.Union["FgsFunctionV2ReservedInstancesTacticsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#count FgsFunctionV2#count}.
        :param qualifier_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#qualifier_name FgsFunctionV2#qualifier_name}.
        :param qualifier_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#qualifier_type FgsFunctionV2#qualifier_type}.
        :param idle_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#idle_mode FgsFunctionV2#idle_mode}.
        :param tactics_config: tactics_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#tactics_config FgsFunctionV2#tactics_config}
        '''
        if isinstance(tactics_config, dict):
            tactics_config = FgsFunctionV2ReservedInstancesTacticsConfig(**tactics_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7da6c941f5586c2a66405e53af5fadef962f3799f3598c2aa49722ab6aab1b8)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument qualifier_name", value=qualifier_name, expected_type=type_hints["qualifier_name"])
            check_type(argname="argument qualifier_type", value=qualifier_type, expected_type=type_hints["qualifier_type"])
            check_type(argname="argument idle_mode", value=idle_mode, expected_type=type_hints["idle_mode"])
            check_type(argname="argument tactics_config", value=tactics_config, expected_type=type_hints["tactics_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "qualifier_name": qualifier_name,
            "qualifier_type": qualifier_type,
        }
        if idle_mode is not None:
            self._values["idle_mode"] = idle_mode
        if tactics_config is not None:
            self._values["tactics_config"] = tactics_config

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#count FgsFunctionV2#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def qualifier_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#qualifier_name FgsFunctionV2#qualifier_name}.'''
        result = self._values.get("qualifier_name")
        assert result is not None, "Required property 'qualifier_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def qualifier_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#qualifier_type FgsFunctionV2#qualifier_type}.'''
        result = self._values.get("qualifier_type")
        assert result is not None, "Required property 'qualifier_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def idle_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#idle_mode FgsFunctionV2#idle_mode}.'''
        result = self._values.get("idle_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tactics_config(
        self,
    ) -> typing.Optional["FgsFunctionV2ReservedInstancesTacticsConfig"]:
        '''tactics_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#tactics_config FgsFunctionV2#tactics_config}
        '''
        result = self._values.get("tactics_config")
        return typing.cast(typing.Optional["FgsFunctionV2ReservedInstancesTacticsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2ReservedInstances(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsFunctionV2ReservedInstancesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2ReservedInstancesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b168020a31120b9837c7b0b2949d2121b154a329f7e6ab815c214ec35c7f2885)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FgsFunctionV2ReservedInstancesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8109985cb292f9b1ecf4e014f229a993d1845c36509e5094c3cf312fbce91dc1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FgsFunctionV2ReservedInstancesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4abd04097879b24ecfa3e9ca1f528208b9e6ea501f472d8772138b62534f3113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36b62780d5adb0996d25e2eac8f92ea2f89a9f5582d7f0fd8dd76add528a738c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbec6dccf0434017b579fdb3eeda7c74c75872fc2be94e398748c977f77b24ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstances]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstances]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstances]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954893e037f19166232539041e52985f7bc59d7ca122ae4cc7ebc513f12c375f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FgsFunctionV2ReservedInstancesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2ReservedInstancesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9c4f211a20a81753f9ac0897adc6f9ce30875fdf9f0276a3c0fb97735ee699e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTacticsConfig")
    def put_tactics_config(
        self,
        *,
        cron_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cron_configs: cron_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#cron_configs FgsFunctionV2#cron_configs}
        '''
        value = FgsFunctionV2ReservedInstancesTacticsConfig(cron_configs=cron_configs)

        return typing.cast(None, jsii.invoke(self, "putTacticsConfig", [value]))

    @jsii.member(jsii_name="resetIdleMode")
    def reset_idle_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleMode", []))

    @jsii.member(jsii_name="resetTacticsConfig")
    def reset_tactics_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTacticsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="tacticsConfig")
    def tactics_config(
        self,
    ) -> "FgsFunctionV2ReservedInstancesTacticsConfigOutputReference":
        return typing.cast("FgsFunctionV2ReservedInstancesTacticsConfigOutputReference", jsii.get(self, "tacticsConfig"))

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="idleModeInput")
    def idle_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "idleModeInput"))

    @builtins.property
    @jsii.member(jsii_name="qualifierNameInput")
    def qualifier_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qualifierNameInput"))

    @builtins.property
    @jsii.member(jsii_name="qualifierTypeInput")
    def qualifier_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qualifierTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tacticsConfigInput")
    def tactics_config_input(
        self,
    ) -> typing.Optional["FgsFunctionV2ReservedInstancesTacticsConfig"]:
        return typing.cast(typing.Optional["FgsFunctionV2ReservedInstancesTacticsConfig"], jsii.get(self, "tacticsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a45ae0e8ab92a984f1b47ecff2e99a8bf9fcc88a811552854c5a589df5caa19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleMode")
    def idle_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "idleMode"))

    @idle_mode.setter
    def idle_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a95c611c53a7382356604d5a248bebdb7272d2cc4dda02688a442768b56787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qualifierName")
    def qualifier_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qualifierName"))

    @qualifier_name.setter
    def qualifier_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d054f37c1cf1d0b18afc59ccff9c79f2b21a2c1d0107c24c4708c156cb9614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifierName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qualifierType")
    def qualifier_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "qualifierType"))

    @qualifier_type.setter
    def qualifier_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b748c1fbc3eddec8aa72eaa1636478f02e2da70046caffbd27b2947f48ce5b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifierType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2ReservedInstances]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2ReservedInstances]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2ReservedInstances]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d9f23f64499836c3cddb9d29689a55d498a82fc37b16d02f7b08141d3e48651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2ReservedInstancesTacticsConfig",
    jsii_struct_bases=[],
    name_mapping={"cron_configs": "cronConfigs"},
)
class FgsFunctionV2ReservedInstancesTacticsConfig:
    def __init__(
        self,
        *,
        cron_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param cron_configs: cron_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#cron_configs FgsFunctionV2#cron_configs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c50a593c7612d11b214611755ea624cfea5928030e1f1439f2bca4929ebea1)
            check_type(argname="argument cron_configs", value=cron_configs, expected_type=type_hints["cron_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron_configs is not None:
            self._values["cron_configs"] = cron_configs

    @builtins.property
    def cron_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs"]]]:
        '''cron_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#cron_configs FgsFunctionV2#cron_configs}
        '''
        result = self._values.get("cron_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2ReservedInstancesTacticsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "cron": "cron",
        "expired_time": "expiredTime",
        "name": "name",
        "start_time": "startTime",
    },
)
class FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs:
    def __init__(
        self,
        *,
        count: jsii.Number,
        cron: builtins.str,
        expired_time: jsii.Number,
        name: builtins.str,
        start_time: jsii.Number,
    ) -> None:
        '''
        :param count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#count FgsFunctionV2#count}.
        :param cron: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#cron FgsFunctionV2#cron}.
        :param expired_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#expired_time FgsFunctionV2#expired_time}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#start_time FgsFunctionV2#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb0847412d7b9eb20a51b38b30218152c11af06738b4a2946c32ec623a20d85)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
            check_type(argname="argument expired_time", value=expired_time, expected_type=type_hints["expired_time"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "count": count,
            "cron": cron,
            "expired_time": expired_time,
            "name": name,
            "start_time": start_time,
        }

    @builtins.property
    def count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#count FgsFunctionV2#count}.'''
        result = self._values.get("count")
        assert result is not None, "Required property 'count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def cron(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#cron FgsFunctionV2#cron}.'''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expired_time(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#expired_time FgsFunctionV2#expired_time}.'''
        result = self._values.get("expired_time")
        assert result is not None, "Required property 'expired_time' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#start_time FgsFunctionV2#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63fe187206920b369e25c180f6ec8e6205d76b1ac2ec514885341d916bbaf6cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a25629d86fd5e0b53aaa8ebc0eec51b22e6851978962de5767a2cd11f6aa9a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146096c646d73fa338ae621eec72c955b178055756bb82261549aee1de2b96cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dcec3aba7490095be0ce43ed60461c99db980ad4255893a452c43c61279fa5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e9989b38cf4760d778a53eb804679e70e154c78d009032ae2f770c4936cc785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927d2dd76e078cf0cee9c7761afe8676adac223a4ea50db6bddf28ab16ee24a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01ece919850b65eb0eadd7e30d00ee4e5fabf5d9d0731af4a412fe27d0d80926)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="countInput")
    def count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "countInput"))

    @builtins.property
    @jsii.member(jsii_name="cronInput")
    def cron_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronInput"))

    @builtins.property
    @jsii.member(jsii_name="expiredTimeInput")
    def expired_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expiredTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e83938bf3c19c8a28d2d3e7f28acde0b1c7b9ac4072b3543f81f8d48cd8f1d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cron")
    def cron(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cron"))

    @cron.setter
    def cron(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1d8e32078473b385c95952271cf572d9cd3eaeccba0b9a955e6eb79f6018d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cron", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expiredTime")
    def expired_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expiredTime"))

    @expired_time.setter
    def expired_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a846549029da7da16c35b364a52974389a3700ef69062683648ebc5f5d028e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiredTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c14e0d3c0184fd5cd974891c26ee34628bacf48e090e6860c27e2e0cddf6bb58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12376978f8216c204e9614c3a855dc20a41ea9789dae26c95dccec532bb15b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80efb70b45c023e6d86a5a043ddc65e1563d72dd4211ef00e6c7ac2f83b0a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FgsFunctionV2ReservedInstancesTacticsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2ReservedInstancesTacticsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b85b4fbe759252ae6d022f4a995abfd40b815476cb0c73d94a5559ebc8ed7f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCronConfigs")
    def put_cron_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31dfd1790efde7402db5690d04af6c8ef873388db530d14f2b8fd13a682cbf08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCronConfigs", [value]))

    @jsii.member(jsii_name="resetCronConfigs")
    def reset_cron_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronConfigs", []))

    @builtins.property
    @jsii.member(jsii_name="cronConfigs")
    def cron_configs(
        self,
    ) -> FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsList:
        return typing.cast(FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsList, jsii.get(self, "cronConfigs"))

    @builtins.property
    @jsii.member(jsii_name="cronConfigsInput")
    def cron_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]]], jsii.get(self, "cronConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FgsFunctionV2ReservedInstancesTacticsConfig]:
        return typing.cast(typing.Optional[FgsFunctionV2ReservedInstancesTacticsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FgsFunctionV2ReservedInstancesTacticsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e90e6ddb925c53068cd3fd91923cedd80bd705a71ea8bb85c699872651ae4a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class FgsFunctionV2Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#create FgsFunctionV2#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#delete FgsFunctionV2#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce0a3c0451b594328753fee14d65befb2381e71fba6fbafeaa945af986915817)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#create FgsFunctionV2#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#delete FgsFunctionV2#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsFunctionV2TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90587dedfa40f70c1158a341e89cf0b66be198ce138c016b54d965f579255273)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cac6a1c827db6b753dd48e70abba258e7e1bbb16d13694f6d73b1581067b1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9748b60bc72dd9b18efaa14ab68cefb291de13f3a18119fd0abb1ea5b891a901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1352f15a4adc820a5a7f442f4816b43e658b63c369332907bd464b305c20d13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2Versions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "aliases": "aliases"},
)
class FgsFunctionV2Versions:
    def __init__(
        self,
        *,
        name: builtins.str,
        aliases: typing.Optional[typing.Union["FgsFunctionV2VersionsAliases", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: The version name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}
        :param aliases: aliases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#aliases FgsFunctionV2#aliases}
        '''
        if isinstance(aliases, dict):
            aliases = FgsFunctionV2VersionsAliases(**aliases)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea080aab6e468bab23daa69d44b3e2dce78ffd228053b08148fa4dd7fd1c480)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aliases", value=aliases, expected_type=type_hints["aliases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if aliases is not None:
            self._values["aliases"] = aliases

    @builtins.property
    def name(self) -> builtins.str:
        '''The version name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aliases(self) -> typing.Optional["FgsFunctionV2VersionsAliases"]:
        '''aliases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#aliases FgsFunctionV2#aliases}
        '''
        result = self._values.get("aliases")
        return typing.cast(typing.Optional["FgsFunctionV2VersionsAliases"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2Versions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2VersionsAliases",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description"},
)
class FgsFunctionV2VersionsAliases:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#description FgsFunctionV2#description}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c309b89db2c0727ae5b7a278abb2e8066746ebf789f6e39a12910f60111967f4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#description FgsFunctionV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FgsFunctionV2VersionsAliases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FgsFunctionV2VersionsAliasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2VersionsAliasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1094f455b98f033fda0bd6e2bbd52bb97905f702db5ade4a52feb09edd218cf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f994e159a0f47800cb8c686dab7aa4df25fbf40b9ce05e821ae73d033557a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35036b1d067bb39139abfc52786792f70487bbb7332391f573e1fa3c8967fcc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FgsFunctionV2VersionsAliases]:
        return typing.cast(typing.Optional[FgsFunctionV2VersionsAliases], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FgsFunctionV2VersionsAliases],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb3d8107e10b460380645643f469ed1c7e14fb95dd1406debb2a71a0c84901a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FgsFunctionV2VersionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2VersionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87b72ca5198abc39165f152df95e85ee57f44c8c18140ed7792ba66cd3d1f2c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FgsFunctionV2VersionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa984e6fb5c65044f687ff04f9bf205d700cfbd220d6d1657ea503c8f432667c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FgsFunctionV2VersionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058dd68f220396815b6cc21697cc286d3f348103c10763a44c9131eb45f988fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21d1be528bb551a2e5fab277ba88a8f4b238fa9b8fbd643a60ced0cd33930984)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce0550a666b1fd804ca298cfc4629c38c6b6e408f106fdb7eb3a9c69b42d9ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2Versions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2Versions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2Versions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ace3ee3573d93ebed5f0c4fac4604193adec93bb6ede8fc7170dfc81c5631b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FgsFunctionV2VersionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.fgsFunctionV2.FgsFunctionV2VersionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c0b649c2d2c40f44e39cd2ccc081da18e1f989bd6814e57dfaea7b04a3409e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAliases")
    def put_aliases(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#name FgsFunctionV2#name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/fgs_function_v2#description FgsFunctionV2#description}.
        '''
        value = FgsFunctionV2VersionsAliases(name=name, description=description)

        return typing.cast(None, jsii.invoke(self, "putAliases", [value]))

    @jsii.member(jsii_name="resetAliases")
    def reset_aliases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAliases", []))

    @builtins.property
    @jsii.member(jsii_name="aliases")
    def aliases(self) -> FgsFunctionV2VersionsAliasesOutputReference:
        return typing.cast(FgsFunctionV2VersionsAliasesOutputReference, jsii.get(self, "aliases"))

    @builtins.property
    @jsii.member(jsii_name="aliasesInput")
    def aliases_input(self) -> typing.Optional[FgsFunctionV2VersionsAliases]:
        return typing.cast(typing.Optional[FgsFunctionV2VersionsAliases], jsii.get(self, "aliasesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579e1a066eda701c1c9fcf0b85efb85a002527b58f4c85b6984e31ae3bde75b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2Versions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2Versions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2Versions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711a564b48c90089fd46d8a1a3a6ed85e654ef78ea7c59778d90e8c0ab63d061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FgsFunctionV2",
    "FgsFunctionV2Config",
    "FgsFunctionV2CustomImage",
    "FgsFunctionV2CustomImageOutputReference",
    "FgsFunctionV2FuncMounts",
    "FgsFunctionV2FuncMountsList",
    "FgsFunctionV2FuncMountsOutputReference",
    "FgsFunctionV2NetworkController",
    "FgsFunctionV2NetworkControllerOutputReference",
    "FgsFunctionV2NetworkControllerTriggerAccessVpcs",
    "FgsFunctionV2NetworkControllerTriggerAccessVpcsList",
    "FgsFunctionV2NetworkControllerTriggerAccessVpcsOutputReference",
    "FgsFunctionV2ReservedInstances",
    "FgsFunctionV2ReservedInstancesList",
    "FgsFunctionV2ReservedInstancesOutputReference",
    "FgsFunctionV2ReservedInstancesTacticsConfig",
    "FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs",
    "FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsList",
    "FgsFunctionV2ReservedInstancesTacticsConfigCronConfigsOutputReference",
    "FgsFunctionV2ReservedInstancesTacticsConfigOutputReference",
    "FgsFunctionV2Timeouts",
    "FgsFunctionV2TimeoutsOutputReference",
    "FgsFunctionV2Versions",
    "FgsFunctionV2VersionsAliases",
    "FgsFunctionV2VersionsAliasesOutputReference",
    "FgsFunctionV2VersionsList",
    "FgsFunctionV2VersionsOutputReference",
]

publication.publish()

def _typecheckingstub__e47922e73245a00d256b7f271d3ba3ca26a58540e6850ffd5f58783c4a7249b1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    memory_size: jsii.Number,
    name: builtins.str,
    runtime: builtins.str,
    timeout: jsii.Number,
    agency: typing.Optional[builtins.str] = None,
    app: typing.Optional[builtins.str] = None,
    app_agency: typing.Optional[builtins.str] = None,
    code_filename: typing.Optional[builtins.str] = None,
    code_type: typing.Optional[builtins.str] = None,
    code_url: typing.Optional[builtins.str] = None,
    concurrency_num: typing.Optional[jsii.Number] = None,
    custom_image: typing.Optional[typing.Union[FgsFunctionV2CustomImage, typing.Dict[builtins.str, typing.Any]]] = None,
    depend_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_dynamic_memory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encrypted_user_data: typing.Optional[builtins.str] = None,
    func_code: typing.Optional[builtins.str] = None,
    func_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2FuncMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    functiongraph_version: typing.Optional[builtins.str] = None,
    gpu_memory: typing.Optional[jsii.Number] = None,
    handler: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initializer_handler: typing.Optional[builtins.str] = None,
    initializer_timeout: typing.Optional[jsii.Number] = None,
    log_group_id: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_topic_id: typing.Optional[builtins.str] = None,
    log_topic_name: typing.Optional[builtins.str] = None,
    max_instance_num: typing.Optional[builtins.str] = None,
    mount_user_group_id: typing.Optional[jsii.Number] = None,
    mount_user_id: typing.Optional[jsii.Number] = None,
    network_controller: typing.Optional[typing.Union[FgsFunctionV2NetworkController, typing.Dict[builtins.str, typing.Any]]] = None,
    network_id: typing.Optional[builtins.str] = None,
    peering_cidr: typing.Optional[builtins.str] = None,
    pre_stop_handler: typing.Optional[builtins.str] = None,
    pre_stop_timeout: typing.Optional[jsii.Number] = None,
    reserved_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2ReservedInstances, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FgsFunctionV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
    versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2Versions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6b5fcb204eb144eef582ef3ba6d0fb1d6fd783096dbf20ca8803c4fc505052bd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e0809ef6329153d82ac25fc1686576563281fec941a74f27d10ac9f9ef20cb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2FuncMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1ef039a087eee0221c6cd8a6a7b773c0c96c4619193187a76841e1965906a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2ReservedInstances, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__926ee800ce53b72e63d68dfaa13102ad8a9808f1b4a606a87ee4b7dc0896d812(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2Versions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f373b1340354778405eeb0fad6bf55e9b3d623c569879398f32a1ca0bf47d61b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f3fe0e0aac9aa97afe6896704e3ab7017bd675d50c43736f7051287466f093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a396c68f19f65ecc014e4af8e4a53fdc91bd9f2e68a7fe9908375c9465815106(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1763affe3cbc2ae9269cd0820353b4d197e6b68274acb767f1eaf9c12de22eab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa8dc3f8a3cf82ba0c080747060d69087c46194124fb85f668aabe59199b5ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8be754646f543f9f44cf01059dea1bef8a4dbf1e4d6bd09ab69d618e1e531e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14037f6229d2a550511b84a05aaa3ac80cdb3a20173234168948bc82dc71e58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e76cbdb78435007f8531426f7fa2efefef352a19cf9a348f293d39895b5d43(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01178bb2108740e1afaa89baa5c88589b4c003077dc2496f3e8d224bb9fc87b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdb435302cbcf4b90b9b9602e1cc6bc8ff8e0bc166b5d3485cc3ddc0c1da3cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19002f94d94aa615505751062586b5257fb3704d0d42b44309bd02ce213c9fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900ee1038835483ba79a56b31f96fbf37cf07a33f1982740006ffa7d14b20ec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ee53159016798f1f87317e908a3fa9ff50294c5a72d0052a3cd749a5f82e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e8f65444d70b99eb30951b6b2dc1adf0cfc95d06c8480fae4935c6915e56c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68c506ab728ff601c70a5c8e069fb611061f8a6e55d312d06a978b64ad87168(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c409cd030ecde6bae6cc9a55b6ddd5514a6233a49d7db0a928013ec52963bcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748822ca0fa57c084b7cec5442d7c0cd92d14450ac4603059366bf276ebc924c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40d145748b06679e346c0ab072594d7c56003d3a73119578d6573d39f8a339b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66d6077a57efa024c7907b003e123653650d434cd5ca4799893f3b8c1b2a63a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b3ae971a966813d5129a90628fbe159638953878d1ec6beab58f1cd6ac0f0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fd28c4a0aac9fe3fff4192f081d94f937be0e8f44690bb8ee62936efaacf1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6e438df19d880201d1db01029e333ea9ca7f197b4485311cd18119757e9156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5ebfafdd4b2e3fdb5ab0e1bcaaa5cc034db1fad079914345525030c9c19d3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc6f261ffdab4b9cd49366477da047350b1b0a489d3996dd8dcd27e996e3b1c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d04e969c5f5c0afab7e7418a8ce61edaefddfefaaade02944b5e2a224d35fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954a996bf12dfc597ae3812e36538509cf5ae5e38069f925d22f98d703f8e74a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf195fab5f015fe672299859f54c6740d5c22e3d35183c777d3e347443a30f80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b05af13f4fa0d8860cb527f67e2da58039ea463eba1d5986f184e48219c0d42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d473a3468ed3e91b232070aaa6102c55f3b22d1552e20f9150fa462ef1d23a6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dbeab3fa6af056790f5a0d147c6101966896a07bda419eda73300015075d7a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332fe459c6a0d4a65b5efb96c80f8425e49febca976c49990b52779831792d66(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b893acf3c20ba52104a37e8fae8e17dd6edfd7251bf64536eb3da768d6d3f450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121b1a5b928d14e607e27dc802ca95e659dc2a0f096812095fc7101804ddf6fa(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad217e4fc65e2f8cdd6ff3ce1644732a761a2e6c5b155f40b7ea7d05695fbb2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456beedc1d43336ef3115559fa4655e181fc3b1743fb7f8cb9fb265754bc875e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb07a132920b4512eb1be7b66771963d551c7b05d822418dc509cd2782ebbc5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228c1d4908a19e49c9bb28512aee83a71052b353d2d78f3c45d7126bca03084e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    memory_size: jsii.Number,
    name: builtins.str,
    runtime: builtins.str,
    timeout: jsii.Number,
    agency: typing.Optional[builtins.str] = None,
    app: typing.Optional[builtins.str] = None,
    app_agency: typing.Optional[builtins.str] = None,
    code_filename: typing.Optional[builtins.str] = None,
    code_type: typing.Optional[builtins.str] = None,
    code_url: typing.Optional[builtins.str] = None,
    concurrency_num: typing.Optional[jsii.Number] = None,
    custom_image: typing.Optional[typing.Union[FgsFunctionV2CustomImage, typing.Dict[builtins.str, typing.Any]]] = None,
    depend_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_dynamic_memory: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encrypted_user_data: typing.Optional[builtins.str] = None,
    func_code: typing.Optional[builtins.str] = None,
    func_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2FuncMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    functiongraph_version: typing.Optional[builtins.str] = None,
    gpu_memory: typing.Optional[jsii.Number] = None,
    handler: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    initializer_handler: typing.Optional[builtins.str] = None,
    initializer_timeout: typing.Optional[jsii.Number] = None,
    log_group_id: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_topic_id: typing.Optional[builtins.str] = None,
    log_topic_name: typing.Optional[builtins.str] = None,
    max_instance_num: typing.Optional[builtins.str] = None,
    mount_user_group_id: typing.Optional[jsii.Number] = None,
    mount_user_id: typing.Optional[jsii.Number] = None,
    network_controller: typing.Optional[typing.Union[FgsFunctionV2NetworkController, typing.Dict[builtins.str, typing.Any]]] = None,
    network_id: typing.Optional[builtins.str] = None,
    peering_cidr: typing.Optional[builtins.str] = None,
    pre_stop_handler: typing.Optional[builtins.str] = None,
    pre_stop_timeout: typing.Optional[jsii.Number] = None,
    reserved_instances: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2ReservedInstances, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FgsFunctionV2Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_data: typing.Optional[builtins.str] = None,
    versions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2Versions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1259cc2700c686c31207bc07d6520b12e9e62c845abcfe1598845dba90751c6(
    *,
    url: builtins.str,
    args: typing.Optional[builtins.str] = None,
    command: typing.Optional[builtins.str] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c2fdc27c666c1383a39ba42f07c2b55c65b8a256135be92a1d4e4548f199fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1372aa88d91c5d2ddf214df352db5bd0a02493607a061993773f9361c2e612c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__214ac0580a3f4cb8b67d536fee533376cebac5c0724421d6b7709d174f9c1364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134569c875ae77d19366e85b750fa7eba19491669c141dc2b0684c01a2b9fde7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42252355ced70547dd05950ee5622b4beaa8e4521fd45a40d0a8a4b8e8b9e30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed35aefdb873b8879b4a64afdc7c6b309b09d5503f3bcc7545edf21ae1df706(
    value: typing.Optional[FgsFunctionV2CustomImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa3547ab9b17d65d041982262c8ff1266215add4d14370434ee5b7c2a600909(
    *,
    local_mount_path: builtins.str,
    mount_resource: builtins.str,
    mount_share_path: builtins.str,
    mount_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b6ea6ce06388910537b9482732887b7e4efe19f5a1bd65dec0675de8115520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd62bf7d48f0064f3cff8020ceb03f8aa188baa5f6c169296e413a252afeb53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1eacf9111a0ea2e3408465530d61922acaac3919a31e319b8520f898661d0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308930eb9a679b386e58b28f85004177311128b26bd3d52ec6aef716d7a177ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a053f4b51ea32120b2588893a773fd425f7e61ccef8c6371bf87c966d58e2b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48945763a501e4621ad81d0da29b29394f2cc0e27774f7c54364ddc9cf9af20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2FuncMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae55bfec509aa2f71ad6c1d4c97722afb12d3ebda765b89c7211ad42b7044cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e4849f94b5c07899512d5f8dc7341665cbd74113d2def8b1358fdb74497ae3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294da7b817fa70412aea59147cbd8a74404f6b59e99bd72783a7ed07dfa5a4d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc956589e8cd62da508762fe1f9d6f19082f7077f55bd670cbd159e21605ef4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b50384e7f445ca2ad2b8d2910ce5716e467635251c55a6c0480476c3cf8b520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd6f220f7d303dcabbd6d4b724e2c03a81506b4cf6e8b37d3d5732e5718106f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2FuncMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c7be383e78d4e69011395c5a7fae48968b76ebde00f6ec57a7977a3de8884d(
    *,
    disable_public_network: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trigger_access_vpcs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2NetworkControllerTriggerAccessVpcs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6e9c801407d34a635639e5271c5f844d47273617ee0c8bc78428a2135d30e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f008ec09eba762108b137d6dc8504911c9332557a108dee922655c9e250e7b91(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2NetworkControllerTriggerAccessVpcs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6bcca82af943d9d5f6a9ffb7d724a461137e84f119a98f763cf77d34b9e0120(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d98670053a46dd2ef4e3b4059ac413a2b9dc230619dfdbf706d42009d3b87ec(
    value: typing.Optional[FgsFunctionV2NetworkController],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057051b6f43137385430147e7345a4c763f9c1bb9978f486ee971cd5978faefe(
    *,
    vpc_id: typing.Optional[builtins.str] = None,
    vpc_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4bb8a0d4068bb4702bae8d30ec67ba0a8cb079f5aa68feefd1729b09747782(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5d1ff7694d32a3ee0e8550a49d634ee09c4f37d9f9d12deea159dc41bfbd43(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6541955e2013ca574213f65d13db07cb8dda0d85160a2e2e8cd77fb7064573e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650858b69eb587aa2179de9c7b88cd0768368d6a994f9e3fa12995107f44bde2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d59be88b5bb0f9d4d7da197d7089e180084f81b52a6ffe346d211698d0c16b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e951d0e86e275be16493de80e1c6b5a12e03d28802a9d23e9e823c149c57f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2NetworkControllerTriggerAccessVpcs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b25354e88fbd95c0fd8b4fdb2f0ffa93e01e10b569535388e4e656b0f10c516(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4595bdc58fa344268bb860898d3077019d8fb7f73dd14ef50fdeff463f4e4f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f998480d04e1ca75c0a7b61af54ea832b92eadd428c4ea14a9ea83d215a603e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e37cff403d08cb083aaa61281561dbbf9cb0f038b7f1bc00c5d22bd3dc7859(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2NetworkControllerTriggerAccessVpcs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7da6c941f5586c2a66405e53af5fadef962f3799f3598c2aa49722ab6aab1b8(
    *,
    count: jsii.Number,
    qualifier_name: builtins.str,
    qualifier_type: builtins.str,
    idle_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tactics_config: typing.Optional[typing.Union[FgsFunctionV2ReservedInstancesTacticsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b168020a31120b9837c7b0b2949d2121b154a329f7e6ab815c214ec35c7f2885(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8109985cb292f9b1ecf4e014f229a993d1845c36509e5094c3cf312fbce91dc1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abd04097879b24ecfa3e9ca1f528208b9e6ea501f472d8772138b62534f3113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b62780d5adb0996d25e2eac8f92ea2f89a9f5582d7f0fd8dd76add528a738c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbec6dccf0434017b579fdb3eeda7c74c75872fc2be94e398748c977f77b24ee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954893e037f19166232539041e52985f7bc59d7ca122ae4cc7ebc513f12c375f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstances]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c4f211a20a81753f9ac0897adc6f9ce30875fdf9f0276a3c0fb97735ee699e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a45ae0e8ab92a984f1b47ecff2e99a8bf9fcc88a811552854c5a589df5caa19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a95c611c53a7382356604d5a248bebdb7272d2cc4dda02688a442768b56787(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d054f37c1cf1d0b18afc59ccff9c79f2b21a2c1d0107c24c4708c156cb9614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b748c1fbc3eddec8aa72eaa1636478f02e2da70046caffbd27b2947f48ce5b18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d9f23f64499836c3cddb9d29689a55d498a82fc37b16d02f7b08141d3e48651(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2ReservedInstances]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c50a593c7612d11b214611755ea624cfea5928030e1f1439f2bca4929ebea1(
    *,
    cron_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb0847412d7b9eb20a51b38b30218152c11af06738b4a2946c32ec623a20d85(
    *,
    count: jsii.Number,
    cron: builtins.str,
    expired_time: jsii.Number,
    name: builtins.str,
    start_time: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63fe187206920b369e25c180f6ec8e6205d76b1ac2ec514885341d916bbaf6cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a25629d86fd5e0b53aaa8ebc0eec51b22e6851978962de5767a2cd11f6aa9a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146096c646d73fa338ae621eec72c955b178055756bb82261549aee1de2b96cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcec3aba7490095be0ce43ed60461c99db980ad4255893a452c43c61279fa5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9989b38cf4760d778a53eb804679e70e154c78d009032ae2f770c4936cc785(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927d2dd76e078cf0cee9c7761afe8676adac223a4ea50db6bddf28ab16ee24a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ece919850b65eb0eadd7e30d00ee4e5fabf5d9d0731af4a412fe27d0d80926(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e83938bf3c19c8a28d2d3e7f28acde0b1c7b9ac4072b3543f81f8d48cd8f1d57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1d8e32078473b385c95952271cf572d9cd3eaeccba0b9a955e6eb79f6018d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a846549029da7da16c35b364a52974389a3700ef69062683648ebc5f5d028e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14e0d3c0184fd5cd974891c26ee34628bacf48e090e6860c27e2e0cddf6bb58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12376978f8216c204e9614c3a855dc20a41ea9789dae26c95dccec532bb15b82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80efb70b45c023e6d86a5a043ddc65e1563d72dd4211ef00e6c7ac2f83b0a4f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b85b4fbe759252ae6d022f4a995abfd40b815476cb0c73d94a5559ebc8ed7f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31dfd1790efde7402db5690d04af6c8ef873388db530d14f2b8fd13a682cbf08(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FgsFunctionV2ReservedInstancesTacticsConfigCronConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e90e6ddb925c53068cd3fd91923cedd80bd705a71ea8bb85c699872651ae4a0(
    value: typing.Optional[FgsFunctionV2ReservedInstancesTacticsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0a3c0451b594328753fee14d65befb2381e71fba6fbafeaa945af986915817(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90587dedfa40f70c1158a341e89cf0b66be198ce138c016b54d965f579255273(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cac6a1c827db6b753dd48e70abba258e7e1bbb16d13694f6d73b1581067b1a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9748b60bc72dd9b18efaa14ab68cefb291de13f3a18119fd0abb1ea5b891a901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1352f15a4adc820a5a7f442f4816b43e658b63c369332907bd464b305c20d13e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea080aab6e468bab23daa69d44b3e2dce78ffd228053b08148fa4dd7fd1c480(
    *,
    name: builtins.str,
    aliases: typing.Optional[typing.Union[FgsFunctionV2VersionsAliases, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c309b89db2c0727ae5b7a278abb2e8066746ebf789f6e39a12910f60111967f4(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1094f455b98f033fda0bd6e2bbd52bb97905f702db5ade4a52feb09edd218cf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f994e159a0f47800cb8c686dab7aa4df25fbf40b9ce05e821ae73d033557a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35036b1d067bb39139abfc52786792f70487bbb7332391f573e1fa3c8967fcc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb3d8107e10b460380645643f469ed1c7e14fb95dd1406debb2a71a0c84901a(
    value: typing.Optional[FgsFunctionV2VersionsAliases],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b72ca5198abc39165f152df95e85ee57f44c8c18140ed7792ba66cd3d1f2c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa984e6fb5c65044f687ff04f9bf205d700cfbd220d6d1657ea503c8f432667c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058dd68f220396815b6cc21697cc286d3f348103c10763a44c9131eb45f988fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21d1be528bb551a2e5fab277ba88a8f4b238fa9b8fbd643a60ced0cd33930984(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0550a666b1fd804ca298cfc4629c38c6b6e408f106fdb7eb3a9c69b42d9ec5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ace3ee3573d93ebed5f0c4fac4604193adec93bb6ede8fc7170dfc81c5631b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FgsFunctionV2Versions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0b649c2d2c40f44e39cd2ccc081da18e1f989bd6814e57dfaea7b04a3409e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579e1a066eda701c1c9fcf0b85efb85a002527b58f4c85b6984e31ae3bde75b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711a564b48c90089fd46d8a1a3a6ed85e654ef78ea7c59778d90e8c0ab63d061(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FgsFunctionV2Versions]],
) -> None:
    """Type checking stubs"""
    pass
