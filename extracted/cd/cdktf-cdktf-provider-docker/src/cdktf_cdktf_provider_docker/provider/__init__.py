r'''
# `provider`

Refer to the Terraform Registry for docs: [`docker`](https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs).
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


class DockerProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-docker.provider.DockerProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs docker}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        ca_material: typing.Optional[builtins.str] = None,
        cert_material: typing.Optional[builtins.str] = None,
        cert_path: typing.Optional[builtins.str] = None,
        context: typing.Optional[builtins.str] = None,
        disable_docker_daemon_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host: typing.Optional[builtins.str] = None,
        key_material: typing.Optional[builtins.str] = None,
        registry_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DockerProviderRegistryAuth", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs docker} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#alias DockerProvider#alias}
        :param ca_material: PEM-encoded content of Docker host CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#ca_material DockerProvider#ca_material}
        :param cert_material: PEM-encoded content of Docker client certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#cert_material DockerProvider#cert_material}
        :param cert_path: Path to directory with Docker TLS config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#cert_path DockerProvider#cert_path}
        :param context: The name of the Docker context to use. Can also be set via ``DOCKER_CONTEXT`` environment variable. Overrides the ``host`` if set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#context DockerProvider#context}
        :param disable_docker_daemon_check: If set to ``true``, the provider will not check if the Docker daemon is running. This is useful for resources/data_sourcess that do not require a running Docker daemon, such as the data source ``docker_registry_image``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#disable_docker_daemon_check DockerProvider#disable_docker_daemon_check}
        :param host: The Docker daemon address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#host DockerProvider#host}
        :param key_material: PEM-encoded content of Docker client private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#key_material DockerProvider#key_material}
        :param registry_auth: registry_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#registry_auth DockerProvider#registry_auth}
        :param ssh_opts: Additional SSH option flags to be appended when using ``ssh://`` protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#ssh_opts DockerProvider#ssh_opts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da705188ecca01a700ef94fd2de8d6f53c7cfd16da3f4ca09db4e6e6b05f171a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DockerProviderConfig(
            alias=alias,
            ca_material=ca_material,
            cert_material=cert_material,
            cert_path=cert_path,
            context=context,
            disable_docker_daemon_check=disable_docker_daemon_check,
            host=host,
            key_material=key_material,
            registry_auth=registry_auth,
            ssh_opts=ssh_opts,
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
        '''Generates CDKTF code for importing a DockerProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DockerProvider to import.
        :param import_from_id: The id of the existing DockerProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DockerProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__012b0f86192221ff7f02a4cec1397023f6ac63b38bc4fb3770bca672ee0e2da9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetCaMaterial")
    def reset_ca_material(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaMaterial", []))

    @jsii.member(jsii_name="resetCertMaterial")
    def reset_cert_material(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertMaterial", []))

    @jsii.member(jsii_name="resetCertPath")
    def reset_cert_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertPath", []))

    @jsii.member(jsii_name="resetContext")
    def reset_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContext", []))

    @jsii.member(jsii_name="resetDisableDockerDaemonCheck")
    def reset_disable_docker_daemon_check(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableDockerDaemonCheck", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetKeyMaterial")
    def reset_key_material(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyMaterial", []))

    @jsii.member(jsii_name="resetRegistryAuth")
    def reset_registry_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryAuth", []))

    @jsii.member(jsii_name="resetSshOpts")
    def reset_ssh_opts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshOpts", []))

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
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="caMaterialInput")
    def ca_material_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caMaterialInput"))

    @builtins.property
    @jsii.member(jsii_name="certMaterialInput")
    def cert_material_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certMaterialInput"))

    @builtins.property
    @jsii.member(jsii_name="certPathInput")
    def cert_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certPathInput"))

    @builtins.property
    @jsii.member(jsii_name="contextInput")
    def context_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextInput"))

    @builtins.property
    @jsii.member(jsii_name="disableDockerDaemonCheckInput")
    def disable_docker_daemon_check_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableDockerDaemonCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="keyMaterialInput")
    def key_material_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyMaterialInput"))

    @builtins.property
    @jsii.member(jsii_name="registryAuthInput")
    def registry_auth_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DockerProviderRegistryAuth"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DockerProviderRegistryAuth"]]], jsii.get(self, "registryAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="sshOptsInput")
    def ssh_opts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshOptsInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa394c0495de6dd1041509289e9c13d048f68da31e6adb4ba2317221ba726663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="caMaterial")
    def ca_material(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caMaterial"))

    @ca_material.setter
    def ca_material(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990ceda2f47d3db26bfe1703b8257df790219af4f8e5de9372aed21c69fb1bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caMaterial", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certMaterial")
    def cert_material(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certMaterial"))

    @cert_material.setter
    def cert_material(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295486daf6ac4fc3687b7f4c9d31e59c30669848191b7e5e0fa819a193a9b76e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certMaterial", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certPath")
    def cert_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certPath"))

    @cert_path.setter
    def cert_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2287547299b0ce87a100f3a06d7d34fbd6e786920d5b2a7bf20b539fd521e2d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="context")
    def context(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "context"))

    @context.setter
    def context(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aede1b42729a492f8b48e507fd26618244f1629ac630013e4cc6f5a8ab86c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "context", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableDockerDaemonCheck")
    def disable_docker_daemon_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableDockerDaemonCheck"))

    @disable_docker_daemon_check.setter
    def disable_docker_daemon_check(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37adec8f2c2561afe6ab1a8e94b06292a5501e49324c295e819b344b19b57a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableDockerDaemonCheck", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "host"))

    @host.setter
    def host(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bcbc08e6d5fcc63955ed6a2f683a31be8fa9586909850f4cb60b8bb01dfbe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyMaterial")
    def key_material(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyMaterial"))

    @key_material.setter
    def key_material(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cfc87867f4655e5c0265a2a6e63497155bb9ea4d77cba574ebf05bd15280743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyMaterial", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryAuth")
    def registry_auth(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DockerProviderRegistryAuth"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DockerProviderRegistryAuth"]]], jsii.get(self, "registryAuth"))

    @registry_auth.setter
    def registry_auth(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DockerProviderRegistryAuth"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aca036998b328fdb571f534ea2d10758957058672bc2b698275e3d053946730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryAuth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sshOpts")
    def ssh_opts(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sshOpts"))

    @ssh_opts.setter
    def ssh_opts(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5524bfa2953e44353f1438e50afcf54da36378100efda139fd9c848abc1c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshOpts", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.provider.DockerProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "ca_material": "caMaterial",
        "cert_material": "certMaterial",
        "cert_path": "certPath",
        "context": "context",
        "disable_docker_daemon_check": "disableDockerDaemonCheck",
        "host": "host",
        "key_material": "keyMaterial",
        "registry_auth": "registryAuth",
        "ssh_opts": "sshOpts",
    },
)
class DockerProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        ca_material: typing.Optional[builtins.str] = None,
        cert_material: typing.Optional[builtins.str] = None,
        cert_path: typing.Optional[builtins.str] = None,
        context: typing.Optional[builtins.str] = None,
        disable_docker_daemon_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host: typing.Optional[builtins.str] = None,
        key_material: typing.Optional[builtins.str] = None,
        registry_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DockerProviderRegistryAuth", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ssh_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#alias DockerProvider#alias}
        :param ca_material: PEM-encoded content of Docker host CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#ca_material DockerProvider#ca_material}
        :param cert_material: PEM-encoded content of Docker client certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#cert_material DockerProvider#cert_material}
        :param cert_path: Path to directory with Docker TLS config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#cert_path DockerProvider#cert_path}
        :param context: The name of the Docker context to use. Can also be set via ``DOCKER_CONTEXT`` environment variable. Overrides the ``host`` if set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#context DockerProvider#context}
        :param disable_docker_daemon_check: If set to ``true``, the provider will not check if the Docker daemon is running. This is useful for resources/data_sourcess that do not require a running Docker daemon, such as the data source ``docker_registry_image``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#disable_docker_daemon_check DockerProvider#disable_docker_daemon_check}
        :param host: The Docker daemon address. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#host DockerProvider#host}
        :param key_material: PEM-encoded content of Docker client private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#key_material DockerProvider#key_material}
        :param registry_auth: registry_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#registry_auth DockerProvider#registry_auth}
        :param ssh_opts: Additional SSH option flags to be appended when using ``ssh://`` protocol. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#ssh_opts DockerProvider#ssh_opts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbe7a4e906bed7b4d543285ccc96150e24451a9e97c513028a5551dd9a9d691)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument ca_material", value=ca_material, expected_type=type_hints["ca_material"])
            check_type(argname="argument cert_material", value=cert_material, expected_type=type_hints["cert_material"])
            check_type(argname="argument cert_path", value=cert_path, expected_type=type_hints["cert_path"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument disable_docker_daemon_check", value=disable_docker_daemon_check, expected_type=type_hints["disable_docker_daemon_check"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument key_material", value=key_material, expected_type=type_hints["key_material"])
            check_type(argname="argument registry_auth", value=registry_auth, expected_type=type_hints["registry_auth"])
            check_type(argname="argument ssh_opts", value=ssh_opts, expected_type=type_hints["ssh_opts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if ca_material is not None:
            self._values["ca_material"] = ca_material
        if cert_material is not None:
            self._values["cert_material"] = cert_material
        if cert_path is not None:
            self._values["cert_path"] = cert_path
        if context is not None:
            self._values["context"] = context
        if disable_docker_daemon_check is not None:
            self._values["disable_docker_daemon_check"] = disable_docker_daemon_check
        if host is not None:
            self._values["host"] = host
        if key_material is not None:
            self._values["key_material"] = key_material
        if registry_auth is not None:
            self._values["registry_auth"] = registry_auth
        if ssh_opts is not None:
            self._values["ssh_opts"] = ssh_opts

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#alias DockerProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_material(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded content of Docker host CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#ca_material DockerProvider#ca_material}
        '''
        result = self._values.get("ca_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert_material(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded content of Docker client certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#cert_material DockerProvider#cert_material}
        '''
        result = self._values.get("cert_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert_path(self) -> typing.Optional[builtins.str]:
        '''Path to directory with Docker TLS config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#cert_path DockerProvider#cert_path}
        '''
        result = self._values.get("cert_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context(self) -> typing.Optional[builtins.str]:
        '''The name of the Docker context to use.

        Can also be set via ``DOCKER_CONTEXT`` environment variable. Overrides the ``host`` if set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#context DockerProvider#context}
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_docker_daemon_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to ``true``, the provider will not check if the Docker daemon is running.

        This is useful for resources/data_sourcess that do not require a running Docker daemon, such as the data source ``docker_registry_image``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#disable_docker_daemon_check DockerProvider#disable_docker_daemon_check}
        '''
        result = self._values.get("disable_docker_daemon_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The Docker daemon address.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#host DockerProvider#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_material(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded content of Docker client private key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#key_material DockerProvider#key_material}
        '''
        result = self._values.get("key_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_auth(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DockerProviderRegistryAuth"]]]:
        '''registry_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#registry_auth DockerProvider#registry_auth}
        '''
        result = self._values.get("registry_auth")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DockerProviderRegistryAuth"]]], result)

    @builtins.property
    def ssh_opts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional SSH option flags to be appended when using ``ssh://`` protocol.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#ssh_opts DockerProvider#ssh_opts}
        '''
        result = self._values.get("ssh_opts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-docker.provider.DockerProviderRegistryAuth",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "auth_disabled": "authDisabled",
        "config_file": "configFile",
        "config_file_content": "configFileContent",
        "password": "password",
        "username": "username",
    },
)
class DockerProviderRegistryAuth:
    def __init__(
        self,
        *,
        address: builtins.str,
        auth_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        config_file: typing.Optional[builtins.str] = None,
        config_file_content: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: Address of the registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#address DockerProvider#address}
        :param auth_disabled: Setting this to ``true`` will tell the provider that this registry does not need authentication. Due to the docker internals, the provider will use dummy credentials (see https://github.com/kreuzwerker/terraform-provider-docker/issues/470 for more information). Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#auth_disabled DockerProvider#auth_disabled}
        :param config_file: Path to docker json file for registry auth. Defaults to ``~/.docker/config.json``. If ``DOCKER_CONFIG`` is set, the value of ``DOCKER_CONFIG`` is used as the path. ``config_file`` has predencen over all other options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#config_file DockerProvider#config_file}
        :param config_file_content: Plain content of the docker json file for registry auth. ``config_file_content`` has precedence over username/password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#config_file_content DockerProvider#config_file_content}
        :param password: Password for the registry. Defaults to ``DOCKER_REGISTRY_PASS`` env variable if set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#password DockerProvider#password}
        :param username: Username for the registry. Defaults to ``DOCKER_REGISTRY_USER`` env variable if set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#username DockerProvider#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeba38e4892015607d46c384ab0174b5e367ad501cdc0a696caab0ab8548ec1b)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument auth_disabled", value=auth_disabled, expected_type=type_hints["auth_disabled"])
            check_type(argname="argument config_file", value=config_file, expected_type=type_hints["config_file"])
            check_type(argname="argument config_file_content", value=config_file_content, expected_type=type_hints["config_file_content"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
        }
        if auth_disabled is not None:
            self._values["auth_disabled"] = auth_disabled
        if config_file is not None:
            self._values["config_file"] = config_file
        if config_file_content is not None:
            self._values["config_file_content"] = config_file_content
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def address(self) -> builtins.str:
        '''Address of the registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#address DockerProvider#address}
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Setting this to ``true`` will tell the provider that this registry does not need authentication.

        Due to the docker internals, the provider will use dummy credentials (see https://github.com/kreuzwerker/terraform-provider-docker/issues/470 for more information). Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#auth_disabled DockerProvider#auth_disabled}
        '''
        result = self._values.get("auth_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def config_file(self) -> typing.Optional[builtins.str]:
        '''Path to docker json file for registry auth.

        Defaults to ``~/.docker/config.json``. If ``DOCKER_CONFIG`` is set, the value of ``DOCKER_CONFIG`` is used as the path. ``config_file`` has predencen over all other options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#config_file DockerProvider#config_file}
        '''
        result = self._values.get("config_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_file_content(self) -> typing.Optional[builtins.str]:
        '''Plain content of the docker json file for registry auth. ``config_file_content`` has precedence over username/password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#config_file_content DockerProvider#config_file_content}
        '''
        result = self._values.get("config_file_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for the registry. Defaults to ``DOCKER_REGISTRY_PASS`` env variable if set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#password DockerProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username for the registry. Defaults to ``DOCKER_REGISTRY_USER`` env variable if set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.4.0/docs#username DockerProvider#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerProviderRegistryAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DockerProvider",
    "DockerProviderConfig",
    "DockerProviderRegistryAuth",
]

publication.publish()

def _typecheckingstub__da705188ecca01a700ef94fd2de8d6f53c7cfd16da3f4ca09db4e6e6b05f171a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    ca_material: typing.Optional[builtins.str] = None,
    cert_material: typing.Optional[builtins.str] = None,
    cert_path: typing.Optional[builtins.str] = None,
    context: typing.Optional[builtins.str] = None,
    disable_docker_daemon_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host: typing.Optional[builtins.str] = None,
    key_material: typing.Optional[builtins.str] = None,
    registry_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DockerProviderRegistryAuth, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__012b0f86192221ff7f02a4cec1397023f6ac63b38bc4fb3770bca672ee0e2da9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa394c0495de6dd1041509289e9c13d048f68da31e6adb4ba2317221ba726663(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990ceda2f47d3db26bfe1703b8257df790219af4f8e5de9372aed21c69fb1bda(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295486daf6ac4fc3687b7f4c9d31e59c30669848191b7e5e0fa819a193a9b76e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2287547299b0ce87a100f3a06d7d34fbd6e786920d5b2a7bf20b539fd521e2d3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aede1b42729a492f8b48e507fd26618244f1629ac630013e4cc6f5a8ab86c1a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37adec8f2c2561afe6ab1a8e94b06292a5501e49324c295e819b344b19b57a1(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bcbc08e6d5fcc63955ed6a2f683a31be8fa9586909850f4cb60b8bb01dfbe7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfc87867f4655e5c0265a2a6e63497155bb9ea4d77cba574ebf05bd15280743(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aca036998b328fdb571f534ea2d10758957058672bc2b698275e3d053946730(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DockerProviderRegistryAuth]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5524bfa2953e44353f1438e50afcf54da36378100efda139fd9c848abc1c09(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbe7a4e906bed7b4d543285ccc96150e24451a9e97c513028a5551dd9a9d691(
    *,
    alias: typing.Optional[builtins.str] = None,
    ca_material: typing.Optional[builtins.str] = None,
    cert_material: typing.Optional[builtins.str] = None,
    cert_path: typing.Optional[builtins.str] = None,
    context: typing.Optional[builtins.str] = None,
    disable_docker_daemon_check: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host: typing.Optional[builtins.str] = None,
    key_material: typing.Optional[builtins.str] = None,
    registry_auth: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DockerProviderRegistryAuth, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ssh_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeba38e4892015607d46c384ab0174b5e367ad501cdc0a696caab0ab8548ec1b(
    *,
    address: builtins.str,
    auth_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    config_file: typing.Optional[builtins.str] = None,
    config_file_content: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
