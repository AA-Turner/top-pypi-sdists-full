r'''
# `data_helm_template`

Refer to the Terraform Registry for docs: [`data_helm_template`](https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template).
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


class DataHelmTemplate(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplate",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template helm_template}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        chart: builtins.str,
        name: builtins.str,
        api_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        atomic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crds: typing.Optional[typing.Sequence[builtins.str]] = None,
        create_namespace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dependency_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        devel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_openapi_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_webhooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keyring: typing.Optional[builtins.str] = None,
        kube_version: typing.Optional[builtins.str] = None,
        manifest: typing.Optional[builtins.str] = None,
        manifests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        pass_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        postrender: typing.Optional[typing.Union["DataHelmTemplatePostrender", typing.Dict[builtins.str, typing.Any]]] = None,
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
        set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSetListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_sensitive: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSetSensitive", typing.Dict[builtins.str, typing.Any]]]]] = None,
        show_only: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_tests: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version: typing.Optional[builtins.str] = None,
        wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template helm_template} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param chart: Chart name to be installed. A path may be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#chart DataHelmTemplate#chart}
        :param name: Release name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}
        :param api_versions: Kubernetes api versions used for Capabilities.APIVersions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#api_versions DataHelmTemplate#api_versions}
        :param atomic: If set, the installation process purges the chart on fail. The 'wait' flag will be set automatically if 'atomic' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#atomic DataHelmTemplate#atomic}
        :param crds: List of rendered CRDs from the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#crds DataHelmTemplate#crds}
        :param create_namespace: Create the namespace if it does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#create_namespace DataHelmTemplate#create_namespace}
        :param dependency_update: Run helm dependency update before installing the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#dependency_update DataHelmTemplate#dependency_update}
        :param description: Add a custom description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#description DataHelmTemplate#description}
        :param devel: Use chart development versions, too. Equivalent to version '>0.0.0-0'. If ``version`` is set, this is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#devel DataHelmTemplate#devel}
        :param disable_openapi_validation: If set, the installation process will not validate rendered templates against the Kubernetes OpenAPI Schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#disable_openapi_validation DataHelmTemplate#disable_openapi_validation}
        :param disable_webhooks: Prevent hooks from running. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#disable_webhooks DataHelmTemplate#disable_webhooks}
        :param include_crds: Include CRDs in the templated output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#include_crds DataHelmTemplate#include_crds}
        :param is_upgrade: Set .Release.IsUpgrade instead of .Release.IsInstall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#is_upgrade DataHelmTemplate#is_upgrade}
        :param keyring: Location of public keys used for verification. Used only if ``verify`` is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#keyring DataHelmTemplate#keyring}
        :param kube_version: Kubernetes version used for Capabilities.KubeVersion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#kube_version DataHelmTemplate#kube_version}
        :param manifest: Concatenated rendered chart templates. This corresponds to the output of the ``helm template`` command. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#manifest DataHelmTemplate#manifest}
        :param manifests: Map of rendered chart templates indexed by the template name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#manifests DataHelmTemplate#manifests}
        :param namespace: Namespace to install the release into. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#namespace DataHelmTemplate#namespace}
        :param notes: Rendered notes if the chart contains a ``NOTES.txt``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#notes DataHelmTemplate#notes}
        :param pass_credentials: Pass credentials to all domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#pass_credentials DataHelmTemplate#pass_credentials}
        :param postrender: Postrender command config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#postrender DataHelmTemplate#postrender}
        :param render_subchart_notes: If set, render subchart notes along with the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#render_subchart_notes DataHelmTemplate#render_subchart_notes}
        :param replace: Re-use the given name, even if that name is already used. This is unsafe in production. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#replace DataHelmTemplate#replace}
        :param repository: Repository where to locate the requested chart. If it is a URL the chart is installed without installing the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository DataHelmTemplate#repository}
        :param repository_ca_file: The repository's CA file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_ca_file DataHelmTemplate#repository_ca_file}
        :param repository_cert_file: The repository's cert file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_cert_file DataHelmTemplate#repository_cert_file}
        :param repository_key_file: The repository's cert key file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_key_file DataHelmTemplate#repository_key_file}
        :param repository_password: Password for HTTP basic authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_password DataHelmTemplate#repository_password}
        :param repository_username: Username for HTTP basic authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_username DataHelmTemplate#repository_username}
        :param reset_values: When upgrading, reset the values to the ones built into the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#reset_values DataHelmTemplate#reset_values}
        :param reuse_values: When upgrading, reuse the last release's values and merge in any overrides. If 'reset_values' is specified, this is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#reuse_values DataHelmTemplate#reuse_values}
        :param set: Custom values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set DataHelmTemplate#set}
        :param set_list: Custom sensitive values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set_list DataHelmTemplate#set_list}
        :param set_sensitive: Custom sensitive values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set_sensitive DataHelmTemplate#set_sensitive}
        :param show_only: Only show manifests rendered from the given templates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#show_only DataHelmTemplate#show_only}
        :param skip_crds: If set, no CRDs will be installed. By default, CRDs are installed if not already present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#skip_crds DataHelmTemplate#skip_crds}
        :param skip_tests: If set, tests will not be rendered. By default, tests are rendered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#skip_tests DataHelmTemplate#skip_tests}
        :param timeout: Time in seconds to wait for any individual Kubernetes operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#timeout DataHelmTemplate#timeout}
        :param validate: Validate your manifests against the Kubernetes cluster you are currently pointing at. This is the same validation performed on an install. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#validate DataHelmTemplate#validate}
        :param values: List of values in raw yaml format to pass to helm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#values DataHelmTemplate#values}
        :param verify: Verify the package before installing it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#verify DataHelmTemplate#verify}
        :param version: Specify the exact chart version to install. If this is not specified, the latest version is installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#version DataHelmTemplate#version}
        :param wait: Will wait until all resources are in a ready state before marking the release as successful. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#wait DataHelmTemplate#wait}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c1e559d09940a986fee4320c6ad4564aaeb41d7bed779451d692fbc4050767)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataHelmTemplateConfig(
            chart=chart,
            name=name,
            api_versions=api_versions,
            atomic=atomic,
            crds=crds,
            create_namespace=create_namespace,
            dependency_update=dependency_update,
            description=description,
            devel=devel,
            disable_openapi_validation=disable_openapi_validation,
            disable_webhooks=disable_webhooks,
            include_crds=include_crds,
            is_upgrade=is_upgrade,
            keyring=keyring,
            kube_version=kube_version,
            manifest=manifest,
            manifests=manifests,
            namespace=namespace,
            notes=notes,
            pass_credentials=pass_credentials,
            postrender=postrender,
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
            show_only=show_only,
            skip_crds=skip_crds,
            skip_tests=skip_tests,
            timeout=timeout,
            validate=validate,
            values=values,
            verify=verify,
            version=version,
            wait=wait,
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
        '''Generates CDKTF code for importing a DataHelmTemplate resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataHelmTemplate to import.
        :param import_from_id: The id of the existing DataHelmTemplate that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataHelmTemplate to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea480acf4a220b3d6ba7a7f3ea415b79d6952d6947a59a54d20a41bab385994)
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
        :param binary_path: The common binary path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#binary_path DataHelmTemplate#binary_path}
        :param args: An argument to the post-renderer (can specify multiple). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#args DataHelmTemplate#args}
        '''
        value = DataHelmTemplatePostrender(binary_path=binary_path, args=args)

        return typing.cast(None, jsii.invoke(self, "putPostrender", [value]))

    @jsii.member(jsii_name="putSet")
    def put_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1596ab16b5d874b157172d384e60dca3a78047fbd42fa1f5b63eee3f239c3aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSet", [value]))

    @jsii.member(jsii_name="putSetList")
    def put_set_list(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSetListStruct", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152cb09b5fbfc57dbe53841927f1ffb77aaf7ba9a73e8477e7ab141afc3b3863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetList", [value]))

    @jsii.member(jsii_name="putSetSensitive")
    def put_set_sensitive(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSetSensitive", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f695897482a9ad07999645b33f485ea7dc3b43747d170cf346beb84d2ac5ea3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetSensitive", [value]))

    @jsii.member(jsii_name="resetApiVersions")
    def reset_api_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiVersions", []))

    @jsii.member(jsii_name="resetAtomic")
    def reset_atomic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAtomic", []))

    @jsii.member(jsii_name="resetCrds")
    def reset_crds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrds", []))

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

    @jsii.member(jsii_name="resetDisableOpenapiValidation")
    def reset_disable_openapi_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableOpenapiValidation", []))

    @jsii.member(jsii_name="resetDisableWebhooks")
    def reset_disable_webhooks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableWebhooks", []))

    @jsii.member(jsii_name="resetIncludeCrds")
    def reset_include_crds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeCrds", []))

    @jsii.member(jsii_name="resetIsUpgrade")
    def reset_is_upgrade(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsUpgrade", []))

    @jsii.member(jsii_name="resetKeyring")
    def reset_keyring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyring", []))

    @jsii.member(jsii_name="resetKubeVersion")
    def reset_kube_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubeVersion", []))

    @jsii.member(jsii_name="resetManifest")
    def reset_manifest(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManifest", []))

    @jsii.member(jsii_name="resetManifests")
    def reset_manifests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManifests", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetNotes")
    def reset_notes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotes", []))

    @jsii.member(jsii_name="resetPassCredentials")
    def reset_pass_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassCredentials", []))

    @jsii.member(jsii_name="resetPostrender")
    def reset_postrender(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostrender", []))

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

    @jsii.member(jsii_name="resetShowOnly")
    def reset_show_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShowOnly", []))

    @jsii.member(jsii_name="resetSkipCrds")
    def reset_skip_crds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipCrds", []))

    @jsii.member(jsii_name="resetSkipTests")
    def reset_skip_tests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipTests", []))

    @jsii.member(jsii_name="resetTfValues")
    def reset_tf_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTfValues", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetValidate")
    def reset_validate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidate", []))

    @jsii.member(jsii_name="resetVerify")
    def reset_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerify", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetWait")
    def reset_wait(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWait", []))

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
    @jsii.member(jsii_name="postrender")
    def postrender(self) -> "DataHelmTemplatePostrenderOutputReference":
        return typing.cast("DataHelmTemplatePostrenderOutputReference", jsii.get(self, "postrender"))

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> "DataHelmTemplateSetList":
        return typing.cast("DataHelmTemplateSetList", jsii.get(self, "set"))

    @builtins.property
    @jsii.member(jsii_name="setList")
    def set_list(self) -> "DataHelmTemplateSetListStructList":
        return typing.cast("DataHelmTemplateSetListStructList", jsii.get(self, "setList"))

    @builtins.property
    @jsii.member(jsii_name="setSensitive")
    def set_sensitive(self) -> "DataHelmTemplateSetSensitiveList":
        return typing.cast("DataHelmTemplateSetSensitiveList", jsii.get(self, "setSensitive"))

    @builtins.property
    @jsii.member(jsii_name="apiVersionsInput")
    def api_versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "apiVersionsInput"))

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
    @jsii.member(jsii_name="crdsInput")
    def crds_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "crdsInput"))

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
    @jsii.member(jsii_name="includeCrdsInput")
    def include_crds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeCrdsInput"))

    @builtins.property
    @jsii.member(jsii_name="isUpgradeInput")
    def is_upgrade_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isUpgradeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyringInput")
    def keyring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyringInput"))

    @builtins.property
    @jsii.member(jsii_name="kubeVersionInput")
    def kube_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestInput")
    def manifest_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manifestInput"))

    @builtins.property
    @jsii.member(jsii_name="manifestsInput")
    def manifests_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "manifestsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="notesInput")
    def notes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataHelmTemplatePostrender"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataHelmTemplatePostrender"]], jsii.get(self, "postrenderInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSet"]]], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="setListInput")
    def set_list_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSetListStruct"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSetListStruct"]]], jsii.get(self, "setListInput"))

    @builtins.property
    @jsii.member(jsii_name="setSensitiveInput")
    def set_sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSetSensitive"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSetSensitive"]]], jsii.get(self, "setSensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="showOnlyInput")
    def show_only_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "showOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="skipCrdsInput")
    def skip_crds_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipCrdsInput"))

    @builtins.property
    @jsii.member(jsii_name="skipTestsInput")
    def skip_tests_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipTestsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateInput"))

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
    @jsii.member(jsii_name="waitInput")
    def wait_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "waitInput"))

    @builtins.property
    @jsii.member(jsii_name="apiVersions")
    def api_versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "apiVersions"))

    @api_versions.setter
    def api_versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eeac916cbbd1662c42211628356d464808cf3ef903532ac24ffd8c4a96aa0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiVersions", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__df81e6585e117067b993a67e46effaf0487be8735e62ccd7f9fed59b5ca071f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "atomic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="chart")
    def chart(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chart"))

    @chart.setter
    def chart(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6506552dd450214ce11c34372b7d04f8b22cadb8999c6ec94f48fb35b050151f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chart", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crds")
    def crds(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "crds"))

    @crds.setter
    def crds(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92799c956fb68e40124d5e9ee07cf0d246bef3a575daa81524655178f1838cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crds", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__3ff07092ae1a03d78b487ed26f127abc4ccd400f01f237d4b407ddf9380278b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c117039ddb8d257c128a704d89f4116fa98acb4b10a4aef1ebfc39e58d1e9ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencyUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc31f5fa9f8444a09f9828975d593887ab442a05a362b03024ddd9b096a6ced2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8f7dccf8dab54c2ce18cc3915f5ee2e4134b8a412dc1184e58a646fe009c21e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "devel", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__a561075e6def8561f9192061f83c3c1a19e41984787a623698101dfb387cf88b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df1f588c7368bc9b6c4691f13f4e3f50607c57bad1598c478eb08f4969fabad5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableWebhooks", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeCrds")
    def include_crds(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeCrds"))

    @include_crds.setter
    def include_crds(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474986d6384bac6fff89d9a17ed843098e1a2ee9ed19fad1f2b5799ed6e3f498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeCrds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isUpgrade")
    def is_upgrade(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isUpgrade"))

    @is_upgrade.setter
    def is_upgrade(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c876c95d429cecfd3d1d3b79538645811b0c738a6eb2f5f313b1ff65ced239b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isUpgrade", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyring")
    def keyring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyring"))

    @keyring.setter
    def keyring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15aa9486bc32e3b05999c435379c9e9b1a6475c1ac67a6f2b1a42b7215d6f463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyring", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kubeVersion")
    def kube_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubeVersion"))

    @kube_version.setter
    def kube_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b4c485adfd4740822f5eb93853551d25323c58aca9d610a80ee864bc55eaea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manifest"))

    @manifest.setter
    def manifest(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934b57dac3797675e0e93cbbd9fa63ec9df2dc9562ea3f665b52906f6e29fda5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="manifests")
    def manifests(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "manifests"))

    @manifests.setter
    def manifests(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50b7a44fe4cac624cc3dcf8e4465799c4a108779bf6dc1069e8781e5b3700d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69d925d1717bd13650969af356184f9101564c0ec716ce0c08e91bb91197c3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828e7e50f014ebcf2901a0beb9f6266c5052361244b42cd27acff9a81a5ca1fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6feec32869e9f991c74424c94f31d08cebc0f5e209d83fe70e563e3231b196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__2dd6108ac52691e48955544b60dc1e67203d89e17ac3786655eb4ac03fac6ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passCredentials", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__e3ba0ec2d71ad524f243f9dd6f7766d4b6da6b836696c2681ebc0c30399641eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a06d09a60cb9e5e636ecef40d21710b43005729b5731a986135afcad3ff7d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3d74aa62fcc91f5ed0822e42a62099c592aac40791eb11ac1aeaa6d343cef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryCaFile")
    def repository_ca_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryCaFile"))

    @repository_ca_file.setter
    def repository_ca_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0694b150e35bcf52fa174f7bb11ba6ad80bec209630e0d8bb3b4b5a62f7243e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCaFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryCertFile")
    def repository_cert_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryCertFile"))

    @repository_cert_file.setter
    def repository_cert_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fefceb2b14c698f4958703951b5e11f816aa2a33f34521561a6a388febe6dacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryCertFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryKeyFile")
    def repository_key_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryKeyFile"))

    @repository_key_file.setter
    def repository_key_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4353b4a969115f738a3bd7848c874a398c7e39ccd05e75d4863e7f87ab614c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryKeyFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryPassword")
    def repository_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryPassword"))

    @repository_password.setter
    def repository_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55cb7797dfc89be7681ae685752c40d032105c88a5478bb8abc790e074ddf81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryUsername")
    def repository_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUsername"))

    @repository_username.setter
    def repository_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c1c3633aeba7bab0170c109f3fa61f138e6b782a74b235ee0f603e3353ecca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90bcb2065a03b1694c05f12bc91f6b1f91025c75d2fe8063f8152d1394c60ab9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5bd289f49d9780b27a6f6641fc91534bf4b87c3c3448a1f515b33e8596d45a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reuseValues", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="showOnly")
    def show_only(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "showOnly"))

    @show_only.setter
    def show_only(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be9760942c024e63a6847d679b7a00ffc6e035b4438b6f459f9a4df75143f83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "showOnly", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__1a3feb8f7119901ebd885e214f90cf39318d7ff2f6999d56ee62c669ac918b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipCrds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipTests")
    def skip_tests(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipTests"))

    @skip_tests.setter
    def skip_tests(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539af9fbb9464df441f0e337716e48fbfaf952dcc8eadcab06f32c706e06d46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipTests", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf898eb8e953048800ae779d726623c46efce3d7cc84ed768a235f03031c93d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validate"))

    @validate.setter
    def validate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e32e337eb6fe1028fad504a177ae3d58fd62758e0090e7d2ba10829e043f62c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eef9b7e6247487f07d45ec5438bec423d8e0a19dd5829f0fc47f9e5444666db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bb18010aa70ac67269f67e5b12a5c1dd1874fa66431cb3c6da626e29787f4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verify", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480b78869a6effed1519d46b4a83794a4c8e0ccdc61a05e6829e5f36b19f13be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc948d679872e9bbd9ff27f3d13ab8bf94ea9643cffa6864f73cfb76b6b586e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wait", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateConfig",
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
        "api_versions": "apiVersions",
        "atomic": "atomic",
        "crds": "crds",
        "create_namespace": "createNamespace",
        "dependency_update": "dependencyUpdate",
        "description": "description",
        "devel": "devel",
        "disable_openapi_validation": "disableOpenapiValidation",
        "disable_webhooks": "disableWebhooks",
        "include_crds": "includeCrds",
        "is_upgrade": "isUpgrade",
        "keyring": "keyring",
        "kube_version": "kubeVersion",
        "manifest": "manifest",
        "manifests": "manifests",
        "namespace": "namespace",
        "notes": "notes",
        "pass_credentials": "passCredentials",
        "postrender": "postrender",
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
        "show_only": "showOnly",
        "skip_crds": "skipCrds",
        "skip_tests": "skipTests",
        "timeout": "timeout",
        "validate": "validate",
        "values": "values",
        "verify": "verify",
        "version": "version",
        "wait": "wait",
    },
)
class DataHelmTemplateConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
        atomic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        crds: typing.Optional[typing.Sequence[builtins.str]] = None,
        create_namespace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dependency_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        devel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_openapi_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_webhooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        keyring: typing.Optional[builtins.str] = None,
        kube_version: typing.Optional[builtins.str] = None,
        manifest: typing.Optional[builtins.str] = None,
        manifests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        pass_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        postrender: typing.Optional[typing.Union["DataHelmTemplatePostrender", typing.Dict[builtins.str, typing.Any]]] = None,
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
        set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSetListStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        set_sensitive: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataHelmTemplateSetSensitive", typing.Dict[builtins.str, typing.Any]]]]] = None,
        show_only: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_tests: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        values: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version: typing.Optional[builtins.str] = None,
        wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param chart: Chart name to be installed. A path may be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#chart DataHelmTemplate#chart}
        :param name: Release name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}
        :param api_versions: Kubernetes api versions used for Capabilities.APIVersions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#api_versions DataHelmTemplate#api_versions}
        :param atomic: If set, the installation process purges the chart on fail. The 'wait' flag will be set automatically if 'atomic' is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#atomic DataHelmTemplate#atomic}
        :param crds: List of rendered CRDs from the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#crds DataHelmTemplate#crds}
        :param create_namespace: Create the namespace if it does not exist. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#create_namespace DataHelmTemplate#create_namespace}
        :param dependency_update: Run helm dependency update before installing the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#dependency_update DataHelmTemplate#dependency_update}
        :param description: Add a custom description. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#description DataHelmTemplate#description}
        :param devel: Use chart development versions, too. Equivalent to version '>0.0.0-0'. If ``version`` is set, this is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#devel DataHelmTemplate#devel}
        :param disable_openapi_validation: If set, the installation process will not validate rendered templates against the Kubernetes OpenAPI Schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#disable_openapi_validation DataHelmTemplate#disable_openapi_validation}
        :param disable_webhooks: Prevent hooks from running. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#disable_webhooks DataHelmTemplate#disable_webhooks}
        :param include_crds: Include CRDs in the templated output. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#include_crds DataHelmTemplate#include_crds}
        :param is_upgrade: Set .Release.IsUpgrade instead of .Release.IsInstall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#is_upgrade DataHelmTemplate#is_upgrade}
        :param keyring: Location of public keys used for verification. Used only if ``verify`` is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#keyring DataHelmTemplate#keyring}
        :param kube_version: Kubernetes version used for Capabilities.KubeVersion. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#kube_version DataHelmTemplate#kube_version}
        :param manifest: Concatenated rendered chart templates. This corresponds to the output of the ``helm template`` command. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#manifest DataHelmTemplate#manifest}
        :param manifests: Map of rendered chart templates indexed by the template name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#manifests DataHelmTemplate#manifests}
        :param namespace: Namespace to install the release into. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#namespace DataHelmTemplate#namespace}
        :param notes: Rendered notes if the chart contains a ``NOTES.txt``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#notes DataHelmTemplate#notes}
        :param pass_credentials: Pass credentials to all domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#pass_credentials DataHelmTemplate#pass_credentials}
        :param postrender: Postrender command config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#postrender DataHelmTemplate#postrender}
        :param render_subchart_notes: If set, render subchart notes along with the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#render_subchart_notes DataHelmTemplate#render_subchart_notes}
        :param replace: Re-use the given name, even if that name is already used. This is unsafe in production. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#replace DataHelmTemplate#replace}
        :param repository: Repository where to locate the requested chart. If it is a URL the chart is installed without installing the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository DataHelmTemplate#repository}
        :param repository_ca_file: The repository's CA file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_ca_file DataHelmTemplate#repository_ca_file}
        :param repository_cert_file: The repository's cert file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_cert_file DataHelmTemplate#repository_cert_file}
        :param repository_key_file: The repository's cert key file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_key_file DataHelmTemplate#repository_key_file}
        :param repository_password: Password for HTTP basic authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_password DataHelmTemplate#repository_password}
        :param repository_username: Username for HTTP basic authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_username DataHelmTemplate#repository_username}
        :param reset_values: When upgrading, reset the values to the ones built into the chart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#reset_values DataHelmTemplate#reset_values}
        :param reuse_values: When upgrading, reuse the last release's values and merge in any overrides. If 'reset_values' is specified, this is ignored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#reuse_values DataHelmTemplate#reuse_values}
        :param set: Custom values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set DataHelmTemplate#set}
        :param set_list: Custom sensitive values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set_list DataHelmTemplate#set_list}
        :param set_sensitive: Custom sensitive values to be merged with the values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set_sensitive DataHelmTemplate#set_sensitive}
        :param show_only: Only show manifests rendered from the given templates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#show_only DataHelmTemplate#show_only}
        :param skip_crds: If set, no CRDs will be installed. By default, CRDs are installed if not already present. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#skip_crds DataHelmTemplate#skip_crds}
        :param skip_tests: If set, tests will not be rendered. By default, tests are rendered. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#skip_tests DataHelmTemplate#skip_tests}
        :param timeout: Time in seconds to wait for any individual Kubernetes operation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#timeout DataHelmTemplate#timeout}
        :param validate: Validate your manifests against the Kubernetes cluster you are currently pointing at. This is the same validation performed on an install. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#validate DataHelmTemplate#validate}
        :param values: List of values in raw yaml format to pass to helm. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#values DataHelmTemplate#values}
        :param verify: Verify the package before installing it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#verify DataHelmTemplate#verify}
        :param version: Specify the exact chart version to install. If this is not specified, the latest version is installed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#version DataHelmTemplate#version}
        :param wait: Will wait until all resources are in a ready state before marking the release as successful. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#wait DataHelmTemplate#wait}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(postrender, dict):
            postrender = DataHelmTemplatePostrender(**postrender)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa661fc2bc6a52eec136c130260e43e15fe67a8017a94efddda364fd2b2f33d2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument chart", value=chart, expected_type=type_hints["chart"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument api_versions", value=api_versions, expected_type=type_hints["api_versions"])
            check_type(argname="argument atomic", value=atomic, expected_type=type_hints["atomic"])
            check_type(argname="argument crds", value=crds, expected_type=type_hints["crds"])
            check_type(argname="argument create_namespace", value=create_namespace, expected_type=type_hints["create_namespace"])
            check_type(argname="argument dependency_update", value=dependency_update, expected_type=type_hints["dependency_update"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument devel", value=devel, expected_type=type_hints["devel"])
            check_type(argname="argument disable_openapi_validation", value=disable_openapi_validation, expected_type=type_hints["disable_openapi_validation"])
            check_type(argname="argument disable_webhooks", value=disable_webhooks, expected_type=type_hints["disable_webhooks"])
            check_type(argname="argument include_crds", value=include_crds, expected_type=type_hints["include_crds"])
            check_type(argname="argument is_upgrade", value=is_upgrade, expected_type=type_hints["is_upgrade"])
            check_type(argname="argument keyring", value=keyring, expected_type=type_hints["keyring"])
            check_type(argname="argument kube_version", value=kube_version, expected_type=type_hints["kube_version"])
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument manifests", value=manifests, expected_type=type_hints["manifests"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument pass_credentials", value=pass_credentials, expected_type=type_hints["pass_credentials"])
            check_type(argname="argument postrender", value=postrender, expected_type=type_hints["postrender"])
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
            check_type(argname="argument show_only", value=show_only, expected_type=type_hints["show_only"])
            check_type(argname="argument skip_crds", value=skip_crds, expected_type=type_hints["skip_crds"])
            check_type(argname="argument skip_tests", value=skip_tests, expected_type=type_hints["skip_tests"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument validate", value=validate, expected_type=type_hints["validate"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument verify", value=verify, expected_type=type_hints["verify"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument wait", value=wait, expected_type=type_hints["wait"])
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
        if api_versions is not None:
            self._values["api_versions"] = api_versions
        if atomic is not None:
            self._values["atomic"] = atomic
        if crds is not None:
            self._values["crds"] = crds
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if dependency_update is not None:
            self._values["dependency_update"] = dependency_update
        if description is not None:
            self._values["description"] = description
        if devel is not None:
            self._values["devel"] = devel
        if disable_openapi_validation is not None:
            self._values["disable_openapi_validation"] = disable_openapi_validation
        if disable_webhooks is not None:
            self._values["disable_webhooks"] = disable_webhooks
        if include_crds is not None:
            self._values["include_crds"] = include_crds
        if is_upgrade is not None:
            self._values["is_upgrade"] = is_upgrade
        if keyring is not None:
            self._values["keyring"] = keyring
        if kube_version is not None:
            self._values["kube_version"] = kube_version
        if manifest is not None:
            self._values["manifest"] = manifest
        if manifests is not None:
            self._values["manifests"] = manifests
        if namespace is not None:
            self._values["namespace"] = namespace
        if notes is not None:
            self._values["notes"] = notes
        if pass_credentials is not None:
            self._values["pass_credentials"] = pass_credentials
        if postrender is not None:
            self._values["postrender"] = postrender
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
        if show_only is not None:
            self._values["show_only"] = show_only
        if skip_crds is not None:
            self._values["skip_crds"] = skip_crds
        if skip_tests is not None:
            self._values["skip_tests"] = skip_tests
        if timeout is not None:
            self._values["timeout"] = timeout
        if validate is not None:
            self._values["validate"] = validate
        if values is not None:
            self._values["values"] = values
        if verify is not None:
            self._values["verify"] = verify
        if version is not None:
            self._values["version"] = version
        if wait is not None:
            self._values["wait"] = wait

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#chart DataHelmTemplate#chart}
        '''
        result = self._values.get("chart")
        assert result is not None, "Required property 'chart' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Release name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Kubernetes api versions used for Capabilities.APIVersions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#api_versions DataHelmTemplate#api_versions}
        '''
        result = self._values.get("api_versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def atomic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, the installation process purges the chart on fail.

        The 'wait' flag will be set automatically if 'atomic' is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#atomic DataHelmTemplate#atomic}
        '''
        result = self._values.get("atomic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def crds(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of rendered CRDs from the chart.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#crds DataHelmTemplate#crds}
        '''
        result = self._values.get("crds")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def create_namespace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Create the namespace if it does not exist.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#create_namespace DataHelmTemplate#create_namespace}
        '''
        result = self._values.get("create_namespace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dependency_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Run helm dependency update before installing the chart.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#dependency_update DataHelmTemplate#dependency_update}
        '''
        result = self._values.get("dependency_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Add a custom description.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#description DataHelmTemplate#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def devel(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use chart development versions, too. Equivalent to version '>0.0.0-0'. If ``version`` is set, this is ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#devel DataHelmTemplate#devel}
        '''
        result = self._values.get("devel")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_openapi_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, the installation process will not validate rendered templates against the Kubernetes OpenAPI Schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#disable_openapi_validation DataHelmTemplate#disable_openapi_validation}
        '''
        result = self._values.get("disable_openapi_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_webhooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent hooks from running.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#disable_webhooks DataHelmTemplate#disable_webhooks}
        '''
        result = self._values.get("disable_webhooks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_crds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Include CRDs in the templated output.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#include_crds DataHelmTemplate#include_crds}
        '''
        result = self._values.get("include_crds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set .Release.IsUpgrade instead of .Release.IsInstall.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#is_upgrade DataHelmTemplate#is_upgrade}
        '''
        result = self._values.get("is_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def keyring(self) -> typing.Optional[builtins.str]:
        '''Location of public keys used for verification. Used only if ``verify`` is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#keyring DataHelmTemplate#keyring}
        '''
        result = self._values.get("keyring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kube_version(self) -> typing.Optional[builtins.str]:
        '''Kubernetes version used for Capabilities.KubeVersion.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#kube_version DataHelmTemplate#kube_version}
        '''
        result = self._values.get("kube_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifest(self) -> typing.Optional[builtins.str]:
        '''Concatenated rendered chart templates. This corresponds to the output of the ``helm template`` command.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#manifest DataHelmTemplate#manifest}
        '''
        result = self._values.get("manifest")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manifests(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Map of rendered chart templates indexed by the template name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#manifests DataHelmTemplate#manifests}
        '''
        result = self._values.get("manifests")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Namespace to install the release into.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#namespace DataHelmTemplate#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''Rendered notes if the chart contains a ``NOTES.txt``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#notes DataHelmTemplate#notes}
        '''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pass_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Pass credentials to all domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#pass_credentials DataHelmTemplate#pass_credentials}
        '''
        result = self._values.get("pass_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def postrender(self) -> typing.Optional["DataHelmTemplatePostrender"]:
        '''Postrender command config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#postrender DataHelmTemplate#postrender}
        '''
        result = self._values.get("postrender")
        return typing.cast(typing.Optional["DataHelmTemplatePostrender"], result)

    @builtins.property
    def render_subchart_notes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, render subchart notes along with the parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#render_subchart_notes DataHelmTemplate#render_subchart_notes}
        '''
        result = self._values.get("render_subchart_notes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replace(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Re-use the given name, even if that name is already used. This is unsafe in production.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#replace DataHelmTemplate#replace}
        '''
        result = self._values.get("replace")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''Repository where to locate the requested chart.

        If it is a URL the chart is installed without installing the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository DataHelmTemplate#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_ca_file(self) -> typing.Optional[builtins.str]:
        '''The repository's CA file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_ca_file DataHelmTemplate#repository_ca_file}
        '''
        result = self._values.get("repository_ca_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_cert_file(self) -> typing.Optional[builtins.str]:
        '''The repository's cert file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_cert_file DataHelmTemplate#repository_cert_file}
        '''
        result = self._values.get("repository_cert_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_key_file(self) -> typing.Optional[builtins.str]:
        '''The repository's cert key file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_key_file DataHelmTemplate#repository_key_file}
        '''
        result = self._values.get("repository_key_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_password(self) -> typing.Optional[builtins.str]:
        '''Password for HTTP basic authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_password DataHelmTemplate#repository_password}
        '''
        result = self._values.get("repository_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_username(self) -> typing.Optional[builtins.str]:
        '''Username for HTTP basic authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#repository_username DataHelmTemplate#repository_username}
        '''
        result = self._values.get("repository_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reset_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When upgrading, reset the values to the ones built into the chart.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#reset_values DataHelmTemplate#reset_values}
        '''
        result = self._values.get("reset_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reuse_values(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When upgrading, reuse the last release's values and merge in any overrides. If 'reset_values' is specified, this is ignored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#reuse_values DataHelmTemplate#reuse_values}
        '''
        result = self._values.get("reuse_values")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSet"]]]:
        '''Custom values to be merged with the values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set DataHelmTemplate#set}
        '''
        result = self._values.get("set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSet"]]], result)

    @builtins.property
    def set_list(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSetListStruct"]]]:
        '''Custom sensitive values to be merged with the values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set_list DataHelmTemplate#set_list}
        '''
        result = self._values.get("set_list")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSetListStruct"]]], result)

    @builtins.property
    def set_sensitive(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSetSensitive"]]]:
        '''Custom sensitive values to be merged with the values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#set_sensitive DataHelmTemplate#set_sensitive}
        '''
        result = self._values.get("set_sensitive")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataHelmTemplateSetSensitive"]]], result)

    @builtins.property
    def show_only(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Only show manifests rendered from the given templates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#show_only DataHelmTemplate#show_only}
        '''
        result = self._values.get("show_only")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_crds(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, no CRDs will be installed. By default, CRDs are installed if not already present.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#skip_crds DataHelmTemplate#skip_crds}
        '''
        result = self._values.get("skip_crds")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_tests(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set, tests will not be rendered. By default, tests are rendered.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#skip_tests DataHelmTemplate#skip_tests}
        '''
        result = self._values.get("skip_tests")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds to wait for any individual Kubernetes operation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#timeout DataHelmTemplate#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def validate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Validate your manifests against the Kubernetes cluster you are currently pointing at.

        This is the same validation performed on an install.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#validate DataHelmTemplate#validate}
        '''
        result = self._values.get("validate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of values in raw yaml format to pass to helm.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#values DataHelmTemplate#values}
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Verify the package before installing it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#verify DataHelmTemplate#verify}
        '''
        result = self._values.get("verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Specify the exact chart version to install. If this is not specified, the latest version is installed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#version DataHelmTemplate#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def wait(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Will wait until all resources are in a ready state before marking the release as successful.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#wait DataHelmTemplate#wait}
        '''
        result = self._values.get("wait")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataHelmTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplatePostrender",
    jsii_struct_bases=[],
    name_mapping={"binary_path": "binaryPath", "args": "args"},
)
class DataHelmTemplatePostrender:
    def __init__(
        self,
        *,
        binary_path: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param binary_path: The common binary path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#binary_path DataHelmTemplate#binary_path}
        :param args: An argument to the post-renderer (can specify multiple). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#args DataHelmTemplate#args}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70be91cd9aa2015f426d7219063f388bce602de2810050ccafa37320051af63c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#binary_path DataHelmTemplate#binary_path}
        '''
        result = self._values.get("binary_path")
        assert result is not None, "Required property 'binary_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An argument to the post-renderer (can specify multiple).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#args DataHelmTemplate#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataHelmTemplatePostrender(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataHelmTemplatePostrenderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplatePostrenderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4554397f144353c7b945b3dac4bec6ed08c92a6df15578a728f8880ae05f2fe5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a75b525ae4df41600b923ef818c94bfaa7dfbb43c645c95abc9ad3e0d0cc1e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="binaryPath")
    def binary_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "binaryPath"))

    @binary_path.setter
    def binary_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b431cbe05aec69b5bca18be16f28c7ac21e7a196815ce737c4af39d74bb9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "binaryPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplatePostrender]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplatePostrender]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplatePostrender]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9cb6eb7e85a198432be9fc5b33031926998f1ff7b4ca869563506b9af08a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSet",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "value": "value"},
)
class DataHelmTemplateSet:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#type DataHelmTemplate#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#value DataHelmTemplate#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3107b5c6b8ed11069788d0b3982cf940428ac686b9fd0f5a29597828bbe5aba)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#type DataHelmTemplate#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#value DataHelmTemplate#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataHelmTemplateSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataHelmTemplateSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f05d1a68c1569bc805b0568fdf6ee57a5a01059865d8a7a3e017f5ce462b3849)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataHelmTemplateSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ecdc5d10f383195dfeb7d28ceaa71eb0eeaffa72e74e1880cf507958133281d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataHelmTemplateSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc947c554147a1493bd53dc9fc3f3df61595d54a303b403fd23c7d2a8f09674)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98017851a0fdf54d488ce61b4da685a83e3b0f9c85e2f501976c9e7e77d44954)
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
            type_hints = typing.get_type_hints(_typecheckingstub__043b3e376e90aab6591fc46043e5d243b8c68bf2a618e467b6fd887864da6cb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf344d6c6d0e3525c45613e9e9c9965817a9ba5bb8aed4c70d3540465ef70091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSetListStruct",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "name": "name"},
)
class DataHelmTemplateSetListStruct:
    def __init__(
        self,
        *,
        value: typing.Sequence[builtins.str],
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#value DataHelmTemplate#value}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d42fdc9606495bede7f237b1a9e802de94a71f69efe80fb8c3c065efb2a78e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def value(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#value DataHelmTemplate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataHelmTemplateSetListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataHelmTemplateSetListStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSetListStructList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c363647b7b98dfae6dea3ed064fbfa5264274ebaf6e903622ffc027360ea3544)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataHelmTemplateSetListStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111974b475103fe7263ddd63889c3425d455b3fae17109a52dac9ee49ca4fdad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataHelmTemplateSetListStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829c4840c317628f43c98379b5fd3534134d14c21df00c6440bd8d2d68982960)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf08e2cbe2cd3689c4eaac91c7ac6d230fd074d10abd18bcaebbc9a73aa51e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23b597ab3b077d8d80833c8eb6f4622c8eeca04f5a97d4fa747c9f8eed3db6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSetListStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSetListStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSetListStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32eba4071b0428b766594486a632f82776cb86fdc6e225d1dc14913219b87ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataHelmTemplateSetListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSetListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b7db2d482e68961af0c9cb75a431d5c8af5d05104f3dc5c9f4b781e406049f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1990dfb0da6441db22ccdd38a4717adf36677d6fbd7604abf876c197334ac2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "value"))

    @value.setter
    def value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7434adba18796e6e7a12046632543f0d36a73f9acbb17b92042523a6e0aa2d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSetListStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSetListStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSetListStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a875cebe0e855ea618c6d23bbe957d7ba99677452ebd01ba71079ff1d9bd1485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataHelmTemplateSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdc6b11db958720bcf5c5e86250bc1a0ac99593b88ac8aaf121c720790e61556)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e99d09698a19fbb5a235d0cafb477a7253396bad35838712d63540a205d2b3e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a294c5d5a17d9d01782ce05462f8e53698dcc7c079890c5cfc280023cbb8234f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9306382949238fef932126e96e0e7d62dda40092082ed876fb610ea1878fa1a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d468251f4b033928b835105345d1ff389b4ace9d8bce3dd2969163e19a3f183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSetSensitive",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "type": "type"},
)
class DataHelmTemplateSetSensitive:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#value DataHelmTemplate#value}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#type DataHelmTemplate#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b14c003c1e72c0f94da94190926ba8230219d5f38b620f88ba7e9b01fe40ad2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#name DataHelmTemplate#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#value DataHelmTemplate#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/helm/3.0.2/docs/data-sources/template#type DataHelmTemplate#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataHelmTemplateSetSensitive(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataHelmTemplateSetSensitiveList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSetSensitiveList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e0761418151b0fca8b2e95abff26cd0aef9cdb3812ff808e5404facba85ffa1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataHelmTemplateSetSensitiveOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2a0de4adc73ff98d603b3994ea98fe58493203b1b79b224e65c271166819c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataHelmTemplateSetSensitiveOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a630c3f64c4c8a16703d8e630452274dc55da1c92f92456bb90075ea23afa3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff68228563a4bdd73fea664e6716c2039c6fbcfa695416f0303eaa39faae1d93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ca75bdbb804abea2b60a0ae7aa7cfd2f323c341890429828851e11da06326ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSetSensitive]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSetSensitive]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSetSensitive]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6c6bd265ba0168f43d365076d0db131ef06963950177843a2d6d49f35bb1f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataHelmTemplateSetSensitiveOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-helm.dataHelmTemplate.DataHelmTemplateSetSensitiveOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80e166f4661db2c555588eda40249032ca14c79cce334882ff5ca7961a6e657a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__611e7e80c5460f5ba67c04155cb6d411d3a8ab0ef7d2315ed0a34692c3a5364a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9dd539af94bdc39f4e7a346797d5f0cbb88468c17cc2aa7fd26854c0227ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53182084eee793437d53c8b575c074723467e71c84378b73712a9938724ddc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSetSensitive]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSetSensitive]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSetSensitive]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e01d43a7feee6700d446c94bc7e19ad1d29fd1923a380820ed5822d642e306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataHelmTemplate",
    "DataHelmTemplateConfig",
    "DataHelmTemplatePostrender",
    "DataHelmTemplatePostrenderOutputReference",
    "DataHelmTemplateSet",
    "DataHelmTemplateSetList",
    "DataHelmTemplateSetListStruct",
    "DataHelmTemplateSetListStructList",
    "DataHelmTemplateSetListStructOutputReference",
    "DataHelmTemplateSetOutputReference",
    "DataHelmTemplateSetSensitive",
    "DataHelmTemplateSetSensitiveList",
    "DataHelmTemplateSetSensitiveOutputReference",
]

publication.publish()

def _typecheckingstub__58c1e559d09940a986fee4320c6ad4564aaeb41d7bed779451d692fbc4050767(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    chart: builtins.str,
    name: builtins.str,
    api_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    atomic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crds: typing.Optional[typing.Sequence[builtins.str]] = None,
    create_namespace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dependency_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    devel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_openapi_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_webhooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keyring: typing.Optional[builtins.str] = None,
    kube_version: typing.Optional[builtins.str] = None,
    manifest: typing.Optional[builtins.str] = None,
    manifests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    pass_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    postrender: typing.Optional[typing.Union[DataHelmTemplatePostrender, typing.Dict[builtins.str, typing.Any]]] = None,
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
    set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSetListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_sensitive: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSetSensitive, typing.Dict[builtins.str, typing.Any]]]]] = None,
    show_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_tests: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version: typing.Optional[builtins.str] = None,
    wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__9ea480acf4a220b3d6ba7a7f3ea415b79d6952d6947a59a54d20a41bab385994(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1596ab16b5d874b157172d384e60dca3a78047fbd42fa1f5b63eee3f239c3aab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152cb09b5fbfc57dbe53841927f1ffb77aaf7ba9a73e8477e7ab141afc3b3863(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSetListStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f695897482a9ad07999645b33f485ea7dc3b43747d170cf346beb84d2ac5ea3c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSetSensitive, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eeac916cbbd1662c42211628356d464808cf3ef903532ac24ffd8c4a96aa0c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df81e6585e117067b993a67e46effaf0487be8735e62ccd7f9fed59b5ca071f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6506552dd450214ce11c34372b7d04f8b22cadb8999c6ec94f48fb35b050151f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92799c956fb68e40124d5e9ee07cf0d246bef3a575daa81524655178f1838cd0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff07092ae1a03d78b487ed26f127abc4ccd400f01f237d4b407ddf9380278b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c117039ddb8d257c128a704d89f4116fa98acb4b10a4aef1ebfc39e58d1e9ba1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc31f5fa9f8444a09f9828975d593887ab442a05a362b03024ddd9b096a6ced2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f7dccf8dab54c2ce18cc3915f5ee2e4134b8a412dc1184e58a646fe009c21e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a561075e6def8561f9192061f83c3c1a19e41984787a623698101dfb387cf88b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df1f588c7368bc9b6c4691f13f4e3f50607c57bad1598c478eb08f4969fabad5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474986d6384bac6fff89d9a17ed843098e1a2ee9ed19fad1f2b5799ed6e3f498(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c876c95d429cecfd3d1d3b79538645811b0c738a6eb2f5f313b1ff65ced239b0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15aa9486bc32e3b05999c435379c9e9b1a6475c1ac67a6f2b1a42b7215d6f463(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b4c485adfd4740822f5eb93853551d25323c58aca9d610a80ee864bc55eaea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934b57dac3797675e0e93cbbd9fa63ec9df2dc9562ea3f665b52906f6e29fda5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50b7a44fe4cac624cc3dcf8e4465799c4a108779bf6dc1069e8781e5b3700d7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d925d1717bd13650969af356184f9101564c0ec716ce0c08e91bb91197c3e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828e7e50f014ebcf2901a0beb9f6266c5052361244b42cd27acff9a81a5ca1fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6feec32869e9f991c74424c94f31d08cebc0f5e209d83fe70e563e3231b196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd6108ac52691e48955544b60dc1e67203d89e17ac3786655eb4ac03fac6ef0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ba0ec2d71ad524f243f9dd6f7766d4b6da6b836696c2681ebc0c30399641eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a06d09a60cb9e5e636ecef40d21710b43005729b5731a986135afcad3ff7d0f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3d74aa62fcc91f5ed0822e42a62099c592aac40791eb11ac1aeaa6d343cef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0694b150e35bcf52fa174f7bb11ba6ad80bec209630e0d8bb3b4b5a62f7243e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefceb2b14c698f4958703951b5e11f816aa2a33f34521561a6a388febe6dacb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4353b4a969115f738a3bd7848c874a398c7e39ccd05e75d4863e7f87ab614c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55cb7797dfc89be7681ae685752c40d032105c88a5478bb8abc790e074ddf81d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c1c3633aeba7bab0170c109f3fa61f138e6b782a74b235ee0f603e3353ecca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bcb2065a03b1694c05f12bc91f6b1f91025c75d2fe8063f8152d1394c60ab9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5bd289f49d9780b27a6f6641fc91534bf4b87c3c3448a1f515b33e8596d45a3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be9760942c024e63a6847d679b7a00ffc6e035b4438b6f459f9a4df75143f83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3feb8f7119901ebd885e214f90cf39318d7ff2f6999d56ee62c669ac918b74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539af9fbb9464df441f0e337716e48fbfaf952dcc8eadcab06f32c706e06d46c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf898eb8e953048800ae779d726623c46efce3d7cc84ed768a235f03031c93d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32e337eb6fe1028fad504a177ae3d58fd62758e0090e7d2ba10829e043f62c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eef9b7e6247487f07d45ec5438bec423d8e0a19dd5829f0fc47f9e5444666db(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb18010aa70ac67269f67e5b12a5c1dd1874fa66431cb3c6da626e29787f4ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480b78869a6effed1519d46b4a83794a4c8e0ccdc61a05e6829e5f36b19f13be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc948d679872e9bbd9ff27f3d13ab8bf94ea9643cffa6864f73cfb76b6b586e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa661fc2bc6a52eec136c130260e43e15fe67a8017a94efddda364fd2b2f33d2(
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
    api_versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    atomic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    crds: typing.Optional[typing.Sequence[builtins.str]] = None,
    create_namespace: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dependency_update: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    devel: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_openapi_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_webhooks: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    keyring: typing.Optional[builtins.str] = None,
    kube_version: typing.Optional[builtins.str] = None,
    manifest: typing.Optional[builtins.str] = None,
    manifests: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    pass_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    postrender: typing.Optional[typing.Union[DataHelmTemplatePostrender, typing.Dict[builtins.str, typing.Any]]] = None,
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
    set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_list: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSetListStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    set_sensitive: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataHelmTemplateSetSensitive, typing.Dict[builtins.str, typing.Any]]]]] = None,
    show_only: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_crds: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_tests: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    validate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version: typing.Optional[builtins.str] = None,
    wait: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70be91cd9aa2015f426d7219063f388bce602de2810050ccafa37320051af63c(
    *,
    binary_path: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4554397f144353c7b945b3dac4bec6ed08c92a6df15578a728f8880ae05f2fe5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75b525ae4df41600b923ef818c94bfaa7dfbb43c645c95abc9ad3e0d0cc1e8c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b431cbe05aec69b5bca18be16f28c7ac21e7a196815ce737c4af39d74bb9dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9cb6eb7e85a198432be9fc5b33031926998f1ff7b4ca869563506b9af08a84(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplatePostrender]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3107b5c6b8ed11069788d0b3982cf940428ac686b9fd0f5a29597828bbe5aba(
    *,
    name: builtins.str,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05d1a68c1569bc805b0568fdf6ee57a5a01059865d8a7a3e017f5ce462b3849(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecdc5d10f383195dfeb7d28ceaa71eb0eeaffa72e74e1880cf507958133281d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc947c554147a1493bd53dc9fc3f3df61595d54a303b403fd23c7d2a8f09674(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98017851a0fdf54d488ce61b4da685a83e3b0f9c85e2f501976c9e7e77d44954(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043b3e376e90aab6591fc46043e5d243b8c68bf2a618e467b6fd887864da6cb1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf344d6c6d0e3525c45613e9e9c9965817a9ba5bb8aed4c70d3540465ef70091(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d42fdc9606495bede7f237b1a9e802de94a71f69efe80fb8c3c065efb2a78e0(
    *,
    value: typing.Sequence[builtins.str],
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c363647b7b98dfae6dea3ed064fbfa5264274ebaf6e903622ffc027360ea3544(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111974b475103fe7263ddd63889c3425d455b3fae17109a52dac9ee49ca4fdad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829c4840c317628f43c98379b5fd3534134d14c21df00c6440bd8d2d68982960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf08e2cbe2cd3689c4eaac91c7ac6d230fd074d10abd18bcaebbc9a73aa51e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b597ab3b077d8d80833c8eb6f4622c8eeca04f5a97d4fa747c9f8eed3db6bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32eba4071b0428b766594486a632f82776cb86fdc6e225d1dc14913219b87ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSetListStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7db2d482e68961af0c9cb75a431d5c8af5d05104f3dc5c9f4b781e406049f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1990dfb0da6441db22ccdd38a4717adf36677d6fbd7604abf876c197334ac2ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7434adba18796e6e7a12046632543f0d36a73f9acbb17b92042523a6e0aa2d09(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a875cebe0e855ea618c6d23bbe957d7ba99677452ebd01ba71079ff1d9bd1485(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSetListStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc6b11db958720bcf5c5e86250bc1a0ac99593b88ac8aaf121c720790e61556(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99d09698a19fbb5a235d0cafb477a7253396bad35838712d63540a205d2b3e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a294c5d5a17d9d01782ce05462f8e53698dcc7c079890c5cfc280023cbb8234f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9306382949238fef932126e96e0e7d62dda40092082ed876fb610ea1878fa1a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d468251f4b033928b835105345d1ff389b4ace9d8bce3dd2969163e19a3f183(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b14c003c1e72c0f94da94190926ba8230219d5f38b620f88ba7e9b01fe40ad2(
    *,
    name: builtins.str,
    value: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0761418151b0fca8b2e95abff26cd0aef9cdb3812ff808e5404facba85ffa1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2a0de4adc73ff98d603b3994ea98fe58493203b1b79b224e65c271166819c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a630c3f64c4c8a16703d8e630452274dc55da1c92f92456bb90075ea23afa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff68228563a4bdd73fea664e6716c2039c6fbcfa695416f0303eaa39faae1d93(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca75bdbb804abea2b60a0ae7aa7cfd2f323c341890429828851e11da06326ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6c6bd265ba0168f43d365076d0db131ef06963950177843a2d6d49f35bb1f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataHelmTemplateSetSensitive]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e166f4661db2c555588eda40249032ca14c79cce334882ff5ca7961a6e657a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611e7e80c5460f5ba67c04155cb6d411d3a8ab0ef7d2315ed0a34692c3a5364a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9dd539af94bdc39f4e7a346797d5f0cbb88468c17cc2aa7fd26854c0227ec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53182084eee793437d53c8b575c074723467e71c84378b73712a9938724ddc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e01d43a7feee6700d446c94bc7e19ad1d29fd1923a380820ed5822d642e306(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataHelmTemplateSetSensitive]],
) -> None:
    """Type checking stubs"""
    pass
