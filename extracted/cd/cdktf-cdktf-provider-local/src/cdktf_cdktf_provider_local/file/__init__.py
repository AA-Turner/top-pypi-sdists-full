r'''
# `local_file`

Refer to the Terraform Registry for docs: [`local_file`](https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file).
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


class File(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-local.file.File",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file local_file}.'''

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
        sensitive_content: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file local_file} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filename: The path to the file that will be created. Missing parent directories will be created. If the file already exists, it will be overridden with the given content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#filename File#filename}
        :param content: Content to store in the file, expected to be a UTF-8 encoded string. Conflicts with ``sensitive_content``, ``content_base64`` and ``source``. Exactly one of these four arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#content File#content}
        :param content_base64: Content to store in the file, expected to be binary encoded as base64 string. Conflicts with ``content``, ``sensitive_content`` and ``source``. Exactly one of these four arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#content_base64 File#content_base64}
        :param directory_permission: Permissions to set for directories created (before umask), expressed as string in `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_. Default value is ``"0777"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#directory_permission File#directory_permission}
        :param file_permission: Permissions to set for the output file (before umask), expressed as string in `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_. Default value is ``"0777"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#file_permission File#file_permission}
        :param sensitive_content: Sensitive content to store in the file, expected to be an UTF-8 encoded string. Will not be displayed in diffs. Conflicts with ``content``, ``content_base64`` and ``source``. Exactly one of these four arguments must be specified. If in need to use *sensitive* content, please use the ```local_sensitive_file`` <./sensitive_file.html>`_ resource instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#sensitive_content File#sensitive_content}
        :param source: Path to file to use as source for the one we are creating. Conflicts with ``content``, ``sensitive_content`` and ``content_base64``. Exactly one of these four arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#source File#source}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66ab1dc34f86592d17bdb4b272a9c6d2646b51db2ff365f978dcd76d2bd5ccd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = FileConfig(
            filename=filename,
            content=content,
            content_base64=content_base64,
            directory_permission=directory_permission,
            file_permission=file_permission,
            sensitive_content=sensitive_content,
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
        '''Generates CDKTF code for importing a File resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the File to import.
        :param import_from_id: The id of the existing File that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the File to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76b6fd7762b83169518709a190f5e8b5c4cdb70136d14e477a5a533dc6aadd41)
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

    @jsii.member(jsii_name="resetSensitiveContent")
    def reset_sensitive_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitiveContent", []))

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
    @jsii.member(jsii_name="sensitiveContentInput")
    def sensitive_content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sensitiveContentInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__182307dbc71a79defe23a59bd343694949e9ab474522506f5812dd2d0653e03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentBase64")
    def content_base64(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentBase64"))

    @content_base64.setter
    def content_base64(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e215b9d949760203d34707a68d37521a64558be7ea0fefc1b5ba7fee7be0b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentBase64", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryPermission")
    def directory_permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryPermission"))

    @directory_permission.setter
    def directory_permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3010b9640cb280bad5c829245a4b6dcdb461e83f4e72dc93251cebc129c35a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryPermission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a64fd4f712c09d9a59b5f4cdc9fdb33ec5954c5473799a93e8c9c123992f14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filePermission")
    def file_permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filePermission"))

    @file_permission.setter
    def file_permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746d608aaf033e2f5f016b570bc52971e40fade486a768663bfa82861f5bd3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filePermission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sensitiveContent")
    def sensitive_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sensitiveContent"))

    @sensitive_content.setter
    def sensitive_content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931857547b6bd56ab094f72cbc9ec55cf2b8cd3ff6e9d0847a0677f652885add)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sensitiveContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c71f01a2965e3a83cc884e4eb0dc0abc9ae8ee20a84f0e042296147af14afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-local.file.FileConfig",
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
        "sensitive_content": "sensitiveContent",
        "source": "source",
    },
)
class FileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        sensitive_content: typing.Optional[builtins.str] = None,
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
        :param filename: The path to the file that will be created. Missing parent directories will be created. If the file already exists, it will be overridden with the given content. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#filename File#filename}
        :param content: Content to store in the file, expected to be a UTF-8 encoded string. Conflicts with ``sensitive_content``, ``content_base64`` and ``source``. Exactly one of these four arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#content File#content}
        :param content_base64: Content to store in the file, expected to be binary encoded as base64 string. Conflicts with ``content``, ``sensitive_content`` and ``source``. Exactly one of these four arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#content_base64 File#content_base64}
        :param directory_permission: Permissions to set for directories created (before umask), expressed as string in `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_. Default value is ``"0777"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#directory_permission File#directory_permission}
        :param file_permission: Permissions to set for the output file (before umask), expressed as string in `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_. Default value is ``"0777"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#file_permission File#file_permission}
        :param sensitive_content: Sensitive content to store in the file, expected to be an UTF-8 encoded string. Will not be displayed in diffs. Conflicts with ``content``, ``content_base64`` and ``source``. Exactly one of these four arguments must be specified. If in need to use *sensitive* content, please use the ```local_sensitive_file`` <./sensitive_file.html>`_ resource instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#sensitive_content File#sensitive_content}
        :param source: Path to file to use as source for the one we are creating. Conflicts with ``content``, ``sensitive_content`` and ``content_base64``. Exactly one of these four arguments must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#source File#source}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2096116de66f92c58057bacda7e9d95a3670b45b8d98520953ca363dc7fd950b)
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
            check_type(argname="argument sensitive_content", value=sensitive_content, expected_type=type_hints["sensitive_content"])
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
        if sensitive_content is not None:
            self._values["sensitive_content"] = sensitive_content
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#filename File#filename}
        '''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''Content to store in the file, expected to be a UTF-8 encoded string.

        Conflicts with ``sensitive_content``, ``content_base64`` and ``source``.
        Exactly one of these four arguments must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#content File#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_base64(self) -> typing.Optional[builtins.str]:
        '''Content to store in the file, expected to be binary encoded as base64 string.

        Conflicts with ``content``, ``sensitive_content`` and ``source``.
        Exactly one of these four arguments must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#content_base64 File#content_base64}
        '''
        result = self._values.get("content_base64")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_permission(self) -> typing.Optional[builtins.str]:
        '''Permissions to set for directories created (before umask), expressed as string in  `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_.  Default value is ``"0777"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#directory_permission File#directory_permission}
        '''
        result = self._values.get("directory_permission")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_permission(self) -> typing.Optional[builtins.str]:
        '''Permissions to set for the output file (before umask), expressed as string in  `numeric notation <https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation>`_.  Default value is ``"0777"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#file_permission File#file_permission}
        '''
        result = self._values.get("file_permission")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sensitive_content(self) -> typing.Optional[builtins.str]:
        '''Sensitive content to store in the file, expected to be an UTF-8 encoded string.

        Will not be displayed in diffs.
        Conflicts with ``content``, ``content_base64`` and ``source``.
        Exactly one of these four arguments must be specified.
        If in need to use *sensitive* content, please use the ```local_sensitive_file`` <./sensitive_file.html>`_
        resource instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#sensitive_content File#sensitive_content}
        '''
        result = self._values.get("sensitive_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Path to file to use as source for the one we are creating.

        Conflicts with ``content``, ``sensitive_content`` and ``content_base64``.
        Exactly one of these four arguments must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/local/2.5.2/docs/resources/file#source File#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "File",
    "FileConfig",
]

