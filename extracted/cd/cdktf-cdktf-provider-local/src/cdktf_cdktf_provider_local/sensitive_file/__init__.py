r'''
# `local_sensitive_file`

Refer to the Terraform Registry for docs: [`local_sensitive_file`](https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file).
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


class SensitiveFile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-local.sensitiveFile.SensitiveFile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file local_sensitive_file}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        filename: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_base64: typing.Optional[builtins.str] = None,
        directory_permission: typing.Optional[builtins.str] = None,
        file_permission: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file local_sensitive_file} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filename: The path to the file that will be created. Missing parent directories will be created. If the file already exists, it will be overridden with the given content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#filename SensitiveFile#filename}
        :param content: Sensitive Content to store in the file, expected to be a UTF-8 encoded string. Conflicts with ``content_base64`` and ``source``. Exactly one of these three arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#content SensitiveFile#content}
        :param content_base64: Sensitive Content to store in the file, expected to be binary encoded as base64 string. Conflicts with ``content`` and ``source``. Exactly one of these three arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#content_base64 SensitiveFile#content_base64}
        :param directory_permission: Permissions to set for directories created (before umask), expressed as string in `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_. Default value is ``"0700"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#directory_permission SensitiveFile#directory_permission}
        :param file_permission: Permissions to set for the output file (before umask), expressed as string in `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_. Default value is ``"0700"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#file_permission SensitiveFile#file_permission}
        :param source: Path to file to use as source for the one we are creating. Conflicts with ``content`` and ``content_base64``. Exactly one of these three arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#source SensitiveFile#source}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553efe008f84aac2715e71038c1006401b728780ed6d0725934afd85c76053c1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = SensitiveFileConfig(
            filename=filename,
            content=content,
            content_base64=content_base64,
            directory_permission=directory_permission,
            file_permission=file_permission,
            source=source,
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
        '''Generates CDKTF code for importing a SensitiveFile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SensitiveFile to import.
        :param import_from_id: The id of the existing SensitiveFile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SensitiveFile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7eda7d9ff1e18a926df3a1868b556f1dc91f28f2936f42844cbcc0135feb6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetContentBase64")
    def reset_content_base64(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentBase64", []))

    @jsii.member(jsii_name="resetDirectoryPermission")
    def reset_directory_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryPermission", []))

    @jsii.member(jsii_name="resetFilePermission")
    def reset_file_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePermission", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

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
    @jsii.member(jsii_name="contentBase64Sha256")
    def content_base64_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentBase64Sha256"))

    @builtins.property
    @jsii.member(jsii_name="contentBase64Sha512")
    def content_base64_sha512(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentBase64Sha512"))

    @builtins.property
    @jsii.member(jsii_name="contentMd5")
    def content_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentMd5"))

    @builtins.property
    @jsii.member(jsii_name="contentSha1")
    def content_sha1(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentSha1"))

    @builtins.property
    @jsii.member(jsii_name="contentSha256")
    def content_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentSha256"))

    @builtins.property
    @jsii.member(jsii_name="contentSha512")
    def content_sha512(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentSha512"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="contentBase64Input")
    def content_base64_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentBase64Input"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryPermissionInput")
    def directory_permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="filePermissionInput")
    def file_permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filePermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692edd5b833148aa8633811d469321f9c3259d56abd08631a29ddd4b324f3216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentBase64")
    def content_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentBase64"))

    @content_base64.setter
    def content_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ecfcf919ae78e57fbfe12d7692c1456830045732520fb67d62d2f9364f409c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryPermission")
    def directory_permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryPermission"))

    @directory_permission.setter
    def directory_permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ce65a035b65ffc5cc4d13846cd11c1ef5c95cad906ba19443919e0d8e3420e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryPermission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae90c02c7e90394953083b911a010f5ccdece45e3d207ca4abbb79c09a4445a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filePermission")
    def file_permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePermission"))

    @file_permission.setter
    def file_permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1872478c5deb2db3d00eb1af26ed9731ca0b37ab3499a229b8bc49bb7acf88c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePermission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b717b66e4e229cdc8003a07f6bbb0abe3a88f563912860ffcce64648e031342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-local.sensitiveFile.SensitiveFileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filename": "filename",
        "content": "content",
        "content_base64": "contentBase64",
        "directory_permission": "directoryPermission",
        "file_permission": "filePermission",
        "source": "source",
    },
)
class SensitiveFileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filename: builtins.str,
        content: typing.Optional[builtins.str] = None,
        content_base64: typing.Optional[builtins.str] = None,
        directory_permission: typing.Optional[builtins.str] = None,
        file_permission: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filename: The path to the file that will be created. Missing parent directories will be created. If the file already exists, it will be overridden with the given content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#filename SensitiveFile#filename}
        :param content: Sensitive Content to store in the file, expected to be a UTF-8 encoded string. Conflicts with ``content_base64`` and ``source``. Exactly one of these three arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#content SensitiveFile#content}
        :param content_base64: Sensitive Content to store in the file, expected to be binary encoded as base64 string. Conflicts with ``content`` and ``source``. Exactly one of these three arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#content_base64 SensitiveFile#content_base64}
        :param directory_permission: Permissions to set for directories created (before umask), expressed as string in `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_. Default value is ``"0700"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#directory_permission SensitiveFile#directory_permission}
        :param file_permission: Permissions to set for the output file (before umask), expressed as string in `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_. Default value is ``"0700"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#file_permission SensitiveFile#file_permission}
        :param source: Path to file to use as source for the one we are creating. Conflicts with ``content`` and ``content_base64``. Exactly one of these three arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#source SensitiveFile#source}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb87d8e0300782880f73b41d51c4661b03af412eae6624965aecdac9117a804a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_base64", value=content_base64, expected_type=type_hints["content_base64"])
            check_type(argname="argument directory_permission", value=directory_permission, expected_type=type_hints["directory_permission"])
            check_type(argname="argument file_permission", value=file_permission, expected_type=type_hints["file_permission"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filename": filename,
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
        if content is not None:
            self._values["content"] = content
        if content_base64 is not None:
            self._values["content_base64"] = content_base64
        if directory_permission is not None:
            self._values["directory_permission"] = directory_permission
        if file_permission is not None:
            self._values["file_permission"] = file_permission
        if source is not None:
            self._values["source"] = source

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
    def filename(self) -> builtins.str:
        '''The path to the file that will be created.

        Missing parent directories will be created.
        If the file already exists, it will be overridden with the given content.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#filename SensitiveFile#filename}
        '''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Sensitive Content to store in the file, expected to be a UTF-8 encoded string.

        Conflicts with ``content_base64`` and ``source``.
        Exactly one of these three arguments must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#content SensitiveFile#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_base64(self) -> typing.Optional[builtins.str]:
        '''Sensitive Content to store in the file, expected to be binary encoded as base64 string.

        Conflicts with ``content`` and ``source``.
        Exactly one of these three arguments must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#content_base64 SensitiveFile#content_base64}
        '''
        result = self._values.get("content_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_permission(self) -> typing.Optional[builtins.str]:
        '''Permissions to set for directories created (before umask), expressed as string in  `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_.  Default value is ``"0700"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#directory_permission SensitiveFile#directory_permission}
        '''
        result = self._values.get("directory_permission")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_permission(self) -> typing.Optional[builtins.str]:
        '''Permissions to set for the output file (before umask), expressed as string in  `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_.  Default value is ``"0700"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#file_permission SensitiveFile#file_permission}
        '''
        result = self._values.get("file_permission")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Path to file to use as source for the one we are creating.

        Conflicts with ``content`` and ``content_base64``.
        Exactly one of these three arguments must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/sensitive_file#source SensitiveFile#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SensitiveFileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SensitiveFile",
    "SensitiveFileConfig",
]

publication.publish()

def _typecheckingstub__553efe008f84aac2715e71038c1006401b728780ed6d0725934afd85c76053c1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    filename: builtins.str,
    content: typing.Optional[builtins.str] = None,
    content_base64: typing.Optional[builtins.str] = None,
    directory_permission: typing.Optional[builtins.str] = None,
    file_permission: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ce7eda7d9ff1e18a926df3a1868b556f1dc91f28f2936f42844cbcc0135feb6f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692edd5b833148aa8633811d469321f9c3259d56abd08631a29ddd4b324f3216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ecfcf919ae78e57fbfe12d7692c1456830045732520fb67d62d2f9364f409c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ce65a035b65ffc5cc4d13846cd11c1ef5c95cad906ba19443919e0d8e3420e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae90c02c7e90394953083b911a010f5ccdece45e3d207ca4abbb79c09a4445a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1872478c5deb2db3d00eb1af26ed9731ca0b37ab3499a229b8bc49bb7acf88c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b717b66e4e229cdc8003a07f6bbb0abe3a88f563912860ffcce64648e031342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb87d8e0300782880f73b41d51c4661b03af412eae6624965aecdac9117a804a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filename: builtins.str,
    content: typing.Optional[builtins.str] = None,
    content_base64: typing.Optional[builtins.str] = None,
    directory_permission: typing.Optional[builtins.str] = None,
    file_permission: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
