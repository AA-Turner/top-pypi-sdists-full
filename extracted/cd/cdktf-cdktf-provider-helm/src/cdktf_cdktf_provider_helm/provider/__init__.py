r'''
# `provider`

Refer to the Terraform Registry for docs: [`helm`](https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs).
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


class HelmProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.provider.HelmProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs helm}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        burst_limit: typing.Optional[jsii.Number] = None,
        debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        experiments: typing.Optional[typing.Union["HelmProviderExperiments", typing.Dict[builtins.str, typing.Any]]] = None,
        helm_driver: typing.Optional[builtins.str] = None,
        kubernetes: typing.Optional[typing.Union["HelmProviderKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        plugins_path: typing.Optional[builtins.str] = None,
        registries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HelmProviderRegistries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        registry_config_path: typing.Optional[builtins.str] = None,
        repository_cache: typing.Optional[builtins.str] = None,
        repository_config_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs helm} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#alias HelmProvider#alias}
        :param burst_limit: Helm burst limit. Increase this if you have a cluster with many CRDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#burst_limit HelmProvider#burst_limit}
        :param debug: Debug indicates whether or not Helm is running in Debug mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#debug HelmProvider#debug}
        :param experiments: Enable and disable experimental features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#experiments HelmProvider#experiments}
        :param helm_driver: The backend storage driver. Values are: configmap, secret, memory, sql. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#helm_driver HelmProvider#helm_driver}
        :param kubernetes: Kubernetes Configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#kubernetes HelmProvider#kubernetes}
        :param plugins_path: The path to the helm plugins directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#plugins_path HelmProvider#plugins_path}
        :param registries: RegistryClient configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#registries HelmProvider#registries}
        :param registry_config_path: The path to the registry config file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#registry_config_path HelmProvider#registry_config_path}
        :param repository_cache: The path to the file containing cached repository indexes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#repository_cache HelmProvider#repository_cache}
        :param repository_config_path: The path to the file containing repository names and URLs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#repository_config_path HelmProvider#repository_config_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9b1d29236885254322c77ebb49db4debaa433e29b9dba83d7fbc53fe1d63a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = HelmProviderConfig(
            alias=alias,
            burst_limit=burst_limit,
            debug=debug,
            experiments=experiments,
            helm_driver=helm_driver,
            kubernetes=kubernetes,
            plugins_path=plugins_path,
            registries=registries,
            registry_config_path=registry_config_path,
            repository_cache=repository_cache,
            repository_config_path=repository_config_path,
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
        '''Generates CDKTF code for importing a HelmProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HelmProvider to import.
        :param import_from_id: The id of the existing HelmProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HelmProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123313e4dc1c57c04c45cc3be5ca11f152571e1e497a6a13eb40e3508b4f840b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetBurstLimit")
    def reset_burst_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBurstLimit", []))

    @jsii.member(jsii_name="resetDebug")
    def reset_debug(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDebug", []))

    @jsii.member(jsii_name="resetExperiments")
    def reset_experiments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExperiments", []))

    @jsii.member(jsii_name="resetHelmDriver")
    def reset_helm_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHelmDriver", []))

    @jsii.member(jsii_name="resetKubernetes")
    def reset_kubernetes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetes", []))

    @jsii.member(jsii_name="resetPluginsPath")
    def reset_plugins_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginsPath", []))

    @jsii.member(jsii_name="resetRegistries")
    def reset_registries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistries", []))

    @jsii.member(jsii_name="resetRegistryConfigPath")
    def reset_registry_config_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryConfigPath", []))

    @jsii.member(jsii_name="resetRepositoryCache")
    def reset_repository_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryCache", []))

    @jsii.member(jsii_name="resetRepositoryConfigPath")
    def reset_repository_config_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryConfigPath", []))

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
    @jsii.member(jsii_name="burstLimitInput")
    def burst_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "burstLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="debugInput")
    def debug_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "debugInput"))

    @builtins.property
    @jsii.member(jsii_name="experimentsInput")
    def experiments_input(self) -> typing.Optional["HelmProviderExperiments"]:
        return typing.cast(typing.Optional["HelmProviderExperiments"], jsii.get(self, "experimentsInput"))

    @builtins.property
    @jsii.member(jsii_name="helmDriverInput")
    def helm_driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "helmDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesInput")
    def kubernetes_input(self) -> typing.Optional["HelmProviderKubernetes"]:
        return typing.cast(typing.Optional["HelmProviderKubernetes"], jsii.get(self, "kubernetesInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginsPathInput")
    def plugins_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginsPathInput"))

    @builtins.property
    @jsii.member(jsii_name="registriesInput")
    def registries_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HelmProviderRegistries"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HelmProviderRegistries"]]], jsii.get(self, "registriesInput"))

    @builtins.property
    @jsii.member(jsii_name="registryConfigPathInput")
    def registry_config_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryConfigPathInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCacheInput")
    def repository_cache_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryCacheInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryConfigPathInput")
    def repository_config_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryConfigPathInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c8d100c082c1b44d45d308583d76102336ca6627dda5440b68f792ae7e709c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="burstLimit")
    def burst_limit(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "burstLimit"))

    @burst_limit.setter
    def burst_limit(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ea915f57f0846c46350065f633c6c7a90cc0ec878e1e157f9632ff3b34ee84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "burstLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="debug")
    def debug(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "debug"))

    @debug.setter
    def debug(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71c4802c45cbb0d4e22f2e2c6527680fb1ae913859591829c2d2e73d49630a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "debug", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="experiments")
    def experiments(self) -> typing.Optional["HelmProviderExperiments"]:
        return typing.cast(typing.Optional["HelmProviderExperiments"], jsii.get(self, "experiments"))

    @experiments.setter
    def experiments(self, value: typing.Optional["HelmProviderExperiments"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7ca3f5c43d109af69ebe9986048dff1f4e81e5000f32ac493e073abe99b695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "experiments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="helmDriver")
    def helm_driver(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "helmDriver"))

    @helm_driver.setter
    def helm_driver(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2d5af5a79a70e391e6ed89e2fc09113460645ef53c14dc53450ddf7dee323b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "helmDriver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubernetes")
    def kubernetes(self) -> typing.Optional["HelmProviderKubernetes"]:
        return typing.cast(typing.Optional["HelmProviderKubernetes"], jsii.get(self, "kubernetes"))

    @kubernetes.setter
    def kubernetes(self, value: typing.Optional["HelmProviderKubernetes"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3deb2b4dafca7e58ca548c00f93e2be543424dec0966dedfcee56e2d4bc42511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pluginsPath")
    def plugins_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginsPath"))

    @plugins_path.setter
    def plugins_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757dd31649762ccdd94b64c3463943e1263ef6c177ca2d9574f8227cd996c2a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginsPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registries")
    def registries(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HelmProviderRegistries"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HelmProviderRegistries"]]], jsii.get(self, "registries"))

    @registries.setter
    def registries(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HelmProviderRegistries"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5168b9aec6e4a1d8cdfac3d78c746151491d6ca73ee21b19bffc0b1a0a3bd005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryConfigPath")
    def registry_config_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryConfigPath"))

    @registry_config_path.setter
    def registry_config_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fac8e2776395bbfffe943a14a74bf425a51cf8b29cd8b1167a6fa7d488cf373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryConfigPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryCache")
    def repository_cache(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryCache"))

    @repository_cache.setter
    def repository_cache(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054c1253b2d4168585cad86a1c74df51ef8aa4949c8fb96911a43d680815098f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCache", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryConfigPath")
    def repository_config_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryConfigPath"))

    @repository_config_path.setter
    def repository_config_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca5ccc55fc9833150a2c2322e6b495be83cfed1ce99147b59db3438ee95c0d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryConfigPath", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.provider.HelmProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "burst_limit": "burstLimit",
        "debug": "debug",
        "experiments": "experiments",
        "helm_driver": "helmDriver",
        "kubernetes": "kubernetes",
        "plugins_path": "pluginsPath",
        "registries": "registries",
        "registry_config_path": "registryConfigPath",
        "repository_cache": "repositoryCache",
        "repository_config_path": "repositoryConfigPath",
    },
)
class HelmProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        burst_limit: typing.Optional[jsii.Number] = None,
        debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        experiments: typing.Optional[typing.Union["HelmProviderExperiments", typing.Dict[builtins.str, typing.Any]]] = None,
        helm_driver: typing.Optional[builtins.str] = None,
        kubernetes: typing.Optional[typing.Union["HelmProviderKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        plugins_path: typing.Optional[builtins.str] = None,
        registries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HelmProviderRegistries", typing.Dict[builtins.str, typing.Any]]]]] = None,
        registry_config_path: typing.Optional[builtins.str] = None,
        repository_cache: typing.Optional[builtins.str] = None,
        repository_config_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#alias HelmProvider#alias}
        :param burst_limit: Helm burst limit. Increase this if you have a cluster with many CRDs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#burst_limit HelmProvider#burst_limit}
        :param debug: Debug indicates whether or not Helm is running in Debug mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#debug HelmProvider#debug}
        :param experiments: Enable and disable experimental features. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#experiments HelmProvider#experiments}
        :param helm_driver: The backend storage driver. Values are: configmap, secret, memory, sql. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#helm_driver HelmProvider#helm_driver}
        :param kubernetes: Kubernetes Configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#kubernetes HelmProvider#kubernetes}
        :param plugins_path: The path to the helm plugins directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#plugins_path HelmProvider#plugins_path}
        :param registries: RegistryClient configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#registries HelmProvider#registries}
        :param registry_config_path: The path to the registry config file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#registry_config_path HelmProvider#registry_config_path}
        :param repository_cache: The path to the file containing cached repository indexes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#repository_cache HelmProvider#repository_cache}
        :param repository_config_path: The path to the file containing repository names and URLs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#repository_config_path HelmProvider#repository_config_path}
        '''
        if isinstance(experiments, dict):
            experiments = HelmProviderExperiments(**experiments)
        if isinstance(kubernetes, dict):
            kubernetes = HelmProviderKubernetes(**kubernetes)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf846e980a90ecff087864941949dc254940696c8e5d0be8d4bae4f0f4aa0a9)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument burst_limit", value=burst_limit, expected_type=type_hints["burst_limit"])
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
            check_type(argname="argument experiments", value=experiments, expected_type=type_hints["experiments"])
            check_type(argname="argument helm_driver", value=helm_driver, expected_type=type_hints["helm_driver"])
            check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
            check_type(argname="argument plugins_path", value=plugins_path, expected_type=type_hints["plugins_path"])
            check_type(argname="argument registries", value=registries, expected_type=type_hints["registries"])
            check_type(argname="argument registry_config_path", value=registry_config_path, expected_type=type_hints["registry_config_path"])
            check_type(argname="argument repository_cache", value=repository_cache, expected_type=type_hints["repository_cache"])
            check_type(argname="argument repository_config_path", value=repository_config_path, expected_type=type_hints["repository_config_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if burst_limit is not None:
            self._values["burst_limit"] = burst_limit
        if debug is not None:
            self._values["debug"] = debug
        if experiments is not None:
            self._values["experiments"] = experiments
        if helm_driver is not None:
            self._values["helm_driver"] = helm_driver
        if kubernetes is not None:
            self._values["kubernetes"] = kubernetes
        if plugins_path is not None:
            self._values["plugins_path"] = plugins_path
        if registries is not None:
            self._values["registries"] = registries
        if registry_config_path is not None:
            self._values["registry_config_path"] = registry_config_path
        if repository_cache is not None:
            self._values["repository_cache"] = repository_cache
        if repository_config_path is not None:
            self._values["repository_config_path"] = repository_config_path

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#alias HelmProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def burst_limit(self) -> typing.Optional[jsii.Number]:
        '''Helm burst limit. Increase this if you have a cluster with many CRDs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#burst_limit HelmProvider#burst_limit}
        '''
        result = self._values.get("burst_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def debug(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Debug indicates whether or not Helm is running in Debug mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#debug HelmProvider#debug}
        '''
        result = self._values.get("debug")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def experiments(self) -> typing.Optional["HelmProviderExperiments"]:
        '''Enable and disable experimental features.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#experiments HelmProvider#experiments}
        '''
        result = self._values.get("experiments")
        return typing.cast(typing.Optional["HelmProviderExperiments"], result)

    @builtins.property
    def helm_driver(self) -> typing.Optional[builtins.str]:
        '''The backend storage driver. Values are: configmap, secret, memory, sql.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#helm_driver HelmProvider#helm_driver}
        '''
        result = self._values.get("helm_driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes(self) -> typing.Optional["HelmProviderKubernetes"]:
        '''Kubernetes Configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#kubernetes HelmProvider#kubernetes}
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["HelmProviderKubernetes"], result)

    @builtins.property
    def plugins_path(self) -> typing.Optional[builtins.str]:
        '''The path to the helm plugins directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#plugins_path HelmProvider#plugins_path}
        '''
        result = self._values.get("plugins_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registries(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HelmProviderRegistries"]]]:
        '''RegistryClient configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#registries HelmProvider#registries}
        '''
        result = self._values.get("registries")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HelmProviderRegistries"]]], result)

    @builtins.property
    def registry_config_path(self) -> typing.Optional[builtins.str]:
        '''The path to the registry config file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#registry_config_path HelmProvider#registry_config_path}
        '''
        result = self._values.get("registry_config_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_cache(self) -> typing.Optional[builtins.str]:
        '''The path to the file containing cached repository indexes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#repository_cache HelmProvider#repository_cache}
        '''
        result = self._values.get("repository_cache")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_config_path(self) -> typing.Optional[builtins.str]:
        '''The path to the file containing repository names and URLs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#repository_config_path HelmProvider#repository_config_path}
        '''
        result = self._values.get("repository_config_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.provider.HelmProviderExperiments",
    jsii_struct_bases=[],
    name_mapping={"manifest": "manifest"},
)
class HelmProviderExperiments:
    def __init__(
        self,
        *,
        manifest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param manifest: Enable full diff by storing the rendered manifest in the state. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#manifest HelmProvider#manifest}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0975af09e993360c7b82d25c4fdbe476021cece87b3feb51429d13f8dac830)
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manifest is not None:
            self._values["manifest"] = manifest

    @builtins.property
    def manifest(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable full diff by storing the rendered manifest in the state.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#manifest HelmProvider#manifest}
        '''
        result = self._values.get("manifest")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmProviderExperiments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.provider.HelmProviderKubernetes",
    jsii_struct_bases=[],
    name_mapping={
        "client_certificate": "clientCertificate",
        "client_key": "clientKey",
        "cluster_ca_certificate": "clusterCaCertificate",
        "config_context": "configContext",
        "config_context_auth_info": "configContextAuthInfo",
        "config_context_cluster": "configContextCluster",
        "config_path": "configPath",
        "config_paths": "configPaths",
        "exec": "exec",
        "host": "host",
        "insecure": "insecure",
        "password": "password",
        "proxy_url": "proxyUrl",
        "tls_server_name": "tlsServerName",
        "token": "token",
        "username": "username",
    },
)
class HelmProviderKubernetes:
    def __init__(
        self,
        *,
        client_certificate: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        cluster_ca_certificate: typing.Optional[builtins.str] = None,
        config_context: typing.Optional[builtins.str] = None,
        config_context_auth_info: typing.Optional[builtins.str] = None,
        config_context_cluster: typing.Optional[builtins.str] = None,
        config_path: typing.Optional[builtins.str] = None,
        config_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        exec: typing.Optional[typing.Union["HelmProviderKubernetesExec", typing.Dict[builtins.str, typing.Any]]] = None,
        host: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        proxy_url: typing.Optional[builtins.str] = None,
        tls_server_name: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_certificate: PEM-encoded client certificate for TLS authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#client_certificate HelmProvider#client_certificate}
        :param client_key: PEM-encoded client certificate key for TLS authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#client_key HelmProvider#client_key}
        :param cluster_ca_certificate: PEM-encoded root certificates bundle for TLS authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#cluster_ca_certificate HelmProvider#cluster_ca_certificate}
        :param config_context: Context to choose from the config file. Can be sourced from KUBE_CTX. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_context HelmProvider#config_context}
        :param config_context_auth_info: Authentication info context of the kube config (name of the kubeconfig user, --user flag in kubectl). Can be sourced from KUBE_CTX_AUTH_INFO. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_context_auth_info HelmProvider#config_context_auth_info}
        :param config_context_cluster: Cluster context of the kube config (name of the kubeconfig cluster, --cluster flag in kubectl). Can be sourced from KUBE_CTX_CLUSTER. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_context_cluster HelmProvider#config_context_cluster}
        :param config_path: Path to the kube config file. Can be set with KUBE_CONFIG_PATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_path HelmProvider#config_path}
        :param config_paths: A list of paths to kube config files. Can be set with KUBE_CONFIG_PATHS environment variable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_paths HelmProvider#config_paths}
        :param exec: Exec configuration for Kubernetes authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#exec HelmProvider#exec}
        :param host: The hostname (in form of URI) of kubernetes master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#host HelmProvider#host}
        :param insecure: Whether server should be accessed without verifying the TLS certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#insecure HelmProvider#insecure}
        :param password: The password to use for HTTP basic authentication when accessing the Kubernetes master endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#password HelmProvider#password}
        :param proxy_url: URL to the proxy to be used for all API requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#proxy_url HelmProvider#proxy_url}
        :param tls_server_name: Server name passed to the server for SNI and is used in the client to check server certificates against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#tls_server_name HelmProvider#tls_server_name}
        :param token: Token to authenticate a service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#token HelmProvider#token}
        :param username: The username to use for HTTP basic authentication when accessing the Kubernetes master endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#username HelmProvider#username}
        '''
        if isinstance(exec, dict):
            exec = HelmProviderKubernetesExec(**exec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b2f14a81c02bbc4322b38259371fa6624c27f8399267e3fbd8d6d1383c420d)
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
            check_type(argname="argument cluster_ca_certificate", value=cluster_ca_certificate, expected_type=type_hints["cluster_ca_certificate"])
            check_type(argname="argument config_context", value=config_context, expected_type=type_hints["config_context"])
            check_type(argname="argument config_context_auth_info", value=config_context_auth_info, expected_type=type_hints["config_context_auth_info"])
            check_type(argname="argument config_context_cluster", value=config_context_cluster, expected_type=type_hints["config_context_cluster"])
            check_type(argname="argument config_path", value=config_path, expected_type=type_hints["config_path"])
            check_type(argname="argument config_paths", value=config_paths, expected_type=type_hints["config_paths"])
            check_type(argname="argument exec", value=exec, expected_type=type_hints["exec"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument proxy_url", value=proxy_url, expected_type=type_hints["proxy_url"])
            check_type(argname="argument tls_server_name", value=tls_server_name, expected_type=type_hints["tls_server_name"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_key is not None:
            self._values["client_key"] = client_key
        if cluster_ca_certificate is not None:
            self._values["cluster_ca_certificate"] = cluster_ca_certificate
        if config_context is not None:
            self._values["config_context"] = config_context
        if config_context_auth_info is not None:
            self._values["config_context_auth_info"] = config_context_auth_info
        if config_context_cluster is not None:
            self._values["config_context_cluster"] = config_context_cluster
        if config_path is not None:
            self._values["config_path"] = config_path
        if config_paths is not None:
            self._values["config_paths"] = config_paths
        if exec is not None:
            self._values["exec"] = exec
        if host is not None:
            self._values["host"] = host
        if insecure is not None:
            self._values["insecure"] = insecure
        if password is not None:
            self._values["password"] = password
        if proxy_url is not None:
            self._values["proxy_url"] = proxy_url
        if tls_server_name is not None:
            self._values["tls_server_name"] = tls_server_name
        if token is not None:
            self._values["token"] = token
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded client certificate for TLS authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#client_certificate HelmProvider#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded client certificate key for TLS authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#client_key HelmProvider#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_ca_certificate(self) -> typing.Optional[builtins.str]:
        '''PEM-encoded root certificates bundle for TLS authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#cluster_ca_certificate HelmProvider#cluster_ca_certificate}
        '''
        result = self._values.get("cluster_ca_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_context(self) -> typing.Optional[builtins.str]:
        '''Context to choose from the config file. Can be sourced from KUBE_CTX.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_context HelmProvider#config_context}
        '''
        result = self._values.get("config_context")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_context_auth_info(self) -> typing.Optional[builtins.str]:
        '''Authentication info context of the kube config (name of the kubeconfig user, --user flag in kubectl).

        Can be sourced from KUBE_CTX_AUTH_INFO.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_context_auth_info HelmProvider#config_context_auth_info}
        '''
        result = self._values.get("config_context_auth_info")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_context_cluster(self) -> typing.Optional[builtins.str]:
        '''Cluster context of the kube config (name of the kubeconfig cluster, --cluster flag in kubectl).

        Can be sourced from KUBE_CTX_CLUSTER.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_context_cluster HelmProvider#config_context_cluster}
        '''
        result = self._values.get("config_context_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_path(self) -> typing.Optional[builtins.str]:
        '''Path to the kube config file. Can be set with KUBE_CONFIG_PATH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_path HelmProvider#config_path}
        '''
        result = self._values.get("config_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of paths to kube config files. Can be set with KUBE_CONFIG_PATHS environment variable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#config_paths HelmProvider#config_paths}
        '''
        result = self._values.get("config_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exec(self) -> typing.Optional["HelmProviderKubernetesExec"]:
        '''Exec configuration for Kubernetes authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#exec HelmProvider#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["HelmProviderKubernetesExec"], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The hostname (in form of URI) of kubernetes master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#host HelmProvider#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether server should be accessed without verifying the TLS certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#insecure HelmProvider#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password to use for HTTP basic authentication when accessing the Kubernetes master endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#password HelmProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_url(self) -> typing.Optional[builtins.str]:
        '''URL to the proxy to be used for all API requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#proxy_url HelmProvider#proxy_url}
        '''
        result = self._values.get("proxy_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_server_name(self) -> typing.Optional[builtins.str]:
        '''Server name passed to the server for SNI and is used in the client to check server certificates against.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#tls_server_name HelmProvider#tls_server_name}
        '''
        result = self._values.get("tls_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Token to authenticate a service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#token HelmProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username to use for HTTP basic authentication when accessing the Kubernetes master endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#username HelmProvider#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmProviderKubernetes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.provider.HelmProviderKubernetesExec",
    jsii_struct_bases=[],
    name_mapping={
        "api_version": "apiVersion",
        "command": "command",
        "args": "args",
        "env": "env",
    },
)
class HelmProviderKubernetesExec:
    def __init__(
        self,
        *,
        api_version: builtins.str,
        command: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param api_version: API version for the exec plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#api_version HelmProvider#api_version}
        :param command: Command to run for Kubernetes exec plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#command HelmProvider#command}
        :param args: Arguments for the exec plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#args HelmProvider#args}
        :param env: Environment variables for the exec plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#env HelmProvider#env}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7e441f97cccff737d356dc06e6be332ad7fe161138eef9da0ab2873bfb11861)
            check_type(argname="argument api_version", value=api_version, expected_type=type_hints["api_version"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_version": api_version,
            "command": command,
        }
        if args is not None:
            self._values["args"] = args
        if env is not None:
            self._values["env"] = env

    @builtins.property
    def api_version(self) -> builtins.str:
        '''API version for the exec plugin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#api_version HelmProvider#api_version}
        '''
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def command(self) -> builtins.str:
        '''Command to run for Kubernetes exec plugin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#command HelmProvider#command}
        '''
        result = self._values.get("command")
        assert result is not None, "Required property 'command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments for the exec plugin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#args HelmProvider#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables for the exec plugin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#env HelmProvider#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmProviderKubernetesExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.provider.HelmProviderRegistries",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "url": "url", "username": "username"},
)
class HelmProviderRegistries:
    def __init__(
        self,
        *,
        password: builtins.str,
        url: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: The password to use for the OCI HTTP basic authentication when accessing the Kubernetes master endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#password HelmProvider#password}
        :param url: OCI URL in form of oci://host:port or oci://host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#url HelmProvider#url}
        :param username: The username to use for the OCI HTTP basic authentication when accessing the Kubernetes master endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#username HelmProvider#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f8bb7b61c6a46eb8a0a583fe21354ff3634a864fc57855fd80958f0d9cb5a3)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "url": url,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''The password to use for the OCI HTTP basic authentication when accessing the Kubernetes master endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#password HelmProvider#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''OCI URL in form of oci://host:port or oci://host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#url HelmProvider#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username to use for the OCI HTTP basic authentication when accessing the Kubernetes master endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs#username HelmProvider#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmProviderRegistries(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HelmProvider",
    "HelmProviderConfig",
    "HelmProviderExperiments",
    "HelmProviderKubernetes",
    "HelmProviderKubernetesExec",
    "HelmProviderRegistries",
]

publication.publish()

def _typecheckingstub__1a9b1d29236885254322c77ebb49db4debaa433e29b9dba83d7fbc53fe1d63a5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    burst_limit: typing.Optional[jsii.Number] = None,
    debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    experiments: typing.Optional[typing.Union[HelmProviderExperiments, typing.Dict[builtins.str, typing.Any]]] = None,
    helm_driver: typing.Optional[builtins.str] = None,
    kubernetes: typing.Optional[typing.Union[HelmProviderKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
    plugins_path: typing.Optional[builtins.str] = None,
    registries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HelmProviderRegistries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    registry_config_path: typing.Optional[builtins.str] = None,
    repository_cache: typing.Optional[builtins.str] = None,
    repository_config_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123313e4dc1c57c04c45cc3be5ca11f152571e1e497a6a13eb40e3508b4f840b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c8d100c082c1b44d45d308583d76102336ca6627dda5440b68f792ae7e709c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ea915f57f0846c46350065f633c6c7a90cc0ec878e1e157f9632ff3b34ee84(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71c4802c45cbb0d4e22f2e2c6527680fb1ae913859591829c2d2e73d49630a1(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7ca3f5c43d109af69ebe9986048dff1f4e81e5000f32ac493e073abe99b695(
    value: typing.Optional[HelmProviderExperiments],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2d5af5a79a70e391e6ed89e2fc09113460645ef53c14dc53450ddf7dee323b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3deb2b4dafca7e58ca548c00f93e2be543424dec0966dedfcee56e2d4bc42511(
    value: typing.Optional[HelmProviderKubernetes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757dd31649762ccdd94b64c3463943e1263ef6c177ca2d9574f8227cd996c2a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5168b9aec6e4a1d8cdfac3d78c746151491d6ca73ee21b19bffc0b1a0a3bd005(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HelmProviderRegistries]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fac8e2776395bbfffe943a14a74bf425a51cf8b29cd8b1167a6fa7d488cf373(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054c1253b2d4168585cad86a1c74df51ef8aa4949c8fb96911a43d680815098f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5ccc55fc9833150a2c2322e6b495be83cfed1ce99147b59db3438ee95c0d4b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf846e980a90ecff087864941949dc254940696c8e5d0be8d4bae4f0f4aa0a9(
    *,
    alias: typing.Optional[builtins.str] = None,
    burst_limit: typing.Optional[jsii.Number] = None,
    debug: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    experiments: typing.Optional[typing.Union[HelmProviderExperiments, typing.Dict[builtins.str, typing.Any]]] = None,
    helm_driver: typing.Optional[builtins.str] = None,
    kubernetes: typing.Optional[typing.Union[HelmProviderKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
    plugins_path: typing.Optional[builtins.str] = None,
    registries: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HelmProviderRegistries, typing.Dict[builtins.str, typing.Any]]]]] = None,
    registry_config_path: typing.Optional[builtins.str] = None,
    repository_cache: typing.Optional[builtins.str] = None,
    repository_config_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0975af09e993360c7b82d25c4fdbe476021cece87b3feb51429d13f8dac830(
    *,
    manifest: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b2f14a81c02bbc4322b38259371fa6624c27f8399267e3fbd8d6d1383c420d(
    *,
    client_certificate: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
    cluster_ca_certificate: typing.Optional[builtins.str] = None,
    config_context: typing.Optional[builtins.str] = None,
    config_context_auth_info: typing.Optional[builtins.str] = None,
    config_context_cluster: typing.Optional[builtins.str] = None,
    config_path: typing.Optional[builtins.str] = None,
    config_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    exec: typing.Optional[typing.Union[HelmProviderKubernetesExec, typing.Dict[builtins.str, typing.Any]]] = None,
    host: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    proxy_url: typing.Optional[builtins.str] = None,
    tls_server_name: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e441f97cccff737d356dc06e6be332ad7fe161138eef9da0ab2873bfb11861(
    *,
    api_version: builtins.str,
    command: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f8bb7b61c6a46eb8a0a583fe21354ff3634a864fc57855fd80958f0d9cb5a3(
    *,
    password: builtins.str,
    url: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
