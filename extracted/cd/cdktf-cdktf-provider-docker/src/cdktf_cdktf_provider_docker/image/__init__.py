r'''
# `docker_image`

Refer to the Terraform Registry for docs: [`docker_image`](https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image).
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


class Image(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.Image",
):
    '''Represents a {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image docker_image}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        build_attribute: typing.Optional[typing.Union["ImageBuild", typing.Dict[builtins.str, typing.Any]]] = None,
        force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keep_locally: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        platform: typing.Optional[builtins.str] = None,
        pull_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ImageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image docker_image} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the Docker image, including any tags or SHA256 repo digests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#name Image#name}
        :param build_attribute: build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build Image#build}
        :param force_remove: If true, then the image is removed forcibly when the resource is destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#force_remove Image#force_remove}
        :param keep_locally: If true, then the Docker image won't be deleted on destroy operation. If this is false, it will delete the image from the docker local storage on destroy operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#keep_locally Image#keep_locally}
        :param platform: The platform to use when pulling the image. Defaults to the platform of the current machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#platform Image#platform}
        :param pull_triggers: List of values which cause an image pull when changed. This is used to store the image digest from the registry when using the `docker_registry_image <../data-sources/registry_image.md>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#pull_triggers Image#pull_triggers}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#timeouts Image#timeouts}
        :param triggers: A map of arbitrary strings that, when changed, will force the ``docker_image`` resource to be replaced. This can be used to rebuild an image when contents of source code folders change Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#triggers Image#triggers}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0489b42b05476ec753523550c3227ebd9d9bdfc42b864cc237e85de1d73269e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ImageConfig(
            name=name,
            build_attribute=build_attribute,
            force_remove=force_remove,
            keep_locally=keep_locally,
            platform=platform,
            pull_triggers=pull_triggers,
            timeouts=timeouts,
            triggers=triggers,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a Image resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Image to import.
        :param import_from_id: The id of the existing Image that should be imported. Refer to the {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Image to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca1941af1df8c7b1c5eeb05c4bcd259852e78227a920ba12b50c9b1bccf9355)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBuildAttribute")
    def put_build_attribute(
        self,
        *,
        context: builtins.str,
        auth_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImageBuildAuthConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        build_id: typing.Optional[builtins.str] = None,
        cache_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        cgroup_parent: typing.Optional[builtins.str] = None,
        cpu_period: typing.Optional[jsii.Number] = None,
        cpu_quota: typing.Optional[jsii.Number] = None,
        cpu_set_cpus: typing.Optional[builtins.str] = None,
        cpu_set_mems: typing.Optional[builtins.str] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        dockerfile: typing.Optional[builtins.str] = None,
        extra_hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
        force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        isolation: typing.Optional[builtins.str] = None,
        label: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_swap: typing.Optional[jsii.Number] = None,
        network_mode: typing.Optional[builtins.str] = None,
        no_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        platform: typing.Optional[builtins.str] = None,
        pull_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_context: typing.Optional[builtins.str] = None,
        remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImageBuildSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        security_opt: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_id: typing.Optional[builtins.str] = None,
        shm_size: typing.Optional[jsii.Number] = None,
        squash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suppress_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        target: typing.Optional[builtins.str] = None,
        ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImageBuildUlimit", typing.Dict[builtins.str, typing.Any]]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context: Value to specify the build context. Currently, only a ``PATH`` context is supported. You can use the helper function '${path.cwd}/context-dir'. This always refers to the local working directory, even when building images on remote hosts. Please see https://docs.docker.com/build/building/context/ for more information about build contexts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#context Image#context}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#auth_config Image#auth_config}
        :param build_args: Pairs for build-time variables in the form of ``ENDPOINT : "https://example.com"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build_args Image#build_args}
        :param build_id: BuildID is an optional identifier that can be passed together with the build request. The same identifier can be used to gracefully cancel the build with the cancel request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build_id Image#build_id}
        :param cache_from: Images to consider as cache sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cache_from Image#cache_from}
        :param cgroup_parent: Optional parent cgroup for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cgroup_parent Image#cgroup_parent}
        :param cpu_period: The length of a CPU period in microseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_period Image#cpu_period}
        :param cpu_quota: Microseconds of CPU time that the container can get in a CPU period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_quota Image#cpu_quota}
        :param cpu_set_cpus: CPUs in which to allow execution (e.g., ``0-3``, ``0``, ``1``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_set_cpus Image#cpu_set_cpus}
        :param cpu_set_mems: MEMs in which to allow execution (``0-3``, ``0``, ``1``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_set_mems Image#cpu_set_mems}
        :param cpu_shares: CPU shares (relative weight). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_shares Image#cpu_shares}
        :param dockerfile: Name of the Dockerfile. Defaults to ``Dockerfile``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#dockerfile Image#dockerfile}
        :param extra_hosts: A list of hostnames/IP mappings to add to the container’s /etc/hosts file. Specified in the form ["hostname:IP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#extra_hosts Image#extra_hosts}
        :param force_remove: Always remove intermediate containers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#force_remove Image#force_remove}
        :param isolation: Isolation represents the isolation technology of a container. The supported values are. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#isolation Image#isolation}
        :param label: Set metadata for an image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#label Image#label}
        :param labels: User-defined key/value metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#labels Image#labels}
        :param memory: Set memory limit for build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#memory Image#memory}
        :param memory_swap: Total memory (memory + swap), -1 to enable unlimited swap. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#memory_swap Image#memory_swap}
        :param network_mode: Set the networking mode for the RUN instructions during build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#network_mode Image#network_mode}
        :param no_cache: Do not use the cache when building the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#no_cache Image#no_cache}
        :param platform: Set platform if server is multi-platform capable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#platform Image#platform}
        :param pull_parent: Attempt to pull the image even if an older image exists locally. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#pull_parent Image#pull_parent}
        :param remote_context: A Git repository URI or HTTP/HTTPS context URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#remote_context Image#remote_context}
        :param remove: Remove intermediate containers after a successful build. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#remove Image#remove}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#secrets Image#secrets}
        :param security_opt: The security options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#security_opt Image#security_opt}
        :param session_id: Set an ID for the build session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#session_id Image#session_id}
        :param shm_size: Size of /dev/shm in bytes. The size must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#shm_size Image#shm_size}
        :param squash: If true the new layers are squashed into a new image with a single new layer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#squash Image#squash}
        :param suppress_output: Suppress the build output and print image ID on success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#suppress_output Image#suppress_output}
        :param tag: Name and optionally a tag in the 'name:tag' format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#tag Image#tag}
        :param target: Set the target build stage to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#target Image#target}
        :param ulimit: ulimit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#ulimit Image#ulimit}
        :param version: Version of the underlying builder to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#version Image#version}
        '''
        value = ImageBuild(
            context=context,
            auth_config=auth_config,
            build_args=build_args,
            build_id=build_id,
            cache_from=cache_from,
            cgroup_parent=cgroup_parent,
            cpu_period=cpu_period,
            cpu_quota=cpu_quota,
            cpu_set_cpus=cpu_set_cpus,
            cpu_set_mems=cpu_set_mems,
            cpu_shares=cpu_shares,
            dockerfile=dockerfile,
            extra_hosts=extra_hosts,
            force_remove=force_remove,
            isolation=isolation,
            label=label,
            labels=labels,
            memory=memory,
            memory_swap=memory_swap,
            network_mode=network_mode,
            no_cache=no_cache,
            platform=platform,
            pull_parent=pull_parent,
            remote_context=remote_context,
            remove=remove,
            secrets=secrets,
            security_opt=security_opt,
            session_id=session_id,
            shm_size=shm_size,
            squash=squash,
            suppress_output=suppress_output,
            tag=tag,
            target=target,
            ulimit=ulimit,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putBuildAttribute", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#create Image#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#delete Image#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#update Image#update}.
        '''
        value = ImageTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBuildAttribute")
    def reset_build_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildAttribute", []))

    @jsii.member(jsii_name="resetForceRemove")
    def reset_force_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceRemove", []))

    @jsii.member(jsii_name="resetKeepLocally")
    def reset_keep_locally(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepLocally", []))

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @jsii.member(jsii_name="resetPullTriggers")
    def reset_pull_triggers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullTriggers", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTriggers")
    def reset_triggers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggers", []))

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
    @jsii.member(jsii_name="buildAttribute")
    def build_attribute(self) -> "ImageBuildOutputReference":
        return typing.cast("ImageBuildOutputReference", jsii.get(self, "buildAttribute"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageId"))

    @builtins.property
    @jsii.member(jsii_name="repoDigest")
    def repo_digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repoDigest"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ImageTimeoutsOutputReference":
        return typing.cast("ImageTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="buildAttributeInput")
    def build_attribute_input(self) -> typing.Optional["ImageBuild"]:
        return typing.cast(typing.Optional["ImageBuild"], jsii.get(self, "buildAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="forceRemoveInput")
    def force_remove_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceRemoveInput"))

    @builtins.property
    @jsii.member(jsii_name="keepLocallyInput")
    def keep_locally_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepLocallyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="pullTriggersInput")
    def pull_triggers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pullTriggersInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ImageTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ImageTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggersInput")
    def triggers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "triggersInput"))

    @builtins.property
    @jsii.member(jsii_name="forceRemove")
    def force_remove(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceRemove"))

    @force_remove.setter
    def force_remove(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe322d5a5578c25d35c1bf5cdf910897b9bce3e64cc93fbc5bd78a675fdd3cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceRemove", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepLocally")
    def keep_locally(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepLocally"))

    @keep_locally.setter
    def keep_locally(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6207293ccbf84f9213ce31b9ad7192a842c0f36975a9ca239862e178c9b160c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepLocally", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1713bea97e5c741c26591528b79508b7c6d59a2ea92d138a7347f1ea95eba368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699ac4b2664b36f151c2eb8f03bf6e9b6d842eff9716e499d2f1fbb290c55a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pullTriggers")
    def pull_triggers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pullTriggers"))

    @pull_triggers.setter
    def pull_triggers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b2857a4e25da7f0b4631af1fc41bfbfed6415f16043fb2354cb5499134f07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullTriggers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "triggers"))

    @triggers.setter
    def triggers(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714c56a23046f7bc91cd621413bd5316c2104703d7f5622743e06c0aef9958ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggers", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.image.ImageBuild",
    jsii_struct_bases=[],
    name_mapping={
        "context": "context",
        "auth_config": "authConfig",
        "build_args": "buildArgs",
        "build_id": "buildId",
        "cache_from": "cacheFrom",
        "cgroup_parent": "cgroupParent",
        "cpu_period": "cpuPeriod",
        "cpu_quota": "cpuQuota",
        "cpu_set_cpus": "cpuSetCpus",
        "cpu_set_mems": "cpuSetMems",
        "cpu_shares": "cpuShares",
        "dockerfile": "dockerfile",
        "extra_hosts": "extraHosts",
        "force_remove": "forceRemove",
        "isolation": "isolation",
        "label": "label",
        "labels": "labels",
        "memory": "memory",
        "memory_swap": "memorySwap",
        "network_mode": "networkMode",
        "no_cache": "noCache",
        "platform": "platform",
        "pull_parent": "pullParent",
        "remote_context": "remoteContext",
        "remove": "remove",
        "secrets": "secrets",
        "security_opt": "securityOpt",
        "session_id": "sessionId",
        "shm_size": "shmSize",
        "squash": "squash",
        "suppress_output": "suppressOutput",
        "tag": "tag",
        "target": "target",
        "ulimit": "ulimit",
        "version": "version",
    },
)
class ImageBuild:
    def __init__(
        self,
        *,
        context: builtins.str,
        auth_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImageBuildAuthConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        build_id: typing.Optional[builtins.str] = None,
        cache_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        cgroup_parent: typing.Optional[builtins.str] = None,
        cpu_period: typing.Optional[jsii.Number] = None,
        cpu_quota: typing.Optional[jsii.Number] = None,
        cpu_set_cpus: typing.Optional[builtins.str] = None,
        cpu_set_mems: typing.Optional[builtins.str] = None,
        cpu_shares: typing.Optional[jsii.Number] = None,
        dockerfile: typing.Optional[builtins.str] = None,
        extra_hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
        force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        isolation: typing.Optional[builtins.str] = None,
        label: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        memory: typing.Optional[jsii.Number] = None,
        memory_swap: typing.Optional[jsii.Number] = None,
        network_mode: typing.Optional[builtins.str] = None,
        no_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        platform: typing.Optional[builtins.str] = None,
        pull_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_context: typing.Optional[builtins.str] = None,
        remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImageBuildSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        security_opt: typing.Optional[typing.Sequence[builtins.str]] = None,
        session_id: typing.Optional[builtins.str] = None,
        shm_size: typing.Optional[jsii.Number] = None,
        squash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suppress_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tag: typing.Optional[typing.Sequence[builtins.str]] = None,
        target: typing.Optional[builtins.str] = None,
        ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImageBuildUlimit", typing.Dict[builtins.str, typing.Any]]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param context: Value to specify the build context. Currently, only a ``PATH`` context is supported. You can use the helper function '${path.cwd}/context-dir'. This always refers to the local working directory, even when building images on remote hosts. Please see https://docs.docker.com/build/building/context/ for more information about build contexts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#context Image#context}
        :param auth_config: auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#auth_config Image#auth_config}
        :param build_args: Pairs for build-time variables in the form of ``ENDPOINT : "https://example.com"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build_args Image#build_args}
        :param build_id: BuildID is an optional identifier that can be passed together with the build request. The same identifier can be used to gracefully cancel the build with the cancel request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build_id Image#build_id}
        :param cache_from: Images to consider as cache sources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cache_from Image#cache_from}
        :param cgroup_parent: Optional parent cgroup for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cgroup_parent Image#cgroup_parent}
        :param cpu_period: The length of a CPU period in microseconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_period Image#cpu_period}
        :param cpu_quota: Microseconds of CPU time that the container can get in a CPU period. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_quota Image#cpu_quota}
        :param cpu_set_cpus: CPUs in which to allow execution (e.g., ``0-3``, ``0``, ``1``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_set_cpus Image#cpu_set_cpus}
        :param cpu_set_mems: MEMs in which to allow execution (``0-3``, ``0``, ``1``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_set_mems Image#cpu_set_mems}
        :param cpu_shares: CPU shares (relative weight). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_shares Image#cpu_shares}
        :param dockerfile: Name of the Dockerfile. Defaults to ``Dockerfile``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#dockerfile Image#dockerfile}
        :param extra_hosts: A list of hostnames/IP mappings to add to the container’s /etc/hosts file. Specified in the form ["hostname:IP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#extra_hosts Image#extra_hosts}
        :param force_remove: Always remove intermediate containers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#force_remove Image#force_remove}
        :param isolation: Isolation represents the isolation technology of a container. The supported values are. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#isolation Image#isolation}
        :param label: Set metadata for an image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#label Image#label}
        :param labels: User-defined key/value metadata. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#labels Image#labels}
        :param memory: Set memory limit for build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#memory Image#memory}
        :param memory_swap: Total memory (memory + swap), -1 to enable unlimited swap. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#memory_swap Image#memory_swap}
        :param network_mode: Set the networking mode for the RUN instructions during build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#network_mode Image#network_mode}
        :param no_cache: Do not use the cache when building the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#no_cache Image#no_cache}
        :param platform: Set platform if server is multi-platform capable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#platform Image#platform}
        :param pull_parent: Attempt to pull the image even if an older image exists locally. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#pull_parent Image#pull_parent}
        :param remote_context: A Git repository URI or HTTP/HTTPS context URI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#remote_context Image#remote_context}
        :param remove: Remove intermediate containers after a successful build. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#remove Image#remove}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#secrets Image#secrets}
        :param security_opt: The security options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#security_opt Image#security_opt}
        :param session_id: Set an ID for the build session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#session_id Image#session_id}
        :param shm_size: Size of /dev/shm in bytes. The size must be greater than 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#shm_size Image#shm_size}
        :param squash: If true the new layers are squashed into a new image with a single new layer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#squash Image#squash}
        :param suppress_output: Suppress the build output and print image ID on success. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#suppress_output Image#suppress_output}
        :param tag: Name and optionally a tag in the 'name:tag' format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#tag Image#tag}
        :param target: Set the target build stage to build. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#target Image#target}
        :param ulimit: ulimit block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#ulimit Image#ulimit}
        :param version: Version of the underlying builder to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#version Image#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3ae9a65f4eadc5c82cad3f8b730013034fdb034ec5796a0d14d707b50e859e)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument auth_config", value=auth_config, expected_type=type_hints["auth_config"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument build_id", value=build_id, expected_type=type_hints["build_id"])
            check_type(argname="argument cache_from", value=cache_from, expected_type=type_hints["cache_from"])
            check_type(argname="argument cgroup_parent", value=cgroup_parent, expected_type=type_hints["cgroup_parent"])
            check_type(argname="argument cpu_period", value=cpu_period, expected_type=type_hints["cpu_period"])
            check_type(argname="argument cpu_quota", value=cpu_quota, expected_type=type_hints["cpu_quota"])
            check_type(argname="argument cpu_set_cpus", value=cpu_set_cpus, expected_type=type_hints["cpu_set_cpus"])
            check_type(argname="argument cpu_set_mems", value=cpu_set_mems, expected_type=type_hints["cpu_set_mems"])
            check_type(argname="argument cpu_shares", value=cpu_shares, expected_type=type_hints["cpu_shares"])
            check_type(argname="argument dockerfile", value=dockerfile, expected_type=type_hints["dockerfile"])
            check_type(argname="argument extra_hosts", value=extra_hosts, expected_type=type_hints["extra_hosts"])
            check_type(argname="argument force_remove", value=force_remove, expected_type=type_hints["force_remove"])
            check_type(argname="argument isolation", value=isolation, expected_type=type_hints["isolation"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument memory_swap", value=memory_swap, expected_type=type_hints["memory_swap"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument no_cache", value=no_cache, expected_type=type_hints["no_cache"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument pull_parent", value=pull_parent, expected_type=type_hints["pull_parent"])
            check_type(argname="argument remote_context", value=remote_context, expected_type=type_hints["remote_context"])
            check_type(argname="argument remove", value=remove, expected_type=type_hints["remove"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument security_opt", value=security_opt, expected_type=type_hints["security_opt"])
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument shm_size", value=shm_size, expected_type=type_hints["shm_size"])
            check_type(argname="argument squash", value=squash, expected_type=type_hints["squash"])
            check_type(argname="argument suppress_output", value=suppress_output, expected_type=type_hints["suppress_output"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument ulimit", value=ulimit, expected_type=type_hints["ulimit"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context": context,
        }
        if auth_config is not None:
            self._values["auth_config"] = auth_config
        if build_args is not None:
            self._values["build_args"] = build_args
        if build_id is not None:
            self._values["build_id"] = build_id
        if cache_from is not None:
            self._values["cache_from"] = cache_from
        if cgroup_parent is not None:
            self._values["cgroup_parent"] = cgroup_parent
        if cpu_period is not None:
            self._values["cpu_period"] = cpu_period
        if cpu_quota is not None:
            self._values["cpu_quota"] = cpu_quota
        if cpu_set_cpus is not None:
            self._values["cpu_set_cpus"] = cpu_set_cpus
        if cpu_set_mems is not None:
            self._values["cpu_set_mems"] = cpu_set_mems
        if cpu_shares is not None:
            self._values["cpu_shares"] = cpu_shares
        if dockerfile is not None:
            self._values["dockerfile"] = dockerfile
        if extra_hosts is not None:
            self._values["extra_hosts"] = extra_hosts
        if force_remove is not None:
            self._values["force_remove"] = force_remove
        if isolation is not None:
            self._values["isolation"] = isolation
        if label is not None:
            self._values["label"] = label
        if labels is not None:
            self._values["labels"] = labels
        if memory is not None:
            self._values["memory"] = memory
        if memory_swap is not None:
            self._values["memory_swap"] = memory_swap
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if no_cache is not None:
            self._values["no_cache"] = no_cache
        if platform is not None:
            self._values["platform"] = platform
        if pull_parent is not None:
            self._values["pull_parent"] = pull_parent
        if remote_context is not None:
            self._values["remote_context"] = remote_context
        if remove is not None:
            self._values["remove"] = remove
        if secrets is not None:
            self._values["secrets"] = secrets
        if security_opt is not None:
            self._values["security_opt"] = security_opt
        if session_id is not None:
            self._values["session_id"] = session_id
        if shm_size is not None:
            self._values["shm_size"] = shm_size
        if squash is not None:
            self._values["squash"] = squash
        if suppress_output is not None:
            self._values["suppress_output"] = suppress_output
        if tag is not None:
            self._values["tag"] = tag
        if target is not None:
            self._values["target"] = target
        if ulimit is not None:
            self._values["ulimit"] = ulimit
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def context(self) -> builtins.str:
        '''Value to specify the build context.

        Currently, only a ``PATH`` context is supported. You can use the helper function '${path.cwd}/context-dir'. This always refers to the local working directory, even when building images on remote hosts. Please see https://docs.docker.com/build/building/context/ for more information about build contexts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#context Image#context}
        '''
        result = self._values.get("context")
        assert result is not None, "Required property 'context' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildAuthConfig"]]]:
        '''auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#auth_config Image#auth_config}
        '''
        result = self._values.get("auth_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildAuthConfig"]]], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Pairs for build-time variables in the form of ``ENDPOINT : "https://example.com"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build_args Image#build_args}
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def build_id(self) -> typing.Optional[builtins.str]:
        '''BuildID is an optional identifier that can be passed together with the build request.

        The same identifier can be used to gracefully cancel the build with the cancel request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build_id Image#build_id}
        '''
        result = self._values.get("build_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Images to consider as cache sources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cache_from Image#cache_from}
        '''
        result = self._values.get("cache_from")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cgroup_parent(self) -> typing.Optional[builtins.str]:
        '''Optional parent cgroup for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cgroup_parent Image#cgroup_parent}
        '''
        result = self._values.get("cgroup_parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_period(self) -> typing.Optional[jsii.Number]:
        '''The length of a CPU period in microseconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_period Image#cpu_period}
        '''
        result = self._values.get("cpu_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_quota(self) -> typing.Optional[jsii.Number]:
        '''Microseconds of CPU time that the container can get in a CPU period.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_quota Image#cpu_quota}
        '''
        result = self._values.get("cpu_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_set_cpus(self) -> typing.Optional[builtins.str]:
        '''CPUs in which to allow execution (e.g., ``0-3``, ``0``, ``1``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_set_cpus Image#cpu_set_cpus}
        '''
        result = self._values.get("cpu_set_cpus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_set_mems(self) -> typing.Optional[builtins.str]:
        '''MEMs in which to allow execution (``0-3``, ``0``, ``1``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_set_mems Image#cpu_set_mems}
        '''
        result = self._values.get("cpu_set_mems")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_shares(self) -> typing.Optional[jsii.Number]:
        '''CPU shares (relative weight).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#cpu_shares Image#cpu_shares}
        '''
        result = self._values.get("cpu_shares")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def dockerfile(self) -> typing.Optional[builtins.str]:
        '''Name of the Dockerfile. Defaults to ``Dockerfile``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#dockerfile Image#dockerfile}
        '''
        result = self._values.get("dockerfile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_hosts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of hostnames/IP mappings to add to the container’s /etc/hosts file. Specified in the form ["hostname:IP"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#extra_hosts Image#extra_hosts}
        '''
        result = self._values.get("extra_hosts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def force_remove(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Always remove intermediate containers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#force_remove Image#force_remove}
        '''
        result = self._values.get("force_remove")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def isolation(self) -> typing.Optional[builtins.str]:
        '''Isolation represents the isolation technology of a container. The supported values are.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#isolation Image#isolation}
        '''
        result = self._values.get("isolation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set metadata for an image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#label Image#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined key/value metadata.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#labels Image#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        '''Set memory limit for build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#memory Image#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_swap(self) -> typing.Optional[jsii.Number]:
        '''Total memory (memory + swap), -1 to enable unlimited swap.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#memory_swap Image#memory_swap}
        '''
        result = self._values.get("memory_swap")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def network_mode(self) -> typing.Optional[builtins.str]:
        '''Set the networking mode for the RUN instructions during build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#network_mode Image#network_mode}
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_cache(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Do not use the cache when building the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#no_cache Image#no_cache}
        '''
        result = self._values.get("no_cache")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Set platform if server is multi-platform capable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#platform Image#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_parent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Attempt to pull the image even if an older image exists locally.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#pull_parent Image#pull_parent}
        '''
        result = self._values.get("pull_parent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remote_context(self) -> typing.Optional[builtins.str]:
        '''A Git repository URI or HTTP/HTTPS context URI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#remote_context Image#remote_context}
        '''
        result = self._values.get("remote_context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remove(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Remove intermediate containers after a successful build. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#remove Image#remove}
        '''
        result = self._values.get("remove")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildSecrets"]]]:
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#secrets Image#secrets}
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildSecrets"]]], result)

    @builtins.property
    def security_opt(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#security_opt Image#security_opt}
        '''
        result = self._values.get("security_opt")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def session_id(self) -> typing.Optional[builtins.str]:
        '''Set an ID for the build session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#session_id Image#session_id}
        '''
        result = self._values.get("session_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shm_size(self) -> typing.Optional[jsii.Number]:
        '''Size of /dev/shm in bytes. The size must be greater than 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#shm_size Image#shm_size}
        '''
        result = self._values.get("shm_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def squash(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true the new layers are squashed into a new image with a single new layer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#squash Image#squash}
        '''
        result = self._values.get("squash")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suppress_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Suppress the build output and print image ID on success.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#suppress_output Image#suppress_output}
        '''
        result = self._values.get("suppress_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tag(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Name and optionally a tag in the 'name:tag' format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#tag Image#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Set the target build stage to build.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#target Image#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ulimit(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildUlimit"]]]:
        '''ulimit block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#ulimit Image#ulimit}
        '''
        result = self._values.get("ulimit")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildUlimit"]]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the underlying builder to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#version Image#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageBuild(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.image.ImageBuildAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "host_name": "hostName",
        "auth": "auth",
        "email": "email",
        "identity_token": "identityToken",
        "password": "password",
        "registry_token": "registryToken",
        "server_address": "serverAddress",
        "user_name": "userName",
    },
)
class ImageBuildAuthConfig:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        auth: typing.Optional[builtins.str] = None,
        email: typing.Optional[builtins.str] = None,
        identity_token: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        registry_token: typing.Optional[builtins.str] = None,
        server_address: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_name: hostname of the registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#host_name Image#host_name}
        :param auth: the auth token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#auth Image#auth}
        :param email: the user emal. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#email Image#email}
        :param identity_token: the identity token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#identity_token Image#identity_token}
        :param password: the registry password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#password Image#password}
        :param registry_token: the registry token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#registry_token Image#registry_token}
        :param server_address: the server address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#server_address Image#server_address}
        :param user_name: the registry user name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#user_name Image#user_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe0ffdc8439b529af22c32094d05c8923d2c37c716722ef286d69a364b211f9)
            check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument identity_token", value=identity_token, expected_type=type_hints["identity_token"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument registry_token", value=registry_token, expected_type=type_hints["registry_token"])
            check_type(argname="argument server_address", value=server_address, expected_type=type_hints["server_address"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_name": host_name,
        }
        if auth is not None:
            self._values["auth"] = auth
        if email is not None:
            self._values["email"] = email
        if identity_token is not None:
            self._values["identity_token"] = identity_token
        if password is not None:
            self._values["password"] = password
        if registry_token is not None:
            self._values["registry_token"] = registry_token
        if server_address is not None:
            self._values["server_address"] = server_address
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def host_name(self) -> builtins.str:
        '''hostname of the registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#host_name Image#host_name}
        '''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth(self) -> typing.Optional[builtins.str]:
        '''the auth token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#auth Image#auth}
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''the user emal.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#email Image#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_token(self) -> typing.Optional[builtins.str]:
        '''the identity token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#identity_token Image#identity_token}
        '''
        result = self._values.get("identity_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''the registry password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#password Image#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_token(self) -> typing.Optional[builtins.str]:
        '''the registry token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#registry_token Image#registry_token}
        '''
        result = self._values.get("registry_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_address(self) -> typing.Optional[builtins.str]:
        '''the server address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#server_address Image#server_address}
        '''
        result = self._values.get("server_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''the registry user name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#user_name Image#user_name}
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageBuildAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImageBuildAuthConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.ImageBuildAuthConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__473dde65b9a20d1fa40a041201a9b48de6b245c31f2fce1c63824d93fc790393)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ImageBuildAuthConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415dcc95f749beb1233c0447ac561a2323f42573a85603c1eef7ba87e0c1d034)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImageBuildAuthConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0d22eabc6840f48000e8937395dd184069dbb990c47741bc0fb87d9e5f2513)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a40765ce9ea756357dfbc44f9dcaa628077ce24de23fe96347e8292518e156fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b58955d702cfa518f453967075cbe027c0073cfef7940fa39f130ad68ec8dea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildAuthConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildAuthConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildAuthConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84dec10c75f36ddc47af24366fa8dd326ae9cefdd2e0a206c85fe5bdf27fe90b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImageBuildAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.ImageBuildAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac1cd6d9fdd4e7dae0f21cf660f287b3e2e87c151d11c9ad34d9a131db475316)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAuth")
    def reset_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuth", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetIdentityToken")
    def reset_identity_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityToken", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetRegistryToken")
    def reset_registry_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryToken", []))

    @jsii.member(jsii_name="resetServerAddress")
    def reset_server_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerAddress", []))

    @jsii.member(jsii_name="resetUserName")
    def reset_user_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserName", []))

    @builtins.property
    @jsii.member(jsii_name="authInput")
    def auth_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="hostNameInput")
    def host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="identityTokenInput")
    def identity_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identityTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="registryTokenInput")
    def registry_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAddressInput")
    def server_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "auth"))

    @auth.setter
    def auth(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165572c15961c0dca36ac22e0d611cb3e7a35f362446b720826a3d10f0971530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e85cc56af3c270a5c5bfee48085607e81d14336240c820c108bb64e461c430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostName")
    def host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostName"))

    @host_name.setter
    def host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247289c44d38a1323f00028fb9a01efcf43bd6b2890dba7d963536a947a58213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identityToken")
    def identity_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityToken"))

    @identity_token.setter
    def identity_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c38fc95488d65194c4677c5a101ae191ca91ab3db922a9e57d694bc5e969429f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5012fc21425225065ac9a5a426b26d5f2c234842b8025a7e53defd867c836818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryToken")
    def registry_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryToken"))

    @registry_token.setter
    def registry_token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97fcff4058835e24577287ccd073b970b9644b4e1d6c90c447a38163f1dce01b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverAddress")
    def server_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverAddress"))

    @server_address.setter
    def server_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c2071782e8b9106cdbe526fbea30409cd7450a2669927eb2a4386134cd4d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225d9b649fb537f977dc192bfc594dac506c178f1fb8dd7e3194c3a379d0adf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildAuthConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildAuthConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildAuthConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18ad30184adf62e6fd3b8722376e5df77a9a126d7af08eef0d7ef530dfc89e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImageBuildOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.ImageBuildOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9354b015bd0398c4189574117b32d7c2ca567b8413985c61dc737bc52531d617)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthConfig")
    def put_auth_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImageBuildAuthConfig, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c496be4381a9b6974582956f90187f4401f79a9d91fa4ec061a11c712b98be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAuthConfig", [value]))

    @jsii.member(jsii_name="putSecrets")
    def put_secrets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImageBuildSecrets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631b17228cc3b7e0d10f6d0310b036e3c5d2e01b2d89fd9774f0a797ac2d66f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecrets", [value]))

    @jsii.member(jsii_name="putUlimit")
    def put_ulimit(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ImageBuildUlimit", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e58f1734fb66cdb683b97f587f55c962ae164912e24465418861dc46cf05899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUlimit", [value]))

    @jsii.member(jsii_name="resetAuthConfig")
    def reset_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthConfig", []))

    @jsii.member(jsii_name="resetBuildArgs")
    def reset_build_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildArgs", []))

    @jsii.member(jsii_name="resetBuildId")
    def reset_build_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildId", []))

    @jsii.member(jsii_name="resetCacheFrom")
    def reset_cache_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacheFrom", []))

    @jsii.member(jsii_name="resetCgroupParent")
    def reset_cgroup_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCgroupParent", []))

    @jsii.member(jsii_name="resetCpuPeriod")
    def reset_cpu_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuPeriod", []))

    @jsii.member(jsii_name="resetCpuQuota")
    def reset_cpu_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuQuota", []))

    @jsii.member(jsii_name="resetCpuSetCpus")
    def reset_cpu_set_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuSetCpus", []))

    @jsii.member(jsii_name="resetCpuSetMems")
    def reset_cpu_set_mems(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuSetMems", []))

    @jsii.member(jsii_name="resetCpuShares")
    def reset_cpu_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuShares", []))

    @jsii.member(jsii_name="resetDockerfile")
    def reset_dockerfile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerfile", []))

    @jsii.member(jsii_name="resetExtraHosts")
    def reset_extra_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraHosts", []))

    @jsii.member(jsii_name="resetForceRemove")
    def reset_force_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceRemove", []))

    @jsii.member(jsii_name="resetIsolation")
    def reset_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsolation", []))

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetMemorySwap")
    def reset_memory_swap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySwap", []))

    @jsii.member(jsii_name="resetNetworkMode")
    def reset_network_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkMode", []))

    @jsii.member(jsii_name="resetNoCache")
    def reset_no_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoCache", []))

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @jsii.member(jsii_name="resetPullParent")
    def reset_pull_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullParent", []))

    @jsii.member(jsii_name="resetRemoteContext")
    def reset_remote_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteContext", []))

    @jsii.member(jsii_name="resetRemove")
    def reset_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemove", []))

    @jsii.member(jsii_name="resetSecrets")
    def reset_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecrets", []))

    @jsii.member(jsii_name="resetSecurityOpt")
    def reset_security_opt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityOpt", []))

    @jsii.member(jsii_name="resetSessionId")
    def reset_session_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionId", []))

    @jsii.member(jsii_name="resetShmSize")
    def reset_shm_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShmSize", []))

    @jsii.member(jsii_name="resetSquash")
    def reset_squash(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSquash", []))

    @jsii.member(jsii_name="resetSuppressOutput")
    def reset_suppress_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppressOutput", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetUlimit")
    def reset_ulimit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUlimit", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="authConfig")
    def auth_config(self) -> ImageBuildAuthConfigList:
        return typing.cast(ImageBuildAuthConfigList, jsii.get(self, "authConfig"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "ImageBuildSecretsList":
        return typing.cast("ImageBuildSecretsList", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="ulimit")
    def ulimit(self) -> "ImageBuildUlimitList":
        return typing.cast("ImageBuildUlimitList", jsii.get(self, "ulimit"))

    @builtins.property
    @jsii.member(jsii_name="authConfigInput")
    def auth_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildAuthConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildAuthConfig]]], jsii.get(self, "authConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="buildArgsInput")
    def build_args_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "buildArgsInput"))

    @builtins.property
    @jsii.member(jsii_name="buildIdInput")
    def build_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheFromInput")
    def cache_from_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cacheFromInput"))

    @builtins.property
    @jsii.member(jsii_name="cgroupParentInput")
    def cgroup_parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cgroupParentInput"))

    @builtins.property
    @jsii.member(jsii_name="contextInput")
    def context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuPeriodInput")
    def cpu_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuQuotaInput")
    def cpu_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSetCpusInput")
    def cpu_set_cpus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuSetCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSetMemsInput")
    def cpu_set_mems_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuSetMemsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSharesInput")
    def cpu_shares_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerfileInput")
    def dockerfile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dockerfileInput"))

    @builtins.property
    @jsii.member(jsii_name="extraHostsInput")
    def extra_hosts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extraHostsInput"))

    @builtins.property
    @jsii.member(jsii_name="forceRemoveInput")
    def force_remove_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceRemoveInput"))

    @builtins.property
    @jsii.member(jsii_name="isolationInput")
    def isolation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isolationInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySwapInput")
    def memory_swap_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memorySwapInput"))

    @builtins.property
    @jsii.member(jsii_name="networkModeInput")
    def network_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkModeInput"))

    @builtins.property
    @jsii.member(jsii_name="noCacheInput")
    def no_cache_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noCacheInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="pullParentInput")
    def pull_parent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pullParentInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteContextInput")
    def remote_context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteContextInput"))

    @builtins.property
    @jsii.member(jsii_name="removeInput")
    def remove_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "removeInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsInput")
    def secrets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildSecrets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildSecrets"]]], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityOptInput")
    def security_opt_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityOptInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionIdInput")
    def session_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="shmSizeInput")
    def shm_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "shmSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="squashInput")
    def squash_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "squashInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressOutputInput")
    def suppress_output_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suppressOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="ulimitInput")
    def ulimit_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildUlimit"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ImageBuildUlimit"]]], jsii.get(self, "ulimitInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="buildArgs")
    def build_args(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "buildArgs"))

    @build_args.setter
    def build_args(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622bdc9b42cfd83b381490a7bbd8bc2fd9baceb44e68aff505118da1a04a7632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildArgs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildId")
    def build_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildId"))

    @build_id.setter
    def build_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa3d4ef05f2e484f18286db4e69bd2b7488497e2e4df4886b0fd66c0f1bd35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheFrom")
    def cache_from(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cacheFrom"))

    @cache_from.setter
    def cache_from(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a55b9fd5bf4acecdc60da4e168452383d936adb1501f126475a99c659761f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheFrom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cgroupParent")
    def cgroup_parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cgroupParent"))

    @cgroup_parent.setter
    def cgroup_parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7246d40ca6e172e72bb721a98dd402cbf4f3f20dd7f2ecdb010fd43326b985d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cgroupParent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "context"))

    @context.setter
    def context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73daaab4d4f75fb5a559721ad6facb568d98a1f1a9fd0fe8d2c9733c0ad95bf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuPeriod")
    def cpu_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuPeriod"))

    @cpu_period.setter
    def cpu_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d757405d5a0325f3daceb2ecb992ceca4f865cee0097eda183502154d92a9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuQuota")
    def cpu_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuQuota"))

    @cpu_quota.setter
    def cpu_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17482d7e6f90532560fef9771a3f4c611cf820aad4ba1be9b244130b8e1d5396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuSetCpus")
    def cpu_set_cpus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuSetCpus"))

    @cpu_set_cpus.setter
    def cpu_set_cpus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3232572146377be6c878e7540042a24894d2de6c449cc423083e382070e1307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuSetCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuSetMems")
    def cpu_set_mems(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuSetMems"))

    @cpu_set_mems.setter
    def cpu_set_mems(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142e62b1b782b4e4fac7972f120ea00ef7c525820fe1512cd4a8a10237fd0bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuSetMems", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuShares")
    def cpu_shares(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuShares"))

    @cpu_shares.setter
    def cpu_shares(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f9e21da2187ca53d0cf207b3681d2c75f89b90eb8515278802775b107edeac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuShares", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dockerfile")
    def dockerfile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerfile"))

    @dockerfile.setter
    def dockerfile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f4eb7b61aaeff69cc5ef9df60501eacebe1411bea8a9315c7a06499cfbea38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dockerfile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="extraHosts")
    def extra_hosts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "extraHosts"))

    @extra_hosts.setter
    def extra_hosts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d820f1129d4bacbd9b5c2e8eccd5f1aca9bef08455973d793fc5c4419c1f3d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraHosts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceRemove")
    def force_remove(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceRemove"))

    @force_remove.setter
    def force_remove(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26506f102d05595aff2df4449ce0ebb4803bb5ae9fe460f559fa4aabf097d000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceRemove", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isolation")
    def isolation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isolation"))

    @isolation.setter
    def isolation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f72b8a27af5c0f9f358023b5cba7e70a95a56ab0cb9f8e0e9975e9bcecea1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "label"))

    @label.setter
    def label(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b8a2d9262014e4c21598620a7afab1489671115a74acda91806cd5c61c8aad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__599667962017ee521c7c9929c18972255992083a67404ca6300e315dfe5536c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ba59d7dc3e68ad26d13660fa6cf20481d107497ce185c1784143c1b940d0ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySwap")
    def memory_swap(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memorySwap"))

    @memory_swap.setter
    def memory_swap(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57c28f68937b1ef03f5dbda7ac4f40e772d7d35d2e20325ead43e2dbacb1ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySwap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkMode")
    def network_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkMode"))

    @network_mode.setter
    def network_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0424f33a0eeb367d8479997070a989e24be4343b9fd890c8d6dfa298ce90c154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noCache")
    def no_cache(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noCache"))

    @no_cache.setter
    def no_cache(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b97b4438e22b6eeb9e0cc8a9472ff4862a386dce514958b97d9587af501f79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCache", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97948fae82822187eec853bd39ec8bc0f72395a4786aeb1edc5b2bc335dd918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pullParent")
    def pull_parent(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pullParent"))

    @pull_parent.setter
    def pull_parent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37a1e4f21a6ddf7428cc2a03e7699cbd3c95536346fd75ec68ed789f39ba846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullParent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteContext")
    def remote_context(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteContext"))

    @remote_context.setter
    def remote_context(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6233072914d2a417649c255f246a0591399b48b91e627a55718f57e91c8f052e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteContext", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remove")
    def remove(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "remove"))

    @remove.setter
    def remove(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75120d4bab470b94cd37ce3093780341d6ef346e6816d665a1fd139bf487c869)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remove", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityOpt")
    def security_opt(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityOpt"))

    @security_opt.setter
    def security_opt(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258b3bfdaf56e305505c46abc0ac7e65b1e4df33e96a7fb4a351a7d586c343a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityOpt", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionId")
    def session_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionId"))

    @session_id.setter
    def session_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5f9e5ac79b0bd6194bc48cc0e8d32e9080c7741723beeac135684d6e589c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shmSize")
    def shm_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shmSize"))

    @shm_size.setter
    def shm_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822c71d42f98a706f13139ad6a328db182f2613ed8c45528f8ca63c6f3b97b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shmSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="squash")
    def squash(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "squash"))

    @squash.setter
    def squash(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635c16794f9e1c1020de11a1e5a03b9fccb0d2d290f756df55ac6716dc3e3c33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "squash", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suppressOutput")
    def suppress_output(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suppressOutput"))

    @suppress_output.setter
    def suppress_output(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a1338f7f84ed45d3f7ce84cea7dfee49c92325d5c9d26a1e2754bf26bfc734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppressOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7900a684f2f45d18f79730aca4550350ab5492a6e8d06d34929b1a49b91637a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3729c70c49651b4ca8d584bacb9f93840ed72a92d112126d4c52993ba5c80dc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83336a32167fe8052670f34d36f88469cff48c4f1a1a0c9f114a108a1482157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ImageBuild]:
        return typing.cast(typing.Optional[ImageBuild], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ImageBuild]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819057e8d2bb71f6969bc1d546edb208f6dba1ecc8e57dfa1807be13a2aebcc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.image.ImageBuildSecrets",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "env": "env", "src": "src"},
)
class ImageBuildSecrets:
    def __init__(
        self,
        *,
        id: builtins.str,
        env: typing.Optional[builtins.str] = None,
        src: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: ID of the secret. By default, secrets are mounted to /run/secrets/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#id Image#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param env: Environment variable source of the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#env Image#env}
        :param src: File source of the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#src Image#src}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd919e8d9770505dce6ba4af60815d0b9e2dd7609eb7fb34793bb88387d453f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument src", value=src, expected_type=type_hints["src"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if env is not None:
            self._values["env"] = env
        if src is not None:
            self._values["src"] = src

    @builtins.property
    def id(self) -> builtins.str:
        '''ID of the secret. By default, secrets are mounted to /run/secrets/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#id Image#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def env(self) -> typing.Optional[builtins.str]:
        '''Environment variable source of the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#env Image#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def src(self) -> typing.Optional[builtins.str]:
        '''File source of the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#src Image#src}
        '''
        result = self._values.get("src")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageBuildSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImageBuildSecretsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.ImageBuildSecretsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3644c284c570ca9a48bf5b918fabe64f7dc3a1494c8158660eb76e153e0f19d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ImageBuildSecretsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4541b9c625313c6f8bd725be21206a8a8cf625c7a29a18e6c8722099d79e9a66)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImageBuildSecretsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfeb92ccf1be8f5adf882adc3449862ee4c4371209eb4ea713a6836bd069ceb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7e11af66f3c15c1213151ff57e53acbc66e9889aba216173ba9d05165304c19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efac6efa62aa00031f0ad420b195d6103de306b9ad243122c15c910b1e45c07c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildSecrets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildSecrets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildSecrets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f932fd7d50fd2afe94b4e9d155e954a3ca1968cfbb6ba95e66fbcbe7f68fe050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImageBuildSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.ImageBuildSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53cf9be75fd893f3e8dafe0be27e69514d869f2a6963c594be7fe85a00f46620)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetSrc")
    def reset_src(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSrc", []))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="srcInput")
    def src_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "srcInput"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "env"))

    @env.setter
    def env(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2ced9686f7ce1e5c112c9e7535c763830cc1171754852ff1a0afc8878597af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a270884a19d07803658a039c3c3b4a8632d897e9637447dd0ff80418ef7f72cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="src")
    def src(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "src"))

    @src.setter
    def src(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b34f5ff9fb1a274a2f32ebd2e7b3a2c2eff78a3118dd0ee0ce11f7aa31e9cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "src", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildSecrets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildSecrets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildSecrets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcafcb752dba230e6fdbbcd7f73c6df8e9847615fa19bd2ae03ac467d7d5ce5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.image.ImageBuildUlimit",
    jsii_struct_bases=[],
    name_mapping={"hard": "hard", "name": "name", "soft": "soft"},
)
class ImageBuildUlimit:
    def __init__(
        self,
        *,
        hard: jsii.Number,
        name: builtins.str,
        soft: jsii.Number,
    ) -> None:
        '''
        :param hard: soft limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#hard Image#hard}
        :param name: type of ulimit, e.g. ``nofile``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#name Image#name}
        :param soft: hard limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#soft Image#soft}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fab5539f178b81de8ebf8bdd56b54276d487296ad971738cc3a3d5d6bf151a)
            check_type(argname="argument hard", value=hard, expected_type=type_hints["hard"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument soft", value=soft, expected_type=type_hints["soft"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hard": hard,
            "name": name,
            "soft": soft,
        }

    @builtins.property
    def hard(self) -> jsii.Number:
        '''soft limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#hard Image#hard}
        '''
        result = self._values.get("hard")
        assert result is not None, "Required property 'hard' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''type of ulimit, e.g. ``nofile``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#name Image#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def soft(self) -> jsii.Number:
        '''hard limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#soft Image#soft}
        '''
        result = self._values.get("soft")
        assert result is not None, "Required property 'soft' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageBuildUlimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImageBuildUlimitList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.ImageBuildUlimitList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__043a6ef6d5df9d805a12043a09a1bcc29eb1b5336d4f94e08b93d93948267eac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ImageBuildUlimitOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d5d21a6431a68b0ddab919ee810a08430df17db056d11e67ce7f020393ba0b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ImageBuildUlimitOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b962572055a8b1f18bb44aedb3e11559cd20d1059e130839ac93f7b46d52bc4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75708ab576620fe3bfa97a6f9a3f2f36a5dcc0aaf760d1b6e780eb3a7ba493e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0639fa4a44e201c7da869a4bb817dda4c653e1643268ce45eeae9c9c281a2f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildUlimit]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildUlimit]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildUlimit]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9f35676cdca104e63cca3f42d9c9754faa3fb60ffb526eca5e8e4f8a76c66b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ImageBuildUlimitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.ImageBuildUlimitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81bab0b9ab13dd9b43994e3016609600132b236f9b9aae05cc1405d72779928c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hardInput")
    def hard_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hardInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="softInput")
    def soft_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "softInput"))

    @builtins.property
    @jsii.member(jsii_name="hard")
    def hard(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hard"))

    @hard.setter
    def hard(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82f384d6c0dd2383589be591c210093a331a6748a8754651bc44cc2de903d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hard", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903dfbb0f76db6aa445c092d5b8a2e65bfad2d39a81a5f0eee49877cda31ed35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="soft")
    def soft(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "soft"))

    @soft.setter
    def soft(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bed4cc836f36ef98f4bc241d19052c08e36d25da9a176216693b88ca1cf8f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "soft", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildUlimit]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildUlimit]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildUlimit]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7d817276e907a6e18a989177737197a3e690b803b466b833b40cfca3981ff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.image.ImageConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "build_attribute": "buildAttribute",
        "force_remove": "forceRemove",
        "keep_locally": "keepLocally",
        "platform": "platform",
        "pull_triggers": "pullTriggers",
        "timeouts": "timeouts",
        "triggers": "triggers",
    },
)
class ImageConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        build_attribute: typing.Optional[typing.Union[ImageBuild, typing.Dict[builtins.str, typing.Any]]] = None,
        force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keep_locally: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        platform: typing.Optional[builtins.str] = None,
        pull_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ImageTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the Docker image, including any tags or SHA256 repo digests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#name Image#name}
        :param build_attribute: build block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build Image#build}
        :param force_remove: If true, then the image is removed forcibly when the resource is destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#force_remove Image#force_remove}
        :param keep_locally: If true, then the Docker image won't be deleted on destroy operation. If this is false, it will delete the image from the docker local storage on destroy operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#keep_locally Image#keep_locally}
        :param platform: The platform to use when pulling the image. Defaults to the platform of the current machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#platform Image#platform}
        :param pull_triggers: List of values which cause an image pull when changed. This is used to store the image digest from the registry when using the `docker_registry_image <../data-sources/registry_image.md>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#pull_triggers Image#pull_triggers}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#timeouts Image#timeouts}
        :param triggers: A map of arbitrary strings that, when changed, will force the ``docker_image`` resource to be replaced. This can be used to rebuild an image when contents of source code folders change Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#triggers Image#triggers}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(build_attribute, dict):
            build_attribute = ImageBuild(**build_attribute)
        if isinstance(timeouts, dict):
            timeouts = ImageTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e063dc09dbb9e75c5687c5d9aa99483b7c26ecff1286f18950904c14ffb30fd3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument build_attribute", value=build_attribute, expected_type=type_hints["build_attribute"])
            check_type(argname="argument force_remove", value=force_remove, expected_type=type_hints["force_remove"])
            check_type(argname="argument keep_locally", value=keep_locally, expected_type=type_hints["keep_locally"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument pull_triggers", value=pull_triggers, expected_type=type_hints["pull_triggers"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if build_attribute is not None:
            self._values["build_attribute"] = build_attribute
        if force_remove is not None:
            self._values["force_remove"] = force_remove
        if keep_locally is not None:
            self._values["keep_locally"] = keep_locally
        if platform is not None:
            self._values["platform"] = platform
        if pull_triggers is not None:
            self._values["pull_triggers"] = pull_triggers
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if triggers is not None:
            self._values["triggers"] = triggers

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
    def name(self) -> builtins.str:
        '''The name of the Docker image, including any tags or SHA256 repo digests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#name Image#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_attribute(self) -> typing.Optional[ImageBuild]:
        '''build block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#build Image#build}
        '''
        result = self._values.get("build_attribute")
        return typing.cast(typing.Optional[ImageBuild], result)

    @builtins.property
    def force_remove(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, then the image is removed forcibly when the resource is destroyed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#force_remove Image#force_remove}
        '''
        result = self._values.get("force_remove")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def keep_locally(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, then the Docker image won't be deleted on destroy operation.

        If this is false, it will delete the image from the docker local storage on destroy operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#keep_locally Image#keep_locally}
        '''
        result = self._values.get("keep_locally")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform to use when pulling the image. Defaults to the platform of the current machine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#platform Image#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values which cause an image pull when changed.

        This is used to store the image digest from the registry when using the `docker_registry_image <../data-sources/registry_image.md>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#pull_triggers Image#pull_triggers}
        '''
        result = self._values.get("pull_triggers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ImageTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#timeouts Image#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ImageTimeouts"], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of arbitrary strings that, when changed, will force the ``docker_image`` resource to be replaced.

        This can be used to rebuild an image when contents of source code folders change

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#triggers Image#triggers}
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.image.ImageTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ImageTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#create Image#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#delete Image#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#update Image#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84e3eaf6ce6ad347078a6cb38d86a90c39e9d7b3534f24aa8e5ef458efefc1b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#create Image#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#delete Image#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs/resources/image#update Image#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImageTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.image.ImageTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__061db6caa08cc70ffb7682b6bd3323719cdc31ac66eb0e2da224286f5529a2e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__042f48d6677c1eb8ed0b8c5f5ecfce42f2299cbd4a04bb5c7f97d4120d256df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42674586638e143f6b4767308b416b9503b38938c45dca6df494cccdeff5bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2563b9cf3ec01ccd126e96b037a2e8af06e54139d013392d136a7dd9cf699df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1074e9d72b40878e19467f462e017f8ea5ebb8e932bb03f6fd0f2a2c65babce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Image",
    "ImageBuild",
    "ImageBuildAuthConfig",
    "ImageBuildAuthConfigList",
    "ImageBuildAuthConfigOutputReference",
    "ImageBuildOutputReference",
    "ImageBuildSecrets",
    "ImageBuildSecretsList",
    "ImageBuildSecretsOutputReference",
    "ImageBuildUlimit",
    "ImageBuildUlimitList",
    "ImageBuildUlimitOutputReference",
    "ImageConfig",
    "ImageTimeouts",
    "ImageTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a0489b42b05476ec753523550c3227ebd9d9bdfc42b864cc237e85de1d73269e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    build_attribute: typing.Optional[typing.Union[ImageBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keep_locally: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    platform: typing.Optional[builtins.str] = None,
    pull_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ImageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__7ca1941af1df8c7b1c5eeb05c4bcd259852e78227a920ba12b50c9b1bccf9355(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe322d5a5578c25d35c1bf5cdf910897b9bce3e64cc93fbc5bd78a675fdd3cf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6207293ccbf84f9213ce31b9ad7192a842c0f36975a9ca239862e178c9b160c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1713bea97e5c741c26591528b79508b7c6d59a2ea92d138a7347f1ea95eba368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699ac4b2664b36f151c2eb8f03bf6e9b6d842eff9716e499d2f1fbb290c55a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b2857a4e25da7f0b4631af1fc41bfbfed6415f16043fb2354cb5499134f07a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714c56a23046f7bc91cd621413bd5316c2104703d7f5622743e06c0aef9958ad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3ae9a65f4eadc5c82cad3f8b730013034fdb034ec5796a0d14d707b50e859e(
    *,
    context: builtins.str,
    auth_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImageBuildAuthConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    build_id: typing.Optional[builtins.str] = None,
    cache_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    cgroup_parent: typing.Optional[builtins.str] = None,
    cpu_period: typing.Optional[jsii.Number] = None,
    cpu_quota: typing.Optional[jsii.Number] = None,
    cpu_set_cpus: typing.Optional[builtins.str] = None,
    cpu_set_mems: typing.Optional[builtins.str] = None,
    cpu_shares: typing.Optional[jsii.Number] = None,
    dockerfile: typing.Optional[builtins.str] = None,
    extra_hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
    force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    isolation: typing.Optional[builtins.str] = None,
    label: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    memory: typing.Optional[jsii.Number] = None,
    memory_swap: typing.Optional[jsii.Number] = None,
    network_mode: typing.Optional[builtins.str] = None,
    no_cache: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    platform: typing.Optional[builtins.str] = None,
    pull_parent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remote_context: typing.Optional[builtins.str] = None,
    remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImageBuildSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    security_opt: typing.Optional[typing.Sequence[builtins.str]] = None,
    session_id: typing.Optional[builtins.str] = None,
    shm_size: typing.Optional[jsii.Number] = None,
    squash: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suppress_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tag: typing.Optional[typing.Sequence[builtins.str]] = None,
    target: typing.Optional[builtins.str] = None,
    ulimit: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImageBuildUlimit, typing.Dict[builtins.str, typing.Any]]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe0ffdc8439b529af22c32094d05c8923d2c37c716722ef286d69a364b211f9(
    *,
    host_name: builtins.str,
    auth: typing.Optional[builtins.str] = None,
    email: typing.Optional[builtins.str] = None,
    identity_token: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    registry_token: typing.Optional[builtins.str] = None,
    server_address: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473dde65b9a20d1fa40a041201a9b48de6b245c31f2fce1c63824d93fc790393(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415dcc95f749beb1233c0447ac561a2323f42573a85603c1eef7ba87e0c1d034(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0d22eabc6840f48000e8937395dd184069dbb990c47741bc0fb87d9e5f2513(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40765ce9ea756357dfbc44f9dcaa628077ce24de23fe96347e8292518e156fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58955d702cfa518f453967075cbe027c0073cfef7940fa39f130ad68ec8dea0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84dec10c75f36ddc47af24366fa8dd326ae9cefdd2e0a206c85fe5bdf27fe90b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildAuthConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1cd6d9fdd4e7dae0f21cf660f287b3e2e87c151d11c9ad34d9a131db475316(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165572c15961c0dca36ac22e0d611cb3e7a35f362446b720826a3d10f0971530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e85cc56af3c270a5c5bfee48085607e81d14336240c820c108bb64e461c430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247289c44d38a1323f00028fb9a01efcf43bd6b2890dba7d963536a947a58213(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c38fc95488d65194c4677c5a101ae191ca91ab3db922a9e57d694bc5e969429f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5012fc21425225065ac9a5a426b26d5f2c234842b8025a7e53defd867c836818(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97fcff4058835e24577287ccd073b970b9644b4e1d6c90c447a38163f1dce01b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c2071782e8b9106cdbe526fbea30409cd7450a2669927eb2a4386134cd4d37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225d9b649fb537f977dc192bfc594dac506c178f1fb8dd7e3194c3a379d0adf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18ad30184adf62e6fd3b8722376e5df77a9a126d7af08eef0d7ef530dfc89e8a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildAuthConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9354b015bd0398c4189574117b32d7c2ca567b8413985c61dc737bc52531d617(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c496be4381a9b6974582956f90187f4401f79a9d91fa4ec061a11c712b98be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImageBuildAuthConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631b17228cc3b7e0d10f6d0310b036e3c5d2e01b2d89fd9774f0a797ac2d66f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImageBuildSecrets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e58f1734fb66cdb683b97f587f55c962ae164912e24465418861dc46cf05899(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ImageBuildUlimit, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622bdc9b42cfd83b381490a7bbd8bc2fd9baceb44e68aff505118da1a04a7632(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa3d4ef05f2e484f18286db4e69bd2b7488497e2e4df4886b0fd66c0f1bd35f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a55b9fd5bf4acecdc60da4e168452383d936adb1501f126475a99c659761f0b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7246d40ca6e172e72bb721a98dd402cbf4f3f20dd7f2ecdb010fd43326b985d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73daaab4d4f75fb5a559721ad6facb568d98a1f1a9fd0fe8d2c9733c0ad95bf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d757405d5a0325f3daceb2ecb992ceca4f865cee0097eda183502154d92a9f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17482d7e6f90532560fef9771a3f4c611cf820aad4ba1be9b244130b8e1d5396(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3232572146377be6c878e7540042a24894d2de6c449cc423083e382070e1307(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142e62b1b782b4e4fac7972f120ea00ef7c525820fe1512cd4a8a10237fd0bf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f9e21da2187ca53d0cf207b3681d2c75f89b90eb8515278802775b107edeac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f4eb7b61aaeff69cc5ef9df60501eacebe1411bea8a9315c7a06499cfbea38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d820f1129d4bacbd9b5c2e8eccd5f1aca9bef08455973d793fc5c4419c1f3d52(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26506f102d05595aff2df4449ce0ebb4803bb5ae9fe460f559fa4aabf097d000(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f72b8a27af5c0f9f358023b5cba7e70a95a56ab0cb9f8e0e9975e9bcecea1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b8a2d9262014e4c21598620a7afab1489671115a74acda91806cd5c61c8aad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__599667962017ee521c7c9929c18972255992083a67404ca6300e315dfe5536c8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ba59d7dc3e68ad26d13660fa6cf20481d107497ce185c1784143c1b940d0ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57c28f68937b1ef03f5dbda7ac4f40e772d7d35d2e20325ead43e2dbacb1ce9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0424f33a0eeb367d8479997070a989e24be4343b9fd890c8d6dfa298ce90c154(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b97b4438e22b6eeb9e0cc8a9472ff4862a386dce514958b97d9587af501f79(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97948fae82822187eec853bd39ec8bc0f72395a4786aeb1edc5b2bc335dd918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37a1e4f21a6ddf7428cc2a03e7699cbd3c95536346fd75ec68ed789f39ba846(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6233072914d2a417649c255f246a0591399b48b91e627a55718f57e91c8f052e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75120d4bab470b94cd37ce3093780341d6ef346e6816d665a1fd139bf487c869(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258b3bfdaf56e305505c46abc0ac7e65b1e4df33e96a7fb4a351a7d586c343a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5f9e5ac79b0bd6194bc48cc0e8d32e9080c7741723beeac135684d6e589c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822c71d42f98a706f13139ad6a328db182f2613ed8c45528f8ca63c6f3b97b0e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635c16794f9e1c1020de11a1e5a03b9fccb0d2d290f756df55ac6716dc3e3c33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a1338f7f84ed45d3f7ce84cea7dfee49c92325d5c9d26a1e2754bf26bfc734(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7900a684f2f45d18f79730aca4550350ab5492a6e8d06d34929b1a49b91637a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3729c70c49651b4ca8d584bacb9f93840ed72a92d112126d4c52993ba5c80dc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83336a32167fe8052670f34d36f88469cff48c4f1a1a0c9f114a108a1482157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819057e8d2bb71f6969bc1d546edb208f6dba1ecc8e57dfa1807be13a2aebcc5(
    value: typing.Optional[ImageBuild],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd919e8d9770505dce6ba4af60815d0b9e2dd7609eb7fb34793bb88387d453f(
    *,
    id: builtins.str,
    env: typing.Optional[builtins.str] = None,
    src: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3644c284c570ca9a48bf5b918fabe64f7dc3a1494c8158660eb76e153e0f19d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4541b9c625313c6f8bd725be21206a8a8cf625c7a29a18e6c8722099d79e9a66(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfeb92ccf1be8f5adf882adc3449862ee4c4371209eb4ea713a6836bd069ceb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e11af66f3c15c1213151ff57e53acbc66e9889aba216173ba9d05165304c19(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efac6efa62aa00031f0ad420b195d6103de306b9ad243122c15c910b1e45c07c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f932fd7d50fd2afe94b4e9d155e954a3ca1968cfbb6ba95e66fbcbe7f68fe050(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildSecrets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53cf9be75fd893f3e8dafe0be27e69514d869f2a6963c594be7fe85a00f46620(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2ced9686f7ce1e5c112c9e7535c763830cc1171754852ff1a0afc8878597af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a270884a19d07803658a039c3c3b4a8632d897e9637447dd0ff80418ef7f72cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b34f5ff9fb1a274a2f32ebd2e7b3a2c2eff78a3118dd0ee0ce11f7aa31e9cc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcafcb752dba230e6fdbbcd7f73c6df8e9847615fa19bd2ae03ac467d7d5ce5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildSecrets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fab5539f178b81de8ebf8bdd56b54276d487296ad971738cc3a3d5d6bf151a(
    *,
    hard: jsii.Number,
    name: builtins.str,
    soft: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043a6ef6d5df9d805a12043a09a1bcc29eb1b5336d4f94e08b93d93948267eac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d5d21a6431a68b0ddab919ee810a08430df17db056d11e67ce7f020393ba0b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b962572055a8b1f18bb44aedb3e11559cd20d1059e130839ac93f7b46d52bc4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75708ab576620fe3bfa97a6f9a3f2f36a5dcc0aaf760d1b6e780eb3a7ba493e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0639fa4a44e201c7da869a4bb817dda4c653e1643268ce45eeae9c9c281a2f62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9f35676cdca104e63cca3f42d9c9754faa3fb60ffb526eca5e8e4f8a76c66b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ImageBuildUlimit]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81bab0b9ab13dd9b43994e3016609600132b236f9b9aae05cc1405d72779928c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82f384d6c0dd2383589be591c210093a331a6748a8754651bc44cc2de903d2c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903dfbb0f76db6aa445c092d5b8a2e65bfad2d39a81a5f0eee49877cda31ed35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bed4cc836f36ef98f4bc241d19052c08e36d25da9a176216693b88ca1cf8f78(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7d817276e907a6e18a989177737197a3e690b803b466b833b40cfca3981ff4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageBuildUlimit]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e063dc09dbb9e75c5687c5d9aa99483b7c26ecff1286f18950904c14ffb30fd3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    build_attribute: typing.Optional[typing.Union[ImageBuild, typing.Dict[builtins.str, typing.Any]]] = None,
    force_remove: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keep_locally: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    platform: typing.Optional[builtins.str] = None,
    pull_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ImageTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    triggers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84e3eaf6ce6ad347078a6cb38d86a90c39e9d7b3534f24aa8e5ef458efefc1b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061db6caa08cc70ffb7682b6bd3323719cdc31ac66eb0e2da224286f5529a2e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042f48d6677c1eb8ed0b8c5f5ecfce42f2299cbd4a04bb5c7f97d4120d256df6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42674586638e143f6b4767308b416b9503b38938c45dca6df494cccdeff5bb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2563b9cf3ec01ccd126e96b037a2e8af06e54139d013392d136a7dd9cf699df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1074e9d72b40878e19467f462e017f8ea5ebb8e932bb03f6fd0f2a2c65babce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ImageTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