publication.publish()

def _typecheckingstub__e66ab1dc34f86592d17bdb4b272a9c6d2646b51db2ff365f978dcd76d2bd5ccd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    filename: builtins.str,
    content: typing.Optional[builtins.str] = None,
    content_base64: typing.Optional[builtins.str] = None,
    directory_permission: typing.Optional[builtins.str] = None,
    file_permission: typing.Optional[builtins.str] = None,
    sensitive_content: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__76b6fd7762b83169518709a190f5e8b5c4cdb70136d14e477a5a533dc6aadd41(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182307dbc71a79defe23a59bd343694949e9ab474522506f5812dd2d0653e03d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e215b9d949760203d34707a68d37521a64558be7ea0fefc1b5ba7fee7be0b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3010b9640cb280bad5c829245a4b6dcdb461e83f4e72dc93251cebc129c35a21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a64fd4f712c09d9a59b5f4cdc9fdb33ec5954c5473799a93e8c9c123992f14c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746d608aaf033e2f5f016b570bc52971e40fade486a768663bfa82861f5bd3b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931857547b6bd56ab094f72cbc9ec55cf2b8cd3ff6e9d0847a0677f652885add(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c71f01a2965e3a83cc884e4eb0dc0abc9ae8ee20a84f0e042296147af14afe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2096116de66f92c58057bacda7e9d95a3670b45b8d98520953ca363dc7fd950b(
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
    sensitive_content: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
