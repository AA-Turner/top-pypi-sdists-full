r'''
# `helm_release`

Refer to the Terraform Registry for docs: [`helm_release`](https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release).
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


class Release(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.Release",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release helm_release}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        chart: builtins.str,
        name: builtins.str,
        atomic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cleanup_on_fail: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_namespace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dependency_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        devel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_crd_hooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_openapi_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_webhooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keyring: typing.Optional[builtins.str] = None,
        lint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_history: typing.Optional[jsii.Number] = None,
        namespace: typing.Optional[builtins.str] = None,
        pass_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        postrender: typing.Optional[typing.Union["ReleasePostrender", typing.Dict[builtins.str, typing.Any]]] = None,
        recreate_pods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        render_subchart_notes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_ca_file: typing.Optional[builtins.str] = None,
        repository_cert_file: typing.Optional[builtins.str] = None,
        repository_key_file: typing.Optional[builtins.str] = None,
        repository_password: typing.Optional[builtins.str] = None,
        repository_username: typing.Optional[builtins.str] = None,
        reset_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reuse_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_sensitive: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetSensitive", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_wo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetWo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_wo_revision: typing.Optional[jsii.Number] = None,
        skip_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version: typing.Optional[builtins.str] = None,
        wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wait_for_jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release helm_release} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param chart: Chart name to be installed. A path may be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#chart Release#chart}
        :param name: Release name. The length must not be longer than 53 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}
        :param atomic: If set, installation process purges chart on fail. The wait flag will be set automatically if atomic is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#atomic Release#atomic}
        :param cleanup_on_fail: Allow deletion of new resources created in this upgrade when upgrade fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#cleanup_on_fail Release#cleanup_on_fail}
        :param create_namespace: Create the namespace if it does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#create_namespace Release#create_namespace}
        :param dependency_update: Run helm dependency update before installing the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#dependency_update Release#dependency_update}
        :param description: Add a custom description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#description Release#description}
        :param devel: Use chart development versions, too. Equivalent to version '>0.0.0-0'. If 'version' is set, this is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#devel Release#devel}
        :param disable_crd_hooks: Prevent CRD hooks from running, but run other hooks. See helm install --no-crd-hook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_crd_hooks Release#disable_crd_hooks}
        :param disable_openapi_validation: If set, the installation process will not validate rendered templates against the Kubernetes OpenAPI Schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_openapi_validation Release#disable_openapi_validation}
        :param disable_webhooks: Prevent hooks from running. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_webhooks Release#disable_webhooks}
        :param force_update: Force resource update through delete/recreate if needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#force_update Release#force_update}
        :param keyring: Location of public keys used for verification, Used only if 'verify is true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#keyring Release#keyring}
        :param lint: Run helm lint when planning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#lint Release#lint}
        :param max_history: Limit the maximum number of revisions saved per release. Use 0 for no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#max_history Release#max_history}
        :param namespace: Namespace to install the release into. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#namespace Release#namespace}
        :param pass_credentials: Pass credentials to all domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#pass_credentials Release#pass_credentials}
        :param postrender: Postrender command config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#postrender Release#postrender}
        :param recreate_pods: Perform pods restart during upgrade/rollback. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#recreate_pods Release#recreate_pods}
        :param render_subchart_notes: If set, render subchart notes along with the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#render_subchart_notes Release#render_subchart_notes}
        :param replace: Re-use the given name, even if that name is already used. This is unsafe in production. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#replace Release#replace}
        :param repository: Repository where to locate the requested chart. If it is a URL, the chart is installed without installing the repository Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository Release#repository}
        :param repository_ca_file: The Repositories CA file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_ca_file Release#repository_ca_file}
        :param repository_cert_file: The repositories cert file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_cert_file Release#repository_cert_file}
        :param repository_key_file: The repositories cert key file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_key_file Release#repository_key_file}
        :param repository_password: Password for HTTP basic authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_password Release#repository_password}
        :param repository_username: Username for HTTP basic authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_username Release#repository_username}
        :param reset_values: When upgrading, reset the values to the ones built into the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#reset_values Release#reset_values}
        :param reuse_values: When upgrading, reuse the last release's values and merge in any overrides. If 'reset_values' is specified, this is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#reuse_values Release#reuse_values}
        :param set: Custom values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set Release#set}
        :param set_list: Custom sensitive values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_list Release#set_list}
        :param set_sensitive: Custom sensitive values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_sensitive Release#set_sensitive}
        :param set_wo: Custom values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_wo Release#set_wo}
        :param set_wo_revision: The current revision of the write-only "set_wo" attribute. Incrementing this integer value will cause Terraform to update the write-only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_wo_revision Release#set_wo_revision}
        :param skip_crds: If set, no CRDs will be installed. By default, CRDs are installed if not already present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#skip_crds Release#skip_crds}
        :param timeout: Time in seconds to wait for any individual kubernetes operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#timeout Release#timeout}
        :param values: List of values in raw YAML format to pass to helm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#values Release#values}
        :param verify: Verify the package before installing it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#verify Release#verify}
        :param version: Specify the exact chart version to install. If this is not specified, the latest version is installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#version Release#version}
        :param wait: Will wait until all resources are in a ready state before marking the release as successful. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#wait Release#wait}
        :param wait_for_jobs: If wait is enabled, will wait until all Jobs have been completed before marking the release as successful. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#wait_for_jobs Release#wait_for_jobs}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc75acd85229e479b8b9aa92aa7d1b843987201bf6028137a9a9eb6a0d093d27)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ReleaseConfig(
            chart=chart,
            name=name,
            atomic=atomic,
            cleanup_on_fail=cleanup_on_fail,
            create_namespace=create_namespace,
            dependency_update=dependency_update,
            description=description,
            devel=devel,
            disable_crd_hooks=disable_crd_hooks,
            disable_openapi_validation=disable_openapi_validation,
            disable_webhooks=disable_webhooks,
            force_update=force_update,
            keyring=keyring,
            lint=lint,
            max_history=max_history,
            namespace=namespace,
            pass_credentials=pass_credentials,
            postrender=postrender,
            recreate_pods=recreate_pods,
            render_subchart_notes=render_subchart_notes,
            replace=replace,
            repository=repository,
            repository_ca_file=repository_ca_file,
            repository_cert_file=repository_cert_file,
            repository_key_file=repository_key_file,
            repository_password=repository_password,
            repository_username=repository_username,
            reset_values=reset_values,
            reuse_values=reuse_values,
            set=set,
            set_list=set_list,
            set_sensitive=set_sensitive,
            set_wo=set_wo,
            set_wo_revision=set_wo_revision,
            skip_crds=skip_crds,
            timeout=timeout,
            values=values,
            verify=verify,
            version=version,
            wait=wait,
            wait_for_jobs=wait_for_jobs,
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
        '''Generates CDKTF code for importing a Release resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Release to import.
        :param import_from_id: The id of the existing Release that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Release to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f22d9bf92f2c37284b57419397b6b7c21cc71a65d75a31f11cddcec3bea801)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPostrender")
    def put_postrender(
        self,
        *,
        binary_path: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param binary_path: The common binary path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#binary_path Release#binary_path}
        :param args: An argument to the post-renderer (can specify multiple). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#args Release#args}
        '''
        value = ReleasePostrender(binary_path=binary_path, args=args)

        return typing.cast(None, jsii.invoke(self, "putPostrender", [value]))

    @jsii.member(jsii_name="putSet")
    def put_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b72a3657c0803010731fa3fd2044a0f404b98ac9399b1fb916895c0de83919d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSet", [value]))

    @jsii.member(jsii_name="putSetList")
    def put_set_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e66f987c47878d4a6946a5a1dc06f0d9f1ca6ba2ae98348676c4bd5950c185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetList", [value]))

    @jsii.member(jsii_name="putSetSensitive")
    def put_set_sensitive(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetSensitive", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf9382a783d49a3885b1e5db3d0b63f63fc7a33b8cdeefbeace8a470ca85b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetSensitive", [value]))

    @jsii.member(jsii_name="putSetWo")
    def put_set_wo(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetWo", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348d8f84de46e2c85afa109d2e4e18ebe58dbf6a5a00304197583870aeba301d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetWo", [value]))

    @jsii.member(jsii_name="resetAtomic")
    def reset_atomic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAtomic", []))

    @jsii.member(jsii_name="resetCleanupOnFail")
    def reset_cleanup_on_fail(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCleanupOnFail", []))

    @jsii.member(jsii_name="resetCreateNamespace")
    def reset_create_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateNamespace", []))

    @jsii.member(jsii_name="resetDependencyUpdate")
    def reset_dependency_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependencyUpdate", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDevel")
    def reset_devel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDevel", []))

    @jsii.member(jsii_name="resetDisableCrdHooks")
    def reset_disable_crd_hooks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableCrdHooks", []))

    @jsii.member(jsii_name="resetDisableOpenapiValidation")
    def reset_disable_openapi_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableOpenapiValidation", []))

    @jsii.member(jsii_name="resetDisableWebhooks")
    def reset_disable_webhooks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableWebhooks", []))

    @jsii.member(jsii_name="resetForceUpdate")
    def reset_force_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdate", []))

    @jsii.member(jsii_name="resetKeyring")
    def reset_keyring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyring", []))

    @jsii.member(jsii_name="resetLint")
    def reset_lint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLint", []))

    @jsii.member(jsii_name="resetMaxHistory")
    def reset_max_history(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxHistory", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetPassCredentials")
    def reset_pass_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassCredentials", []))

    @jsii.member(jsii_name="resetPostrender")
    def reset_postrender(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostrender", []))

    @jsii.member(jsii_name="resetRecreatePods")
    def reset_recreate_pods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecreatePods", []))

    @jsii.member(jsii_name="resetRenderSubchartNotes")
    def reset_render_subchart_notes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenderSubchartNotes", []))

    @jsii.member(jsii_name="resetReplace")
    def reset_replace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplace", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @jsii.member(jsii_name="resetRepositoryCaFile")
    def reset_repository_ca_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryCaFile", []))

    @jsii.member(jsii_name="resetRepositoryCertFile")
    def reset_repository_cert_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryCertFile", []))

    @jsii.member(jsii_name="resetRepositoryKeyFile")
    def reset_repository_key_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryKeyFile", []))

    @jsii.member(jsii_name="resetRepositoryPassword")
    def reset_repository_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryPassword", []))

    @jsii.member(jsii_name="resetRepositoryUsername")
    def reset_repository_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepositoryUsername", []))

    @jsii.member(jsii_name="resetResetValues")
    def reset_reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResetValues", []))

    @jsii.member(jsii_name="resetReuseValues")
    def reset_reuse_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReuseValues", []))

    @jsii.member(jsii_name="resetSet")
    def reset_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSet", []))

    @jsii.member(jsii_name="resetSetList")
    def reset_set_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetList", []))

    @jsii.member(jsii_name="resetSetSensitive")
    def reset_set_sensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetSensitive", []))

    @jsii.member(jsii_name="resetSetWo")
    def reset_set_wo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetWo", []))

    @jsii.member(jsii_name="resetSetWoRevision")
    def reset_set_wo_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetWoRevision", []))

    @jsii.member(jsii_name="resetSkipCrds")
    def reset_skip_crds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipCrds", []))

    @jsii.member(jsii_name="resetTfValues")
    def reset_tf_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTfValues", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetVerify")
    def reset_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerify", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetWait")
    def reset_wait(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWait", []))

    @jsii.member(jsii_name="resetWaitForJobs")
    def reset_wait_for_jobs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWaitForJobs", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manifest"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "ReleaseMetadataOutputReference":
        return typing.cast("ReleaseMetadataOutputReference", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="postrender")
    def postrender(self) -> "ReleasePostrenderOutputReference":
        return typing.cast("ReleasePostrenderOutputReference", jsii.get(self, "postrender"))

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> "ReleaseSetList":
        return typing.cast("ReleaseSetList", jsii.get(self, "set"))

    @builtins.property
    @jsii.member(jsii_name="setList")
    def set_list(self) -> "ReleaseSetListStructList":
        return typing.cast("ReleaseSetListStructList", jsii.get(self, "setList"))

    @builtins.property
    @jsii.member(jsii_name="setSensitive")
    def set_sensitive(self) -> "ReleaseSetSensitiveList":
        return typing.cast("ReleaseSetSensitiveList", jsii.get(self, "setSensitive"))

    @builtins.property
    @jsii.member(jsii_name="setWo")
    def set_wo(self) -> "ReleaseSetWoList":
        return typing.cast("ReleaseSetWoList", jsii.get(self, "setWo"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="atomicInput")
    def atomic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "atomicInput"))

    @builtins.property
    @jsii.member(jsii_name="chartInput")
    def chart_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chartInput"))

    @builtins.property
    @jsii.member(jsii_name="cleanupOnFailInput")
    def cleanup_on_fail_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cleanupOnFailInput"))

    @builtins.property
    @jsii.member(jsii_name="createNamespaceInput")
    def create_namespace_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "createNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="dependencyUpdateInput")
    def dependency_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dependencyUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="develInput")
    def devel_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "develInput"))

    @builtins.property
    @jsii.member(jsii_name="disableCrdHooksInput")
    def disable_crd_hooks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableCrdHooksInput"))

    @builtins.property
    @jsii.member(jsii_name="disableOpenapiValidationInput")
    def disable_openapi_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableOpenapiValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="disableWebhooksInput")
    def disable_webhooks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableWebhooksInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateInput")
    def force_update_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="keyringInput")
    def keyring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyringInput"))

    @builtins.property
    @jsii.member(jsii_name="lintInput")
    def lint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lintInput"))

    @builtins.property
    @jsii.member(jsii_name="maxHistoryInput")
    def max_history_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxHistoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="passCredentialsInput")
    def pass_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="postrenderInput")
    def postrender_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ReleasePostrender"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ReleasePostrender"]], jsii.get(self, "postrenderInput"))

    @builtins.property
    @jsii.member(jsii_name="recreatePodsInput")
    def recreate_pods_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recreatePodsInput"))

    @builtins.property
    @jsii.member(jsii_name="renderSubchartNotesInput")
    def render_subchart_notes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "renderSubchartNotesInput"))

    @builtins.property
    @jsii.member(jsii_name="replaceInput")
    def replace_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "replaceInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCaFileInput")
    def repository_ca_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryCaFileInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCertFileInput")
    def repository_cert_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryCertFileInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryKeyFileInput")
    def repository_key_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryKeyFileInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryPasswordInput")
    def repository_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUsernameInput")
    def repository_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="resetValuesInput")
    def reset_values_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resetValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="reuseValuesInput")
    def reuse_values_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "reuseValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="setInput")
    def set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSet"]]], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="setListInput")
    def set_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetListStruct"]]], jsii.get(self, "setListInput"))

    @builtins.property
    @jsii.member(jsii_name="setSensitiveInput")
    def set_sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetSensitive"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetSensitive"]]], jsii.get(self, "setSensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="setWoInput")
    def set_wo_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetWo"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetWo"]]], jsii.get(self, "setWoInput"))

    @builtins.property
    @jsii.member(jsii_name="setWoRevisionInput")
    def set_wo_revision_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "setWoRevisionInput"))

    @builtins.property
    @jsii.member(jsii_name="skipCrdsInput")
    def skip_crds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipCrdsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyInput")
    def verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="waitForJobsInput")
    def wait_for_jobs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitForJobsInput"))

    @builtins.property
    @jsii.member(jsii_name="waitInput")
    def wait_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitInput"))

    @builtins.property
    @jsii.member(jsii_name="atomic")
    def atomic(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "atomic"))

    @atomic.setter
    def atomic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64d1ea2d4d5c0481d8d2a15fc4f143dbdef8ab41305fc11564450cdd45168cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "atomic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="chart")
    def chart(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chart"))

    @chart.setter
    def chart(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0972b5f344751dc09888b8fdf49f426ba74bd115c7bf939efa8cbe108094db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cleanupOnFail")
    def cleanup_on_fail(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cleanupOnFail"))

    @cleanup_on_fail.setter
    def cleanup_on_fail(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37497fd707dd6ad0c6a6b1755e1b65b9bd4e1643e80194841b30de8d7a541719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cleanupOnFail", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createNamespace")
    def create_namespace(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "createNamespace"))

    @create_namespace.setter
    def create_namespace(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70664fb2b60e53eb7984a10c7d4873f03dffacaabb5371072f7c932f815a879d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependencyUpdate")
    def dependency_update(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dependencyUpdate"))

    @dependency_update.setter
    def dependency_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8726af0cd133ebc83278398bf17a00684cc7ea549abcb2ed489b0dbcd1a73c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencyUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33f630af84ebed1c38b5556ab929098c5840644dd12764b1d0dbbad9b1faa86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="devel")
    def devel(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "devel"))

    @devel.setter
    def devel(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4925d70a12400e378464de8adcf097b32a6e7fa55547ae56a3854209a257d2d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "devel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableCrdHooks")
    def disable_crd_hooks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableCrdHooks"))

    @disable_crd_hooks.setter
    def disable_crd_hooks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ca50f8b4a144c892fda160eb884e1df188a56ea06d633bf07b7afe253241f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableCrdHooks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableOpenapiValidation")
    def disable_openapi_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableOpenapiValidation"))

    @disable_openapi_validation.setter
    def disable_openapi_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874ec0e11ad9c3c0b6720eef0a1356730e45f1a4565dc52f009d468321bf62f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableOpenapiValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableWebhooks")
    def disable_webhooks(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableWebhooks"))

    @disable_webhooks.setter
    def disable_webhooks(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd480ec846441f10de7b93fcd878789f6a39b3f26f9557124d682352fb6018d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableWebhooks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forceUpdate")
    def force_update(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceUpdate"))

    @force_update.setter
    def force_update(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00fb4fd9f947ec509a72ea5df207806c78db1f0bdb4dc5dfb98bb4e165fa124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyring")
    def keyring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyring"))

    @keyring.setter
    def keyring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72e97527302e9450ca9ddb8351f9162f113637b872335b5f5a384e5d83cb02c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lint")
    def lint(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lint"))

    @lint.setter
    def lint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebefd20b5ab48275a464a8c7c78ace5dc7303737eda6dd1173d2b87d766c9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxHistory")
    def max_history(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxHistory"))

    @max_history.setter
    def max_history(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396f4fa6654a36f4b029f0fdfbac7cb17d59c5a4277e02067a0a4572080552e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxHistory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f78192da9ffa2588128021bab8cc62b4c1885e04a30d156da8e1bc52909d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce927be764a91bed32dd47e6d200dba849f59c938d25042eed1a254535ea77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passCredentials")
    def pass_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passCredentials"))

    @pass_credentials.setter
    def pass_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defb85457399fa43643f8b85054001f91ef22c1b085e80338f181a1f8bf71330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recreatePods")
    def recreate_pods(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recreatePods"))

    @recreate_pods.setter
    def recreate_pods(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8021737dc70fde376fd307eeeceff08eb6e262c5ef095a79cee8538f3f022ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recreatePods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="renderSubchartNotes")
    def render_subchart_notes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "renderSubchartNotes"))

    @render_subchart_notes.setter
    def render_subchart_notes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda9ecf3c5d8298fa6866e24c3d45ffea7dfaff11f106c7b04985a73e8c43731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renderSubchartNotes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replace")
    def replace(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "replace"))

    @replace.setter
    def replace(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810f8f0f875cba91fd2f30bebdfd606318cee23d858b63c8fa3e3572398c5b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5aeeefc17c0b60ea0f1040c237b6816524f29703deee6f467d4d92fb49d420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryCaFile")
    def repository_ca_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryCaFile"))

    @repository_ca_file.setter
    def repository_ca_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b5e4e0f62cc6e9d49340203075836922bfbeec046ef951937bd70320abfcc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCaFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryCertFile")
    def repository_cert_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryCertFile"))

    @repository_cert_file.setter
    def repository_cert_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0253e86727e3dda147544d73591ec9c7dfefc63f9b5b28ded78fe0879f7ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCertFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryKeyFile")
    def repository_key_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryKeyFile"))

    @repository_key_file.setter
    def repository_key_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621352acc4776b44aea7e43dede99a4bf3c1153e4dff66d1545066db21be2d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryKeyFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryPassword")
    def repository_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryPassword"))

    @repository_password.setter
    def repository_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050722a21ec7404de1dce14e6868df429d8007b2ead81a4f565050beef5bc14b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryUsername")
    def repository_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUsername"))

    @repository_username.setter
    def repository_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bc40d9b0c867608d404c07c13d4b3154594bcd91558c32c6f828b45adade26b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "resetValues"))

    @reset_values.setter
    def reset_values(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45878404436c4d09b10a954b5f6f79b67a5322f943e28be2fe3c88100471583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resetValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reuseValues")
    def reuse_values(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "reuseValues"))

    @reuse_values.setter
    def reuse_values(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39bdd2d1d76a4eaa3b8bcdc62bb294e13642ab521d59e8683a345c63eb355b5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reuseValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="setWoRevision")
    def set_wo_revision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "setWoRevision"))

    @set_wo_revision.setter
    def set_wo_revision(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126382aa9f62f1a4a6eb6642cd56021452a3570e6b4c218b63f16f2227b48418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setWoRevision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipCrds")
    def skip_crds(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipCrds"))

    @skip_crds.setter
    def skip_crds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842028bb5398dae0afe025b331cfac2e399e0b3392a25e154a8b45e9e6df62fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipCrds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce093763d1e99d1031c3d9f244d12dc614bf528e5ba752c43ccca3d29d96f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b719961948e4ed89dbc8e48b7a1d51792f716cf2c6bb00bfb266a656d6df5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verify")
    def verify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verify"))

    @verify.setter
    def verify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa71240bc0a569257fd1df4bab30e3ee9907b3ff14b999b808d7a535753138c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ae21aa002d2702ab16a4877ff2a5d7a6d5f14e9f1b917eecaff9ede140825a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wait")
    def wait(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wait"))

    @wait.setter
    def wait(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b25640d7d4e45b12467e1045d8c98a166002706634010cbce3351fc1f680e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="waitForJobs")
    def wait_for_jobs(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "waitForJobs"))

    @wait_for_jobs.setter
    def wait_for_jobs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5926058acef0ca2b7e353de193a9045b7d1dce153706e704e0078f7103f20a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "waitForJobs", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.release.ReleaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "chart": "chart",
        "name": "name",
        "atomic": "atomic",
        "cleanup_on_fail": "cleanupOnFail",
        "create_namespace": "createNamespace",
        "dependency_update": "dependencyUpdate",
        "description": "description",
        "devel": "devel",
        "disable_crd_hooks": "disableCrdHooks",
        "disable_openapi_validation": "disableOpenapiValidation",
        "disable_webhooks": "disableWebhooks",
        "force_update": "forceUpdate",
        "keyring": "keyring",
        "lint": "lint",
        "max_history": "maxHistory",
        "namespace": "namespace",
        "pass_credentials": "passCredentials",
        "postrender": "postrender",
        "recreate_pods": "recreatePods",
        "render_subchart_notes": "renderSubchartNotes",
        "replace": "replace",
        "repository": "repository",
        "repository_ca_file": "repositoryCaFile",
        "repository_cert_file": "repositoryCertFile",
        "repository_key_file": "repositoryKeyFile",
        "repository_password": "repositoryPassword",
        "repository_username": "repositoryUsername",
        "reset_values": "resetValues",
        "reuse_values": "reuseValues",
        "set": "set",
        "set_list": "setList",
        "set_sensitive": "setSensitive",
        "set_wo": "setWo",
        "set_wo_revision": "setWoRevision",
        "skip_crds": "skipCrds",
        "timeout": "timeout",
        "values": "values",
        "verify": "verify",
        "version": "version",
        "wait": "wait",
        "wait_for_jobs": "waitForJobs",
    },
)
class ReleaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        chart: builtins.str,
        name: builtins.str,
        atomic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cleanup_on_fail: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_namespace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dependency_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        devel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_crd_hooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_openapi_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_webhooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        force_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keyring: typing.Optional[builtins.str] = None,
        lint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_history: typing.Optional[jsii.Number] = None,
        namespace: typing.Optional[builtins.str] = None,
        pass_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        postrender: typing.Optional[typing.Union["ReleasePostrender", typing.Dict[builtins.str, typing.Any]]] = None,
        recreate_pods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        render_subchart_notes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        repository: typing.Optional[builtins.str] = None,
        repository_ca_file: typing.Optional[builtins.str] = None,
        repository_cert_file: typing.Optional[builtins.str] = None,
        repository_key_file: typing.Optional[builtins.str] = None,
        repository_password: typing.Optional[builtins.str] = None,
        repository_username: typing.Optional[builtins.str] = None,
        reset_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reuse_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_sensitive: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetSensitive", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_wo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ReleaseSetWo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_wo_revision: typing.Optional[jsii.Number] = None,
        skip_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version: typing.Optional[builtins.str] = None,
        wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        wait_for_jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param chart: Chart name to be installed. A path may be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#chart Release#chart}
        :param name: Release name. The length must not be longer than 53 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}
        :param atomic: If set, installation process purges chart on fail. The wait flag will be set automatically if atomic is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#atomic Release#atomic}
        :param cleanup_on_fail: Allow deletion of new resources created in this upgrade when upgrade fails. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#cleanup_on_fail Release#cleanup_on_fail}
        :param create_namespace: Create the namespace if it does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#create_namespace Release#create_namespace}
        :param dependency_update: Run helm dependency update before installing the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#dependency_update Release#dependency_update}
        :param description: Add a custom description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#description Release#description}
        :param devel: Use chart development versions, too. Equivalent to version '>0.0.0-0'. If 'version' is set, this is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#devel Release#devel}
        :param disable_crd_hooks: Prevent CRD hooks from running, but run other hooks. See helm install --no-crd-hook. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_crd_hooks Release#disable_crd_hooks}
        :param disable_openapi_validation: If set, the installation process will not validate rendered templates against the Kubernetes OpenAPI Schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_openapi_validation Release#disable_openapi_validation}
        :param disable_webhooks: Prevent hooks from running. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_webhooks Release#disable_webhooks}
        :param force_update: Force resource update through delete/recreate if needed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#force_update Release#force_update}
        :param keyring: Location of public keys used for verification, Used only if 'verify is true'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#keyring Release#keyring}
        :param lint: Run helm lint when planning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#lint Release#lint}
        :param max_history: Limit the maximum number of revisions saved per release. Use 0 for no limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#max_history Release#max_history}
        :param namespace: Namespace to install the release into. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#namespace Release#namespace}
        :param pass_credentials: Pass credentials to all domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#pass_credentials Release#pass_credentials}
        :param postrender: Postrender command config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#postrender Release#postrender}
        :param recreate_pods: Perform pods restart during upgrade/rollback. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#recreate_pods Release#recreate_pods}
        :param render_subchart_notes: If set, render subchart notes along with the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#render_subchart_notes Release#render_subchart_notes}
        :param replace: Re-use the given name, even if that name is already used. This is unsafe in production. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#replace Release#replace}
        :param repository: Repository where to locate the requested chart. If it is a URL, the chart is installed without installing the repository Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository Release#repository}
        :param repository_ca_file: The Repositories CA file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_ca_file Release#repository_ca_file}
        :param repository_cert_file: The repositories cert file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_cert_file Release#repository_cert_file}
        :param repository_key_file: The repositories cert key file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_key_file Release#repository_key_file}
        :param repository_password: Password for HTTP basic authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_password Release#repository_password}
        :param repository_username: Username for HTTP basic authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_username Release#repository_username}
        :param reset_values: When upgrading, reset the values to the ones built into the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#reset_values Release#reset_values}
        :param reuse_values: When upgrading, reuse the last release's values and merge in any overrides. If 'reset_values' is specified, this is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#reuse_values Release#reuse_values}
        :param set: Custom values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set Release#set}
        :param set_list: Custom sensitive values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_list Release#set_list}
        :param set_sensitive: Custom sensitive values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_sensitive Release#set_sensitive}
        :param set_wo: Custom values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_wo Release#set_wo}
        :param set_wo_revision: The current revision of the write-only "set_wo" attribute. Incrementing this integer value will cause Terraform to update the write-only value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_wo_revision Release#set_wo_revision}
        :param skip_crds: If set, no CRDs will be installed. By default, CRDs are installed if not already present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#skip_crds Release#skip_crds}
        :param timeout: Time in seconds to wait for any individual kubernetes operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#timeout Release#timeout}
        :param values: List of values in raw YAML format to pass to helm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#values Release#values}
        :param verify: Verify the package before installing it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#verify Release#verify}
        :param version: Specify the exact chart version to install. If this is not specified, the latest version is installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#version Release#version}
        :param wait: Will wait until all resources are in a ready state before marking the release as successful. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#wait Release#wait}
        :param wait_for_jobs: If wait is enabled, will wait until all Jobs have been completed before marking the release as successful. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#wait_for_jobs Release#wait_for_jobs}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(postrender, dict):
            postrender = ReleasePostrender(**postrender)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3351956da04ddf8ca86567e1dd64c43a3a02b9b30bc17a13da12597bc326e840)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument chart", value=chart, expected_type=type_hints["chart"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument atomic", value=atomic, expected_type=type_hints["atomic"])
            check_type(argname="argument cleanup_on_fail", value=cleanup_on_fail, expected_type=type_hints["cleanup_on_fail"])
            check_type(argname="argument create_namespace", value=create_namespace, expected_type=type_hints["create_namespace"])
            check_type(argname="argument dependency_update", value=dependency_update, expected_type=type_hints["dependency_update"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument devel", value=devel, expected_type=type_hints["devel"])
            check_type(argname="argument disable_crd_hooks", value=disable_crd_hooks, expected_type=type_hints["disable_crd_hooks"])
            check_type(argname="argument disable_openapi_validation", value=disable_openapi_validation, expected_type=type_hints["disable_openapi_validation"])
            check_type(argname="argument disable_webhooks", value=disable_webhooks, expected_type=type_hints["disable_webhooks"])
            check_type(argname="argument force_update", value=force_update, expected_type=type_hints["force_update"])
            check_type(argname="argument keyring", value=keyring, expected_type=type_hints["keyring"])
            check_type(argname="argument lint", value=lint, expected_type=type_hints["lint"])
            check_type(argname="argument max_history", value=max_history, expected_type=type_hints["max_history"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument pass_credentials", value=pass_credentials, expected_type=type_hints["pass_credentials"])
            check_type(argname="argument postrender", value=postrender, expected_type=type_hints["postrender"])
            check_type(argname="argument recreate_pods", value=recreate_pods, expected_type=type_hints["recreate_pods"])
            check_type(argname="argument render_subchart_notes", value=render_subchart_notes, expected_type=type_hints["render_subchart_notes"])
            check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_ca_file", value=repository_ca_file, expected_type=type_hints["repository_ca_file"])
            check_type(argname="argument repository_cert_file", value=repository_cert_file, expected_type=type_hints["repository_cert_file"])
            check_type(argname="argument repository_key_file", value=repository_key_file, expected_type=type_hints["repository_key_file"])
            check_type(argname="argument repository_password", value=repository_password, expected_type=type_hints["repository_password"])
            check_type(argname="argument repository_username", value=repository_username, expected_type=type_hints["repository_username"])
            check_type(argname="argument reset_values", value=reset_values, expected_type=type_hints["reset_values"])
            check_type(argname="argument reuse_values", value=reuse_values, expected_type=type_hints["reuse_values"])
            check_type(argname="argument set", value=set, expected_type=type_hints["set"])
            check_type(argname="argument set_list", value=set_list, expected_type=type_hints["set_list"])
            check_type(argname="argument set_sensitive", value=set_sensitive, expected_type=type_hints["set_sensitive"])
            check_type(argname="argument set_wo", value=set_wo, expected_type=type_hints["set_wo"])
            check_type(argname="argument set_wo_revision", value=set_wo_revision, expected_type=type_hints["set_wo_revision"])
            check_type(argname="argument skip_crds", value=skip_crds, expected_type=type_hints["skip_crds"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument verify", value=verify, expected_type=type_hints["verify"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument wait", value=wait, expected_type=type_hints["wait"])
            check_type(argname="argument wait_for_jobs", value=wait_for_jobs, expected_type=type_hints["wait_for_jobs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "chart": chart,
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
        if atomic is not None:
            self._values["atomic"] = atomic
        if cleanup_on_fail is not None:
            self._values["cleanup_on_fail"] = cleanup_on_fail
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if dependency_update is not None:
            self._values["dependency_update"] = dependency_update
        if description is not None:
            self._values["description"] = description
        if devel is not None:
            self._values["devel"] = devel
        if disable_crd_hooks is not None:
            self._values["disable_crd_hooks"] = disable_crd_hooks
        if disable_openapi_validation is not None:
            self._values["disable_openapi_validation"] = disable_openapi_validation
        if disable_webhooks is not None:
            self._values["disable_webhooks"] = disable_webhooks
        if force_update is not None:
            self._values["force_update"] = force_update
        if keyring is not None:
            self._values["keyring"] = keyring
        if lint is not None:
            self._values["lint"] = lint
        if max_history is not None:
            self._values["max_history"] = max_history
        if namespace is not None:
            self._values["namespace"] = namespace
        if pass_credentials is not None:
            self._values["pass_credentials"] = pass_credentials
        if postrender is not None:
            self._values["postrender"] = postrender
        if recreate_pods is not None:
            self._values["recreate_pods"] = recreate_pods
        if render_subchart_notes is not None:
            self._values["render_subchart_notes"] = render_subchart_notes
        if replace is not None:
            self._values["replace"] = replace
        if repository is not None:
            self._values["repository"] = repository
        if repository_ca_file is not None:
            self._values["repository_ca_file"] = repository_ca_file
        if repository_cert_file is not None:
            self._values["repository_cert_file"] = repository_cert_file
        if repository_key_file is not None:
            self._values["repository_key_file"] = repository_key_file
        if repository_password is not None:
            self._values["repository_password"] = repository_password
        if repository_username is not None:
            self._values["repository_username"] = repository_username
        if reset_values is not None:
            self._values["reset_values"] = reset_values
        if reuse_values is not None:
            self._values["reuse_values"] = reuse_values
        if set is not None:
            self._values["set"] = set
        if set_list is not None:
            self._values["set_list"] = set_list
        if set_sensitive is not None:
            self._values["set_sensitive"] = set_sensitive
        if set_wo is not None:
            self._values["set_wo"] = set_wo
        if set_wo_revision is not None:
            self._values["set_wo_revision"] = set_wo_revision
        if skip_crds is not None:
            self._values["skip_crds"] = skip_crds
        if timeout is not None:
            self._values["timeout"] = timeout
        if values is not None:
            self._values["values"] = values
        if verify is not None:
            self._values["verify"] = verify
        if version is not None:
            self._values["version"] = version
        if wait is not None:
            self._values["wait"] = wait
        if wait_for_jobs is not None:
            self._values["wait_for_jobs"] = wait_for_jobs

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
    def chart(self) -> builtins.str:
        '''Chart name to be installed. A path may be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#chart Release#chart}
        '''
        result = self._values.get("chart")
        assert result is not None, "Required property 'chart' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Release name. The length must not be longer than 53 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def atomic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, installation process purges chart on fail. The wait flag will be set automatically if atomic is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#atomic Release#atomic}
        '''
        result = self._values.get("atomic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cleanup_on_fail(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow deletion of new resources created in this upgrade when upgrade fails.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#cleanup_on_fail Release#cleanup_on_fail}
        '''
        result = self._values.get("cleanup_on_fail")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_namespace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Create the namespace if it does not exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#create_namespace Release#create_namespace}
        '''
        result = self._values.get("create_namespace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dependency_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Run helm dependency update before installing the chart.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#dependency_update Release#dependency_update}
        '''
        result = self._values.get("dependency_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Add a custom description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#description Release#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def devel(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use chart development versions, too. Equivalent to version '>0.0.0-0'. If 'version' is set, this is ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#devel Release#devel}
        '''
        result = self._values.get("devel")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_crd_hooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent CRD hooks from running, but run other hooks. See helm install --no-crd-hook.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_crd_hooks Release#disable_crd_hooks}
        '''
        result = self._values.get("disable_crd_hooks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_openapi_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, the installation process will not validate rendered templates against the Kubernetes OpenAPI Schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_openapi_validation Release#disable_openapi_validation}
        '''
        result = self._values.get("disable_openapi_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_webhooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent hooks from running.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#disable_webhooks Release#disable_webhooks}
        '''
        result = self._values.get("disable_webhooks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def force_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force resource update through delete/recreate if needed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#force_update Release#force_update}
        '''
        result = self._values.get("force_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def keyring(self) -> typing.Optional[builtins.str]:
        '''Location of public keys used for verification, Used only if 'verify is true'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#keyring Release#keyring}
        '''
        result = self._values.get("keyring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Run helm lint when planning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#lint Release#lint}
        '''
        result = self._values.get("lint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_history(self) -> typing.Optional[jsii.Number]:
        '''Limit the maximum number of revisions saved per release. Use 0 for no limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#max_history Release#max_history}
        '''
        result = self._values.get("max_history")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace to install the release into.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#namespace Release#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pass_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Pass credentials to all domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#pass_credentials Release#pass_credentials}
        '''
        result = self._values.get("pass_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def postrender(self) -> typing.Optional["ReleasePostrender"]:
        '''Postrender command config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#postrender Release#postrender}
        '''
        result = self._values.get("postrender")
        return typing.cast(typing.Optional["ReleasePostrender"], result)

    @builtins.property
    def recreate_pods(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Perform pods restart during upgrade/rollback.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#recreate_pods Release#recreate_pods}
        '''
        result = self._values.get("recreate_pods")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def render_subchart_notes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, render subchart notes along with the parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#render_subchart_notes Release#render_subchart_notes}
        '''
        result = self._values.get("render_subchart_notes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Re-use the given name, even if that name is already used. This is unsafe in production.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#replace Release#replace}
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Repository where to locate the requested chart.

        If it is a URL, the chart is installed without installing the repository

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository Release#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_ca_file(self) -> typing.Optional[builtins.str]:
        '''The Repositories CA file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_ca_file Release#repository_ca_file}
        '''
        result = self._values.get("repository_ca_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_cert_file(self) -> typing.Optional[builtins.str]:
        '''The repositories cert file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_cert_file Release#repository_cert_file}
        '''
        result = self._values.get("repository_cert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_key_file(self) -> typing.Optional[builtins.str]:
        '''The repositories cert key file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_key_file Release#repository_key_file}
        '''
        result = self._values.get("repository_key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_password(self) -> typing.Optional[builtins.str]:
        '''Password for HTTP basic authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_password Release#repository_password}
        '''
        result = self._values.get("repository_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_username(self) -> typing.Optional[builtins.str]:
        '''Username for HTTP basic authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#repository_username Release#repository_username}
        '''
        result = self._values.get("repository_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reset_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When upgrading, reset the values to the ones built into the chart.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#reset_values Release#reset_values}
        '''
        result = self._values.get("reset_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reuse_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When upgrading, reuse the last release's values and merge in any overrides. If 'reset_values' is specified, this is ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#reuse_values Release#reuse_values}
        '''
        result = self._values.get("reuse_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSet"]]]:
        '''Custom values to be merged with the values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set Release#set}
        '''
        result = self._values.get("set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSet"]]], result)

    @builtins.property
    def set_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetListStruct"]]]:
        '''Custom sensitive values to be merged with the values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_list Release#set_list}
        '''
        result = self._values.get("set_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetListStruct"]]], result)

    @builtins.property
    def set_sensitive(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetSensitive"]]]:
        '''Custom sensitive values to be merged with the values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_sensitive Release#set_sensitive}
        '''
        result = self._values.get("set_sensitive")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetSensitive"]]], result)

    @builtins.property
    def set_wo(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetWo"]]]:
        '''Custom values to be merged with the values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_wo Release#set_wo}
        '''
        result = self._values.get("set_wo")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ReleaseSetWo"]]], result)

    @builtins.property
    def set_wo_revision(self) -> typing.Optional[jsii.Number]:
        '''The current revision of the write-only "set_wo" attribute.

        Incrementing this integer value will cause Terraform to update the write-only value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#set_wo_revision Release#set_wo_revision}
        '''
        result = self._values.get("set_wo_revision")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def skip_crds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, no CRDs will be installed. By default, CRDs are installed if not already present.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#skip_crds Release#skip_crds}
        '''
        result = self._values.get("skip_crds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds to wait for any individual kubernetes operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#timeout Release#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values in raw YAML format to pass to helm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#values Release#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Verify the package before installing it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#verify Release#verify}
        '''
        result = self._values.get("verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Specify the exact chart version to install. If this is not specified, the latest version is installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#version Release#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Will wait until all resources are in a ready state before marking the release as successful.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#wait Release#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def wait_for_jobs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If wait is enabled, will wait until all Jobs have been completed before marking the release as successful.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#wait_for_jobs Release#wait_for_jobs}
        '''
        result = self._values.get("wait_for_jobs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.release.ReleaseMetadata",
    jsii_struct_bases=[],
    name_mapping={},
)
class ReleaseMetadata:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61490c34098948e59690943dad087e722da0311d13b99853b9a18bcc8b623f4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="appVersion")
    def app_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appVersion"))

    @builtins.property
    @jsii.member(jsii_name="chart")
    def chart(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chart"))

    @builtins.property
    @jsii.member(jsii_name="firstDeployed")
    def first_deployed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "firstDeployed"))

    @builtins.property
    @jsii.member(jsii_name="lastDeployed")
    def last_deployed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastDeployed"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "revision"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ReleaseMetadata]:
        return typing.cast(typing.Optional[ReleaseMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ReleaseMetadata]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0c323387b308763e517d47b2ea47e7211b9d1655b9b6c88d3a3678a60c0d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.release.ReleasePostrender",
    jsii_struct_bases=[],
    name_mapping={"binary_path": "binaryPath", "args": "args"},
)
class ReleasePostrender:
    def __init__(
        self,
        *,
        binary_path: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param binary_path: The common binary path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#binary_path Release#binary_path}
        :param args: An argument to the post-renderer (can specify multiple). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#args Release#args}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981056baac01e08a9be241caf4b8905301446900d1d7eecfc096ec7c50fd4c55)
            check_type(argname="argument binary_path", value=binary_path, expected_type=type_hints["binary_path"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "binary_path": binary_path,
        }
        if args is not None:
            self._values["args"] = args

    @builtins.property
    def binary_path(self) -> builtins.str:
        '''The common binary path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#binary_path Release#binary_path}
        '''
        result = self._values.get("binary_path")
        assert result is not None, "Required property 'binary_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An argument to the post-renderer (can specify multiple).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#args Release#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleasePostrender(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleasePostrenderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleasePostrenderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f96a8a6d8aa8ec1e7abee5ffdaec6e7e7103b6c972c40e3ea94d237ec6659934)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="binaryPathInput")
    def binary_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "binaryPathInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5be9dc2d3336e5ce2d8f2e4e3e6e79c1c144f2457f966f176ff3d54478684c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryPath")
    def binary_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryPath"))

    @binary_path.setter
    def binary_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee4b033c3e9de1722a215756c780e8ff0378d0493e7c0f883e1c093e3909cbd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleasePostrender]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleasePostrender]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleasePostrender]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844a501608c2a9c6233555fbfed820dc99204232e5cdf42f37235c0257764013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.release.ReleaseSet",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "value": "value"},
)
class ReleaseSet:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#type Release#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#value Release#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b40ee13479cae3240c1ba06fd537a3e15ab3fbca99f29411b2d968f452c5a980)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if type is not None:
            self._values["type"] = type
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#type Release#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#value Release#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f390bcfbcfa6eda2156f0abc4488d3f5186be9ca1004b3425325c696c95c6874)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ReleaseSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53f9d4a9bcd94d41efd0d15efe364c0d6393db56e3d6b20f2e6937f9fe18882)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ReleaseSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59954bbea5a7a1f52bb4948fc01eb6c3b45a4eb2d694020e96aa79704376f2d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81ab9a690bd7c9fbc8ccf1451d1236374293c964e95246e79bc279fa763ff8a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8baaaa01d471c8d2ec5cc6e13c4401f948d4d7a810990e33e63453769731be9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ca85907af9cf85a8ac2dc36272b5268e80c3a54e28b189fccbbaaa77e83094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.release.ReleaseSetListStruct",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ReleaseSetListStruct:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#value Release#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__508f3584f37548827519997a7378963046271d485d0bb70d9ba0ee49230f97b1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#value Release#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseSetListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseSetListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseSetListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__506e3c4fb8d423f7c946de19016f6ebc30c1bcbb7a3ded0e9273d68545fb1dc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ReleaseSetListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebea825e6d9857a5a200e3a0a0a0a7f402755c1a9a6f74cce00614feee2edb9f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ReleaseSetListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650b5d025108ec67ac17015a5be61baa8e0d1d9fd908dbd015d5a0eeb2701e73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ef07a70eee43811f80dae9728021bec9ea4a82e9ea6d05537fba481ed607312)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60909616a85d34562129544b26e7f3be6d889d64839017ec3d2d5ed9439a7f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcca7dc69fbd34bba0bdcfe01d96ba624825aa38bb09e9a24ad6bf77dcaa295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ReleaseSetListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseSetListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9da10675f069e7d164482711958df693111957ebaa0a5569aff52837d57081e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__288d802b0cacbddb2d07c7b72ccf95eb794c3b5f1da482f47cc28254afbd0f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "value"))

    @value.setter
    def value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cd18e83dfef4ac26bd1113e6537cf2469ca874f77954d24c1523bb828f497e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350fa01806e21d206a65b4e7cebe986132bd002ae3ab7d01a7a6e03343183688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ReleaseSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6efd1b4f4eb146a9e29807c430593a784d3e67a3ca29c40ed2b49dc8658eb55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eda69f6f187ce8f5861e920f50c00d8eacd32ed2fc65ab43583251995a3275e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfdd1464a6625527552276dca98bda1b1fe60bbc02735d9e1240d48af7384768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4334fc4c7d3ff7bf5960f1bbd88b7429e3f7c757bc29afe81894783ffad5c461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978caa0aad6ace4b6c6ee8080a9489eef1304413bbfe439cf2252c297f5ec88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.release.ReleaseSetSensitive",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "type": "type"},
)
class ReleaseSetSensitive:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#value Release#value}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#type Release#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819e69b309674d2d9b39573b21155edba86166772433bfb823f741b56247a94e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#value Release#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#type Release#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseSetSensitive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseSetSensitiveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseSetSensitiveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ef69146cc70ac730118b416e187f9ed90bf25422837c8a1ed115893834c27dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ReleaseSetSensitiveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d719d68ebf4252965bcf2aaaff40bf479123e17c7eabfb7c5f5435d7a3654f2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ReleaseSetSensitiveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b952a3c4924ab3391257f580fee9bfd409a339364718d0c4581804d1e174895)
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
            type_hints = typing.get_type_hints(_typecheckingstub__007dfb68ff9ee91853f795c8f769e2a28c6c05efed76d6ab8343f95648a11890)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c114ba9bdbcc4a982cb8a6bb128510f7d500eb9c5495f6bf5905f0914632df0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetSensitive]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetSensitive]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetSensitive]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d02ddbfc3b0e8f56a18c4e0597b20d09ac585b07cf7a4c61ed0c88bea2302259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ReleaseSetSensitiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseSetSensitiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b32c7b1b00da0e80772ddb7eedc48b1fcf4db8c973780ddc1a9b2e4df917a59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a35527b69468ecf2c368325e77ba07ada3ba8de8b9cb9745e9abf5e3be0efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59506ff637e7756d6d5d93515bd5b4aed6ce140d3db9468592c32dfe7e625162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a8b0628c2879ecfc03aa347dd950544b66941f82f1bcad89a49300ccfde3bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetSensitive]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetSensitive]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetSensitive]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb736301413166055dd669397c951f73d8e5d9a18078bd1ea2f70ab9f137ba88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.release.ReleaseSetWo",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "type": "type"},
)
class ReleaseSetWo:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#value Release#value}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#type Release#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382d5fafb9edfe6976872de67b0f06002699ff2d8f9910132a2dfd628848deba)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#name Release#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#value Release#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/resources/release#type Release#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseSetWo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReleaseSetWoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseSetWoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b2d7e258aded12f30ee5120519f0f28fe44bdfe0f1801dcf651a45c930e3354)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ReleaseSetWoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eed53bb762101c39869be420e8dc42735b54d77a0e2df57d1e1984abdc7decc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ReleaseSetWoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9183283013278742154ef4e69c714ed7742a1ef7fbb679e15b61bce31d96be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7798c6a10b7aed2b3cec0a988e748ad310bc85a5af335ba7ac32384f7322149a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbc1aece30ff98bd104de09fdac3e1caf5aea9a4b294f02765463a5d4f8b5fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetWo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetWo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetWo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4760ee5dccf7a3debace4c4bb55ffadce2fe63414574df908d0d9ac513719317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ReleaseSetWoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.release.ReleaseSetWoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c877b112773e5dff54b01884cce3efc221e01974b0b1cdfeafdf230156ed5104)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b758d4cae37b0f4dddb35b59a9186f1efcc9a15e7dd4c06a57b7bd14e1e8d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31e4e8b95129d065326badba0c8a437eae0f7d4bb95ee3eee7a104ffc81237e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13053390dc1400101bfa6e94d06a51bc7e1475b637cf0555fecb5237cc8f947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetWo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetWo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetWo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d1ac40d275788a3c4ae3038e78a09c503e2518b2b22232976104bf8c22f9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Release",
    "ReleaseConfig",
    "ReleaseMetadata",
    "ReleaseMetadataOutputReference",
    "ReleasePostrender",
    "ReleasePostrenderOutputReference",
    "ReleaseSet",
    "ReleaseSetList",
    "ReleaseSetListStruct",
    "ReleaseSetListStructList",
    "ReleaseSetListStructOutputReference",
    "ReleaseSetOutputReference",
    "ReleaseSetSensitive",
    "ReleaseSetSensitiveList",
    "ReleaseSetSensitiveOutputReference",
    "ReleaseSetWo",
    "ReleaseSetWoList",
    "ReleaseSetWoOutputReference",
]

publication.publish()

def _typecheckingstub__dc75acd85229e479b8b9aa92aa7d1b843987201bf6028137a9a9eb6a0d093d27(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    chart: builtins.str,
    name: builtins.str,
    atomic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cleanup_on_fail: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_namespace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dependency_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    devel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_crd_hooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_openapi_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_webhooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keyring: typing.Optional[builtins.str] = None,
    lint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_history: typing.Optional[jsii.Number] = None,
    namespace: typing.Optional[builtins.str] = None,
    pass_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    postrender: typing.Optional[typing.Union[ReleasePostrender, typing.Dict[builtins.str, typing.Any]]] = None,
    recreate_pods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    render_subchart_notes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    repository: typing.Optional[builtins.str] = None,
    repository_ca_file: typing.Optional[builtins.str] = None,
    repository_cert_file: typing.Optional[builtins.str] = None,
    repository_key_file: typing.Optional[builtins.str] = None,
    repository_password: typing.Optional[builtins.str] = None,
    repository_username: typing.Optional[builtins.str] = None,
    reset_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reuse_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_sensitive: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetSensitive, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_wo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetWo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_wo_revision: typing.Optional[jsii.Number] = None,
    skip_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version: typing.Optional[builtins.str] = None,
    wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_for_jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__23f22d9bf92f2c37284b57419397b6b7c21cc71a65d75a31f11cddcec3bea801(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b72a3657c0803010731fa3fd2044a0f404b98ac9399b1fb916895c0de83919d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e66f987c47878d4a6946a5a1dc06f0d9f1ca6ba2ae98348676c4bd5950c185(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf9382a783d49a3885b1e5db3d0b63f63fc7a33b8cdeefbeace8a470ca85b20(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetSensitive, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348d8f84de46e2c85afa109d2e4e18ebe58dbf6a5a00304197583870aeba301d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetWo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64d1ea2d4d5c0481d8d2a15fc4f143dbdef8ab41305fc11564450cdd45168cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0972b5f344751dc09888b8fdf49f426ba74bd115c7bf939efa8cbe108094db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37497fd707dd6ad0c6a6b1755e1b65b9bd4e1643e80194841b30de8d7a541719(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70664fb2b60e53eb7984a10c7d4873f03dffacaabb5371072f7c932f815a879d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8726af0cd133ebc83278398bf17a00684cc7ea549abcb2ed489b0dbcd1a73c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33f630af84ebed1c38b5556ab929098c5840644dd12764b1d0dbbad9b1faa86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4925d70a12400e378464de8adcf097b32a6e7fa55547ae56a3854209a257d2d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ca50f8b4a144c892fda160eb884e1df188a56ea06d633bf07b7afe253241f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874ec0e11ad9c3c0b6720eef0a1356730e45f1a4565dc52f009d468321bf62f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd480ec846441f10de7b93fcd878789f6a39b3f26f9557124d682352fb6018d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00fb4fd9f947ec509a72ea5df207806c78db1f0bdb4dc5dfb98bb4e165fa124(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72e97527302e9450ca9ddb8351f9162f113637b872335b5f5a384e5d83cb02c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebefd20b5ab48275a464a8c7c78ace5dc7303737eda6dd1173d2b87d766c9e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396f4fa6654a36f4b029f0fdfbac7cb17d59c5a4277e02067a0a4572080552e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f78192da9ffa2588128021bab8cc62b4c1885e04a30d156da8e1bc52909d6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce927be764a91bed32dd47e6d200dba849f59c938d25042eed1a254535ea77b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defb85457399fa43643f8b85054001f91ef22c1b085e80338f181a1f8bf71330(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8021737dc70fde376fd307eeeceff08eb6e262c5ef095a79cee8538f3f022ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda9ecf3c5d8298fa6866e24c3d45ffea7dfaff11f106c7b04985a73e8c43731(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810f8f0f875cba91fd2f30bebdfd606318cee23d858b63c8fa3e3572398c5b1d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5aeeefc17c0b60ea0f1040c237b6816524f29703deee6f467d4d92fb49d420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b5e4e0f62cc6e9d49340203075836922bfbeec046ef951937bd70320abfcc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0253e86727e3dda147544d73591ec9c7dfefc63f9b5b28ded78fe0879f7ebd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621352acc4776b44aea7e43dede99a4bf3c1153e4dff66d1545066db21be2d5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050722a21ec7404de1dce14e6868df429d8007b2ead81a4f565050beef5bc14b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc40d9b0c867608d404c07c13d4b3154594bcd91558c32c6f828b45adade26b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45878404436c4d09b10a954b5f6f79b67a5322f943e28be2fe3c88100471583(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39bdd2d1d76a4eaa3b8bcdc62bb294e13642ab521d59e8683a345c63eb355b5f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126382aa9f62f1a4a6eb6642cd56021452a3570e6b4c218b63f16f2227b48418(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842028bb5398dae0afe025b331cfac2e399e0b3392a25e154a8b45e9e6df62fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce093763d1e99d1031c3d9f244d12dc614bf528e5ba752c43ccca3d29d96f4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b719961948e4ed89dbc8e48b7a1d51792f716cf2c6bb00bfb266a656d6df5d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa71240bc0a569257fd1df4bab30e3ee9907b3ff14b999b808d7a535753138c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ae21aa002d2702ab16a4877ff2a5d7a6d5f14e9f1b917eecaff9ede140825a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b25640d7d4e45b12467e1045d8c98a166002706634010cbce3351fc1f680e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5926058acef0ca2b7e353de193a9045b7d1dce153706e704e0078f7103f20a6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3351956da04ddf8ca86567e1dd64c43a3a02b9b30bc17a13da12597bc326e840(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    chart: builtins.str,
    name: builtins.str,
    atomic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cleanup_on_fail: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_namespace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dependency_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    devel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_crd_hooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_openapi_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_webhooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    force_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keyring: typing.Optional[builtins.str] = None,
    lint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_history: typing.Optional[jsii.Number] = None,
    namespace: typing.Optional[builtins.str] = None,
    pass_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    postrender: typing.Optional[typing.Union[ReleasePostrender, typing.Dict[builtins.str, typing.Any]]] = None,
    recreate_pods: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    render_subchart_notes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    repository: typing.Optional[builtins.str] = None,
    repository_ca_file: typing.Optional[builtins.str] = None,
    repository_cert_file: typing.Optional[builtins.str] = None,
    repository_key_file: typing.Optional[builtins.str] = None,
    repository_password: typing.Optional[builtins.str] = None,
    repository_username: typing.Optional[builtins.str] = None,
    reset_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reuse_values: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_sensitive: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetSensitive, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_wo: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ReleaseSetWo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_wo_revision: typing.Optional[jsii.Number] = None,
    skip_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version: typing.Optional[builtins.str] = None,
    wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    wait_for_jobs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61490c34098948e59690943dad087e722da0311d13b99853b9a18bcc8b623f4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0c323387b308763e517d47b2ea47e7211b9d1655b9b6c88d3a3678a60c0d4b(
    value: typing.Optional[ReleaseMetadata],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981056baac01e08a9be241caf4b8905301446900d1d7eecfc096ec7c50fd4c55(
    *,
    binary_path: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96a8a6d8aa8ec1e7abee5ffdaec6e7e7103b6c972c40e3ea94d237ec6659934(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5be9dc2d3336e5ce2d8f2e4e3e6e79c1c144f2457f966f176ff3d54478684c7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4b033c3e9de1722a215756c780e8ff0378d0493e7c0f883e1c093e3909cbd6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844a501608c2a9c6233555fbfed820dc99204232e5cdf42f37235c0257764013(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleasePostrender]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40ee13479cae3240c1ba06fd537a3e15ab3fbca99f29411b2d968f452c5a980(
    *,
    name: builtins.str,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f390bcfbcfa6eda2156f0abc4488d3f5186be9ca1004b3425325c696c95c6874(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e53f9d4a9bcd94d41efd0d15efe364c0d6393db56e3d6b20f2e6937f9fe18882(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59954bbea5a7a1f52bb4948fc01eb6c3b45a4eb2d694020e96aa79704376f2d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ab9a690bd7c9fbc8ccf1451d1236374293c964e95246e79bc279fa763ff8a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8baaaa01d471c8d2ec5cc6e13c4401f948d4d7a810990e33e63453769731be9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ca85907af9cf85a8ac2dc36272b5268e80c3a54e28b189fccbbaaa77e83094(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508f3584f37548827519997a7378963046271d485d0bb70d9ba0ee49230f97b1(
    *,
    name: builtins.str,
    value: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506e3c4fb8d423f7c946de19016f6ebc30c1bcbb7a3ded0e9273d68545fb1dc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebea825e6d9857a5a200e3a0a0a0a7f402755c1a9a6f74cce00614feee2edb9f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650b5d025108ec67ac17015a5be61baa8e0d1d9fd908dbd015d5a0eeb2701e73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef07a70eee43811f80dae9728021bec9ea4a82e9ea6d05537fba481ed607312(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60909616a85d34562129544b26e7f3be6d889d64839017ec3d2d5ed9439a7f1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bcca7dc69fbd34bba0bdcfe01d96ba624825aa38bb09e9a24ad6bf77dcaa295(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9da10675f069e7d164482711958df693111957ebaa0a5569aff52837d57081e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288d802b0cacbddb2d07c7b72ccf95eb794c3b5f1da482f47cc28254afbd0f0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cd18e83dfef4ac26bd1113e6537cf2469ca874f77954d24c1523bb828f497e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350fa01806e21d206a65b4e7cebe986132bd002ae3ab7d01a7a6e03343183688(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6efd1b4f4eb146a9e29807c430593a784d3e67a3ca29c40ed2b49dc8658eb55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eda69f6f187ce8f5861e920f50c00d8eacd32ed2fc65ab43583251995a3275e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfdd1464a6625527552276dca98bda1b1fe60bbc02735d9e1240d48af7384768(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4334fc4c7d3ff7bf5960f1bbd88b7429e3f7c757bc29afe81894783ffad5c461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978caa0aad6ace4b6c6ee8080a9489eef1304413bbfe439cf2252c297f5ec88d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819e69b309674d2d9b39573b21155edba86166772433bfb823f741b56247a94e(
    *,
    name: builtins.str,
    value: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef69146cc70ac730118b416e187f9ed90bf25422837c8a1ed115893834c27dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d719d68ebf4252965bcf2aaaff40bf479123e17c7eabfb7c5f5435d7a3654f2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b952a3c4924ab3391257f580fee9bfd409a339364718d0c4581804d1e174895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007dfb68ff9ee91853f795c8f769e2a28c6c05efed76d6ab8343f95648a11890(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c114ba9bdbcc4a982cb8a6bb128510f7d500eb9c5495f6bf5905f0914632df0e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02ddbfc3b0e8f56a18c4e0597b20d09ac585b07cf7a4c61ed0c88bea2302259(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetSensitive]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b32c7b1b00da0e80772ddb7eedc48b1fcf4db8c973780ddc1a9b2e4df917a59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a35527b69468ecf2c368325e77ba07ada3ba8de8b9cb9745e9abf5e3be0efb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59506ff637e7756d6d5d93515bd5b4aed6ce140d3db9468592c32dfe7e625162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a8b0628c2879ecfc03aa347dd950544b66941f82f1bcad89a49300ccfde3bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb736301413166055dd669397c951f73d8e5d9a18078bd1ea2f70ab9f137ba88(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetSensitive]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382d5fafb9edfe6976872de67b0f06002699ff2d8f9910132a2dfd628848deba(
    *,
    name: builtins.str,
    value: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2d7e258aded12f30ee5120519f0f28fe44bdfe0f1801dcf651a45c930e3354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eed53bb762101c39869be420e8dc42735b54d77a0e2df57d1e1984abdc7decc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9183283013278742154ef4e69c714ed7742a1ef7fbb679e15b61bce31d96be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7798c6a10b7aed2b3cec0a988e748ad310bc85a5af335ba7ac32384f7322149a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc1aece30ff98bd104de09fdac3e1caf5aea9a4b294f02765463a5d4f8b5fd8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4760ee5dccf7a3debace4c4bb55ffadce2fe63414574df908d0d9ac513719317(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ReleaseSetWo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c877b112773e5dff54b01884cce3efc221e01974b0b1cdfeafdf230156ed5104(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b758d4cae37b0f4dddb35b59a9186f1efcc9a15e7dd4c06a57b7bd14e1e8d44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31e4e8b95129d065326badba0c8a437eae0f7d4bb95ee3eee7a104ffc81237e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13053390dc1400101bfa6e94d06a51bc7e1475b637cf0555fecb5237cc8f947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d1ac40d275788a3c4ae3038e78a09c503e2518b2b22232976104bf8c22f9cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ReleaseSetWo]],
) -> None:
    """Type checking stubs"""
    pass
